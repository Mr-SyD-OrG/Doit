import re
import asyncio
from datetime import datetime, timedelta
from pytz import timezone
from bot import mrsyd
from telethon import events
from telethon.tl.types import PeerChannel
from .mrsyd import PROCESS
IST = timezone("Asia/Kolkata")

@mrsyd.on(events.NewMessage(func=lambda e: isinstance(e.message.from_id, PeerChannel) and e.message.from_id.channel_id == 2623780966))
async def handle_channel_d_message(event):
    global PROCESS
    if not PROCESS:
        return

    text = event.message.raw_text or ""
    result = None
    lower_text = text.lower()

    # 1. Delay if "second"/"third" is in text but not "first"/"frist"
    if any(w in lower_text for w in ['second', 'third']) and not any(w in lower_text for w in ['first', 'frist']):
        await asyncio.sleep(1)

    # 2. Detect time (e.g., "Time 12:32", "At 12:32", "at 5:03 😎")
    time_match = re.search(r'\b(?:time|at)\s+(\d{1,2}):(\d{2})', lower_text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))

        # Convert to datetime in IST
        now = datetime.now(IST)
        target_time = now.replace(hour=hour % 12, minute=minute, second=0, microsecond=0)

        # Use nearest future time
        if target_time <= now:
            target_time += timedelta(hours=12) if hour <= 6 else timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)

    # 3. Detect math expression like "10+10+9 =??"
    math_expr_match = re.search(r'(?i)(\d+(?:\s*[×x+]\s*\d+)+)\s*=*\s*\?+', text)
    if math_expr_match:
        expr_raw = math_expr_match.group(1)
        expr = expr_raw.replace('×', '*').replace('x', '*').replace(' ', '')
        try:
            result = str(eval(expr))
        except Exception:
            result = None

    # 4. Try "code:" or "question:" fallback
    if result is None:
        match = re.search(r'\b(code|question)\b\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
        if match:
            expr = match.group(2).strip()

            mul_match = re.match(r'^(\d+)\s*[x×]\s*(\d+)$', expr)
            if mul_match:
                a = int(mul_match.group(1))
                b = int(mul_match.group(2))
                result = str(a * b)

            elif re.fullmatch(r'(\d+\+)+\d+', expr):
                parts = list(map(int, expr.split('+')))
                result = str(sum(parts))

            else:
                result = re.sub(r'[^\w\s]', '', expr).strip()

    # 5. Send result
    if not result:
        await event.client.send_message(ADMIN_ID, "NO MATCH FOUND", parse_mode='markdown')
        return

    if len(result.strip().split()) <= 2:
        await event.reply(result)
    else:
        await event.client.send_message(ADMIN_ID, f"Too Long {result} Ignoring", parse_mode='markdown')



from datetime import datetime, timedelta
from pytz import timezone

IST = timezone("Asia/Kolkata")

@mrsyd.on(events.NewMessage(func=lambda e: isinstance(e.message.from_id, PeerChannel) and e.message.from_id.channel_id == 2623780966))
async def handle_channel_posted_message(event):
    global PROCESS
    if not PROCESS:
        return

    text = event.message.raw_text or ""
    result = None
    lower_text = text.lower()

    # 1. Delay if "second"/"third" is in text but not "first"/"frist"
    if any(w in lower_text for w in ['second', 'third']) and not any(w in lower_text for w in ['first', 'frist']):
        await asyncio.sleep(1)

    # 2. Detect time (e.g., "Time 12:32", "At 12:32", "at 5:03 😎")
    time_match = re.search(r'\b(?:time|at)\s+(\d{1,2}):(\d{2})', lower_text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))

        # Convert to datetime in IST
        now = datetime.now(IST)
        target_time = now.replace(hour=hour % 12, minute=minute, second=0, microsecond=0)

        # Use nearest future time
        if target_time <= now:
            target_time += timedelta(hours=12) if hour <= 6 else timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)

    # 3. Detect math expression like "10+10+9 =??"
    math_expr_match = re.search(r'(?i)(\d+(?:\s*[×x+]\s*\d+)+)\s*=*\s*\?+', text)
    if math_expr_match:
        expr_raw = math_expr_match.group(1)
        expr = expr_raw.replace('×', '*').replace('x', '*').replace(' ', '')
        try:
            result = str(eval(expr))
        except Exception:
            result = None

    # 4. Try "code:" or "question:" fallback
    if result is None:
        match = re.search(r'\b(code|question)\b\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
        if match:
            expr = match.group(2).strip()

            mul_match = re.match(r'^(\d+)\s*[x×]\s*(\d+)$', expr)
            if mul_match:
                a = int(mul_match.group(1))
                b = int(mul_match.group(2))
                result = str(a * b)

            elif re.fullmatch(r'(\d+\+)+\d+', expr):
                parts = list(map(int, expr.split('+')))
                result = str(sum(parts))

            else:
                result = re.sub(r'[^\w\s]', '', expr).strip()

    # 5. Send result
    if not result:
        await event.client.send_message(ADMIN_ID, "NO MATCH FOUND", parse_mode='markdown')
        return

    if len(result.strip().split()) <= 2:
        await event.reply(result)
    else:
        await event.client.send_message(ADMIN_ID, f"Too Long {result} Ignoring", parse_mode='markdown')
