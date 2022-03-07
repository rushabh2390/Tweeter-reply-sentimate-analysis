		
<html>
	<head>
		<title>Twitter Reply Analysis</title>
		<style type="text/css"> 
			input[type=text] {
			width: 80%;
			padding: 12px 20px;
			margin: 8px 0;
			box-sizing: border-box;
			border: none;
			border-bottom: 2px solid violet;
			font-family:Verdana,Sans-serif;
}
	.container {
    display: block;
    position: relative;
    padding-left: 35px;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 22px;
    /*-webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;*/
}

.lbl {
    display: block;
    position: relative;
    padding-left: 10px;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 22px;
}
/* Hide the browser's default radio button */
.container input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
}

/* Create a custom radio button */
.checkmark {
    position: absolute;
    top: 0;
    left: 0;
    height: 25px;
    width: 25px;
    background-color: #eee;
    border-radius: 50%;
}

/* On mouse-over, add a grey background color */
.container:hover input ~ .checkmark {
    background-color: #ccc;
}

/* When the radio button is checked, add a blue background */
.container input:checked ~ .checkmark {
    background-color: #2196F3;
}

/* Create the indicator (the dot/circle - hidden when not checked) */
.checkmark:after {
    content: "";
    position: absolute;
    display: none;
}

/* Show the indicator (dot/circle) when checked */
.container input:checked ~ .checkmark:after {
    display: block;
}

/* Style the indicator (dot/circle) */
.container .checkmark:after {
 	top: 9px;
	left: 9px;
	width: 8px;
	height: 8px;
	border-radius: 50%;
	background: white;
}

.button {
  background-color: #f4511e;
  border: none;
  color: white;
  padding: 16px 32px;
  text-align: center;
  font-size: 16px;
  margin: 4px 2px;
  opacity: 0.6;
  transition: 0.3s;
  display: inline-block;
  text-decoration: none;
  cursor: pointer;
}

.button:hover {opacity: 1}

.formdata {
    background-color: lightyellow;
    width: 90%;
    border: 5px solid #f4511e;
    padding-left: 25px;
	padding-top:5px;
    
	
}
h1{
	color:	#a0a;
	
}
.res{
	font-family:Verdana,Sans-serif;
	
}
.resdata
{
	background-color: lightyellow;
    width: 90%;
    border: 5px solid #f4511e;
    padding-left: 25px;
	padding-top:5px;
    
}
</style>
</head>
<body>	
	<div class="formdata">
		<h1 align="center">Twitter Reply Analysis</h1>
		<form method="post" action="" >
			<label class="lbl">Enter Your URL:</label><br/><input type="text" name="url"/><br/>
			<label class="lbl">Enter No of Reply:</label><br/><input type="text" name="no"/><br/>
			<label class="container">Character
				<input type="radio" checked="checked" name="radio" value="Character">
				<span class="checkmark"></span>
			</label>
			<label class="container">Product
				<input type="radio" name="radio" value="Product">
				<span class="checkmark"></span>
			</label>
			<label class="container">Custom
			  <input type="radio" name="radio" value="Custom">
			  <span class="checkmark"></span>
			</label>
			
			<button class="button">Submit</button>
		</form>
	</div>
	<div class="resdata">
	<label class="res">
	<?php

if(!empty($_POST))
{
	$pyscript = '"C:\\xampp\\htdocs\\phppython\\tweeterrepliesanalysis.py"';
	$python = 'C:\\Python\\Python37\\python.exe';
	if($_POST['url']!='')
	{
		$filname=$_POST['url'];
		if(isset($_POST['no']))
		{
				$no=$_POST['no'];
		}
		else 
		{
				$no=0;
		}
		$bt=$_POST['radio'];
		$output=shell_exec("$python $pyscript $filname $no $bt 2>&1");
		print_r($output);
		$arr = explode("/", $filname);
		$id= end($arr);
		echo "<img src='".$id.".png' alt='hello!!!'/>";
		// echo "<img src='wordwise_".$id.".png' alt='hello!!!'/>";
	}
	else
	{
		echo "error";
		
	}
	
	
	
}
?>
</label>
</div>
</body>
</html>