<?php
class TestAction {
    function doEcho($data){
        return $data;
    }

    function doEchoSlow($data){
        sleep(3);
        return $data;
    }

    function square($num){
        if(!is_numeric($num)){
            throw new Exception('Call to square with a value that is not a number');
        }
        return $num * $num;
    }

    function add($num1, $num2){
        if(!is_numeric($num1)){
            throw new Exception('Number 1 not a number');
        }
        if(!is_numeric($num2)){
            throw new Exception('Number 2 not a number');
        }
        return $num1 + $num2;
    }
}
