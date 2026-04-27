import pymysql
import boto3

# Connect MariaDB
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='shiva',
    database='user_app'
)

cursor = conn.cursor()

# Fetch ALL data
cursor.execute("SELECT id, name, phone, age FROM users")

# Connect DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('users')

for row in cursor.fetchall():
    item = {
        'user_id': str(row[0]),
        'name': row[1],
        'phone': row[2],
        'age': int(row[3])
    }

    table.put_item(Item=item)

print("✅ All data migrated to DynamoDB")
