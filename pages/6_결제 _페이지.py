import streamlit as st
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

methods = [ "신용카드", "계좌이체", "카카오페이", "네이버페이", "휴대폰결제" ]

st.set_page_config(page_title="결제 정보 확인", page_icon="💳")

st.title("💳 결제 정보 확인 페이지")

# 결제 정보 입력 폼
with st.form("payment_form"):
   st.subheader("결제 정보 입력")
   
   name = st.text_input("이름")
   price = st.number_input("결제 금액 (원)", min_value=0, step=1000)
   method = st.selectbox("결제 수단", methods)
   product = st.text_input("카드 번호")
   cvc = st.date_input("CVC", datetime.now().date())

   stroke_width = st.slider("펜 굵기 : ", 1, 25, 3)

   # Create a canvas component
   canvas_result = st_canvas(
      fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
      stroke_width=stroke_width,
      stroke_color="000",
      background_color="#eee",
      background_image=None,
      update_streamlit=False,
      width=200,
      height=200,
      drawing_mode="freedraw",
      point_display_radius=0,
      display_toolbar=True,
      key="full_app",
   )

   submitted = st.form_submit_button("결제 정보 저장")

# 결과 표시
if submitted:
   st.success("✅ 결제 정보가 저장되었습니다.")
   st.toast('저장되었습니다', duration="short")