import asyncio
import random
import ssl
import json
import time
import uuid
import requests
import websockets
import os, base64
from loguru import logger
from fake_useragent import UserAgent
from base64 import b64decode, b64encode
import aiohttp
from aiohttp import ClientSession, ClientWebSocketResponse

WEBSOCKET_URLS = [
    "wss://proxy2.wynd.network:4650",
    "wss://proxy2.wynd.network:4444"
]

async def connect_to_wss():
    user_agent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    ]
    random_user_agent = random.choice(user_agent)
    device_id = str(uuid.uuid4())
    logger.info(f"Generated Device ID: {device_id}")
    
    websocket_index = 0
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": random_user_agent,
                "Origin": "chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            uri = WEBSOCKET_URLS[websocket_index % len(WEBSOCKET_URLS)]
            websocket_index += 1
            logger.info(f"Connecting to WebSocket: {uri}")
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with ClientSession(connector=connector) as session:
                async with session.ws_connect(
                    uri, 
                    headers=custom_headers, 
                ) as websocket:
                    
                    response = await websocket.receive()
                    message = json.loads(response.data)
                    logger.debug(f"Received message: {message}")

                    if message["action"] == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": "e5ace647-0cb8-46f8-9d47-19abd6d72b1c",
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "4.26.2",
                                "extension_id": "lkbnfiajjmbhnfledhphioinpickokdi"
                            }
                        }
                        logger.debug("Sending authentication request...")
                        await websocket.send_json(auth_response)
                        
                        response_auth = await websocket.receive()
                        message_auth = json.loads(response_auth.data)
                        logger.debug(f"Received auth response: {message_auth}")
                        
                        if message_auth["action"] == "HTTP_REQUEST":
                            headers = {
                                "Content-Type": "application/json; charset=utf-8",
                                "User-Agent": custom_headers['User-Agent']
                            }
                            logger.debug(f"Sending HTTP request to: {message_auth['data']['url']}")
                            async with session.get(message_auth["data"]["url"], headers=headers) as response:
                                result = await response.json()
                                content = await response.text()
                                code = result.get('code')
                                if None == code:
                                    logger.error(f"Error sending HTTP request")
                                    logger.error(f"Status: {response.status}")
                                else:
                                    logger.info(f"HTTP request successful: {code}")
                                    logger.info(f"Status: {response.status}")
                                    response_body = base64.b64encode(content.encode()).decode()
                                    httpreq_response = {
                                        "id": message_auth["id"],
                                        "origin_action": "HTTP_REQUEST",
                                        "result": {
                                            "url": message_auth["data"]["url"],
                                            "status": response.status,
                                            "status_text": response.reason,
                                            "headers": dict(response.headers),
                                            "body": response_body
                                        }
                                    }
                                    logger.debug("Sending HTTP request response...")
                                    await websocket.send_json(httpreq_response)
                            
                                    while True:
                                        send_ping = {
                                            "id": str(uuid.uuid4()),
                                            "version": "1.0.0",
                                            "action": "PING",
                                            "data": {}
                                        }
                                        logger.debug("Sending Ping message...")
                                        await websocket.send_json(send_ping)
                                
                                        response_ping = await websocket.receive()
                                        message_ping = json.loads(response_ping.data)
                                        logger.debug(f"Received Ping response: {message_ping}")
                                        
                                        if message_ping["action"] == "PONG":
                                            pong_response = {
                                                "id": message_ping["id"],
                                                "origin_action": "PONG"
                                            }
                                            logger.debug("Ping Success! Sending PONG response...")
                                            await websocket.send_json(pong_response)
                                            await asyncio.sleep(10,60)
        except Exception as e:
            logger.error(f"WebSocket Error: {e}")

async def main():
    print("Grass Network")
    await connect_to_wss()

if __name__ == '__main__':
    asyncio.run(main())
