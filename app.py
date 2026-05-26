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
user_query = st.text_input("🔍 อยากถามเรื่องอะไรดีลูก?", placeholder="เช่น ระบบสุริยะ, วันสุนทรภู่, กฎของนิวตัน, ตรีโกณมิติ")

# 3. การทำงานของระบบหลังบ้านสารานุกรมความรู้แน่น (Backend)
if user_query:
    with st.spinner("⏳ฉันกำลังใช้สมองส่วนกลางค้นคว้าและเรียบเรียงข้อมูลแน่นๆ ให้หนูอยู่จ้า รอแป๊บแม่น้า"):
        try:
            # คลีนข้อความและแปลงภาษาไทยให้เป็นรหัส URL 
            clean_query = user_query.strip()
            encoded_query = urllib.parse.quote(clean_query)
            
            # ยิงไปดึงคลังสารานุกรมวิชาการไทยโดยตรง (เสถียรที่สุด ไม่ตอบเพี้ยน)
            wiki_url = f"https://th.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1&titles={encoded_query}"
            
            req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                pages = data.get('query', {}).get('pages', {})
                
                answer = ""
                for page_id, page_data in pages.items():
                    if page_id != "-1": 
                        answer = page_data.get('extract', '')
                
                if answer:
                    st.markdown("---")
                    st.subheader("📝 ผลการค้นคว้า:")
                    
                    # ตัดเอาเนื้อหามาแสดงแบบหนาแน่น สาระเน้นๆ ตรงคำถามชัวร์
                    # แสดงแค่ 1,500 ตัวอักษรแรกเพื่อให้ยาวกำลังดี ดึงเฉพาะใจความสำคัญ
                    short_answer = answer[:1500] + "..." if len(answer) > 1500 else answer
                    
                    st.info(f"✨ **สรุปข้อมูลเรื่อง \"{user_query}\" ให้หนูฟังอย่างละเอียดดังนี้ค่ะลูก:**\n\n{short_answer}")
                else:
                    # ถ้าค้นแบบตรงตัวไม่เจอ ให้สลับไปค้นแบบคำใกล้เคียงทันทีเพื่อป้องกันเว็บค้าง
                    search_url = f"https://th.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&format=json"
                    req_search = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
                    
                    with urllib.request.urlopen(req_search) as search_res:
                        s_data = json.loads(search_res.read().decode('utf-8'))
                        s_results = s_data.get('query', {}).get('search', [])
                        
                        if s_results:
                            # ดึงหัวข้อที่ใกล้เคียงที่สุดมาค้นรอบสองอัตโนมัติ
                            next_title = urllib.parse.quote(s_results[0]['title'])
                            wiki_url2 = f"https://th.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&explaintext=1&titles={next_title}"
                            req2 = urllib.request.Request(wiki_url2, headers={'User-Agent': 'Mozilla/5.0'})
                            
                            with urllib.request.urlopen(req2) as res2:
                                data2 = json.loads(res2.read().decode('utf-8'))
                                pages2 = data2.get('query', {}).get('pages', {})
                                for p_id, p_data in pages2.items():
                                    answer2 = p_data.get('extract', '')
                                    
                            if answer2:
                                st.markdown("---")
                                st.subheader("📝 ผลการค้นคว้า:")
                                short_answer2 = answer2[:1500] + "..." if len(answer2) > 1500 else answer2
                                st.info(f"✨ **สรุปข้อมูลเรื่อง \"{s_results[0]['title']}\" ให้หนูฟังดังนี้ค่ะลูก:**\n\n{short_answer2}")
                            else:
                                st.warning("หาข้อมูลเรื่องนี้ไม่เจอเลยลูก ลองใช้คำค้นหาหลักสั้นๆ ดูนะจ๊ะ")
                        else:
                            st.warning("หาข้อมูลเรื่องนี้ไม่เจอเลยลูก ลองใช้คำค้นหาหลักสั้นๆ ดูนะจ๊ะ")
                    
        except Exception as e:
            st.warning("ระบบประมวลผลข้อมูลหนาแน่นมากลูก ลองกด Enter อีกทีเพื่อรีเฟรชข้อมูลนะลูกแม่")

# ส่วนท้ายเว็บ
st.markdown("---")
st.caption("พัฒนาด้วย Python + Streamlit | ปลอดภัยสำหรับเด็ก วัยเรียนรักส์การค้นคว้า")
