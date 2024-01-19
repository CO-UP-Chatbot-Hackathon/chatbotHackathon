import requests
from flask import request
import cv2
import numpy as np
import base64

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
# content = request.get_json()
# content = content['userRequest']['utterance']
# content = content.replace("\n", "")
content = "WHKJ125"
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
print(img2.shape)
print(img1.shape)

if img1 is None or img2 is None:
    print("이미지를 올바르게 불러오지 못했습니다.")
else:
    # 마스크 생성
    mask = np.full_like(img2, 255)

    # 두 이미지의 중심점 계산
    height, width = img2.shape[:2]
    center = (width // 2, height // 2)

    # 이미지 블렌딩
    normal = cv2.seamlessClone(img2, img1, mask, center, cv2.NORMAL_CLONE)
    mixed = cv2.seamlessClone(img2, img1, mask, center, cv2.MIXED_CLONE)

    # 이미지 크기 조절: 0.2 배율
    resize_normal = cv2.resize(normal, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)
    resize_mixed = cv2.resize(mixed, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR)

    # 두 이미지를 가로로 합성하여 출력
    result = cv2.addWeighted(resize_mixed, 0.6, resize_normal, 0.4, 0)

    # 결과 이미지 표시
    cv2.imwrite('static/images/image.png', result)

image = cv2.imread('static/images/image.png')