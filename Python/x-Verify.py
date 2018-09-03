# This script generates Base 64 and SHA 256 encrypted values for given Path, Merchant Key, Key Index and Payload and
# compare expected value with generated value.

import base64
import hashlib
import json
import requests


# Function to generate Base64 and SHA 256 encrypted values
# Params - Path - String,
#          Merchant Key - String,
#          Merchant Key Index - String,
#          Payload - Json request - String
def generateXVerify(path, merchant_key, key_index, request):
    data = {}
    url = "https://mercury-uat.phonepe.com/v3/service/initiate"

    # Base 64 encryption
    base64_encode = base64.b64encode(request.encode('utf-8')).decode('utf-8')

    payload = "{\"request\":" + "\"" + base64_encode + "\"" + "}"

    # Inputs for sha256 encryption
    sha256_input = base64_encode + path + merchant_key

    # sha256 encryption
    sha256_output = \
        hashlib.sha256(sha256_input.encode('utf-8')).hexdigest()

    headers = {
        'content-type': "application/json",
        'x-verify': sha256_output + "###2",
        'x-tracking-url': "http://www.phonepe.com",
        'x-callback-url': "http://www.phonepe.com"
    }
    # adding values to dict
    data["Given Request"] = request
    data["Base64Encoded"] = base64_encode
    data["Payload should be {\"request\""] = "\"BASE64 of Request}\""
    data["Payload"] = payload
    data["Sha256 Input"] = "BASE64 of request + API + Merchant Key"
    data["Sha256Input"] = sha256_input
    data["Sha256 Output"] = sha256_output
    data["X-Verify"] = "Sha256 Output + ### + Key Index"
    data["x-verify"] = sha256_output + "###2"

    # returning dict
    return data


if __name__ == '__main__':
    request = """
    {
    "merchantId": "M2306160483220675579140",
    "transactionId": "TX20180820030134",
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
}""".strip()

    # expected values
    expected_base64 = "eyJtZXJjaGFudElkIjogIk0yMzA2MTYwNDgzMjIwNjc1NTc5MTQwIiwidHJhbnNhY3Rpb25JZCI6ICJUWDExMTExNzU0OTg1MyIsImFtb3VudCI6IDIwMCwibWVyY2hhbnRPcmRlcklkIjogIk9EMTIzNDY1NiIsIm1lcmNoYW50T3JkZXJDb250ZXh0IjogeyJ0aWQiOiAiVFgxMjM0NTY3ODkifSwicXVhbnRpdHkiOiAxLCJtb2JpbGVOdW1iZXIiOiAiOXh4eHh4eHh4IiwidmFsaWRGb3IiOiAxODAsImZhcmVEZXRhaWxzIjogeyJjYXRlZ29yeSI6ICJNT1ZJRSIsImZhcmVCcmVha3VwIjogW3siZmFyZVR5cGUiOiAiVE9UQUxfRkFSRSIsImFtb3VudCI6IDUwMH1dfSwiY2FydERldGFpbHMiOiB7ImNhcnRJdGVtIjogeyJjYXRlZ29yeSI6ICJNT1ZJRSIsIml0ZW1JZCI6ICJYVkdTREEzIiwibW92aWVOYW1lIjogIlRoZSBBdmVuZ2VycyIsImZvcm1hdCI6ICJJTUFYKDNEKSIsImxhbmd1YWdlIjogIkVuZ2xpc2giLCJpbWFnZVVybCI6ICJodHRwczovL3ByZTAwLmRldmlhbnRhcnQubmV0LzcwMjUvdGgvcHJlL2kvMjAxNi8yNTkvMS9iL2F2ZW5nZXJzX19pbmZpbml0eV93YXJfcG9zdGVyX18yX2J5X2Jha2lrYXlhYS1kYWh0dWJjLmpwZyIsInNjcmVlbkRldGFpbHMiOiB7InNjcmVlbk5vIjogIkF1ZGkgMiIsInZlbnVlIjogIlBWUiBLb3JhbWFuZ2FsYSwgQmFuZ2Fsb3JlIiwic2VhdHMiOiBbeyJzZWF0Tm8iOiAiQjEyIiwic2VhdFR5cGUiOiAiR09MRCIsInNlYXRQcmljZSI6IDEwMH1dLCJkYXRlIjogIjIyLTAzLTIwMTggMTA6MTk6NTYifSwiYWRkT25zIjogW3siYWRkb25UeXBlIjogIkZBTkRCIiwiaXRlbU5hbWUiOiAiUG9wQ29ybiBQZXBzaSBDb21ibyIsInF1YW50aXR5IjogMSwicHJpY2UiOiAyMDB9XX19fQ=="
    expected_sha256 = "68bdbe35e199073e7b1b61013a44906d99a04ce70bd9aaffc75da0d3567f4c73"

    response = generateXVerify("/v3/service/initiate", "48b7228c-605e-4bab-9632-5bf9e61e8b75", "2", request)
    print("{" + "\n".join("{}: {}".format(k, v) for k, v in response.items()) + "}")

    # Comparing expected values with generated values
    print (response.get("Sha256 Output") == expected_sha256)
