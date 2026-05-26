import streamlit as st
from duckduckgo_search import DDGS

# 1. ตั้งค่าหน้าตาซอฟต์แวร์ (Frontend)
st.set_page_config(
    page_title="AIตัวแม่ที่พร้อมจะช่วยนักเรียนค้นคว้าข้อมูล", 
    page_icon="🎓", 
    layout="centered"
)

st.title("สงสัยอะไรถามได้เลยนะลูก")
st.write("พิมพ์เรื่องที่สงสัยลงไปได้เลยนะลูก")

# 2. กล่องรับคำถามจากนักเรียน
user_query = st.text_input("🔍 อยากถามเรื่องอะไรดีลูก?", placeholder="เช่น สูตรตรีโกณมิติ ")

# 3. การทำงานของระบบ (Backend) - ปรับเป็นแบบไม่ใช้ API Key 
if user_query:
    with st.spinner("⏳ฉันกำลังบินไปหาคว้าข้อมูลให้อยู่จ้า รอแป๊บแม่น้า"):
        try:
            # ดึงข้อมูลจากอินเทอร์เน็ตสดๆ มาตอบทันทีโดยไม่ต้องง้อคีย์
            with DDGS() as ddgs:
                search_results = [r for r in ddgs.text(user_query, region="th-th", max_results=2)]
            
            if search_results:
                # แสดงผลลัพธ์บนหน้าเว็บแบบคลีนๆ ตามโครงสร้างเดิม
                st.markdown("---")
                st.subheader("📝 ผลการค้นคว้า:")
                
                # รวมเนื้อหาจากแหล่งข้อมูลมาแสดงให้เด็กอ่าน
                for result in search_results:
                    st.write(result['body'])
            else:
                st.warning("หาข้อมูลเรื่องนี้ไม่เจอเลยลูก ลองเปลี่ยนคำถามดูนะ")
                
        except Exception as e:
            st.error(format(e))

# ส่วนท้ายเว็บ
st.markdown("---")
st.caption("พัฒนาด้วย Python + Streamlit | ปลอดภัยสำหรับเด็ก วัยเรียนรักส์การค้นคว้า")
