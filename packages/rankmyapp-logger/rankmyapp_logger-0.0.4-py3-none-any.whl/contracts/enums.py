from enum import Enum

class LogActionEnum(Enum):
    CREATE_MANY = 'CREATE_MANY'
    CREATE_ONE = 'CREATE_ONE'
    DELETE_MANY = 'DELETE_MANY'
    DELETE_ONE = 'DELETE_ONE'
    UPDATE_ALL = 'UPDATE_ALL'
    UPDATE_ONE = 'UPDATE_ONE'
    FIND_ONE = 'FIND_ONE'
    FIND_ALL = 'FIND_ALL'
    PROCESS_ONE = 'PROCESS_ONE'
    PROCESS_MANY = 'PROCESS_MANY'

class LogLevelEnum(Enum):
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    ERROR = 'ERROR'
    WARN = 'WARN'

class LogProtocolEnum(Enum):
    HTTP_1_1 = 'HTTP_1_1',
    AMQP_RMQ = 'AMQP_RMQ',

class	LogAuditKindEnum(Enum):
    AUDIT = 'AUDIT',
    OPERATIONAL = 'OPERATIONAL',

class LogProviderDestinationEnum(Enum):
    GRAYLOG = 'GRAYLOG',
    OPENSEARCH = 'OPENSEARCH',