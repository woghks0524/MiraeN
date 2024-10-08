import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import pandas as pd

# 사이드바에 활동 설명 추가
st.sidebar.title("활동 설명")
st.sidebar.write("""
이 활동은 사용자가 입력한 그림이 픽셀의 크기에 따라 어떻게 다르게 보일 수 있는지 살펴보는 활동입니다. 픽셀이 작을수록 실제 그림과 비슷하게 보이며, 실제로 픽셀은 굉장히 작아 픽셀로 만든 이미지가 인간의 눈에는 자연스럽게 연결된 이미지로 보이게 됩니다.
- 흑백 이미지를 넣었을 때 더 효과적입니다.
- '정사각형 크기 설정'을 통해 픽셀의 크기를 바꿀 수 있습니다.
- '흑백 전환 임계값 설정'을 통해 흑백으로 칠해지는 기준을 바꿀 수 있습니다.
""")

# 이미지 업로드 및 설명 추가
uploaded_file = st.file_uploader("이미지를 업로드하세요. (흑백 이미지를 넣었을 때 더 효과적입니다.)", type=["png", "jpg", "jpeg"])

# 정사각형 크기 슬라이더
square_size = st.slider("정사각형 크기 설정", min_value=5, max_value=100, value=20, step=5)

# 임계값 슬라이더
threshold = st.slider("흑백 전환 임계값 설정", min_value=0, max_value=255, value=128, step=1)

if uploaded_file is not None:
    # 이미지 열기
    image = Image.open(uploaded_file)
    
    # 두 개의 열을 생성하여 나란히 배치
    col1, col2 = st.columns(2)

    # 첫 번째 열에 원본 이미지 표시
    with col1:
        st.image(image, caption="원본 이미지", use_column_width=True)

    # 이미지를 흑백으로 변환
    image = ImageOps.grayscale(image)
    
    # 이미지를 정사각형 단위로 분할하여 처리
    img_array = np.array(image)
    height, width = img_array.shape
    new_image = np.zeros((height, width), dtype=np.uint8)

    # 이미지 처리 및 변환
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            # 각 정사각형 영역의 평균 값 계산
            region = img_array[y:y+square_size, x:x+square_size]
            avg_value = np.mean(region)

            # 임계값 기준으로 흑백 변환
            color = 255 if avg_value >= threshold else 0
            new_image[y:y+square_size, x:x+square_size] = color

    # 두 번째 열에 변환된 이미지 표시
    with col2:
        st.image(new_image, caption="변환된 이미지", use_column_width=True)

    # 숫자로 변환하는 버튼
    if st.button("숫자로 변환하기"):
        # 정사각형 단위로 숫자로 변환하기
        binary_image = []

        for y in range(0, height, square_size):
            row = []
            for x in range(0, width, square_size):
                # 각 정사각형 영역의 평균 값 계산
                region = new_image[y:y+square_size, x:x+square_size]
                avg_value = np.mean(region)

                # 임계값 기준으로 1 또는 0 할당
                if avg_value >= 128:  # 50% 이상 검정이면 1, 아니면 0
                    row.append(1)
                else:
                    row.append(0)
            binary_image.append(row)

        # 숫자 배열을 Pandas DataFrame으로 변환하여 출력
        binary_df = pd.DataFrame(binary_image)
        st.dataframe(binary_df.style.set_properties(**{'text-align': 'center'}))
