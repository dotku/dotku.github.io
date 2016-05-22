<?php 
$mysqli = new mysqli("localhost", "root", "admin123");
echo mysqli_real_escape_string($mysqli, '<b>Bold</b>');