class ConfirmationTypes:
    """Self explanatory :("""

    """Received by server if the client's connection is refused.
        id:CLIENT_ID, type:CONNECTION_REFUSED"""
    CONNECTION_REFUSED = "CONNECTION_REFUSED"

class InfoTypes:
    """Information Types"""

    """Received by server, storing client id, rsa public key and connection timeout.
        id:CLIENT_ID, rsa-public-key:KEY, timeout:TIMEOUT(SEC) type:CONNECTION_INFO"""
    CONNECTION_INFO = "CONNECTION_INFO"

    """Sent by server, containing all active clients' id's.
        clients:string_array_of_client_id, type:SERVER_INFO"""
    SERVER_INFO = "SERVER_INFO"

    """Stores information of current connection, content:True/False
        id:CLIENT_ID, content:True/False, type:CONNECTION_STATUS"""
    CONNECTION_STATUS = "CONNECTION_STATUS"


class RequestTypes:
    """Request Types to create requests"""

    """Sent by client to establish a connection.
        id:CLIENT_ID, type:CONNECTION_REQUEST"""
    CONNECTION_REQUEST = "CONNECTION_REQUEST"

class MessageTypes:
    """Text Message Types"""

    """Sent by client to foward the message to another client
        id:CLIENT_ID, to:string_array_of_client_id, content:MESSAGE, type:CARRY_MESSAGE"""
    CARRY_MESSAGE = "CARRY_MESSAGE"

    """Sent by either server or client, to a client or to the server.
        id/from:CLIENT_ID/SENDER_ID, to:string_array_of_client_id, content:MESSAGE, type:TEXT_MESSAGE"""
    TEXT_MESSAGE = "TEXT_MESSAGE"

class TcpTypes:
    """TCP Communication Message Types"""

    """Sent by client to maintain connection and prevent timeout.
        id:CLIENT_ID, type:KEEP_ALIVE"""
    KEEP_ALIVE = "KEEP_ALIVE"
