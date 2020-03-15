<?php

class CitiesGateway {

    private $db;

    public function __construct($db)
    {
        $this->db = $db;
    }

    public function getAll() {
        $query = "SELECT id, name, country, size, population FROM cities;"; 

        $getQuery = mysqli_query($this->db, $query);

        if($getQuery) {
            $rez = array();
            while ($row = $getQuery->fetch_assoc()) 
                array_push($rez, $row);
        } else
            return false;

        return $rez;
    }

    public function getById($id) {
        $query = "SELECT * FROM cities where id = $id;"; 

        $getQuery = mysqli_query($this->db, $query);

        if($getQuery)
            $rez = mysqli_fetch_assoc($getQuery);
        else
            return false;

        return $rez;
    }

    public function insert($name, $country, $size, $population) {
        $query = "INSERT INTO 
                    cities (id, name, country, size, population)
                    VALUES (NULL, '$name', '$country', '$size', '$population');";

        $getQuery = mysqli_query($this->db, $query);

        if($getQuery)
            $newQuery = "SELECT * FROM cities ORDER BY id DESC LIMIT 1;";
            $newGetQuery = mysqli_query($this->db, $newQuery);
            if($newGetQuery)
                return mysqli_fetch_assoc($newGetQuery);
            return false;
        return false;
    }

    public function replace($id, $name, $country, $size, $population) {
        $query = "UPDATE cities 
                    SET 
                        name = '$name',
                        country = '$country',
                        size = '$size',
                        population = '$population'
                    WHERE id = $id;";

        $getQuery = mysqli_query($this->db, $query);

        if($getQuery)
            return true;
        return false;
    }

    public function modify($id, $name, $country, $size, $population) {
        $query = "UPDATE cities SET ";
        if($name)
            $query .= "name = '$name',";
        if($country)                
            $query .= "country = '$country',";           
        if($size)
            $query .= "size = '$size',";
        if($population)                
            $query .= "population = '$population'";       
        else
            $query = substr($query, 0, -1);   
        $query .= " WHERE id = $id;";

        $getQuery = mysqli_query($this->db, $query);

        if($getQuery)
            return true;
        return false;
    }

    public function delete($id) {
        $query = "DELETE FROM cities WHERE id = $id;";

        $getQuery = mysqli_query($this->db, $query);

        if($getQuery)
            return true;
        return false;
    }
}

?>