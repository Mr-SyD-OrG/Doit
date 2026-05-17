import asyncio
import random
import logging


#logging.basicConfig(level=logging.INFO)

from playwright.async_api import async_playwright


playwright_instance = None
browser = None
context = None
page = None

TASK_COUNT = 0


# =========================================
# START BROWSER
# =========================================

async def start_browser():

    global playwright_instance
    global browser
    global context
    global page

    try:

        playwright_instance = await async_playwright().start()

        browser = await playwright_instance.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

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

    except Exception as e:

        logging.info(f"start_browser error: {e}")

        import traceback
        traceback.print_exc()


# =========================================
# REFRESH CONTEXT
# =========================================

async def refresh_context():

    global context
    global page
    global browser

    try:

        logging.info("Refreshing context")

        # close old page
        try:

            if page:
                await page.close()

        except:
            pass

        # close old context
        try:

            if context:
                await context.close()

        except:
            pass

        # create new context
        context_new = await browser.new_context(
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

        # IMPORTANT
        globals()["context"] = context_new

        # create new page
        page_new = await context_new.new_page()

        globals()["page"] = page_new

        logging.info("Context refreshed successfully")

    except Exception as e:

        logging.info(f"refresh_context error: {e}")

        import traceback
        traceback.print_exc()



async def open_real(url):

    global page
    global TASK_COUNT

    try:

        # ================================
        # SAFETY CHECKS
        # ================================

        if not url:

            logging.info("URL is None")

            return

        if page is None:

            logging.info("Page is None")

            return

        TASK_COUNT += 1

        logging.info(f"Opening: {url}")

        # random delay before open
        await asyncio.sleep(
            random.uniform(0.12, 0.78)
        )

        # open page
        await page.goto(
            url,
            wait_until="commit",
            timeout=3500
        )

        # reading time
        await asyncio.sleep(
            random.uniform(0.05, 0.2)
        )

        # ================================
        # RANDOM SCROLL
        # ================================

        try:

            # 70% chance to scroll
            if random.random() < 0.4:

                scroll_amount = random.randint(
                    200,
                    1200
                )

                await page.mouse.wheel(
                    0,
                    scroll_amount
                )

                logging.info(
                    f"Scrolled: {scroll_amount}px"
                )

                await asyncio.sleep(
                    random.uniform(0.001, 0.8)
                )

            else:

                logging.info(
                    "Skipped scrolling"
                )

        except Exception as e:

            logging.info(f"Scroll error: {e}")

        # ================================
        # RANDOM MOUSE MOVE
        # ================================

        try:

            # 60% chance
            if random.random() < 0.2:

                await page.mouse.move(
                    random.randint(100, 800),
                    random.randint(100, 600),
                    steps=random.randint(10, 30)
                )

                logging.info("Mouse moved")

        except Exception as e:

            logging.info(f"Mouse error: {e}")

        # ================================
        # OCCASIONAL LONG HUMAN PAUSE
        # ================================

        try:

            # every ~25 tasks sometimes pause
            if TASK_COUNT % 25 == 0:

                pause_time = random.uniform(
                    1,
                    4
                )

                logging.info(
                    f"Long pause: {pause_time}"
                )

                await asyncio.sleep(
                    pause_time
                )

        except:
            pass

        logging.info("Opened successfully")

        # ================================
        # REFRESH CONTEXT EVERY 50 TASKS
        # ================================

        if TASK_COUNT % 50 == 0:

            await refresh_context()

    except Exception as e:

        logging.info(f"open_real error: {e}")

        import traceback
        traceback.print_exc()
