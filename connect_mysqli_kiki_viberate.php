<?php

	/*

		Connection string for Kiki mySQL server
		Author: Boštjan Žakelj
		Last update: 17.6.2016
		(c) Viberate 2016

	*/

	error_reporting(E_ALL & ~E_NOTICE);

	$mysql_streznik = "192.168.1.50";
	$mysql_username = "root";
	$mysql_password = "vIbE2ol6";

	$mysql_baza = "viberate";
	
	// Create connection

	$conn_kiki_viberate = new mysqli($mysql_streznik, $mysql_username, $mysql_password, $mysql_baza);

	// Check connection

	if ($conn_kiki_viberate->connect_error) {
		die("Connection failed: " . $conn_kiki_viberate->connect_error);
	}

	$result = mysqli_query($conn_kiki_viberate, "SET NAMES 'utf8'");

?>