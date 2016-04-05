<?php
namespace Home\Model;
use Think\Model;
class TestUnderModel extends Model {
  public function sayHi(){
    echo 'hello_home';
  }
}