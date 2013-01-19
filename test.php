<?php
/**
 * This class handles API-communation
 */
class ApiServer {
    /**
     * Makes an HTTP GET-request
	 *
	 * @param string $url Specifies url to call
	 * @param array $vars Sets request parameters
	 * @param boolean $raw Whether or not to return raw response.
	 */
    public static function get ($url, $vars = array(), $raw = false) {
        // Build URL
        if (!empty($vars)) {
            $url .= (stripos($url, '?') !== false) ? '&' : '?';
            $url .= (is_string($vars)) ? $vars : http_build_query($vars, '', '&');
        }

        // Send request
        return self::request('GET', $url, null, $raw);
    }
    
    /**
     * Makes an HTTP POST-request
     *
	 * @param string $url Specifies url to call
	 * @param array $vars Sets request parameters
	 * @param boolean $raw Whether or not to return raw response.
	 */
    public static function post ($url, $vars = array(), $raw = false) {
        // Send request
        return self::request('POST', $url, $vars, $raw);
    }
    
    /**
     * Makes an HTTP PUT-request
     *
	 * @param string $url Specifies url to call
	 * @param array $vars Sets request parameters
	 * @param boolean $raw Whether or not to return raw response.
	 */
    public static function put ($url, $vars = array(), $raw = false) {    
        // Send request
        return self::request('PUT', $url, $vars, $raw);
    }
    
    /**
     * Makes an HTTP DELETE-request
     *
	 * @param string $url Specifies url to call
	 * @param array $vars Sets request parameters
	 * @param boolean $raw Whether or not to return raw response.
	 */
    public static function delete ($url, $vars = array(), $raw = false) {
        // Send request
        return self::request('DELETE', $url, $vars, $raw);
    }
    
    /**
     * Makes the actual request
     *
     * @param string $method Specifies request method
	 * @param string $url Specifies url to call
	 * @param array $vars Sets request parameters
	 * @param boolean $raw Whether or not to return raw response.
	 */
    private static function request ($method, $url, $vars = array(), $raw) {        
        // Initialize CURL
        $request = curl_init();
        
        // Set URL
        curl_setopt($request, CURLOPT_URL, APISERVER_HOST . $url);
        
        // Loop through vars and unset empty values
        if(count($vars)) {
            foreach($vars as $key => $value) {
                if(empty($value)) unset($vars[$key]);
            }
        }
        
        // Handle method
        switch (strtoupper($method)) {
            case 'HEAD':
                if (is_array($vars)) $vars = http_build_query($vars, '', '&');
                curl_setopt($request, CURLOPT_NOBODY, true);
                break;
            case 'GET':
                if (is_array($vars)) $vars = http_build_query($vars, '', '&');
                curl_setopt($request, CURLOPT_HTTPGET, true);
                break;
            case 'POST':
                if (is_array($vars)) $vars = json_encode($vars);
                curl_setopt($request, CURLOPT_POST, true);
                break;
            default:
                if (is_array($vars)) $vars = json_encode($vars);
                curl_setopt($request, CURLOPT_CUSTOMREQUEST, $method);
        }
        
        // Set fields
        if (!empty($vars)) curl_setopt($request, CURLOPT_POSTFIELDS, $vars);
        
        // Set headers
        curl_setopt($request, CURLOPT_HTTPHEADER, array('Content-Type: application/json','Content-Length: ' . strlen($vars)));
        
        // Return transfer
        curl_setopt($request, CURLOPT_RETURNTRANSFER, true);
        
        // Set password and username
        curl_setopt($request, CURLOPT_HTTPAUTH, CURLAUTH_DIGEST); 
        curl_setopt($request, CURLOPT_USERPWD, APISERVER_USERNAME . ':' . APISERVER_PASSWORD);
        
        // Set timeout to 2000 ms
        curl_setopt($request, CURLOPT_TIMEOUT_MS, 2000);
        
        // Send request
        $response = curl_exec($request);
        
        // Get HTTP status code
        $http_status = curl_getinfo($request, CURLINFO_HTTP_CODE);
        
        // Close curl
        curl_close($request);
        
        // Handle raw output
        if($raw) return $response;
        
        // JSON-decode
        $response = json_decode($response, true);
        
        // Return response
        return ($response) ? $response : (($http_status == 200) ? true : false);
    }
}

// Configuration
define('APISERVER_HOST',        'http://api.ru.istykker.dk/');
define('APISERVER_USERNAME',    'hackathon');
define('APISERVER_PASSWORD',    '179d50c6eb31188925926a5d1872e8117dc58572');

// Get profile
$profile = ApiServer::get(sprintf('profile/%s', '320002'));
var_dump($profile);


