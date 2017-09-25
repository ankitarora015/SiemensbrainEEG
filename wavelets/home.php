<?php
   include("includes/fusioncharts.php");
?>
<html>
	<head>
		<title> My first PHP page </title>
		<script src="js/fusioncharts.js"></script>
	</head>
	<?php
		session_start();
		if(!($_SESSION['user'])){
			header("location:index.php");
		}
		$user= $_SESSION['user'];
	?>
	<body>
		<h2> WELCOME TO BRAIN WORLD</h2>
		<p> Hello <?php Print "$user" ?> !</p>
		<a href = "logout.php" align="bottom"> Click here to logout </a><br/>
		
		<h2 align = "center"> PREDICTION STATUS </h2>
		<table border="1px" width = "100%">
		<tr>
			<th> Id </th>
			<th> alpha </th>
			<th> beta </th>
			<th> delta </th>
			<th> gamma </th>
			<th> prediction </th>	
		</tr>
		<?php
			mysql_connect("localhost","root","") or die(mysql_error());
			mysql_select_db("first_db") or die("Cannot connect to database");
			$query = mysql_query("SELECT * FROM data WHERE id > (SELECT MAX(id) - 5 FROM data)");
			while($row = mysql_fetch_array($query)){
				Print "<tr>";
					Print '<td align = "center">'. $row['id'] ."</td>";
					Print '<td align = "center">'. $row['alpha']."</td>";
					Print '<td align = "center">'. $row['beta']."</td>";
					Print '<td align = "center">'. $row['delta']."</td>";
					Print '<td align = "center">'. $row['gamma'] ."</td>";
					Print '<td align = "center">'. $row['prediction'] ."</td>";
				Print "</tr>";
			}
		?>
		</table>
		<?php
			mysql_connect("localhost","root","") or die(mysql_error());
			mysql_select_db("first_db") or die("Cannot connect to database");
			$result = mysql_query("SELECT * FROM data WHERE id > (SELECT MAX(id) - 1 FROM data)");
			$row = mysql_fetch_array($result);
			$arrData = array(
				  "chart" => array("caption" => "Percentage Presence of waves")
			);
	
			 $arrData["data"] = array();

				// Push the data into the array
				array_push($arrData["data"], array(
					  "label" => "alpha",
					  "value" => $row["alpha"]
					  )
				  );
				array_push($arrData["data"], array(
					  "label" => "beta",
					  "value" => $row["beta"]
					  )
				  );
				  array_push($arrData["data"], array(
					  "label" => "delta",
					  "value" => $row["delta"]
					  )
				  );
				  array_push($arrData["data"], array(
					  "label" => "gamma",
					  "value" => $row["gamma"]
					  )
				  );
				$jsonEncodedData = json_encode($arrData);

				$columnChart = new FusionCharts("column2D", "myFirstChart" , 600, 300, "chart-1", "json", $jsonEncodedData);

				// Render the chart
				$columnChart->render();
			  

			?>
			<div id="chart-1" align="center"></div>
	</body>
</html>