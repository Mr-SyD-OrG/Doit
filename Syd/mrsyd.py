from telethon import events
import asyncio
import re
from bot import mrsyd
from .web import open_real
import random
from telethon.tl.types import PeerChannel
import logging
from datetime import datetime, timedelta
from telethon.tl.types import PeerUser
from pytz import timezone

logging.basicConfig(level=logging.INFO)


client = mrsyd

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


    
@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"^send\s"))
async def handle_send_message(event):
    text = event.message.raw_text.strip()

    # Format: send @username Your message
    match = re.match(
        r'^send\s+@?(\w{5,32})\s+(.+)',
        text,
        re.IGNORECASE
    )

    if not match:
        await event.reply(
            "❌ Invalid format.\nUse:\nsend @username Your message"
        )
        return

    username = match.group(1)
    message_text = match.group(2).strip()

    try:
        user = await event.client.get_entity(username)

        await event.client.send_message(
            user,
            message_text
        )

        await event.reply(
            f"✅ Sent message to @{username}"
        )

    except Exception as e:
        await event.reply(
            f"❌ Failed to send message to @{username}\nError: {e}"
        )
            

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
import time
from telethon import events
from telethon.tl.types import KeyboardButtonUrl
from playwright.async_api import async_playwright

PHOTO_TASKS = {}
SUBSCRIBE_TASKS = {}
GENERAL = False
TURN = False
STOPP = True
ADMIN_ID = 1733124290
bot_id = 8006795826  # replace 8097888032  g/c 8006795826
TASK_LIFETIME = 3600
MINIMUM_REMAINING_LIFE = 120
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

@mrsyd.on(events.NewMessage(from_users=[1733124290], pattern=r"break"))
async def had_on_tigger(event):
    global STOPP
    STOPP = False
    await event.reply("STOPPinggggg")




import random
import asyncio
import logging
from playwright.async_api import async_playwright

playwright_instance = None
browser = None
context = None
page = None

TASK_COUNT = 0


# =========================================
# START BROWSER ONCE
# =========================================

async def start_browsers():

    global playwright_instance
    global browser
    global context
    global page

    playwright_instance = await async_playwright().start()

    browser = await playwright_instance.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )

    # persistent-like context
    context = await browser.new_context(
        viewport={
            "width": random.randint(1280, 1920),
            "height": random.randint(720, 1080)
        },
        locale="en-US",
        user_agent=random.choice([

            # Windows Chrome
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

            # Android Chrome
            "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        ])
    )

    # SINGLE PAGE
    page = await context.new_page()

    logging.info("Persistent browser started")


# =========================================
# OPEN URL USING SAME PAGE
# =========================================

async def open_reals(url):
    global page
    global TASK_COUNT

    try:

        TASK_COUNT += 1

        logging.info(f"Opening: {url}")

        # random pre delay
        await asyncio.sleep(
            random.uniform(1.5, 4.2)
        )

        # reuse SAME page
        await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=20000
        )

        # human reading time
        await asyncio.sleep(
            random.uniform(2.5, 7)
        )

        # random scroll
        try:
            if random.random() < 0.7:
                scroll_amount = random.randint(200, 1200)
                await page.mouse.wheel(0, scroll_amount)
                await asyncio.sleep(random.uniform(1, 3))

        except:
            pass

        # random mouse move
        try:

            await page.mouse.move(
                random.randint(100, 800),
                random.randint(100, 600),
                steps=random.randint(10, 30)
            )

        except:
            pass

        logging.info("Opened successfully")

        # =====================================
        # REFRESH CONTEXT EVERY 50 TASKS
        # =====================================

        if TASK_COUNT % 50 == 0:

            logging.info("Refreshing context")

            try:

                # CLOSE OLD PAGE
                await page.close()

            except:
                pass

            try:

                await context.close()

            except:
                pass

            # CREATE NEW CONTEXT
            context_new = await browser.new_context(
                viewport={
                    "width": random.randint(1280, 1920),
                    "height": random.randint(720, 1080)
                },
                locale="en-US"
            )

            globals()["context"] = context_new

            # CREATE NEW SINGLE PAGE
            page_new = await context.new_page()

            globals()["page"] = page_new

            logging.info("Context refreshed")

    except Exception as e:

        logging.info(f"open_real error: {e}")

async def handle_buttonss(btn, msg):
    try:
        logging.info("1")
        bot_entity = await mrsyd.get_entity(bot_id)
        logging.info("2")
        await open_real(btn.url)
        logging.info("2.5")
      #  if isinstance(btn, KeyboardButtonUrl):
         #   print("3")
     #       url = btn.url
      #      logging.info("URL found:", url)
     #       await open_real(url)
    #    else:
           # logging.info("4")
         #   await msg.click(text=btn.text)

    except Exception as e:
        logging.info(e)
        import traceback
        traceback.print_exc()





async def handle_button(btn, msg):

    try:
        if getattr(btn, "url", None):

            logging.info(
                f"URL found: {btn.url}"
            )

            await open_real(btn.url)

        # NORMAL BUTTON
        else:

            logging.info(
                f"Clicking normal button: {btn.text}"
            )

            await msg.click(text=btn.text)

    except Exception as e:

        logging.info(f"handle_button error: {e}")

        import traceback
        traceback.print_exc()

@mrsyd.on(events.NewMessage(from_users=bot_id))
async def save_ids(event):
    global PHOTO_TASKS
    global SUBSCRIBE_TASKS
    global TURN
    global GENERAL

    msg = event.message

    if TURN is True:

        # save photo message ids
        if msg.photo:
            urls = []
            if msg.buttons:
                for row in msg.buttons:
                    for btn in row:
                        if getattr(btn, "url", None):
                            urls.append(btn.url)
            if urls:

                PHOTO_TASKS[msg.id] = {
                    "urls": urls[:2],
                    "arrived": time.time()
                }

                logging.info(
                    f"Saved photo task: {msg.id}"
                )
            return
        # save subscribe ids
        if (
            msg.raw_text and
            msg.raw_text.startswith(
                "💡 Получай Звёзды за простые задания! 👇\n\n1. Нажми «Подписаться», дождись"
            )
        ):

            SUBSCRIBE_TASKS[msg.id] = {
                "arrived": time.time()
            }

            logging.info(f"Saved subscribe msg id: {msg.id}")
            return 
    elif msg.raw_text and msg.buttons:

        text = msg.raw_text.strip()

        if ("💡 Получай Звёзды за простые задания!" in text and "🟢 Подпишись на канал" in text):
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
    global TURN, STOPP
    global PHOTO_TASKS
    global SUBSCRIBE_TASKS

    TURN = True

    #PHOTO_MSG_IDS.clear()
   # SUBSCRIBE_MSG_IDS.clear()

    await event.reply("Started collecting tasks")

    # =========================================
    # SEND "💎 Задания" FOR 55 MINUTES
    # =========================================

    start_time = asyncio.get_event_loop().time()

    while ((asyncio.get_event_loop().time() - start_time) < (38 * 60) and STOPP is True):

        try:

            await mrsyd.send_message(bot_id, "💎 Задания")
            wait_time = random.uniform(4.5, 9)
            logging.info(f"Sleeping for {wait_time} seconds")
            await asyncio.sleep(wait_time)
        except Exception as e:
            logging.info(e)
            import traceback
            traceback.print_exc()
    await asyncio.sleep(1.5)
    
    STOPP = True
    try: 
        await backup_ids(event)
    except:
        pass
    logging.info("Finished collecting IDs")

    all_ids = sorted(
        set(PHOTO_TASKS.keys()).union(
            SUBSCRIBE_TASKS.keys()
        )
    )

    logging.info(f"Total IDs found: {len(all_ids)}")

    # =========================================
    # PROCESS ALL IDS
    # =========================================

    for msg_id in all_ids:
        current_time = time.time()
        try:
            if msg_id in PHOTO_TASKS:
                task = PHOTO_TASKS.get(msg_id)

                if not task:
                    continue

                age = (
                    current_time - task["arrived"]
                )

                remaining = (
                    TASK_LIFETIME - age
                )

                if remaining < MINIMUM_REMAINING_LIFE:

                    logging.info(
                        f"Skipped expired photo task: {msg_id}"
                    )

                    PHOTO_TASKS.pop(
                        msg_id,
                        None
                    )

                    continue

                urls = task["urls"]

                logging.info(
                    f"Processing photo task: {msg_id}"
                )

                for url in urls:

                    await open_real(url)
                    logging.info(url)

                    await asyncio.sleep(
                        random.uniform(
                            0.01,
                            0.08
                        )
                    )

                PHOTO_TASKS.pop(
                    msg_id,
                    None
                )

            elif msg_id in SUBSCRIBE_TASKS:

                task = SUBSCRIBE_TASKS.get(msg_id)

                if not task:
                    continue

                age = (
                    current_time - task["arrived"]
                )

                remaining = (
                    TASK_LIFETIME - age
                )

                if remaining < MINIMUM_REMAINING_LIFE:

                    logging.info(
                        f"Skipped expired subscribe task: {msg_id}"
                    )

                    SUBSCRIBE_TASKS.pop(
                        msg_id,
                        None
                    )

                    continue

                msg = await mrsyd.get_messages(
                    bot_id,
                    ids=msg_id
                )

                if not msg:

                    SUBSCRIBE_TASKS.pop(
                        msg_id,
                        None
                    )

                    continue

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
                                await asyncio.sleep(random.uniform(0.1, 0.4))
                                await handle_button(btn, msg)
                                await asyncio.sleep(random.uniform(0.01, 0.1))
                                done = True
                                break
                        if done:
                            break
                          
            SUBSCRIBE_TASKS.pop(
                    msg_id,
                    None
            )
        except Exception as e:
            logging.info(e)
            import traceback
            traceback.print_exc()

    TURN = False
    await event.reply("Finished all tasks")


# ---------- open in real browser ----------

# =====================================
# CLEAR IDS
# =====================================

@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^clear$"
))
async def clear_ids(event):

    global PHOTO_TASKS
    global SUBSCRIBE_TASKS

    photo_count = len(PHOTO_TASKS)
    subscribe_count = len(SUBSCRIBE_TASKS)

    PHOTO_TASKS.clear()
    SUBSCRIBE_TASKS.clear()

    await event.reply(
        f"Cleared tasks\n\n"
        f"Photo tasks removed: {photo_count}\n"
        f"Subscribe tasks removed: {subscribe_count}"
    )

# =====================================
# SEE COUNTS
# =====================================

@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^seecount$"
))
async def see_count(event):

    global PHOTO_TASKS
    global SUBSCRIBE_TASKS

    photo_count = len(PHOTO_TASKS)
    subscribe_count = len(SUBSCRIBE_TASKS)

    total = photo_count + subscribe_count

    await event.reply(
        f"Stored ID Counts\n\n"
        f"Photo IDs: {photo_count}\n"
        f"Subscribe IDs: {subscribe_count}\n"
        f"Total IDs: {total}"
    )

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

import re
from telethon import events


@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^getpress\s+\d+\s+\d+-\d+$"
))
async def getpress_button(event):

    try:

        text = event.raw_text.strip()

        # =====================================
        # EXTRACT MESSAGE ID + ROW/COLUMN
        # =====================================

        match = re.search(
            r"^getpress\s+(\d+)\s+(\d+)-(\d+)$",
            text
        )

        if not match:

            await event.reply("Invalid format")

            return

        message_id = int(match.group(1))

        row = int(match.group(2)) - 1
        column = int(match.group(3)) - 1

        # =====================================
        # GET MESSAGE
        # =====================================

        msg = await mrsyd.get_messages(
            bot_id,
            ids=message_id
        )

        if not msg:

            await event.reply("Message not found")

            return

        # =====================================
        # CHECK BUTTONS
        # =====================================

        if not msg.buttons:

            await event.reply(
                "Message has no buttons"
            )

            return

        # validate row
        if row >= len(msg.buttons):

            await event.reply("Invalid row")

            return

        # validate column
        if column >= len(msg.buttons[row]):

            await event.reply("Invalid column")

            return

        # =====================================
        # PRESS BUTTON
        # =====================================

        btn = msg.buttons[row][column]

        await msg.click(row, column)

        await event.reply(
            f"Pressed button\n\n"
            f"Message ID: `{message_id}`\n"
            f"Position: [{row+1}-{column+1}]\n"
            f"Text: {btn.text}"
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

        text = (
            msg.raw_text
            if msg.raw_text
            else "No text"
        )

        # =====================================
        # BUTTON INFO
        # =====================================

        button_text = ""

        if msg.buttons:

            for row_index, row in enumerate(
                msg.buttons,
                start=1
            ):

                for col_index, btn in enumerate(
                    row,
                    start=1
                ):

                    # detect url using btn.url
                    if getattr(btn, "url", None):

                        button_text += (
                            f"\n[{row_index}, {col_index}] "
                            f"{btn.text} : {btn.url}"
                        )

                    else:

                        button_text += (
                            f"\n[{row_index}, {col_index}] "
                            f"{btn.text}"
                        )

        else:

            button_text = "\nNone"

        # =====================================
        # REPLY
        # =====================================

        await event.reply(
            f"Last Message\n\n"
            f"ID: `{msg.id}`\n\n"
            f"Text:\n{text}\n\n"
            f"Buttons:"
            f"{button_text}"
        )

    except Exception as e:

        import traceback
        traceback.print_exc()

        await event.reply(f"Error: {e}")
      
#@mrsyd.on(events.NewMessage(from_users=ADMINS, pattern=r"^last"))
async def lsssast_message(event):

    try:

        msgs = await mrsyd.get_messages(
            bot_id,
            limit=1
        )

        if not msgs:

            await event.reply("No messages found")

            return

        msg = msgs[0]

        text = (
            msg.raw_text
            if msg.raw_text
            else "No text"
        )

        # =====================================
        # BUTTON INFO
        # =====================================

        button_text = ""

        if msg.buttons:

            for row_index, row in enumerate(
                msg.buttons,
                start=1
            ):

                for col_index, btn in enumerate(
                    row,
                    start=1
                ):

                    # URL BUTTON
                    if isinstance(btn, KeyboardButtonUrl):

                        button_text += (
                            f"\n[{row_index}, {col_index}] "
                            f"{btn.text} : {btn.url}"
                        )

                    # NORMAL BUTTON
                    else:

                        button_text += (
                            f"\n[{row_index}, {col_index}] "
                            f"{btn.text}"
                        )

        else:

            button_text = "\nNone"

        # =====================================
        # REPLY
        # =====================================

        await event.reply(
            f"Last Message\n\n"
            f"ID: `{msg.id}`\n\n"
            f"Text:\n{text}\n\n"
            f"Buttons:"
            f"{button_text}"
        )

    except Exception as e:

        import traceback
        traceback.print_exc()

        await event.reply(f"Error: {e}")

@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^get\s+\d+$"
))
async def get_message(event):

    try:

        text_input = event.raw_text.strip()

        match = re.search(r"^get\s+(\d+)$", text_input)

        if not match:

            await event.reply("Invalid format")

            return

        message_id = int(match.group(1))

        # =====================================
        # GET MESSAGE
        # =====================================
        entity = await mrsyd.get_entity(bot_id)

        msg = await mrsyd.get_messages(
            bot_id,
            ids=message_id
        )

        if not msg:

            await event.reply("Message not found")

            return

        # =====================================
        # MESSAGE TEXT
        # =====================================

        text = (
            msg.raw_text
            if msg.raw_text
            else "No text"
        )

        # =====================================
        # BUTTON INFO
        # =====================================

        button_text = ""

        if msg.buttons:

            for row_index, row in enumerate(
                msg.buttons,
                start=1
            ):

                for col_index, btn in enumerate(
                    row,
                    start=1
                ):

                    # URL BUTTON
                    if isinstance(btn, KeyboardButtonUrl):

                        button_text += (
                            f"\n[{row_index}, {col_index}] "
                            f"{btn.text} : {btn.url}"
                        )

                    # NORMAL BUTTON
                    else:

                        button_text += (
                            f"\n[{row_index}, {col_index}] "
                            f"{btn.text}"
                        )

        else:

            button_text = "\nNone"

        # =====================================
        # FORWARD MEDIA IF EXISTS
        # =====================================

        if msg.media:

            await mrsyd.forward_messages(
                event.chat_id,
                msg
            )

        # =====================================
        # SEND DETAILS
        # =====================================

        await event.reply(
            f"Message ID: `{msg.id}`\n\n"
            f"Text:\n{text}\n\n"
            f"Buttons:"
            f"{button_text}"
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

        text = (
            last_msg.raw_text
            if last_msg.raw_text
            else "Empty message"
        )

        # =====================================
        # BUTTON INFO
        # =====================================

        buttons_text = ""

        if last_msg.buttons:

            for row_index, row in enumerate(
                last_msg.buttons,
                start=1
            ):

                for col_index, btn in enumerate(
                    row,
                    start=1
                ):

                    buttons_text += (
                        f"\n[{row_index}, {col_index}] "
                        f"{btn.text}"
                    )

        else:

            buttons_text = "\nNo buttons"

        # =====================================
        # SEND RESULT
        # =====================================

        await mrsyd.send_message(
            event.chat_id,
            f"Message ID: `{last_msg.id}`\n\n"
            f"Text:\n{text}\n\n"
            f"Buttons:"
            f"{buttons_text}"
        )

    except Exception as e:

        logging.info(e)

        import traceback
        traceback.print_exc()

        await event.reply(f"Error: {e}")

@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^status$"
))
async def status_cmd(event):

    try:

        # =====================================
        # GET LAST 8 MESSAGES
        # =====================================

        msgs = await mrsyd.get_messages(
            bot_id,
            limit=8
        )

        if not msgs:
            await event.reply("No messages found")
            return

        result = "Last 8 Messages\n\n"

        # oldest first
        msgs = list(reversed(msgs))

        for msg in msgs:

            text = (
                msg.raw_text
                if msg.raw_text
                else "No text"
            )

            # limit huge messages
            if len(text) > 300:

                text = text[:300] + "..."

            result += (
                f"ID: `{msg.id}`\n"
                f"{text}\n\n"
                f"====================\n\n"
            )

        # =====================================
        # SEND RESULT
        # =====================================

        await event.reply(result)

    except Exception as e:

        import traceback
        traceback.print_exc()

        await event.reply(f"Error: {e}")

@mrsyd.on(events.NewMessage(from_users=ADMINS, pattern=r"^task$"))
async def task_cmd(event):

    try:

        # =====================================
        # SEND TASK COMMAND
        # =====================================

        await mrsyd.send_message(
            bot_id,
            "💎 Задания"
        )

        # wait for bot reply
        await asyncio.sleep(10)

        # =====================================
        # GET LAST MESSAGE
        # =====================================

        msgs = await mrsyd.get_messages(
            bot_id,
            limit=1
        )

        if not msgs:

            await event.reply(
                "No response received"
            )

            return

        msg = msgs[0]

        # =====================================
        # FORWARD IMAGE/MEDIA DIRECTLY
        # =====================================

        if msg.media:

            await mrsyd.forward_messages(
                event.chat_id,
                msg
            )

        # =====================================
        # TEXT
        # =====================================

        text = (
            msg.raw_text
            if msg.raw_text
            else "No text"
        )

        # =====================================
        # BUTTON INFO
        # =====================================

        buttons_info = ""

        if msg.buttons:

            for row_index, row in enumerate(
                msg.buttons,
                start=1
            ):

                for col_index, btn in enumerate(
                    row,
                    start=1
                ):

                    # detect url using btn.url
                    if getattr(btn, "url", None):

                        buttons_info += (
                            f"\n[{row_index}, {col_index}] "
                            f"{btn.text} : {btn.url}"
                        )

                    # normal button
                    else:

                        buttons_info += (
                            f"\n[{row_index}, {col_index}] "
                            f"{btn.text}"
                        )

        else:

            buttons_info = "\nNo buttons"

        # =====================================
        # SEND DETAILS
        # =====================================

        await mrsyd.send_message(
            event.chat_id,
            f"Message ID: `{msg.id}`\n\n"
            f"Text:\n{text}\n\n"
            f"Buttons:"
            f"{buttons_info}"
        )

    except Exception as e:

        logging.info(e)

        import traceback
        traceback.print_exc()

        await event.reply(
            f"Error: {e}"
        )

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
                    entity = await mrsyd.get_entity(username)
                    if getattr(entity, "bot", False):

                        await mrsyd.send_message(username, "/start")
                        await event.reply(f"🤖 Started bot:\n@{username}")
                        return

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


@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^delphoto (\d+)$"
))
async def delete_photo_task(event):

    global PHOTO_TASKS

    try:

        msg_id = int(
            event.pattern_match.group(1)
        )

        if msg_id not in PHOTO_TASKS:

            await event.reply(
                f"Photo task not found: {msg_id}"
            )

            return

        PHOTO_TASKS.pop(msg_id, None)

        await event.reply(
            f"Removed photo task: {msg_id}"
        )

    except Exception as e:

        import traceback
        traceback.print_exc()

        await event.reply(
            f"Error: {e}"
        )
import json

# =========================================
# BACKUP
# =========================================

@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^backup$"
))
async def backup_ids(event):

    global PHOTO_TASKS
    global SUBSCRIBE_TASKS

    try:

        data = {
            "photo_tasks": PHOTO_TASKS,
            "subscribe_tasks": SUBSCRIBE_TASKS
        }

        file_name = "tasks_backup.json"

        with open(file_name, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )

        await mrsyd.send_file(
            event.chat_id,
            file_name,
            caption=(
                f"Backup created\n\n"
                f"Photo tasks: {len(PHOTO_TASKS)}\n"
                f"Subscribe tasks: {len(SUBSCRIBE_TASKS)}"
            )
        )

    except Exception as e:

        import traceback
        traceback.print_exc()

        await event.reply(
            f"Error: {e}"
        )

# =========================================
# RESTORE
# =========================================

@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^restore$"
))
async def restore_ids(event):

    global PHOTO_TASKS
    global SUBSCRIBE_TASKS

    try:

        if not event.is_reply:

            await event.reply(
                "Reply to backup file"
            )

            return

        reply = await event.get_reply_message()

        if not reply.file:

            await event.reply(
                "Reply must contain file"
            )

            return

        path = await reply.download_media()

        with open(path, "r", encoding="utf-8") as f:

            data = json.load(f)

        # convert string keys back to int
        PHOTO_TASKS = {
            int(k): v
            for k, v in data.get(
                "photo_tasks",
                {}
            ).items()
        }

        SUBSCRIBE_TASKS = {
            int(k): v
            for k, v in data.get(
                "subscribe_tasks",
                {}
            ).items()
        }

        await event.reply(
            f"Backup restored\n\n"
            f"Photo tasks: {len(PHOTO_TASKS)}\n"
            f"Subscribe tasks: {len(SUBSCRIBE_TASKS)}"
        )

    except Exception as e:

        import traceback
        traceback.print_exc()

        await event.reply(
            f"Error: {e}"
        )

@mrsyd.on(events.NewMessage(
    from_users=ADMINS,
    pattern=r"^check sub$"
))
async def check_subscribe_ids(event):

    global SUBSCRIBE_TASKS

    try:

        if not event.is_reply:

            await event.reply(
                "Reply to file containing subscribe ids"
            )

            return

        reply = await event.get_reply_message()

        if not reply.file:

            await event.reply(
                "Reply must contain file"
            )

            return

        path = await reply.download_media()

        with open(path, "r", encoding="utf-8") as f:

            data = json.load(f)

        # supports both list and dict
        if isinstance(data, dict):

            ids = list(
                map(
                    int,
                    data.get(
                        "subscribe_tasks",
                        {}
                    ).keys()
                )
            )

        else:

            ids = list(
                map(int, data)
            )

        pressed = 0
        failed = 0
        removed = 0

        for msg_id in ids:

            try:

                msg = await mrsyd.get_messages(
                    bot_id,
                    ids=msg_id
                )

                if not msg:

                    SUBSCRIBE_TASKS.pop(
                        msg_id,
                        None
                    )

                    removed += 1
                    continue

                if not msg.buttons:

                    continue

                # press first button
                await msg.click(0)

                pressed += 1

                await asyncio.sleep(
                    random.uniform(5, 8.5)
                )

            except Exception as e:

                failed += 1

                logging.info(
                    f"{msg_id} failed: {e}"
                )

        await event.reply(
            f"Finished checking subscribe ids\n\n"
            f"Pressed: {pressed}\n"
            f"Removed: {removed}\n"
            f"Failed: {failed}"
        )

    except Exception as e:

        import traceback
        traceback.print_exc()

        await event.reply(
            f"Error: {e}"
        )


import re
SYDFLAG = False
import asyncio
import random
import logging
from datetime import datetime
import pytz

ADMIN_ID = 1733124290

IST = pytz.timezone("Asia/Kolkata")

last_daily_run = None


async def daily_profile_check(event):

    try:
        await mrsyd.send_message(
            "patrickstarsrobot",
            "/start"
        )

        await asyncio.sleep(10)

        target_msg_id = None

        # get recent messages
        messages = await mrsyd.get_messages(
            "patrickstarsrobot",
            limit=15
        )

        for m in messages:

            if (
                m.text and
                re.search(
                    r'Получи\s+свою\s+личную\s+ссылку',
                    m.text
                )
            ):

                target_msg_id = m.id
                break

        if not target_msg_id:

            return await event.reply(
                "❌ Start message not found"
            )

        msg = await mrsyd.get_messages(
            "patrickstarsrobot",
            ids=target_msg_id
        )

        if not msg.buttons:

            return await event.reply(
                "❌ No buttons in start message"
            )

        clicked = False

        # click profile button
        for row in msg.buttons:
            for btn in row:

                if "Профиль" in btn.text:

                    await msg.click(
                        text=btn.text
                    )

                    clicked = True
                    break

            if clicked:
                break

        if not clicked:

            return await event.reply(
                "❌ Профиль button not found"
            )

        await asyncio.sleep(5)

        # check latest 2 messages
        messages = await mrsyd.get_messages(
            "patrickstarsrobot",
            limit=2
        )

        latest = None

        for m in messages:

            clean_text = (
                m.text
                .replace("**", "")
                .replace("__", "")
                .strip()
            ) if m.text else ""

            if clean_text.startswith("✨ Профиль"):

                latest = m
                break

        if not latest:

            return await event.reply(
                "❌ Profile message not found"
            )

        if not latest.buttons:

            return await event.reply(
                "❌ No buttons in profile message"
            )

        clicked = False

        # click Ежедневка button
        for row in latest.buttons:
            for btn in row:

                if "Ежедневка" in btn.text:

                    await latest.click(
                        text=btn.text
                    )

                    clicked = True
                    break

            if clicked:
                break

        if clicked:

            await event.reply(
                "✅ Daily reward claimed"
            )

        else:

            await event.reply(
                "❌ Ежедневка button not found"
            )

    except Exception as e:

        await event.reply(
            f"⚠️ Daily task error: {e}"
        )


async def wait_until_6am():

    while True:

        now = datetime.now(IST)

        # run only after 6 AM
        if now.hour >= 6:
            return

        await asyncio.sleep(30)


async def click_loop(msg_id, event, ttl=30):
    global SYDFLAG
    global last_daily_run

    while SYDFLAG:
        await wait_until_6am()
        now = datetime.now(IST)
        today = now.date()
        if (
            now.hour >= 6 and
            last_daily_run != today
        ):
            await daily_profile_check(event)
            last_daily_run = today
        
        click_count = 0
        first = True

        await event.reply("▶️ Starting today's clicking session")

        # 30 clicks daily
        while SYDFLAG and click_count < ttl:

            try:
                msg = await mrsyd.get_messages(
                    "patrickstarsrobot",
                    ids=msg_id
                )

                last_msg_id = (
                    await mrsyd.get_messages(
                        "patrickstarsrobot",
                        limit=1
                    )
                )[0].id

                if not msg:
                    await event.reply(
                        f"No Message {last_msg_id}"
                    )
                    SYDFLAG = False
                    return await auto_runner(event, ttl - click_count)
                    

                if first:
                    await event.reply(
                        f"Message {msg.text}"
                    )
                    first = False

                if msg.buttons:

                    clicked = False

                    for row in msg.buttons:
                        for btn in row:

                            if "Кликер" in btn.text:

                                await msg.click(
                                    text="✨ Кликер"
                                )

                                click_count += 1
                                clicked = True

                                logging.info(
                                    f"✅ Clicked {click_count}/30"
                                )

                                break

                        if clicked:
                            break

                    if not clicked:
                        return await event.reply(
                            "❌ Button not found"
                        )

                else:
                    return await event.reply(
                        "❌ No buttons in message"
                    )

            except Exception as e:
                await event.reply(f"⚠️ Error: {e}")

            # random wait
            now = datetime.now(IST)
            if now.hour < 13:
                wait_time = random.randint(620, 1400)
            elif now.hour < 18:
                wait_time = random.randint(420, 700)
            elif now.hour < 22:
                wait_time = random.randint(370, 400)
            else:
                wait_time = random.randint(370, 400)
            for _ in range(wait_time):
                if not SYDFLAG:
                    await event.reply(f"Stopped: {click_count}")
                    return
                await asyncio.sleep(1)

        await event.reply(
            "✅ Finished today's 30 clicks"
        )

        # wait for next day
        while True:

            if not SYDFLAG:
                await event.reply(f"Stopped")
                return

            now = datetime.now(IST)

            # next day after midnight resets loop
            if now.hour < 6:
                break

            await asyncio.sleep(60)




@mrsyd.on(
    events.NewMessage(
        from_users=ADMIN_ID,
        pattern=r"(?i)(24 process|sydflag false|start auto process)"
    )
)
async def auto_runner(event, syd=None):

    global SYDFLAG

    text = event.raw_text.strip()

    # =====================================================
    # START 24 PROCESS
    # =====================================================
    if text.lower() == "24 process":

        try:
            if SYDFLAG: return await event.reply("a process already running")
            SYDFLAG = True

            await event.reply(
                "🔍 Searching process message..."
            )

            # send /start
            await mrsyd.send_message(
                7996790736,
                "/start"
            )

            # wait 20 sec
            await asyncio.sleep(20)

            target_msg_id = None

            # check only last 4 messages
            messages = await mrsyd.get_messages(
                7996790736,
                limit=4
            )

            for m in messages:
             #   await event.reply(f"•{m.text}")
                if m.text and re.search(r'Получи\s+свою\s+личную\s+ссылку', m.text):
                    target_msg_id = m.id
                    break

            # not found
            if not target_msg_id:
                SYDFLAG = False
                return await event.reply(
                    "❌ Target process message not found in last 4 messages"
                )

            await event.reply(
                f"✅ Found target message: {target_msg_id}"
            )

            # start loop
            if syd:
                asyncio.create_task(click_loop(target_msg_id, event, syd))
            else:
                asyncio.create_task(click_loop(target_msg_id, event))
            return

        except Exception as e:
            SYDFLAG = False
            await event.reply(f"⚠️ Error: {e}")
            return

    # =====================================================
    # MANUAL START WITH ID
    # =====================================================
    elif text.startswith("24 process "):
        try:
            if SYDFLAG: return await event.reply("a process already running")
                
            msg_id = int(text.split()[2])
            SYDFLAG = True
            await event.reply(
                "🚀 Started clicking process"
            )
            asyncio.create_task(
                click_loop(msg_id, event)
            )
            return

        except Exception as e:
            await event.reply(f"⚠️ Error: {e}")
            return

    elif text.startswith("24 syd "):
        try:
            if SYDFLAG: return await event.reply("a process already running")
            SYDFLAG = True
            csyd = int(text.split()[2])

            await event.reply(
                "🔍 Searching process message..."
            )

            # send /start
            await mrsyd.send_message(
                7996790736,
                "/start"
            )

            # wait 20 sec
            await asyncio.sleep(20)

            target_msg_id = None

            # check only last 4 messages
            messages = await mrsyd.get_messages(
                7996790736,
                limit=4
            )

            for m in messages:
             #   await event.reply(f"•{m.text}")
                if m.text and re.search(r'Получи\s+свою\s+личную\s+ссылку', m.text):
                    target_msg_id = m.id
                    break

            # not found
            if not target_msg_id:
                SYDFLAG = False
                return await event.reply(
                    "❌ Target process message not found in last 4 messages"
                )

            await event.reply(
                f"✅ Found target message: {target_msg_id}"
            )

           
            asyncio.create_task(click_loop(target_msg_id, event, csyd))
            return

        except Exception as e:
            SYDFLAG = False
            await event.reply(f"⚠️ Error: {e}")
            return

    # =====================================================
    # STOP LOOP
    # =====================================================
    elif text.lower() == "sydflag false":

        SYDFLAG = False

        await event.reply(
            "🛑 SYDFLAG set to False. Stopping loop."
        )

        return


from telethon import events
from telethon.errors import (
    UserAlreadyParticipantError,
    InviteHashExpiredError,
    InviteHashInvalidError
)

from telethon.tl.functions.messages import (
    ImportChatInviteRequest
)

from telethon.tl.functions.channels import (
    JoinChannelRequest
)

FRUIT_EMOJIS = {
    "яблоко": "🍎",
    "клубника": "🍓",
    "банан": "🍌",
    "апельсин": "🍊",
    "лимон": "🍋",
    "арбуз": "🍉",
    "вишня": "🍒",
    "виноград": "🍇",
    "персик": "🍑",
    "груша": "🍐",
    "ананас": "🍍",
    "киви": "🥝",
    "манго": "🥭",
    "кокос": "🥥",
    "черника": "🫐",
}


@mrsyd.on(
    events.NewMessage(
        from_users=[7996790736],
        pattern=r"(?i)(🤖 ПРОВЕРКА НА|💫 Для продолжения фарма|✨ Новое задание)"
    )
)
async def solve_robot_check(event):
    message = event.message
    logging.info(message)

    try:

        await asyncio.sleep(6)

        if not message.text:
            return

        text = message.text.strip()

        # =========================================================
        # CASE 1 -> MATH CAPTCHA
        # =========================================================

        if text.startswith("🤖 ПРОВЕРКА НА") and "получить" in text:

            match = re.search(r'(\d+)\s*\+\s*(\d+)', text)

            if not match:
                return

            num1 = int(match.group(1))
            num2 = int(match.group(2))

            answer = str(num1 + num2)

            if not message.buttons:
                return

            for row in message.buttons:
                for btn in row:

                    if btn.text.strip() == answer:

                        await btn.click()

                        logging.info(
                            f"Clicked answer button: {answer}"
                        )

                        
                        return

        # =========================================================
        # CASE 2 -> FARM CONTINUE
        # =========================================================

        elif text and re.search(r'💫.*Для продолжения фарма|✨.*Новое задание!', text):
            if not message.buttons:
                return

            # =====================================================
            # OPEN ALL URL BUTTONS
            # =====================================================

            for row in message.buttons:
                for btn in row:

                    if getattr(btn, "url", None):

                        url = btn.url

                        logging.info(
                            f"Opening URL: {url}"
                        )

                        try:

                            clean_link = (
                                url.replace("https://", "")
                                .replace("http://", "")
                            )

                            # =====================================
                            # INVITE LINKS
                            # =====================================

                            if (
                                "t.me/+" in clean_link or
                                "telegram.me/+" in clean_link or
                                "joinchat/" in clean_link
                            ):

                                invite_hash = None

                                if "joinchat/" in clean_link:

                                    invite_hash = (
                                        clean_link.split(
                                            "joinchat/"
                                        )[1]
                                    )

                                elif "+" in clean_link:

                                    invite_hash = (
                                        clean_link.split("+")[1]
                                    )

                                try:

                                    await mrsyd(
                                        ImportChatInviteRequest(
                                            invite_hash
                                        )
                                    )

                                    logging.info(
                                        "Joined invite"
                                    )

                                except (
                                    UserAlreadyParticipantError
                                ):

                                    pass

                                except (
                                    InviteHashExpiredError,
                                    InviteHashInvalidError
                                ):

                                    logging.info(
                                        "Invalid invite"
                                    )

                            # =====================================
                            # NORMAL T.ME LINKS
                            # =====================================

                            elif "t.me/" in clean_link:

                                path = (
                                    clean_link.split(
                                        "t.me/"
                                    )[1]
                                )

                                path = path.strip("/")

                                # bot start
                                if "?start=" in path:

                                    bot_username = (
                                        path.split(
                                            "?start="
                                        )[0]
                                    )

                                    start_param = (
                                        path.split(
                                            "?start="
                                        )[1]
                                    )

                                    await mrsyd.send_message(
                                        bot_username,
                                        f"/start {start_param}"
                                    )

                                    logging.info(
                                        f"Started bot: "
                                        f"{bot_username}"
                                    )

                                # webapp
                                elif "/" in path:

                                    username = (
                                        path.split("/")[0]
                                    )

                                    try:

                                        await mrsyd.send_message(
                                            username,
                                            "/start"
                                        )

                                    except:
                                        pass

                                # normal username
                                else:

                                    username = path

                                    try:

                                        entity = (
                                            await mrsyd.get_entity(
                                                username
                                            )
                                        )

                                        if getattr(
                                            entity,
                                            "bot",
                                            False
                                        ):

                                            await mrsyd.send_message(
                                                username,
                                                "/start"
                                            )

                                        else:

                                            await mrsyd(
                                                JoinChannelRequest(
                                                    username
                                                )
                                            )

                                    except (
                                        UserAlreadyParticipantError
                                    ):

                                        pass

                                    except:
                                        pass

                            await asyncio.sleep(2)

                        except Exception as e:

                            logging.info(
                                f"URL open failed: {e}"
                            )

            # =====================================================
            # CLICK LAST CALLBACK BUTTON ONLY
            # =====================================================

            for row in message.buttons:

                for btn in row:
                    if not (
                        hasattr(btn, "data")
                        and btn.data
                    ):
                        continue

                    btn_text = (btn.text or "").strip()

                    # FIRST PRIORITY
                    if "Подтвердить подписку" in btn_text:

                        await btn.click()

                        logging.info(
                            "Pressed confirm subscription button"
                        )

                        await mrsyd.send_message(
                            ADMIN_ID,
                            f"✅ Pressed confirm button\n"
                            f"Button: {btn_text}"
                        )

                        

                    
                    elif "Я выполнил (а)" in btn_text:
                        await asyncio.sleep(30)
                        await btn.click()

                        logging.info(
                            "Pressed completed button"
                        )

                        await mrsyd.send_message(
                            ADMIN_ID,
                            f"✅ Pressed completed button\n"
                            f"Button: {btn_text}"
                        )
            return

        # =========================================================
        # CASE 3 -> ROBOT FRUIT CHECK
        # =========================================================

        elif text.startswith("🤖 ПРОВЕРКА НА РОБОТА"):

            fruit_match = re.search(
                r'«(.*?)»',
                text
            )

            if not fruit_match:
                return

            fruit_name = re.sub(r'[^а-яё]', '', fruit_match.group(1).lower())
            
            logging.info(f"#{fruit_name}")
            fruit_name = re.sub(r'[\u200b\u200c\u200d\ufeff\xa0]', '', fruit_name)
            logging.info(f"#{fruit_name}")
            fruit_emoji = FRUIT_EMOJIS.get(
                fruit_name
            )

            if not fruit_emoji:

                await mrsyd.send_message(
                    ADMIN_ID,
                    f"❌ Unknown fruit:\n"
                    f"{fruit_name}"
                )

                return

            if not message.buttons:
                return

            for row in message.buttons:
                for btn in row:

                    btn_text = btn.text.lower()

                    if (
                        fruit_emoji in btn.text or
                        fruit_name in btn_text
                    ):

                        await btn.click()

                        logging.info(
                            f"Clicked fruit: "
                            f"{fruit_name}"
                        )

                        await mrsyd.send_message(
                            ADMIN_ID,
                            f"✅ Clicked fruit button\n"
                            f"Fruit: {fruit_name} "
                            f"{fruit_emoji}"
                        )

                        return

            await mrsyd.send_message(
                ADMIN_ID,
                f"❌ Fruit button not found:\n"
                f"{fruit_name}"
            )

    except Exception as e:

        logging.info(
            f"solve_robot_check error: {e}"
        )

        await mrsyd.send_message(
            ADMIN_ID,
            f"⚠️ Robot check error:\n{e}"
        )
