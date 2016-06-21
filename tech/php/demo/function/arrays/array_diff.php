<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>array_diff</title>
    <link href="/lib/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="/lib/dpatch/dist/css/general-cn.css" rel="stylesheet"/>
    <script src="/lib/angular/angular.js"></script>
    <script src="/lib/jquery/dist/jquery.min.js"></script>
    <script src="/lib/bootstrap/dist/js/bootstrap.min.js"></script>
  </head>
  <body>
    <div class="container">
      <h1>array_diff</h1>
      <p>Array Diff would course `Array to string conversion`, you could turn off the notice, 
      but there is a better way to achieve. The solution is `array_map`.</p>
      
      <script src="https://gist.github.com/dotku/400b97ac717aa247a3060bdb7c187a9a.js"></script>

      <pre><?php 
        $arr1 = array(
            'level1' => array(
                'level2' => array(
                    'level3' => 'hello',
                    'level3_sub' => 'world'
                )
            )
        );
        $arr2 = array('level3'=>'world');
        $needle1 = array('level3'=>'hello');
        $needle2 = array('level3'=>'world');
        $needle3 = array('level3_sub'=>'world');
        $needle4 = array('level4' => '');

        var_dump(!array_diff($arr1, $needle1));
        var_dump(!array_diff($arr1, $needle2));

        var_dump(!array_diff(array_map('serialize',$arr1), array_map('serialize',$needle1)));
        var_dump(!array_diff(array_map('serialize',$arr1), array_map('serialize',$needle2)));

        var_dump(!array_diff(array_map('serialize',$arr2), array_map('serialize',$needle1)));
        var_dump(!array_diff(array_map('serialize',$arr2), array_map('serialize',$needle2)));
        var_dump(!array_diff(array_map('serialize',$arr2), array_map('serialize',$needle3)));
        var_dump(!array_diff(array_map('serialize',$arr2), array_map('serialize',$needle4)));
        ?>
    </pre>
    </div>
  </body>
</html>
