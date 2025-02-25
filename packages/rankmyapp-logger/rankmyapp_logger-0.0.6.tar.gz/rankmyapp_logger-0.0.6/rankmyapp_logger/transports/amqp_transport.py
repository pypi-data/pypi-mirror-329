import pika
from contracts.message import AuditMessage
from contracts.transport import Transport
import json

class AuditAmqpTransport(Transport[AuditMessage]):
    def __init__(self, url, queue):
        super().__init__()
        self._queue = queue

        self._connection = pika.BlockingConnection(pika.URLParameters(url))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=queue)
        
    @property
    def queue(self):
        return self._queue

    def log(self, message: AuditMessage):
        if not isinstance(message, AuditMessage):
            raise ValueError('Message parameter isn\'t a AuditMessage instance!')
        
        message_dict = message.to_dict()
        
        self._channel.basic_publish(
            exchange='',
            routing_key=self._queue,
            body=json.dumps({"pattern": "logs", "data": message_dict}),
            properties=pika.BasicProperties(delivery_mode=2)
        )
    
    def close(self):
        self._connection.close()    

    def info(self, message: AuditMessage):
        self.log(message)

    def error(self, message: AuditMessage):
        self.log(message)
    
    def warn(self, message: AuditMessage):
       self.log(message)

    def debug(self, message: AuditMessage):
        self.log(message)