<?php
class arrayHelper{
/**
 * searches a simple as well as multi dimension array
 * @param type $needle
 * @param type $haystack
 * @return boolean
 */
public static function in_array_multi($needle, $haystack){
    // var_dump($haystack);
    if (is_string($needle)){
        $needle = trim($needle);
    }
    if (is_array($haystack) && is_array($needle)){
        
        try {
            if (!array_diff($haystack, $needle)){
                return True;
            }
        } catch (\Exception $e){
            var_dump($e);
        }

    }
    if(!is_array($haystack))
        return False;

    foreach($haystack as $key=>$value){
        if(is_array($value)){
            if(self::in_array_multi($needle, $value))
                return True;
            else
               self::in_array_multi($needle, $value);
        } else if(is_string($needle) && trim($value) === trim($needle)){//visibility fix//
            var_dump('string check');
            error_log("$value === $needle setting visibility to 1 hidden");
            return True;
        }
    }

    return False;
}
}

// tester

$arr1 = array(
        'level1' => array(
            'level2' => array(
                'level3' => 'hello')
            )
    );
$needle = array('level3'=>'hello');

var_dump(arrayHelper::in_array_multi($needle, $arr1));
var_dump(arrayHelper::in_array_multi('hello', $arr1));