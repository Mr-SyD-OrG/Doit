

import os, secrets
from aiohttp import web

routes = web.RouteTableDef()

# REQUIRED on Render:
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "CHANGE_ME")
connection_code = os.environ.get("CONNECTION_CODE", "482731")
website_url = os.environ.get("WEBSITE_URL", "https://doit-u30d.onrender.com")

# In-memory relay. It does not proxy video. Messages are short-lived and
# survive only while the Render instance is running.
sessions = {}
admin_tokens = set()

def valid_code(code):
    return bool(code) and secrets.compare_digest(str(code), str(connection_code))

def session_for(code):
    return sessions.setdefault(code, {
        "phone": {"messages": []},
        "tv": {"messages": []},
        "history": []
    })

def admin_ok(request):
    value = request.headers.get("Authorization", "")
    return value.startswith("Bearer ") and value[7:] in admin_tokens

@routes.get("/", allow_head=True)
async def root(request):
    return web.json_response({
        "name": "SyDnSnH Relay",
        "status": "online",
        "website_url": website_url
    })

@routes.get("/stream")
async def stream(request):
    raise web.HTTPFound(website_url)

@routes.post("/api/admin/login")
async def admin_login(request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    password = str(body.get("password", ""))
    if secrets.compare_digest(password, ADMIN_PASSWORD):
        token = secrets.token_urlsafe(32)
        admin_tokens.add(token)
        return web.json_response({"ok": True, "token": token})
    return web.json_response({"ok": False, "error": "Invalid password"}, status=401)

@routes.get("/api/admin/settings")
async def admin_get_settings(request):
    if not admin_ok(request):
        return web.json_response({"error": "Unauthorized"}, status=401)
    return web.json_response({
        "website_url": website_url,
        "connection_code": connection_code
    })

@routes.post("/api/admin/settings")
async def admin_set_settings(request):
    global website_url, connection_code
    if not admin_ok(request):
        return web.json_response({"error": "Unauthorized"}, status=401)
    try:
        body = await request.json()
    except Exception:
        body = {}

    if "website_url" in body:
        value = str(body.get("website_url", "")).strip()
        if value:
            website_url = value[:2000]

    if "connection_code" in body:
        value = str(body.get("connection_code", "")).strip()
        if not value or len(value) > 64:
            return web.json_response({"error": "Invalid connection code"}, status=400)
        connection_code = value

    return web.json_response({
        "ok": True,
        "website_url": website_url,
        "connection_code": connection_code
    })

@routes.post("/api/send")
async def send(request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    role = str(body.get("role", ""))
    code = str(body.get("code", ""))
    text = str(body.get("text", ""))[:10000]
    kind = "link" if str(body.get("kind", "")) == "link" else "text"

    if role not in ("phone", "tv") or not valid_code(code) or not text:
        return web.json_response({"ok": False, "error": "Invalid request"}, status=400)

    other = "tv" if role == "phone" else "phone"
    session = session_for(code)
    item = {
        "id": secrets.token_urlsafe(8),
        "sender": role,
        "kind": kind,
        "text": text
    }
    session[other]["messages"].append(item)
    session["history"].append(item)
    session[other]["messages"] = session[other]["messages"][-100:]
    session["history"] = session["history"][-200:]
    return web.json_response({"ok": True})

@routes.get("/api/poll")
async def poll(request):
    role = request.query.get("role", "")
    code = request.query.get("code", "")
    if role not in ("phone", "tv") or not valid_code(code):
        return web.json_response({"error": "Invalid code"}, status=401)
    session = session_for(code)
    messages = session[role]["messages"]
    session[role]["messages"] = []
    return web.json_response({"messages": messages, "history": session["history"]})

@routes.get("/api/history")
async def history(request):
    code = request.query.get("code", "")
    if not valid_code(code):
        return web.json_response({"error": "Invalid code"}, status=401)
    return web.json_response({"history": session_for(code)["history"]})


async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
