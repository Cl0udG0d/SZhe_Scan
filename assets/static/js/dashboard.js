$('#chart1').easyPieChart({
        size:180,
        barColor:'#3ba0ff',
        lineWidth:5,
    });

    $('#chart2').easyPieChart({
        size:180,
        barColor:'#57BE85',
        lineWidth:5,
    });

    $('#chart3').easyPieChart({
        size:180,
        barColor:'#ff6c60',
        lineWidth:5,
    });
    $('#chart4').easyPieChart({
        size:180,
        barColor:'black',
        lineWidth:5,
    });

	window.chart = c3.generate({
 	bindto: '#spline-chart',
    data: {
        columns: [
            ['Speed', 210, 170, 145, 200, 220, 210],
            ['Time', 130, 100, 130, 180, 150, 50],
            ['Visitors', 80, 110, 70, 150, 110, 140],
        ],
        types: {
            Speed: 'area-spline',
            Time: 'spline',
            Visitors:'area-spline'
        }
    },
    color: {
        pattern: ['#57BE85','#ff6c60','#3ba0ff']
        },
        size: {
		height: 300
		},
    });

	//charts sidebar toggle resize
	$('#sidebar-collapse').on('click',function(){

		setTimeout(function() {
			window.chart.resize({height:300});
		},100);

	});

    var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));

	elems.forEach(function(html) {
	  var switchery = new Switchery(html);
	});

	// Switch Buttons :

	var blue = document.querySelector('.js-switch-blue');
	var switchery = new Switchery(blue, { color: '#3ba0ff' });

	var green = document.querySelector('.js-switch-green');
	var switchery = new Switchery(green, { color: '#57BE85' });

	var teal = document.querySelector('.js-switch-teal');
	var switchery = new Switchery(teal, { color: '#3cc8ad' });

	var sky = document.querySelector('.js-switch-sky');
	var switchery = new Switchery(sky, { color: '#54D1F1' });


	//Calendar
	$wrapper = $('#custom-inner'), $calendar = $('#calendar'), cal = $calendar.calendario({
	onDayClick: function($el, $contentEl, dateProperties) {
		if ($contentEl.length > 0) {
			showEvents($contentEl, dateProperties);
		}
	},
	displayWeekAbbr: true
	}), $month = $('#custom-month').html(cal.getMonthName()), $year = $('#custom-year').html(cal.getYear());

	$('#custom-next').on('click', function() {
		cal.gotoNextMonth(updateMonthYear);
	});

	$('#custom-prev').on('click', function() {
		cal.gotoPreviousMonth(updateMonthYear);
	});

	function updateMonthYear() {
		$month.html(cal.getMonthName());
		$year.html(cal.getYear());
	}