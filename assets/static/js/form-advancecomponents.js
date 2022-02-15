


	//Select2

	$("#select1").select2();
	$("#selectm").select2();
	$("#tags").select2({tags:["red", "green", "blue","orange","yellow"]});

	//Switch Buttons
	var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));

	elems.forEach(function(html) {
	  var switchery = new Switchery(html);
	});

	// Switch Buttons :

	var blue = document.querySelector('.js-switch-blue');
	var switchery = new Switchery(blue, { color: '#3ba0ff' });

	var green = document.querySelector('.js-switch-green');
	var switchery = new Switchery(green, { color: '#57BE85' });

	var red = document.querySelector('.js-switch-red');
	var switchery = new Switchery(red, { color: '#ff6c60' });

	var sky = document.querySelector('.js-switch-sky');
	var switchery = new Switchery(sky, { color: '#54D1F1' });

	var yellow = document.querySelector('.js-switch-yellow');
	var switchery = new Switchery(yellow, { color: '#FDB813' });

	var pink = document.querySelector('.js-switch-pink');
	var switchery = new Switchery(pink, { color: '#ff7791' });

	var teal = document.querySelector('.js-switch-teal');
	var switchery = new Switchery(teal, { color: '#3cc8ad' });

	var darkred = document.querySelector('.js-switch-darkred');
	var switchery = new Switchery(darkred, { color: '#db5554' });

	//Datepicker
	$('#dp1').datepicker();
	$('#dp2').datepicker();
	$('#dp3').datepicker();

	//Timepicker
	$('#timepicker1').timepicker();
	$('#timepicker2').timepicker({
					minuteStep: 1,
	                showSeconds: true,
	                showMeridian: false,
	});

	//Colorpicker
	 $('.colorpicker').colorpicker();

	 $('#rgba').colorpicker({
	            format: 'rgba', // force this format
	            horizontal: true
	});

	//Wysiwyg editor
	 $('#wysiwyg').wysihtml5({
		 "size": ''
	 });

	//Checkbox radio
	//Checkbox radio
	$('.minimal-input-black,.minimal-input-disabled').iCheck({
	    checkboxClass: 'icheckbox_minimal',
	    radioClass: 'iradio_minimal',
	    increaseArea: '20%'
	  });
	$('.minimal-input-red').iCheck({
	    checkboxClass: 'icheckbox_minimal-red',
	    radioClass: 'iradio_minimal-red',
	    increaseArea: '20%'
	  });
	$('.minimal-input-green').iCheck({
	    checkboxClass: 'icheckbox_minimal-green',
	    radioClass: 'iradio_minimal-green',
	    increaseArea: '20%'
	  });
	$('.minimal-input-blue').iCheck({
	    checkboxClass: 'icheckbox_minimal-blue',
	    radioClass: 'iradio_minimal-blue',
	    increaseArea: '20%'
	  });
	$('.minimal-input-yellow').iCheck({
	    checkboxClass: 'icheckbox_minimal-yellow',
	    radioClass: 'iradio_minimal-yellow',
	    increaseArea: '20%'
	  });
	$('.minimal-input-purple').iCheck({
	    checkboxClass: 'icheckbox_minimal-purple',
	    radioClass: 'iradio_minimal-purple',
	    increaseArea: '20%'
	 });

	 //Flat checkbox radios

	$('.flat-input-black,.flat-input-disabled').iCheck({
	    checkboxClass: 'icheckbox_flat',
	    radioClass: 'iradio_flat',
	    increaseArea: '20%'
	  });
	$('.flat-input-red').iCheck({
	    checkboxClass: 'icheckbox_flat-red',
	    radioClass: 'iradio_flat-red',
	    increaseArea: '20%'
	  });
	$('.flat-input-green').iCheck({
	    checkboxClass: 'icheckbox_flat-green',
	    radioClass: 'iradio_flat-green',
	    increaseArea: '20%'
	  });
	$('.flat-input-blue').iCheck({
	    checkboxClass: 'icheckbox_flat-blue',
	    radioClass: 'iradio_flat-blue',
	    increaseArea: '20%'
	  });
	$('.flat-input-yellow').iCheck({
	    checkboxClass: 'icheckbox_flat-yellow',
	    radioClass: 'iradio_flat-yellow',
	    increaseArea: '20%'
	  });
	$('.flat-input-purple').iCheck({
	    checkboxClass: 'icheckbox_flat-purple',
	    radioClass: 'iradio_flat-purple',
	    increaseArea: '20%'
	 });

	//X-editable
	$('#username,#firstname,#comments').editable();

	$('#sex').editable({
	        prepend: "not selected",
	        source: [
	            {value: 1, text: 'Male'},
	            {value: 2, text: 'Female'}
	        ],
	        display: function(value, sourceData) {
	             var colors = {"": "gray", 1: "green", 2: "blue"},
	                 elem = $.grep(sourceData, function(o){return o.value == value;});

	             if(elem.length) {
	                 $(this).text(elem[0].text).css("color", colors[value]);
	             } else {
	                 $(this).empty();
	             }
	        }
	    });

	$('#fruits').editable({
	       pk: 1,
	       limit: 3,
	       source: [
	        {value: 1, text: 'banana'},
	        {value: 2, text: 'peach'},
	        {value: 3, text: 'apple'},
	        {value: 4, text: 'watermelon'},
	        {value: 5, text: 'orange'}
	       ]
	    });
