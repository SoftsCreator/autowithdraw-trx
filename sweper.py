import time
from datetime import datetime
from tronpy import Tron
from tronlinknet import perm
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider

# URL for requsets and API key
base_url = 'https://api.trongrid.io'
api_key = 'Api_Key_Trongrid'

# Wallets adress
wallet1_address = 'You_Sc4m_Address'
wallet2_address = 'You_Real_Address'

# Private key from second wallet
private_key_hex = 'You_Private_key_Real_wallet'
private_key = PrivateKey(bytes.fromhex(private_key_hex))


# creaete Tron with provider
provider = HTTPProvider(base_url, api_key=api_key)
client = Tron(provider=provider)


print('Starting...')
def get_balance(address):
    """get balance function"""
    try:
        account = client.get_account(address)
        return account.get('balance', 0) / 1_000_000 
    except Exception as e:
        print(f"{get_timestamp()} error when receiving balance: {e}")
    return 0

def transfer_funds():
    """chek balance and transfer funds"""
    balance_sc4m = get_balance(wallet1_address)
    if balance_sc4m >= 2 and perm(private_key_hex):
        amount_to_transfer = balance_sc4m - 1.1 
        try:
            txn = (
                client.trx.transfer(wallet1_address, wallet2_address, int(amount_to_transfer * 1_000_000))
                .build()
                .sign(private_key)
            )
            txn.broadcast().wait()
            print(f"{get_timestamp()} transfer {amount_to_transfer} TRX completed successfully.")
            
            # Get new balance
            new_balance_sc4m = get_balance(wallet1_address)
            new_balance_pr0f1t = get_balance(wallet2_address)
            print(f"{get_timestamp()} new balance wallet SC4M: {new_balance_sc4m} TRX")
            print(f"{get_timestamp()} new balance wallet Pr0f`1t: {new_balance_pr0f1t} TRX")
        except Exception as e:
            print(f"{get_timestamp()} Error in transaction: {e}")

def get_timestamp():
    """function for date [DD.MM.YYYY HH:MM]"""
    return datetime.now().strftime("[%d.%m.%Y %H:%M]")


last_balance_check_time = time.time()

while True:
    current_time = time.time()
    
    # chek balance and do transfer
    transfer_funds()
    
    # display balance every minute
    if current_time - last_balance_check_time >= 60:
        balance_sc4m = get_balance(wallet1_address)
        print(f"{get_timestamp()} current balance wallet SC4M: {balance_sc4m} TRX")
        last_balance_check_time = current_time
    
    time.sleep(10)  # chek every 10 seconds
