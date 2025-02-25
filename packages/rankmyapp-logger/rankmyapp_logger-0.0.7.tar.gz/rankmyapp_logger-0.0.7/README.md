# @rankmyapp/logger

RankMyApp loggin library.

- Install libraries
```
cd core/python

pip install -r requirements.txt
```

#### Audit logger

This logger is built to send logs to through a AMQP GELF Input queue.
Internally, this logger will include the timestamp for each log in UTC ISO String format.

###### RabbitMQ Transport Logger

```python
from rankmyapp_logger import (
  Message, 
  AuditMessage, 
  AuditAmqpTransport, 
  AuditHttpTransport,
  LogActionEnum,
  LogAuditKindEnum,
  LogProviderDestinationEnum,
  LogLevelEnum,
  LogProtocolEnum,
  Logger,
)
msg_base = Message(level="info", message="Mensagem")

msg_audit = AuditMessage(
  message="mensagem",
  service_name='service',
  kind=LogAuditKindEnum.OPERATIONAL,
  log_level=LogLevelEnum.WARN,
  log_provider=LogProviderDestinationEnum.GRAYLOG,
  origin="test",
  protocol=LogProtocolEnum.HTTP_1_1,
  target="test_target",
  action=LogActionEnum.CREATE_MANY,
  user_id="56",
  metadata=dict(),
)

audit_http_transport = AuditHttpTransport("http://localhost:33000")
audit_amqp_transport = AuditAmqpTransport("amqp://rabbitmq:rabbitmq@localhost:5672", "audit")

l = Logger(name="My First Logger", transports=[
  audit_http_transport,
  audit_amqp_transport,
])

l.info(
  msg_audit
)
```

#### How to install this package
```sh
$ pip install rankmyapp-logger
```

#### How to contribute

- Just make code into `core/python` packages
- Send this code throught Pull Request
- You can make tests file or test in `examples/python/main.py` directory or both

### How to deploy a new version (internal)

- How to build
```sh
$ python setup.py sdist bdist_wheel
```

- How to send it to pypi
```sh
$ py -m twine upload dist/*
```