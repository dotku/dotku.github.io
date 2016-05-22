<?php 
    echo mt_rand()."<br/>";
    echo time()."<br/>";
    echo md5(time().mt_rand());
    // $bytes = random_bytes(5);
    // var_dump(bin2hex($bytes));