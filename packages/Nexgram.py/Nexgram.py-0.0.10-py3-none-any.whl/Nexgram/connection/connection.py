import asyncio
import struct
import time
import hashlib
from Crypto.Cipher import AES

class Connection:
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.reader = None
    self.writer = None
  async def connect(self):
    self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
  async def send(self, data):
    if self.writer is None:
      raise ConnectionError("Socket is not connected.")
    self.writer.write(data)
    await self.writer.drain()
  async def receive(self, length=1024):
    if self.reader is None:
      raise ConnectionError("Socket is not connected.")
    return await self.reader.read(length)
  async def close(self):
    if self.writer:
      self.writer.close()
    await self.writer.wait_closed()