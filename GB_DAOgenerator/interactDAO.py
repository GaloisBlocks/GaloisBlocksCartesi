from web3 import Web3
from eth_abi import encode
from eth_utils import keccak
import json
import random
import time
import datetime

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

with open('contractInfo.json', 'r') as f:
    contract_info = json.load(f)

ABI = contract_info['abi']
contract_address = contract_info['contract_address']

# Cuenta para deploy
deploy_address = web3.eth.accounts[0]

#Esta variable es la que interactua con el servicio frontend
interaction_address = deploy_address
contract_instance = web3.eth.contract(address=contract_address,abi=ABI)

def create_proposal(contract_instance, proposer, proposal_description, proposal_title):

    tx_hash = contract_instance.functions.createProposal(proposal_title,proposal_description).transact({'from':proposer})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def get_active_proposals(contract_instance):
    proposal_count = contract_instance.functions.proposalCount().call()
    active_proposals = []
    for i in range(proposal_count):
        proposal = contract_instance.functions.proposals(i).call()
        print(proposal)
        if int(proposal[-1]) > int(time.time()):
            active_proposals.append({
                'id': i,
                'title': proposal[0],
                'description': proposal[1],
                'votingDeadline': proposal[-1],
                'forVotes': proposal[2],
                'againstVotes': proposal[3],
                'creator': proposal[6]
                })
    return active_proposals

def vote_proposal(contract_instance,voter_address,proposalId,reason):

    tx_hash = contract_instance.functions.vote(str(voter_address),proposalId,reason).transact({'from':voter_address,  'gas': 5000000})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

""" titulo = "antisat proposalnnn"
razon = "vamos a votar por n-bugattis a cada miembro"

x = create_proposal(contract_instance, interaction_address,razon, titulo)
print(x) 
 """
active = get_active_proposals(contract_instance)
print(active)
""" 
razon = "yo también quiero un bugatti"
vote = vote_proposal(contract_instance,interaction_address,2,razon)
print(vote)

active = get_active_proposals(contract_instance)
print(active) """