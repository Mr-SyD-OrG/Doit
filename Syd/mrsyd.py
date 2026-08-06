from telethon import events
from telethon.errors import FloodWaitError
import asyncio
from bot import mrsyd
FORWARD_STOP = False
client = mrsyd

def parse_chat(value):
    value = value.strip()

    if value.startswith(("https://t.me/", "http://t.me/")):
        value = value.replace("https://t.me/", "").replace("http://t.me/", "")
        parts = value.strip("/").split("/")

        if len(parts) == 1:
            return parts[0], None

        if len(parts) == 2:
            return parts[0], int(parts[1])

        if parts[0] == "c" and len(parts) >= 3:
            return int("-100" + parts[1]), int(parts[2])

    if value.lstrip("-").isdigit():
        return int(value), None

    return value, None
    
async def ask_or_cancel(event, text):
    async with event.client.conversation(event.chat_id) as conv:
        await conv.send_message(text + "\n\n(Type `cancel` to abort)")
        reply = await conv.get_response()

    if reply.raw_text.strip().lower() == "cancel":
        raise RuntimeError("Cancelled by user.")

    return reply.raw_text.strip()


async def resolbve_chat(client, value, chat_id, label):
    while True:
        chat, detected = parse_chat(value)

        try:
            await client.get_messages(chat, ids=1)
            return chat, detected

        except Exception as e:
            value = await ask_or_cancel(
                type("obj", (), {
                    "client": client,
                    "chat_id": chat_id
                }),
                f"k I can't access that {label}.\n"
                "Send a message in that chat first (or ask an admin to), "
                "then send the chat ID/username/link again."
                f" ~ {e}"
            )


                       
            
            

@client.on(events.NewMessage(pattern=r"\.id$"))
async def get_chat_id(event):
    await event.reply(
        f"Chat ID: `{event.chat_id}`\n"
        f"Sender ID: `{event.sender_id}`",
        parse_mode="md"
    )
            
async def resolve_chat(client, value, chat_id, label):
    while True:
        chat, detected = parse_chat(value)

        await client.send_message(
            1733124290,
            f"Parsed:\n{chat!r}\nType: {type(chat).__name__}"
        )
        try:
            msg = await client.get_messages(chat, ids=1)

            await client.send_message(
                1733124290,
                f"Success!\nMessage: {msg}"
            )

            return chat, detected

        except Exception as e:
            await client.send_message(
                1733124290,
                f"Exception:\n"
                f"{type(e).__name__}\n\n"
                f"{repr(e)}"
            )

            try:
                if isinstance(chat, int) and str(chat).startswith("-100"):
                    target = int(str(chat)[4:])

                    async for dialog in client.iter_dialogs():
                        if dialog.id == target:
                            await client.send_message(
                                1733124290,
                                f"Found in dialogs:\n"
                                f"{dialog.name}\n"
                                f"{dialog.id}"
                            )
                            return dialog.entity, detected

                    await client.send_message(
                        1733124290,
                        f"Not found in dialogs.\nLooking for: {target}"
                    )

            except Exception as e2:
                await client.send_message(
                    1733124290,
                    f"Dialog Exception:\n"
                    f"{type(e2).__name__}\n\n"
                    f"{repr(e2)}"
                )

            value = await ask_or_cancel(
                type(
                    "obj",
                    (),
                    {
                        "client": client,
                        "chat_id": chat_id,
                    },
                ),
                f"🌱 I can't access that {label}.\n"
                "Send the chat ID/username/link again."
            )



@client.on(events.NewMessage(pattern=r"\.stop$"))
async def stop_forward(event):
    global FORWARD_STOP
    FORWARD_STOP = True
    await event.reply("🛑 Stop request received.")


@mrsyd.on(events.NewMessage(pattern=r"\.forward$"))
async def forward_messages(event):
    global FORWARD_STOP
    FORWARD_STOP = False

    client = event.client

    try:
        from_input = await ask_or_cancel(event, "📥 Send FROM chat/link")
        from_chat, detected_end = await resolve_chat(
            client,
            from_input,
            event.chat_id,
            "FROM chat"
        )

        to_input = await ask_or_cancel(event, "📤 Send TO chat/link")
        to_chat, _ = await resolve_chat(
            client,
            to_input,
            event.chat_id,
            "TO chat"
        )

        start_id = int(await ask_or_cancel(event, "🔢 Send Start Message ID"))

        if detected_end is not None:
            ans = (await ask_or_cancel(
                event,
                f"📌 Detected End Message ID: {detected_end}\nUse it? (yes/no)"
            )).lower()

            if ans in ("yes", "y"):
                end_id = detected_end
            else:
                end_id = int(await ask_or_cancel(event, "🔢 Send End Message ID"))
        else:
            end_id = int(await ask_or_cancel(event, "🔢 Send End Message ID"))

        pause = max(
            1.0,
            float(await ask_or_cancel(event, "⏱ Pause between messages"))
        )

        total = end_id - start_id + 1
        sent = 0
        last_id = start_id - 1

        progress = await event.reply(
            f"🚀 Started\n\n"
            f"From: {from_chat}\n"
            f"To: {to_chat}\n"
            f"Start ID: {start_id}\n"
            f"Skipped: 0\n"
            f"Forwarded: 0\n"
            f"Left: {total}\n"
            f"Total: {total}\n"
            f"Last Original ID: {last_id}"
        )

        for msg_id in range(start_id, end_id + 1):

            if FORWARD_STOP:
                await progress.edit(
                    f"🛑 Stopped\n\n"
                    f"Skipped: {max(0,last_id-start_id+1-sent)}\n"
                    f"Forwarded: {sent}\n"
                    f"Left: {max(0,total-sent)}\n"
                    f"Total: {total}\n"
                    f"Last Original ID: {last_id}"
                )
                return

            try:
                msg = await client.get_messages(from_chat, ids=msg_id)

                if not msg:
                    continue

                while True:
                    try:
                        await mrsyd.forward_messages(
                            to_chat,
                            msg,
                            from_chat,
                            drop_author=True
                        )
                        sent += 1
                        last_id = msg_id
                        break

                    except FloodWaitError as e:
                        await asyncio.sleep(e.seconds)

                    except Exception as ex:
                        print(ex)
                        break

                if sent % 100 == 0 or msg_id == end_id:
                    try:
                        await progress.edit(
                            f"🚀 Forwarding...\n\n"
                            f"Skipped: {max(0,last_id-start_id+1-sent)}\n"
                            f"Forwarded: {sent}\n"
                            f"Left: {max(0,total-sent)}\n"
                            f"Total: {total}\n"
                            f"Last Original ID: {last_id}\n"
                            f"~ .stop to end"
                        )
                    except Exception:
                        pass

                await asyncio.sleep(pause)

            except Exception as ex:
                print(ex)

        await progress.edit(
            f"✅ Completed\n\n"
            f"Skipped: {max(0,last_id-start_id+1-sent)}\n"
            f"Forwarded: {sent}\n"
            f"Left: {max(0,total-sent)}\n"
            f"Total: {total}\n"
            f"Last Original ID: {last_id}"
        )

    except Exception as e:
        await event.reply(f"❌ {e}")

