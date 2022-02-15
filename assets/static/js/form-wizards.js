	//Form Wizard Next previous button and validate next button
	$('.btn-previous').click(function(){
		$(this).parents().prevAll().closest('.wizard').wizard('previous');
	});
	$('.btn-next').click(function(){
		$(this).parents().prevAll().closest('.wizard').wizard('next');
	});
	$('.btn-next-validate').click(function(){

		var form=$(this).parents().prevAll().closest('form');
		var validated=form.valid();
		if(validated){$(this).parents().prevAll().closest('.wizard').wizard('next');}

	});