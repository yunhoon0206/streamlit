import streamlit as st
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="결제 정보 확인", page_icon="💳")

st.title("💳 결제 정보 확인 페이지")

# 결제 정보 입력 폼
with st.form("payment_form"):
	st.subheader("결제 정보 입력")
	
	name = st.text_input("이름")
	product = st.text_input("상품명")
	price = st.number_input("결제 금액 (원)", min_value=0, step=1000)
	method = st.selectbox("결제 수단", ["신용카드", "계좌이체", "카카오페이", "네이버페이", "기타"])
	pay_date = st.date_input("결제일", datetime.now().date())
	
	drawing_mode = st.selectbox("Drawing tool:",
		("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
	)
	if drawing_mode == "point":
		point_display_radius = st.slider("Point display radius: ", 1, 25, 3)

	stroke_width = st.slider("펜 굵기 : ", 1, 25, 3)
	bg_image = st.file_uploader("Background image:", type=["png", "jpg"])

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
		drawing_mode=drawing_mode,
		point_display_radius=point_display_radius if drawing_mode == "point" else 0,
		display_toolbar=True,
		key="full_app",
	)

	submitted = st.form_submit_button("결제 정보 저장")

# 결과 표시
if submitted:
	st.success("✅ 결제 정보가 저장되었습니다.")
	st.divider()
	st.subheader("📋 결제 정보 요약")
	st.write(f"**이름:** {name}")
	st.write(f"**상품명:** {product}")
	st.write(f"**결제 금액:** {price:,.0f} 원")
	st.write(f"**결제 수단:** {method}")
	st.write(f"**결제일:** {pay_date.strftime('%Y-%m-%d')}")
	
	st.divider()
	st.toast('저장되었습니다', duration="short")
	st.info("감사합니다! 결제가 정상적으로 처리되었습니다.")