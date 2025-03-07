# plugins/forwarder.py
import asyncio
import re
import pytz
from datetime import datetime
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import random
from bot import mrsyd
from asyncio import Semaphore
from telethon import events
from pyrogram.types import Message

#from info import SOURCE_CHAT_ID

# Semaphore to limit concurrent forwards (adjust as needed)
semaphore = Semaphore(2)
DESTINATION_CHATS = [-1002433450358, -1002464733363]
SOURCE_CHATS = [-1002295881345, -1002281540615, 1983814301, -1001780243928, -1002274015746, -1001862599580, -1002077435396]


@mrsyd.on(events.NewMessage(chats=SOURCE_CHATS, func=lambda e: e.message.media and (e.message.video or e.message.document)))
async def forward_if_allowed(event):
    """Forom destination chat."""
    message = event.message
    async with semaphore:
        try:
            DESTINATION_CHAT_ID = random.choice(DESTINATION_CHATS)
            await event.client.forward_messages(DESTINATION_CHAT_ID, message)
            print(f"✅ Message {message.id} forwarded successfully.")
            await asyncio.sleep(320)

        except Exception as e:
            print(f"❌ Message {message.id} {e}")

@mrsyd.on(events.NewMessage(from_users=1733124290))
async def handle_new_source(event):
    """Handles input, sets source chat & forwards messages within range if allowed."""
    
    message_text = event.message.text.strip()
    
    # Ensure correct input format: "-100XXXX YYYY ZZZZ"
    parts = message_text.split()
    if len(parts) == 3 and parts[0].startswith("-100") and parts[0][4:].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        source_chat = int(parts[0])  # Extract source chat ID
        start_msg_id = int(parts[1])  # First message ID to forward
        end_msg_id = int(parts[2])  # Last message ID to forward

        await event.respond(f"✅ Forwarding from `{source_chat}` | `{start_msg_id}` ➝ `{end_msg_id}`")
        print(f"User {event.sender_id} set source chat {source_chat} from {start_msg_id} to {end_msg_id}")

        # Fetch and forward messages within the range
        async with semaphore:
            for msg_id in range(start_msg_id, end_msg_id + 1):
                try:
                    DESTINATION_CHAT_ID = random.choice(DESTINATION_CHATS)
                    message = await event.client.get_messages(source_chat, ids=msg_id)
                    if message:  # Ensure message exists
                        if not message.forwards:  # Check if forwarding is allowed
                            print(f"❌ Message {msg_id} is restricted. Skipping.")
                            continue

                        print(f"📤 Forwarding message {msg_id} from {source_chat}...")
                        await event.client.send_message(-1002398194127, message)
                        print(f"✅ Message {msg_id} forwarded successfully!")
                        await asyncio.sleep(300)  # Small delay to avoid spam
                    else:
                        print(f"No ⚡ Message {msg_id} does not exist. Skipping.")

                except Exception as e:
                    print(f"⚠️ Error forwarding message {msg_id}: {e}")

    else:
        await event.respond("❌ Invalid format! Use: `-100XXXX YYYY ZZZZ` (Source Chat, Start ID, End ID)")


@mrsyd.on(events.NewMessage(from_users=[1983814301, 7755788244], pattern=r"^🔍 Results for your Search"))
async def handle_message(event):
    """Press each button repeatedly every 15 seconds until a new message arrives, 
    then move to the next button. Skips '⬅️ BACK' but ensures 'NEXT' is clicked last.
    """
    async with semaphore:
        message = event.message
        chat_id = message.chat_id
        message_id = message.id  # Track the same message ID

        if not message.buttons:
            return  # Exit if no buttons are present

        while True:
            # Extract buttons and filter out "⬅️ BACK"
            buttons = [(i, j, button) for i, row in enumerate(message.buttons) for j, button in enumerate(row)
                       if button.text != "⬅️ BACK"]

            next_button = None  # Store "NEXT" button separately

            for row_idx, col_idx, button in buttons:
                if button.text.startswith(" NEXT"):
                    next_button = (row_idx, col_idx, button)  # Save "NEXT" button for later
                    continue  # Skip clicking "NEXT" for now

                while True:
                    # Check if a new message has arrived
                    new_message = await event.client.get_messages(chat_id, limit=1)
                    if new_message and new_message[0].id != message_id:
                        print("New message detected, moving to next button...")
                        message_id = new_message[0].id  # Update message ID
                        message = new_message[0]  # Update message
                        break  # Move to the next button

                    try:
                        await message.click(row_idx, col_idx)  # Click button
                        print(f"Pressed: {button.text}")
                        await asyncio.sleep(15)  # 15-second delay before clicking again
                    except Exception as e:
                        print(f"Error pressing button {button.text}: {e}")
                        break  # If error occurs, move to the next button

            # If "NEXT" exists, click it and restart button processing
            if next_button:
                row_idx, col_idx, button = next_button
                try:
                    await message.click(row_idx, col_idx)  # Click "NEXT" button
                    print(f"Pressed: {button.text}, waiting for new buttons...")
                    await asyncio.sleep(8)  # Wait for new buttons to load

                    # Fetch the updated message with new buttons
                    updated_msg = await event.client.get_messages(chat_id, ids=message_id)
                    if updated_msg and updated_msg.buttons != message.buttons:
                        print("Message updated with new buttons, restarting...")
                        message = updated_msg  # Update message with new buttons
                        continue  # Restart button processing
                except Exception as e:
                    print(f"Error pressing 'NEXT': {e}")

            break  # Exit loop if no more buttons are left

        print("All buttons processed.")



@mrsyd.on(events.NewMessage(from_users=[1983814301, 7755788244], pattern=r"^❗️Join SearchBot users"))
async def handle_invite(event):
    """Click the first inline button if it's an invite link and request to join."""
    message = event.message

    if message.buttons:
        first_button = message.buttons[0][0]  # First button in the inline keyboard

        # Check if the button contains an invite link
        if first_button.url and ("t.me/" in first_button.url):
            try:
                invite_link = first_button.url

                # Check for different Telegram invite link formats
                match = re.search(r"(?:https?://)?t\.me/(?:\+|joinchat/)?([\w_-]+)", invite_link)

                if match:
                    invite_code = match.group(1)  # Extract invite hash or username
                    
                    if "+" in first_button.url or "joinchat" in first_button.url:
                        # It's an invite hash, use ImportChatInviteRequest
                        await event.client(ImportChatInviteRequest(invite_code))
                        print(f"Joined via invite link: {invite_code}")
                    else:
                        # It's a public username, use JoinChannelRequest
                        await event.client(JoinChannelRequest(invite_code))
                        print(f"Joined public channel: {invite_code}")
                else:
                    print(f"Invalid invite link format: {invite_link}")

            except Exception as e:
                print(f"Failed to join: {e}")


IST = pytz.timezone("Asia/Kolkata")  # Indian Standard Tim

@mrsyd.on(events.NewMessage(from_users=6510851298))
async def forward_mesages(event):
    async with semaphore:  # Ensures only one message is handled at a time
        await asyncio.sleep(10 * 60)  # Wait 10 minutes (1800 seconds)

        while True:
            now = datetime.now(IST).time()
            
            if now.hour >= 1 and now.hour < 7:
                await event.client.send_message(DESTINATION_ID, event.message.text)
                print(f"Forwarded message at {now}")
                break  # Stop after forwarding
            else:
                print(f"Not in forwarding time. Waiting until 1 AM IST...")
                await asyncio.sleep(1000)  # Check every 5 minutes until forwarding is allowed
