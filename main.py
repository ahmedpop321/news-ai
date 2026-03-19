import streamlit as st
import google.generativeai as genai

# 1. إعداد المفتاح
API_KEY = "AIzaSyB1mhwJoxgXjxTuRZsveaPCEGr9fCeg7Fk"
genai.configure(api_key=API_KEY)

st.title("🚀 فحص الاتصال بالذكاء الاصطناعي")

# 2. محاولة جلب النماذج المتاحة لمفتاحك
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    st.write("✅ النماذج المتاحة لحسابك هي:", available_models)
    
    # اختيار أول نموذج متاح تلقائياً
    selected_model = available_models[0]
    model = genai.GenerativeModel(selected_model)
    
    # 3. تجربة عملية بسيطة
    text_input = st.text_input("اكتب شيئاً هنا لتجربة الذكاء الاصطناعي:")
    if st.button("تشغيل"):
        response = model.generate_content(text_input)
        st.success(response.text)

except Exception as e:
    st.error(f"❌ فشل الاتصال: {e}")
    st.info("تأكد من أن مفتاح الـ API صحيح ومنشور في Google AI Studio.")
