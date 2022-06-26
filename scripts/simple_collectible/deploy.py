from brownie import SimpleCollectible
from scripts.helpful_scripts import get_account,OPENSEA_URL


sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

#OPENSEA_URL = "https://iknow.io/lambo/143/{}/{}"


def deploy_and_create():
    account = get_account()
    simpleCollectable = SimpleCollectible.deploy({"from": account})
    tx = simpleCollectable.createCollectibles(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"you can view your nft {OPENSEA_URL.format(simpleCollectable.address, simpleCollectable.tokenCounter() - 1)}"
    )
    return simpleCollectable


def main():
    deploy_and_create()
