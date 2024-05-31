from solders.signature import Signature #type: ignore
from solana.rpc.api import Client
import time

def verify_transaction(solana_client, sign : str):

    print("Verifying txn...")
    start_time = time.time()

    """
    With a 3 seconds of delay, 40 tries will result in 2 minutes of continuous tracking. 
    If TXN, takes longer than that we won't track it anymore and consider it fail.
    """

    for _ in range(40):
        
        try:
            txn = solana_client.get_transaction(Signature.from_string(str(sign)), encoding="jsonParsed", commitment="confirmed")

            if txn.value.transaction.meta.err == None:

                stop_time = time.time()

                print(f"Transaction Successful. Completion Period : {stop_time - start_time:.2f} seconds")

                return True
            
            else:
                stop_time = time.time()

                print(f"Transaction Failed. Completion Period : {stop_time - start_time:.2f} seconds")

                return False

        except Exception as Er:

            # # print(f"Error -> {Er}")
            time.sleep(3)
    else:
        print("WARNING! Txn took longer than expected for varification! This txn will be ignored and considered fail.")
        return False

    


