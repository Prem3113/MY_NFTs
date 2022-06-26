from brownie import accounts, network, config, Contract, VRFCoordinatorV2Mock, LinkToken
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "mainnet-fork", "ganache"]
OPENSEA_URL = "https://iknow.io/lambo/143/{}/{}"

breed_mapping = {0: "pug", 1: "shiba_inu", 2: "st_bernard"}


def get_breed(breed_number):
    return breed_mapping[breed_number]


def get_account(id=None, index=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorV2Mock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]
        # MockV3Aggregator[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = (
            Contract.from_abi(  # to form a new mock contract from contract data...
                contract_type._name, contract_address, contract_type.abi
            )
        )
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(_decimals=DECIMALS, _initialAnswer=INITIAL_VALUE):
    account = get_account()
    # MockV3Aggregator.deploy(_decimals, _initialAnswer, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorV2Mock.deploy(
        30 * 10**18,
        config["networks"][network.show_active()]["fee"],
        # link_token.address,
        {"from": account},
    )
    print("mocks deployed....!!!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"funded {contract_address}")
    return funding_tx
