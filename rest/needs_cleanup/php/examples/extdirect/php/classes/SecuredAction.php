<?php

session_start();

function getHeaders()
{
$headers = array();
foreach ($_SERVER as $k => $v)
{
if (substr($k, 0, 5) == "HTTP_")
{
$k = str_replace('_', ' ', substr($k, 5));
$k = str_replace(' ', '-', ucwords(strtolower($k)));
$headers[$k] = $v;
}
}
return $headers;
}

foreach (getHeaders() as $name => $value) {
    error_log("$name: $value");
}

class SecuredAction {
    function doEcho($data){
        //session_start();
        return $data;
    }
}
