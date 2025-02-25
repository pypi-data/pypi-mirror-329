import base64
import hashlib
import hmac
import time
import uuid
from urllib.parse import quote, urlencode

from connector.generated import OAuth1Credential
from connector.oai.capability import Request, get_oauth_1


def create_oauth1_signature(
    method: str, url: str, params: dict[str, str], auth: OAuth1Credential
) -> str:
    """Generate HMAC-SHA256 OAuth 1.0 signature."""
    sorted_params = urlencode(sorted(params.items()), safe="~")
    base_string = "&".join([method.upper(), quote(url, safe=""), quote(sorted_params, safe="")])

    signing_key = f"{quote(auth.consumer_secret)}&{quote(auth.token_secret)}"
    signature = hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


def get_oauth1_headers(method: str, url: str, args: Request) -> dict[str, str]:
    """Generate OAuth 1.0 headers for HTTPX."""
    auth = get_oauth_1(args)

    nonce = str(uuid.uuid4())
    timestamp = str(int(time.time()))

    oauth_params = {
        "oauth_consumer_key": auth.consumer_key,
        "oauth_token": auth.token_id,
        "oauth_nonce": nonce,
        "oauth_timestamp": timestamp,
        "oauth_signature_method": "HMAC-SHA256",
        "oauth_version": "1.0",
    }

    oauth_signature = create_oauth1_signature(method, url, oauth_params, auth)
    oauth_params["oauth_signature"] = oauth_signature

    # Format the Authorization header
    auth_header = "OAuth " + ", ".join(f'{quote(k)}="{quote(v)}"' for k, v in oauth_params.items())
    return {"Authorization": auth_header}
