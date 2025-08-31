import requests
import time
import hmac
import hashlib
from env_manager.env_manager import BINGX_API_KEY, BINGX_SECRET_KEY


class BingXClient:
    def __init__(self, is_demo):
        self.base_url = "https://open-api-vst.bingx.com" if is_demo else "https://open-api.bingx.com"

    def get_signature(self, payload, secret_key):
        """Generate HMAC signature for API authentication"""
        signature = hmac.new(secret_key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return signature

    def make_request(self, method, path, params=None):
        """Send authenticated request to BingX API"""
        params["timestamp"] = str(int(time.time() * 1000))
        query_string = "&".join(f"{key}={value}" for key, value in sorted(params.items()))
        signature = self.get_signature(query_string, BINGX_SECRET_KEY)
        url = f"{self.base_url}{path}?{query_string}&signature={signature}"
        headers = {"X-BX-APIKEY": BINGX_API_KEY}
        response = requests.request(method, url, headers=headers)
        return response.json()

    def get_account_balance(self):
        """Get current USDT balance"""
        path = "/openApi/swap/v3/user/balance"
        params = {}
        response = self.make_request("GET", path, params)

        if response.get("code") == 0:
            for item in response["data"]:
                if item.get("asset") == "USDT":
                    return float(item["balance"])
        else:
            print("Error fetching balance:", response)
        return 0.0
