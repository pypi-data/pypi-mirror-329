import unittest
from unittest.mock import patch
from contracts.enums import LogActionEnum, LogAuditKindEnum, LogLevelEnum, LogProtocolEnum, LogProviderDestinationEnum
from transports.http_transport import AuditHttpTransport
from contracts.message import AuditMessage, Message

def create_audit_message_fixture(**kwargs):
    params = dict()
    params["message"]="mensagem"
    params["service_name"]='service'
    params["kind"]=LogAuditKindEnum.OPERATIONAL
    params["log_level"]=LogLevelEnum.WARN
    params["log_provider"]=LogProviderDestinationEnum.GRAYLOG
    params["origin"]="test"
    params["protocol"]=LogProtocolEnum.HTTP_1_1
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

def create_successfull_response_fixture(**kwargs):
   return { "status_code": 200, "headers": dict(), "body": dict(), **kwargs }

class TestAuditHttpTransport(unittest.TestCase):
  @patch("services.http.http_service")
  def test_sends_log_without_throwing(self, mock_http_service_instance):
    mock_http_service_instance.request.return_value = create_successfull_response_fixture()

    audit_http_transport = AuditHttpTransport('http://fake-url:10000')
    audit_http_transport._http_service = mock_http_service_instance

    audit_message_fixture = create_audit_message_fixture()

    audit_http_transport.info(audit_message_fixture)
    audit_http_transport.warn(audit_message_fixture)
    audit_http_transport.debug(audit_message_fixture)
    result = mock_http_service_instance.request.return_value

    self.assertEqual(mock_http_service_instance.request.call_count, 3)
    self.assertEqual(result['status_code'], 200)

  @patch("services.http.http_service")
  def test_throw_error_when_service_is_unavailable(self, mock_http_service_instance):
    mock_http_service_instance.request.side_effect = Exception("Erro na requisição HTTP")

    audit_http_transport = AuditHttpTransport('http://fake-url:10000')
    audit_http_transport._http_service = mock_http_service_instance

    audit_message_fixture = create_audit_message_fixture(message="minhamensagem")

    with self.assertRaises(Exception) as ctx:
      audit_http_transport.info(audit_message_fixture)
    
    self.assertEqual(str(ctx.exception), "Erro na requisição HTTP")

  def test_throw_error_when_the_message_param_is_not_an_audit_message(self):
    audit_http_transport = AuditHttpTransport('http://fake-url:10000')
    fake_audit_message_fixture = create_simple_message_fixture(message="minhamensagem")

    with self.assertRaises(ValueError) as ctx:
      audit_http_transport.info(fake_audit_message_fixture)
    
    self.assertEqual(str(ctx.exception), 'Message parameter isn\'t a AuditMessage instance!')

  def test_throw_error_when_the_message_protocol_is_http_and_provider_is_opensearch(self):
    audit_http_transport = AuditHttpTransport('http://fake-url:10000')
    audit_message_fixture = create_audit_message_fixture(log_provider=LogProviderDestinationEnum.OPENSEARCH)

    with self.assertRaises(ValueError) as ctx:
      audit_http_transport.info(audit_message_fixture)
    
    self.assertEqual(str(ctx.exception), 'You can\'t send http log to OPENSEARCH destination')

if __name__ == '__main__':
    unittest.main()