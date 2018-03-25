<?php

//echo $_POST['jsonData'];
include 'ChromePhp.php';
$json = json_encode($_POST['jsonData']);

//$json = json_decode($argv[1]);

//$json = json_decode('[{"id":"TESTmorning","time":{"hours":"6","minutes":"30"},"days":[{"Mon":"false"},{"Tue":"false"},{"Wed":"false"},{"Thu":"true"},{"Fri":"false"},{"Sat":"true"},{"Sun":"true"}],"enabled":"true"},{"id":"TESTevening","time":{"hours":"15","minutes":"30"},"days":[{"Mon":"true"},{"Tue":"false"},{"Wed":"true"},{"Thu":"true"},{"Fri":"false"},{"Sat":"false"},{"Sun":"true"}],"enabled":"true"}]');

$jjson = json_decode($json);

foreach ($jjson as $data) {

    $data->time->hours = (int) $data->time->hours;
    $data->time->minutes = (int) $data->time->minutes;
    
    if ($data->enabled == "true") {
      $data->enabled = true;
    } else {
      $data->enabled = false;
    }

    // $data->enabled = (bool) $data->enabled;

    foreach($data->days as $key => $val) {
      $first = get_object_vars($val);
    //$first = (bool) $first;
      //ChromePhp::log(array_keys($first)[0]);
      $day = array_keys($first)[0];
   //   ChromePhp::log("First", $val->$day);
   //   $data->days->day = (bool) $val->$day;
    // ChromePhp::log("Second",$val->$day);



    if ($val->$day == "true") {
      $val->$day = true;
    } else {
      $val->$day = false;
    }



  }

  //   foreach ($data->days as $week) {
  //    ChromePhp::log($week->Mon);




    // // $week->Mon = (bool) $week->Mon;
    // // $week->Tue = (bool) $week->Tue;
    // // $week->Wed = (bool) $week->Wed;
    // // $week->Thu = (bool) $week->Thu;
    // // $week->Fri = (bool) $week->Fri;
    // // $week->Sat = (bool) $week->Sat;
    // // $week->Sun = (bool) $week->Sun;
  //   }

}

$filename = '/var/www/html/Alarm/alarms.json';
if (file_exists($filename)) {
  ChromePhp::log('Exists');
  if (is_writable($filename)) {
    ChromePhp::log('Writable');
      file_put_contents($filename, json_encode($jjson,JSON_PRETTY_PRINT));
  } else {
      ChromePhp::log('The file is not writable');
  }
} else {
  ChromePhp::log('Does not exist');
}


?>