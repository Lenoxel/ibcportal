/*
INDEX
	- MAIN JQUERY DOCUMENT READY
		- SCROLL TO TOP
        - MAIN MENU
        - BILINGUAL BUTTONS
        - MOVE ASIDE POSITION
    - SECTION NAVIGATION
    - INDEX PAGE CONTENT
	- TABS
    - TOGGLE BTN
	- EDIT CONTENT
    - SUBMITFORM
	- CONFIRM DELETE
    - BUTTONS E-BLAST SCHEDULE
    - PAGINATION
*/

/* MAIN JQUERY DOCUMENT READY ------------------------------------------------------------------*/
$(function() {
	var window_width = $(window).width();

	/* SCROLL TO TOP ----------------*/
    var scroll_to_top = $('#scrollToTop');
	$(window).scroll(function() {
		$(this).scrollTop() > 100 ? $(scroll_to_top).fadeIn() : $(scroll_to_top).fadeOut();
	});
	$(scroll_to_top).click(function() {
		$('html, body').animate({scrollTop : 0}, 800);
		return false;
	});
	
    
    /* MAIN MENU --------------------*/	
	// SmartMenus mobile menu toggle button
	var $mainMenuState = $('#main-menu-state');
	if ($mainMenuState.length) {
		// animate mobile menu
		$mainMenuState.change(function(e) {
			var $menu = $('#main-menu');
			if (this.checked) {
				$menu.hide().slideDown(250, function() { $menu.css('display', ''); });
			} else {
				$menu.show().slideUp(250, function() { $menu.css('display', ''); });
			}
		});
		
		// hide mobile menu beforeunload
		$(window).bind('beforeunload unload', function() {
			if ($mainMenuState[0].checked) {
				$mainMenuState[0].click();
			}
		});
	}
    
    /* BILINGUAL BUTTONS ------------*/
	$('#bilingual_btns span').click(function(){
			if(!$(this).hasClass('selected')){
				$('#bilingual_btns span').removeClass('selected');
				if ($('.english').is(':visible')) {
					$('#btn_sp').addClass('selected');
					$('.english').hide();
					$('.spanish').show();
				} else {
					$('#btn_en').addClass('selected');
					$('.english').show();
					$('.spanish').hide();
				}		
			}
		}
	);        
    
    /* MOVE ASIDE POSITION ----------*/
    if( window_width < 880 ){
        var vm_aside = $('aside:has(div[class*="vmenu"])');
        $('aside:has(div[class*="vmenu"])').remove();
        $('main').append(vm_aside);
        $( "aside" ).wrap( "<section></section>" );
    }

    
}); // end document ready

/* SECTION NAVIGATION --------------------------------------------------------------------------*/
$(document).on('click', '#section_navigation a', function(event){
    // https://css-tricks.com/using-the-html5-history-api/
	$('#sn_content').fadeOut();

	var this_section    = $(this).attr('data-section');
	var this_url        = location.href;
	if( this_url.search('Section=') > 0 ){
		var new_url     = this_url.replace(/Section=[A-Za-z-_]*/i,'Section='+this_section);    
	} else {
		var new_url     = this_url+'&Section='+this_section;    
	}
	history.pushState(null,null,new_url);  

	$('#section_navigation a').removeClass('selected');
	$(this).addClass('selected');
	var params  = $(this).data();
	$.ajax({
		url: 'library/php/section_navigation.php',
		data : params,            
		success: function( data ) {
			$('#sn_content').html( data );
			$('#sn_content').fadeIn();
		},
	});        
	event.preventDefault();
});

/* INDEX PAGE CONTENT --------------------------------------------------------------------------*/
$(document).ready(function(){
	
	buildBookmarks();
	
	$('.box_index h1').click(function(){
		$('.page_index').slideToggle();
		if($(this).hasClass('open')){
			$(this).removeClass('open').addClass('close');
		} else {
			$(this).removeClass('close').addClass('open');
		}	
	});
});

function buildBookmarks(){
	var cAnchorCount 	= 0;
	var cAnchorCount2 	= 0;
	var n = $('div.index_this' ).length;

	if(n > 3){
		$('div.index_this').first().before('<div id="index_list"><a name="page_index">&nbsp;</a></div>');
		
		$('div.index_this').each(function() {
			$(this).prepend('<a name="bookmark' +cAnchorCount+ '"></a>');
			$(this).append('<div class="index_back"><a href="#page_index"><i class="fas fa-chevron-up"></i></i></a>');
			cAnchorCount += 1;
		});
	
		var oList 	= '<div class="box_index"><h1 class="open">Page Index</h1><div class="page_index">';
		$('div.index_this h3').each(function() {
			oList = oList + '<a href="#bookmark' +cAnchorCount2+ '">'+ $(this).text() +'</a>';
			cAnchorCount2 += 1;
		});
		oList = oList + '<div style="clear:both;"></div></div></div>';
		
		$('#index_list').after(oList);

		if(n > 15){
			$("div.page_index").addClass("index_hide");
			$(".box_index h1").removeClass("open").addClass("closed");
		}
	}
}

/* TABS ----------------------------------------------------------------------------------------*/
function openTab(TabName) {
  var i;
  var x = document.getElementsByClassName("Tab");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  document.getElementById(TabName).style.display = "block";  
}

/*  TOGGLE BTN ---------------------------------------------------------------------------------*/
$(document).on('click', '.js-toggle-btn', function(event){
    $(this).find('.js-toggle-content').toggle();
})


/*  EDIT CONTENT -------------------------------------------------------------------------------*/
$(document).on('click', 'a.js-edit_content', function(event){	
	var message 	 = $(this).attr('data-confirm-message');
    var cm_href      = $(this).attr('href');
    var cm_elementid = $(this).attr('data-element_id');
	var after_ajax	 = $(this).attr('data-after_ajax');    
    var params       = $(this).data();
	var pass 		 = true;
    
	if (typeof cm_elementid === 'undefined') {
		js_parent = $(this).closest('.js-parent');
	}	
	
	if (typeof message != 'undefined') {
		if (!(confirm(message))) {
			pass = false;
		}
	} 	
	
	if (pass){	    
	    $.ajax({
	        url: cm_href,
	        data : params,            
	        success: function( data ) {
	        	if (typeof cm_elementid === 'undefined') {
					js_parent.html( data );
	            } else if(cm_elementid === 'first_content') {
	                $('main').html( data );
					//$('.content').first().html( data );
	            } else {
	                $('#'+cm_elementid).html( data );   
	            } 
				if (!(typeof after_ajax === 'undefined')) {
					eval(after_ajax+';');
				}                           
	        },
	    });   
    }
         
    event.preventDefault();
});


/*  SUBMITFORM ---------------------------------------------------------------------------------*/
function submitForm(form) {	
	var validation   = $(form).find('input[name=form_validation]').val();
    var cm_action    = $(form).attr('action');
    var cm_elementid = $(form).find('input[name=sys_element_id]').val(); 
    var params       = $(form).serialize();
	if (typeof cm_elementid === 'undefined') {
		js_parent = $(form).closest('.js-parent');
	}	    
    
    if (typeof validation !== 'undefined') {
    	var status = eval(validation);
    	if (!status) {
    		return false;
    	}	
    }
    
	if (default_validation(form)) {
		$.ajax({
			method: "POST",
			url: cm_action,
			data : params,            
			success: function( data ) {
				if (typeof cm_elementid === 'undefined') {
					js_parent.html( data );
				} else if(cm_elementid === 'first_content') {                    
					$('main').html( data );
					//$('.content').first().html( data );
				} else {
					$('#'+cm_elementid).html( data );   
				}    
			},
			error: function (xhr, ajaxOptions, thrownError) {
				$('#'+cm_elementid).html('submitForm error: '+thrownError);
			}
    	});        	    
	}	    
	return false;
}

/*  CONFIRM DELETE -----------------------------------------------------------------------------*/
$(document).on('click', 'a.js-confirm', function(event){
   var retVal = confirm('Are you sure you want to delete this record?');
   if( retVal == true ){ return true; } else { return false; }
});


/* BUTTONS E-BLAST SCHEDULE --------------------------------------------------------------------*/
$(document).on('click', '#display_iframe a.js-btn', function(event){
    $('#display_iframe a').removeClass('selected');
    $(this).addClass('selected');      

    var this_class = $(this).attr('data-class');

    $('iframe').removeClass().addClass(this_class);
    event.preventDefault();
});   

/*-----------------------------------------------------------  PAGINATION ----------------------*/
$(document).on('click', 'a.js-pagination', function(event){
    var cm_href      = $(this).attr('href');
    var this_url     = location.href;
    var cm_elementid = $(this).attr('data-element_id');
    var this_page    = $(this).attr('data-page');
    var params       = $(this).data();
    
    if( this_url.search('page=') > 0 ){
        var new_url     = this_url.replace(/page=[0-9]*/i,'page='+this_page);    
    } else {
        var new_url     = this_url+'&page='+this_page;    
    }
    history.pushState(null,null,new_url);     
    
    $.ajax({
        url: cm_href,
        data : params,            
        success: function( data ) {
            $('#'+cm_elementid).html( data );   
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('An error occurred... Look at the console for more information!');

            $('#'+cm_elementid).html('<p>status code: '+jqXHR.status+'</p><p>errorThrown: ' + errorThrown + '</p><p>jqXHR.responseText:</p><div>'+jqXHR.responseText + '</div>');
            console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
        }        
        
    });        
    event.preventDefault();
});

function default_validation(form) {
	var passed      = true;
	var message     = '';
	var email       = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	var phone       = /^((([0-9]{1})*[- .(]*([0-9]{3})[- .)]*[0-9]{3}[- .]*[0-9]{4})+)*$/;
	var input_array = [];

	// some cleaning up if multiple form submissions are attempted
	$(form).find('.input_error').removeClass('input_error');

	$(form).find('.js-required:input:enabled').each(function() {
		var value = $(this).val().trim();

        if ($(this).is(':radio')) {
        	var name = $(this).attr('name');

        	if (input_array.indexOf(name) < 0) {
        		input_array.push(name);
        		//console.log(input_array);
        	}
        } else if ($(this).hasClass('js-checkbox')) {

        	if ($(this).find(':checkbox').filter(':checked').length === 0) {
        		message = 'Please review mandatory fields.';
        		$(this).addClass('input_error');
        	}
        } else if (value === '') {
			message = 'Please review mandatory fields.';
			$(this).addClass('input_error');
        }
	});

	for (var i = 0; i < input_array.length; i++) {
		// pick up all the inputs with the name from the input_array created above
		var inputs = $(form).find('input[name='+input_array[i]+']');

		//console.log(inputs);
		// we now have a jquery object and we are going to filter that using :checked
		// if :checked.length is 0, we know that nothing was checked and therefore must return false
		if ($(inputs).filter(':checked').length === 0) {
			message = 'Please review mandatory fields.';
			$(inputs).addClass('input_error');
		}
	}

	if (!alert_validation_error(form, message)) {
		return false;
	}

    //email
	$(form).find('.js-email').each(function() {
		// .test() returns true if passed
        if($(this).val().trim() !=''){
    		if (!email.test($(this).val().trim())) {
    			message = 'Email is not in a correct format.';
    	        $(this).addClass('input_error');
    		}
        }
	});

	if (!alert_validation_error(form, message)) {
		return false;
	}

    //phone
	$(form).find('.js-phone').each(function() {
		// .test() returns true if passed
		if (!phone.test($(this).val().trim())) {
			message = 'Please enter the phone number';
            $(this).addClass('input_error');
		}
	});
	
		
	if ($(form).find('.js-confirm_password').length === 2) {		
		if ($(form).find('.js-confirm_password').eq(0).val() != $(form).find('.js-confirm_password').eq(1).val()) {
			message = 'Passwords do not match.';
			$(form).find('.js-confirm_password').addClass('input_error');
		}			
	} 
		

	if (!alert_validation_error(form, message)) {
		return false;
	}

	return true;
}

function alert_validation_error(form, message) {
	// if it exists, it will focus on the first thing that is wrong
	if ($('.input_error').length > 0) {
		$(form).find('.input_error:first').focus();
		alert(message);
		return false;
	}
	return true;
}