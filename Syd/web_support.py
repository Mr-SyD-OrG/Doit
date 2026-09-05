

import os,secrets
from aiohttp import web
routes=web.RouteTableDef()
ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD','CHANGE_ME')
connection_code=os.environ.get('CONNECTION_CODE','482731')
website_url=os.environ.get('WEBSITE_URL','https://doit-u30d.onrender.com')
sessions={};admin_tokens=set()
def valid(c): return bool(c) and secrets.compare_digest(str(c),str(connection_code))
def sess(c): return sessions.setdefault(c,{'phone':{'messages':[]},'tv':{'messages':[]},'history':[]})
def admin_ok(r):
 a=r.headers.get('Authorization','');return a.startswith('Bearer ') and a[7:] in admin_tokens
@routes.get('/',allow_head=True)
async def root(r): return web.json_response({'name':'SyDnSnH Relay','status':'online','website_url':website_url})
@routes.get('/stream')
async def stream(r): raise web.HTTPFound(website_url)
@routes.get('/api/history')
async def history(r): return web.json_response({'history':sess(connection_code)['history'][-500:]})
@routes.post('/api/send')
async def send(r):
 try:b=await r.json()
 except: b={}
 role=str(b.get('role',''));code=str(b.get('code',''));text=str(b.get('text',''))[:10000]
 kind='link' if ('http://' in text or 'https://' in text) else 'text'
 if role not in ('phone','tv') or not valid(code) or not text:return web.json_response({'ok':False},status=400)
 s=sess(code);item={'id':secrets.token_urlsafe(10),'sender':role,'kind':kind,'text':text};other='tv' if role=='phone' else 'phone';s[other]['messages'].append(item);s['history'].append(item);s[other]['messages']=s[other]['messages'][-100:];s['history']=s['history'][-500:];return web.json_response({'ok':True,'id':item['id']})
@routes.post('/api/delete')
async def delete(r):
 try:b=await r.json()
 except:b={}
 role=str(b.get('role',''));code=str(b.get('code',''));mid=str(b.get('id',''))
 if role!='phone' or not valid(code) or not mid:return web.json_response({'ok':False},status=403)
 s=sess(code);s['history']=[x for x in s['history'] if str(x.get('id'))!=mid]
 for peer in ('phone','tv'):s[peer]['messages']=[x for x in s[peer]['messages'] if str(x.get('id'))!=mid]
 return web.json_response({'ok':True})
@routes.get('/api/poll')
async def poll(r):
 role=r.query.get('role','');code=r.query.get('code','')
 if role not in ('phone','tv') or not valid(code):return web.json_response({'error':'Invalid code'},status=401)
 s=sess(code);msgs=s[role]['messages'];s[role]['messages']=[];return web.json_response({'messages':msgs,'history':s['history'][-500:]})
@routes.post('/api/admin/login')
async def login(r):
 try:b=await r.json()
 except:b={}
 if secrets.compare_digest(str(b.get('password','')),ADMIN_PASSWORD):
  t=secrets.token_urlsafe(32);admin_tokens.add(t);return web.json_response({'ok':True,'token':t})
 return web.json_response({'ok':False},status=401)
@routes.get('/api/admin/settings')
async def aset(r):
 if not admin_ok(r):return web.json_response({'error':'Unauthorized'},status=401)
 return web.json_response({'website_url':website_url,'connection_code':connection_code})
@routes.post('/api/admin/settings')
async def save_settings(r):
 global website_url,connection_code
 if not admin_ok(r):return web.json_response({'error':'Unauthorized'},status=401)
 try:b=await r.json()
 except:b={}
 if str(b.get('website_url','')).strip():website_url=str(b['website_url']).strip()[:2000]
 if 'connection_code' in b:
  v=str(b.get('connection_code','')).strip()
  if not v or len(v)>64:return web.json_response({'error':'Invalid code'},status=400)
  connection_code=v
 return web.json_response({'ok':True,'website_url':website_url,'connection_code':connection_code})

async def web_server():
 web_app = web.Application(client_max_size=30000000)
 web_app.add_routes(routes)
 return web_app
