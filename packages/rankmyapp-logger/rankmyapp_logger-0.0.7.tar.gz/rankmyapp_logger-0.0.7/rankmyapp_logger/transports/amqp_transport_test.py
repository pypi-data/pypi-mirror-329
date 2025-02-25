import unittest
from unittest.mock import patch
from contracts.transport import AuditAmqpTransport
from contracts.message import AuditMessage, Message
from contracts.enums import LogActionEnum, LogAuditKindEnum, LogLevelEnum, LogProtocolEnum, LogProviderDestinationEnum

def create_audit_message_fixture(**kwargs):
    params = dict()
    params["message"]="mensagem"
    params["service_name"]='service'
    params["kind"]=LogAuditKindEnum.AUDIT
    params["log_level"]=LogLevelEnum.INFO
    params["log_provider"]=LogProviderDestinationEnum.GRAYLOG
    params["origin"]="test"
    params["protocol"]=LogProtocolEnum.AMQP_RMQ
    params["target"]="test_target"
    params["action"]=LogActionEnum.CREATE_MANY
    params["user_id"]="56"
    params["metadata"]=dict()

    return AuditMessage(**{**params, **kwargs})

def create_simple_message_fixture(**kwargs):
    params = dict()
    params["message"]="mensagem"
    params["level"]="warn"

    return Message(**{**params, **kwargs})

class TestAuditAmqpTransport(unittest.TestCase):
  @patch("transports.audit.amqp_transport.AuditAmqpTransport.log")
  def test_sends_log_without_throwing(self, mock_amqp_transport_instance):
    audit_amqp_transport = AuditAmqpTransport('amqp://rabbitmq:rabbitmq@localhost:5672', 'queue')
    try:
      audit_message_fixture = create_audit_message_fixture(message="minhamensagem")

      audit_amqp_transport.info(audit_message_fixture)
      audit_amqp_transport.warn(audit_message_fixture)
      audit_amqp_transport.debug(audit_message_fixture)

      self.assertEqual(mock_amqp_transport_instance.call_count, 3)
    finally:
      audit_amqp_transport.close()

  @patch("transports.audit.amqp_transport.AuditAmqpTransport.info")
  def test_throw_error_when_service_is_unavailable(self, mock_amqp_transport_instance):
    mock_amqp_transport_instance.side_effect = Exception("Service is unavailable")

    audit_amqp_transport = AuditAmqpTransport('amqp://rabbitmq:rabbitmq@localhost:5672', 'queue')

    audit_message_fixture = create_audit_message_fixture(message="minhamensagem")

    with self.assertRaises(Exception) as ctx:
      audit_amqp_transport.info(audit_message_fixture)

    self.assertEqual(str(ctx.exception), "Service is unavailable")

  def test_throw_error_when_the_message_param_is_not_an_audit_message(self):
    audit_amqp_transport = AuditAmqpTransport('amqp://rabbitmq:rabbitmq@localhost:5672', 'queue')
    fake_audit_message_fixture = create_simple_message_fixture(message="minhamensagem")
    
    with self.assertRaises(ValueError) as ctx:
      audit_amqp_transport.info(fake_audit_message_fixture)

    self.assertEqual(str(ctx.exception), 'Message parameter isn\'t a AuditMessage instance!')

if __name__ == '__main__':
    unittest.main()