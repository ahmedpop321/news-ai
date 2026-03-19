import streamlit as st
import google.generativeai as genai

# --- 1. الإعدادات ومفتاح الـ API ---
API_KEY = "AIzaSyB1mhwJoxgXjxTuRZsveaPCEGr9fCeg7Fk" 
genai.configure(api_key=API_KEY)

# وظيفة لاختيار أفضل نموذج متاح تلقائياً
def get_available_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # نفضل v1.5 flash إذا وجد، وإلا نختار أول واحد متاح
        for m in models:
            if 'gemini-1.5-flash' in m:
                return m
        return models[0] if models else 'gemini-pro'
    except:
        return 'gemini-pro'

selected_model_name = get_available_model()
model = genai.GenerativeModel(selected_model_name)

# --- 2. واجهة المستخدم ---
st.set_page_config(page_title="محرر الأخبار الذكي", layout="wide")

st.title("🤖 أداة صياغة الأخبار الذكية")
st.caption(f"النموذج المستخدم حالياً: {selected_model_name}")

# --- 3. قائمة الأخبار اليومية ---
st.sidebar.header("📅 أخبار اليوم")
news_list = {
    "تقنية": "شركة آبل تعلن عن تحديث جديد لنظام iOS يضيف ميزات ذكاء اصطناعي متطورة.",
    "اقتصاد": "ارتفاع مؤشرات البورصة العالمية بنسبة 2% بعد تصريحات البنك الفيدرالي.",
    "رياضة": "انتقال لاعب عالمي إلى الدوري السعودي في صفقة قياسية."
}

selection = st.sidebar.radio("اختر خبراً:", list(news_list.keys()))
original_text = news_list[selection]

st.info(f"**الخبر الأصلي:** {original_text}")

# --- 4. العمليات ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 إعادة صياغة النص"):
        with st.spinner("جاري المعالجة..."):
            try:
                prompt = f"أعد صياغة هذا الخبر بأسلوب جذاب مع إيموجي: {original_text}"
                response = model.generate_content(prompt)
                st.success("النتيجة:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الصياغة: {e}")

with col2:
    if st.button("🎨 وصف الصورة"):
        with st.spinner("جاري الابتكار..."):
            try:
                prompt_img = f"Describe a professional news image for: {original_text}"
                response_img = model.generate_content(prompt_img)
                st.info("وصف الصورة:")
                st.write(response_img.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء وصف الصورة: {e}")
