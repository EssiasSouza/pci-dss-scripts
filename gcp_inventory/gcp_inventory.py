from google.cloud import asset_v1

client = asset_v1.AssetServiceClient()

parent = "projects/gringo-vpc"

response = client.list_assets(
    request={
        "parent": parent,
        "content_type": asset_v1.ContentType.RESOURCE,
        "page_size": 1000
    }
)

for asset in response:
    print(asset.asset_type)
    print(asset.name)
    with open("gringo_inventory.csv", "a", encoding="utf-8") as file:
        file.write(f"{asset.asset_type};{asset.name}\n")