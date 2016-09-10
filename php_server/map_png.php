<?php

include_once('config.php');

$MEMCACHED_KEY = "musashi_map";
$WIDTH = 640;
$HEIGHT = 640;
$ICON_WIDTH = 32;
$ICON_HEIGHT = 32;
$POKEBALL_ICON_WIDTH = 8;
$POKEBALL_ICON_HEIGHT = 8;
$DRONE_ICON_LIFE_MS = 30000;
$SPAWN_POINT_RADIUS = 1.5;

$arg_show_spawn_point = isset($_GET['show_spawn_point']);

$memcache = new Memcache;
$memcache->connect('localhost', 11211) or die ("VMUMVHEA memcache fail");
$data_json = $memcache->get($MEMCACHED_KEY);
$memcache->close();

if(!$data_json){
	exit("no data");
}

$data = json_decode($data_json,true);

function latlng_to_xy($lag,$lng){
	global $HEIGHT,$WIDTH,$data;
	$y = $HEIGHT*($lag-$data['latitude_n'])/($data['latitude_s']-$data['latitude_n']);
	$x = $WIDTH*($lng-$data['longitude_w'])/($data['longitude_e']-$data['longitude_w']);
	//return array(100,100);
	return array($x,$y);
}


$url = "https://maps.googleapis.com/maps/api/staticmap?size=640x640";
$url .= "&style=element:labels%7Cvisibility:off";
$url .= "&zoom=17";
$url .= "&center=".$data['center_latitude'].",".$data['center_longitude'];

//$nearby_dict = $data['nearby_dict'];
//foreach($nearby_dict as $k=>$nearby){
//	$maker = "color:gray";
//	$maker .= "|label:".$nearby['cell_label'];
//	$maker .= "|".$nearby['latitude'].",".$nearby['longitude'];
//	$url .= "&markers=".urlencode($maker);
//}
//
//$pokemon_dict = $data['pokemon_dict'];
//foreach($pokemon_dict as $k=>$pokemon){
//	if(!isset($pokemon['latitude']))continue;
//	$maker = "color:yellow";
//	$maker .= "|label:".$pokemon['maker_label'];
//	$maker .= "|".$pokemon['latitude'].",".$pokemon['longitude'];
//	$url .= "&markers=".urlencode($maker);
//}
//
//$drone_dict = $data['drone_dict'];
//foreach($drone_dict as $k=>$drone){
//	$maker = "color:blue";
//	$maker .= "|size:tiny";
//	$maker .= "|".$drone['latitude'].",".$drone['longitude'];
//	$url .= "&markers=".urlencode($maker);
//}

//// debug map border
//$tmp_path = 'color:blue|weight:5';
//$tmp_path .= '|'.$data['latitude_n'].",".$data['center_longitude'];
//$tmp_path .= '|'.$data['center_latitude'].",".$data['longitude_e'];
//$tmp_path .= '|'.$data['latitude_s'].",".$data['center_longitude'];
//$tmp_path .= '|'.$data['center_latitude'].",".$data['longitude_w'];
//$tmp_path .= '|'.$data['latitude_n'].",".$data['center_longitude'];
//$url .= "&path=".urlencode($tmp_path);

$url .= "&key=".$GOOGLE_MAP_API_KEY;

$im = new Imagick($url);

// draw drone
$pokeball_im = new Imagick('icon/pokeball.png');
$drone_dict = $data['drone_dict'];
foreach($drone_dict as $k=>$drone){
	if(($drone['last_update_time_ms']+$DRONE_ICON_LIFE_MS)/1000<time())continue;
	$xy = latlng_to_xy($drone['latitude'],$drone['longitude']);
	$im->compositeImage($pokeball_im, imagick::COMPOSITE_OVER, $xy[0]-$POKEBALL_ICON_WIDTH/2, $xy[1]-$POKEBALL_ICON_HEIGHT/2);
}

// draw nearby pokemon
$draw0 = new ImagickDraw();
$draw0->setFontSize(48);
$draw0->setFillColor('#ccc');
$draw0->setStrokeColor('#ccc');
$draw0->setStrokeWidth(10);
$draw0->setGravity(Imagick::GRAVITY_CENTER);

$draw1 = new ImagickDraw();
$draw1->setFontSize(48);
$draw1->setFillColor('white');
$draw1->setStrokeColor('transparent');
$draw1->setGravity(Imagick::GRAVITY_CENTER);

$nearby_pokemon_im = array();
$nearby_dict = $data['nearby_dict'];
foreach($nearby_dict as $k=>$nearby){foreach($nearby['pokemon_list'] as $pokemon){
	$pokemon_id=$pokemon['pokemon_id'];
	if(isset($nearby_pokemon_im[$pokemon_id]))continue;
	$nearby_pokemon_im[$pokemon_id] = new Imagick(sprintf('icon/%03d.png',$pokemon_id));
	$nearby_pokemon_im[$pokemon_id]->evaluateImage(Imagick::EVALUATE_MULTIPLY, 0.618, Imagick::CHANNEL_ALPHA);
}}
foreach($nearby_dict as $k=>$nearby){
	$pokemon_list = array();
	foreach($nearby['pokemon_list'] as $pokemon){
		if($pokemon['discover_expiration_timestamp_ms']/1000<time())continue;
		$pokemon_list[] = $pokemon;
	}
        if(count($pokemon_list)<=0)continue;
	$label = strtoupper(substr(md5($k),28));
	$xy = latlng_to_xy($nearby['latitude'],$nearby['longitude']);
	$im->annotateImage($draw0, $xy[0]-($WIDTH/2), $xy[1]-($HEIGHT/2), 0, $label);
	$im->annotateImage($draw1, $xy[0]-($WIDTH/2), $xy[1]-($HEIGHT/2), 0, $label);
	$x0=$xy[0]-(count($pokemon_list)*$ICON_WIDTH/2);
	$y0=$xy[1]-($ICON_HEIGHT/2);
	foreach($pokemon_list as $pokemon){
		$pokemon_id=$pokemon['pokemon_id'];
		$im->compositeImage($nearby_pokemon_im[$pokemon_id], imagick::COMPOSITE_OVER, $x0, $y0);
		$x0+=$ICON_WIDTH;
	}
}

// $arg_show_spawn_point
if($arg_show_spawn_point){
	$draw = new \ImagickDraw();
	$draw->setStrokeColor('grey');
	$draw->setFillColor('yellow');
	$draw->setStrokeOpacity(1);
	$draw->setStrokeWidth(1);
	
	//$draw->circle(100, 100, 103, 103);

	foreach($data['spawn_point_dict'] as $k=>$spawn_point){
		if((floor($spawn_point['discover_expiration_timestamp_ms']/1000)-time())<0)continue;
		$xy = latlng_to_xy($spawn_point['latitude'],$spawn_point['longitude']);
		$draw->circle($xy[0], $xy[1], $xy[0]+$SPAWN_POINT_RADIUS, $xy[1]+$SPAWN_POINT_RADIUS);
	}
	
	$im->drawImage($draw);
	
	$draw = NULL;
}

// draw pokemon

$draw0 = new ImagickDraw();
$draw0->setFontSize(10);
$draw0->setFillColor('white');
$draw0->setStrokeColor('white');
$draw0->setStrokeWidth(2);

$draw1 = new ImagickDraw();
$draw1->setFontSize(10);
$draw1->setFillColor('black');
$draw1->setStrokeColor('transparent');

$pokemon_im = array();
$pokemon_dict = $data['pokemon_dict'];
foreach($pokemon_dict as $k=>$pokemon){
	if(!isset($pokemon['latitude']))continue;
	if((floor($pokemon['expiration_timestamp_ms']/1000)-time())<0)continue;
	$pokemon_id=$pokemon['pokemon_id'];
	if(isset($pokemon_im[$pokemon_id]))continue;
	$pokemon_im[$pokemon_id] = new Imagick(sprintf('icon/%03d.png',$pokemon_id));
}
foreach($pokemon_dict as $k=>$pokemon){
	if(!isset($pokemon['latitude']))continue;
	if((floor($pokemon['expiration_timestamp_ms']/1000)-time())<0)continue;
	$pokemon_id=$pokemon['pokemon_id'];
	$xy = latlng_to_xy($pokemon['latitude'],$pokemon['longitude']);
	$im->compositeImage($pokemon_im[$pokemon_id], imagick::COMPOSITE_OVER, $xy[0]-$ICON_WIDTH/2, $xy[1]-$ICON_HEIGHT/2);
}
foreach($pokemon_dict as $k=>$pokemon){
	if(!isset($pokemon['latitude']))continue;
	if((floor($pokemon['expiration_timestamp_ms']/1000)-time())<0)continue;
	$xy = latlng_to_xy($pokemon['latitude'],$pokemon['longitude']);
	$expiration_time = date('i:s',$pokemon['expiration_timestamp_ms']/1000);
	$im->annotateImage($draw0, $xy[0]-$ICON_WIDTH/2, $xy[1]-$ICON_HEIGHT/2, 0, $expiration_time);
	$im->annotateImage($draw1, $xy[0]-$ICON_WIDTH/2, $xy[1]-$ICON_HEIGHT/2, 0, $expiration_time);
}

$im->setImageFormat("jpg");
header("Content-Type: image/jpg");
echo($im);
