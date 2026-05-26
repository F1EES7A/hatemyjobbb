import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

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
# 🧠 2. หลังบ้าน (BACKEND - โหลดตรงไม่ผ่าน Pipeline)
# =================================================================

# ใช้ฟังก์ชันแคชของ Streamlit เพื่อโหลดโมเดลเข้าหน่วยความจำแค่ครั้งเดียว
@st.cache_resource
def load_ai_core():
    model_name = "google/mt5-small"
    # โหลดตัวแปลงข้อความเป็นตัวเลข (Tokenizer) และตัวโมเดลสมองกลโดยตรง
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

with st.spinner("⏳ ระบบกำลังสตาร์ทสมองครู AI ครั้งแรกสุด (อาจใช้เวลา 1-2 นาทีในการดาวน์โหลดโมเดล)..."):
    tokenizer, model = load_ai_core()

# กล่องรับคำถามจากเด็กๆ
user_query = st.text_input(
    "🔍 หนูอยากค้นคว้าเรื่องอะไรวันนี้ พิมพ์บอกครูได้เลยครับ/ค่ะ:", 
    placeholder="เช่น ประเทศไทยมีกี่จังหวัด?, ข้อมูลของดวงอาทิตย์"
)

if user_query:
    with st.spinner("⏳ ครู AI กำลังประมวลผลคำตอบให้จ้า..."):
        try:
            # 1. แปลงข้อความคำถามของเด็กให้เป็นตัวเลขที่โมเดลเข้าใจ
            prompt = f"ตอบคำถามนักเรียนสั้นๆ เป็นข้อๆ: {user_query}"
            inputs = tokenizer(prompt, return_tensors="pt", padding=True)
            
            # 2. สั่งให้โมเดลคำนวณและสร้างคำตอบออกมา
            with torch.no_grad():
                outputs = model.generate(
                    **inputs, 
                    max_length=256, 
                    num_beams=4, 
                    early_stopping=True
                )
            
            # 3. แปลงผลลัพธ์จากตัวเลขกลับมาเป็นภาษาไทยที่อ่านออก
            response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # แสดงผลหน้าบ้าน
            st.markdown("---")
            st.balloons() # เอฟเฟกต์ลูกโป่งลอย
            st.markdown(f"### 📝 ผลการค้นคว้าเรื่อง: **{user_query}**")
            
            if response_text.strip():
                st.info(f"✨ ครู AI ขอสรุปให้น้องๆ ฟังดังนี้ครับ:\n\n{response_text}")
            else:
                st.warning("ครู AI กำลังคิดคำตอบที่เหมาะสมอยู่ ลองเปลี่ยนคำถามให้กระชับขึ้นดูนะจ๊ะ")
                
        except Exception as e:
            st.error("😥 เกิดข้อผิดพลาดในการประมวลผล ลองพิมพ์ใหม่อีกครั้งนะครับ")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>ระบบนี้ทำงานด้วยโมเดลคณิตศาสตร์ในตัวซอฟต์แวร์เอง ปลอดภัย ไร้ API Key</p>", unsafe_allow_html=True)
