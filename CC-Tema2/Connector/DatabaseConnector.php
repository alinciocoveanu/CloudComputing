<?php

class DatabaseConnector {

    private $dbConnection;

    public function __construct()
    {
        $file = file_get_contents("Config\config.json");
        $config = json_decode($file, true);
        try {
            $this->dbConnection = mysqli_connect($config['host'], $config['username'], $config['password'], $config['db']);
        }
        catch (mysqli_sql_exception $e) {
            echo "Erorr: can't connect to mysql db." . PHP_EOL;
            echo "Errno: " . mysqli_connect_errno() . PHP_EOL;
            echo "Error: " . mysqli_connect_error() . PHP_EOL;
            echo $e;
            exit;
        }
    }

    public function getConnection()
    {
        return $this->dbConnection;
    }

    public function __destruct()
    {
        mysqli_close($this->dbConnection);
    }
}

?>