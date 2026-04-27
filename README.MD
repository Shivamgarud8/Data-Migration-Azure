# Multi-Cloud Data Migration Pipeline (AWS to Azure)

> An end-to-end automated data pipeline that captures user data from a web application, persists it in a relational database, and migrates it across cloud platforms — from AWS DynamoDB to Azure Cosmos DB — using Python automation scripts.

---

## Table of Contents

- [Project Summary](#project-summary)
- [Tech Stack](#tech-stack)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Step-by-Step Setup](#step-by-step-setup)
  - [1. AWS EC2 Server Setup](#1-aws-ec2-server-setup)
  - [2. Web Application Setup](#2-web-application-setup)
  - [3. MariaDB Configuration](#3-mariadb-configuration)
  - [4. AWS IAM and CLI Configuration](#4-aws-iam-and-cli-configuration)
  - [5. DynamoDB Table Setup](#5-dynamodb-table-setup)
  - [6. MariaDB to DynamoDB Migration](#6-mariadb-to-dynamodb-migration)
  - [7. Azure Cosmos DB Setup](#7-azure-cosmos-db-setup)
  - [8. DynamoDB to Cosmos DB Migration](#8-dynamodb-to-cosmos-db-migration)
  - [9. Security and Credential Handling](#9-security-and-credential-handling)
  - [10. GitHub Integration](#10-github-integration)
- [Key Features](#key-features)
- [Learning Outcomes](#learning-outcomes)
- [Future Enhancements](#future-enhancements)

---

## Project Summary

This project demonstrates a real-world, production-style multi-cloud data migration pipeline. A PHP-backed HTML form collects user data and stores it in a MariaDB instance running on AWS EC2. Two Python migration scripts then move the data sequentially — first from MariaDB into AWS DynamoDB, then from DynamoDB into Azure Cosmos DB — handling SQL-to-NoSQL transformation, pagination, and secure credential management throughout.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5 |
| Backend | PHP |
| Local Database | MariaDB (on EC2) |
| AWS NoSQL | Amazon DynamoDB |
| Azure NoSQL | Azure Cosmos DB (Core SQL API) |
| Cloud Compute | Amazon EC2 |
| Identity & Access | AWS IAM |
| Migration Scripts | Python 3, Boto3, azure-cosmos, pymysql |
| Version Control | Git, GitHub |

---

## Architecture Overview

![Architecture](jen/d1.png).

**Data Flow Summary**

```
User Input  -->  HTML Form  -->  PHP  -->  MariaDB  -->  DynamoDB (AWS)  -->  Cosmos DB (Azure)
```

---

## Prerequisites

Before starting, ensure you have the following:

- An active **AWS account** with permissions to create EC2, DynamoDB, and IAM resources
- An active **Azure account** with permissions to create Cosmos DB resources
- A local machine with **Git** installed
- Basic familiarity with Linux terminal commands

---

## Step-by-Step Setup

### 1. AWS EC2 Server Setup

**Launch an EC2 Instance**

1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).
2. Navigate to **EC2 > Instances > Launch Instance**.
3. Select **Amazon Linux 2** or **Ubuntu 22.04 LTS** as the AMI.
4. Choose instance type `t2.micro` (free tier eligible).
5. Configure security group to allow:
   - Port `22` (SSH)
   - Port `80` (HTTP)
6. Download your `.pem` key pair and launch.

**Connect to the instance**

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@<your-ec2-public-ip>
```

**Install required packages**

```bash
# Update system
sudo yum update -y   # Amazon Linux
# or
sudo apt update && sudo apt upgrade -y   # Ubuntu

# Install Apache, PHP, MariaDB
sudo yum install -y httpd php php-mysqlnd mariadb-server   # Amazon Linux
# or
sudo apt install -y apache2 php php-mysql mariadb-server   # Ubuntu

# Install Python and pip
sudo yum install -y python3 python3-pip   # Amazon Linux
# or
sudo apt install -y python3 python3-pip   # Ubuntu

# Start and enable services
sudo systemctl start httpd mariadb
sudo systemctl enable httpd mariadb
```

---

### 2. Web Application Setup

Create the HTML form at `/var/www/html/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>User Registration</title>
</head>
<body>
  <h2>User Registration Form</h2>
  <form action="submit.php" method="POST">
    <label>Name: <input type="text" name="name" required></label><br><br>
    <label>Phone: <input type="text" name="phone" required></label><br><br>
    <label>Age: <input type="number" name="age" required></label><br><br>
    <button type="submit">Submit</button>
  </form>
</body>
</html>
```

Create the PHP handler at `/var/www/html/submit.php`:

```php
<?php
$host     = "localhost";
$user     = "root";
$password = "your_db_password";
$database = "user_app";

$conn = new mysqli($host, $user, $password, $database);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$name  = $_POST['name'];
$phone = $_POST['phone'];
$age   = $_POST['age'];

$stmt = $conn->prepare("INSERT INTO users (name, phone, age) VALUES (?, ?, ?)");
$stmt->bind_param("ssi", $name, $phone, $age);
$stmt->execute();

echo "User data saved successfully.";
$conn->close();
?>
```

---

### 3. MariaDB Configuration

```bash
# Secure MariaDB installation
sudo mysql_secure_installation
```

Log in and configure the database:

```sql
-- Log into MariaDB
sudo mysql -u root -p

-- Create database and table
CREATE DATABASE user_app;
USE user_app;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100),
    phone   VARCHAR(20),
    age     INT
);

-- Verify
SHOW TABLES;
DESCRIBE users;

EXIT;
```

---

### 4. AWS IAM and CLI Configuration

**Create an IAM User for programmatic access**

1. Go to **AWS Console > IAM > Users > Add User**.
2. Set a username (e.g., `migration-bot`).
3. Select **Programmatic access**.
4. Attach policy: `AmazonDynamoDBFullAccess`.
5. Save the **Access Key ID** and **Secret Access Key**.

**Configure AWS CLI on EC2**

```bash
# Install AWS CLI if not present
pip3 install awscli

# Configure credentials
aws configure
# Provide:
#   AWS Access Key ID
#   AWS Secret Access Key
#   Default region: eu-north-1
#   Output format: json

# Verify configuration
aws sts get-caller-identity
```

---

### 5. DynamoDB Table Setup

```bash
aws dynamodb create-table \
  --table-name users \
  --attribute-definitions AttributeName=user_id,AttributeType=N \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-north-1
```

Verify the table was created:

```bash
aws dynamodb describe-table --table-name users --region eu-north-1
```

---

### 6. MariaDB to DynamoDB Migration

Install Python dependencies:

```bash
pip3 install pymysql boto3
```

Create `migrate_to_dynamo.py`:

```python
import pymysql
import boto3

# MariaDB connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="your_db_password",
    database="user_app"
)

cursor = db.cursor()
cursor.execute("SELECT user_id, name, phone, age FROM users")
rows = cursor.fetchall()

# DynamoDB connection
dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
table = dynamodb.Table("users")

migrated = 0
for row in rows:
    user_id, name, phone, age = row
    table.put_item(Item={
        "user_id": user_id,
        "name": name,
        "phone": phone,
        "age": age
    })
    migrated += 1

print(f"Migration complete. {migrated} records moved to DynamoDB.")
db.close()
```

Run the script:

```bash
python3 migrate_to_dynamo.py
```

---

### 7. Azure Cosmos DB Setup

**Create a Cosmos DB Account**

1. Log in to the [Azure Portal](https://portal.azure.com/).
2. Navigate to **Create a resource > Azure Cosmos DB**.
3. Select **Core (SQL) API**.
4. Configure:
   - **Subscription**: Your active subscription
   - **Resource Group**: Create new, e.g., `migration-rg`
   - **Account Name**: e.g., `user-migration-cosmos`
   - **Location**: Choose the nearest region (e.g., East US)
   - **Capacity Mode**: Serverless
5. Click **Review + Create**, then **Create**.

**Create Database and Container**

Once the account is deployed:

1. Go to your Cosmos DB account > **Data Explorer**.
2. Click **New Database**:
   - Database ID: `user_db`
3. Click **New Container**:
   - Database ID: `user_db`
   - Container ID: `users`
   - Partition Key: `/user_id`
4. Click **OK**.

**Retrieve Connection Credentials**

1. In your Cosmos DB account, go to **Settings > Keys**.
2. Copy:
   - **URI** (the endpoint URL)
   - **PRIMARY KEY**

Store these as environment variables — never hardcode them:

```bash
export AZURE_COSMOS_ENDPOINT="https://your-account.documents.azure.com:443/"
export AZURE_COSMOS_KEY="your_primary_key_here"
```

To persist across sessions, add the above lines to `~/.bashrc` or `~/.bash_profile`:

```bash
echo 'export AZURE_COSMOS_ENDPOINT="https://your-account.documents.azure.com:443/"' >> ~/.bashrc
echo 'export AZURE_COSMOS_KEY="your_primary_key_here"' >> ~/.bashrc
source ~/.bashrc
```

---

### 8. DynamoDB to Cosmos DB Migration

Install dependencies:

```bash
pip3 install boto3 azure-cosmos
```

Create `migrate_to_cosmos.py`:

```python
import os
import boto3
from decimal import Decimal
from azure.cosmos import CosmosClient

# Load Azure credentials from environment variables
endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
key      = os.environ["AZURE_COSMOS_KEY"]

# Azure Cosmos DB client
cosmos_client = CosmosClient(endpoint, credential=key)
database      = cosmos_client.get_database_client("user_db")
container     = database.get_container_client("users")

# DynamoDB client
dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
table    = dynamodb.Table("users")

def convert_decimals(obj):
    """Recursively convert Decimal types to int or float for Cosmos DB."""
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

# Paginate through DynamoDB and upsert into Cosmos DB
migrated     = 0
last_key     = None

while True:
    if last_key:
        response = table.scan(ExclusiveStartKey=last_key)
    else:
        response = table.scan()

    for item in response.get("Items", []):
        item_clean = convert_decimals(item)
        item_clean["id"] = str(item_clean["user_id"])   # Cosmos DB requires an "id" field
        container.upsert_item(item_clean)
        migrated += 1

    last_key = response.get("LastEvaluatedKey")
    if not last_key:
        break

print(f"Migration complete. {migrated} records upserted into Azure Cosmos DB.")
```

Run the script:

```bash
python3 migrate_to_cosmos.py
```

**Verify in Azure Portal**

1. Go to your Cosmos DB account > **Data Explorer > user_db > users > Items**.
2. Confirm all records are present.

---

### 9. Security and Credential Handling

- Never hardcode credentials in source files.
- Always use **environment variables** for API keys, database passwords, and cloud access credentials.
- Add a `.env` file to `.gitignore` if used locally:

```bash
echo ".env" >> .gitignore
```

- If credentials are accidentally committed, rotate them immediately from the respective cloud console (AWS IAM > Security credentials / Azure Portal > Cosmos DB Keys).
- Review your Git history and remove sensitive data using `git filter-branch` or [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) before pushing to a public repository.

---

### 10. GitHub Integration

```bash
# Initialize Git in your project directory
git init

# Add a .gitignore file to exclude secrets and unnecessary files
cat <<EOF > .gitignore
.env
*.pem
__pycache__/
*.pyc
EOF

# Stage and commit your code
git add .
git commit -m "Initial commit: Multi-cloud data migration pipeline"

# Add remote and push
git remote add origin https://github.com/your-username/multi-cloud-migration.git
git branch -M main
git push -u origin main
```

---

## Key Features

- End-to-end multi-cloud data migration from AWS to Azure
- SQL to NoSQL data transformation with type safety
- Pagination support for large DynamoDB datasets
- Secure credential management via environment variables
- Upsert logic preventing duplicate entries in Cosmos DB
- LAMP-style web application for real-time data ingestion

---

## Learning Outcomes

- Hands-on experience provisioning and configuring cloud infrastructure on both AWS and Azure
- Understanding of relational-to-NoSQL data modeling and migration strategies
- Practical application of AWS IAM roles, policies, and CLI tooling
- Cross-cloud architecture design and trade-off analysis
- Debugging real-world deployment issues including credential exposure and data type mismatches

---

## Future Enhancements

- Automate the full pipeline using AWS Lambda and CloudWatch Events or a cron job on EC2
- Implement an Azure Data Factory pipeline as an alternative managed migration path
- Add a CI/CD pipeline using GitHub Actions to validate and run migration scripts on push
- Build a monitoring dashboard using AWS CloudWatch and Azure Monitor with unified alerting
- Containerize the migration scripts using Docker for environment consistency and portability
- Add schema validation and data quality checks before each migration stage
- Implement dead-letter logging to capture and retry failed record migrations
- Extend the pipeline to support bidirectional sync between AWS and Azure for disaster recovery scenarios

---

> Built by Shivam | Cloud & DevOps Engineer | [GitHub](https://github.com/your-username) | [LinkedIn](https://linkedin.com/company/cloudbuild-technologies/)
