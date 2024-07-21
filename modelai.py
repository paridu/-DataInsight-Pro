# สร้างโมเดล
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# ส่งคำสั่ง (Prompt) และรับผลลัพธ์
response = model.generate_content("The opposite of hot is")
print(response.text)
