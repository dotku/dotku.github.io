<!DOCTYPE html>
<html ng-app="myApp">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Product</title>
    <link href="/lib/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="/lib/dpatch/dist/css/general-cn.css" rel="stylesheet"/>
    <script src="/lib/angular/angular.js"></script>
    <script src="/lib/jquery/dist/jquery.min.js"></script>
    <script src="/lib/bootstrap/dist/js/bootstrap.min.js"></script>
  </head>
  <body ng-controller="Aaa">
  <?php var_dump($_GET) ?>

    <script>
    var m1 = angular.module('myApp',[]);
    /*
    m1.config(function($locationProvider){
      $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
      });
    });
    */
    m1.controller('Aaa',['$location',function($location){
      //$location.search().id;
      //console.log($location.search({id:10}));
      //$location.html5Mode(true);
      console.log($location.search().id);
    }]);
  </script>
  </body>
</html>