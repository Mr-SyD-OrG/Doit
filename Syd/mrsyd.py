from telethon import events
import asyncio
import re
from bot import mrsyd
import random
from telethon.tl.types import PeerChannel
import logging



logging.basicConfig(level=logging.INFO)


client = mrsyd
PROCESS = False
OCESS = False
MPROCESS = False
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#start_year = 2000
start_year = 2021
end_year = 2023
messge = ["A 2000 480p", "A 2000 720p", "A 2000 1080p", "B 2001 480p", "B 2001 720p", "B 2001 1080p", "C 2002 480p", "C 2002 720p", "C 2002 1080p"]
resolutions = ["240p", "480p", "720p", "1080p", "2160p"]
WAIT = [35, 120, 240, 300, 360, 420, 540, 600, 700, 800, 1000, 1200, 3000]

@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"Search"))
async def handle_search_trigger(event):
    await event.reply("Starting resolution.")
 #   start_from = "V 2001 480p"
    start_reached = False
    start_from = "A 2021 240p"
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
                await event.client.send_message(7519971717, msg)
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

@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"sendf"))
async def handle_admn_message(event):
    text = event.message.raw_text.strip()

    # Match pattern: Send @username time 4:30 Message here
    match = re.match(r'^sendf\s+@?(\w{5,32})\s+time\s+(\d{1,2})[:;](\d{2})\s+(.+)', text, re.IGNORECASE)
    if not match:
        await event.reply("❌ Invalid format. Use:\nSendf @username time 4:30 Your message")
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

    await event.reply(f"✅ Mess will be sent to @{username} at {target_time.strftime('%I:%M %p')} IST.")

    await asyncio.sleep(wait_time)

    try:
        user = await event.client.get_entity(username)
        await event.client.send_message(user, message_text)
        await event.reply(f"✅ Sent message to @{username}")
    except Exception as e:
        await event.reply(f"❌ Failed to send message to @{username}\nError: {e}")


#@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"on"))
async def handle_on_trigger(event):
    global PROCESS
    PROCESS = True
    await event.reply("Set To True .")

#@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"oon"))
async def hand_on_ntrigger(event):
    global OCESS
    OCESS = True
    await event.reply("Bot- Set To True .")

    
#@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"stop"))
async def hand_offf_trigger(event):
    global MPROCESS
    MPROCESS = False
    await event.reply("ALL Set To False .")
    
#@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"start"))
async def had_on_tigger(event):
    global MPROCESS
    MPROCESS = True
    await event.reply("All Set To True .")

    
#@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"ooff"))
async def hand_off_trigger(event):
    global OCESS
    OCESS = False
    await event.reply("Bot- Set To False .")
    
#@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"off"))
async def handle_off_trigger(event):
    global PROCESS
    PROCESS = False
    await event.reply("Set To False .")


# Replace this with your target channel ID (use a negative number for channels)
TARGET_CHANNEL_ID = 1562013

DISCUSSION_GROUP_ID = -1002470503901  # ID of the group linked to the channel
ADMIN_ID = 1733124290  # Repoce with the actual admin ID


#@mrsyd.on(events.NewMessage(func=lambda e: isinstance(e.message.from_id, PeerChannel) and e.message.from_id.channel_id == TARGET_CHANNEL_ID))
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

TxT = ["Plez", "Me", "O?", "H", "Yo?", "he", "me", "try..", "plez", "."]
TRIGGER_TEXT = "Unlocked all."

#@mrsyd.on(events.NewMessage(func=lambda e: isinstance(e.message.from_id, PeerChannel) and e.message.from_id.channel_id == 2265803056))
async def handle_auro_postd_message(event):
    global PROCESS
    if not PROCESS:
        return
    syd = random.choice(TxT)
    await event.reply(syd)
    
TxxT = "/unlock"
#@mrsyd.on(events.NewMessage(from_users=609517172))
async def handle_bot_message(event):
    global OCESS
    if not OCESS:
        return
    await event.client.send_message(ADMIN_ID, f"D: Unlocked all. {event.raw_text.strip().lower()}")
    if event.raw_text.strip().lower() == TRIGGER_TEXT.lower():
        await event.client.send_message(ADMIN_ID, "D: Unlocked all.")
        await event.reply(TxxT)
        
ALLOWED_CHANNEL_DS = [1562527013, 1845700427, 2107245494, 2623780966, 2827374506, 2520764012, 2265803056, 2857066294]  # Add more channel IDs here
SYDSET = [2827374506, 2107245494, 2623780966]
WAIT_SYD = [0, 0.5, 1, 1, 1, 1.4, 1.2, 1.5, 2, 2, 2.5, 3, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8]


#@mrsyd.on(events.NewMessage(func=lambda e: isinstance(e.message.from_id, PeerChannel) and e.message.from_id.channel_id in ALLOWED_CHANNEL_DS))
async def handle_channel_postd_message(event):
    global PROCESS, MPROCESS
    if not MPROCESS:
        return
    if not PROCESS:
        await asyncio.sleep(300) 
        PROCESS = True
        return
    channel_id = event.message.from_id.channel_id
    
    if channel_id in SYDSET:
        wsyd = random.choice(WAIT_SYD)
        await asyncio.sleep(wsyd)
        await event.client.send_message(ADMIN_ID, f"Matched SYDSET: Channel {channel_id}, Wait {wsyd}")
        

    
    text = event.message.raw_text
    if not text:
        return
    lower_text = text.lower()
    result = None
    
    # 1️⃣ Delay if "second"/"third" but not "first"/"frist"
    if any(w in lower_text for w in ['second', 'third']) and not any(w in lower_text for w in ['first', 'frist']):
        await asyncio.sleep(0.8)
        
    if all(x in lower_text for x in ['first', 'win', 'dm']):
        # Code detection
        
        code_match = re.search(r'\bcode\b\s*[:\-;]?\s*(.+)', text, re.IGNORECASE)
        user_match = re.search(r'(?:dm|to)\s*[:\-]?\s*@([\w\d_]{3,})', lower_text)
        time_match = re.search(r'(?:time|at)\s*[:\-]?\s*(\d{1,2})[:;](\d{2})', lower_text)

        if code_match and user_match and time_match:
            code_to_send = code_match.group(1).strip()
            username = "@" + user_match.group(1)
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))

            now = datetime.now(IST)
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if target_time <= now:
                if hour < 12:
                    # PM fallback
                    target_time_pm = now.replace(hour=hour+12, minute=minute, second=0, microsecond=0)
                    if target_time_pm > now:
                        target_time = target_time_pm
                    else:
                        target_time += timedelta(days=1)
                else:
                    target_time += timedelta(days=1)

            wait_seconds = (target_time - now).total_seconds()
            await event.client.send_message(ADMIN_ID, f"Dm detected {text} ==>`{code_to_send}`")
            async def delayed_dm():
                await asyncio.sleep(wait_seconds)
                try:
                    await event.client.send_message(username, code_to_send)
                    await event.client.send_message(ADMIN_ID, f"✅ Sent DM to {username} at {target_time.strftime('%I:%M %p')} → `{code_to_send}`")
                except Exception as e:
                    await event.client.send_message(ADMIN_ID, f"❌ Failed to DM {username} → `{str(e)}`")

            asyncio.create_task(delayed_dm())
            return
    # 2️⃣ Detect time like "time 6:30" → wait till nearest future occurrence (AM/PM)
    time_match = re.search(r'\b(?:time|at)[\s:\-–—]*\s*(\d{1,2})[:;](\d{2})', lower_text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))
        now = datetime.now(IST)

        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target_time <= now:
            if hour < 12:
                # try PM (hour+12)
                target_time_pm = now.replace(hour=hour+12, minute=minute, second=0, microsecond=0)
                if target_time_pm > now:
                    target_time = target_time_pm
                else:
                    target_time += timedelta(days=1)
            else:
                target_time += timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)

    # 3️⃣ Detect math expr like 10+5-2+3=?? or similar
    math_expr_match = re.search(r'(?i)(\d+(?:\s*[-+×x*/]\s*\d+)+)\s*=*\s*\?+', text)
    if math_expr_match:
        expr_raw = math_expr_match.group(1)
        expr = expr_raw.replace('×', '*').replace('x', '*').replace(' ', '')
        try:
            result = str(eval(expr))
            if int(result) >= 400:
                wwsyd = random.choice(WAIT_SYD)
                print(f"Long {result} so ===> {wwsyd} ¹")
                await asyncio.sleep(wwsyd if 1 <= wwsyd <= 4 else 2)
        except Exception:
            result = None

    # 4️⃣ Detect "1st comment win", "1st ans win", "first answer win" etc.
    if result is None and re.search(r'1st\s*(comment|ans|answer)\s*win|first\s*(comment|ans|answer)\s*win', lower_text):
        numbers_match = re.search(r'que\.?\s*([0-9+\-×x*/\s]+)', lower_text)
        if numbers_match:
            expr = numbers_match.group(1).replace('×', '*').replace('x', '*').replace(' ', '')
            # check if expr is only digits & operators
            if re.fullmatch(r'[\d+\-*/]+', expr):
                try:
                    result = str(eval(expr))
                except Exception:
                    result = None

    # 5️⃣ Detect if message ONLY says "first comment win" (ignore emojis/punct) → reply random text
    if result is None:
        cleaned_text = re.sub(r'[^\w\s]', '', lower_text).strip()
        if cleaned_text == 'first comment win' or 'second comment win' or 'third comment win' or 'fourth comment win':
           # random_texts = ["ok", "yes", "done", "✅", "🙌", "👀"]
            result = random.choice(TxT)

    # 6️⃣ Fallback: detect "code:" or "question:" → either eval math or send text
    if result is None:
        match = re.search(r'\b(code|question)\b\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
        if match:
            expr = match.group(2).strip().replace('×', '*').replace('x', '*')
            # keep only numbers, + - * / and spaces
            expr_cleaned = re.sub(r'[^0-9+\-*/ ]', '', expr)
            expr_nospace = expr_cleaned.replace(' ', '')
            if re.fullmatch(r'[\d+\-*/]+', expr_nospace):
                try:
                    result = str(eval(expr_nospace))
                    if int(result) >= 500:
                        wwwsyd = random.choice(WAIT_SYD)
                        print(f"Long {result} so ===> {wwwsyd} ²")
                        await asyncio.sleep(wwwsyd if 1 <= wwwsyd <= 4 else 2)
                except Exception:
                    result = None
            else:
                # keep words and spaces, remove other punctuation
                result = re.sub(r'[^\w\s]', '', expr).strip()

     # 🔥 7️⃣ New Feature: If "first" + "win" + "dm" and code+user+time → DM the user at that time

    

    # ✅ Send result
    if result and len(result.strip().split()) <= 12 and "dm" not in lower_text:
        sent = await event.reply(result)
        sennt = None
        if result.lower() == "dhruv ka age":
            sennt = await event.reply("16")
        link = f"https://t.me/c/{str(event.chat.id)[4:]}/{sent.id}"
        await event.client.send_message(ADMIN_ID, f' {text} ===> <a href="{link}">{result}</a>' + (f" ===> {sennt.text}" if 'sennt' in locals() and sennt else ""), parse_mode='html')
        # Check message ID difference between channel message and sent message
        if sent.id - event.message.id == 1:
            PROCESS = False
            await event.client.send_message(ADMIN_ID, "Turned Off: First Message \n ```Send = `on` ```")
            return
            

    else:
        await event.client.send_message(ADMIN_ID, f"NO MATCH / Too Long / DM: {text}", parse_mode='markdown')


SYD_CCHANNELS = [
    -1003130682508,   
]

TARGET_BOT = "raffle_tickets_bot"   # bot username (without @)

#@mrsyd.on(events.NewMessage(chats=SYD_CCHANNELS))
async def handlergifft(event):
    try:
        text = event.raw_text or ""

        if "🎟 Цена билета: 0⭐" in text:
            print("Matched message!")

            # Check buttons
            if not event.message.buttons:
                return

            # Click first button (adjust if needed)
            button = event.message.buttons[0][0]
            result = await button.click()

            # Extract URL (if callback returns one)
            url = None

            if hasattr(result, "url"):
                url = result.url

            elif isinstance(result, str):
                url = result

            if not url:
                print("No URL found")
                return

            print("URL:", url)

            # Extract join_xxxxx
            match = re.search(r"(join_\d+)", url)

            if match:
                join_code = match.group(1)
                print("Found:", join_code)

                await client.send_message(
                    TARGET_BOT,
                    f"/start {join_code}"
                )

            else:
                print("No join code found")

    except Exception as e:
        print("Error:", e)


import random
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.types import MessageService


TARGETT_USER_ID = [1330490706, 5277255457]  # 👈 replace with user id

# Random replies
RANDOM_TEXTS = [
    "❤️",
    "😌",
    "⚡",
]

# Store last sent date
last_sent_date = None



#@mrsyd.on(events.NewMessage(from_users=TARGETT_USER_ID))
async def handlerpmmm(event):
    if isinstance(event.message, MessageService):
        today = datetime.now().date()

        # ✅ Only once per day
        if last_sent_date == today:
            print("Already replied today, skipping...")
            return

        # ✅ Send random text
        reply_text = random.choice(RANDOM_TEXTS)
        await event.reply(reply_text)

        print(f"Replied: {reply_text}")

        # ✅ Update last sent date
        last_sent_date = today



from telethon import TelegramClient, events, functions
from telethon.tl.types import KeyboardButtonWebView, KeyboardButtonUrl

CHAT_ID = 7974361539
async def open_and_close_webapp(button, peer, bot):
    try:
        # for web app buttons
        print("12")
        result = await mrsyd(
            functions.messages.RequestWebViewRequest(
                peer=peer,
                bot=bot,
                platform="android",
                url=getattr(button, "url", None),
                from_bot_menu=False
            )
        )

        print("Opened webapp:", result.url)

        # instantly close = do nothing more
        # Telegram itself considers request complete

    except Exception as e:
        print("Webapp open failed:", e)


async def press_button(message, text_to_find):
    if not message.buttons:
        return False

    for row in message.buttons:
        for btn in row:
            txt = (btn.text or "").strip()

            if txt == text_to_find:
                print("Pressing:", txt)

                # webapp button
                if isinstance(btn.button, KeyboardButtonWebView):
                    await open_and_close_webapp(btn.button, message.peer_id, 7974361539)

                else:
                    await message.click(text=txt)

                return True
    return False


# ---------- main handler ----------

#@mrsyd.on(events.NewMessage(from_users=7974361539))
async def handlersyyddd(event):
    msg = event.message

    # detect image/photo message
    if msg.photo:
        print("Image detected")
        if msg.buttons:
            for row in msg.buttons:
                for btn in row:
                    targets = ["Открыть", "Вперёд!", "Играть!", "Забрать награду!"]
                    if btn.text and any(t in btn.text for t in targets):
                        print("Opening webapp:", btn.text)

                        try:
                            if isinstance(btn, KeyboardButtonWebView):
                                print("1")
                                await open_and_close_webapp(
                                    btn.button,
                                    msg.peer_id,
                                    7974361539
                                )
                                print("2")
                            else:
                                try:
                                    print("3")
                                    await msg.click(text=btn.text)
                                    print("4")
                                except Exception as e:
                                    print(f"Failed to click {btn.text}: {e}")
                        except Exception as e:
                            print(e)

        # find next message below current image message
        async for nxt in mrsyd.iter_messages(
            7974361539,
            min_id=msg.id,
            reverse=True,
            limit=5
        ):
            if nxt.id > msg.id:
                ok = await press_button(nxt, "✅ Подтвердить")
                if ok:
                    print("Pressed Xxvhh below image msg")
                break



from telethon import TelegramClient, events, functions
from telethon.tl.types import KeyboardButtonWebView, KeyboardButtonUrl
from playwright.async_api import async_playwright
import asyncio


import asyncio
import random
import logging
from telethon import events
from telethon.tl.types import KeyboardButtonUrl
from playwright.async_api import async_playwright

PHOTO_MSG_IDS = set()
SUBSCRIBE_MSG_IDS = set()
GENERAL = False
TURN = False
ADMIN_ID = 1733124290
bot_id = 8006795826  # replace
ADMINS = [ADMIN_ID]
# =========================
# OPEN URL
# =========================

@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"stop"))
async def hand_offf_trigger(event):
    global GENERAL
    GENERAL = False
    await event.reply("GENERAL Set To False .")
    
@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"start"))
async def had_on_tigger(event):
    global GENERAL
    GENERAL = True
    await event.reply("GENERAL Set To True .")

import random
import asyncio
from playwright.async_api import async_playwright

playwright_instance = None
browser = None
context = None
page = None


# =========================================
# START BROWSER ONCE
# =========================================

async def start_browser():

    global playwright_instance
    global browser
    global context
    global page

    playwright_instance = await async_playwright().start()

    browser = await playwright_instance.chromium.launch(
        headless=True,  # False looks more human but slower
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )

    # create persistent-like context
    context = await browser.new_context(
        viewport={
            "width": random.randint(1280, 1920),
            "height": random.randint(720, 1080)
        },
        locale="en-US",
        user_agent=random.choice([
            # Chrome Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

            # Chrome Android
            "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        ])
    )

    page = await context.new_page()

    logging.info("Persistent browser started")


# =========================================
# HUMAN-LIKE OPEN
# =========================================

async def open_real(url):

    global page

    try:

        logging.info(f"Opening: {url}")

        # random pre-delay
        await asyncio.sleep(
            random.uniform(1.5, 4.2)
        )

        # open page
        await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=45000
        )

        # random reading time
        await asyncio.sleep(
            random.uniform(2.5, 7)
        )

        # slight random scroll
        try:

            scroll_amount = random.randint(200, 1200)

            await page.mouse.wheel(0, scroll_amount)

            await asyncio.sleep(
                random.uniform(1, 3)
            )

        except:
            pass

        # occasional mouse move
        try:

            await page.mouse.move(
                random.randint(100, 800),
                random.randint(100, 600),
                steps=random.randint(10, 30)
            )

        except:
            pass

        logging.info("Opened successfully")

    except Exception as e:

        logging.info(f"open_real error: {e}")


# =========================================
# OPTIONAL:
# REFRESH CONTEXT EVERY 50 TASKS
# =========================================

TASK_COUNT = 0

async def refresh_context_if_needed():

    global TASK_COUNT
    global context
    global page

    TASK_COUNT += 1

    if TASK_COUNT % 50 == 0:

        logging.info("Refreshing browser context")

        await context.close()

        context = await browser.new_context()

        page = await context.new_page()


# ---------- extract + open ----------
async def handle_button(btn, msg):
    try:
        logging.info("1")
        bot_entity = await mrsyd.get_entity(bot_id)
        logging.info("2")
        await open_real(btn.url)
        logging.info("2.5")
        if isinstance(btn, KeyboardButtonUrl):
            print("3")
            url = btn.url
            logging.info("URL found:", url)
            await open_real(url)
        else:
            logging.info("4")
            await msg.click(text=btn.text)

    except Exception as e:
        logging.info(e)
        import traceback
        traceback.print_exc()




@mrsyd.on(events.NewMessage(from_users=bot_id))
async def save_ids(event):

    global PHOTO_MSG_IDS
    global SUBSCRIBE_MSG_IDS
    global TURN
    global GENERAL

    msg = event.message

    if TURN is True:

        # save photo message ids
        if msg.photo:

            PHOTO_MSG_IDS.add(msg.id)

            logging.info(f"Saved photo msg id: {msg.id}")
            return 
        # save subscribe ids
        if (
            msg.raw_text and
            msg.raw_text.startswith(
                "💡 Получай Звёзды за простые задания! 👇\n\n1. Нажми «Подписаться», дождись"
            )
        ):

            SUBSCRIBE_MSG_IDS.add(msg.id)

            logging.info(f"Saved subscribe msg id: {msg.id}")
            return
    elif msg.raw_text and msg.buttons:

        text = msg.raw_text.strip()

        if text.startswith(
            "💡 Получай Звёзды за простые задания! 👇\n\n🟢 Подпишись на канал и нажми «Подтвердить»"
        ):

            # =========================
            # GENERAL TRUE
            # =========================

            if GENERAL or TURN:

                logging.info("Detected subscribe task message")

                for row in msg.buttons:
                    for btn in row:

                        if btn.text and "Пропустить" in btn.text:

                            logging.info(
                                f"Clicking skip button: {btn.text}"
                            )

                            await handle_button(btn, msg)

                            await asyncio.sleep(3)

                            return

            # =========================
            # GENERAL FALSE
            # =========================

            else:

                await mrsyd.send_message(
                    ADMIN_ID,
                    f"Message ID: {msg.id}\n\n{text}"
                )
# =========================
# MAIN COMMAND
# =========================

@mrsyd.on(events.NewMessage(from_users=ADMINS, pattern="catch it"))
async def catch_it(event):
    global TURN
    global PHOTO_MSG_IDS
    global SUBSCRIBE_MSG_IDS

    TURN = True

    PHOTO_MSG_IDS.clear()
    SUBSCRIBE_MSG_IDS.clear()

    await event.reply("Started collecting tasks")

    # =========================================
    # SEND "💎 Задания" FOR 55 MINUTES
    # =========================================

    start_time = asyncio.get_event_loop().time()

    while (asyncio.get_event_loop().time() - start_time) < (55 * 60):

        try:

            await mrsyd.send_message(bot_id, "💎 Задания")
            wait_time = random.randint(6, 10)
            logging.info(f"Sleeping for {wait_time} seconds")
            await asyncio.sleep(wait_time)
        except Exception as e:
            logging.info(e)
            import traceback
            traceback.print_exc()
    TURN = False
    logging.info("Finished collecting IDs")

    # =========================================
    # MERGE + SORT IDS
    # =========================================

    all_ids = sorted(
        PHOTO_MSG_IDS.union(SUBSCRIBE_MSG_IDS)
    )

    logging.info(f"Total IDs found: {len(all_ids)}")

    # =========================================
    # PROCESS ALL IDS
    # =========================================

    for msg_id in all_ids:

        try:

            msg = await mrsyd.get_messages(bot_id, ids=msg_id)

            if not msg:
                continue

            logging.info(f"Processing msg id: {msg_id}")

            # =================================
            # PHOTO MESSAGE
            # =================================

            if msg_id in PHOTO_MSG_IDS:

                if msg.buttons:

                    all_buttons = []

                    for row in msg.buttons:
                        for btn in row:
                            all_buttons.append(btn)

                    # first button
                    if len(all_buttons) >= 1:

                        btn1 = all_buttons[0]

                        logging.info(
                            f"Clicking first button: {btn1.text}"
                        )

                        await handle_button(btn1, msg)

                        await asyncio.sleep(5)

                    # second button
                    if len(all_buttons) >= 2:

                        btn2 = all_buttons[1]

                        logging.info(
                            f"Clicking second button: {btn2.text}"
                        )

                        await handle_button(btn2, msg)

                        await asyncio.sleep(5)

            # =================================
            # SUBSCRIBE MESSAGE
            # =================================

            elif msg_id in SUBSCRIBE_MSG_IDS:

                if msg.buttons:

                    done = False

                    for row in msg.buttons:
                        for btn in row:
                            if (
                                btn.text and
                                "Подтвердить" in btn.text
                            ):
                                logging.info(
                                    f"Clicking confirm button: {btn.text}"
                                )
                                await handle_button(btn, msg)
                                await asyncio.sleep(5)
                                done = True
                                break
                        if done:
                            break
        except Exception as e:
            logging.info(e)
            import traceback
            traceback.print_exc()
    await event.reply("Finished all tasks")


# ---------- open in real browser ----------



# ---------- main handler ----------
#@mrsyd.on(events.NewMessage(from_users=bot_id))
async def handlllller(event):
    msg = event.message

    if msg.photo and msg.buttons:
        logging.info("Hello from Docker")
        print("Image detected")

        targets = ["Открыть", "Вперёд!", "Посмотреть", "Присоединяйся!", "Играть!", "Забрать награду!"]

        for row in msg.buttons:
            for btn in row:
                if btn.text and any(t in btn.text for t in targets):
                    logging.info("Matched:", btn.text)

                    await handle_button(btn, msg)
                    logging.info("Yo")

                    # avoid spam clicking too fast
                    await asyncio.sleep(5)




@mrsyd.on(events.NewMessage(from_users=ADMINS, pattern=r"^press\s+\d+-\d+$"))
async def press_button(event):
    try:

        text = event.raw_text.strip()

        # extract row-column
        match = re.search(r"press\s+(\d+)-(\d+)", text)

        if not match:
            await event.reply("Invalid format")
            return

        row = int(match.group(1)) - 1
        column = int(match.group(2)) - 1

        # get latest bot message
        msgs = await mrsyd.get_messages(
            bot_id,
            limit=1
        )

        if not msgs:
            await event.reply("No messages found")
            return

        msg = msgs[0]

        if not msg.buttons:
            await event.reply("Last message has no buttons")
            return

        # validate row
        if row >= len(msg.buttons):
            await event.reply("Invalid row")
            return

        # validate column
        if column >= len(msg.buttons[row]):
            await event.reply("Invalid column")
            return

        btn = msg.buttons[row][column]

        await msg.click(row, column)

        await event.reply(
            f"Pressed button [{row+1}-{column+1}] : {btn.text}"
        )

    except Exception as e:

        import traceback
        traceback.print_exc()

        await event.reply(f"Error: {e}")



from telethon.tl.types import KeyboardButtonUrl


@mrsyd.on(events.NewMessage(from_users=ADMINS, pattern=r"^last"))
async def last_message(event):
    try:
        msgs = await mrsyd.get_messages(
            bot_id,
            limit=1
        )
        if not msgs:
            await event.reply("No messages found")
            return
        msg = msgs[0]
        text = msg.raw_text if msg.raw_text else "No text"
        button_text = ""

        if msg.buttons:
            for row_index, row in enumerate(msg.buttons, start=1):
                for col_index, btn in enumerate(row, start=1):
                    if isinstance(btn, KeyboardButtonUrl):
                        button_text += (
                            f"\n{btn.text} : {btn.url} "
                            f"({row_index}, {col_index})"
                        )

        await event.reply(
            f"Last Message\n\n"
            f"ID: `{msg.id}`\n\n"
            f"Text:\n{text}\n\n"
            f"URL Buttons:"
            f"{button_text if button_text else ' None'}"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        await event.reply(f"Error: {e}")
        
@mrsyd.on(events.NewMessage(from_users=ADMINS, pattern="balance"))
async def balance_cmd(event):
    try:
        await mrsyd.send_message(
            bot_id,
            "🎁 Вывести Подарки"
        )

        # wait for bot response
        await asyncio.sleep(10)

        # get latest message from bot
        msgs = await mrsyd.get_messages(
            bot_id,
            limit=1
        )

        if not msgs:
            await event.reply("No response received")
            return

        last_msg = msgs[0]

        text = last_msg.raw_text if last_msg.raw_text else "Empty message"

        # send message id + text
        await mrsyd.send_message(
            event.chat_id,
            f"Message ID: `{last_msg.id}`\n\n{text}"
        )

    except Exception as e:

        logging.info(e)

        import traceback
        traceback.print_exc()

        await event.reply(f"Error: {e}")



from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import StartBotRequest
from telethon.errors import (
    UserAlreadyParticipantError,
    InviteHashExpiredError,
    InviteHashInvalidError
)



@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^open\s+(.+)"
))
async def open_link(event):

    try:

        text = event.raw_text.strip()

        match = re.match(r"^open\s+(.+)", text)

        if not match:
            return

        link = match.group(1).strip()

        await event.reply(f"Processing:\n{link}")

        # =========================================
        # CLEAN LINK
        # =========================================

        link = link.replace("https://", "")
        link = link.replace("http://", "")

        # =========================================
        # INVITE LINK
        # =========================================

        # t.me/+xxxx
        # telegram.me/+xxxx
        # t.me/joinchat/xxxx

        if (
            "t.me/+" in link or
            "telegram.me/+" in link or
            "joinchat/" in link
        ):

            invite_hash = None

            if "joinchat/" in link:
                invite_hash = link.split("joinchat/")[1]

            elif "+" in link:
                invite_hash = link.split("+")[1]

            try:

                result = await mrsyd(
                    ImportChatInviteRequest(invite_hash)
                )

                await event.reply(
                    f"Joined invite successfully"
                )

            except UserAlreadyParticipantError:

                await event.reply(
                    "Already joined"
                )

            except (
                InviteHashExpiredError,
                InviteHashInvalidError
            ):

                await event.reply(
                    "Invalid or expired invite"
                )

            except Exception as e:

                await event.reply(
                    f"Invite error:\n{e}"
                )

            return

        # =========================================
        # NORMAL USERNAME LINKS
        # =========================================

        # t.me/username
        # t.me/bot?start=abc
        # t.me/bot/app
        # t.me/channel

        if "t.me/" in link:

            path = link.split("t.me/")[1]

            # remove trailing /
            path = path.strip("/")

            # =====================================
            # BOT START LINK
            # =====================================

            # example:
            # t.me/TestBot?start=abc123

            if "?start=" in path:

                bot_username = path.split("?start=")[0]

                start_param = path.split("?start=")[1]

                entity = await mrsyd.get_entity(
                    bot_username
                )

                await mrsyd.send_message(
                    bot_username,
                    f"/start {start_param}"
                )

                await event.reply(
                    f"Started bot:\n"
                    f"@{bot_username}\n\n"
                    f"Parameter:\n{start_param}"
                )

                return

            # =====================================
            # WEBAPP LINKS
            # =====================================

            # t.me/bot/app
            # t.me/bot/app?startapp=xxx

            elif "/" in path:

                parts = path.split("/")

                username = parts[0]

                await event.reply(
                    f"Detected possible webapp:\n"
                    f"@{username}"
                )

                try:

                    await mrsyd.send_message(
                        username,
                        "/start"
                    )

                except:
                    pass

                return

            # =====================================
            # NORMAL CHANNEL/GROUP/BOT
            # =====================================

            else:

                username = path

                try:

                    await mrsyd(
                        JoinChannelRequest(username)
                    )

                    await event.reply(
                        f"Joined:\n@{username}"
                    )

                except UserAlreadyParticipantError:

                    await event.reply(
                        f"Already joined:\n@{username}"
                    )

                except Exception:

                    # maybe bot/private user

                    try:

                        await mrsyd.send_message(
                            username,
                            "/start"
                        )

                        await event.reply(
                            f"Started bot/user:\n@{username}"
                        )

                    except Exception as e:

                        await event.reply(
                            f"Failed:\n{e}"
                        )

                return

        await event.reply("Unsupported link")

    except Exception as e:

        import traceback
        traceback.print_exc()

        await event.reply(f"Error:\n{e}")

import asyncio
import re
import asyncio

SYDFLAG = False

async def click_loop(msg_id, event):
    global SYDFLAG
    first = True
    click_count = 0

    while SYDFLAG and click_count < 30:
        try:
            msg = await mrsyd.get_messages("patrickstarsrobot", ids=msg_id)
            last_msg_id = (await mrsyd.get_messages("patrickstarsrobot", limit=1))[0].id
            if not msg: 
                return await event.reply(f"No Message {last_msg_id}")
            if first:
                await event.reply(f"Message {msg.text}")
                first = False
                
            if msg.buttons:
                clicked = False

                for row in msg.buttons:
                    for btn in row:
                        if "Кликер" in btn.text:
                            await msg.click(text="✨ Кликер")
                            clicked = True
                            click_count += 1
                            break
                    if clicked:
                        break

                if clicked:
                    logging.info("✅ Clicked 'Кликер'")
                else:
                    return await event.reply("❌ Button not found")

            else:
                return await event.reply("❌n No buttons in message")

        except Exception as e:
            await event.reply(f"⚠️ Error: {e}")

        # wait 6 minutes
        for _ in range(random.randint(620, 1400)):
            if not SYDFLAG: return
            await asyncio.sleep(1)



ADMIN_ID = 1733124290  # replace with your admin id

@mrsyd.on(events.NewMessage(from_users=ADMIN_ID, pattern=r"(?i)(24 process|sydflag false|start auto process)"))
async def auto_runner(event):
    global SYDFLAG

    text = event.raw_text.strip()

    # START LOOP
    if text.startswith("24 process"):
        try:
            msg_id = int(text.split()[2])
            SYDFLAG = True

            await event.reply("🚀 Started clicking every 6 minutes")

            # run loop in background
            asyncio.create_task(click_loop(msg_id, event))
            return 
        except Exception as e:
            await event.reply(f"⚠️ Error: {e}")
            return 

    # STOP LOOP
    elif text.lower() == "sydflag false":
        SYDFLAG = False
        await event.reply("🛑 SYDFLAG set to False. Stopping loop.")
        return
        
    msg = event.message

    if msg.text and "start auto process" in msg.text.lower():
        logging.info("Auto process triggered")

        start_id = None
        last_id = None

        # --- SEND 300 MESSAGES ---
        for i in range(30):
            try:
                sent = await mrsyd.send_message(bot_id, "💎 Задания")

                if start_id is None:
                    start_id = sent.id

                last_id = sent.id

                logging.info(f"Sent {i+1}/300 → id {sent.id}")

                await asyncio.sleep(10)

            except Exception as e:
                logging.error(f"Send failed at {i}: {e}")
                await asyncio.sleep(60)

        # --- DEFINE RANGE ---
        if start_id and last_id:
            end_id = last_id + 3

            logging.info(f"Auto range: {start_id} → {end_id}")

            # --- PROCESS LOOP ---
            for message_id in range(start_id, end_id + 1):
                try:
                    target_msg = await mrsyd.get_messages(bot_id, ids=message_id)

                    if not target_msg:
                        continue

                    # reuse your logic style
                    if target_msg.buttons:
                        for row in target_msg.buttons:
                            for btn in row:
                                if not btn.text:
                                    continue

                                # PHOTO FLOW
                                if target_msg.photo and any(t in btn.text for t in ["Открыть", "Вперёд!", "Посмотреть", "Присоединяйся!", "Играть!", "Забрать награду!"]):
                                    logging.info(f"[AUTO PHOTO] {btn.text}")
                                    await handle_button(btn, target_msg)
                                    await asyncio.sleep(3)
                                    break

                                # NORMAL BUTTON FLOW
                               # if any(t in btn.text for t in ["Открыть", "Вперёд!", "Посмотреть", "Присоединяйся!", "Играть!", "Забрать награду!"]):
                                    #logging.info(f"[AUTO TEXT] {btn.text}")
                                 #   await target_msg.click(text=btn.text)
                                    #await asyncio.sleep(3)
                                #    break

                                # CONFIRM FLOW
                                if "Подтвердить" in btn.text:
                                    logging.info(f"[AUTO CONFIRM] {btn.text}")
                                    await target_msg.click(text=btn.text)
                                    await asyncio.sleep(2)
                                    break

                except Exception as e:
                    logging.error(f"Error processing {message_id}: {e}")


import re
@mrsyd.on(events.NewMessage(from_users=[7996790736], pattern=r"(?i)(🤖 ПРОВЕРКА НА|sydflag false|start auto)"))
async def solve_robot_check(event):
    message = event.message
    try:
        await asyncio.sleep(6)
        if not message.text:
            return False

        text = message.text

        # Find math expression like: 30 + 7
        match = re.search(r'(\d+)\s*\+\s*(\d+)', text)

        if not match:
            return False

        num1 = int(match.group(1))
        num2 = int(match.group(2))

        answer = str(num1 + num2)

        # Search buttons
        if not message.buttons:
            return False

        for row in message.buttons:
            for btn in row:
                if btn.text.strip() == answer:
                    await btn.click()
                    logging.info(f"Clicked answer button: {answer}")
                    return True

        logging.info("Answer button not found")
        return False

    except Exception as e:
        logging.info(f"solve_robot_check error: {e}")
        return False
