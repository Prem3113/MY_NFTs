from scripts.Advance_collectible.deploy_and_create import deploy_and_create
from brownie import network, AdvanceCollectible
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
import pytest


def test_can_create_and_deploy():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for localtesting")
    advance_collectible, advance_tx = deploy_and_create()
    requestId = advance_tx.events["requestCollectible"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, advance_collectible.address, {"from": get_account}
    )
    assert advance_collectible.tokenCounter() == 1
    assert advance_collectible.tokenIdToBreed(0) == 777 % 3
