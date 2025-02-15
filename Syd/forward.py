# plugins/forwarder.py
import asyncio
import random
from bot import mrsyd
from asyncio import Semaphore
from telethon import events
#from info import SOURCE_CHAT_ID

# Semaphore to limit concurrent forwards (adjust as needed)
semaphore = Semaphore(2)
DESTINATION_CHAT = [-1002433450358, -1002464733363]
SOURCE_CHAT_ID = -1002295881345

@mrsyd.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def forward_if_allowed(event):
    if event.message.forward:  # Check if forwarding is allowed
        async with semaphore:  # Limit concurrent forwards
            try:
                DESTINATION_CHAT_ID = random.choice(DESTINATION_CHAT)
                await client.forward_messages(DESTINATION_CHAT_ID, event.message)
                print("✅ Message forwarded successfully.")
                await asyncio.sleep(300)
            except Exception as e:
                print(f"⚠️ Error forwarding message: {e}")
    else:
        print("❌ Forwarding not allowed for this message. Skipping...")



@mrsyd.register(events.NewMessage(from_users=1733124290))
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
                    DESTINATION_CHAT_ID = random.choice(DESTINATION_CHAT)
                    message = await event.client.get_messages(source_chat, ids=msg_id)
                    if message:  # Ensure message exists
                        if not message.forwards:  # Check if forwarding is allowed
                            print(f"❌ Message {msg_id} is restricted. Skipping.")
                            continue

                        print(f"📤 Forwarding message {msg_id} from {source_chat}...")
                        await event.client.forward_messages(DESTINATION_CHAT_ID, message, as_forward=True)
                        print(f"✅ Message {msg_id} forwarded successfully!")
                        await asyncio.sleep(300)  # Small delay to avoid spam
                    else:
                        print(f"❌ Message {msg_id} does not exist. Skipping.")

                except Exception as e:
                    print(f"⚠️ Error forwarding message {msg_id}: {e}")

    else:
        await event.respond("❌ Invalid format! Use: `-100XXXX YYYY ZZZZ` (Source Chat, Start ID, End ID)")
