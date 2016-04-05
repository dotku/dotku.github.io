<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="initial-scale=1,user-scalable=no,maximum-scale=1,width=device-width">
    <title>TITLE</title>
    <link href="/lib/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="/lib/dpatch/dist/css/general-cn.css" rel="stylesheet"/>
    <script src="/lib/angular/angular.js"></script>
    <script src="/lib/jquery/dist/jquery.min.js"></script>
    <script src="/lib/bootstrap/dist/js/bootstrap.min.js"></script>
  </head>
  <body>
    <div class="container">
      <h1>TITLE</h1>
    </div>
  </body>
</html>

<?php 
  if ($_GET){
    $input = $_GET['input'];
    var_dump(ctype_digit($input));
  }
