import boto3
from azure.cosmos import CosmosClient
from decimal import Decimal
import uuid

# -----------------------------
# AWS DynamoDB Configuration
# -----------------------------
AWS_REGION = "eu-north-1"
DYNAMODB_TABLE = "users"

# -----------------------------
# Azure Cosmos DB Configuration
# -----------------------------
COSMOS_ENDPOINT = "ENTER YOUE END POINT"
COSMOS_KEY = "ENTER YOUR KEY"
COSMOS_DB = "user_db"
COSMOS_CONTAINER = "users"

# -----------------------------
# Convert Decimal safely
# -----------------------------
def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    else:
        return obj

# -----------------------------
# DynamoDB Connection
# -----------------------------
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

# -----------------------------
# Cosmos DB Connection (FIXED)
# -----------------------------
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# AUTO CREATE DB + CONTAINER (IMPORTANT FIX)
database = client.create_database_if_not_exists(COSMOS_DB)

container = database.create_container_if_not_exists(
    id=COSMOS_CONTAINER,
    partition_key="/id"
)

# -----------------------------
# DynamoDB Scan (PAGINATION FIXED)
# -----------------------------
items = []
response = table.scan()
items.extend(response.get("Items", []))

while "LastEvaluatedKey" in response:
    response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
    items.extend(response.get("Items", []))

print(f"Found {len(items)} records in DynamoDB")

# -----------------------------
# Insert into Cosmos DB
# -----------------------------
for item in items:

    item = convert_decimal(item)

    # Ensure unique ID (VERY IMPORTANT)
    item["id"] = str(item.get("id", item.get("phone", uuid.uuid4())))

    try:
        container.upsert_item(item)
        print(f"Migrated: {item['id']}")
    except Exception as e:
        print(f"Failed for {item['id']} → {e}")

print("✅ Migration Completed Successfully!")
