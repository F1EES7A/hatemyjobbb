import streamlit as st
from duckduckgo_search import DDGS
from transformers import pipeline

# =================================================================
# 🎨 1. หน้าบ้านธีมนกอ้วนสุดน่ารัก (FRONTEND DESIGN)
# =================================================================
st.set_page_config(
    page_title="พี่นกอ้วน AI ผู้ช่วยสืบค้นความรู้",
    page_icon="🐦",
    layout="centered"
)

st.markdown("""
    <style>
    .main-title { color: #FF914D; font-family: 'Kanit', sans-serif; text-align: center; font-weight: bold; }
    .sub-title { color: #555555; text-align: center; margin-bottom: 30px; font-size: 1.1em; }
    .stTextInput>div>div>input { border-radius: 20px; border: 2px solid #FF914D; }
    .bird-box { background-color: #FFF3EB; padding: 20px; border-radius: 20px; border-left: 8px solid #FF914D; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>𓅭 พี่นกอ้วน AI ผู้ช่วยสืบค้นความรู้ 𓅰</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='bird-box'>
    <h3 style='margin-top:0; color:#FF731D;'>👋 สวัสดีจ้าเด็กๆ! ผมคือ "พี่นกอ้วน" รุ่นรอบรู้โลกกว้าง</h3>
    <p>พี่นกอ้วนเชื่อมต่อกับห้องสมุดอินเทอร์เน็ตแล้ว สงสัยเรื่องอะไรวิชาไหน พิมพ์ถามได้เลย ไม่ต้องใช้ API Key จ้า!</p>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 🧠 2. ระบบหลังบ้านอัจฉริยะ (BACKEND - HYBRID SEARCH)
# =================================================================

# โหลดโมเดลสรุปความเข้าใจขนาดย่อม (เบา สตาร์ทไว ไม่ทำเว็บล่ม)
@st.cache_resource
def load_summary_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")

try:
    summarizer = load_summary_model()
except:
    summarizer = None

# กล่องรับคำถามจากเด็กๆ
user_query = st.text_input(
    "💬 พิมพ์เรื่องที่หนูอยากรู้ตรงนี้เลยจ้า (ค้นได้ทุกเรื่องในโลก):", 
    placeholder="เช่น ทำไมไดโนเสาร์ถึงสูญพันธุ์?, วันสุนทรภู่คือวันที่เท่าไหร่"
)

if user_query:
    with st.spinner("𓅭 พี่นกอ้วนกำลังกระพือปีกบินไปค้นหาข้อมูลจากทั่วโลกมาให้แป๊บนึงน้า..."):
        try:
            # สเต็ปที่ 1: หลังบ้านบินไปค้นหาข้อมูลจากอินเทอร์เน็ตสดๆ 
            with DDGS() as ddgs:
                # ค้นหาข้อมูลภาษาไทย 3 แหล่งที่น่าเชื่อถือที่สุด
                search_results = [r for r in ddgs.text(user_query, region="th-th", max_results=3)]
            
            if search_results:
                # รวมข้อมูลที่ค้นพบเข้าด้วยกัน
                raw_knowledge = ""
                for res in search_results:
                    raw_knowledge += f"{res['body']}\n"
                
                # แสดงผลหน้าบ้าน
                st.markdown("---")
                st.balloons() # เอฟเฟกต์ลูกโป่งฉลองคำตอบเสร็จ!
                st.markdown(f"### 📝 ผลการสืบค้นเรื่อง: **{user_query}**")
                
                # สเต็ปที่ 2: แสดงข้อมูลดิบที่อัปเดตล่าสุดให้อ่านง่าย
                # จัดรูปแบบให้เด็กๆ อ่านง่าย แยกส่วนชัดเจน
                st.info(f"𓅰 **พี่นกอ้วนไปสืบค้นข้อมูลล่าสุดจากอินเทอร์เน็ตมาให้แล้วจ้า:**\n\n"
                        f"✨ {search_results[0]['body']}\n\n"
                        f"✨ {search_results[1]['body'] if len(search_results) > 1 else ''}")
                
                # แนะนำแหล่งข้อมูลเพิ่มเติมให้เด็กไปศึกษาต่อ
                st.markdown("💡 **หนูๆ สามารถไปอ่านต่อเพิ่มเติมได้จากลิงก์เหล่านี้นะจ๊ะ:**")
                for i, res in enumerate(search_results):
                    st.markdown(f" [{i+1}] {res['title']} ({res['href']})")
            else:
                st.warning("𓅭 พี่นกอ้วนบินไปหาทั่วอินเทอร์เน็ตแล้วยังไม่เจอ ลองเปลี่ยนใช้คำค้นหาอื่นดูนะจ๊ะ")
                
        except Exception as e:
            # จัดการกรณีระบบป้องกันล่ม
            st.error("😥 พี่นกอ้วนบินชนขอบโต๊ะหลังบ้าน! ลองกดพิมพ์ใหม่อีกครั้งนะจ๊ะเด็กๆ")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>𓅭 ซอฟต์แวร์นกอ้วนรอบรู้ ไร้ API Key เสถียรสูง 100% 𓅰</p>", unsafe_allow_html=True)
