import asyncio
import random
import ssl
import json
import time
import uuid
from loguru import logger
from aiohttp import ClientSession, ClientTimeout
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector


ID = "ТУТ ID"



user_agent = UserAgent(os='windows', platforms='pc', browsers='chrome')
async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
    logger.info(device_id)
    random_user_agent = user_agent.random
    while 'Windows' not in random_user_agent:
        random_user_agent = user_agent.random
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": random_user_agent,
                "Origin": "chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi"
            }
            connector = ProxyConnector.from_url(socks5_proxy)
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                uri = random.choice(["wss://proxy.wynd.network:4444/", "wss://proxy.wynd.network:4650/"])
                async with session.ws_connect(uri, headers=custom_headers,
                                              ssl=ssl.create_default_context()) as websocket:
                    logger.info("Connected to websocket via proxy")

                    async def send_ping():
                        while True:
                            send_message = json.dumps(
                                {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                            logger.debug(send_message)
                            await websocket.send_str(send_message)
                            await asyncio.sleep(5)

                    await asyncio.sleep(1)
                    asyncio.create_task(send_ping())

                    while True:
                        response = await websocket.receive()
                        message = response.json()
                        logger.info(message)
                        if message.get("action") == "AUTH":
                            auth_response = {
                                "id": message["id"],
                                "origin_action": "AUTH",
                                "result": {
                                    "browser_id": device_id,
                                    "user_id": user_id,
                                    "user_agent": custom_headers['User-Agent'],
                                    "timestamp": (time.time()),
                                    "device_type": "extension",
                                    "version": "4.26.2",
                                    "extension_id": "lkbnfiajjmbhnfledhphioinpickokdi"
                                }
                            }
                            logger.debug(auth_response)
                            await websocket.send_str(json.dumps(auth_response))

                        elif message.get("action") == "PONG":
                            pong_response = {"id": message["id"], "origin_action": "PONG"}
                            logger.debug(pong_response)
                            await websocket.send_str(json.dumps(pong_response))
        except Exception as e:
            logger.error(e)
            logger.error(socks5_proxy)


async def main():

    _user_id = ID
    with open('proxy.txt', 'r') as file:
            local_proxies = file.read().splitlines()
    tasks = [asyncio.ensure_future(connect_to_wss(i, _user_id)) for i in local_proxies ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':

    asyncio.run(main())
