import streamlit as st
import google.generativeai as genai
import datetime

# הגדרת המפתח
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # התיקון: שימוש במודל ללא קידומת models/ ובלי v1beta
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("חסר מפתח API ב-Secrets")

st.set_page_config(page_title="BodyTrack AI", layout="wide")

# עיצוב RTL
st.markdown("""<style>
    .main { direction: RTL; text-align: right; background-color: #050a0e; color: white; }
    .stButton>button { background: #00ff88; color: black; width: 100%; border-radius: 10px; }
    </style>""", unsafe_allow_html=True)

st.title("⚡ BodyTrack AI Pro")
tabs = st.tabs(["🏋️ אימון", "🥗 תפריט", "✅ יומן"])

with tabs[0]:
    goal = st.selectbox("מטרה:", ["בניית שריר", "חיטוב"])
    if st.button("צור תוכנית"):
        with st.spinner("חושב..."):
            try:
                response = model.generate_content(f"צור תוכנית אימון ל{goal} בעברית")
                st.write(response.text)
            except Exception as e:
                st.error(f"שגיאה: {e}")

with tabs[1]:
    if st.button("צור תפריט"):
        with st.spinner("בונה תפריט..."):
            try:
                response = model.generate_content("צור תפריט יומי עשיר בחלבון למתאמן בעברית")
                st.success(response.text)
            except Exception as e:
                st.error(f"שגיאה: {e}")

with tabs[2]:
    st.subheader("סיכום יום")
    w = st.checkbox("התאמנתי היום")
    f = st.checkbox("אכלתי נכון")
    if w and f:
        st.balloons()
        st.success("אלוף! יום מושלם.")
