$(function(){
  // init
  $("title, h1").text(app.name);
  for (var prop in app) {
    $('.' + 'app' + '-' + prop).text(app[prop]);
    console.log(app[prop]);
  }
})