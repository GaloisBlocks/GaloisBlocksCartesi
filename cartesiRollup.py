# Copyright 2022 Cartesi Pte. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from os import environ
import traceback
import logging
import requests
import random 
import json
from GB_NFTgenerator import compileNFT, interactNFT
from GB_ERC20generator import compileERC20, interactERC20
from GB_DAOgenerator import compileDAO, interactDAO


logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()

def handle_advance(data):
    """
    An advance request may be processed as follows:

    1. A notice may be generated, if appropriate:

    response = requests.post(rollup_server + "/notice", json={"payload": data["payload"]})
    logger.info(f"Received notice status {response.status_code} body {response.content}")

    2. During processing, any exception must be handled accordingly:

    try:
        # Execute sensible operation
        op.execute(params)

    except Exception as e:
        # status must be "reject"
        status = "reject"
        msg = "Error executing operation"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})

    finally:
        # Close any resource, if necessary
        res.close()

    3. Finish processing

    return status
    """

    response = requests.post(rollup_server + "/notice", json={"payload": data["payload"]})
    logger.info(f"Received notice status {response.status_code} body {response.content}")


    """
    The sample code from the Echo DApp simply generates a notice with the payload of the
    request and print some log messages.
    """

    logger.info(f"Received advance request data {data}")

    status = "accept"
    try:
        input = hex2str(data["payload"])

        # BUILD OUTPUT
        print(input)
        parsedInput = input.split(" ")
        print(parsedInput)
        # Create a collection called MyNFT for given address with 100 maxSupply tokens
        # Example 1: "NFT MyNFT MNFT 0x9fFC0375FF244F83877bb2fe47b1bbbE4ab37c25 100"
        if parsedInput[0] == "NFT":
            contract_gen = compileNFT.main(*parsedInput[1:])
            output = str2hex(contract_gen)

        # Example 2: "DAO GB_DAOToken GBTkn 0x9fFC0375FF244F83877bb2fe47b1bbbE4ab37c25 3600"
        # Create DAO contract with GB_DAOToken as governance token, given address as governor and vote_period for 3600 seconds
        elif parsedInput[0] == "DAO":
            contract_gen = compileDAO.main(*parsedInput[1:])
            output = str2hex(contract_gen)

        # Example 3: "ERC20 GB_Token GBT 0x9fFC0375FF244F83877bb2fe47b1bbbE4ab37c25 1000"
        # Create ERC20 contract called "GB_Token" with given address and mint 1000 units to same address
        elif parsedInput[0] == "ERC20":
            contract_gen = compileERC20.main(*parsedInput[1:-1])
            gen_interaction = interactERC20.interact(contract_gen,parsedInput[3])
            mint_interaction = interactERC20.mintTokens(parsedInput[3],parsedInput[3],parsedInput[-1],gen_interaction)
            output = str2hex(contract_gen + " " + mint_interaction)
        else:
            output = str2hex("Wrong String given")

        logger.info("Adding notice with payload: '{input}'" )
        response = requests.post(rollup_server + "/notice", json={ "payload":str2hex(output)})
        logger.info(f"Received notice status {response.status_code} body {response.content}")
  
    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")

    return status

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    response = requests.post(rollup_server + "/report", json={"payload": data["payload"]})
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}
rollup_address = None

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        if "metadata" in data:
            metadata = data["metadata"]
            if metadata["epoch_index"] == 0 and metadata["input_index"] == 0:
                rollup_address = metadata["msg_sender"]
                logger.info(f"Captured rollup address: {rollup_address}")
                continue
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
