from openai import OpenAI
# from django.conf import settings
import os

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)


def chatgpt(user_message):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "너는 환자들의 증상을 토대로 진료과를 추천해주는 병원 상담원이야. 우리 병원에는 내과, 외과, 피부과, 정형외과 이렇게 4가지 진료부서가 있어. 만약에 앞서 말한 네가지 부서에 적합하지 않는 증상이라면, 다른 병원의 진료과를 추천해줘 "
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return completion.choices[0].message.content
