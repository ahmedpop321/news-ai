import streamlit as st
import google.generativeai as genai

# --- 1. الإعدادات ومفتاح الـ API ---
# تأكد أن هذا هو مفتاحك الصحيح
API_KEY = "AIzaSyB1mhwJoxgXjxTuRZsveaPCEGr9fCeg7Fk" 
genai.configure(api_key=API_KEY)

# وظيفة ذكية لجلب اسم أول نموذج متاح يعمل في حسابك لتفادي خطأ 404
@st.cache_resource
def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # يعيد الاسم الكامل مثل models/gemini-1.5-flash
                return m.name
        return "models/gemini-1.5-flash" 
    except Exception:
        return "models/gemini-1.5-flash"

model_name = get_working_model()
model = genai.GenerativeModel(model_name)

# --- 2. واجهة المستخدم ---
st.set_page_config(page_title="محرر الأخبار الذكي", layout="wide")

# تصميم الواجهة باللغة العربية
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
        width: 100%;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📰 محرر الأخبار بالذكاء الاصطناعي")
st.info(f"🟢 متصل حالياً عبر نموذج: `{model_name}`")

# --- 3. جلب الخبر من القائمة ---
st.sidebar.header("🗂️ المصادر المتاحة")
news_data = {
    "تقنية": "أعلنت شركات التقنية الكبرى عن دمج نماذج الذكاء الاصطناعي التوليدي في أنظمة التشغيل القادمة لتسهيل تجربة المستخدم.",
    "فضاء": "ناسا تنجح في استقبال بيانات من مسبار فضائي بعيد باستخدام تقنية الليزر المتطورة لأول مرة.",
    "صحة": "دراسة جديدة تؤكد أن النوم المنتظم يحسن من كفاءة الذاكرة الطويلة لدى البالغين بنسبة 30%."
}

choice = st.sidebar.selectbox("اختر خبراً لمعالجته:", list(news_data.keys()))
content = news_data[choice]

st.subheader("📄 الخبر الأصلي:")
st.write(content)

st.divider()

# --- 4. الأزرار والعمليات ---
col1, col2 = st.columns(2)

with col1:
    if st.button("✨ إعادة صياغة إبداعية"):
        with st.spinner("جاري المعالجة..."):
            try:
                prompt = f"أعد صياغة هذا الخبر بأسلوب صحفي عصري مع إيموجي وعناوين: {content}"
                response = model.generate_content(prompt)
                st.success("✅ الصياغة الجديدة:")
                st.write(response.text)
            except Exception as e:
                st.error(f"خطأ في الصياغة: {e}")

with col2:
    if st.button("🎨 وصف صورة للخبر"):
        with st.spinner("جاري ابتكار وصف..."):
            try:
                prompt_img = f"Write a detailed image generation prompt for this news in English: {content}"
                response_img = model.generate_content(prompt_img)
                st.success("✅ وصف الصورة المقترح:")
                st.code(response_img.text, language="text")
            except Exception as e:
                st.error(f"خطأ في الوصف: {e}")

# --- 5. إدخال يدوي ---
st.divider()
user_input = st.text_area("✍️ أو أدخل نصاً من عندك هنا:")
if st.button("معالجة النص المكتوب"):
    if user_input:
        res = model.generate_content(user_input)
        st.write(res.text)
    else:
        st.warning("يرجى كتابة نص أولاً.")
