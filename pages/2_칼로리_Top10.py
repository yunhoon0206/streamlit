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
        cols = ['식품대분류명', '식품명', '식품기원명', '에너지(kcal)']
        return df[cols]
    except FileNotFoundError:
        st.error("food.csv 파일을 찾을 수 없습니다. 파일을 현재 디렉토리에 업로드해주세요.")
        return pd.DataFrame()

# 데이터 로드
food_df = load_data()

if not food_df.empty:
    st.header("🏆 칼로리 Top 10")
    st.info("대분류를 선택하여 해당 카테고리의 칼로리 랭킹을 (100g 기준) 확인하세요.")

    # 대분류 선택
    unique_dae = food_df['식품대분류명'].unique().tolist()
    selected_dae = st.selectbox('대분류', unique_dae)

    # 선택된 대분류에 따라 데이터 필터링 및 정렬
    top_10_df = food_df[food_df['식품대분류명'] == selected_dae].copy()
    
    # '에너지(kcal)' 컬럼을 숫자형으로 변환 (오류 발생 시 NaN으로 처리)
    top_10_df['에너지(kcal)'] = pd.to_numeric(top_10_df['에너지(kcal)'], errors='coerce')
    
    # NaN 값을 가진 행 제거
    top_10_df.dropna(subset=['에너지(kcal)'], inplace=True)

    # 칼로리 기준으로 내림차순 정렬
    top_10_df = top_10_df.sort_values(by='에너지(kcal)', ascending=False)

    # 표시할 데이터 개수 결정 (10개 또는 그 미만)
    display_count = min(10, len(top_10_df))
    
    st.subheader(f"'{selected_dae}' 카테고리의 칼로리 Top {display_count} (100g 기준)")
    
    # 결과 표시
    display_df = top_10_df[['식품명', '식품기원명', '에너지(kcal)']].head(display_count).reset_index(drop=True)
    st.dataframe(display_df)

    # 대화형 그래프 추가
    st.subheader("📊 칼로리 비교 그래프 (100g 기준)")
    fig = px.bar(
        display_df.sort_values('에너지(kcal)', ascending=True), 
        x='에너지(kcal)', 
        y='식품명',
        orientation='h',
        title=f"'{selected_dae}' 칼로리 Top {display_count} 비교 (100g 기준)",
        labels={'식품명': '음식 이름', '에너지(kcal)': '칼로리(kcal) (100g 기준)'}
    )
    fig.update_layout(yaxis_title="", xaxis_title="칼로리(kcal) (100g 기준)")
    st.plotly_chart(fig)
