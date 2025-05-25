# plugins/forwarder.py
import asyncio
import re
import pytz
from datetime import datetime
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import random
from helper.database import db
from bot import mrsyd
from asyncio import Semaphore
from telethon import events
from pyrogram.types import Message

#from info import SOURCE_CHAT_ID

# Semaphore to limit concurrent forwards (adjust as needed)
semaphore = Semaphore(2)
semapore = asyncio.Semaphore(1)
#DESTINATION_CHAT = [-1002536001013, -1002523513653]
DESTINATION_CHATS = [-1002433450358, -1002464733363, -1002429058090]
SOURCE_CHATS = [-1002295881345, -1002525578839, 7065204410, -1002281540615, 7671667739, 1983814301, 7755788244, 8162570573, -1002588744450, 7193976370, -1001780243928, -1002274015746, -1001862599580, -1002077435396]


@mrsyd.on(events.NewMessage(chats=SOURCE_CHATS, func=lambda e: e.message.media and (e.message.video or e.message.document)))
async def forward_if_allowed(event):
    """Forom destination chat."""
    message = event.message
    async with semaphore:
        try:
            DESTINATION_CHAT_ID = random.choice(DESTINATION_CHATS)
            await event.client.forward_messages(DESTINATION_CHAT_ID, message)
            print(f"✅ Message {message.id} forwarded successfully.")
            await asyncio.sleep(120)

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
                        await asyncio.sleep(280)  # Small delay to avoid spam
                    else:
                        print(f"No ⚡ Message {msg_id} does not exist. Skipping.")

                except Exception as e:
                    print(f"⚠️ Error forwarding message {msg_id}: {e}")

    else:
        await event.respond("❌ Invalid format! Use: `-100XXXX YYYY ZZZZ` (Source Chat, Start ID, End ID)")



@mrsyd.on(events.NewMessage(from_users=[1983814301, 7755788244, 7065204410, 8162570573, 7671667739], pattern=r"^🔍 Results for your Search"))
async def handle_message(event):
    """Press each button every 60 seconds until a new message arrives, then move to the next button.
    'NEXT' is only pressed at the end, followed by a 60-second delay before fetching new buttons.
    """
    async with semaphore:  # Ensuring only one task runs at a time
        message = event.message
        chat_id = message.chat_id
        message_id = message.id
        last_processed_id = message_id  # Store the last processed message ID# Track the same message ID

        if not message.buttons:
            print("No buttons found, exiting...")
            return  # Exit if no buttons are present

        while True:
            # Extract buttons and filter out "⬅️ BACK"
            buttons = []
            next_button = None  # Store "NEXT" button separately

            for row_idx, row in enumerate(message.buttons):
                for col_idx, button in enumerate(row):
                    if button.text == "⬅️ BACK":
                        continue  # Skip "⬅️ BACK"
                    if button.text.startswith(" NEXT ["):
                        next_button = (row_idx, col_idx, button)  # Save "NEXT" button for later
                        continue  # Skip clicking "NEXT" for now
                    buttons.append((row_idx, col_idx, button))  # Store normal buttons

            if not buttons and not next_button:
                print("No clickable buttons found, exiting...")
                break  # No buttons left to process

            # Click each button one by one until a new message arrives
            for row_idx, col_idx, button in buttons:
                while True:
                    try:
                        await message.click(row_idx, col_idx)  # Click button
                        print(f"Pressed: {button.text}")

                        # Wait up to 60 seconds for a new message
                        for _ in range(60):  # Check every second for a new message
                            await asyncio.sleep(1)
                            new_message = await event.client.get_messages(chat_id, limit=1)
                            if new_message and new_message[0].id != last_processed_id:  # Store the last processed message ID
                                print("New message detected, moving to the next button...")
                                last_processed_id = new_message[0].id  # Update the last proce
                                break  # Move to the next button
                        else:
                            await asyncio.sleep(10)
                            continue  # If no new message, keep pressing the same button

                        await asyncio.sleep(60)
                        break  # Exit while loop when a new message arrives

                    except Exception as e:
                        print(f"Error pressing button {button.text}: {e}")
                        break  # If error occurs, move to the next button

            # If "NEXT" exists, press it immediately and wait 60 seconds before handling new buttons
          #  if next_button:
               # row_idx, col_idx, button = next_button
               # try:
                  #  await message.click(row_idx, col_idx)  # Click "NEXT" button
                  #  print(f"Pressed: {button.text}, waiting 60 seconds for new buttons...")
                  #  await asyncio.sleep(40)  # Full 60-second wait before checking new buttons

                    # Fetch the updated message with new buttons
                  #  updated_msg = await event.client.get_messages(chat_id, ids=message_id)
                   # if updated_msg and updated_msg.buttons != message.buttons:
                      #  print("Message updated with new buttons, restarting...")
                     #   message = updated_msg  # Update message with new buttons
                     #   continue  # Restart button processing
              #  except Exception as e:
                  #  print(f"Error pressing 'NEXT': {e}")

            break  # Exit loop if no more buttons are left

        print("All buttons processed.")



@mrsyd.on(events.NewMessage(from_users=[1983814301, 7755788244, 7065204410, 8162570573, 7671667739], pattern=r"^❗️Join SearchBot users"))
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

@mrsyd.on(events.NewMessage(from_users=6592320604))
async def forward_messs(event):
    async with semapore:  # Ensures only one message is handled at a time
        await asyncio.sleep(10 * 60)  # Wait 10 minutes

        while True:
            now = datetime.now(IST).time()
            
            if 1 <= now.hour < 7:  # Forwarding allowed only between 1 AM - 7 AM IST
                message_id = event.message.id  # Use message ID to track uniqueness
                message_text = event.message.text

                # Check if message was already forwarded
                if await db.find_used(message_id):
                    print(f"⏩ Skipped duplicate: {message_text}")
                else:
                    user_ids = [1983814301, 7755788244]
                    
                    #for user_id in user_ids:  # ✅ FIX: Indentation added below
                       # await event.client.send_message(user_id, message_text)  # ✅ Indented correctly
                    
                    # Mark message as forwarded
                    await db.add_used(message_id)
                    print(f"✅ Forwarded: {message_text} at {now}")

                break  # Stop after processing the message
            else:
                print("⏳ Not in forwarding time. Waiting until 1 AM IST...")
                await asyncio.sleep(1000)  # Wait before checking again

@mrsyd.on(events.NewMessage(chats=-1002658187814))
async def forwd_mesages(event):
    message = event.message
    await asyncio.sleep(100 * 60)
    if message.buttons:
        await message.click(0, 0)
    
