# 🏥AIBoot-Project-MEDI BRIDGE

병원 정보 시스템 (Hospital Information System, HIS) 
[![Video Label](https://github.com/quasar2yh/KHIS/assets/58003233/51c0dc9b-077e-49b2-b1b6-7b61dfa6911e
)](https://www.youtube.com/watch?v=_F9465J8xnk)

<br><br>

## 🖥프로젝트 소개

**메디 브릿지**는 EMR (Electronic Medical Record, **전자 의무 기록**), OCS(Order Communication System, **오더 커뮤니케이션 시스템**), 병원 편의 기능을 하나로 통합한 표준화된 병원 정보 시스템입니다. 의료 빅데이터 활용을 위한 기반을 마련하고**AI**를 활용하여, 파편화된 기존 의료 시스템의 문제를 해결할 수 있는 더 효율적이고 정밀한 의료 서비스를 제공합니다. 

<br><br>


## 🕰개발 기간

* 24.05.13일 - 24.06.13일(32 일)

<br><br>


## 🧑‍🤝‍🧑팀원구성

 - 팀장  : 이윤후 -  프로젝트 전반 기획/설계/관리, 수납 청구(CRUD) , AWS 배포
 - 부팀장 : 현효민 - DB 설계 및 구현, 회원관리(CRUD), 의료진 진료 기록(CRUD), React 프론트엔드 전반 개발 및 관리 
 - 팀원: 이훈희 - 환자 진료 예약 (CRUD) , 예약가능한 환자조회 , 채팅 기능 , React 개발 , Deepl 번역기 ,Account조회(통합유저정보)
 - 팀원: 안채연 - API 설계, 의료진 및 병원 스케줄 관리(CRUD), 메일 비동기 처리, 진료과 상담 AI챗봇, React 개발

<br><br>


## ⚒ 개발 환경

**Environment**

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

**Config**

![npm](https://img.shields.io/badge/npm-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white)
![Yarn](https://img.shields.io/badge/yarn-%232C8EBB.svg?style=for-the-badge&logo=yarn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


**Development**

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23009272.svg?style=for-the-badge&logo=celery&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![OpenAI](https://img.shields.io/badge/OpenAI-%234EA94B.svg?style=for-the-badge&logo=openai&logoColor=white)
![DeepL](https://img.shields.io/badge/DeepL-%23009272.svg?style=for-the-badge&logo=deepl&logoColor=white)



**Communication**

![Slack](https://img.shields.io/badge/slack-%230075B5.svg?style=for-the-badge&logo=slack&logoColor=white)
![Notion](https://img.shields.io/badge/notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)
![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)


<br><br>


## 📌 주요 기능


**EMR (진료 기록관련)**

-[환자 데이터 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/registration/views.py)

-[진단기록 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/ocs/views.py#L12)

-[수술기록 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/ocs/views.py#L44)


**수납 시스템**

-[청구 항목 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/acceptance/views.py)


**수술,수술 요금**

-[수술 요금 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/procedure_fee/views.py)

-[수술 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/procedure/views.py#L13)
 

**연차/휴일 시스템**

-[연차신청 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/schedule/views.py)

-[병원 자체 휴일 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/schedule/views.py#L156)

-[공휴일 조회](https://github.com/quasar2yh/KHIS/blob/dev/schedule/views.py#L200) 

-[부서별 일정 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/schedule/views.py#L324)


**예약 및 시스템**

-[예약, 예약가능한의사 조회, Deepl 연결 CRUD](https://github.com/quasar2yh/KHIS/blob/dev/appointment/views.py#L27)

-[진료과 추천 AI](https://github.com/quasar2yh/KHIS/blob/dev/appointment/open_ai.py)


**대기열 시스템**

[의료진 관련](https://github.com/quasar2yh/KHIS/blob/dev/practitioner_registration/views.py)

[의료진 데이터 CRU](https://github.com/quasar2yh/KHIS/blob/dev/practitioner_registration/views.py)

**채팅 시스템**

[채팅 기능](https://github.com/quasar2yh/KHIS/blob/dev/chat/views.py)
<br><br>

## ⚙프로젝트 아키텍쳐

![기술 다이어그램](https://github.com/quasar2yh/KHIS/assets/58003233/e4bc8e5f-7806-4751-931e-54067357862a)

<br><br>

## ERD (Entity-Relationship Diagram)
[![EMR](https://github.com/quasar2yh/KHIS/assets/159987685/ee4c5547-29ef-4249-a4b0-06ff403ad469)](https://www.erdcloud.com/d/WMitesP6FrntKxh4Z)

<br><br>

## API 명세서

<a href="https://holy-rose-f0a.notion.site/API-_-RESTful-API-4cd40b87dc1d4d6aad7c3b81e37a78ca">
    <img src="https://github.com/quasar2yh/KHIS/assets/58003233/2273653e-ca81-47ad-9d63-b7471b9f5724" alt="API 명세서" width="180" height="40">
</a>

<br><br>


## 요구 명세서

<a href="https://docs.google.com/spreadsheets/d/1ygR2d3qv8T-GOCpKKjD7No1jeWYWcizmtUxoSVP73N4/edit?gid=1333301150#gid=1333301150">
    <img src="https://github.com/quasar2yh/KHIS/assets/58003233/a3801ebe-e2e4-42a8-a41c-01894045f794" alt="요구 명세서" width="180" height="40">
</a>

<br><br>
## 5분 이슈보드
<a href="https://docs.google.com/spreadsheets/d/1ygR2d3qv8T-GOCpKKjD7No1jeWYWcizmtUxoSVP73N4/edit?gid=1333301150#gid=1333301150">
    <img src="https://www.notion.so/5-0d9a013a1224470f98a2b441f1821120" alt="5분 이슈보드 노션ver" width="180" height="40">
</a>
<a href="https://docs.google.com/spreadsheets/d/1ygR2d3qv8T-GOCpKKjD7No1jeWYWcizmtUxoSVP73N4/edit?gid=1333301150#gid=1333301150">
    <img src="https://github.com/users/quasar2yh/projects/3" alt="5분 이슈보드 깃허브ver" width="180" height="40">
</a>





