// JavaScript Document
$(document).ready(function(){
	var number = $('.post-main .slider > div');
	$('.title > .wrap > .count').text('/' + number.length);
	$('#post-bar').slick({
		slidesToShow: 4,
		slidesToScroll: 1,
		autoplay: true,
		autoplaySpeed: 5000,
	});
	
	$('.post-main .autoplay').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		autoplay: true,
		autoplaySpeed: 5000,
	});
	$('.post-main .autoplay').on('beforeChange', function(event, slick, currentSlide, nextSlide){
			console.log(nextSlide);
			$('.title > .wrap > .activeindex').text(nextSlide+1);
	});
	
	/*回到顶部*/
	/*$(".scrolltop3").click(function(){goTop()});
	function goTop(){
		$('html,body').animate({'scrollTop':0},600);
	}*/
	
	jQuery(window).scroll(function() {
        if (jQuery(this).scrollTop() > 200) {
            jQuery(".scrolltop3").fadeIn(200)
        } else {
            jQuery(".scrolltop3").fadeOut(200)
        }
    });
    jQuery(".scrolltop3").click(function() {
        /*jQuery(window).scrollTop(0);*/
		$('html,body').animate({'scrollTop':0},600);
        return false
    });
	
	/*end 回到顶部*/

});