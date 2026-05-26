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

# 2. กล่องรับคำถามจากนักเรียน
user_query = st.text_input("🔍 อยากถามเรื่องอะไรดีลูก?", placeholder="เช่น อธิบายกฎของนิวตัน, สรุปประวัติศาสตร์อยุธยาให้ฟังหน่อย")

# 3. การทำงานของระบบหลังบ้านสมองกลอัจฉริยะ (Backend)
if user_query:
    with st.spinner("⏳ฉันกำลังใช้สมองส่วนกลางค้นคว้าและเรียบเรียงข้อมูลแน่นๆ ให้หนูอยู่จ้า รอแป๊บแม่น้า"):
        try:
            # ใช้โมเดลภาษาไทย-อังกฤษระดับโลกที่เปิดให้ใช้ฟรีผ่าน Server สาธารณะ
            api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
            
            # ปรับแต่งคำสั่ง (Prompt) พ่วงไปหลังบ้านเพื่อบังคับให้ AI ตอบกลับมาเป็นภาษาไทยอธิบายยาวๆ แน่นๆ
            full_prompt = f"<|system|>\nคุณคือครูผู้รอบรู้ ตอบคำถามนักเรียนเป็นภาษาไทยอย่างละเอียด ข้อมูลแน่นและถูกต้องตามหลักวิชาการ\n<|user|>\nช่วยอธิบายเรื่องนี้อย่างละเอียด: {user_query}\n<|assistant|>\n"
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 500, # สั่งให้ตอบยาวสะใจ ข้อมูลแน่นๆ
                    "temperature": 0.4,
                    "return_full_text": False
                }
            }
            
            # ส่งข้อมูลไปประมวลผลหลังบ้านแบบเบ็ดเสร็จ
            req = urllib.request.Request(api_url, data=json.dumps(payload).encode('utf-8'))
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # ทำความสะอาดข้อความผลลัพธ์
                answer = ""
                if isinstance(result, list) and len(result) > 0:
                    answer = result[0].get('generated_text', '')
                elif isinstance(result, dict):
                    answer = result.get('generated_text', '')
                
                if answer:
                    # แสดงผลลัพธ์บนหน้าเว็บแบบจัดเต็ม ข้อมูลหนาแน่น
                    st.markdown("---")
                    st.subheader("📝 ผลการค้นคว้า:")
                    st.info(answer.strip())
                else:
                    st.warning("สมองกลกำลังปรับปรุงข้อมูล ลองกดส่งคำถามใหม่อีกครั้งนะลูก")
                    
        except Exception as e:
            # แผนสำรอง: หาก Server ฟรีคิวยาวเกินไป ให้ใช้ระบบสารานุกรมภาษาไทยทันทีเพื่อไม่ให้เด็กหน้าแตก
            try:
                import urllib.parse
                encoded_query = urllib.parse.quote(user_query)
                wiki_url = f"https://th.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"
                req_wiki = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_wiki) as response_wiki:
                    data_wiki = json.loads(response_wiki.read().decode())
                    answer_wiki = data_wiki.get('extract', '')
                    if answer_wiki:
                        st.markdown("---")
                        st.subheader("📝 ผลการค้นคว้า (ระบบสารานุกรมสำรอง):")
                        st.info(answer_wiki)
                    else:
                        st.warning("หาข้อมูลเรื่องนี้ไม่เจอเลยลูก ลองใช้คำค้นหาที่กว้างขึ้นดูนะ")
            except:
                st.error("😥 ตอนนี้สมองกลประมวลผลหนักเกินไป ลองกดพิมพ์ถามใหม่อีกทีนะลูกแม่")

# ส่วนท้ายเว็บ
st.markdown("---")
st.caption("พัฒนาด้วย Python + Streamlit | ปลอดภัยสำหรับเด็ก วัยเรียนรักส์การค้นคว้า")

