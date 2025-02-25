import logging
import httpx
from .Methods import *

log = logging.getLogger(__name__)

class Client(Methods):
  def __init__(self, name: str, bot_token: str):
    self.name = name
    self.bot_token = bot_token
    self.connected = False
    self.me = None

  async def start(self):
    url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
    async with httpx.AsyncClient() as client:
      r = (await client.get(url)).json()
      if r.get("ok"):
        self.connected = True
        self.me = r["result"]
        log.info(f"Client connected as {self.me['first_name']} (@{self.me['username']})")
      return r