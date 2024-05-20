import xml.etree.ElementTree as ET
from urllib import parse
import requests
import datetime
from .models import Holiday


# API로부터 공휴일 데이터를 가져와서 데이터베이스에 저장


def save_holidays_from_api():
    url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    api_key_utf8 = "nUgOhG9NcPs00A1y%2BvW6SyDJnFRKYQSev%2FyyPHsi1c7SgU8si2l3myzsAIb%2FFMbmL9rclj7ItCJC0auZlS19yw%3D%3D"
    api_key_decode = parse.unquote(api_key_utf8)

    params = {
        "ServiceKey": api_key_decode,
        "solYear": 2021,
        "numOfRows": 100
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        items = root.findall('.//item')

        for item in items:
            date_str = item.find('locdate').text
            name = item.find('dateName').text

            # 날짜 문자열을 datetime 객체로 변환
            date = datetime.datetime.strptime(date_str, '%Y%m%d').date()

            # 이미 저장된 공휴일인지 확인하여 중복 저장 방지
            if not Holiday.objects.filter(date=date).exists():
                Holiday.objects.create(date=date, name=name)
    else:
        print("Error:", response.status_code, response.text)
