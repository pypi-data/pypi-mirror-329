import json
import hashlib
import hmac
from urllib.parse import urlencode, quote_plus
from .encrypt import encrypt


def get_prebuild_form_url(public_key, secretkey, **data):
    value = json.dumps(data)
    # get from checkout-form page
    # encrypt
    encrypted_payload = encrypt(value, public_key=public_key)
    # calculate hash
    hash_value = hmac.new(secretkey.encode("utf-8"), value.encode("utf-8"), hashlib.sha256).hexdigest()
    # send GET request to this final url
    # url = f"https://form.dinger.asia?{urlencode({'payload': encrypted_payload, 'hashValue': hash_value}, quote_via=quote_plus)}"
    return encrypted_payload,hash_value
