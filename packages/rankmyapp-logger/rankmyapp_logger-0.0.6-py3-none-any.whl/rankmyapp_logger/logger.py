from contracts.transport import LogContract, Transport
from contracts.message import Message
from typing import List

class Logger(LogContract[Message]):
  def __init__(self, name: str, transports: List[Transport] = []):
    self.name = name
    self._transports = transports

  def _log(self, message: Message):
    for transport in self._transports:
      transport.set_context(dict(name=self.name))

      log_type = message.level
      default_log_fn = lambda message: print(f"Method '{log_type}' not allowed {message.to_dict()}")

      log_fn = getattr(transport, log_type, default_log_fn)

      if callable(log_fn):
        log_fn(message)

  def info(self, message: Message):
    message.level = "info";
    self._log(message)

  def error(self, message: Message):
    message.level = "error";
    self._log(message)
  
  def warn(self, message: Message):
    message.level = "warn";
    self._log(message)

  def debug(self, message: Message):
    message.level = "debug";
    self._log(message)