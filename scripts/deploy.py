from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    ## pass the price feed address to our fundme contract
    fund_me = FundMe.deploy(
        price_feed_address,  ## This is how you pass data into the constructor variables
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  ##Use .get in case verify is missing so we dont get index errors
    )  ## Add publish_source to verify and publish source on etherscan. Set env Variable in .env file
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
