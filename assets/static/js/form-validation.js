//Form Validation
	//validation rules taken from : http://jqueryvalidation.org/documentation/
	$('#jqueryForm').validate({
		highlight: function(elem) {
	      $(elem).closest('.form-group').removeClass('has-success').addClass('has-error');
	    },
	    errorClass: "error",
	    success: function(elem){
		    $(elem).closest('.form-group').removeClass('has-error').addClass('has-success');
	    },
	    rules: {
		    range: {
		      required: true,
		      range: [3, 6]
		    },
		    digits: {
		      required: true,
		      digits: true
		    },
		    numbers: {
		      required: true,
		      number: true
		    },
		    rangelength: {
		      required: true,
		      rangelength: [4, 7]
		    }
	  }
	});

