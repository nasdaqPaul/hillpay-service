from pydantic import BaseSettings


class DarajaConfig(BaseSettings):
    consumer_key: str = "uMuaemnIASpIFB5C5oW9K9uxPYofMmSl"
    consumer_secret: str = "HY0O0PcH7bh3hCne"
    passkey: str = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    jws_secret: str = 'SomeRandomString'
    daraja_url: str = 'https://sandbox.safaricom.co.ke'
    webhook_url: str = 'https://6b50-41-90-185-2.ngrok.io'

daraja_config = DarajaConfig()
