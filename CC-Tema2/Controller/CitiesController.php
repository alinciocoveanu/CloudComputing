<?php
require_once('Gateway\CitiesGateway.php');

class CitiesController {
    private $requestMethod;
    private $cityId;
    private $citiesGateway;

    public function __construct($db, $requestMethod, $cityId)
    {
        $this->requestMethod = $requestMethod;
        $this->cityId = $cityId;
        $this->citiesGateway = new CitiesGateway($db);
    }

    public function processRequest()
    {
        switch($this->requestMethod) {
            case 'GET':
                $response = $this->cityId ? $this->getCity($this->cityId) : $this->getAllCities();
                break;
            case 'POST':
                $response = $this->createCity();
                break;
            case 'PUT':
                $response = $this->replaceCity($this->cityId);
                break;
            case 'PATCH':
                $response = $this->modifyCity($this->cityId);
                break;
            case 'DELETE':
                $response = $this->deleteCity($this->cityId);
                break;
            default:
                $response = $this->notImplemented();
                break;
        }
                
        header($response['status_code_header']);
        if ($response['body'])
            echo $response['body'];
    }

    private function getCity($id)
    {
        $result = $this->citiesGateway->getById($id);
        if(!$result) 
            return $this->notFoundResponse();

        return $this->okCode($result);
    }

    private function getAllCities()
    {
        $result = $this->citiesGateway->getAll();

        return $this->okCode($result);
    }

    private function createCity()
    {
        $input = (array) json_decode(file_get_contents('php://input'), TRUE);

        if (!$this->validateRequest($input)) 
            return $this->badRequest();
        if ($this->cityId)
            return $this->notImplemented();

        $result = $this->citiesGateway->insert($input['name'], $input['country'], $input['size'], $input['population']);

        return $this->createdCode($result);
    }
    
    private function replaceCity($id)
    {
        if (!$this->cityId)
            return $this->methodNotAllowed();

        $result = $this->citiesGateway->getById($id);

        if (!$result) 
            return $this->notFoundResponse();

        $input = (array) json_decode(file_get_contents('php://input'), TRUE);
        if (!$this->validateRequest($input))
            return $this->badRequest();

        $this->citiesGateway->replace($id, $input['name'], $input['country'], $input['size'], $input['population']);

        return $this->noContent();
    }

    private function modifyCity($id)
    {
        if (!$this->cityId)
            return $this->methodNotAllowed();

        $result = $this->citiesGateway->getById($id);

        if (!$result) 
            return $this->notFoundResponse();

        $input = (array) json_decode(file_get_contents('php://input'), TRUE);
        $name = isset($input['name']) ? $input['name'] : null;
        $country = isset($input['country']) ? $input['country'] : null;
        $size = isset($input['size']) ? $input['size'] : null;
        $population = isset( $input['population']) ? $input['population'] : null;

        $this->citiesGateway->modify($id, $name, $country, $size, $population);

        return $this->noContent();
    }

    private function deleteCity($id)
    {
        if (!$this->cityId)
            return $this->methodNotAllowed();

        $result = $this->citiesGateway->getById($id);

        if (!$result) 
            return $this->notFoundResponse();

        $this->citiesGateway->delete($id);

        return $this->noContent();
    }

    private function validateRequest($input)
    {
        if (isset($input['name']) && isset($input['country']) && isset($input['size']) && isset($input['population']))
            return true;
        return false;
    }

    private function okCode($result)
    {
        $response['status_code_header'] = 'HTTP/1.1 200 OK';
        $response['body'] = json_encode($result);
        return $response;
    }

    private function createdCode($result)
    {
        $response['status_code_header'] = 'HTTP/1.1 201 Created';
        $response['body'] = json_encode($result);
        return $response;
    }

    private function noContent()
    {
        $response['status_code_header'] = 'HTTP/1.1 204 No Content';
        $response['body'] = null;
        return $response;
    }

    private function badRequest()
    {
        $response['status_code_header'] = 'HTTP/1.1 400 Bad Request';
        $response['body'] = null;
        return $response;
    }

    private function notFoundResponse()
    {
        $response['status_code_header'] = 'HTTP/1.1 404 Not Found';
        $response['body'] = null;
        return $response;
    }

    private function methodNotAllowed()
    {
        $response['status_code_header'] = 'HTTP/1.1 405 Method Not Allowed';
        $response['body'] = null;
        return $response;
    }

    private function notImplemented()
    {
        $response['status_code_header'] = 'HTTP/1.1 501 Not Implemented';
        $response['body'] = null;
        return $response;
    }
}

?>