import streamlit as st
import pandas as pd
# --- 상수 및 설정 ---
NUTRIENT_COLS = [
    '에너지(kcal)', '수분(g)', '단백질(g)', '지방(g)', '회분(g)', '탄수화물(g)', 
    '당류(g)', '식이섬유(g)', '칼슘(mg)', '철(mg)', '인(mg)', '칼륨(mg)', 
    '나트륨(mg)', '비타민 A(μg RAE)', '레티놀(μg)', '베타카로틴(μg)', '티아민(mg)', 
    '리보플라빈(mg)', '니아신(mg)', '비타민 C(mg)', '비타민 D(μg)', '콜레스테롤(mg)', 
    '포화지방산(g)', '트랜스지방산(g)'
]

# 5대 영양소 및 권장 섭취량 기준 (일반적인 성인 기준, g/mg 단위)
RECOMMENDED_INTAKE = {
    '탄수화물(g)': 324, # g
    '단백질(g)': 55,    # g
    '지방(g)': 54,      # g
    '당류(g)': 100,     # g
    '나트륨(mg)': 2000   # mg
}

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('food.csv', encoding='euc-kr')
        df.columns = df.columns.str.strip()
        for col in NUTRIENT_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        st.error("food.csv 파일을 찾을 수 없습니다.")
        return pd.DataFrame()

food_df = load_data()

# --- 세션 상태 초기화 ---
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'selected_dae_filter' not in st.session_state: st.session_state.selected_dae_filter = '전체'
# ... (이하 필터 초기화 동일)
if 'selected_joong_filter' not in st.session_state: st.session_state.selected_joong_filter = '전체'
if 'selected_so_filter' not in st.session_state: st.session_state.selected_so_filter = '전체'
if 'selected_giwon_filter' not in st.session_state: st.session_state.selected_giwon_filter = '전체'

def reset_all():
    st.session_state.cart = {}
    st.session_state.selected_dae_filter = '전체'
    st.session_state.selected_joong_filter = '전체'
    st.session_state.selected_so_filter = '전체'
    st.session_state.selected_giwon_filter = '전체'
    # 사용자 정보도 초기화
    st.session_state.user_gender = "남성"
    st.session_state.user_height = 0
    st.session_state.user_weight = 0
    st.rerun()

# --- 메인 앱 ---
if not food_df.empty:
    st.header("🧮 스마트 영양성분 계산기")
    st.info("사용자 정보를 입력하고 음식을 추가하여 영양 섭취량을 분석해 보세요.")

    # --- 사용자 정보 입력 ---
    with st.expander("👤 사용자 정보 입력 (권장 섭취량 분석에 사용됩니다)", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.radio("성별", ["남성", "여성"], key='user_gender', horizontal=True)
        with col2:
            st.number_input("키(cm)", min_value=0, key='user_height')
        with col3:
            st.number_input("체중(kg)", min_value=0, key='user_weight')
        st.caption("입력된 정보는 페이지를 벗어나면 사라집니다.")

    st.button("모두 초기화", on_click=reset_all)

    # --- 필터링 UI (기존과 동일) ---
    st.subheader("음식 필터")
    # ... (필터 UI 코드는 변경 없음)
    col1, col2 = st.columns(2)
    with col1:
        unique_dae = ['전체'] + food_df['식품대분류명'].unique().tolist()
        selected_dae = st.selectbox(
            '대분류', unique_dae, index=unique_dae.index(st.session_state.selected_dae_filter), key='dae_filter_widget',
            on_change=lambda: st.session_state.update(selected_dae_filter=st.session_state.dae_filter_widget, selected_joong_filter='전체', selected_so_filter='전체', selected_giwon_filter='전체')
        )
    filtered_df1 = food_df[food_df['식품대분류명'] == st.session_state.selected_dae_filter] if st.session_state.selected_dae_filter != '전체' else food_df
    with col2:
        unique_joong = ['전체'] + filtered_df1['식품중분류명'].unique().tolist()
        selected_joong = st.selectbox(
            '중분류', unique_joong, index=unique_joong.index(st.session_state.selected_joong_filter), key='joong_filter_widget',
            on_change=lambda: st.session_state.update(selected_joong_filter=st.session_state.joong_filter_widget, selected_so_filter='전체', selected_giwon_filter='전체')
        )
    filtered_df2 = filtered_df1[filtered_df1['식품중분류명'] == st.session_state.selected_joong_filter] if st.session_state.selected_joong_filter != '전체' else filtered_df1
    col3, col4 = st.columns(2)
    with col3:
        unique_so = ['전체'] + filtered_df2['식품소분류명'].unique().tolist()
        selected_so = st.selectbox(
            '소분류', unique_so, index=unique_so.index(st.session_state.selected_so_filter), key='so_filter_widget',
            on_change=lambda: st.session_state.update(selected_so_filter=st.session_state.so_filter_widget, selected_giwon_filter='전체')
        )
    filtered_df3 = filtered_df2[filtered_df2['식품소분류명'] == st.session_state.selected_so_filter] if st.session_state.selected_so_filter != '전체' else filtered_df2
    with col4:
        unique_giwon = ['전체'] + filtered_df3['식품기원명'].unique().tolist()
        selected_giwon = st.selectbox(
            '식품기원명', unique_giwon, index=unique_giwon.index(st.session_state.selected_giwon_filter), key='giwon_filter_widget',
            on_change=lambda: st.session_state.update(selected_giwon_filter=st.session_state.giwon_filter_widget)
        )
    final_filtered_df = filtered_df3[filtered_df3['식품기원명'] == st.session_state.selected_giwon_filter] if st.session_state.selected_giwon_filter != '전체' else filtered_df3
    food_list = final_filtered_df['식품명'].unique().tolist()

    # --- 음식 선택 및 장바구니 추가 (기존과 동일) ---
    def add_to_cart():
        selected_foods = st.session_state.food_multiselect_widget
        for food_name in selected_foods:
            if food_name not in st.session_state.cart:
                food_info = food_df[food_df['식품명'] == food_name].iloc[0]
                st.session_state.cart[food_name] = {'grams': 100, 'nutrients': food_info[NUTRIENT_COLS]}
        st.session_state.food_multiselect_widget = []
    st.subheader("음식 선택하여 장바구니에 추가")
    st.multiselect('음식을 검색하거나 목록에서 선택하세요', food_list, label_visibility="collapsed", key='food_multiselect_widget')
    st.button("장바구니에 추가", key='add_to_cart_button', on_click=add_to_cart)

    # --- 장바구니 및 영양성분 계산 (기존과 동일) ---
    if st.session_state.cart:
        st.subheader("🛒 나의 장바구니")
        total_nutrients = pd.Series(0.0, index=NUTRIENT_COLS)
        # ... (장바구니 UI 및 계산 로직은 변경 없음)
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        col1.write("**음식명**"); col2.write("**그램(g)**"); col3.write("**칼로리(kcal)**")
        for food_name, details in list(st.session_state.cart.items()):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1: st.write(food_name)
            with col2:
                grams = st.number_input(f"grams_for_{food_name}", min_value=0, value=details['grams'], step=10, key=f"num_{food_name}", label_visibility="collapsed")
                st.session_state.cart[food_name]['grams'] = grams
            item_nutrients = (details['nutrients'] / 100) * grams
            total_nutrients += item_nutrients
            with col3: st.write(f"{item_nutrients['에너지(kcal)']:,.1f}")
            with col4:
                if st.button("삭제", key=f"del_{food_name}"):
                    del st.session_state.cart[food_name]
                    st.rerun()
        
        st.subheader(f"총 칼로리: **{total_nutrients['에너지(kcal)']:,.2f} kcal**")

        # --- 개인화된 영양 분석 ---
        if st.session_state.user_weight > 0 and st.session_state.user_height > 0:
            st.subheader("📈 내 섭취량 분석")
            
            # 표준 체중 및 권장 칼로리 계산 (단순화된 공식)
            std_weight = (st.session_state.user_height - 100) * 0.9
            recommended_calories = std_weight * 30 if st.session_state.user_gender == "남성" else std_weight * 25
            
            # 칼로리 분석
            total_calories_val = total_nutrients['에너지(kcal)']
            if total_calories_val < recommended_calories * 0.8:
                st.warning(f"현재 섭취 칼로리는 권장량({recommended_calories:,.0f} kcal)보다 부족합니다.")
            elif total_calories_val > recommended_calories * 1.2:
                st.error(f"현재 섭취 칼로리는 권장량({recommended_calories:,.0f} kcal)을 초과합니다.")
            else:
                st.success(f"현재 섭취 칼로리가 권장량({recommended_calories:,.0f} kcal)에 가깝습니다.")
            
            # 5대 영양소 분석
            st.write("**주요 영양소 섭취 현황**")
            for nutrient, rec_val in RECOMMENDED_INTAKE.items():
                current_val = total_nutrients.get(nutrient, 0)
                percentage_raw = (current_val / rec_val) * 100 if rec_val > 0 else 0

                # 섭취량에 따른 색상 결정
                if percentage_raw >= 200:
                    color = "#ff4b4b"  # 빨강 (2배 초과)
                elif percentage_raw >= 150:
                    color = "#ffc400"  # 노랑 (1.5배 초과)
                elif percentage_raw >= 80:
                    color = "#28a745"  # 초록 (적절)
                else:
                    color = "#007bff"  # 파랑 (부족)

                # 시각적 표시를 위한 퍼센티지 (최대 100%)
                percentage_display = min(percentage_raw, 100)

                # 텍스트 표시
                st.write(f"**{nutrient.split('(')[0]}** : {current_val:,.1f} / {rec_val:,.0f} {nutrient.split('(')[1].replace(')','')}")
                
                # 커스텀 진행률 막대 (HTML/CSS)
                progress_bar_html = f"""
                <div style="background-color: #e9ecef; border-radius: 5px; height: 10px; width: 100%;">
                  <div style="background-color: {color}; width: {percentage_display}%; border-radius: 5px; height: 100%;"></div>
                </div>
                """
                st.markdown(progress_bar_html, unsafe_allow_html=True)

        with st.expander("📊 모든 영양성분 합계 보기"):
            nutrient_df = total_nutrients.reset_index(); nutrient_df.columns = ['영양성분', '함량']
            nutrient_df['함량'] = nutrient_df['함량'].map('{:,.2f}'.format)
            col1, col2 = st.columns(2)
            with col1: st.dataframe(nutrient_df.iloc[:len(NUTRIENT_COLS)//2])
            with col2: st.dataframe(nutrient_df.iloc[len(NUTRIENT_COLS)//2:])
    else:
        st.warning("음식을 선택하고 '장바구니에 추가' 버튼을 눌러주세요.")

    # --- 칼로리 초과 시 동영상 표시 ---
    if 'total_nutrients' in locals() and total_nutrients['에너지(kcal)'] > 2500:
        st.subheader("오늘 섭취 칼로리가 높네요! 가벼운 운동은 어떠신가요? 💪")
        st.video("https://www.youtube.com/watch?v=DCAp0b16kyo")
        import streamlit as st
