# plugins/forwarder.py
import asyncio
import re
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


@mrsyd.on(events.NewMessage(chats=SOURCE_CHATS))
async def forward_if_allowed(event):
    message = event.message
    if message.media and (message.document or message.file):
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

@mrsyd.on(events.NewMessage(from_users=1983814301, pattern=r"^🔍 Results for your Search"))
async def handle_message(event):
    """Press all buttons in order, including updated ones after 'NEXT'."""
    message = event.message
    chat_id = message.chat_id
    message_id = message.id  # Track the same message ID

    while True:
        if message.buttons:
            buttons = message.buttons
            last_button_text = buttons[-1][-1].text if buttons[-1] else ""

            for row_idx, row in enumerate(buttons):  
                for col_idx, button in enumerate(row):  
                    try:
                        await message.click(row_idx, col_idx)  # Click button
                        print(f"Pressed: {button.text}")
                        await asyncio.sleep(120)  # 120-second delay
                    except Exception as e:
                        print(f"Error pressing button {button.text}: {e}")

            # If the last button is "NEXT", wait for the message to be edited
            if last_button_text.startswith(" NEXT"):
                print("Waiting for updated buttons...")

                while True:
                    await asyncio.sleep(8)  # Check for edits every 5 seconds
                    edited_msg = await event.client.get_messages(chat_id, ids=message_id)

                    if edited_msg and edited_msg.buttons != message.buttons:
                        print("Message updated with new buttons, continuing...")
                        message = edited_msg  # Update message with new buttons
                        break  # Restart button clicking process

                continue  # Loop again with updated buttons

        break  # Stop if no buttons left



@mrsyd.on(events.NewMessage(from_users=1983814301, pattern=r"^Hi"))
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

