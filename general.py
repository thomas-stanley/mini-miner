# A more general piece of code that is less specific to hackattic
import requests
import hashlib
import json



BLOCK_URL = input("Enter block url (if you want to manually input the parts of the block, press enter): ")
SUBMIT_URL = input("Enter url to submit to (if you just want the nonce printing, press enter): ")

if BLOCK_URL:
    response = requests.get(BLOCK_URL)
    data = response.json()
    block = data["block"]
    difficulty = data["difficulty"]
else:
    difficulty = int(input("Enter block difficulty: "))
    block = {
        "nonce": 0
    }
    finished = False
    while not finished:
        print("Begin entering information for the block. When finished, press enter at the next input prompt.")
        information = input("Enter a key and a value, separated with a space (they will be parsed as strings): ")
        if information:
            key, value = information.split()
            block[key] = value
        else:
            finished = True

requirement = "0" * difficulty  # How many leading zeroes are required


solved = False
nonce = 0
while not solved:
    serialised_block = json.dumps(block, separators=(",", ":"), sort_keys=True)  # Gets a string of the json without whitespace and with sorted keys

    block_hash = hashlib.sha256(serialised_block.encode()).digest()  # Hashes and digests in binary
    block_hash_bits = "".join(f"{byte:08b}" for byte in block_hash)  # Converts it to readable binary
    to_check = block_hash_bits[:difficulty]  # Leading bits to check
    if to_check == requirement:
        solved = True
    else:
        nonce += 1
        block["nonce"] = nonce

if SUBMIT_URL:
    solution = {
        "nonce": nonce
    }
    response = requests.post(SUBMIT_URL, json=solution)
    print(response.json())
else:
    print(f"Nonce: {nonce}")
    print(f"For Block: {serialised_block}")