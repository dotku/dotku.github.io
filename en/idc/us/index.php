<?php 
	$pageinfo = array(
		'title' 			=> 'IDC-US',
		'description' 	=> '介绍美国的 IDC 的情况',
		'keywords' 	=> 'idc, us, discount, cheap, web hosting, web host, rank, cloud'
	);
?>
<!DOCTYPE html>
<!-- http://www.w3schools.com/tags/ref_language_codes.asp -->
<html lang="zh">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
		
		<title><?php echo $pageinfo['title'];?></title>
		<meta name='description' content='<?php echo $pageinfo['description'];?>'>
		<meta name='keywords' content='<?php echo $pageinfo['keywords'];?>'>
		
		<link rel="icon" href="/favicon.png">
		<link href="/lib/dotku/dist/css/base.css" rel="stylesheet">
		<!-- Bootstrap -->
		<link href="/lib/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
		<link href="/lib/dotku/dist/css/general-cn.css" rel="stylesheet">
		

		<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
		<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
		<!--[if lt IE 9]>
		  <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
		  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		<![endif]-->
	  </head>
	<body>
		<div class="container">
			<h1><?php echo $pageinfo['title'];?></h1>
			<p><?php echo $pageinfo['description'];?></p>
			<h2>247Zilla</h2>
            <h3>General</h3>
            <table class="table">
                <tr>
					<th class="col-md-2">属性</h2>
					<th>内容</h2>
				</tr>
                <tr>
                    <td></td>
                    <td></td>
                </tr>
            </table>
            <h3>Server</h3>
            <table class="table sortable">
                <thead>
				<tr>
					<th class="col-md-2">属性</h2>
					<th>内容</h2>
				</tr>
				</thead>
				<tr>
					<td>Name Server</td>
					<td>
						<?php 
							echo nl2br("Primary Hostname : ns1.premium.247zilla.com
								Primary IP Address : 50.28.14.156
								Secondary Hostname : ns2.premium.247zilla.com
								Secondary IP Address : 50.28.14.157"
							);
						?>
					</td>
				</tr>
                <tr>
					<td>System</td>
					<td>
						<?php 
							echo nl2br("CentOS 6.7");
						?>
					</td>
				</tr>
				</tbody>
			</table>
			<h3>MySQL</h3>
			<table class="table sortable">
				<thead>
				<tr>
					<th class="col-md-2">属性</h2>
					<th>内容</h2>
				</tr>
				</thead>
				<tbody>
				<tr>
					<td>SQL最大值</td>
					<td>50MiB</td>
				</tr>
                </table>
                
                
			
		</div>
		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
		<script src="/lib/jquery/dist/jquery.min.js"></script>
		<!-- Include all compiled plugins (below), or include individual files as needed -->
		<script src="/lib/bootstrap/dist/js/bootstrap.min.js"></script>
		<script>
		</script>
	</body>
</html>