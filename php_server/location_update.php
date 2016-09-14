<?php

include_once('common.php');

checkPass();

$MEMCACHED_KEY = "musashi_location";
$CHECK_PARAM = array("lat","lng","acc","time","provider");

foreach($CHECK_PARAM as $k=>$v){
	if(!isset($_GET[$v])) {
		die("CGFYGWNU arg fail ".$v);
	}
}

$argLat = $_GET["lat"];
$argLng = $_GET["lng"];
$argAcc = $_GET["acc"];
$argTime = $_GET["time"];
$argProvider = $_GET["provider"];

$data = array();
foreach($CHECK_PARAM as $k=>$v){
	$data[$v] = $_GET[$v];
}
$data_json = json_encode($data);

$memcache = new Memcache;
$memcache->connect('localhost', 11211) or die ("VMUMVHEA memcache fail");
$memcache->set($MEMCACHED_KEY, $data_json, false, 60) or die ("Failed to save data at the server");
$memcache->close();

echo "OK";
