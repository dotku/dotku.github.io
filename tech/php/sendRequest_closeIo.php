<?php 
    $url = "http://app.close.io/hackwithus/";    
    $content = "{"
    ." 'first_name' : 'Weijing',"
    ." 'last_name' : 'Lin', "
    ." 'email' : 'lwjct@hotmail.com', "
    ." 'phone' : '4153702887', "
    ." 'cover_letter': 'I\'m Weijing Jay Lin and applying for the position',"
    ." 'urls' : {"
    ."    'github' : 'http://www.github.com/dotku'"
    ." }"
    ."}";

    $curl = curl_init($url);
    curl_setopt($curl, CURLOPT_HEADER, false);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER,
            array("Content-type: application/json"));
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $content);

    $json_response = curl_exec($curl);

    $status = curl_getinfo($curl, CURLINFO_HTTP_CODE);

    if ( $status != 201 ) {
        die("Error: call to URL $url failed with status $status, response $json_response, curl_error " . curl_error($curl) . ", curl_errno " . curl_errno($curl));
    }


    curl_close($curl);
    echo $json_response;
    //$response = json_decode($json_response, true);
    ?>