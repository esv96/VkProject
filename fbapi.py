import requests


class FBApi:
    @staticmethod
    def get_share_count(url: str) -> int:
        res = requests.get("http://graph.facebook.com", params={'id': url})
        json = res.json()
        if 'share' in json:
            count = json['share']['share_count']
        else:
            count = 0
        return count
