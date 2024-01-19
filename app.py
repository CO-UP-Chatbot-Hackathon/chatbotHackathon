import os
from flask import Flask, json, request, jsonify
import flask
from openai import OpenAI
import cv2
import requests
import numpy as np
import mysql.connector

My_OpenAI_key = os.environ.get("My_key");

client = OpenAI(api_key=My_OpenAI_key)

def generate_dataSend(text):
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }
    return jsonify(dataSend)


app = Flask(__name__)


@app.route('/message', methods=['POST'])
def Message():
    content = request.get_json()
    content = content['userRequest']['utterance']
    content = content.replace("\n", "")
    print(content)
    dataSend = None
    if content == u"오늘의 메뉴":
        dataSend = generate_dataSend("테스트입니다.")
    elif content == u"수리":
        dataSend = generate_dataSend("수리입니다.")
    else:
        dataSend = generate_dataSend("error입니다.")
    return dataSend


@app.route('/')
def home():
    return 'This is Home!'

@app.route('/glass-cover', methods = ['POST'])
def AI():
    image_dict = {
        "WHKJ101": "https://ifh.cc/g/OxloLj.jpg",
        "WHKJ102": "https://ifh.cc/g/OxloLj.jpg",
        "WHKJ103": "https://ifh.cc/g/lJXGdw.jpg",
        "WHKJ104": "https://ifh.cc/g/lJXGdw.jpg",
        "WHKJ105": "https://ifh.cc/g/21jtfB.jpg",
        "WHKJ106": "https://ifh.cc/g/21jtfB.jpg",
        "WHKJ107": "https://ifh.cc/g/5tYTql.jpg",
        "WHKJ108": "https://ifh.cc/g/5tYTql.jpg",
        "WHKJ109": "https://ifh.cc/g/ch8HL1.jpg",
        "WHKJ110": "https://ifh.cc/g/ch8HL1.jpg",
        "WHKJ111": "https://ifh.cc/g/afYwGk.jpg",
        "WHKJ112": "https://ifh.cc/g/afYwGk.jpg",
        "WHKJ113": "https://ifh.cc/g/TZ0P1P.jpg",
        "WHKJ114": "https://ifh.cc/g/TZ0P1P.jpg",
        "WHKJ115": "https://ifh.cc/g/rQVpGh.jpg",
        "WHKJ116": "https://ifh.cc/g/rQVpGh.jpg",
        "WHKJ117": "https://ifh.cc/g/T0Zzx8.jpg",
        "WHKJ118": "https://ifh.cc/g/T0Zzx8.jpg",
        "WHKJ119": "https://ifh.cc/g/2q0rdL.jpg",
        "WHKJ120": "https://ifh.cc/g/2q0rdL.jpg",
        "WHKJ121": "https://ifh.cc/g/mqL7T6.jpg",
        "WHKJ122": "https://ifh.cc/g/mqL7T6.jpg",
        "WHKJ123": "https://ifh.cc/g/FKB9Cs.jpg",
        "WHKJ124": "https://ifh.cc/g/FKB9Cs.jpg",
        "WHKJ125": "https://ifh.cc/g/nSwXSy.jpg",
        "WHKJ126": "https://ifh.cc/g/nSwXSy.jpg",
        "WHKJ127": "https://ifh.cc/g/cKrtOb.jpg",
        "WHKJ128": "https://ifh.cc/g/cKrtOb.jpg"
    }
    content = request.get_json()
    content = content['userRequest']['utterance']
    content = content.replace("\n", "")
    print(content)
    url = image_dict[content]
    response = requests.get(url)

    # Ensure that the request was successful
    img2 = None
    if response.status_code == 200:
        # Convert the response content to a NumPy array
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)

        # Read the image data using OpenCV
        img2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    img1 = cv2.imread('2.png')
    img2 = cv2.resize(img2, (1000, 1000))
    img1 = img1[500:800, 0:500]
    img2 = img2[500:800, 0:500]
    print(img2.shape)
    print(img1.shape)


    # 마스크 생성
    mask = np.full_like(img2, 255)
    print(1)
    # 두 이미지의 중심점 계산
    height, width = img2.shape[:2]
    center = (width // 2, height // 2)
    print(2)
    # 이미지 블렌딩
    normal = cv2.seamlessClone(img2, img1, mask, center, cv2.NORMAL_CLONE)
    mixed = cv2.seamlessClone(img2, img1, mask, center, cv2.MIXED_CLONE)
    print(3)
    # 이미지 크기 조절: 0.2 배율
    resize_normal = cv2.resize(normal, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
    resize_mixed = cv2.resize(mixed, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
    print(4)
    # 두 이미지를 가로로 합성하여 출력
    result = cv2.addWeighted(resize_mixed, 0.6, resize_normal, 0.4, 0)
    print(5)
    # 결과 이미지 표시
    cv2.imwrite('static/images/image.png', result)
    return generate_dataSend("이미지 생성이 완료되었습니다 \"확인하기\"를 입력하여 이미지를 확인하세요.")

@app.route('/add-photo', methods=['POST', 'GET'])
def add_photo():
    content = request.get_json()
    print(1, content)
    content = content['action']['params']['secureimage']
    print(2, content)
    content = content.split('ist(')[1]
    content = content.split(')\",\"expire\":')[0]
    print(3, content)
    url = content
    response = requests.get(url)

    # Ensure that the request was successful
    img2 = None
    if response.status_code == 200:
        # Convert the response content to a NumPy array
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)

        # Read the image data using OpenCV
        img2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    cv2.imwrite('2.png', img2)
    return generate_dataSend("사진이 업로드 되었습니다.")

@app.route('/image', methods=['GET', 'POST'])
def image_show(): #https://whj.wrslab.app/static/images/image.png
    return flask.render_template('index.html')
@app.route('/check', methods=['POST'])
def check():
    dataSend = {
        "version" : "2.0",
        "template" : {
            "outputs" : [
                {
                    "simpleImage": {
                        "imageUrl" : "https://whj.wrslab.app/static/images/image.png",
                        "altText" : "일시적 오류입니다."
                    }
                }
            ]
        }
    }
    return jsonify(dataSend)
@app.route('/ask-age', methods=['POST'])
def message():
    content = request.get_json()
    content = content['userRequest']['utterance']
    content=content.replace("\n","")
    print(content)
    question = content + ". 저에게 어울리는 안경을 추천해주세요"
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """
    현재 당신(우학정 안경점)은 다음과 같은 안경들을 팔고 있습니다.
    모양    색깔     가격     판매량    모델명     특징
    원형    검정색   110000원  103     WHKJ101    10세~19세 남성 및 여성에게 잘 어울림
    원형    검정색   90000원   127     WHKJ102    10세~19세 남성 및 여성에게 잘 어울림
    원형    금색     210000원  158     WHKJ103    10세 이하 남성에게 잘 어울림
    원형    금색     190000원  204     WHKJ104    10세 이하 남성에게 잘 어울림
    원형    은색     160000원  78      WHKJ105    10세~29세 초반 남성 및 여성에게 잘 어울림
    원형    은색     140000원  96      WHKJ106    10세~29세 초반 남성 및 여성에게 잘 어울림
    원형    남색     130000원  47      WHKJ107    10세~16세 남성에게 잘 어울림
    원형    남색     110000원  59      WHKJ108    10세~16세 남성에게 잘 어울림
    원형    빨간색   190000원  29      WHKJ109    60세 이상 및 10세 이하 남성 및 여성에게 잘 어울림
    원형    빨간색   170000원  53      WHKJ110    60세 이상 및 10세 이하 남성 및 여성에게 잘 어울림
    원형    하얀색   140000원  61      WHKJ111    10세~19세 여성에게 잘 어울림
    원형    하얀색   120000원  72      WHKJ112    10세~19세 여성에게 잘 어울림
    원형    연두색   85000원   7       WHKJ113    10세~19세 여성 및 남성에게 잘 어울림
    원형    연두색   75000원   14      WHKJ114    10세~19세 여성 및 남성에게 잘 어울림
    사각형  검정색   360000원  315     WHKJ115   20세~29세 남성에게 잘 어울림
    사각형  검정색   340000원  389     WHKJ116   20세~29세 남성에게 잘 어울림
    사각형  금색     260000원  122     WHKJ117   30세~49세 남성에게 잘 어울림
    사각형  금색     240000원  143     WHKJ118   30세~49세 남성에게 잘 어울림
    사각형  은색     210000원  237     WHKJ119   30세~49세 남성에게 잘 어울림
    사각형  은색     190000원  261     WHKJ120   30세~49세 남성에게 잘 어울림
    사각형  남색     150000원  42      WHKJ121   20세~29세 남성에게 잘 어울림
    사각형  남색     130000원  51      WHKJ122   20세~29세 남성에게 잘 어울림
    사각형  빨간색   105000원  27      WHKJ123    40세 이상 여성에게 잘 어울림
    사각형  빨간색   95000원   38      WHKJ124    40세 이상 여성에게 잘 어울림
    사각형  하얀색   155000원  68      WHKJ125    10세~19세 남성 및 여성에게 잘 어울림
    사각형  하얀색   145000원  77      WHKJ126    10세~19세 남성 및 여성에게 잘 어울림
    사각형  연두색   95000원   9       WHKJ127    30세~39세 여성에게 잘 어울림
    사각형  연두색   85000원   18      WHKJ128    30세~39세 여성에게 잘 어울림
    """},
            {
                "role": "assistant", "content": "답변은 한 문장이여야 하고 한 개의 모델만 알려줘야 하고, 답변에 모델명과 그에 맞는 모양, 색, 가격에 대한 언급이 있어야합니다."
            },
            {"role": "user", "content": question}
        ]
    )
    gpt_generated_text = str(completion.choices[0].message.content)
    WHKJ_index = gpt_generated_text.find("WHKJ")
    image_dict = {
        "WHKJ101": "https://ifh.cc/g/OxloLj.jpg",
        "WHKJ102": "https://ifh.cc/g/OxloLj.jpg",
        "WHKJ103": "https://ifh.cc/g/lJXGdw.jpg",
        "WHKJ104": "https://ifh.cc/g/lJXGdw.jpg",
        "WHKJ105": "https://ifh.cc/g/21jtfB.jpg",
        "WHKJ106": "https://ifh.cc/g/21jtfB.jpg",
        "WHKJ107": "https://ifh.cc/g/5tYTql.jpg",
        "WHKJ108": "https://ifh.cc/g/5tYTql.jpg",
        "WHKJ109": "https://ifh.cc/g/ch8HL1.jpg",
        "WHKJ110": "https://ifh.cc/g/ch8HL1.jpg",
        "WHKJ111": "https://ifh.cc/g/afYwGk.jpg",
        "WHKJ112": "https://ifh.cc/g/afYwGk.jpg",
        "WHKJ113": "https://ifh.cc/g/TZ0P1P.jpg",
        "WHKJ114": "https://ifh.cc/g/TZ0P1P.jpg",
        "WHKJ115": "https://ifh.cc/g/rQVpGh.jpg",
        "WHKJ116": "https://ifh.cc/g/rQVpGh.jpg",
        "WHKJ117": "https://ifh.cc/g/T0Zzx8.jpg",
        "WHKJ118": "https://ifh.cc/g/T0Zzx8.jpg",
        "WHKJ119": "https://ifh.cc/g/2q0rdL.jpg",
        "WHKJ120": "https://ifh.cc/g/2q0rdL.jpg",
        "WHKJ121": "https://ifh.cc/g/mqL7T6.jpg",
        "WHKJ122": "https://ifh.cc/g/mqL7T6.jpg",
        "WHKJ123": "https://ifh.cc/g/FKB9Cs.jpg",
        "WHKJ124": "https://ifh.cc/g/FKB9Cs.jpg",
        "WHKJ125": "https://ifh.cc/g/nSwXSy.jpg",
        "WHKJ126": "https://ifh.cc/g/nSwXSy.jpg",
        "WHKJ127": "https://ifh.cc/g/cKrtOb.jpg",
        "WHKJ128": "https://ifh.cc/g/cKrtOb.jpg"
    }
    model_num = gpt_generated_text[WHKJ_index:WHKJ_index+7]
    gpt_generated_text = "해당 모델은 [우학정 안경원]에서 직접 착용해보실 수 있습니다.\n" + gpt_generated_text

    url = image_dict[str(model_num)]

    dataSend = {
        "version" : "2.0",
        "template" : {
            "outputs" : [

                {
                    "simpleText" : {
                        "text" : gpt_generated_text
                    }
                },
                {
                    "simpleImage": {
                        "imageUrl" : url,
                        "altText" : "일시적 오류입니다."
                    }
                }
            ]
        }
    }
    print(str(model_num))
    print(image_dict[str(model_num)])
    print(gpt_generated_text)
    return jsonify(dataSend)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bycycle1!",
    auth_plugin="mysql_native_password",
    database="WOOHAKJUNG"
)

mycursor = mydb.cursor(dictionary=True)

@app.route('/membershipId', methods=['POST'])
def membershipId():
    content = request.get_json()
    print("body: ", content)

    user_id = content.get('user_id')

    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"멤버십 아이디 {content['action']['params']['user_id']}를 받았습니다."
                    }
                }
            ]
        }
    }
    return jsonify(dataSend)

# @app.route('/eyeWatch', methods=['POST'])
# def eyeWatch():
#     content = request.get_json()
#     print("body: ", content)

# @app.route('/buy', methods=['POST'])
# def buy():
#     content = request.get_json()
#     print("body: ", content)
#
#     model_name = content.get('model_name')

@app.route('/getPrice', methods=['POST'])
def getPrice():
    content = request.get_json()
    #print("body: ", content)
    model_name = content.get('action', {}).get('params', {}).get('ok_model')
    #print(type(model_name))
    model_name = str(model_name)
    model_name = model_name.split("OK")[1]
    query = f"SELECT price FROM products WHERE model_name = '{model_name}'"
    mycursor.execute(query)
    result = mycursor.fetchone()
    #print("result:", result)
    #print("model_name:", model_name)
    if result:
        price = result['price']
        print("price", price)
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"모델명 {model_name}의 현재 가격은 {price}원 입니다."
                        }
                    }
                ]
            }
        }
        return jsonify(dataSend)
    else:
        return generate_dataSend("error: 해당 제품을 찾을 수 없습니다.")

@app.route('/isMember', methods=['POST'])
def isMember():
    content = request.get_json()
    print("body: ", content)

    user_id = content.get('action', {}).get('params', {}).get('user_id')

    # 여기서부터 추가된 코드
    # 데이터베이스에서 해당 'user_id' 조회
    query = f"SELECT user_name FROM users WHERE user_id = '{user_id}'"
    mycursor.execute(query)
    result = mycursor.fetchone()

    if result:  # 결과가 있으면
        user_name = result['user_name']
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        # "simpleText": {
                        #     "text": f"{user_name}님은 회원입니다."
                        # }
                        "basicCard": {
                            "title": f"{user_name}님은 회원입니다.\n온라인 구매를 진행하실 수 있습니다!✨",
                            "buttons": [
                                {
                                    "label": "온라인 안경 예약하기",
                                    "action": "message",
                                    "messageText": "온라인 예약"
                                },
                                {
                                    "label": "이 주의 Best 안경 테!",
                                    "action": "message",
                                    "messageText": "BEST"
                                }
                                # 여기에 필요한 만큼 버튼을 추가할 수 있습니다
                            ]
                        }
                    }
                ]
            }
        }
    else:  # 결과가 없으면
        dataSend = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": "등록되지 않은 사용자입니다.\n매장에 방문하여 주세요.",
                            "buttons": [
                                {
                                    "label": "무시하고 주문하기",
                                    "action": "message",
                                    "messageText": "는 안됩니다."
                                }
                                # 여기에 필요한 만큼 버튼을 추가할 수 있습니다
                            ]
                        }
                    }
                ]
            }
        }

    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)