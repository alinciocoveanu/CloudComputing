<?php
require_once('Controller\CitiesController.php');
require_once('Connector\DatabaseConnector.php');

header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: GET,POST,PUT,PATCH,DELETE");

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$uri = explode( '/', $uri );

if ($uri[2] != 'cities') {
    header("HTTP/1.1 404 Not Found");
    exit();
}

$database = new DatabaseConnector();
$dbConnection = $database->getConnection();

$userId = null;
$request = (array) json_decode(file_get_contents('php://input'), TRUE);

if (isset($uri[3]))
    $userId = $uri[3];
elseif (isset($request['id']))
    $userId = $request['id'];

$requestMethod = $_SERVER["REQUEST_METHOD"];

$controller = new CitiesController($dbConnection, $requestMethod, $userId);
$controller->processRequest();
?>