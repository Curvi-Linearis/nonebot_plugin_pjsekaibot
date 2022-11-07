import httpx

async def Notify(data_to_post):
    url = ""    # your server to receive notification
    async with httpx.AsyncClient() as client:
        await client.post(url, data = data_to_post)
