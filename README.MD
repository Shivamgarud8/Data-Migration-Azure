# Multi-Cloud Data Migration Pipeline (AWS to Azure)

> An end-to-end automated data pipeline that captures user data from a web application, persists it in a relational database, and migrates it across cloud platforms — from AWS DynamoDB to Azure Cosmos DB — using Python automation scripts.



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


<style>
@keyframes flow1 { 0%{stroke-dashoffset:200} 100%{stroke-dashoffset:0} }
@keyframes flow2 { 0%{stroke-dashoffset:240} 100%{stroke-dashoffset:0} }
@keyframes flow3 { 0%{stroke-dashoffset:180} 100%{stroke-dashoffset:0} }
@keyframes pulse { 0%,100%{r:5;opacity:1} 50%{r:8;opacity:.5} }
@keyframes pulse2 { 0%,100%{r:5;opacity:1} 50%{r:8;opacity:.4} }
@keyframes pulse3 { 0%,100%{r:5;opacity:1} 50%{r:8;opacity:.5} }
@keyframes dot-travel1 { 0%{offset-distance:0%} 100%{offset-distance:100%} }
@keyframes dot-travel2 { 0%{offset-distance:0%} 100%{offset-distance:100%} }
@keyframes dot-travel3 { 0%{offset-distance:0%} 100%{offset-distance:100%} }
@keyframes fadein { from{opacity:0;transform:translateY(-6px)} to{opacity:1;transform:translateY(0)} }
@keyframes shimmer { 0%,100%{opacity:.7} 50%{opacity:1} }
@keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }

.lane-label { font-size:11px; fill:#888780; font-family:var(--font-sans); }
.box-title { font-size:13px; font-weight:500; font-family:var(--font-sans); }
.box-sub { font-size:11px; font-family:var(--font-sans); }
.arrow-label { font-size:10px; font-family:var(--font-sans); fill:#888780; }

.node1 { animation: fadein .5s ease both .1s; }
.node2 { animation: fadein .5s ease both .3s; }
.node3 { animation: fadein .5s ease both .5s; }
.node4 { animation: fadein .5s ease both .7s; }
.node5 { animation: fadein .5s ease both .9s; }
.node6 { animation: fadein .5s ease both 1.1s; }
.node7 { animation: fadein .5s ease both 1.3s; }

.pipe1 { stroke-dasharray:6 4; stroke-dashoffset:200; animation: flow1 1.8s linear infinite 1.6s; }
.pipe2 { stroke-dasharray:6 4; stroke-dashoffset:240; animation: flow2 2s linear infinite 2s; }
.pipe3 { stroke-dasharray:6 4; stroke-dashoffset:180; animation: flow3 1.6s linear infinite 2.4s; }

.dot1 { offset-path: path('M340,118 L340,158'); animation: dot-travel1 1.8s linear infinite 1.6s; }
.dot2 { offset-path: path('M340,270 L340,310'); animation: dot-travel2 2s linear infinite 2s; }
.dot3 { offset-path: path('M340,422 L340,462'); animation: dot-travel3 1.6s linear infinite 2.4s; }
</style>

<svg width="100%" viewBox="0 0 680 620" role="img">
<title>Multi-cloud data migration pipeline: browser to EC2 to DynamoDB to Cosmos DB</title>
<desc>Animated architecture diagram showing data flowing from a user browser through PHP on EC2, MariaDB, AWS DynamoDB, and finally Azure Cosmos DB.</desc>
<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>

  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>
</defs>

<!-- ── BACKGROUND LANES ── -->
<rect x="52" y="22" width="614" height="108" rx="10" fill="#E6F1FB" opacity=".18"/>
<rect x="52" y="148" width="614" height="108" rx="10" fill="#E1F5EE" opacity=".2"/>
<rect x="52" y="274" width="614" height="120" rx="10" fill="#FAEEDA" opacity=".22"/>
<rect x="52" y="412" width="614" height="120" rx="10" fill="#EEEDFE" opacity=".2"/>

<text class="lane-label" x="60" y="36">User</text>
<text class="lane-label" x="60" y="162">EC2 instance</text>
<text class="lane-label" x="60" y="288">AWS cloud  ·  eu-north-1</text>
<text class="lane-label" x="60" y="426">Azure cloud</text>

<!-- ── ROW 1: BROWSER ── -->
<g class="node1">
  <rect x="220" y="44" width="240" height="72" rx="10" fill="#B5D4F4" stroke="#378ADD" stroke-width="1.2"/>
  <!-- browser chrome -->
  <rect x="238" y="56" width="56" height="42" rx="5" fill="none" stroke="#185FA5" stroke-width="1"/>
  <line x1="238" y1="66" x2="294" y2="66" stroke="#185FA5" stroke-width=".8"/>
  <circle cx="244" cy="61" r="2" fill="#185FA5" opacity=".7"/>
  <circle cx="251" cy="61" r="2" fill="#185FA5" opacity=".7"/>
  <circle cx="258" cy="61" r="2" fill="#185FA5" opacity=".7"/>
  <!-- form lines inside browser -->
  <rect x="242" y="70" width="44" height="4" rx="1" fill="#185FA5" opacity=".3"/>
  <rect x="242" y="77" width="30" height="4" rx="1" fill="#185FA5" opacity=".2"/>
  <rect x="242" y="84" width="20" height="6" rx="2" fill="#185FA5" opacity=".4"/>
  <text class="box-title" x="370" y="76" text-anchor="middle" fill="#0C447C">User browser</text>
  <text class="box-sub" x="370" y="96" text-anchor="middle" fill="#185FA5">HTML form  ·  POST /submit.php</text>
</g>

<!-- pulse dot at bottom of browser -->
<circle cx="340" cy="116" r="5" fill="#378ADD" opacity=".9">
  <animate attributeName="r" values="4;7;4" dur="1.8s" repeatCount="indefinite" begin="1.6s"/>
  <animate attributeName="opacity" values="1;.4;1" dur="1.8s" repeatCount="indefinite" begin="1.6s"/>
</circle>

<!-- arrow 1 -->
<line x1="340" y1="120" x2="340" y2="155" stroke="#378ADD" stroke-width="1.8" class="pipe1" marker-end="url(#arr)"/>
<text class="arrow-label" x="348" y="140">POST request</text>

<!-- ── ROW 2: EC2 ── -->
<g class="node2">
  <rect x="62" y="160" width="176" height="80" rx="10" fill="#9FE1CB" stroke="#1D9E75" stroke-width="1.2"/>
  <!-- PHP swirl icon -->
  <ellipse cx="96" cy="196" rx="20" ry="12" fill="none" stroke="#085041" stroke-width="1.2"/>
  <text style="font-size:11px;font-weight:600;font-family:var(--font-sans)" x="96" y="200" text-anchor="middle" fill="#085041">PHP</text>
  <text class="box-title" x="178" y="192" text-anchor="middle" fill="#085041">submit.php</text>
  <text class="box-sub" x="178" y="210" text-anchor="middle" fill="#0F6E56">Validates + inserts</text>
</g>

<g class="node3">
  <rect x="252" y="160" width="176" height="80" rx="10" fill="#FAC775" stroke="#BA7517" stroke-width="1.2"/>
  <!-- DB icon -->
  <ellipse cx="284" cy="184" rx="16" ry="7" fill="none" stroke="#633806" stroke-width="1"/>
  <line x1="268" y1="184" x2="268" y2="200" stroke="#633806" stroke-width="1"/>
  <line x1="300" y1="184" x2="300" y2="200" stroke="#633806" stroke-width="1"/>
  <ellipse cx="284" cy="200" rx="16" ry="7" fill="none" stroke="#633806" stroke-width="1"/>
  <text class="box-title" x="358" y="192" text-anchor="middle" fill="#633806">MariaDB</text>
  <text class="box-sub" x="358" y="210" text-anchor="middle" fill="#854F0B">user_app.users</text>
</g>

<g class="node4">
  <rect x="442" y="160" width="176" height="80" rx="10" fill="#D3D1C7" stroke="#5F5E5A" stroke-width="1.2"/>
  <!-- stack icon -->
  <rect x="460" y="174" width="36" height="7" rx="2" fill="none" stroke="#444441" stroke-width="1"/>
  <rect x="460" y="184" width="36" height="7" rx="2" fill="none" stroke="#444441" stroke-width="1"/>
  <rect x="460" y="194" width="36" height="7" rx="2" fill="none" stroke="#444441" stroke-width="1"/>
  <text class="box-title" x="548" y="192" text-anchor="middle" fill="#2C2C2A">LAMP stack</text>
  <text class="box-sub" x="548" y="210" text-anchor="middle" fill="#444441">Apache · PHP · Python3</text>
</g>

<!-- PHP → MariaDB arrow -->
<line x1="238" y1="200" x2="250" y2="200" stroke="#1D9E75" stroke-width="1.5" marker-end="url(#arr)"/>
<!-- MariaDB → Stack arrow (informational) -->
<line x1="428" y1="200" x2="440" y2="200" stroke="#888780" stroke-width="1" stroke-dasharray="3 2" marker-end="url(#arr)"/>

<!-- pulse dot -->
<circle cx="340" cy="268" r="5" fill="#BA7517" opacity=".9">
  <animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite" begin="2s"/>
  <animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite" begin="2s"/>
</circle>

<!-- arrow 2 -->
<line x1="340" y1="272" x2="340" y2="308" stroke="#BA7517" stroke-width="1.8" class="pipe2" marker-end="url(#arr)"/>
<text class="arrow-label" x="348" y="292">pymysql + boto3</text>

<!-- ── ROW 3: AWS ── -->
<g class="node5">
  <rect x="62" y="316" width="176" height="88" rx="10" fill="#FAC775" stroke="#BA7517" stroke-width="1.2"/>
  <!-- shield -->
  <path d="M92 330 L92 346 Q92 353 100 357 Q108 353 108 346 L108 330 Z" fill="none" stroke="#633806" stroke-width="1.2"/>
  <line x1="100" y1="338" x2="100" y2="348" stroke="#633806" stroke-width=".8"/>
  <text class="box-title" x="162" y="343" text-anchor="middle" fill="#633806">AWS IAM</text>
  <text class="box-sub" x="162" y="361" text-anchor="middle" fill="#854F0B">Access keys</text>
  <text class="box-sub" x="162" y="376" text-anchor="middle" fill="#854F0B">DynamoDB perms</text>
</g>

<g class="node6">
  <rect x="252" y="316" width="176" height="88" rx="10" fill="#FAC775" stroke="#BA7517" stroke-width="1.5"/>
  <!-- DynamoDB stacked ovals -->
  <ellipse cx="284" cy="342" rx="18" ry="8" fill="none" stroke="#633806" stroke-width="1.1"/>
  <line x1="266" y1="342" x2="266" y2="360" stroke="#633806" stroke-width="1.1"/>
  <line x1="302" y1="342" x2="302" y2="360" stroke="#633806" stroke-width="1.1"/>
  <ellipse cx="284" cy="360" rx="18" ry="8" fill="none" stroke="#633806" stroke-width="1.1"/>
  <ellipse cx="284" cy="351" rx="18" ry="8" fill="none" stroke="#633806" stroke-width=".6" opacity=".4"/>
  <text class="box-title" x="360" y="343" text-anchor="middle" fill="#633806">DynamoDB</text>
  <text class="box-sub" x="360" y="361" text-anchor="middle" fill="#854F0B">Table: users</text>
  <text class="box-sub" x="360" y="376" text-anchor="middle" fill="#854F0B">Partition key: user_id</text>
  <!-- shimmer -->
  <rect x="252" y="316" width="176" height="88" rx="10" fill="#EF9F27" opacity="0">
    <animate attributeName="opacity" values="0;.12;0" dur="3s" repeatCount="indefinite" begin="2s"/>
  </rect>
</g>

<g class="node7">
  <rect x="442" y="316" width="176" height="88" rx="10" fill="#D3D1C7" stroke="#5F5E5A" stroke-width="1.2"/>
  <!-- terminal -->
  <rect x="460" y="330" width="36" height="26" rx="3" fill="none" stroke="#444441" stroke-width="1"/>
  <text style="font-size:9px;font-family:monospace" x="463" y="344" fill="#2C2C2A">$ aws</text>
  <text style="font-size:9px;font-family:monospace" x="463" y="354" fill="#2C2C2A">config</text>
  <text class="box-title" x="548" y="343" text-anchor="middle" fill="#2C2C2A">AWS CLI</text>
  <text class="box-sub" x="548" y="361" text-anchor="middle" fill="#444441">Region eu-north-1</text>
  <text class="box-sub" x="548" y="376" text-anchor="middle" fill="#444441">boto3 SDK</text>
</g>

<!-- IAM → Dynamo arrow -->
<line x1="238" y1="360" x2="250" y2="360" stroke="#BA7517" stroke-width="1.2" marker-end="url(#arr)"/>

<!-- pulse dot -->
<circle cx="340" cy="420" r="5" fill="#7F77DD" opacity=".9">
  <animate attributeName="r" values="4;7;4" dur="1.6s" repeatCount="indefinite" begin="2.4s"/>
  <animate attributeName="opacity" values="1;.4;1" dur="1.6s" repeatCount="indefinite" begin="2.4s"/>
</circle>

<!-- arrow 3 -->
<line x1="340" y1="424" x2="340" y2="460" stroke="#7F77DD" stroke-width="1.8" class="pipe3" marker-end="url(#arr)"/>
<text class="arrow-label" x="348" y="444">azure-cosmos SDK</text>

<!-- ── ROW 4: AZURE ── -->
<!-- Cosmos DB -->
<rect x="62" y="468" width="200" height="88" rx="10" fill="#AFA9EC" stroke="#534AB7" stroke-width="1.5"/>
<!-- atom rings -->
<circle cx="100" cy="510" r="18" fill="none" stroke="#3C3489" stroke-width="1.2">
  <animateTransform attributeName="transform" type="rotate" from="0 100 510" to="360 100 510" dur="6s" repeatCount="indefinite"/>
</circle>
<ellipse cx="100" cy="510" rx="18" ry="8" fill="none" stroke="#3C3489" stroke-width="1" opacity=".6">
  <animateTransform attributeName="transform" type="rotate" from="30 100 510" to="390 100 510" dur="4s" repeatCount="indefinite"/>
</ellipse>
<circle cx="100" cy="510" r="4" fill="#534AB7"/>
<text class="box-title" x="182" y="498" text-anchor="middle" fill="#26215C">Cosmos DB</text>
<text class="box-sub" x="182" y="516" text-anchor="middle" fill="#3C3489">Core SQL API · serverless</text>
<text class="box-sub" x="182" y="531" text-anchor="middle" fill="#3C3489">user_db / users</text>
<rect x="62" y="468" width="200" height="88" rx="10" fill="#7F77DD" opacity="0">
  <animate attributeName="opacity" values="0;.1;0" dur="2.5s" repeatCount="indefinite" begin="2.4s"/>
</rect>

<!-- Python script -->
<rect x="278" y="468" width="200" height="88" rx="10" fill="#AFA9EC" stroke="#534AB7" stroke-width="1.2"/>
<path d="M314 488 Q314 480 322 480 L330 480 Q338 480 338 488 L338 496 Q338 504 330 504 L322 504 Q314 504 314 496 Z" fill="none" stroke="#3C3489" stroke-width="1"/>
<path d="M338 494 Q338 502 346 502 L354 502 Q362 502 362 494 L362 486 Q362 478 354 478 L346 478 Q338 478 338 486 Z" fill="none" stroke="#3C3489" stroke-width="1"/>
<line x1="330" y1="504" x2="346" y2="504" stroke="#3C3489" stroke-width="1"/>
<text class="box-title" x="386" y="498" text-anchor="middle" fill="#26215C">Python script</text>
<text class="box-sub" x="386" y="516" text-anchor="middle" fill="#3C3489">Pagination + upsert</text>
<text class="box-sub" x="386" y="531" text-anchor="middle" fill="#3C3489">Decimal conversion</text>

<!-- Env vars -->
<rect x="494" y="468" width="152" height="88" rx="10" fill="#9FE1CB" stroke="#1D9E75" stroke-width="1.2"/>
<rect x="516" y="488" width="24" height="20" rx="3" fill="none" stroke="#085041" stroke-width="1.2"/>
<path d="M520 488 L520 483 Q520 476 528 476 Q536 476 536 483 L536 488" fill="none" stroke="#085041" stroke-width="1.2"/>
<circle cx="528" cy="498" r="2.5" fill="#085041"/>
<text class="box-title" x="562" y="498" text-anchor="middle" fill="#085041">Env vars</text>
<text class="box-sub" x="562" y="516" text-anchor="middle" fill="#0F6E56">No hardcoded</text>
<text class="box-sub" x="562" y="531" text-anchor="middle" fill="#0F6E56">secrets</text>

<!-- script → cosmos -->
<line x1="278" y1="510" x2="264" y2="510" stroke="#7F77DD" stroke-width="1.5" marker-end="url(#arr)"/>
<!-- env → script -->
<line x1="494" y1="510" x2="480" y2="510" stroke="#1D9E75" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#arr)"/>

<!-- ── LEGEND ── -->
<rect x="60" y="578" width="8" height="8" rx="1" fill="#378ADD"/>
<text class="arrow-label" x="74" y="586">Blue = user/web tier</text>
<rect x="168" y="578" width="8" height="8" rx="1" fill="#1D9E75"/>
<text class="arrow-label" x="182" y="586">Teal = app / EC2</text>
<rect x="268" y="578" width="8" height="8" rx="1" fill="#BA7517"/>
<text class="arrow-label" x="282" y="586">Amber = AWS</text>
<rect x="356" y="578" width="8" height="8" rx="1" fill="#534AB7"/>
<text class="arrow-label" x="370" y="586">Purple = Azure</text>
<line x1="450" y1="582" x2="470" y2="582" stroke="#888780" stroke-width="1" stroke-dasharray="3 2"/>
<text class="arrow-label" x="476" y="586">Config / creds</text>

</svg>

## Architecture Overview

```
                    +------------------+
                    |   User Browser   |
                    +--------+---------+
                             |
                    HTML Form (index.html)
                             |
                    +--------v---------+
                    |   PHP Backend    |
                    |   submit.php     |
                    +--------+---------+
                             |
                    +--------v---------+
                    |    MariaDB       |
                    |  (AWS EC2)       |
                    |  DB: user_app    |
                    |  Table: users    |
                    +--------+---------+
                             |
                   Python Script (migrate_to_dynamo.py)
                   pymysql + boto3
                             |
                    +--------v---------+
                    |  AWS DynamoDB    |
                    |  Region:         |
                    |  eu-north-1      |
                    |  Table: users    |
                    +--------+---------+
                             |
                   Python Script (migrate_to_cosmos.py)
                   boto3 + azure-cosmos
                             |
                    +--------v---------+
                    |  Azure Cosmos DB |
                    |  API: Core SQL   |
                    |  DB: user_db     |
                    |  Container: users|
                    +------------------+
```

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
