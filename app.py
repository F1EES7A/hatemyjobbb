import streamlit as st
import urllib.request
import json
import urllib.parse

# 1. ตั้งค่าหน้าตาซอฟต์แวร์ (Frontend)
st.set_page_config(
    page_title="AIตัวแม่ที่พร้อมจะช่วยนักเรียนค้นคว้าข้อมูล", 
    page_icon="🎓", 
    layout="centered"
)

st.title("สงสัยอะไรถามได้เลยนะลูก")
st.write("พิมพ์เรื่องที่สงสัยลงไปได้เลยนะลูก")

# 2. กล่องรับคำถามจากนักเรียน
user_query = st.text_input("🔍 อยากถามเรื่องอะไรดีลูก?", placeholder="เช่น ดวงอาทิตย์, วันสุนทรภู่, ตรีโกณมิติ")

# 3. การทำงานของระบบหลังบ้านสารานุกรมฉลาดแบบ ChatGPT (Backend)
if user_query:
    with st.spinner("⏳ฉันกำลังบินไปหาคว้าข้อมูลให้อยู่จ้า รอแป๊บแม่น้า"):
        try:
            # แปลงข้อความภาษาไทยให้เป็นรหัส URL ที่ระบบเข้าใจ
            encoded_query = urllib.parse.quote(user_query)
            
            # ยิงไปดึงข้อมูลสรุปจาก API ฟรีของ Wikipedia ภาษาไทยโดยตรง (ไม่ต้องใช้คีย์)
            wiki_url = f"https://th.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
            
            req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                # ดึงเฉพาะเนื้อหาบทความสรุปภาษาไทยมาใช้
                answer = data.get('extract', '')
                
                if answer:
                    st.markdown("---")
                    st.subheader("📝 ผลการค้นคว้า:")
                    
                    # จัดรูปแบบคำตอบให้ละมุน แยกเป็นบรรทัดให้อ่านง่ายสไตล์ ChatGPT
                    st.info(f"✨ **สิ่งที่หนูควรรู้เกี่ยวกับ \"{user_query}\" มีดังนี้ค่ะลูก:**\n\n{answer}")
                else:
                    st.warning("หาข้อมูลเรื่องนี้ไม่เจอเลยลูก ลองเปลี่ยนใช้คำค้นหาที่กว้างขึ้นดูนะ")
                    
        except Exception as e:
            # ถ้าค้นคำเฉพาะเจาะจงในคลังวิชาการไม่เจอ ให้ระบบเปลี่ยนไปค้นหาแบบทั่วไปแบบนุ่มนวล
            st.warning("หนูพิมพ์คำค้นหาเจาะจงเกินไป หรือไม่คลังวิชาการยังไม่มีเรื่องนี้ ลองเปลี่ยนเป็นคำค้นหลักสั้นๆ ดูนะลูก (เช่น พิมพ์แค่ 'ดวงอาทิตย์' แทนคำว่า 'ข้อมูลดวงอาทิตย์')")
            
# ส่วนท้ายเว็บ
st.markdown("---")
st.caption("พัฒนาด้วย Python + Streamlit | ปลอดภัยสำหรับเด็ก วัยเรียนรักส์การค้นคว้า")
