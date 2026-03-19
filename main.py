import streamlit as st
import google.generativeai as genai

# --- 1. الإعدادات ومفتاح الـ API ---
API_KEY = "AIzaSyB1mhwJoxgXjxTuRZsveaPCEGr9fCeg7Fk" # مفتاحك الذي أرسلته
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. واجهة المستخدم بتصميم أنيق ---
st.set_page_config(page_title="محرر الأخبار الذكي", layout="wide")

st.markdown("""
    <style>
    body { direction: rtl; text-align: right; }
    .stButton>button { background-color: #2E7D32; color: white; border-radius: 10px; }
    .news-card { background-color: #f9f9f9; padding: 15px; border-radius: 10px; border-right: 5px solid #2E7D32; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("?? أداة صياغة الأخبار والمنشورات الذكية")

# --- 3. قائمة الأخبار اليومية (تجميع تلقائي محاكي) ---
st.sidebar.header("?? أخبار اليوم المجمعة")
# ملاحظة: هنا يمكنك مستقبلاً وضع كود RSS Scraper لجلبها من الجزيرة أو CNN
news_list = {
    "تقنية": "شركة آبل تعلن عن تحديث جديد لنظام iOS يضيف ميزات ذكاء اصطناعي متطورة.",
    "اقتصاد": "ارتفاع مؤشرات البورصة العالمية بنسبة 2% بعد تصريحات البنك الفيدرالي.",
    "رياضة": "انتقال لاعب عالمي إلى الدوري السعودي في صفقة قياسية."
}

selection = st.sidebar.radio("اختر خبراً لمعالجته:", list(news_list.keys()))
original_text = news_list[selection]

# عرض الخبر الأصلي
st.markdown(f'<div class="news-card"><b>الخبر الأصلي:</b><br>{original_text}</div>', unsafe_allow_html=True)

# --- 4. العمليات الذكية ---
col1, col2 = st.columns(2)

with col1:
    if st.button("?? إعادة صياغة احترافية"):
        with st.spinner("جاري الكتابة..."):
            prompt = f"أعد صياغة هذا الخبر بأسلوب إبداعي جذاب لفيسبوك وتويتر مع إيموجي: {original_text}"
            response = model.generate_content(prompt)
            st.success("النسخة الجديدة جاهزة:")
            st.text_area("انسخ من هنا:", value=response.text, height=150)

with col2:
    if st.button("?? تعديل وتوليد صورة"):
        with st.spinner("جاري تصميم وصف الصورة..."):
            prompt_img = f"بناءً على هذا الخبر: {original_text}، اكتب وصفاً لصورة (Prompt) بالإنجليزية لاستخدامها في Midjourney."
            response_img = model.generate_content(prompt_img)
            st.info("وصف الصورة المقترح:")
            st.code(response_img.text, language="text")

# --- 5. ميزة الإدخال اليدوي ---
st.divider()
st.subheader("?? أو أدخل منشورك الخاص يدوياً")
custom_input = st.text_area("ضع أي نص هنا لإعادة صياغته:")
if st.button("معالجة النص اليدوي"):
    res = model.generate_content(f"أعد صياغة هذا النص: {custom_input}")
    st.write(res.text)
