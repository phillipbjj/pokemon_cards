#ASGI messages
def create_mesasge(body, more_body):
    return {
        "type": 'http.request',
        'body': body,
        'more_body': more_body,
    }
#First message app sends to server 
"""message = {
    'type': 'http.response.start',
    'status': 200,
    'headers': [(b'content-length': b"0")],
}"""
#Second message if it has body (make content matches length)
"""message = {
    'type': 'http.response.body',
    'body': b'hello',
    'more_body': false,
}"""

