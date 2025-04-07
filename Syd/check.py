

from bot import mrsyd
  # Replace with admin's user ID
from telethon import events
#from telethon.tl.functions.users import GetFullUserRequest
import asyncio

# Define your admin and target user IDs
admin_user_id = 1733124290  # Replace with actual admin user ID
#target_user_ids = [6592320604, 5334261812, 5329540859, 5378426785, 6006903252, 5378661049, 6278143617, 8036619264, 7868859577, 7658164007, 7017921723, 7872466736]  # Replace with your target user IDs
target_user_ids = [6592320604, 5329540859]
# Create global boolean flags for each target user
user_flags = {user_id: False for user_id in target_user_ids}
usernames_cache = {}


# Replace with your actual chat and message IDs
REPORT_CHAT_ID = -1001778495166
REPORT_MSG_ID = 9  
# <- Update with actual message ID

@mrsyd.on(events.NewMessage(chats=-1002687879857))
async def handle_group_messages(event):

    sender = await event.get_sender()
    sender_id = sender.id   #Update with actual message ID
    if sender_id in target_user_ids:

        user_flags[sender_id] = True
        print(f"Message received from target user {sender_id}, flag set to True.")

@mrsyd.on(events.NewMessage(from_users=admin_user_id, pattern=r"^SyD"))
async def trigger(event):
    await mrsyd.send_message(REPORT_CHAT_ID, "/start")
    await asyncio.sleep(15)
    await mrsyd.send_message(admin_user_id, 'C')

    # Fetch the original message to edit
    message_to_edit = await mrsyd.get_messages(REPORT_CHAT_ID, ids=REPORT_MSG_ID)
    original_lines = message_to_edit.text.splitlines()

    updated_lines = []
    report_lines = ["User message check report:"]
    
    for line in original_lines:
        if not line.startswith("@"):
            updated_lines.append(line)
            continue

        username = line.split(":")[0][1:].strip()  # remove @ and spaces
        uid = next((uid for uid, uname in usernames_cache.items() if uname.lower() == username.lower()), None)

        if uid and uid in user_flags:
            status_icon = '✅' if user_flags[uid] else '❌'
            updated_line = f"@{username}: {status_icon}"
            updated_lines.append(updated_line)
            report_lines.append(updated_line)
        else:
            updated_lines.append(line)

    # Edit the group message
    updated_report = "\n".join(updated_lines)
    await mrsyd.edit_message(REPORT_CHAT_ID, REPORT_MSG_ID, updated_report)

    # Send full report to admin
    admin_report = "\n".join(report_lines)
    await mrsyd.send_message(admin_user_id, admin_report)

    # Reset all flags
    for uid in user_flags:
        user_flags[uid] = False
