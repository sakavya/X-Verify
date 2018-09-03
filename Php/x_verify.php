//This script generates Base64 and SHA256 encrypted data for given path, Merchant Key and Request

<?php
/**
* params - $path - String
*          $merchantKey given by phonepe - String
*          $keyIndex given by phonepe - String
*          $request - String
*/
function generateXVerify($path, $merchantKey, $keyIndex, $request) {
    // base64 encryption
    $base64_encode = base64_encode($request);
    $payload = "{\"request:\"". "\"" .$base64_encode . "\""."}";
    // input for sha256
    $sha256_input = $base64_encode . $path . $merchantKey;

    //sha256 encryption
    $sha256_output = hash('sha256', $sha256_input);

    //x-verify header
    $x_verify = $sha256_output . "###" . $keyIndex;
    
    // adding to an object
    $data = [];
    $data["Given Request"]= $request;
    $data["Base64Encoded"]= $base64_encode;
    $data["Payload should be"]= "{\"request\": \"BASE64 of Request\"}";
    $data["Payload"]= $payload;
    $data["SHA256 Input"]= "BASE64 of request + API + Merchant Key";
    $data["Sha256Input"]= $sha256_input;
    $data["Sha256Output"]= $sha256_output;
    $data["X-Verify"]= "Sha256 Output +" . " ### + " . "KeyIndex";
    $data["X_verify"]= $x_verify;

    //returning object
    return $data;
}

// program start from here
// Request payload, transactionId should be different for each call
$request = <<<EOT
{
    "merchantId": "M2306160483220675579140",
    "transactionId": "TX20180827105520",
    "amount": 200,
    "merchantOrderId": "OD1234656",
    "merchantOrderContext": {
        "tid": "TX123456789"
    },
    "quantity": 1,
    "mobileNumber": "9xxxxxxxx",
    "validFor": 180,
    "fareDetails": {
        "category": "MOVIE",
        "fareBreakup": [{
            "fareType": "TOTAL_FARE",
            "amount": 500
        }]
    },
    "cartDetails": {
        "cartItem": {
            "category": "MOVIE",
            "itemId": "XVGSDA3",
            "movieName": "The Avengers",
            "format": "IMAX(3D)",
            "language": "English",
            "imageUrl": "https://pre00.deviantart.net/7025/th/pre/i/2016/259/1/b/avengers__infinity_war_poster__2_by_bakikayaa-dahtubc.jpg",
            "screenDetails": {
                "screenNo": "Audi 2",
                "venue": "PVR Koramangala, Bangalore",
                "seats": [{
                    "seatNo": "B12",
                    "seatType": "GOLD",
                    "seatPrice": 100
                }],
                "date": "22-03-2018 10:19:56"
            },
            "addOns": [{
                "addonType": "FANDB",
                "itemName": "PopCorn Pepsi Combo",
                "quantity": 1,
                "price": 200
            }]
        }
    }
}
EOT;
    // calling encryption()
    $result = generateXVerify("/v3/service/initiate", "48b7228c-605e-4bab-9632-5bf9e61e8b75", "2", $request);
    foreach($result as $x=>$x_value)
      {
      echo $x . " = " . $x_value . "\r\n";
      }
    echo strcmp($result["Sha256Output"], "8bb3c9e60235e02e533b7d112859d8d51ef835f704450414e7c9857898c9e491");

?>
