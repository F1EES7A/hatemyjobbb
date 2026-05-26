import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# =================================================================
# 🎨 1. หน้าบ้านธีมนกอ้วนสุดน่ารัก (FRONTEND DESIGN)
# =================================================================
st.set_page_config(
    page_title="พี่นกอ้วน AI ผู้ช่วยสืบค้นความรู้",
    page_icon="🐦", # ไอคอนแท็บเว็บเป็นเจ้านกอ้วน
    layout="centered"
)

# ใช้ CSS ปรับแต่งสีสันและขนาดตัวหนังสือให้เป็นมิตรกับเด็กๆ
st.markdown("""
    <style>
    .main-title { color: #FF914D; font-family: 'Kanit', sans-serif; text-align: center; font-weight: bold; }
    .sub-title { color: #555555; text-align: center; margin-bottom: 30px; font-size: 1.2em; }
    .stTextInput>div>div>input { border-radius: 20px; border: 2px solid #FF914D; }
    .bird-box { background-color: #FFF3EB; padding: 20px; border-radius: 20px; border-left: 8px solid #FF914D; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# ส่วนหัวหน้าเว็บโชว์ตัวพี่นกอ้วน
st.markdown("<h1 class='main-title'>𓅭 พี่นกอ้วน AI ผู้ช่วยสืบค้นความรู้ 𓅰</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='bird-box'>
    <h3 style='margin-top:0; color:#FF731D;'>👋 สวัสดีจ้าเด็กๆ! ผมคือ "พี่นกอ้วน" </h3>
    <p>หนูๆ อยากค้นคว้าหรือสงสัยเรื่องอะไรในบทเรียน พิมพ์ถามพี่นกอ้วนด้านล่างได้เลยน้า ไม่ต้องใช้ API Key ฟรี 100% จ้า!</p>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 🧠 2. หลังบ้านระบบสมองกล (BACKEND)
# =================================================================

@st.cache_resource
def load_ai_core():
    # เปลี่ยนมาใช้โมเดลโครงสร้างขนาดย่อมที่เข้าใจบริบทคำถามและภาษาไทยได้ดีขึ้น
    model_name = "Fuji-X/Xwin-LM-7B-V0.1" 
    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base") # ใช้ Tokenizer ที่เก่งภาษาไทย
    model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0") # โมเดลขนาดเล็กที่วิ่งบน Cloud ฟรีได้ฉลุย
    return tokenizer, model

with st.spinner("⏳ พี่นกอ้วนกำลังบินไปเปิดสมุดขุดความรู้แป๊บนึงน้า (รอโหลดครั้งแรก 1-2 นาทีจ้า)..."):
    tokenizer, model = load_ai_core()

# กล่องรับคำถามจากเด็กๆ
user_query = st.text_input(
    "💬 พิมพ์เรื่องที่หนูอยากรู้ตรงนี้เลยจ้า:", 
    placeholder="เช่น ทำไมฝนถึงตก?, ดวงอาทิตย์คืออะไร?"
)

if user_query:
    with st.spinner("𓅭 พี่นกอ้วนกำลังใช้สมองอันชาญฉลาดคิดคำตอบอยู่จ้า..."):
        try:
            # สร้างข้อความสั่งการ (Prompt) บังคับให้ตอบแบบใจดี
            prompt = f"<|system|>\nคุณคือพี่นกอ้วน AI ใจดี ตอบคำถามเด็กนักเรียนสั้นๆ เป็นข้อๆ เข้าใจง่าย หลีกเลี่ยงคำหยาบคาย\n<|user|>\n{user_query}\n<|assistant|>\n"
            
            inputs = tokenizer(prompt, return_tensors="pt")
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs, 
                    max_new_tokens=150, # จำกัดความยาวคำตอบให้กระชับ เด็กอ่านง่าย
                    temperature=0.4,
                    do_sample=True
                )
            
            response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # ตัดส่วนที่เป็น Prompt ออก ให้เหลือแต่คำตอบจริง
            clean_response = response_text.split("<|assistant|>\n")[-1]
            
            # แสดงผลหน้าบ้าน
            st.markdown("---")
            st.balloons() # เอฟเฟกต์ลูกโป่งฉลองคำตอบเสร็จ!
            st.markdown(f"### 📝 ผลการสืบค้นเรื่อง: **{user_query}**")
            
            if clean_response.strip():
                st.info(f"𓅰 **พี่นกอ้วนสรุปให้ฟังดังนี้จ้า:**\n\n{clean_response}")
            else:
                st.warning("𓅭 พี่นกอ้วนคิดคำตอบยาวๆ ไม่ทัน ลองเปลี่ยนคำถามให้สั้นลงหน่อยนะจ๊ะ")
                
        except Exception as e:
            st.error("😥 เกิดข้อผิดพลาดหลังบ้าน: ลองพิมพ์ใหม่อีกครั้งนะครับเด็กๆ")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>𓅭 ซอฟต์แวร์สืบค้นความรู้นกอ้วนเวอร์ชันปลอดภัย ไร้ API Key 𓅰</p>", unsafe_allow_html=True)
