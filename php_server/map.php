<?php

include_once('common.php');

checkPass();

$MEMCACHED_KEY = "musashi_map";

$memcache = new Memcache;
$memcache->connect('localhost', 11211) or die ("VMUMVHEA memcache fail");
$data_json = $memcache->get($MEMCACHED_KEY);
$memcache->close();

if(!$data_json){
	exit("no data");
}

$data = json_decode($data_json,true);

$url = "https://maps.googleapis.com/maps/api/staticmap?size=640x640";
$url .= "&style=element:labels%7Cvisibility:off";
$url .= "&zoom=17";
$url .= "&center=".$data['center_latitude'].",".$data['center_longitude'];

$nearby_dict = $data['nearby_dict'];
foreach($nearby_dict as $k=>$nearby){
	$maker = "color:gray";
	$maker .= "|label:".$nearby['cell_label'];
	$maker .= "|".$nearby['latitude'].",".$nearby['longitude'];
	$url .= "&markers=".urlencode($maker);
}

$pokemon_dict = $data['pokemon_dict'];
foreach($pokemon_dict as $k=>$pokemon){
	if(!isset($pokemon['latitude']))continue;
	$maker = "color:yellow";
	$maker .= "|label:".$pokemon['maker_label'];
	$maker .= "|".$pokemon['latitude'].",".$pokemon['longitude'];
	$url .= "&markers=".urlencode($maker);
}

$drone_dict = $data['drone_dict'];
foreach($drone_dict as $k=>$drone){
	$maker = "color:blue";
	$maker .= "|size:tiny";
	$maker .= "|".$drone['latitude'].",".$drone['longitude'];
	$url .= "&markers=".urlencode($maker);
}

//// debug map border
//$tmp_path = 'color:blue|weight:5';
//$tmp_path .= '|'.$data['latitude_n'].",".$data['center_longitude'];
//$tmp_path .= '|'.$data['center_latitude'].",".$data['longitude_e'];
//$tmp_path .= '|'.$data['latitude_s'].",".$data['center_longitude'];
//$tmp_path .= '|'.$data['center_latitude'].",".$data['longitude_w'];
//$tmp_path .= '|'.$data['latitude_n'].",".$data['center_longitude'];
//$url .= "&path=".urlencode($tmp_path);

$url .= "&key=".$GOOGLE_MAP_API_KEY;

echo("<p>".htmlspecialchars($url)."</p>");
echo("<img src=\"".htmlspecialchars($url)."\"/>");

echo('<table border="1">');
foreach($pokemon_dict as $k=>$pokemon){
	if(!isset($pokemon['latitude']))continue;
	echo("<tr>");
	echo("<td>".$pokemon['maker_label']."</td>");
	echo('<td><img src="icon/'.sprintf("%03d",$pokemon['pokemon_id']).'.png"/></td>');
	echo("<td>".date("H:i:s",$pokemon['expiration_timestamp_ms']/1000)."</td>");
	echo("<td>".(floor($pokemon['expiration_timestamp_ms']/1000)-time())."</td>");
	echo("</tr>");
}
echo("</table>");

echo('<table border="1">');
foreach($nearby_dict as $k=>$nearby){
	echo("<tr>");
	echo("<td>".$nearby['cell_label']."</td>");
	echo("<td>");
	foreach($nearby['pokemon_list'] as $pokemon){
		echo('<img src="icon/'.sprintf("%03d",$pokemon['pokemon_id']).'.png"/>');
	}
	echo("</td>");
	echo("</tr>");
}
echo("</table>");
