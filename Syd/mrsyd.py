from telethon import events
import asyncio
import re
from bot import mrsyd
import random
from telethon.tl.types import PeerChannel

PROCESS = False

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#start_year = 2000
start_year = 2020
end_year = 2023
messge = ["A 2000 480p", "A 2000 720p", "A 2000 1080p", "B 2001 480p", "B 2001 720p", "B 2001 1080p", "C 2002 480p", "C 2002 720p", "C 2002 1080p"]
resolutions = ["240p", "480p", "720p", "1080p", "2160p"]
WAIT = [35, 120, 240, 300, 360, 420, 540, 600, 700, 800, 1000, 1200, 3000]

@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"Search"))
async def handle_search_trigger(event):
    await event.reply("Starting resolution.")
 #   start_from = "V 2001 480p"
    start_reached = False
    start_from = "A 2020 240p"
    for letter in letters:
        for year in range(start_year, end_year + 1):
            for res in resolutions:
                msg = f"{letter} {year} {res}"
                # Wait until we reach the starting point
                if not start_reached:
                    if msg == start_from:
                        start_reached = True
                    else:
                        continue
                # Skip if already sent
                if msg in messge:
                    continue
                sydd = random.choice(WAIT)
                await event.client.send_message(1983814301, msg)
                print(f"Sent: {msg} Wait {sydd}")
                await asyncio.sleep(sydd)

    await event.client.send_message(1733124290, "Done sending all resolutions.")




@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"on"))
async def handle_on_trigger(event):
    global PROCESS
    PROCESS = True
    await event.reply("Set To True")

    
@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"off"))
async def handle_off_trigger(event):
    global PROCESS
    PROCESS = False
    await event.reply("Set To False")


# Replace this with your target channel ID (use a negative number for channels)
TARGET_CHANNEL_ID = 2623780966

DISCUSSION_GROUP_ID = -1002470503901  # ID of the group linked to the channel
ADMIN_ID = 1733124290  # Replace with the actual admin ID

# Replace with your channel ID

@mrsyd.on(events.NewMessage(chats=DISCUSSION_GROUP_ID))
async def handle_comment(event):
    global PROCESS
    if not PROCESS:
        return
    from_id = event.message.from_id

    # Check if the message was sent as the channel
    if not (isinstance(from_id, PeerChannel) and from_id.channel_id == TARGET_CHANNEL_ID):
        return

    text = event.message.raw_text or ""

    # Match keyword and extract expression
    match = re.search(r'\b(code|question)\b\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
    if not match:
        await event.client.send_message(ADMIN_ID, "NO MATCH FOUND", parse_mode='markdown')
        return  # No keyword found

    expr = match.group(2).strip()

    # Handle multiplication
    mul_match = re.match(r'^(\d+)\s*[x×]\s*(\d+)$', expr)
    if mul_match:
        a = int(mul_match.group(1))
        b = int(mul_match.group(2))
        result = f"{a * b}"

    # Handle addition
    elif re.fullmatch(r'(\d+\+)+\d+', expr):
        parts = list(map(int, expr.split('+')))
        total = sum(parts)
        result = f"{total}"

    else:
        result = expr

    # Count number of words in response
    word_count = len(result.strip().split())

    if word_count <= 2:
        # Repeat short responses for emphasis
        await event.reply(result)
    else:
        # Reply once for long responses
        await event.client.send_message(ADMIN_ID, f"Too Long {result} Ignoring", parse_mode='markdown')

   # PROCESS = False
