from os import environ
import logging
import requests
from config import Config
from auction_logic import Auction

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = Config.ROLLUP_HTTP_SERVER_URL
logger.info(f"HTTP rollup_server url is {rollup_server}")

auction = Auction()

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    bid_data = data["payload"]
    user = bid_data["user"]
    amount = bid_data["amount"]
    
    if auction.submit_bid(user, amount):
        notice = {"payload": f"New highest bid by {user}: {amount}"}
        response = requests.post(rollup_server + "/notice", json=notice)
        logger.info(f"Received notice status {response.status_code} body {response.content}")
        return "accept"
    return "reject"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    report = {"payload": auction.get_bid_history()}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
