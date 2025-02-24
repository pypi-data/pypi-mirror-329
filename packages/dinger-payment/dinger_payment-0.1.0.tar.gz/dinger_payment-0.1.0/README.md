# Dinger Prebuild Checkout From for URL

## Usage

```python
import json
from urllib.parse import urlencode, quote_plus

from dinger_payment import get_prebuild_form_url

if __name__ == '__main__':
    items = [
        {"name": "DiorAct Sandal", "amount": 250, "quantity": 1},
        {"name": "Aime Leon Dore", "amount": 250, "quantity": 1},
    ]
    data = {
        # items must be string
        "items": json.dumps(items),
        "customerName": "James",
        "totalAmount": 500,
        "merchantOrderId": "123456",
        # get from checkout-form page
        "clientId": "6ecf9792-f093-369e-bb25-ec5c2702c5f4",
        # get from data-dashboard page
        "publicKey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCucqVPf8TB71ZAHRxcJE9Ac2AknmLwJmoqZ5FxB7+vfe6Gsg7dFfegMCrl29P3vLp58rpzLl436RHr8/RSymsiJWI8ARpc26oPWAXgmx6P7LtdyYw7R8GrHhq8o8jTGnNA0oHbptlbLIxSlLHmLXUlSUj7T+PlQd4HQ3E4jANPBQIDAQAB",
        # get from data-dashboard page
        "merchantKey": "mhgsnvm.89_wMpuTVA9yecHyUr4aMibvbIU",
        # your project name
        "projectName": "prebuilt-test-2",
        # your account username
        "merchantName": "Jamesssy",
        "email": "misterjames.thiha@gmail.com",
        "billCity": "city",
        "billAddress": "address",
        "state": "state",
        "country": "MM",
        "postalCode": "15015",
    }
    secretkey = "1be2e692d3a1d80b8e9e3e665028b6f7"
    public_key = "-----BEGIN PUBLIC KEY-----\n"\
    + "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFD4IL1suUt/TsJu6zScnvsEdLPuACgBdjX82QQf8NQlFHu2v/84dztaJEyljv3TGPuEgUftpC9OEOuEG29z7z1uOw7c9T/luRhgRrkH7AwOj4U1+eK3T1R+8LVYATtPCkqAAiomkTU+aC5Y2vfMInZMgjX0DdKMctUur8tQtvkwIDAQAB"\
    + "\n-----END PUBLIC KEY-----"
    encrypted_payload, hash_value = get_prebuild_form_url(public_key=public_key, secretkey=secretkey, **data)
    url = f"https://form.dinger.asia?{urlencode({'payload': encrypted_payload, 'hashValue': hash_value}, quote_via=quote_plus)}"
    print(url)
```