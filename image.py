import aiohttp
import os

async def save_image_from_url(url, user_id, category):
    try:
        if not os.path.exists(f"downloads/{user_id}/{category}"):
            os.makedirs(f"downloads/{user_id}/{category}")

        filename = url.split("/")[-1]
        path = f"downloads/{user_id}/{category}/{filename}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(path, 'wb') as f:
                        f.write(await resp.read())
                    return path
                else:
                    return None
    except Exception as e:
        return None
