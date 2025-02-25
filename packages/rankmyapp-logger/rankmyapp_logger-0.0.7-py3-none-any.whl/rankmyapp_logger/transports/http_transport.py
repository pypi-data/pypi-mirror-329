from services.http_service import HttpService
from contracts.message import AuditMessage
from contracts.transport import Transport
from contracts.enums import LogProtocolEnum, LogProviderDestinationEnum

class AuditHttpTransport(Transport[AuditMessage]):
    def __init__(self, endpoint):
        super().__init__()
        self._http_service = HttpService(endpoint)

    def log(self, message: AuditMessage):
        if not isinstance(message, AuditMessage):
            raise ValueError('Message parameter isn\'t a AuditMessage instance!')

        if message.protocol == LogProtocolEnum.HTTP_1_1:
            if message.log_provider == LogProviderDestinationEnum.OPENSEARCH:
                raise ValueError('You can\'t send http log to OPENSEARCH destination')

        opts = {'method': 'POST', 'headers': {'Content-Type': 'application/json'}}

        self._http_service.request({
            'path': 'posts',
            'body': {'message': message.to_dict() },
            **opts,
        })

    def info(self, message: AuditMessage):
        self.log(message)

    def error(self, message: AuditMessage):
        self.log(message)
    
    def warn(self, message: AuditMessage):
       self.log(message)

    def debug(self, message: AuditMessage):
        self.log(message)