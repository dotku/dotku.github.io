// JavaScript Document
window.onload = function(){
	
	// 切换搜索框
	(function(){
		var text = $('#top .search .text');
		text.focus(function (){
			if(this.value == '最多输入10个运单号，用Enter或斜杠/分隔') {
				this.value = '';
			}
		});
		text.blur(function(){
			if(this.value == '') {
				this.value = '最多输入10个运单号，用Enter或斜杠/分隔';
			}
		});
	})();
	
	/*banner无缝切换*/
	(function(){
		var ul = $('#banner > ul');
		var li = $('#banner > ul li');
		var img = $('#banner > ul li img');
		var prev = $('#banner .prev');
		var next = $('#banner .next');
		var play = $('#banner .play');
		var btnWrap = $('#banner .btn_wrap');
		
		var now = 0;
		var btn = true;
		var timer = null;
		
		$(ul).width(li.length * $(li[0]).width());
	
		$('#banner').hover(function(){
			$(prev).show();
			$(next).show();
		},
		function(){
			$(prev).hide();
			$(next).hide();
		});
		
		/*图片居中*/
		function winSize(){
			var viewWidth = document.documentElement.clientWidth;
			if(viewWidth > 1000){
				for(var i=0; i<img.length; i++){
					$(img[i]).css('left',-($(img).width() - viewWidth)/2);
				}
			}
		}
		winSize();
		window.onresize = function(){
			winSize();
		};
		/*end 图片居中*/
		
		/*添加按扭*/
		for(var i=0; i<li.length; i++){
			$(btnWrap).append('<a href="javascript:;"></a>');
		};
		$(btnWrap).find('a:eq(1)').attr('class','active');
		/*end 添加按扭*/
		
		/*上一张*/
		$(prev).click(function(){
			clearInterval(timer);
			if($(play).attr('class') == 'pause'){
				clearInterval(timer);
			}
			else{
				autoPlay();
			}
			if(btn){
				btn = false;
				if(now == 0){
					now = li.length-1;				
				}
				else{
					now--;	
				}
				if(now == li.length-1){
					$(li[0]).animate({left:$(li[0]).width()},'slow');
				}
				else if(now == 0){
					$(li[li.length-1]).css('left',-$(li[0]).width());
				}
				else{
					$(li[now-1]).animate({left:-$(li[0]).width()},'slow');
				}
				$(li[now-1]).css('left',-$(li[0]).width());
				$(li[now+1]).animate({left:$(li[0]).width()},'slow');
				$(li[now]).animate({left:0},'slow',function(){
					if(now == li.length-1){
						$(li[0]).css('left',$(li[0]).width());
					}
					btn = true;
				});
			}
			$(btnWrap).find('a:gt(0)').removeClass('active');
			$(btnWrap).find('a:eq('+(now+1)+')').attr('class','active');
		});
		/*end 上一张*/
				
		/*下一张*/
		$(next).click(function(){
			clearInterval(timer);
			if($(play).attr('class') == 'pause'){
				clearInterval(timer);
			}
			else{
				autoPlay();
			}
			move();
		});
		/*end 下一张*/
		for(var i=0;i<li.length-1;i++){
			$(li[now]).css('left',0);
			$(li[now+i]).css('left',$(li[0]).width());
			$(li[li.length-1]).css('left',-$(li[0]).width());
		}
		autoPlay();
		
		/*运行暂停*/
		$(play).click(function(){
			if($(this).attr('class') == 'play'){
				$(this).attr('class','pause')
				clearInterval(timer);
			}
			else{
				$(this).attr('class','play')
				autoPlay();
			}
		});
		/*end 运行暂停*/
		
		function move(){
			if(btn){
				btn = false;
				if(now == li.length-1){
					now = 0;				
				}
				else{
					now++;	
				}
				if(now == 0){
					$(li[li.length-1]).animate({left:-$(li[0]).width()},'slow');
				}
				else {
					$(li[now-1]).animate({left:-$(li[0]).width()},'slow');
				}
				$(li[now+1]).css('left',$(li[0]).width());	
				$(li[now]).animate({left:0},'slow',function(){
					if(now == li.length-1){
						$(li[0]).css('left',$(li[0]).width());
					}
					btn = true;
				});
			}
			$(btnWrap).find('a:gt(0)').removeClass('active');
			$(btnWrap).find('a:eq('+(now+1)+')').attr('class','active');
		}
		
		/*自动播放*/
		function autoPlay(){
			timer = setInterval(function () {
				move();
			}, 3000);
		};
		/*end 自动播放*/	
		
	})();
	/*end banner无缝切换*/
	
	/*回到顶部*/
	$(".scrolltop3").click(function(){goTop()});
	function goTop(){
		$('html,body').animate({'scrollTop':0},600);
	}
	/*end 回到顶部*/
	
	(function(){
		var ul = $('.navbar > .wrap ul');
		var li = $('.navbar > .wrap ul li');
		
		$(ul).width(li.length * $(li[0]).width() + (li.length - 1) * parseInt($(li[0]).css('margin-right')));
		
		$('.navbar > .wrap').jCarouselLite({
					btnPrev: '.navbar > .next',
					btnNext: '.navbar > .prev',
					visible: 4
		});		
	})();
	
	(function(){
		var li = $('.main > .wrap ul li');
		var prev = $('.main > .prev');
		var next = $('.main > .next');
		
		$('.main').hover(function(){
			$(prev).show();
			$(next).show();
		},
		function(){
			$(prev).hide();
			$(next).hide();
		});
		$('.main > .wrap').jCarouselLite({
					btnPrev: '.main > .next',
					btnNext: '.main > .prev',
					visible: 1,
					afterEnd:function(a){
						var index = $(a).index() == (li.length + 1)?1:$(a).index();
						$('.title >.wrap >.activeindex').text(index);
					}
		});
	})();
};