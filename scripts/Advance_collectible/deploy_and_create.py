from brownie import AdvanceCollectible, network, config
from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)


sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

# OPENSEA_URL = "https://iknow.io/lambo/143/{}/{}"


def deploy_and_create():
    account = get_account()
    advanceCollectible = AdvanceCollectible.deploy(
        get_contract("vrf_coordinator"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        1,
        2,
        3,
        {"from": account},
    )
    fund_with_link(advanceCollectible.address)
    advance_tx = advanceCollectible.createCollectible({"from": account})
    advance_tx.wait(1)
    print("new token has been created....!!!")
    return advanceCollectible, advance_tx


def main():
    deploy_and_create()
