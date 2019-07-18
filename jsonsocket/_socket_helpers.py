import json

def receive_message(connection):
    """ Assuming that the first four bytes of the message denotes its length,
        will read an incoming tcp message from a socket connection
    """
    message_length_bytes = connection.recv(4)
    message_length = int.from_bytes(message_length_bytes, "big")
    message_body_bytes = connection.recv(message_length)
    message = _parse_message(message_body_bytes)
    return message

def send_message(connection, body):
    """ Given a connected socket, will serialize the string value "body", send the length
        of the message in the first four bytes, and then sends the message
    """
    message = _format_message(body)
    connection.send(message)
    
def _parse_message(message_body_bytes):
    message_body = message_body_bytes.decode("UTF8")
    payload = json.loads(message_body)
    return payload
    
def _format_message(body):
    json_message = json.dumps(body)
    message_length = len(json_message)
    header_bytes = message_length.to_bytes(4, "big")
    message_bytes = json_message.encode("UTF8")
    message = header_bytes + message_bytes
    return message
