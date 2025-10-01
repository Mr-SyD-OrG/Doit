

from bot import mrsyd
  # Replace with admin's user ID
from telethon import events
#from telethon.tl.functions.users import GetFullUserRequest
import asyncio
from telethon.tl import functions

# Define your admin and target user IDs
admin_user_id = [1733124290]  # Replace with actual admin user ID
target_user_ids = [6592320604, 5334261812, 5329540859, 5378426785, 6006903252, 5378661049, 6278143617, 8036619264, 7868859577, 7658164007, 7017921723, 7872466736]  # Replace with your target user IDs
#target_user_ids = [6592320604, 5329540859]
# Create global boolean flags for each target user
user_flags = {user_id: False for user_id in target_user_ids}
usernames_cache = {
    6592320604: 'Mr_Movies_File_bot',
    5329540859: 'Pro_Moviez_bot',
    7872466736: 'Mr_Auto_Rename_Bot',
    7658164007: 'Movies_forage_Bot',
    7868859577: 'Files_Forwarding_Bot',
    8036619264: 'Auto_Caption_Edit_bot',
    6006903252: 'Instant_Approval_Bot',
    5334261812: 'MrMoviez_bot',
    5378426785: 'MoViE_2022_NT_Bot',
    6278143617: 'Ms_FiLe2LINk_bOt',
    7017921723: 'Mr_File_Forward_Bot',
    5378661049: 'MS_ReNamEr_BoT'
}

# Replace with your actual chat and message IDs
REPORT_CHAT_ID = -1001778495166
REPORT_MSG_ID = 9  
# <- Update with actual message ID

semapore = asyncio.Semaphore(1)

@mrsyd.on(events.NewMessage(chats=-1002687879857))
async def handle_group_messages(event):
    async with semapore:
        await asyncio.sleep(0.5)
        sender = await event.get_sender()
        sender_id = sender.id
        if sender_id in target_user_ids:
            user_flags[sender_id] = True
            print(f"Message received from target user {sender_id}, flag set to True.")

@mrsyd.on(events.NewMessage(from_users=admin_user_id, pattern=r"^SyD"))
async def trigge(event):
    await mrsyd.send_message(-1002687879857, "/start")
    await asyncio.sleep(15)
    await mrsyd.send_message(admin_user_id, 'C')

    # Fetch the message to edit
    message_to_edit = await mrsyd.get_messages(REPORT_CHAT_ID, ids=REPORT_MSG_ID)
    original_lines = message_to_edit.text.splitlines()

    updated_lines = []
    report_lines = ["User message check report:"]

    found_usernames = set()

    for line in original_lines:
        if not line.startswith("@"):
            updated_lines.append(line)
            continue

        username = line.split(":")[0][1:].strip()
        found_usernames.add(username.lower())

        uid = next(
            (uid for uid, uname in usernames_cache.items() if uname.lower() == username.lower()),
            None
        )

        status = user_flags.get(uid, False) if uid is not None else False
        status_icon = '✅' if status else '❌'
        updated_line = f"@{username}: {status_icon}"

        updated_lines.append(updated_line)
        report_lines.append(updated_line)
      
    for uid, uname in usernames_cache.items():
        if uname.lower() not in found_usernames:
            status = user_flags.get(uid, False)
            status_icon = '✅' if status else '❌'
            extra_line = f"@{uname}: {status_icon}"
            report_lines.append(extra_line)

    # Send report to admin
    admin_report = "\n".join(report_lines)
    await mrsyd.send_message(admin_user_id, admin_report)

    # Update group message if changed
    updated_report = "\n".join(updated_lines)
    if updated_report != message_to_edit.text:
        await mrsyd.edit_message(REPORT_CHAT_ID, REPORT_MSG_ID, updated_report)

    # Reset flags
    for uid in user_flags:
        user_flags[uid] = False



from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputUser

# ======== CONFIG ========


TARGET_CHAT = -1002965604896  # Chat where requests come
ADMIN_IDS = admin_user_id        # IDs allowed to send the document
BLOCK_LIST = [11111111, 22222222]  # Users to ignore/deny

ADMIN_USER_ID = 1733124290

@mrsyd.on(events.NewMessage(from_users=admin_user_id))
async def on_document(event):
    try:
        if not event.message.file:
            return

        # Parse document -> block list
        doc_bytes = await event.message.download_media(bytes)
        blocked_users = set(BLOCK_LIST)
        for line in doc_bytes.decode("utf-8").splitlines():
            line = line.strip()
            if line.isdigit():
                blocked_users.add(int(line))

        await event.client.send_message(ADMIN_USER_ID, f"🚫 Blocked list updated: {blocked_users}")

        # Fetch pending join requests
        try:
            res = await event.client(functions.messages.GetChatInviteImporters(
                peer=TARGET_CHAT,
                limit=10  # adjust if you expect more
            ))
        except Exception as e:
            await event.client.send_message(ADMIN_USER_ID, f"⚠️ Failed to fetch requests: {e}")
            return

        if not res.importers:
            await event.client.send_message(ADMIN_USER_ID, "ℹ️ No pending join requests found.")
            return

        await event.client.send_message(ADMIN_USER_ID, f"Found {len(res.importers)} pending requests")

        # Approve/skip based on block list
        for imp in res.importers:
            user_id = imp.user_id
            if user_id not in blocked_users:
                try:
                    await event.client(functions.messages.HideChatJoinRequestRequest(
                        peer=TARGET_CHAT,
                        user_id=user_id,
                        approved=True
                    ))
                    await event.client.send_message(ADMIN_USER_ID, f"✅ Approved {user_id}")
                except Exception as e:
                    await event.client.send_message(ADMIN_USER_ID, f"⚠️ Failed to approve {user_id}: {e}")
            else:
                await event.client.send_message(ADMIN_USER_ID, f"❌ Skipped blocked {user_id}")

    except Exception as e:
        await event.client.send_message(ADMIN_USER_ID, f"❌ Unexpected error: {e}")

async def on_document(event):
    try:
        await event.client.send_message(1733124290, "Starting")

        if not event.message.file:
            return

        await event.client.send_message(1733124290, "Starting 2")

        # Process document
        try:
            doc_bytes = await event.message.download_media(bytes)
            blocked_users = set(BLOCK_LIST)
            for line in doc_bytes.decode("utf-8").splitlines():
                line = line.strip()
                if line.isdigit():
                    blocked_users.add(int(line))
        except Exception as e:
            await event.client.send_message(1733124290, f"⚠️ Failed to process document: {e}")
            blocked_users = set(BLOCK_LIST)

        await event.client.send_message(1733124290, f"Blocked users: {blocked_users}")

        # Fetch pending join requests
        try:
            full_chat = await event.client(GetFullChannelRequest(TARGET_CHAT))
            participants = getattr(full_chat.full_chat, "participants", None)
            if not participants or not hasattr(participants, "requests"):
                await event.client.send_message(1733124290, "No pending join requests found.")
                return

            requests = participants.requests
            await event.client.send_message(1733124290, f"Found {len(requests)} pending requests.")

            for req in requests:
                user_id = req.user_id
                if user_id not in blocked_users:
                    try:
                        await event.client(functions.messages.HideChatJoinRequestRequest(
                            peer=TARGET_CHAT,
                            user_id=user_id,
                            approved=True
                        ))
                        await event.client.send_message(1733124290, f"✅ Approved user {user_id}")
                    except Exception as e:
                        await event.client.send_message(1733124290, f"⚠️ Failed to approve {user_id}: {str(e)}")
                else:
                    await event.client.send_message(1733124290, f"❌ Skipped blocked user {user_id}")

        except Exception as e:
            await event.client.send_message(1733124290, f"⚠️ Failed to get channel info or approve requests: {str(e)}")

    except Exception as main_e:
        await event.client.send_message(1733124290, f"❌ Unexpected error: {str(main_e)}")
        print(f"❌ Unexpected error in event handler: {main_e}")
