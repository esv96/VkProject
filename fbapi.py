import requests


class FBApi:
    @staticmethod
    def get_share_count(url: str) -> int:
        res = requests.get("https://graph.facebook.com",
                           params={'id': url, 'access_token': '1235602329852571|GSIboWHuaEJcxZ-rKDFQMaT-guY'})
        json = res.json()
        if 'share' in json:
            count = json['share']['share_count']
        else:
            count = 0
        return count
