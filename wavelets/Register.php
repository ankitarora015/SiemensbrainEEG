<html>
	<head>
		<title> My first PHP website </title>
	</head>
	<body>
	<h2> Registration Page</h2>
	<a href="index.php"> Click here to go back </a><br/><br/>
	<form action="Register.php" method="POST">
		Name           : <input type="text" name="name" required="required" /> <br/>
		Enter email    : <input type="text" name="email" required="required" /> <br/>
		Enter Username : <input type="text" name="username" required="required" /> <br/>
		Enter Password : <input type="password" name="password" required="required" /> <br/>
		<input type="submit" value="Register"/>
	</form>
	</body>
<html>	

<?php
	if($_SERVER["REQUEST_METHOD"]=="POST"){
		$username= mysql_real_escape_string($_POST['username']);
		$password= mysql_real_escape_string($_POST['password']);
		$name= mysql_real_escape_string($_POST['name']);
		$email= mysql_real_escape_string($_POST['email']);
		$bool = true;
	
		mysql_connect("localhost","root","") or die(mysql_erroe());
		mysql_select_db("first_db") or die("Cannot connect to database");
		$query = mysql_query("Select * from users");
		while($row = mysql_fetch_array($query)){
			$table_users=$row['username'];
			if($username == $table_users){
				$bool = false;
				Print '<script>alert("Username has been taken");</script>';
				Print '<script>window.location.assign("Register.php");</script>';
			}
		}
		if($bool){
			mysql_query("INSERT INTO users(Name,email,username,password) VALUES('$name','$email','$username','$password')");
			Print '<script>alert("Successfully Registered!!")</script>';
			Print '<script>window.location.assign("Register.php")</script>';
		}
	}
?>