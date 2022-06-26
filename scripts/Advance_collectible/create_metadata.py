from brownie import AdvanceCollectible, network
from scripts.helpful_scripts import get_breed
from scripts.MetaData.sample_metadata import metadata_template
from pathlib import Path
import requests
import json


def main():
    advance_collectible = AdvanceCollectible[-1]
    no_of_advanced_collectibles = advance_collectible.tokenCounter()
    print(f"you have created {no_of_advanced_collectibles} collectibles")
    for tokenId in range(no_of_advanced_collectibles):
        breed = get_breed(advance_collectible.tokenIdToBreed(tokenId))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{tokenId}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_filepath(image_path)
            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_filepath(metadata_file_name)


def upload_to_filepath(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
