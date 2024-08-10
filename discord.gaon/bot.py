import aiohttp
from .client import DiscordClient

class Bot(DiscordClient):
    def __init__(self, token, prefix="!"):
        super().__init__(token)
        self.prefix = prefix
        self.commands = {}

    def command(self, name):
        def wrapper(func):
            self.commands[self.prefix + name] = func
            return func
        return wrapper

    async def on_message(self, message):
        content = message['content']
        if content.startswith(self.prefix):
            command_name = content.split(" ")[0]
            if command_name in self.commands:
                await self.commands[command_name](self, message)

    async def send_message(self, channel_id, content):
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "content": content
        }
        async with aiohttp.ClientSession() as session:
            await session.post(url, headers=headers, json=data)
