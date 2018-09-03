/**
 * This script generates Base64 and SHA256 encryption and compares with expected values.
 */

var buffer = require("buffer");
const crypto = require('crypto');

/**
 * Function to generate Base64 and SHA256 encryption for given path, merchant key and request.
 * @param path - String 
 * @param merchantKey - String
 * @param keyIndex - String
 * @param request - Json- String
 * @returns Object
 */
var generateXVerify = function(path, merchantKey, keyIndex, request)
{
    // Base 64 encryption
    var base64Encoded = Buffer.from(request).toString('base64');

    // complete payload
    payload = "{\"request\":" + "\"" + base64Encoded + "\"" + "}";

    // Input for sha256 encryption
    sha256Input = base64Encoded + path + merchantKey;

    // SHA256 encryption
    const hash = crypto.createHash("sha256")
    sha256Data = (hash.update(sha256Input).digest('hex'))

    // adding values into an object
    var encryption = {
        "Given Request":request,
        Base64Encoded: base64Encoded,
        "Payload should be \"{request\"": "\"BASE64 of Request}\"",
        Payload: payload,
        "Sha256 Input": "BASE64 of request + API + Merchant Key",
        sha256Input: sha256Input,
        sha256Output: sha256Data,
        "X-Verify": "Sha256 Output + ### + Key Index",
        xVerify: sha256Data + "###" + keyIndex
    }
    return encryption

}

// Request payload, Transaction Id shoulbe be different for every call
var request = `
{
    "merchantId": "M2306160483220675579140",
    "transactionId": "TX20180827095812",
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
`.trim(); 
// calling  generateXVerify()   
response = generateXVerify("/v3/service/initiate", "48b7228c-605e-4bab-9632-5bf9e61e8b75", "2", request);
console.log(response);
console.log(response.xVerify === "fe2e625fca574eead548243bb9bfa54d3cec19adf34f94b5df99ce5857d09fa0###2")
