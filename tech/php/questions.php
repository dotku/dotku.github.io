<?php 

class A {
  var $sampleArray = array('hi');
  public function __construct() {
    //$this->sampleArray = array('aArray');
  }
  public function getSampleArray(){
    $this->output['msg'] = 'logout successfully';
    $this->output['status_code'] = 1;
    $this->output['status'] = 'success';
    var_dump($this->output);
  }
}

$aClass = new A();
$aClass->getSampleArray();