#분류 결과 + 이미지 + 텍스트와 함께 분류 결과에 따라 다른 출력 보여주기
#파일 이름 streamlit_app.py
import streamlit as st
from fastai.vision.all import *
from PIL import Image
import gdown

# Google Drive 파일 ID
file_id = '1WgL-eqnQptxSQFWbKvH8s1kxY5KpXQhQ'

# Google Drive에서 파일 다운로드 함수
@st.cache(allow_output_mutation=True)
def load_model_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.pkl'
    gdown.download(url, output, quiet=False)

    # Fastai 모델 로드
    learner = load_learner(output)
    return learner

def display_left_content(image, prediction, probs, labels):
    st.write("### 왼쪽: 기존 출력 결과")
    if image is not None:
        st.image(image, caption="업로드된 이미지", use_column_width=True)
    st.write(f"예측된 클래스: {prediction}")
    st.markdown("<h4>클래스별 확률:</h4>", unsafe_allow_html=True)
    for label, prob in zip(labels, probs):
        st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 5px; padding: 5px; margin: 5px 0;">
                <strong style="color: #333;">{label}:</strong>
                <div style="background-color: #d3d3d3; border-radius: 5px; width: 100%; padding: 2px;">
                    <div style="background-color: #4CAF50; width: {prob*100}%; padding: 5px 0; border-radius: 5px; text-align: center; color: white;">
                        {prob:.4f}
                    </div>
                </div>
        """, unsafe_allow_html=True)

def display_right_content(prediction, data):
    st.write("### 오른쪽: 동적 분류 결과")
    cols = st.columns(3)

    # 1st Row - Images
    for i in range(3):
        with cols[i]:
            st.image(data['images'][i], caption=f"이미지: {prediction}", use_column_width=True)
    # 2nd Row - YouTube Videos
    for i in range(3):
        with cols[i]:
            st.video(data['videos'][i])
            st.caption(f"유튜브: {prediction}")
    # 3rd Row - Text
    for i in range(3):
        with cols[i]:
            st.write(data['texts'][i])

# 모델 로드
st.write("모델을 로드 중입니다. 잠시만 기다려주세요...")
learner = load_model_from_drive(file_id)
st.success("모델이 성공적으로 로드되었습니다!")

labels = learner.dls.vocab

# 스타일링을 통해 페이지 마진 줄이기
st.markdown("""
    <style>
    .reportview-container .main .block-container {
        max-width: 90%;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 분류에 따라 다른 콘텐츠 관리
content_data = {
    labels[0]: {
        'images': [
            "https://via.placeholder.com/300?text=Label1_Image1",
            "https://via.placeholder.com/300?text=Label1_Image2",
            "https://via.placeholder.com/300?text=Label1_Image3"
        ],
        'videos': [
            "https://youtube.com/shorts/kqnRszMI9SM?si=dEbWfU9B_Yj0Iq70",
            "https://youtu.be/ZHy2a7f7OxU?si=x4ngIM-hkAYMYV1t",
            "https://youtu.be/d--J48fqyi8?si=rm8k9ajqTX_VIRPc"
        ],
        'texts': [
            "0026 라이츄 : 전격은 10만볼트에 이르기도 해서 잘못 만지면 인도 코끼리라도 기절한다.",
            "꼬리가 어스 역할을 하여 전기를 지면으로 흘려보내므로 자신은 감전되거나 하지 않는다.",
            "몸에 전기가 모여 있으면 공격적인 성격으로 바뀐다. 어두운 곳에서 밝게 보인다."
        ]
    },
    labels[1]: {
        'images': [
            "https://via.placeholder.com/300?text=Label2_Image1",
            "https://via.placeholder.com/300?text=Label2_Image2",
            "https://via.placeholder.com/300?text=Label2_Image3"
        ],
        'videos': [
            "https://youtu.be/dA4fAiQ0tNM?si=WuA9rHumjMhHleT-",
            "https://youtu.be/4rtNTW4aIEY?si=VuhIaCkbHhuQnvSP",
            "https://youtube.com/shorts/TzlMOziiBKg?si=lU0-Z3drjCpew445"
        ],
        'texts': [
            "0172 피츄 : 아직 전기를 모으는 게 서툴다. 놀라거나 웃으면 바로 방전돼 버린다.",
            "작아도 어른을 찌릿찌릿 감전시킬 정도의 전기를 낸다. 단, 자신도 놀라 어찌할 줄 모른다.",
            "전기를 모으는 게 서툴다. 조금만 충격을 받아도 금방 방전해 버린다.."
        ]
    },
    labels[2]: {
        'images': [
            "https://via.placeholder.com/300?text=Label3_Image1",
            "https://via.placeholder.com/300?text=Label3_Image2",
            "https://via.placeholder.com/300?text=Label3_Image3"
        ],
        'videos': [
            "https://youtu.be/h4-ftQE3zEQ?si=GJPfyB8-LHQ8t2iq",
            "https://youtube.com/shorts/r1SACy3lx-E?si=qAsG1vAdJiZZ8tHr",
            "https://youtu.be/9kK86zmhpWc?si=_RFHVdlCa7pb2pXj"
        ],
        'texts': [
            "0025 피카츄 : 뺨의 양쪽에 작은 전기 주머니가 있다. 위기 상황일 때 방전한다.",
            "여러 마리가 모여 있으면 그 자리에 맹렬하게 전기가 모여서 벼락이 떨어질 때가 있다고 한다.",
            "꼬리를 세워서 주변의 기척을 느낀다고 한다. 그래서 무턱대고 꼬리를 잡아당기면 물어버린다."
        ]
    }
}

# 레이아웃 설정
left_column, right_column = st.columns([1, 2])  # 왼쪽과 오른쪽의 비율 조정

# 파일 업로드 컴포넌트 (jpg, png, jpeg, webp, tiff 지원)
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg", "webp", "tiff"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = PILImage.create(uploaded_file)
    prediction, _, probs = learner.predict(img)

    with left_column:
        display_left_content(image, prediction, probs, labels)

    with right_column:
        # 분류 결과에 따른 콘텐츠 선택
        data = content_data.get(prediction, {
            'images': ["https://via.placeholder.com/300"] * 3,
            'videos': ["https://www.youtube.com/watch?v=3JZ_D3ELwOQ"] * 3,
            'texts': ["기본 텍스트"] * 3
        })
        display_right_content(prediction, data)

