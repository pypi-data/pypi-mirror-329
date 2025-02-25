import logging
import struct
import time
import os
import hashlib
import asyncio
from .connection import Connection

log = logging.getLogger(__name__)

class Client:
  def __init__(
    self,
    name: str,
    api_id: int,
    api_hash: str,
    bot_token: str = None,
    session_string: str = None      
  ):
    self.name = name
    self.api_id = api_id
    self.api_hash = api_hash
    self.bot_token = bot_token
    self.session_string = session_string
    self.auth_key = None
    self.socket = Connection("91.108.56.165", 443)

  async def connect(self):
    await self.socket.connect()

  async def req_pq(self):
    random_bytes = os.urandom(16)
    message_id = int(time.time() * (2**32))
    payload = struct.pack("<Q", message_id) + random_bytes

    await self.socket.send(payload)
    response = await self.socket.receive()
    return response