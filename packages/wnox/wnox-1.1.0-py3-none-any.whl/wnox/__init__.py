#%%
import asyncio
import nest_asyncio
import logging
from slixmpp import ClientXMPP 
import ssl
import json
from bson import ObjectId 
import requests as r

import random
import string
from dotenv import load_dotenv
import os
from pymongo import MongoClient

import zlib
import base64

def deflate_to_base64(input_string):
    """
    Compress (deflate) a string and return it as a Base64-encoded string.
    
    :param input_string: The string to compress.
    :return: The Base64-encoded compressed string.
    """
    try:
        # Step 1: Convert the input string to bytes
        input_data = input_string.encode('utf-8')

        # Step 2: Compress the data using zlib
        compressed_data = zlib.compress(input_data)

        # Step 3: Encode the compressed data as a Base64 string
        base64_string = base64.b64encode(compressed_data).decode('utf-8')

        return base64_string
    except Exception as e:
        print(f'Failed to deflate data: {e}')
        raise

def inflate_from_base64(base64_string):
    """
    Inflate (decompress) a Base64-encoded string using zlib.
    
    :param base64_string: The Base64-encoded compressed string.
    :return: The decompressed string.
    """
    try:
        # Step 1: Decode the Base64 string into bytes
        compressed_data = base64.b64decode(base64_string)

        # Step 2: Decompress the data using zlib
        decompressed_data = zlib.decompress(compressed_data)

        # Step 3: Convert the decompressed bytes to a string
        return decompressed_data.decode('utf-8')
    except Exception as e:
        print(f'Failed to inflate data: {e}')
        raise


nest_asyncio.apply()
eventdatax = {}
eventsx = {}
# logging.basicConfig(level=logging.DEBUG)

def serial_generator(length: int) -> str:
    chars = string.digits + string.ascii_uppercase + string.ascii_lowercase
    random_string = ''.join(random.choice(chars) for _ in range(length))
    return random_string

class EventEmitter:
    def __init__(self):
        self._events = {}

    def on(self, event_name, callback):
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    async def emit(self, event_name, *args, **kwargs):
        if event_name in self._events:
            # Collect the results of all event handlers
            results = []
            for callback in self._events[event_name]:
                result = callback(*args, **kwargs)
                if asyncio.iscoroutinefunction(callback):  # If callback is async
                    results.append(await result)
                else:  # If callback is sync
                    results.append(result)
            return results[0]

class WSX(ClientXMPP, EventEmitter):
    connected = False
    def __init__(self, jid, password, app:str, uid:str, resource:str):
    
        if "-" in app:
            raise "app should not contain dash '-'"
        if "-" in resource:
            raise "resource should not contain dash '-'"
        
        ClientXMPP.__init__(self, jid, password)
        EventEmitter.__init__(self)
        self.app = app
        self.uid = uid
        self._resource = resource
        self.password = password
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("failed_auth", self.on_failed_auth)
        self.add_event_handler("disconnected", self.on_disconnect)
        self.add_event_handler("message", self.on_message) 

    async def start(self, event):
        """Handle session start."""
        
        self.send_presence(ptype="presence")
        await self.get_roster()
        await self.emit("__connect",{})
        self.connected = True
        

    def on_failed_auth(self, event):
        """Handle authentication failure."""

    async def on_disconnect(self, event):
        """Handle disconnection and attempt reconnection."""
        await self.emit("__disconnect",{})
        self.connected = False
        asyncio.create_task(self.reconnect())

    async def reconnect(self):
        await asyncio.sleep(5) 
        self.connect(address=("direct.qepal.com", 5222), disable_starttls=False, force_starttls=True)
        self.process(forever=False)

    async def on_message(self, stanza):
        """Handle incoming messages."""
        if stanza.tag == "{jabber:client}message":
            body = str(stanza['body'])
            try:
                body = inflate_from_base64(body)
            except:
                pass
            from_jid = str(stanza['from'])
            itsme = from_jid and f"{self.boundjid.bare.split('@')[0]}-{self.boundjid.bare.split('@')[1]}" in from_jid
            itsbro = not itsme and f"{self.boundjid.bare.split('@')[0]}-" in from_jid
            
            if "conference.qepal.com" in from_jid:
                itsme = f"{self.app}-{self.uid}-{self._resource}" in from_jid
                itsbro = not itsme and f"{self.app}-{self.uid}-" in from_jid
                
            delayed = "urn:xmpp:delay" in str(stanza)

            if body and not delayed:
               
                    
                if body.startswith("{"):
                    try:
                        json_data = json.loads(body)
                        if "__connect" in json_data:
                            return
                        if "__disconnect" in  json_data:
                            return
                        if "__message" in  json_data:
                            return
                        
                        if "api" in json_data:
                            user_uid = from_jid.split('@')[0]
                            data = {key: val for key, val in json_data.items() if key != "api"}
                            data = {key: val for key, val in data.items() if key != "mid"}
                            data["from"] = from_jid
                            data["app"] = None
                           
                            if len(user_uid) == 24 and ObjectId.is_valid(user_uid):
                                data["uid"] = user_uid
                                data["app"] = None
                                data["resource"] = None
                                if "@qepal.com/" in  from_jid:
                                    data["resource"] = from_jid.split("@qepal.com/")[1]
                                
                            elif "conference.qepal.com" in from_jid:
                                pass
                            elif "-" in user_uid:
                                app = user_uid.split('-')[0]
                                user_uid = user_uid.split('-')[1]
                                data["app"] = app
                                data["uid"] = user_uid
                                data["resource"] = from_jid.split('@qepal.com/')[1]
                                
                            result = await self.emit(json_data["api"], data)
                            if result == None:
                                result = {}    
                            self.send_message(
                                    mto=from_jid,
                                    mbody= deflate_to_base64(json.dumps({**result, "mid": json_data.get("mid")}))
                                )
                                
                        else:
                            if "mid" in json_data:
                                data = {key: val for key, val in json_data.items() if key != "mid"}
                                eventdatax[json_data.get("mid")] = data
                                if json_data.get("mid") in eventsx:
                                    eventsx.get(json_data.get("mid")).set()
                            else:
                               
                                data["channel"] = None
                                if "@conference.qepal.com" in from_jid:
                                    s = from_jid.split("@conference.qepal.com/")
                                    data = {"from": from_jid, "body": body, "itsme": itsme, "itsbro": itsbro}
                                    data["channel"] = s[0]
                                    data["uid"] = None
                                    data["resource"] = None
                                    data["app"] = None
                                    ss = s[1].split("-")
                                    if len(ss) == 2 and len(ss[0]) == 24 and ObjectId.is_valid(ss[0]):
                                        data["uid"] = ss[0]
                                        data["resource"] = ss[1]
                                    elif len(ss) == 3 and len(ss[1]) == 24 and ObjectId.is_valid(ss[1]):
                                        data["uid"] = ss[1]
                                        data["app"] = ss[0]
                                        data["resource"] = ss[2]
                                await self.emit("__message", data)
                   
                    except json.JSONDecodeError:
                        pass
                else:
                    data = {"from": from_jid, "body": body, "itsme": itsme, "itsbro": itsbro}
                    data["channel"] = None
                    data["uid"] = None
                    data["resource"] = None
                    data["app"] = None
                    if "@qepal.com" in from_jid:
                        ss = from_jid.split("@qepal.com/")
                        if len(ss) == 2 and len(ss[0]) == 24 and ObjectId.is_valid(ss[0]):
                            data["uid"] = ss[0]
                            data["resource"] = ss[1]
                        elif "-" in ss[0]:
                            sss = ss[0].split("-")
                            data["app"] = sss[0]
                            data["uid"] = sss[1]
                            data["resource"] = ss[1]
                    elif "@conference.qepal.com" in from_jid:
                        ss = from_jid.split("@conference.qepal.com/")
                        data["channel"] = ss[0]
                        if "-" in ss[1]:
                            sss = ss[1].split("-")
                            if len(sss) == 2:
                                data["uid"] = sss[0]
                                data["resource"] = sss[1]
                            elif len(sss) == 3 and len(sss[1]) == 24 and ObjectId.is_valid(sss[1]):
                                data["app"] = sss[0]
                                data["uid"] = sss[1]
                                data["resource"] = sss[2]
                    await self.emit("__message",data)
                                


class App:
    
    udb = None
    def __init__(self, *, app:str, resource:str, securekey:str, image:str, public:bool=False):
        
        load_dotenv(".env.local")
        mongourl = os.getenv("UMONGOURL")
        mongo_db = os.getenv("UMONGODB_DB")

        if mongourl:
            try:
                client = MongoClient(mongourl)
                client.server_info()
                self.udb = client[mongo_db]
                print("✅ mongo udb connected.")
            except:
                print("❌ mongo udb not connected.")
        else:
            print("❌ no .env.local correct file")
                
            
        self.app = app
        self.channels = set()
        self.resource = resource
        self.securekey = securekey
        self.image = image
        self.public = public
        
        _json = r.post("https://qepal.com/api/bridge/worker/init", json={
            "app":app, "resource":resource, "securekey":securekey, "image":image, "public":public}).json()
        
        self.uid = _json["uid"]
        self.myjid = self.app + "-" + str(self.uid) + "@qepal.com/" + self.resource
        self.password = _json["password"]
        self.xmpp = WSX(self.myjid, self.password, self.app, self.uid, self.resource)

    def on(self, api:str, cb:callable):
        self.xmpp.on(api, cb)
    
    def sendtojid(self, jid:str, body:str):
        self.xmpp.send_message(mto=jid, mbody=deflate_to_base64(body))
        
    def connected(self):
        return self.xmpp.connected
        
    async def api(self, app:str, cmd:str, body:dict, jid:str = None, prioritize_public:bool = False):
        if jid == None:
            res:dict = r.post("https://qepal.com/api/bridge/worker/findfreeresource", json={ "app":app, "securekey": self.securekey }).json()
            jids = list(res.get("jids",[]))
            if len(jids) > 0:
                if prioritize_public:
                    jid = jids[-1]
                else:
                    jid = jids[0]
        if jid == None:
            return { "error": "no worker found" }
    
        mid = serial_generator(10)
        msg = {"mid":mid, "api":cmd, **body }  
        eventsx[mid] = asyncio.Event()
        self.sendtojid(jid, json.dumps(msg))
        await eventsx[mid].wait()
        data = eventdatax.get(mid)
        return data
        
        
            
    def subscribe(self, channelname:str):
        self.xmpp.send_presence(pto=channelname+ "@conference.qepal.com/"+ self.app + "-" + self.uid + "-" + self.resource , ptype="presence")
        self.xmpp.get_roster()
        self.channels.add(channelname)
        
    def unsubscribe(self, channelname:str):
        self.xmpp.send_presence(pto=channelname+ "@conference.qepal.com" , ptype="unavailable")
        self.xmpp.get_roster()
        self.channels.remove(channelname)
        
    def sendtochannel(self, channelname:str, body:str):
        if channelname not in self.channels:
            self.subscribe(channelname)
        self.xmpp.send_message(mto=f"{channelname}@conference.qepal.com", mbody=deflate_to_base64(body), mtype='groupchat')
        
    async def loop(self):

        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False 
        ssl_ctx.verify_mode = ssl.CERT_NONE  
        self.xmpp.ssl_context = ssl_ctx
    
        self.xmpp.connect(address=("direct.qepal.com", 5222), disable_starttls=False, force_starttls=True)
        self.xmpp.process(forever=True)



