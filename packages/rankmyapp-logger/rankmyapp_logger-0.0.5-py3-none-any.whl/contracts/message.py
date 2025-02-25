import os

from .enums import LogAuditKindEnum, LogLevelEnum, LogProtocolEnum, LogProviderDestinationEnum, LogActionEnum

class Message:
  def __init__(self, 
    level: str,
    message: str,
  ):
    self._level = level.lower()
    self.message = message

  @property
  def level(self):
    return self._level
  
  @level.setter
  def level(self, value):
    self._level = value

  def to_dict(self):
    return {
      "level": self.level,
      "message": self.message,
    }

class AuditMessage(Message):
  def __init__(self, 
    message: str,
    service_name: str,
    target: str,
    user_id: str,
    origin: str,
    log_level=LogLevelEnum.INFO, 
    log_provider=LogProviderDestinationEnum.OPENSEARCH,
    kind=LogAuditKindEnum.OPERATIONAL,
    protocol=LogProtocolEnum.HTTP_1_1,
    action=LogActionEnum.PROCESS_ONE,
    metadata=dict(),
  ):
    super().__init__(str(log_level.value).lower(), message)
    self.message = message
    self.service_name = service_name
    self.target = target
    self.user_id = user_id
    self.origin = origin
    self.log_level = log_level
    self.log_provider = log_provider
    self.kind = kind
    self.action = action
    self.protocol = protocol
    self.metadata = dict(hostname=os.name, **metadata)

  @property
  def level(self):
    return self._level

  @level.setter
  def level(self, value):
    self._level = value
    self.log_level = LogLevelEnum[value.upper()]


  def to_dict(self):
    return {
      "message": self.message,
      "serviceName": self.service_name,
      "target": self.target,
      "userId": self.user_id,
      "origin": self.origin,
      "level": self.level,
      "logLevel": str(self.log_level.value),
      "logProvider": str(self.log_provider.value[0]),
      "action": str(self.action.value),
      "kind": str(self.kind.value[0]),
      "protocol": str(self.protocol.value[0]),
      "metadata": self.metadata
    }