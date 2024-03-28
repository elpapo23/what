from web3 import Web3
from telegram import Bot
import time

# Telegram bot setup
TELEGRAM_TOKEN = '7174947017:AAFziEHVcnj4IvEVQWz2te2DEOxIMEp2Uvo'
CHAT_ID = '-1002087659113'  # The specific Telegram chat ID where notifications should be sent

bot = Bot(TELEGRAM_TOKEN)

# Setup Web3 with Alchemy as the provider
web3_eth = Web3(Web3.HTTPProvider("https://base-mainnet.g.alchemy.com/v2/Fk8eajDiPZ7E2O2lqTOjQlJDCjs8frd_"))

# Uniswap configuration
uniswap_factory_address = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
uniswap_factory_abi = [{
      "anonymous": False,
      "inputs": [
        {"indexed": True, "internalType": "address", "name": "token0", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "token1", "type": "address"},
        {"indexed": False, "internalType": "address", "name": "pair", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "", "type": "uint256"}
      ],
      "name": "PairCreated",
      "type": "event"
    }]  # Uniswap Factory contract ABI

# SushiSwap configuration
sushiswap_factory_address = "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
sushiswap_factory_abi = [{
      "anonymous": False,
      "inputs": [
        {"indexed": True, "internalType": "address", "name": "token0", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "token1", "type": "address"},
        {"indexed": False, "internalType": "address", "name": "pair", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "", "type": "uint256"}
      ],
      "name": "PairCreated",
      "type": "event"
    }]  # SushiSwap Factory contract ABI

uniswap_factory_contract = web3_eth.contract(address=uniswap_factory_address, abi=uniswap_factory_abi)
sushiswap_factory_contract = web3_eth.contract(address=sushiswap_factory_address, abi=sushiswap_factory_abi)

def check_new_pairs():
    uniswap_event_filter = uniswap_factory_contract.events.PairCreated.createFilter(fromBlock='latest')
    sushiswap_event_filter = sushiswap_factory_contract.events.PairCreated.createFilter(fromBlock='latest')

    while True:
        check_and_notify(uniswap_event_filter, "Uniswap")
        check_and_notify(sushiswap_event_filter, "SushiSwap")
        time.sleep(10)  # Check every 10 seconds. Adjust as needed

def check_and_notify(event_filter, dex_name):
    events = event_filter.get_new_entries()
    for event in events:
        pair_address = event.args.pair
        token0 = event.args.token0
        token1 = event.args.token1
        message = f"{dex_name} New Pair: {token0} - {token1} at {pair_address}"
        bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    check_new_pairs()


