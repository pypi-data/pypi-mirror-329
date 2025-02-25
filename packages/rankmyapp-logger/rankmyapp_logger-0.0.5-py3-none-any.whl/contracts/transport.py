from abc import ABC, abstractmethod
from contracts.message import Message
from typing import TypeVar, Generic

T = TypeVar('T', bound=Message)

class LogContract(ABC, Generic[T]):
  @abstractmethod
  def info(self, message: T):
    pass

  @abstractmethod
  def error(self, message: T):
    pass
  
  @abstractmethod
  def warn(self, message: T):
    pass

  @abstractmethod
  def debug(self, message: T):
    pass

class Transport(LogContract[T]):
  def __init__(self):
    self._context = dict()

  def set_context(self, data = dict()):
    if isinstance(data, dict):
      self._context = data
    

  @abstractmethod
  def log(self, message: T):
    ...