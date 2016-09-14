<?php

include_once("config.php");

function checkPass(){
	global $SECRET_PASS;
	if(!isset($_GET["pass"])) {
        	die("DYNDPUMI pass fail ".$v);
	}
	if($_GET["pass"]!=$SECRET_PASS){
        	die("MDNFEKEC pass error");
	}
}
