<?php 
include 'ChromePhp.php';

    $jsonTemplate = "{
        \"id\": \"label\",
        \"time\": {
            \"hours\": 0,
            \"minutes\": 0
        },
        \"days\": [
            {
                \"Mon\": false
            },
            {
                \"Tue\": false
            },
            {
                \"Wed\": false
            },
            {
                \"Thu\": false
            },
            {
                \"Fri\": false
            },
            {
                \"Sat\": false
            },
            {
                \"Sun\": false
            }
        ],
        \"enabled\": false
    }";

    $jsonTemplate = json_decode($jsonTemplate);

    if(isset($_POST['alarmFrmSubmit']) && !empty($_POST['label'])) {
        $label = $_POST['label'];
        $days = explode(",", $_POST['days']);
        $clock = explode(':', $_POST['clock']);

        $jsonTemplate->id = $label;
        $jsonTemplate->enabled = true;
        $jsonTemplate->time->hours = (int) $clock[0];
        $jsonTemplate->time->minutes = (int) $clock[1];

        foreach ($jsonTemplate->days as $key => $val) {
            $first = get_object_vars($val);
            $day = array_keys($first)[0];
            if (in_array($day, $days)) {
                $val->$day = true;
            } else {
                $val->$day = false;
            }
        }

        ChromePhp::log($jsonTemplate);

        $inp = file_get_contents('alarms.json');
        if ($inp == "null") {
            file_put_contents('alarms.json', $jsonTemplate);
        } else {
            $tempArray = json_decode($inp);
            array_push($tempArray, $jsonTemplate);
            $jsonData = json_encode($tempArray, JSON_PRETTY_PRINT);
            file_put_contents('alarms.json', $jsonData);
        }
        

        $status = 'ok';
    } else {
        $status = 'err';
    }

    echo $status;die;

?>

