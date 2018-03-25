<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="Access-Control-Allow-Origin" content="*"/>



    <script data-require="jquery@1.10.1" data-semver="1.10.1" src="http://code.jquery.com/jquery-1.10.1.min.js"></script>


<link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,300,300italic,200,600,700,900' rel='stylesheet' type='text/css'> 

 <!-- Latest minified bootstrap css -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

<!-- jQuery library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>

<!-- Latest minified bootstrap js -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script type='text/javascript' src='http://code.jquery.com/jquery-1.11.0.js'></script>

    <link rel="stylesheet" type="text/css" href="index.css">
    <link rel="stylesheet" type="text/css" href="pace.css">

<link rel="stylesheet" type="text/css" href="bootstrap-clockpicker.min.css">
<link rel="stylesheet" type="text/css" href="jquery-clockpicker.min.css">
<script type="text/javascript" src="jquery-clockpicker.min.js"></script>
<script type="text/javascript" src="bootstrap-clockpicker.min.js"></script>




    <script data-require="application/javascript" src="javascript.js"></script>
    <h1>Pi Alarm</h1>
</head>

<body onload="startup()">
	
	<div id="alarms"></div>
	<button type="button" class="btn btn-default" onclick="refresh()">Refresh data</button>
	<button type="button" class="btn btn-default" type="button" class="btn btn-default" onclick="readJSON(function(){getAlarms();});">READ</button>
	<button type="button" class="btn btn-default" onclick="writeJSON()">WRITE</button>
	<p></p><p></p><p></p><p></p>
	<button type="button" class="btn btn-default" onclick="readOrigiJSON()">READ Original</button>

	<!-- Button to trigger modal -->
<button type="button" class="btn btn-default" data-toggle="modal" data-target="#modalForm">
    Add Alarm
</button>

<!-- Modal -->
<div class="modal fade" id="modalForm" role="dialog">
    <div class="modal-dialog">
        <div class="modal-content">
            <!-- Modal Header -->
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">
                    <span aria-hidden="true">&times;</span>
                    <span class="sr-only">Close</span>
                </button>
                <h4 class="modal-title" id="myModalLabel">Contact Form</h4>
            </div>
            
            <!-- Modal Body -->
            <div class="modal-body">
                <p class="statusMsg"></p>
                <form role="form">
                    <div class="form-group">
                        <label for="labelName" style="color: black">Label</label>
                        <input type="text" class="form-control" id="inputLabel" placeholder="Enter your alarm Label"/>
                    </div>

                    <div class="form-group">
                    	<label for="inputDays" style="color: black">Select which days the alarm should go off</label><p></p>
                        <label style="color: black; font-weight: normal"><input type="checkbox" value="Mon" name="days">Mon</label>
                        <label style="color: black; font-weight: normal"><input type="checkbox" value="Tue" name="days">Tue</label>
                        <label style="color: black; font-weight: normal"><input type="checkbox" value="Wed" name="days">Wed</label>
                        <label style="color: black; font-weight: normal"><input type="checkbox" value="Thu" name="days">Thu</label>
                        <label style="color: black; font-weight: normal"><input type="checkbox" value="Fri" name="days">Fri</label>
                        <label style="color: black; font-weight: normal"><input type="checkbox" value="Sat" name="days">Sat</label>
                        <label style="color: black; font-weight: normal"><input type="checkbox" value="Sun" name="days">Sun</label>
                    </div>
                    <div class="input-group clockpicker">
					    <input type="text" class="form-control" id="clock">
					    <span class="input-group-addon">
					        <span class="glyphicon glyphicon-time"></span>
					    </span>
					</div>
					<script type="text/javascript">
                        // var input = $('#clock');
                        // input.clockpicker({
                        //     autoclose: true,
                        //     align: 'left',
                        //     donetext: 'Done'
                        // });
                        $('.clockpicker').clockpicker({
                            align: 'left',
                            autoclose: true
                        });
                    </script>
                </form>
            </div>
            
            <!-- Modal Footer -->
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary submitBtn" onclick="saveAlarm()">SUBMIT</button>
            </div>
        </div>
    </div>
</div>

</body>