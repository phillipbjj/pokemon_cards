#Needs to be easily searchable with many options for cards based on many factors
#Design the database to store all of the cards for ourself in a way that makes accessing the data efficient.
#Cards in database, table for each card showing their listings as well outside of the database.

import asyncio
"""def main():
    asyncio.run(main())"""
    
async def echo_server(reader, writer):
    while not reader.at_eof():
        data = await reader.read(100)    
        writer.write(data)
        await writer.drain()
    writer.close()
    
async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port=8000)
    await server.serve_forever()
    
 #ASGI Scope
def create_scope(parser):
    return {
        "type": "http",
        "method": parser.method,
        "scheme": "http",
        "raw_path": parser.path,
        "path": parser.path.decode(),
        "headers": parser.headers,
    }   


    
