<?php 
    session_start();
    $_SESSION['cart_id'] = 'cart_a';
    echo 'session_id: '.session_id()."<br/>";
    echo $_SESSION['cart_id']."<br/>";
    // session_destroy();
    session_write_close();
    session_id($_GET['cart_id']);
    echo 'new_session_id: '.session_id()."<br/>";
    session_start();
    // cookie('session_id', session_id());
    if (!isset($_GET['cart_id'])){
      header("location:".$_SERVER['REQUEST_URI']."?cart_id=".session_id());
    }

    echo $_SERVER['REQUEST_URI']."<br/>";
    echo session_id()."<br/>";
    // echo cookie('session_id');
    echo 'new session cart_id: '.@$_SESSION['cart_id'];