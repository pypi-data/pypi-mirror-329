import logging
import httpx
import aiohttp
import asyncio
from .methods import *

log = logging.getLogger(__name__)

class Client(Methods):
  def __init__(self, name: str, bot_token: str):
    self.name = name
    self.bot_token = bot_token
    self.connected = False
    self.me = None
    self.on_listeners = []
    self.offset = 0
    self.polling = False

  async def start(self):
    url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
    async with httpx.AsyncClient() as client:
      r = (await client.get(url)).json()
      if r.get("ok"):
        self.connected = True
        self.me = r["result"]
        log.info(f"Client connected as {self.me['first_name']} (@{self.me['username']})")
        return r
      raise ValueError("Failed to connect with your bot token. Please make sure your bot token is correct.")

  async def start_polling(self):
    if not self.connected:
      raise ConnectionError("Client is not connected. Please connect the client and start polling.")
    elif self.polling: raise "Polling already started, why you trying again and again? didn't you receive any updates?"
    self.polling = True
    log.info("Nexgram polling started!")
    while self.polling:
      try:
        async with aiohttp.ClientSession() as session:
          params = {"offset": self.offset, "timeout": 30}
          async with session.get(f"https://api.telegram.org/bot{self.bot_token}/getUpdates", params=params) as response:
            updates = await response.json()
            if "result" in updates:
              for update in updates["result"]:
                self.offset = update["update_id"] + 1
                asyncio.create_task(self.dispatch_update(update))
      except Exception as e:
        log.error(f"Error in start_polling: {e}")
      await asyncio.sleep(1)

  async def dispatch_update(self, update):
    for x in self.on_listeners:
      asyncio.create_task(x(update))

  def on(self, func):
    self.on_listeners.append(func)
  async def stop(self):
    self.polling = False
    self.connected = False
    log.info("Client stopped.")