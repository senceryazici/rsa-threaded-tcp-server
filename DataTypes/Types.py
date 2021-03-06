class ConfirmationTypes:
    """Self explanatory :("""

    """Received by server if the client's connection is refused.
        id:CLIENT_ID, type:CONNECTION_REFUSED"""
    CONNECTION_REFUSED = "CONNECTION_REFUSED"

    """Sent by either server or client to reject previous request
        id:CLIENT_ID, type:REJECTED, request:PREVIOUS_REQUEST"""
    REJECTED = "REJECTED"


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

    """Sent by client to terminate connection.
        id:CLIENT_ID, type:DISCONNECTION_REQUEST"""
    DISCONNECTION_REQUEST = "DISCONNECTION_REQUEST"

    """Sent by client to gather information about the active connections.
        id:CLIENT_ID, type:SERVER_INFO_REQUEST"""
    SERVER_INFO_REQUEST = "SERVER_INFO_REQUEST"

class MessageTypes:
    """Text Message Types. Usage:
    Client sends CARRY_MESSAGE to the server, and server fowards the message as TEXT_MESSAGE."""

    """Sent by client to foward the message to another client
        id:CLIENT_ID, to:string_array_of_client_id, content:MESSAGE, type:CARRY_MESSAGE"""
    CARRY_MESSAGE = "CARRY_MESSAGE"

    """Sent by server, to a client.
        id/from:CLIENT_ID/SENDER_ID, to:string_array_of_client_id, content:MESSAGE, type:TEXT_MESSAGE"""
    TEXT_MESSAGE = "TEXT_MESSAGE"
    
class TcpTypes:
    """TCP Communication Message Types"""

    """Sent by client to maintain connection and prevent timeout.
        id:CLIENT_ID, type:KEEP_ALIVE"""
    KEEP_ALIVE = "KEEP_ALIVE"
