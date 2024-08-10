import asyncio
import websockets # type: ignore
import json

class DiscordClient:
    def __init__(self, token):
        self.token = token
        self.gateway_url = "wss://gateway.discord.gg/?v=10&encoding=json"
        self.heartbeat_interval = None
        self.session = None

    async def connect(self):
        self.session = await websockets.connect(self.gateway_url)
        await self.identify()
        await self.listen()

    async def identify(self):
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": 513,
                "properties": {
                    "$os": "windows",
                    "$browser": "discord.gaon",
                    "$device": "discord.gaon"
                }
            }
        }
        await self.session.send(json.dumps(payload))

    async def heartbeat(self):
        while True:
            await asyncio.sleep(self.heartbeat_interval / 1000)
            heartbeat_payload = {"op": 1, "d": None}
            await self.session.send(json.dumps(heartbeat_payload))

    async def listen(self):
        async for message in self.session:
            data = json.loads(message)
            if data["op"] == 10:
                self.heartbeat_interval = data["d"]["heartbeat_interval"]
                asyncio.create_task(self.heartbeat())
            elif data["op"] == 0:
                event_type = data["t"]
                if event_type == "MESSAGE_CREATE":
                    await self.on_message(data["d"])

    async def on_message(self, message):
        pass

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect())
