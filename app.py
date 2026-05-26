import streamlit as st
import urllib.request
import json

# 1. ตั้งค่าหน้าตาซอฟต์แวร์ (Frontend)
st.set_page_config(
    page_title="AIตัวแม่ที่พร้อมจะช่วยนักเรียนค้นคว้าข้อมูล", 
    page_icon="🎓", 
    layout="centered"
)

st.title("สงสัยอะไรถามได้เลยนะลูก")
st.write("พิมพ์เรื่องที่สงสัยลงไปได้เลยนะลูก")

# 2. กล่องรับคำถามจากนักเรียน (Backend)
user_query = st.text_input("🔍 อยากถามเรื่องอะไรดีลูก?", placeholder="เช่น อธิบายทฤษฎีสัมพัทธภาพ, สรุปรามเกียรติ์, สูตรคณิตศาสตร์")

if user_query:
    with st.spinner("⏳ ฉันกำลังใช้สมองส่วนกลางสแกนความรู้ให้หนูอยู่จ้า รอแป๊บนะแม่นะ..."):
        try:
            # เชื่อมต่อเซิร์ฟเวอร์สมองกลฟรีระดับโลก (ฉลาดระดับเดียวกับ Gemini)
            api_url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
            
            system_instruction = (
                "คุณคือ AI ตัวแม่ผู้รอบรู้และใจดี ทำหน้าที่ตอบคำถามวิชาการให้เด็กนักเรียน "
                "จงตอบเป็นภาษาไทยที่สุภาพ อ่านง่าย แบ่งเป็นข้อๆ ชัดเจน ข้อมูลต้องแน่น ลึกซึ้ง "
                "และห้ามพ่นลิงก์เว็บไซต์เด็ดขาด ให้ตอบเป็นเนื้อหาความรู้ล้วนๆ"
            )
            
            payload = {
                "inputs": f"<|im_start|>system\n{system_instruction}<|im_end|>\n<|im_start|>user\n{user_query}<|im_end|>\n<|im_start|>assistant\n",
                "parameters": {
                    "max_new_tokens": 600, 
                    "temperature": 0.5,
                    "return_full_text": False
                }
            }
            
            req = urllib.request.Request(api_url, data=json.dumps(payload).encode('utf-8'))
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                answer = ""
                if isinstance(result, list) and len(result) > 0:
                    answer = result[0].get('generated_text', '')
                elif isinstance(result, dict):
                    answer = result.get('generated_text', '')
                
                if answer.strip():
                    st.markdown("---")
                    st.subheader("📝 ผลการค้นคว้า:")
                    st.info(answer.strip())
                else:
                    st.warning("สมองกลกำลังประมวลผลคำตอบอยู่ลูก ลองกดส่งคำถามซ้ำอีกทีนะจ๊ะ")
                    
        except Exception as e:
            # แผนสำรองกรณีเซิร์ฟเวอร์นอกคิวยาว ดึงวิกิพีเดียไทยมาแสดงทันทีเพื่อป้องกันตัวแดง
            try:
                import urllib.parse
                encoded_query = urllib.parse.quote(user_query.strip())
                wiki_url = f"https://th.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
                req_wiki = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_wiki) as response_wiki:
                    data_wiki = json.loads(response_wiki.read().decode('utf-8'))
                    answer_wiki = data_wiki.get('extract', '')
                    if answer_wiki:
                        st.markdown("---")
                        st.subheader("📝 ผลการค้นคว้า:")
                        st.info(f"✨ สรุปเนื้อหาสำคัญให้หนูฟังดังนี้ค่ะลูก:\n\n{answer_wiki}")
                    else:
                        st.warning("เรื่องนี้ลึกซึ้งเกินไปลูก ลองใช้คำค้นหาที่สั้นและกระชับขึ้นดูนะจ๊ะ")
            except:
                st.warning("ระบบประมวลผลข้อมูลพร้อมกันเยอะมากเลยลูกแม่ ลองกด Enter อีกทีเพื่อกระตุ้นสมอง AI นะคะ")

# ส่วนท้ายเว็บ
st.markdown("---")
st.caption("พัฒนาด้วย Python + Streamlit | ปลอดภัยสำหรับเด็ก วัยเรียนรักส์การค้นคว้า")
