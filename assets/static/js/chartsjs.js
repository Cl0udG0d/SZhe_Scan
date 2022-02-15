/*
	Main function for responsiveness modified by Abhishek gahlot
	Pass selector type of chart data and options (for overriding default)
	eg: respChart($("#lineChart"),'Line',data);
	Here 'Line' is type of charts shown in chart.js docs : http://www.chartjs.org/docs/

*/
function respChart(selector,type,data, options){
	// get selector by context
	var ctx = selector.get(0).getContext("2d");
	// pointing parent container to make chart js inherit its width
	var container = $(selector).parent();

	// enable resizing matter
	$(window).resize( generateChart );

	// this function produce the responsive Chart JS
	function generateChart(){
		// make chart width fit with its container
		var ww = selector.attr('width', $(container).width() );
		switch(type){
			case 'Line':
				new Chart(ctx).Line(data, options);
				break;
			case 'Doughnut':
				new Chart(ctx).Doughnut(data, options);
				break;
			case 'Pie':
				new Chart(ctx).Pie(data, options);
				break;
			case 'Bar':
				new Chart(ctx).Bar(data, options);
				break;
			case 'Radar':
				new Chart(ctx).Radar(data, options);
				break;
			case 'PolarArea':
				new Chart(ctx).PolarArea(data, options);
				break;
		}
		// Initiate new chart or Redraw

	};
	// run function - render chart at first load
	generateChart();
}

var data = {
		labels : ["January","February","March","April","May","June","July"],
		datasets : [
			{
				fillColor : "rgba(220,220,220,0.5)",
				strokeColor : "rgba(220,220,220,1)",
				pointColor : "rgba(220,220,220,1)",
				pointStrokeColor : "#fff",
				data : [65,59,90,81,56,55,40]
			},
			{
				fillColor : "rgba(151,187,205,0.5)",
				strokeColor : "rgba(151,187,205,1)",
				pointColor : "rgba(151,187,205,1)",
				pointStrokeColor : "#fff",
				data : [28,48,40,19,96,27,100]
			}
		]
	}

respChart($("#lineChart"),'Line',data);


//donut chart
var data1 = [
	{
		value: 30,
		color:"#F7464A"
	},
	{
		value : 50,
		color : "#E2EAE9"
	},
	{
		value : 100,
		color : "#D4CCC5"
	},
	{
		value : 40,
		color : "#949FB1"
	},
	{
		value : 120,
		color : "#4D5360"
	}

]
respChart($("#doughnut"),'Doughnut',data1);


//Pie chart
var data2 = [
	{
		value: 30,
		color:"#F38630"
	},
	{
		value : 50,
		color : "#E0E4CC"
	},
	{
		value : 100,
		color : "#69D2E7"
	}
]
respChart($("#pie"),'Pie',data2);


//barchart
var data3 = {
	labels : ["January","February","March","April","May"],
	datasets : [
		{
			fillColor : "rgba(220,220,220,0.5)",
			strokeColor : "rgba(220,220,220,1)",
			data : [65,59,90,81,56]
		},
		{
			fillColor : "rgba(151,187,205,0.5)",
			strokeColor : "rgba(151,187,205,1)",
			data : [28,48,40,19,96]
		}
	]
}
respChart($("#bar"),'Bar',data3);

//radar chart
var data4 = {
	labels : ["Eating","Drinking","Sleeping","Designing","Coding","Partying","Running"],
	datasets : [
		{
			fillColor : "rgba(220,220,220,0.5)",
			strokeColor : "rgba(220,220,220,1)",
			pointColor : "rgba(220,220,220,1)",
			pointStrokeColor : "#fff",
			data : [65,59,90,81,56,55,40]
		},
		{
			fillColor : "rgba(151,187,205,0.5)",
			strokeColor : "rgba(151,187,205,1)",
			pointColor : "rgba(151,187,205,1)",
			pointStrokeColor : "#fff",
			data : [28,48,40,19,96,27,100]
		}
	]
}
respChart($("#radar"),'Radar',data4);

//Polar area chart
var data5 = [
	{
		value : 30,
		color: "#D97041"
	},
	{
		value : 90,
		color: "#C7604C"
	},
	{
		value : 24,
		color: "#21323D"
	},
	{
		value : 58,
		color: "#9D9B7F"
	},
	{
		value : 82,
		color: "#7D4F6D"
	},
	{
		value : 8,
		color: "#584A5E"
	}
]
respChart($("#polarArea"),'PolarArea',data5);


