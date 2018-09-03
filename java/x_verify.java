import java.util.*;
import java.security.MessageDigest;


public class Encryption
{
    /*
     * @params - path - String
     * @params - merchantKey - Key given by phonepe - String
     * @params - keyIndex - Index of given Key
     * @ params - request - payload - String
     *
     * @return - map of generated values
     */
    public static LinkedHashMap<String, String> generateXVerify(String path, String merchantKey, String keyIndex, String request)
    {
        LinkedHashMap<String, String>map = new LinkedHashMap<>();

        try {
            // base 64 encryption
            String base64Encode = Base64.getEncoder().encodeToString(request.toString().getBytes("utf-8"));

            // complete payload
            String payload = "{\"request\":" + "\"" + base64Encode + "\"" + "}";

            // inputs for sha256 hashing
            String sha256Input = base64Encode + path + merchantKey;

            // sha256 hashing
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            digest.update(sha256Input.getBytes());
            byte[] dataBytes = digest.digest();
            StringBuffer sb = new StringBuffer();
            for (int i = 0; i < dataBytes.length; i++) {
                sb.append(Integer.toString((dataBytes[i])).substring(1));
            }
            StringBuffer hexString = new StringBuffer();
            for (int i=0;i<dataBytes.length;i++) {
                String hex=Integer.toHexString(0xff & dataBytes[i]);
                if(hex.length()==1) hexString.append('0');
                hexString.append(hex);
            }
            String sha256Output = hexString.toString();

            // adding values to map
            map.put("Given Request", request);
            map.put("Base64Encoded", base64Encode);
            map.put("Payload should be {\"request\"", "\"BASE64 of Request\"}");
            map.put("Payload", payload);
            map.put("Sha256 Input", "BASE64 of request + API + Merchant Key");
            map.put("Sha256Input", sha256Input);
            map.put("Sha256Output", sha256Output);
            map.put("x-Verify", "Sha256 Output + ### + Key Index");
            map.put("X-Verify", sha256Output + "###" + keyIndex);

        }catch(Exception ex)
        {
            System.out.println(ex);
        }

        //returning map
        return map;
    }

    public static void main(String[] args)
    {
        String request = "{\"merchantId\": \"M2306160483220675579140\"," +
                "\"transactionId\": \"TX20180827123012\"," +
                "\"amount\": 200,"+
                "\"merchantOrderId\": \"OD1234656\"," +
                "\"merchantOrderContext\": {" +
                "\"tid\": \"TX123456789\"" +
                "}," +
                "\"quantity\": 1," +
                "\"mobileNumber\": \"9xxxxxxxx\"," +
                "\"validFor\": 180," +
                "\"fareDetails\": {" +
                "\"category\": \"MOVIE\","+
                "\"fareBreakup\": [{" +
                "\"fareType\": \"TOTAL_FARE\"," +
                "\"amount\": 500" +
                "}]" +
                "}," +
                "\"cartDetails\": {" +
                "\"cartItem\": {" +
                "\"category\": \"MOVIE\"," +
                "\"itemId\": \"XVGSDA3\"," +
                "\"movieName\": \"The Avengers\"," +
                "\"format\": \"IMAX(3D)\","+
                "\"language\": \"English\"," +
                "\"imageUrl\": \"https://pre00.deviantart.net/7025/th/pre/i/2016/259/1/b/avengers__infinity_war_poster__2_by_bakikayaa-dahtubc.jpg\"," +
                "\"screenDetails\": {" +
                "\"screenNo\": \"Audi 2\"," +
                "\"venue\": \"PVR Koramangala, Bangalore\"," +
                "\"seats\": [{" +
                "\"seatNo\": \"B12\"," +
                "\"seatType\": \"GOLD\"," +
                "\"seatPrice\": 100" +
                "}]," +
                "\"date\": \"22-03-2018 10:19:56\"" +
                "}," +
                "\"addOns\": [{" +
                "\"addonType\": \"FANDB\"," +
                "\"itemName\": \"PopCorn Pepsi Combo\"," +
                "\"quantity\": 1," +
                "\"price\": 200" +
                "}]" +
                "}" +
                "}" +
                "}";

        LinkedHashMap<String, String> map = new LinkedHashMap<>();

        // calling generateXVerify()
        map = generateXVerify("/v3/service/initiate", "48b7228c-605e-4bab-9632-5bf9e61e8b75", "2", request);
        map.forEach((key, value) -> {
            System.out.println(key +":"+ value);
        });
        // comparing generated sha256 hashing with expected value
        System.out.println (map.get("Sha256Output").equals("e5ae534a69cda6d153ad305aaa34ce4c243bf7f1944a238cf3ccc58634f4a551"));
    }
}
