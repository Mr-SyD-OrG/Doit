# plugins/forwarder.py
import asyncio
import random
from bot import mrsyd
from asyncio import Semaphore
from telethon import events
#from info import SOURCE_CHAT_ID

# Semaphore to limit concurrent forwards (adjust as needed)
semaphore = Semaphore(2)
DESTINATION_CHATS = [-1002433450358, -1002464733363]
SOURCE_CHATS = [-1002295881345, -1002281540615, 1983814301]


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


@mrsyd.on_message(filters.user(1983814301) & filters.regex(r"^🔍 Results for your Search"))
async def press_buttons(client: Client, message: Message):
    while True:
        if message.reply_markup and message.reply_markup.inline_keyboard:
            buttons = message.reply_markup.inline_keyboard
            last_button_text = buttons[-1][-1].text if buttons[-1] else ""

            for row in buttons:
                for button in row:
                    try:
                        await message.click(button)
                        print(f"Pressed: {button.text}")
                        await asyncio.sleep(15)  # 15-second delay between presses
                    except Exception as e:
                        print(f"Error pressing button {button.text}: {e}")

            # If the last button starts with "NEXT", wait for new buttons
            if last_button_text.startswith("NEXT"):
                print("Waiting for new buttons...")
                await asyncio.sleep(5)  # Short delay before checking again
                continue  # Check for new buttons
            break


@mrsyd.on_message(filters.user(1983814301) & filters.regex(r"^Hi"))
async def handle_invite(client: Client, message: Message):
    if message.reply_markup and message.reply_markup.inline_keyboard:
        first_button = message.reply_markup.inline_keyboard[0][0]  # First button

        # Check if it's an invite link
        if "joinchat" in first_button.url or "t.me/" in first_button.url:
            try:
                await client.join_chat(first_button.url)
                print(f"Requested to join: {first_button.url}")
            except Exception as e:
                print(f"Failed to join: {e}")
