<?php
class MyDestructableClass {
   function __construct() {
       print "In constructor\n";
       $this->name = "MyDestructableClass";
   }
   
   function foo() {
       print "foo" . "\n";
   }

   function __destruct() {
       print "Destroying " . $this->name . "\n";
   }
}

$obj = new MyDestructableClass(); // In constructor
$obj->foo(); // foo
// will display "Destroying MyDestructableClass" after all function done
?> 