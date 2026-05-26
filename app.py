import streamlit as st
from transformers import pipeline

# =================================================================
# 🎨 1. หน้าบ้าน (FRONTEND)
# =================================================================
st.set_page_config(
    page_title="ครู AI ผู้ช่วยสืบค้นข้อมูลสำหรับเด็กๆ",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
    <style>
    .main-title { color: #2E5BFF; font-family: 'Helvetica Neue', sans-serif; text-align: center; font-weight: bold; }
    .sub-title { color: #555555; text-align: center; margin-bottom: 30px; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎓 ครู AI ผู้ช่วยสืบค้นความรู้</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>ระบบซอฟต์แวร์ฟรี 100% ไม่ต้องใช้ API Key ปลอดภัยสำหรับนักเรียน ✨</p>", unsafe_allow_html=True)

# =================================================================
# 🧠 2. หลังบ้าน (BACKEND - โหลดโมเดล AI ฟรีในตัว)
# =================================================================

# ฟังก์ชันล็อกให้ดาวน์โหลดโมเดลแค่ครั้งเดียว ไม่โหลดซ้ำทุกครั้งที่เด็กพิมพ์
@st.cache_resource
def load_ai_model():
    # ใช้โมเดลซอฟต์แวร์เปิด (Open-source) ขนาดย่อมที่รองรับภาษาไทยในการตอบคำถาม
    return pipeline("text2text-generation", model="google/mt5-small")

with st.spinner("⏳ ระบบกำลังสตาร์ทสมองครู AI ครั้งแรกสุด (อาจใช้เวลา 1-2 นาทีในการตั้งค่าหลังบ้าน)..."):
    text_generator = load_ai_model()

# กล่องรับคำถามจากเด็กๆ
user_query = st.text_input(
    "🔍 หนูอยากค้นคว้าเรื่องอะไรวันนี้ พิมพ์บอกครูได้เลยครับ/ค่ะ:", 
    placeholder="เช่น ประเทศไทยมีกี่จังหวัด?, ข้อมูลของดวงอาทิตย์"
)

if user_query:
    with st.spinner("⏳ ครู AI กำลังประมวลผลคำตอบให้จ้า..."):
        try:
            # สั่งให้โมเดลประมวลผลข้อความไทย
            # ส่งคำสั่งควบคุมพฤติกรรมพ่วงไปกับคำถามของเด็ก
            prompt = f"ตอบคำถามนักเรียนด้วยภาษาที่เข้าใจง่ายและเป็นข้อๆ: {user_query}"
            
            # รันผลลัพธ์ผ่านตัวโมเดลซอฟต์แวร์ตรงๆ ไม่วิ่งไปผ่าน API ค่ายไหน
            result = text_generator(prompt, max_length=200, num_return_sequences=1)
            response_text = result[0]['generated_text']
            
            # แสดงผลหน้าบ้าน
            st.markdown("---")
            st.balloons() # เอฟเฟกต์ลูกโป่ง
            st.markdown(f"### 📝 ผลการค้นคว้าเรื่อง: **{user_query}**")
            
            # กรณีโมเดลฟรีขนาดเล็กอาจจะตอบสั้น ให้มีโครงสร้างรองรับ
            if response_text:
                st.info(f"✨ ครู AI ขอสรุปให้น้องๆ ฟังดังนี้ครับ:\n\n{response_text}")
            else:
                st.warning("ครู AI คิดคำตอบนี้ไม่ทัน ลองเปลี่ยนคำถามให้กระชับขึ้นดูนะจ๊ะ")
                
        except Exception as e:
            st.error("😥 เกิดข้อผิดพลาดในการประมวลผล ลองพิมพ์ใหม่อีกครั้งนะครับ")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>ระบบนี้ทำงานด้วยโมเดล Open-source ภายในซอฟต์แวร์เอง ไม่พึ่งพาคีย์ภายนอก</p>", unsafe_allow_html=True)
