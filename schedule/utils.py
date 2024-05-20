import requests
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import datetime
from .models import HospitalSchedule


def save_holidays_from_api():
    # 공휴일 정보 API URL
    url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    api_key_utf8 = "nUgOhG9NcPs00A1y%2BvW6SyDJnFRKYQSev%2FyyPHsi1c7SgU8si2l3myzsAIb%2FFMbmL9rclj7ItCJC0auZlS19yw%3D%3D"
    api_key_decode = unquote(api_key_utf8)

    # 파라미터 설정
    params = {
        "ServiceKey": api_key_decode,
        "solYear": 2024,  # 받아온 연도로 설정
        "numOfRows": 100
    }

    # API 호출 및 응답 처리
    response = requests.get(url, params=params)  # API 요청 보내기
    print("save_holidays_from_api")

    if response.status_code == 200:  # 요청 성공 여부 확인
        root = ET.fromstring(response.text)  # XML 데이터 파싱

        # 공휴일 정보 추출
        items = root.findall('.//item')

        for item in items:
            date = item.find('locdate').text  # 공휴일 날짜를 XML에서 추출
            date_name = item.find('dateName').text  # 공휴일 설명을 XML에서 추출

            # 문자열 형식의 날짜를 datetime 객체로 변환
            date = datetime.datetime.strptime(date, '%Y%m%d').date()
            print("date: ", date)

            # 중복 저장 방지를 위해 이미 저장된 공휴일인지 확인 후 저장
            if not HospitalSchedule.objects.filter(date=date, date_name=date_name).exists():
                # 모델에 맞게 공휴일 정보 저장
                HospitalSchedule.objects.create(
                    date=date, date_name=date_name, is_holiday=True)

            else:
                print("Error: 이미 지정된 (공)휴일 입니다", response.status_code,
                      response.text)  # 오류 메시지 출력


def sync_schedules_with_holidays():
    holidays = HospitalSchedule.objects.filter(is_holiday=True)  # 공휴일 필터링
    for holiday in holidays:
        # 이미 저장된 공휴일인지 확인 후 동기화
        if not HospitalSchedule.objects.filter(date=holiday.date, date_name=holiday.date_name, is_holiday=True).exists():
            HospitalSchedule.objects.create(
                date=holiday.date, date_name=holiday.date_name, is_holiday=True)
