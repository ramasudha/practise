import asyncio
import aiohttp
import json


ids = [1264527, 1277333, 1275339, 1273294, 1275004]

base_url = "https://api.openweathermap.org/data/2.5/forecast?id={}"
appid = "4d9995cd11167bf2cd72d44a5ad6bb5e"
#complete_url = base_url.format(id) + "&APPID=" + appid

# C:\Users\Admin\Downloads\city_id_list.json


async def fetch_weather(session, url, *args):
    async with session.get(url) as response:
        return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        for id in ids:
            complete_url = base_url.format(id) + "&APPID=" + appid
            response = await fetch_weather(session, complete_url)
            with open("weather_data1.txt", 'w') as f:
                data = json.dump(response, f)


        print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())





