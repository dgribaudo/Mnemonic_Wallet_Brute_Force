import requests
import csv
from datetime import datetime
from bip_utils import *
from multiprocessing import Process, Queue


def check_addresses(address_list):
    global active_addresses
    headers = {'Content-Type': 'application/json'}
    # Prepare a single batch for both transaction count and balance for all addresses
    batch = []
    for k, address in enumerate(address_list):
        batch.append({"jsonrpc": "2.0", "method": "eth_getTransactionCount", "params": [address, "latest"], "id": 2 * k})
        batch.append({"jsonrpc": "2.0", "method": "eth_getBalance", "params": [address, "latest"], "id": 2 * k + 1})

    # Send batch request
    try:
        response = requests.post("http://localhost:8545", headers=headers, json=batch, timeout=None)
        response.raise_for_status()
        results = response.json()
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

    result_mapping = {result['id']: result for result in results}

    # Process and match results more efficiently
    active_addresses = []
    for k in range(len(address_list)):
        txn_count_id = 2 * k
        balance_id = 2 * k + 1

        txn_count_result = result_mapping.get(txn_count_id, {})
        balance_result = result_mapping.get(balance_id, {})

        if 'error' in txn_count_result or 'error' in balance_result:
            error_msg = txn_count_result.get('error', balance_result.get('error'))
            print(f"Error with address {address_list[k]}: {error_msg}")
            active_addresses.append(False)
        else:
            txn_count = int(txn_count_result.get('result', '0x0'), 16)
            balance = int(balance_result.get('result', '0x0'), 16)
            active_addresses.append((txn_count > 0) or (balance > 0))


def list_add(quq, n):
    while quq.qsize() < 100000:
        all_add = []
        all_mnemo = []
        for _ in range(n):
            mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
            seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
            all_mnemo.append(str(mnemonic))
            all_add.append(Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM).DeriveDefaultPath().PublicKey().ToAddress())
        quq.put([all_mnemo, all_add])

if __name__ == '__main__':
    queue = Queue()
    processes = []
    n_add = int(input("Number of Add in a Batch: "))
    n_pr = int(input("Number of Processes: "))
    active_addresses = []
    money_add = []
    count = 0
    found = 0
    for _ in range(n_pr):
        p = Process(target=list_add, args=(queue, n_add))
        p.start()
        processes.append(p)
    try:
        while found == 0:
            addresses = queue.get()
            check_addresses(addresses[1])
            for i, active in enumerate(active_addresses):
                if active:
                    money_add.append([addresses[0][i], addresses[1][i]])
            if len(money_add) != 0:
                found += len(money_add)
                with open("excel/active.csv", mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerows(money_add)
                print("***** F O U N D  $$$$$$$$$$$ *****")
            count += n_add
            print(datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + " - " + str(found) + "/" + str(count))
    except KeyboardInterrupt:
        print("Terminating processes...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()