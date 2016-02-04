<script type="text/javascript" SRC="http://www.leyant.com/data/resource/js/jquery.js"></script>
<script type="text/javascript" SRC="http://www.leyant.com/data/resource/js/jquery-ui/jquery.ui.js"></script>
<div style="height: 100px; width:100px;" id="block">
</div>
<input type="button" value="run" onclick="run()">
<script>
	function run(){
		$("#block").css('background-color', 'red');
		$("#block").animate({
			backgroundColor: '#fff',
		});
		$("#block").fadeOut();
	}
</script>