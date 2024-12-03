import asyncio
from urllib.parse import parse_qs

class SimpleASGIServer:
    def __init__(self, app, host='127.0.0.1', port=8000):
        self.app = app
        self.host = host
        self.port = port

    async def handle_connection(self, reader, writer):
        # Step 1: Parse HTTP request to ASGI
        print("Step 1: Converting HTTP to ASGI")
        http_request = await reader.read(1024)
        request_lines = http_request.decode().split('\r\n')
        method, path, _ = request_lines[0].split(' ')
        
        # Create ASGI scope
        scope = {
            'type': 'http',
            'method': method,
            'path': path.split('?')[0],
            'query_string': path.split('?')[1].encode() if '?' in path else b'',
            'headers': []
        }
        
        # Step 2: Create ASGI message dictionary
        message = {
            'type': 'http.request',
            'body': b'',
            'more_body': False
        }

        async def receive():
            return message

        async def send(response):
            # Step 3: Convert ASGI response back to HTTP
            print("Step 3: Converting ASGI response to HTTP")
            if response['type'] == 'http.response.start':
                status = response['status']
                headers = response.get('headers', [])
                writer.write(f'HTTP/1.1 {status} OK\r\n'.encode())
                for header in headers:
                    writer.write(f'{header[0].decode()}: {header[1].decode()}\r\n'.encode())
                writer.write(b'\r\n')
            elif response['type'] == 'http.response.body':
                writer.write(response['body'])
                if not response.get('more_body', False):
                    await writer.drain()
                    writer.close()

        # Call the ASGI application
        print("Step 2: Calling ASGI application")
        await self.app(scope, receive, send)

    async def serve(self):
        server = await asyncio.start_server(
            self.handle_connection,
            self.host,
            self.port
        )
        print(f'Server running on {self.host}:{self.port}')
        async with server:
            await server.serve_forever()

class SimpleASGIApplication:
    async def __call__(self, scope, receive, send):
        # Handle the request
        if scope['type'] == 'http':
            # Get the request body
            request = await receive()
            
            # Generate response
            response_body = f"Received {scope['method']} request to {scope['path']}".encode()
            
            # Send response headers
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', b'text/plain'],
                    [b'content-length', str(len(response_body)).encode()]
                ]
            })
            
            # Send response body
            await send({
                'type': 'http.response.body',
                'body': response_body,
                'more_body': False
            })

# Usage example
if __name__ == "__main__":
    app = SimpleASGIApplication()
    server = SimpleASGIServer(app)
    
    asyncio.run(server.serve())