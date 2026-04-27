<?php
$host = "localhost";
$user = "root";
$pass = "shiva";   // change if needed
$db   = "user_app";

// Connect to DB
$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get form data
$name  = $_POST['name'];
$phone = $_POST['phone'];
$age   = $_POST['age'];

// Insert query
$sql = "INSERT INTO users (name, phone, age) VALUES (?, ?, ?)";

$stmt = $conn->prepare($sql);
$stmt->bind_param("ssi", $name, $phone, $age);

if ($stmt->execute()) {
    echo "✅ Data stored successfully!";
} else {
    echo "❌ Error: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
