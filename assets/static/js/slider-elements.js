//Sliders
		$( "#slider" ).slider();

		$( "#master" ).slider({
	      value: 60,
	      orientation: "horizontal",
	      range: "min",
	      animate: true
	    });

		$( "#slider-range" ).slider({
	      range: true,
	      min: 0,
	      max: 500,
	      values: [ 75, 300 ],
	      slide: function( event, ui ) {
	        $( "#amount-range" ).html( "Price Range: $" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
	      }
	    });
	    $( "#amount-range" ).html( "Price Range: $" + $( "#slider-range" ).slider( "values", 0 ) +
		   " - $" + $( "#slider-range" ).slider( "values", 1 ) );


	    $( "#slider-range-min" ).slider({
	      range: "min",
	      value: 37,
	      min: 1,
	      max: 700,
	      slide: function( event, ui ) {
	        $( "#amount-range-min" ).html( "Minimum price: $" + ui.value );
	      }
	    });
	    $( "#amount-range-min" ).html( "Minimum price: $" + $( "#slider-range-min" ).slider( "value" ) );

	    $( "#slider-range-max" ).slider({
	      range: "max",
	      min: 1,
	      max: 10,
	      value: 2,
	      slide: function( event, ui ) {
	        $( "#amount-range-max" ).html( "Maximum price: $" + ui.value );
	      }
	    });
	    $( "#amount-range-max" ).html( "Maximum price: $" + $( "#slider-range-max" ).slider( "value" ) );

	    $( "#steps-slider" ).slider({
	      value:100,
	      min: 0,
	      max: 500,
	      step: 50,
	      slide: function( event, ui ) {
	        $( "#amount-steps-slider" ).html( "Donation: $" + ui.value );
	      }
	    });
	    $( "#amount-steps-slider" ).html( "Donation: $" + $( "#steps-slider" ).slider( "value" ) );

	    $( "#slider-vertical" ).slider({
	      orientation: "vertical",
	      range: "min",
	      min: 0,
	      max: 100,
	      value: 60,
	      slide: function( event, ui ) {
	        $( "#amount-slider-vertical" ).html("Volume: " + ui.value );
	      }
	    });
	    $( "#amount-slider-vertical" ).html( "Volume: " + $( "#slider-vertical" ).slider( "value" ) );

	    $( "#slider-vertical-range" ).slider({
	      orientation: "vertical",
	      range: true,
	      values: [ 17, 67 ],
	      slide: function( event, ui ) {
	        $( "#amount-slider-vertical-range" ).html( "Sales: $" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
	      }
	    });
	    $( "#amount-slider-vertical-range" ).html( "Sales $" + $( "#slider-vertical-range" ).slider( "values", 0 ) +
	      " - $" + $( "#slider-vertical-range" ).slider( "values", 1 ) );

		  $( "#eq > span" ).each(function() {
	      // read initial values from markup and remove that
	      var value = parseInt( $( this ).text(), 10 );
	      $( this ).empty().slider({
	        value: value,
	        range: "min",
	        animate: true,
	        orientation: "vertical"
	      });
	    });