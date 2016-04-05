<?php
namespace Common\Model;
use Think\Model;
class TestUnderModel extends Model {
  public function sayHi(){
    echo 'hello_common';
  }
}