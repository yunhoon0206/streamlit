import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드 함수 (캐싱 사용)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('food.csv', encoding='euc-kr')
        # 불필요한 공백 제거
        df.columns = df.columns.str.strip()
        # 필요한 컬럼만 선택
        cols = ['식품대분류명', '에너지(kcal)']
        return df[cols]
    except FileNotFoundError:
        st.error("food.csv 파일을 찾을 수 없습니다. 파일을 현재 디렉토리에 업로드해주세요.")
        return pd.DataFrame()

# 데이터 로드
food_df = load_data()

if not food_df.empty:
    st.header("📊 카테고리별 평균 칼로리")
    st.info("각 식품 대분류의 평균 칼로리 정보를 (100g 기준) 확인하세요.")

    # '에너지(kcal)' 컬럼을 숫자형으로 변환 (오류 발생 시 NaN으로 처리)
    food_df['에너지(kcal)'] = pd.to_numeric(food_df['에너지(kcal)'], errors='coerce')
    
    # NaN 값을 가진 행 제거
    food_df.dropna(subset=['에너지(kcal)'], inplace=True)

    # 카테고리별 평균 에너지 계산
    avg_calorie_df = food_df.groupby('식품대분류명')['에너지(kcal)'].mean().sort_values(ascending=False).reset_index()
    
    # 컬럼명 변경
    avg_calorie_df.columns = ['식품대분류명', '평균 에너지(kcal)']

    st.subheader("🍽️ 식품 대분류별 평균 칼로리 표 (100g 기준)")
    st.dataframe(avg_calorie_df)

    # 대화형 그래프 추가
    st.subheader("📈 식품 대분류별 평균 칼로리 그래프 (100g 기준)")
    fig = px.bar(
        avg_calorie_df.sort_values('평균 에너지(kcal)', ascending=True),
        x='평균 에너지(kcal)', 
        y='식품대분류명',
        orientation='h',
        title="식품 대분류별 평균 칼로리 비교 (100g 기준)",
        labels={'식품대분류명': '식품 대분류', '평균 에너지(kcal)': '평균 칼로리(kcal) (100g 기준)'}
    )
    fig.update_layout(yaxis_title="", xaxis_title="평균 칼로리(kcal) (100g 기준)")
    st.plotly_chart(fig)
