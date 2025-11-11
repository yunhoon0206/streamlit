import streamlit as st
import pandas as pd

# 데이터 로드 함수 (캐싱 사용)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('food.csv', encoding='euc-kr')
        # 불필요한 공백 제거
        df.columns = df.columns.str.strip()
        # 필요한 컬럼만 선택
        cols = ['식품대분류명', '식품중분류명', '식품소분류명', '식품명', '식품기원명', '에너지(kcal)']
        return df[cols]
    except FileNotFoundError:
        st.error("food.csv 파일을 찾을 수 없습니다. 파일을 현재 디렉토리에 업로드해주세요.")
        return pd.DataFrame()

# 데이터 로드
food_df = load_data()

if not food_df.empty:
    st.header("🍔 카테고리 별 음식 탐색")
    st.info("대분류, 중분류, 소분류를 선택하여 원하는 음식의 칼로리 정보를 (100g 기준) 확인하세요.")

    # 대분류 선택
    unique_dae = food_df['식품대분류명'].unique().tolist()
    selected_dae = st.selectbox('대분류', unique_dae)

    # 중분류 선택 (대분류에 따라 동적 변경)
    unique_joong = food_df[food_df['식품대분류명'] == selected_dae]['식품중분류명'].unique().tolist()
    selected_joong = st.selectbox('중분류', unique_joong)

    # 소분류 선택 (중분류에 따라 동적 변경)
    unique_so = food_df[(food_df['식품대분류명'] == selected_dae) & (food_df['식품중분류명'] == selected_joong)]['식품소분류명'].unique().tolist()
    selected_so = st.selectbox('소분류', unique_so)

    # 선택된 값에 따라 데이터 필터링
    filtered_df = food_df[
        (food_df['식품대분류명'] == selected_dae) &
        (food_df['식품중분류명'] == selected_joong) &
        (food_df['식품소분류명'] == selected_so)
    ]

    # 동적으로 제목 생성
    title_parts = [selected_dae]
    if selected_joong != '해당없음':
        title_parts.append(selected_joong)
    if selected_so != '해당없음':
        title_parts.append(selected_so)
    
    dynamic_title = " > ".join(title_parts)
    st.subheader(f"'{dynamic_title}' 카테고리의 음식 목록 (100g 기준)")
    
    # 결과 표시 (상품명, 식품기원명, 에너지(kcal) 컬럼만)
    st.dataframe(filtered_df[['식품명', '식품기원명', '에너지(kcal)']].reset_index(drop=True))
