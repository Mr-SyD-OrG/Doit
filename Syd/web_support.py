

import os, secrets, asyncio
from aiohttp import web

routes = web.RouteTableDef()
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "CHANGE_ME")
connection_code = os.environ.get("CONNECTION_CODE", "482731")
website_url = os.environ.get("WEBSITE_URL", "https://doit-u30d.onrender.com")

.
sessions = {}
admin_tokens = set()

def valid_code(c): return bool(c) and secrets.compare_digest(c, connection_code)
def sess(code):
    return sessions.setdefault(code, {"phone":{"messages":[]}, "tv":{"messages":[]}, "history":[]})

@routes.get("/", allow_head=True)
async def root(request):
    return web.json_response({"name":"SyDnSnH Relay","status":"online","website_url":website_url})

@routes.get("/stream")
async def stream(request):
    raise web.HTTPFound(website_url)

@routes.get("/admin")
async def admin(request):
    return web.FileResponse("static/admin.html")

@routes.get("/connection")
async def connection(request):
    return web.FileResponse("static/connection.html")

@routes.post("/api/admin/login")
async def admin_login(request):
    try: body=await request.json()
    except Exception: body={}
    if secrets.compare_digest(str(body.get("password","")), ADMIN_PASSWORD):
        token=secrets.token_urlsafe(32); admin_tokens.add(token)
        return web.json_response({"ok":True,"token":token})
    return web.json_response({"ok":False,"error":"Invalid password"},status=401)

def admin_ok(request):
    return request.headers.get("Authorization","").startswith("Bearer ") and request.headers["Authorization"][7:] in admin_tokens

@routes.get("/api/admin/settings")
async def get_settings(request):
    if not admin_ok(request): return web.json_response({"error":"Unauthorized"},status=401)
    return web.json_response({"website_url":website_url,"connection_code":connection_code})

@routes.post("/api/admin/settings")
async def set_settings(request):
    global website_url, connection_code
    if not admin_ok(request): return web.json_response({"error":"Unauthorized"},status=401)
    try: body=await request.json()
    except Exception: body={}
    if "website_url" in body: website_url=str(body["website_url"])[:2000]
    if "connection_code" in body:
        c=str(body["connection_code"]).strip()
        if not c or len(c)>64: return web.json_response({"error":"Invalid connection code"},status=400)
        connection_code=c
    return web.json_response({"ok":True,"website_url":website_url,"connection_code":connection_code})

@routes.post("/api/send")
async def send(request):
    try: body=await request.json()
    except Exception: body={}
    role=str(body.get("role","")); code=str(body.get("code","")); text=str(body.get("text",""))[:10000]
    if role not in ("phone","tv") or not valid_code(code) or not text:
        return web.json_response({"ok":False,"error":"Invalid request"},status=400)
    other="tv" if role=="phone" else "phone"
    s=sess(code)
    item={"id":secrets.token_urlsafe(8),"sender":role,"kind":"link" if str(body.get("kind"))=="link" else "text","text":text}
    s[other]["messages"].append(item)
    s["history"].append(item)
    s["history"]=s["history"][-200:]
    s[other]["messages"]=s[other]["messages"][-100:]
    return web.json_response({"ok":True})

@routes.get("/api/poll")
async def poll(request):
    role=request.query.get("role",""); code=request.query.get("code","")
    if role not in ("phone","tv") or not valid_code(code):
        return web.json_response({"error":"Invalid code"},status=401)
    s=sess(code)
    msgs=s[role]["messages"]
    s[role]["messages"]=[]
    return web.json_response({"messages":msgs,"history":s["history"]})

@routes.get("/api/history")
async def history(request):
    code=request.query.get("code","")
    if not valid_code(code): return web.json_response({"error":"Invalid code"},status=401)
    return web.json_response({"history":sess(code)["history"]})



async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
