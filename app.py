import streamlit as st
from duckduckgo_search import DDGS

# =================================================================
# 🎨 1. หน้าบ้านธีมนกอ้วน (FRONTEND DESIGN)
# =================================================================
st.set_page_config(
    page_title="พี่นกอ้วน ค้นปุ๊บเจอเขียนปั๊บ",
    page_icon="🐦",
    layout="centered"
)

# แต่งหน้าตาเว็บให้สดใส น่ารัก เหมาะกับเด็กๆ
st.markdown("""
    <style>
    .main-title { color: #FF914D; font-family: 'Kanit', sans-serif; text-align: center; font-weight: bold; }
    .sub-title { color: #555555; text-align: center; margin-bottom: 25px; font-size: 1.1em; }
    .stTextInput>div>div>input { border-radius: 20px; border: 2px solid #FF914D; padding: 12px; font-size: 1.1em; }
    .bird-box { background-color: #FFF3EB; padding: 20px; border-radius: 20px; border-left: 8px solid #FF914D; margin-bottom: 25px; }
    .result-box { background-color: #F0F4FF; padding: 20px; border-radius: 15px; border-left: 6px solid #2E5BFF; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>𓅭 พี่นกอ้วน ค้นไวได้ความรู้ 𓅰</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='bird-box'>
    <h3 style='margin-top:0; color:#FF731D;'>👋 สวัสดีจ้าเด็กๆ! พิมพ์คำถามได้เลย</h3>
    <p>พี่นกอ้วนเตรียมข้อมูลจากห้องสมุดทั่วโลกไว้ให้แล้ว ค้นปุ๊บแสดงคำตอบปั๊บทันใจแน่นอนจ้า!</p>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 🧠 2. ระบบหลังบ้านเสิร์ชเอนจินความเร็วสูง (BACKEND)
# =================================================================

# กล่องรับคำถามจากเด็กๆ
user_query = st.text_input(
    "💬 หนูอยากรู้เรื่องอะไร พิมพ์บอกพี่นกอ้วนเลยจ้า:", 
    placeholder="เช่น ทำไมท้องฟ้าถึงเป็นสีฟ้า?, ประวัติศาสตร์วันสุนทรภู่"
)

if user_query:
    # สั่งให้ระบบทำงานทันที
    with st.spinner("𓅭 พี่นกอ้วนกำลังกางปีกบินไปคาบข้อมูลมาให้ใน 1 วินาที..."):
        try:
            # ใช้ระบบค้นหาข้อมูลภาษาไทยหลังบ้านแบบไม่ต้องใช้คีย์
            with DDGS() as ddgs:
                search_results = [r for r in ddgs.text(user_query, region="th-th", max_results=3)]
            
            if search_results:
                # พ่นผลลัพธ์ออกหน้าจอทันที
                st.markdown("---")
                st.balloons() # เอฟเฟกต์ลูกโป่งลอยฉลองความสำเร็จ 🎈
                st.markdown(f"### 📝 ผลการค้นคว้าเรื่อง: **{user_query}**")
                
                # แสดงเนื้อหาสรุปที่ดึงมาได้แบบอ่านง่าย แยกเป็นกล่องๆ
                for i, result in enumerate(search_results[:2]): # เอาตัวเด็ดๆ มาโชว์ 2 เรื่อง
                    st.markdown(f"""
                    <div class='result-box'>
                        <b style='color:#2E5BFF; font-size:1.1em;'>💡 ข้อมูลสรุปชุดที่ {i+1}</b><br><br>
                        {result['body']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # แปะลิงก์อ้างอิงให้เด็กๆ คลิกไปอ่านเพิ่มเผื่อทำรายงาน
                st.markdown("<br>🔗 **แหล่งข้อมูลอ้างอิงสำหรับไปศึกษาต่อจ้า:**", unsafe_allow_html=True)
                for res in search_results:
                    st.markdown(f" * [{res['title']}]({res['href']})")
                    
            else:
                st.warning("𓅭 พี่นกอ้วนหาเรื่องนี้ไม่เจอ ลองเปลี่ยนไปใช้คำค้นหาอื่นดูนะจ๊ะเด็กๆ")
                
        except Exception as e:
            st.error("😥 ระบบขัดข้องเล็กน้อย ลองกดเอนเทอร์หรือพิมพ์คำถามใหม่อีกครั้งนะจ๊ะ")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>𓅭 ซอฟต์แวร์นกอ้วนค้นไว ปลอดภัย ไร้ API Key 100% 𓅰</p>", unsafe_allow_html=True)
