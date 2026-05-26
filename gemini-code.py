import streamlit as st
from google import genai
from google.genai import types
import os

# =================================================================
# 🎨 1. จัดการหน้าบ้าน (FRONTEND DESIGN)
# =================================================================
st.set_page_config(
    page_title="ครู AI ผู้ช่วยสืบค้นข้อมูลสำหรับเด็กๆ",
    page_icon="🤖",
    layout="centered"
)

# ใช้ CSS ตกแต่งสีสัน
st.markdown("""
    <style>
    .main-title { color: #2E5BFF; font-family: 'Helvetica Neue', sans-serif; text-align: center; font-weight: bold; }
    .sub-title { color: #555555; text-align: center; margin-bottom: 30px; }
    .stButton>button { background-color: #2E5BFF; color: white; border-radius: 20px; padding: 10px 25px; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎓 ครู AI ผู้ช่วยสืบค้นความรู้</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>ปลอดภัย เข้าใจง่าย พร้อมตอบคำถามเด็กๆ ตลอด 24 ชั่วโมงจ้า ✨</p>", unsafe_allow_html=True)

# แถบเมนูด้านซ้ายสำหรับปุ่มคำถามแนะนำ (ตัดช่องใส่ API Key ออกไปแล้ว)
st.sidebar.markdown("💡 **หัวข้อน่าลองค้นหา:**")
suggested_topics = [
    "ทำไมท้องฟ้าถึงเป็นสีฟ้า?",
    "ต้นไม้ปรุงอาหารได้อย่างไร?",
    "ไดโนเสาร์สูญพันธุ์เพราะอะไร?",
    "ประวัติศาสตร์วันสุนทรภู่"
]
for topic in suggested_topics:
    if st.sidebar.button(topic):
        st.session_state.search_query = topic

# =================================================================
# 🧠 2. จัดการหลังบ้าน (BACKEND & SECRET KEY)
# =================================================================

# กฎเหล็กควบคุมพฤติกรรม AI
STUDENT_PROMPT = """
คุณคือ 'ครู AI ใจดี' ผู้เชี่ยวชาญด้านการสอนเด็กวัยเรียน (ประถม-มัธยม) 
คุณต้องตอบคำถามด้วยกฎเหล็กดังต่อไปนี้อย่างเคร่งครัด:
1. ภาษา: ใช้ภาษาไทยที่สุภาพ เป็นกันเอง มีหางเสียง (ครับ/ค่ะ/จ้า) เข้าใจง่ายมาก ไม่ใช้ศัพท์เทคนิคยากๆ หากเลี่ยงไม่ได้ให้วงเล็บอธิบายสั้นๆ
2. รูปแบบ: ห้ามเขียนยาวเป็นพารากราฟยัดเยียด ให้แบ่งเป็นข้อๆ (1, 2, 3) หรือใช้ Bullet points ชัดเจน
3. ความปลอดภัย: ห้ามตอบเรื่องความรุนแรง เรื่องเพศ สิ่งผิดกฎหมาย การกลั่นแกล้ง หรือเรื่องที่ไม่เหมาะสมกับเด็กเด็ดขาด หากเจอคำถามประเภทนี้ ให้ตอบปฏิเสธอย่างสุภาพและเปลี่ยนไปชวนคุยเรื่องที่เป็นประโยชน์แทน
4. ความถูกต้อง: ต้องอิงความจริงตามหลักวิชาการ ห้ามมโนหรือแต่งเรื่องโกหก
5. ส่วนเสริม: ในตอนท้ายของคำตอบ ต้องมีหัวข้อ "💡 เกร็ดความรู้น่าคิด" เสมอ เพื่อกระتعุ้นให้เด็กอยากเรียนรู้ต่อ
"""

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

user_query = st.text_input(
    "🔍 หนูอยากค้นคว้าเรื่องอะไรวันนี้ บอกครูได้เลยครับ/ค่ะ:", 
    value=st.session_state.search_query,
    placeholder="เช่น ทำไมฝนถึงตก?, สรุปเรื่องระบบสุริยะสั้นๆ"
)

# ดึง API Key ที่แอบซ่อนไว้ในระบบ Streamlit Cloud (ชื่อตัวแปร GEMINI_API_KEY)
# วิธีนี้ทำให้เด็กๆ ไม่เห็นคีย์ และโค้ดปลอดภัย 100%
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    api_key = None

if user_query:
    if api_key:
        with st.spinner("⏳ ครู AI กำลังเปิดห้องสมุดค้นข้อมูลให้แป๊บนึงน้า..."):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_query,
                    config=types.GenerateContentConfig(
                        system_instruction=STUDENT_PROMPT,
                        temperature=0.3
                    )
                )
                
                st.markdown("---")
                st.balloons() # เอฟเฟกต์ลูกโป่ง
                st.markdown(f"### 📝 ผลการค้นคว้าเรื่อง: **{user_query}**")
                st.info(response.text)
                
            except Exception as e:
                st.error("😥 เกิดข้อผิดพลาดหลังบ้าน: ลองกดส่งคำถามใหม่อีกครั้งนะครับ")
    else:
        st.error("⚠️ ระบบยังไม่ได้ตั้งค่า API Key หลังบ้าน (กรุณาตั้งค่าใน Streamlit Secrets)")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>ระบบซอฟต์แวร์ค้นคว้าปลอดภัยสำหรับโรงเรียนและเยาวชน</p>", unsafe_allow_html=True)