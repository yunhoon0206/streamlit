import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 상수 및 설정 ---
NUTRIENT_COLS_FOR_COMPARE = [
    '에너지(kcal)', '탄수화물(g)', '단백질(g)', '지방(g)', '당류(g)', '나트륨(mg)',
    '콜레스테롤(mg)', '포화지방산(g)', '식이섬유(g)'
]

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('food.csv', encoding='euc-kr')
        df.columns = df.columns.str.strip()
        required_cols = ['식품대분류명', '식품중분류명', '식품소분류명', '식품명'] + NUTRIENT_COLS_FOR_COMPARE
        for col in required_cols:
            if col in df.columns:
                if col in NUTRIENT_COLS_FOR_COMPARE:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                st.error(f"'{col}' 컬럼을 food.csv 파일에서 찾을 수 없습니다.")
                return pd.DataFrame()
        return df[required_cols]
    except FileNotFoundError:
        st.error("food.csv 파일을 찾을 수 없습니다.")
        return pd.DataFrame()

food_df = load_data()

# --- 메인 앱 ---
if not food_df.empty:
    st.header("🎯 음식 vs 음식 비교 분석기")
    st.info("필터를 이용해 두 가지 음식을 선택하여 영양성분(100g 기준)을 비교해 보세요.")

    col1, col2 = st.columns(2)

    # --- 음식 1 선택 UI ---
    with col1:
        st.subheader("음식 1")
        dae1_options = ['전체'] + food_df['식품대분류명'].unique().tolist()
        dae1 = st.selectbox('대분류', dae1_options, key='dae1')
        
        df1_filtered = food_df[food_df['식품대분류명'] == dae1] if dae1 != '전체' else food_df
        joong1_options = ['전체'] + df1_filtered['식품중분류명'].unique().tolist()
        joong1 = st.selectbox('중분류', joong1_options, key='joong1')

        df1_filtered = df1_filtered[df1_filtered['식품중분류명'] == joong1] if joong1 != '전체' else df1_filtered
        so1_options = ['전체'] + df1_filtered['식품소분류명'].unique().tolist()
        so1 = st.selectbox('소분류', so1_options, key='so1')

        df1_filtered = df1_filtered[df1_filtered['식품소분류명'] == so1] if so1 != '전체' else df1_filtered
        
        food1_list = df1_filtered['식품명'].unique().tolist()
        food1_name = st.selectbox("**음식 선택**", options=food1_list, index=None, placeholder="첫 번째 음식을 선택하세요.", key='food1_select')

    # --- 음식 2 선택 UI ---
    with col2:
        st.subheader("음식 2")
        dae2_options = ['전체'] + food_df['식품대분류명'].unique().tolist()
        dae2 = st.selectbox('대분류', dae2_options, key='dae2')

        df2_filtered = food_df[food_df['식품대분류명'] == dae2] if dae2 != '전체' else food_df
        joong2_options = ['전체'] + df2_filtered['식품중분류명'].unique().tolist()
        joong2 = st.selectbox('중분류', joong2_options, key='joong2')

        df2_filtered = df2_filtered[df2_filtered['식품중분류명'] == joong2] if joong2 != '전체' else df2_filtered
        so2_options = ['전체'] + df2_filtered['식품소분류명'].unique().tolist()
        so2 = st.selectbox('소분류', so2_options, key='so2')

        df2_filtered = df2_filtered[df2_filtered['식품소분류명'] == so2] if so2 != '전체' else df2_filtered

        food2_list = df2_filtered['식품명'].unique().tolist()
        food2_name = st.selectbox("**음식 선택**", options=food2_list, index=None, placeholder="두 번째 음식을 선택하세요.", key='food2_select')

    # --- 비교 분석 ---
    if food1_name and food2_name:
        food1_data = food_df[food_df['식품명'] == food1_name].iloc[0]
        food2_data = food_df[food_df['식품명'] == food2_name].iloc[0]

        st.subheader("📊 영양성분 비교표")
        compare_df = pd.DataFrame({
            '영양성분': NUTRIENT_COLS_FOR_COMPARE,
            food1_name: food1_data[NUTRIENT_COLS_FOR_COMPARE].values,
            food2_name: food2_data[NUTRIENT_COLS_FOR_COMPARE].values
        }).set_index('영양성분')
        st.dataframe(compare_df)

        st.subheader("📈 영양성분 비교 그래프")
        fig = go.Figure()
        fig.add_trace(go.Bar(y=[col.split('(')[0] for col in NUTRIENT_COLS_FOR_COMPARE], x=food1_data[NUTRIENT_COLS_FOR_COMPARE], name=food1_name, orientation='h'))
        fig.add_trace(go.Bar(y=[col.split('(')[0] for col in NUTRIENT_COLS_FOR_COMPARE], x=food2_data[NUTRIENT_COLS_FOR_COMPARE], name=food2_name, orientation='h'))
        fig.update_layout(
            title=f"'{food1_name}' vs '{food2_name}' 영양성분 비교",
            yaxis_title="영양성분",
            xaxis_title="함량 (단위는 표 참고)",
            barmode='group',
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig)

    elif food1_name or food2_name:
        st.warning("비교를 위해 두 가지 음식을 모두 선택해주세요.")
