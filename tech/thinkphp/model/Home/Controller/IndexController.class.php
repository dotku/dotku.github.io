<?php
namespace Home\Controller;
use Think\Controller;
class IndexController extends Controller {
    public function index(){
        $model_test = D('test_under', 'Common');
        $model_test->sayHi();
    }
}