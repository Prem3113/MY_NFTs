from brownie import network, AdvanceCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account


def main():
    print(f"working on {network.show_active()}")
    advance_collectible = AdvanceCollectible[-1]
    numberofCollectibles = advance_collectible.tokenCounter()
    print(f"you have {numberofCollectibles} tokenids")
    for token_id in range(numberofCollectibles):
        breed = get_breed(advance_collectible.tokenIdToBreed(token_id))
        if not advance_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI()


def set_tokenURI(token_id, nft_contract, token_URI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_URI)
    tx.wait(1)
    print(
        f"Awesome you can view your nft at {OPENSEA_URL.format(nft_contract.address.token_id)}"
    )
