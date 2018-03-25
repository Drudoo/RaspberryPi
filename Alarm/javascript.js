var alarmJSON={};

function readJSON(_callback) {
	$.ajax({
		url: 'readJSON.php',
		success: function(data){
			alarmJSON = JSON.parse(data);
			//console.log(alarmJSON);
			_callback();
		}
	});
	
}

function readOrigiJSON() {
	$.ajax({
		url: 'readOrigiJSON.php',
		success: function(data){
			alarmJSON = JSON.parse(data);
			console.log(alarmJSON);
		}
	});
}


function getAlarms() {
	var api = alarmJSON;
	var HTML = "<table class=\"table table-bordered\"><tr><th>Label</th><th>Time</th><th>Days</th>";

	HTML+="<th>Action</th></tr>";

	for(var i = 0; i < api.length; i++) {
		var obj = api[i];
		HTML+= "<tr><td>" + obj.id + "</td><td>" + obj.time.hours +":"+ obj.time.minutes+ "</td><td>";
		for (var j = 0; j < obj.days.length; j++) {
			for (var key in obj.days[j]) {
				if (obj.days[j][key]) {
					HTML+=key+" ";
				} else {
					HTML+="---"+" ";
				}
			}
		}
		HTML+="</td><td>";
		if (obj.enabled) {
			HTML+="<button type=\"button\" class=\"btn btn-success\" onclick=\"disable('" + obj.id.toString() + "')\">Enabled</button>";
		} else {
			HTML+="<button type=\"button\" class=\"btn btn-danger\" onclick=\"enable('" + obj.id.toString() + "')\">Disabled</button>";
		}
		HTML+="\n<button type=\"button\" class=\"btn btn-warning\" onclick=\"deleteAlarm('" + obj.id.toString() + "')\">Delete</button></td></tr>";

	}
	HTML+="</table>";
	document.getElementById("alarms").innerHTML = HTML;
}

function enable(id) {
	for (var key in alarmJSON) {
		if (alarmJSON[key].id==id) {
			alarmJSON[key].enabled = true;
			console.log(alarmJSON[key].id, " is now enabled");
		}
	}
	//refresh();
	writeJSON();
	getAlarms();
}

function disable(id) {
	for (var key in alarmJSON) {
		if (alarmJSON[key].id==id) {
			alarmJSON[key].enabled = false;
			console.log(alarmJSON[key].id, " is now disabled");
		}
	}
	//refresh();
	writeJSON();
	getAlarms();
}

function deleteAlarm(id) {

	tempJSON = alarmJSON;

	for (var key in tempJSON) {
		//console.log("checking ", tempJSON[key].id);
		if (tempJSON[key].id==id) {
			//console.log("should delete", id);
			tempJSON.splice(key, 1);
			break;
		}
	}
	alarmJSON = tempJSON;
	//console.log(alarmJSON);
	// //refresh();
	writeJSON();
	readJSON(function() {
		getAlarms();
	});
	getAlarms();
}

function writeJSON() {
	//var params = JSON.stringify(alarmJSON);
	var params = alarmJSON;
	$.post('writeJSON.php', {jsonData: params});
	// $.ajax({
	//     type: 'POST',
	//     url: 'writeJSON.php',
	//     data: params,
	//     success: function(data){
	//         console.log("Sucess: " + data + "--EOL--");
	//     },
	//     error: function(data){
	//         console.log("Error" + data);
	//     }
	// });
}


function refresh() {
	getAlarms();
}

function startup() {
	readJSON(function() {
        getAlarms();
    });
}


function saveAlarm() {
	var label = $('#inputLabel').val();
	var clock = $('#clock').val();

	console.log(clock);

	var days = [];
    $.each($("input[name='days']:checked"), function() {
      days.push($(this).val());
    });

	if (label.trim() == '') {
		alert('Please enter a label');
		$('#inputLabel').focus();
		return false;
	} else if (days.length < 1) {
		alert('Please select a day');
		return false;
	} else if (clock.trim() == '') {
		alert('Please select a time');
		$('#clock').focus();
		return false;
	} else {
		$.ajax({
			type: 'POST',
			url: 'saveAlarm.php',
			data:'alarmFrmSubmit=1&label='+label+'&days='+days+'&clock='+clock,
			beforeSend: function () {
                $('.submitBtn').attr("disabled","disabled");
                $('.modal-body').css('opacity', '.5');
            },
            success:function(msg){
                if(msg == 'ok'){
                    $('#inputLabel').val('');
                    $('#clock').val('');
                    $('.statusMsg').html('<span style="color:green;">Alarm Saved</p>');
                }else{
                    $('.statusMsg').html('<span style="color:red;">Some problem occurred, please try again.</span>');
                }
                $('.submitBtn').removeAttr("disabled");
                $('.modal-body').css('opacity', '');
            }
		});
	}
}
