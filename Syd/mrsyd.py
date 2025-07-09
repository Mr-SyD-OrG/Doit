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


import re
import asyncio
from datetime import datetime, timedelta
from telethon.tl.types import PeerUser
from pytz import timezone

  # Replace with your actual admin user ID
IST = timezone('Asia/Kolkata')

@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"send"))
async def handle_admn_message(event):
    text = event.message.raw_text.strip()

    # Match pattern: Send @username time 4:30 Message here
    match = re.match(r'^send\s+@?(\w{5,32})\s+time\s+(\d{1,2})[:;](\d{2})\s+(.+)', text, re.IGNORECASE)
    if not match:
        await event.reply("❌ Invalid format. Use:\nSend @username time 4:30 Your message")
        return

    username = match.group(1)
    hour = int(match.group(2))
    minute = int(match.group(3))
    message_text = match.group(4).strip()

    # Time calculation
    now = datetime.now(IST)
    target_time = now.replace(hour=hour % 12, minute=minute, second=0, microsecond=0)
    
    # Adjust for next day or AM/PM
    if target_time <= now:
        target_time += timedelta(hours=12) if hour <= 6 else timedelta(days=1)

    wait_time = (target_time - now).total_seconds()

    await event.reply(f"✅ Message will be sent to @{username} at {target_time.strftime('%I:%M %p')} IST.")

    await asyncio.sleep(wait_time)

    try:
        user = await event.client.get_entity(username)
        await event.client.send_message(user, message_text)
        await event.reply(f"✅ Sent message to @{username}")
    except Exception as e:
        await event.reply(f"❌ Failed to send message to @{username}\nError: {e}")


@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"on"))
async def handle_on_trigger(event):
    global PROCESS
    PROCESS = True
    await event.reply("Set To True .")

    
@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"off"))
async def handle_off_trigger(event):
    global PROCESS
    PROCESS = False
    await event.reply("Set To False .")


# Replace this with your target channel ID (use a negative number for channels)
TARGET_CHANNEL_ID = 1562013

DISCUSSION_GROUP_ID = -1002470503901  # ID of the group linked to the channel
ADMIN_ID = 1733124290  # Replace with the actual admin ID


@mrsyd.on(events.NewMessage(func=lambda e: isinstance(e.message.from_id, PeerChannel) and e.message.from_id.channel_id == TARGET_CHANNEL_ID))
async def handle_channel_posted_message(event):
    global PROCESS
    if not PROCESS:
        return

    text = event.message.raw_text or ""
    result = None

    # Detect math problems like "10+10+10+10+10+9 =??" or "2×2×6×8×9 = ???"
    math_expr_match = re.search(r'(?i)(\d+(?:\s*[×x+]\s*\d+)+)\s*=*\s*\?+', text)
    if math_expr_match:
        expr_raw = math_expr_match.group(1)

        # Clean and standardize expression
        expr = expr_raw.replace('×', '*').replace('x', '*').replace(' ', '')
        try:
            # Safe evaluation of math expression
            result = str(eval(expr))
        except Exception:
            result = None

    # If not a math question, try matching with keyword like "code:" or "question:"
    if result is None:
        match = re.search(r'\b(code|question)\b\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
        if match:
            expr = match.group(2).strip()
            
            # Handle multiplication
            mul_match = re.match(r'^(\d+)\s*[x×]\s*(\d+)$', expr)
            if mul_match:
                a = int(mul_match.group(1))
                b = int(mul_match.group(2))
                result = str(a * b)

            # Handle addition
            elif re.fullmatch(r'(\d+\+)+\d+', expr):
                parts = list(map(int, expr.split('+')))
                result = str(sum(parts))

            else:
                # Fallback: just echo the extracted text (removing special chars)
                result = re.sub(r'[^\w\s]', '', expr).strip()

    if not result:
        await event.client.send_message(ADMIN_ID, "NO MATCH FOUND", parse_mode='markdown')
        return

    # Decide how to respond
    word_count = len(result.strip().split())
    if word_count <= 2:
        await event.reply(result)
    else:
        await event.client.send_message(ADMIN_ID, f"Too Long {result} Ignoring", parse_mode='markdown')
  #  PROCESS = False

TxT = ["Plez", "Me", "O?", "H", "Yo?", "he", "me", "try..", "pleaz", "."]

#@mrsyd.on(events.NewMessage(func=lambda e: isinstance(e.message.from_id, PeerChannel) and e.message.from_id.channel_id == 2265803056))
async def handle_auro_postd_message(event):
    global PROCESS
    if not PROCESS:
        return
    syd = random.choice(TxT)
    await event.reply(syd)
    


ALLOWED_CHANNEL_DS = [1562527013, 1845700427, 2623780966, 2827374506, 2520764012, 2265803056]  # Add more channel IDs here



@mrsyd.on(events.NewMessage(func=lambda e: isinstance(e.message.from_id, PeerChannel) and e.message.from_id.channel_id in ALLOWED_CHANNEL_DS))
async def handle_channel_postd_message(event):
    global PROCESS
    if not PROCESS:
        await asyncio.sleep(3600)
        PROCESS = True
        return

    await event.client.send_message(ADMIN_ID, "Received Message", parse_mode='markdown')

    text = event.message.raw_text or ""
    lower_text = text.lower()
    result = None

    # Delay if "second"/"third" is in text but not "first"/"frist"
    if any(w in lower_text for w in ['second', 'third']) and not any(w in lower_text for w in ['first', 'frist']):
        await asyncio.sleep(0.8)

    # Detect time like "time 6:30"
    time_match = re.search(r'\b(?:time|at)[\s:\-–—]*\s*(\d{1,2})[:;](\d{2})', lower_text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))

        now = datetime.now(IST)

        # FIX: get nearest future time today: try AM first, else PM
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target_time <= now:
            if hour < 12:
                # if hour <12, try PM (hour+12)
                target_time_pm = now.replace(hour=hour+12, minute=minute, second=0, microsecond=0)
                if target_time_pm > now:
                    target_time = target_time_pm
                else:
                    target_time += timedelta(days=1)
            else:
                target_time += timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)

    # Detect math expr like 10+5-2+3=??
    math_expr_match = re.search(r'(?i)(\d+(?:\s*[-+×x]\s*\d+)+)\s*=*\s*\?+', text)
    if math_expr_match:
        expr_raw = math_expr_match.group(1)
        expr = expr_raw.replace('×', '*').replace('x', '*').replace(' ', '')
        try:
            result = str(eval(expr))
        except Exception:
            result = None

    # Detect "1st comment win", "1st ans win", etc.
    if result is None and re.search(r'1st\s*(comment|ans|answer)\s*win', lower_text):
        numbers_match = re.search(r'que\.?\s*([0-9+\-×x\s]+)', lower_text)
        if numbers_match:
            expr = numbers_match.group(1).replace('×', '*').replace('x', '*').replace(' ', '')
            if re.fullmatch(r'(\d+[-+]\d+)+', expr):
                try:
                    result = str(eval(expr))
                except Exception:
                    result = None

    # Fallback: code: or question:
    if result is None:
        match = re.search(r'\b(code|question)\b\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
        if match:
            expr = match.group(2).strip().replace('×', '*').replace('x', '*')
            # FIX: do NOT remove spaces; keep them for text answers
            # If it's math, eval; else keep as is with spaces
            expr_nospace = expr.replace(' ', '')
            if re.fullmatch(r'(\d+[-+]\d+)+', expr_nospace) or re.fullmatch(r'(\d+[*]\d+)+', expr_nospace):
                try:
                    result = str(eval(expr_nospace))
                except Exception:
                    result = None
            else:
                # Remove only punctuation, keep words & spaces
                result = re.sub(r'[^\w\s]', '', expr).strip()

    # Send result
    if result and len(result.strip().split()) <= 12:  # allow up to ~12 words
        await event.reply(result)
        PROCESS = False
    else:
        await event.client.send_message(ADMIN_ID, f"NO MATCH FOUND or Too Long: {text}", parse_mode='markdown')

