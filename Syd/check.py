

from bot import mrsyd
  # Replace with admin's user ID
from telethon import events
#from telethon.tl.functions.users import GetFullUserRequest
import asyncio

# Define your admin and target user IDs
admin_user_id = 1733124290  # Replace with actual admin user ID
target_user_ids = [6592320604, 5334261812, 5329540859, 5378426785, 6006903252, 5378661049, 6278143617, 8036619264, 7868859577, 7658164007, 7017921723, 7872466736]  # Replace with your target user IDs
#target_user_ids = [6592320604, 5334261812]
# Create global boolean flags for each target user
user_flags = {user_id: False for user_id in target_user_ids}
usernames_cache = {}


      
# Set user flag True when a message is received from them
@mrsyd.on(events.NewMessage(chats=group_chat_id))
async def handle_group_messages(event):
    sender = await event.get_sender()
    sender_id = sender.id

    if sender_id in target_user_ids:
        user_flags[sender_id] = True
        print(f"Message received from target user {sender_id}, flag set to True.")
      
# When admin sends "Check", send the current status of each target user
@mrsyd.on(events.NewMessage(from_users=admin_user_id, pattern=r"^SyD"))
async def trigger(event):
    report_lines = ["User message check report:"]
    for user_id in target_user_ids:
        await mrsyd.send_message(user_id, '/start')
        await asyncio.sleep(1)
    await mrsyd.send_message(admin_user_id, 'start')
    for uid, status in user_flags.items():
        # Fetch username from cache or Telegram
        if uid not in usernames_cache:
            user = await mrsyd.get_entity(uid)
            usernames_cache[uid] = user.username if user.username else f"{user.first_name} {user.last_name or ''}".strip()
        
        name = usernames_cache[uid]
        report_lines.append(f"@{name}: {'✅' if status else '❌'}")
    
    report = "\n".join(report_lines)
    await event.respond(report)

    # Reset all flags for the next day
    for uid in user_flags:
        user_flags[uid] = False

#from telethon import events

# === CONFIG ===

status_chat_id = -1001778495166  # Replace with chat ID of the message to be edited
status_message_id = 8  # Replace with the message ID to update
