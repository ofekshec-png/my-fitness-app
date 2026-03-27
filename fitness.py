import streamlit as st
import google.generativeai as genai
import datetime
import json

# ─────────────────────────────────────────────
# הגדרות עמוד
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BodyTrack AI Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# עיצוב RTL + סגנון כהה מתקדם
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    direction: RTL !important;
    text-align: right !important;
    font-family: 'Assistant', sans-serif !important;
    background-color: #0b0f14 !important;
    color: #e8eaf0 !important;
}

[data-testid="stHeader"] { background: transparent !important; }

h1, h2, h3, h4, p, span, div, label {
    text-align: right !important;
    direction: RTL !important;
    font-family: 'Assistant', sans-serif !important;
}

.card {
    background: linear-gradient(135deg, #141921, #1a2130);
    border: 1px solid #2a3445;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

.stButton > button {
    background: linear-gradient(135deg, #00e676, #00b248) !important;
    color: #000 !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px 28px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    font-family: 'Assistant', sans-serif !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,230,118,0.35) !important;
}

.stTabs [data-baseweb="tab-list"] {
    direction: RTL !important;
    gap: 6px !important;
    justify-content: center !important;
    background: #141921 !important;
    border-radius: 14px !important;
    padding: 6px !important;
    border: 1px solid #2a3445 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: #8892a4 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 10px 20px !important;
    font-family: 'Assistant', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00e676, #00b248) !important;
    color: #000 !important;
}

div[role="radiogroup"] { direction: RTL !important; }

.stSelectbox > div > div {
    background: #141921 !important;
    border: 1px solid #2a3445 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
}

.stNumberInput input {
    background: #141921 !important;
    border: 1px solid #2a3445 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    text-align: center !important;
}
.stTextInput input, .stTextArea textarea {
    background: #141921 !important;
    border: 1px solid #2a3445 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    direction: RTL !important;
}

[data-testid="stMetric"] {
    background: #141921 !important;
    border: 1px solid #2a3445 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricValue"] { color: #00e676 !important; font-size: 2rem !important; }
[data-testid="stMetricLabel"] { color: #8892a4 !important; }

.stSlider { direction: LTR !important; }

.ai-result {
    background: linear-gradient(135deg, #0d1117, #141921);
    border: 1px solid #00e676;
    border-radius: 14px;
    padding: 20px;
    line-height: 1.9;
    direction: RTL;
    text-align: right;
    white-space: pre-wrap;
}

.badge {
    display: inline-block;
    background: linear-gradient(135deg, #00e676, #00b248);
    color: #000;
    font-weight: 800;
    font-size: 0.8rem;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# חיבור ל-Gemini
# ─────────────────────────────────────────────
model = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
    else:
        st.error("⚠️ מפתח API חסר. הוסף GOOGLE_API_KEY ב-Streamlit Secrets.")
except Exception as e:
    st.error(f"❌ שגיאת חיבור: {e}")


# ─────────────────────────────────────────────
# פונקציית AI עם טיפול בשגיאות
# ─────────────────────────────────────────────
def ask_ai(prompt: str) -> str:
    if model is None:
        return "❌ אין חיבור ל-AI. בדוק את מפתח ה-API."
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(max_output_tokens=1500, temperature=0.7)
        )
        return response.text
    except Exception as e:
        err = str(e)
        if "429" in err:
            return "⏳ חרגת ממכסת הבקשות. המתן מספר שניות ונסה שוב."
        elif "quota" in err.lower():
            return "⚠️ מכסת ה-API אזלה. הפעל חיוב ב-Google AI Studio."
        return f"❌ שגיאה: {e}"


# ─────────────────────────────────────────────
# Session State ליומן
# ─────────────────────────────────────────────
if "journal" not in st.session_state:
    st.session_state.journal = []

# ─────────────────────────────────────────────
# כותרת ראשית
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 30px 0 10px;">
    <h1 style="font-size:2.8rem; font-weight:800; text-align:center !important;
               background: linear-gradient(135deg,#00e676,#00b248);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        ⚡ BodyTrack AI Pro
    </h1>
    <p style="color:#8892a4; font-size:1.1rem; text-align:center !important;">
        תוכנית אימון · תזונה · מעקב · AI חכם
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# טאבים
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏋️ תוכנית אימון",
    "🥗 תפריט תזונה",
    "📊 מדדי גוף",
    "✅ יומן מעקב"
])

# ══════════════════════════════════════════════
# טאב 1 — תוכנית אימון
# ══════════════════════════════════════════════
with tab1:
    st.markdown("### 🏋️ בניית תוכנית אימון אישית")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        gender   = st.radio("מין", ["גבר", "אישה"], horizontal=True, key="t1_gender")
        location = st.radio("מיקום אימון", ["חדר כושר", "בית (משקל גוף)", "פארק / גינת כושר"], horizontal=True)
        goal     = st.selectbox("מטרת האימון", [
            "בניית מסת שריר", "חיטוב וירידה בשומן",
            "כוח מתפרץ", "סיבולת ואנרגיה", "שיפור כושר כללי"
        ])
    with col2:
        level    = st.selectbox("רמת כושר", ["מתחיל", "בינוני", "מתקדם"])
        days     = st.slider("ימי אימון בשבוע", 1, 7, 4)
        duration = st.slider("אורך אימון (דקות)", 20, 120, 60, step=10)

    extra = st.text_input("הגבלות / פציעות / הערות (אופציונלי)", placeholder="לדוגמה: כאב ברך, אסור כריעות...")

    if st.button("⚡ בנה לי תוכנית אימון", key="btn_workout"):
        with st.spinner("🤖 AI בונה תוכנית אישית..."):
            prompt = f"""
אתה מאמן כושר מקצועי. צור תוכנית אימון שבועית מפורטת עבור:
- מין: {gender} | רמת כושר: {level} | מטרה: {goal}
- מיקום: {location} | ימי אימון: {days} | אורך: {duration} דקות
- הגבלות: {extra if extra else 'אין'}

בנה {days} ימי אימון. לכל יום: שם הקבוצות, חימום 5 דקות, רשימת תרגילים (שם, סטים, חזרות, מנוחה), קירור 5 דקות.
הוסף טיפ מקצועי אחד בסוף. כתוב בעברית ברורה.
"""
            result = ask_ai(prompt)
            st.markdown(f'<div class="ai-result">{result}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# טאב 2 — תפריט תזונה
# ══════════════════════════════════════════════
with tab2:
    st.markdown("### 🥗 בניית תפריט תזונה אישי")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        gender_n = st.radio("מין", ["גבר", "אישה"], horizontal=True, key="t2_gender")
        nut_goal = st.selectbox("יעד תזונתי", ["מסה (עלייה במשקל)", "חיטוב (ירידה בשומן)", "תחזוקה"])
        meals    = st.slider("מספר ארוחות ביום", 3, 6, 4)
    with col2:
        weight_n = st.number_input('משקל (ק"ג)', 40.0, 200.0, 75.0, key="t2_weight")
        height_n = st.number_input('גובה (ס"מ)', 140, 220, 175, key="t2_height")
        activity = st.selectbox("רמת פעילות", ["נמוכה (1-2 ימים)", "בינונית (3-4 ימים)", "גבוהה (5+ ימים)"])

    allergies = st.text_input("אלרגיות / מגבלות תזונתיות", placeholder="לדוגמה: צמחוני, ללא גלוטן...")

    if st.button("🥗 צור תפריט יומי", key="btn_diet"):
        with st.spinner("🤖 AI מחשב תפריט מותאם..."):
            if gender_n == "גבר":
                bmr = 10 * weight_n + 6.25 * height_n - 5 * 25 + 5
            else:
                bmr = 10 * weight_n + 6.25 * height_n - 5 * 25 - 161

            act_map = {"נמוכה (1-2 ימים)": 1.375, "בינונית (3-4 ימים)": 1.55, "גבוהה (5+ ימים)": 1.725}
            tdee = int(bmr * act_map[activity])

            if "מסה" in nut_goal:
                cal_target = tdee + 300
            elif "חיטוב" in nut_goal:
                cal_target = tdee - 400
            else:
                cal_target = tdee

            prompt = f"""
אתה דיאטן ספורט מקצועי. צור תפריט יומי מפורט:
- {gender_n}, {weight_n}ק"ג, {height_n}ס"מ | יעד: {nut_goal}
- יעד קלורי: ~{cal_target} קק"ל | {meals} ארוחות | מגבלות: {allergies if allergies else 'אין'}

לכל ארוחה: שם, מרכיבים + כמויות, קלוריות משוערות.
סיכום יומי: קלוריות / חלבון / פחמימות / שומן.
2 טיפים תזונתיים מעשיים. כתוב בעברית.
"""
            st.info(f"📊 יעד קלורי: **{cal_target} קק\"ל/יום** | TDEE: {tdee} קק\"ל")
            result = ask_ai(prompt)
            st.markdown(f'<div class="ai-result">{result}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# טאב 3 — מדדי גוף
# ══════════════════════════════════════════════
with tab3:
    st.markdown("### 📊 מחשבון מדדי גוף")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        weight_b = st.number_input('משקל (ק"ג)', 30.0, 200.0, 75.0, key="bmi_w")
    with col2:
        height_b = st.number_input('גובה (ס"מ)', 100, 250, 175, key="bmi_h")
    with col3:
        age_b = st.number_input('גיל', 10, 100, 25)

    gender_b = st.radio("מין", ["גבר", "אישה"], horizontal=True, key="bmi_g")

    if height_b > 0:
        bmi = weight_b / ((height_b / 100) ** 2)

        if bmi < 18.5:
            bmi_label, bmi_color = "תת משקל", "#64b5f6"
        elif bmi < 25:
            bmi_label, bmi_color = "משקל תקין ✅", "#00e676"
        elif bmi < 30:
            bmi_label, bmi_color = "עודף משקל", "#ffb74d"
        else:
            bmi_label, bmi_color = "השמנה", "#ff5252"

        if gender_b == "גבר":
            bmr_b = 10 * weight_b + 6.25 * height_b - 5 * age_b + 5
        else:
            bmr_b = 10 * weight_b + 6.25 * height_b - 5 * age_b - 161

        ideal_min = 18.5 * (height_b / 100) ** 2
        ideal_max = 24.9 * (height_b / 100) ** 2

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("BMI", f"{bmi:.1f}", bmi_label)
        c2.metric("BMR", f"{int(bmr_b)} קק\"ל", "בזאלי ביום")
        c3.metric("משקל מינימלי", f"{ideal_min:.1f} ק\"ג")
        c4.metric("משקל מקסימלי", f"{ideal_max:.1f} ק\"ג")

        st.markdown(f"""
        <div class="card" style="border-color:{bmi_color}; margin-top:16px;">
            <div class="badge">ניתוח BMI</div>
            <h3 style="color:{bmi_color}; margin:0 0 8px;">סיווג: {bmi_label}</h3>
            <p>טווח משקל אידאלי: <strong>{ideal_min:.1f} – {ideal_max:.1f} ק"ג</strong></p>
            <p>BMR (קלוריות בזאלי): <strong>{int(bmr_b)} קק"ל/יום</strong></p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🤖 קבל המלצות AI לפי המדדים שלי", key="btn_bmi_ai"):
            with st.spinner("מנתח מדדים..."):
                prompt = f"""
{gender_b} גיל {age_b}, {weight_b}ק"ג, {height_b}ס"מ. BMI: {bmi:.1f} ({bmi_label}), BMR: {int(bmr_b)}.
ספק: ניתוח קצר, 3 המלצות תזונה, 3 המלצות אימון, יעד משקל ריאלי ל-3 חודשים. עברית ידידותית.
"""
                result = ask_ai(prompt)
                st.markdown(f'<div class="ai-result">{result}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# טאב 4 — יומן מעקב
# ══════════════════════════════════════════════
with tab4:
    st.markdown("### ✅ יומן מעקב יומי")
    st.markdown("---")

    today = datetime.date.today()
    st.markdown(f"#### 📅 {today.strftime('%d/%m/%Y')}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🏋️ אימון**")
        w_done   = st.checkbox("ביצעתי אימון היום")
        w_type   = st.text_input("סוג האימון", placeholder="לדוגמה: רגליים, ריצה 5ק\"מ...")
        w_rating = st.slider("עצימות (1-10)", 1, 10, 7, key="w_rate")

    with col2:
        st.markdown("**🥗 תזונה**")
        f_done    = st.checkbox("אכלתי לפי התפריט")
        f_water   = st.slider("כוסות מים", 0, 15, 8, key="f_water")
        f_feeling = st.select_slider("תחושה כללית", ["גרוע", "לא טוב", "בסדר", "טוב", "מצוין"], value="טוב")

    notes = st.text_area("📝 הערות", placeholder="מה הרגשת? מה הלך טוב? מה לשפר?", height=100)

    if st.button("💾 שמור יומן להיום", key="btn_journal"):
        entry = {
            "date": str(today),
            "workout_done": w_done,
            "workout_type": w_type,
            "workout_intensity": w_rating,
            "diet_done": f_done,
            "water_cups": f_water,
            "feeling": f_feeling,
            "notes": notes
        }
        st.session_state.journal = [e for e in st.session_state.journal if e["date"] != str(today)]
        st.session_state.journal.append(entry)

        if w_done and f_done:
            st.balloons()
            st.success("🏆 יום מושלם! אימון + תזונה — אלוף אמיתי!")
        elif w_done or f_done:
            st.success("✅ יומן נשמר! המשך כך 💪")
        else:
            st.info("📝 יומן נשמר. מחר מתחילים מחדש!")

    if st.session_state.journal:
        st.markdown("---")
        st.markdown("### 📈 היסטוריית יומן")

        total     = len(st.session_state.journal)
        workouts  = sum(1 for e in st.session_state.journal if e["workout_done"])
        diet_days = sum(1 for e in st.session_state.journal if e["diet_done"])

        c1, c2, c3 = st.columns(3)
        c1.metric("ימים מוקלטים", total)
        c2.metric("אימונים שבוצעו", f"{workouts}/{total}")
        c3.metric("ימי תזונה נכונה", f"{diet_days}/{total}")

        st.markdown("#### 5 הימים האחרונים:")
        for entry in reversed(st.session_state.journal[-5:]):
            w_icon = "✅" if entry["workout_done"] else "❌"
            f_icon = "✅" if entry["diet_done"] else "❌"
            st.markdown(
                f"**{entry['date']}** | אימון: {w_icon} {entry.get('workout_type','')} | "
                f"תזונה: {f_icon} | מים: {entry['water_cups']} כוסות | תחושה: {entry['feeling']}"
            )

        if st.button("🤖 ניתוח AI של ההתקדמות שלי", key="btn_progress"):
            with st.spinner("מנתח נתונים..."):
                summary = json.dumps(st.session_state.journal[-7:], ensure_ascii=False)
                prompt = f"""
נתוני מעקב 7 ימים אחרונים: {summary}
ספק: סיכום התקדמות, נקודות חזקות, נקודות לשיפור, 3 המלצות לשבוע הבא. עברית מעודדת.
"""
                result = ask_ai(prompt)
                st.markdown(f'<div class="ai-result">{result}</div>', unsafe_allow_html=True)
