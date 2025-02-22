# This code is specific to the hackattic problem
import requests
import hashlib
import json
from dotenv import load_dotenv
import os


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PROBLEM_URL = f"https://hackattic.com/challenges/mini_miner/problem?access_token={ACCESS_TOKEN}"

response = requests.get(PROBLEM_URL)
data = response.json()
difficulty = data["difficulty"]
requirement = "0" * difficulty

block = data["block"]

solved = False
nonce = 0
while not solved:
    serialised_block = json.dumps(block, separators=(",", ":"), sort_keys=True)

    block_hash = hashlib.sha256(serialised_block.encode()).digest()
    block_hash_bits = "".join(f"{byte:08b}" for byte in block_hash)  # Converts it to readable binary
    to_check = block_hash_bits[:difficulty]
    if to_check == requirement:
        solved = True
        print(f"Nonce: {nonce}")
    else:
        nonce += 1
        block["nonce"] = nonce

solution = {
    "nonce": nonce
}
SUBMIT_URL = f"https://hackattic.com/challenges/mini_miner/solve?access_token={ACCESS_TOKEN}"  # Add &plaground=1 if answer already correctly submitted   
response = requests.post(SUBMIT_URL, json=solution)
print(response.json()) 

