import asyncio
import aiohttp
import ssl

def function():
    # The URLs and headers (blank in this demo) that will be requested async
    routes = [("https://vstfrd.redmond.corp.microsoft.com", ""), ("https://internalsite/api/2", "")]

    # Create out SSL context object with our CA cert file
    sslcontext = ssl.create_default_context(cafile="/etc/ssl/certs/ca-certificates.crt")

    # Pass this SSL context to aiohttp and create a TCPConnector
    conn = aiohttp.TCPConnector(ssl_context=sslcontext)

    # Using this TCPConnector, open a session
    with aiohttp.ClientSession(connector=conn) as client:
        # This is the asyncio part
        # Create a list of futures
        futures = [
            fetch_json(client, url=url, headers=headers)
            for (url, headers) in routes
        ]

        # Then wait for the futures to all complete
        content = asyncio.get_event_loop().run_until_complete(asyncio.wait(futures))

        # Extract the resulting data
        data = [item.result() for item in content[0]]
    return data

async def fetch_json(client, url, headers):
    async with client.get(url, headers=headers) as resp:
        return await resp.json()
