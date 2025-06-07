import streamlit as st
from textblob import TextBlob

# Keywords/phrases often used in suspicious content
sensational_words = [
    'breaking', 'shocking', 'exclusive', 'miracle', 'you won’t believe', 'conspiracy',
    'secret', 'scandal', 'exposed', 'hidden truth'
]

fake_phrases = [
    'global conspiracy', 'they don’t want you to know', 'fake news', 'hoax',
    'manipulated media', 'deep state', 'hidden agenda', 'paid actors'
]

def analyze_article(text):
    text_lower = text.lower()
    word_count = len(text.split())
    blob = TextBlob(text)

    polarity = blob.sentiment.polarity  # Measures emotional tone

    # Count flagged words
    sensational_hits = sum(word in text_lower for word in sensational_words)
    fake_hits = sum(phrase in text_lower for phrase in fake_phrases)

    # Scoring logic
    score = 100
    score -= sensational_hits * 10
    score -= fake_hits * 20

    if polarity < -0.5 or polarity > 0.5:
        score -= 15
    if word_count < 30:
        score -= 10

    score = max(0, min(score, 100))  # Clamp between 0 and 100

    if score >= 75:
        credibility = ("🟢 Likely True", "#4CAF50")
    elif score >= 40:
        credibility = ("🟡 Needs Review", "#FFC107")
    else:
        credibility = ("🔴 Likely Fake", "#FF4B4B")

    reasons = []
    if sensational_hits:
        reasons.append(f"Detected {sensational_hits} sensational word(s).")
    if fake_hits:
        reasons.append(f"Found {fake_hits} fake news phrase(s).")
    if polarity < -0.5:
        reasons.append("Strongly negative emotional tone.")
    elif polarity > 0.5:
        reasons.append("Strongly positive (possibly exaggerated) tone.")
    if word_count < 30:
        reasons.append("Article is very short and may lack context.")
    if not reasons:
        reasons.append("No major red flags found.")

    sources = [
        {"title": "Vera Files", "url": "https://verafiles.org"},
        {"title": "Rappler Fact Check", "url": "https://www.rappler.com/newsbreak/fact-check/"},
        {"title": "Philippine Star News", "url": "https://www.philstar.com"}
    ]

    return credibility, reasons, score, sources

# --- Streamlit UI ---
st.set_page_config(page_title="FAKEtector", page_icon="🕵️", layout="centered")
st.title("🕵️ FAKEtector: News Credibility Checker")
st.write("Paste a news article or post and let FAKEtector analyze its credibility.")

text_input = st.text_area("📝 Paste the article text here", height=300)

if st.button("🔍 Analyze Now"):
    if not text_input.strip():
        st.warning("Please paste some news content first.")
    else:
        credibility, reasons, score, sources = analyze_article(text_input)

        st.markdown(f"<h2 style='color:{credibility[1]}'>{credibility[0]}</h2>", unsafe_allow_html=True)
        st.markdown(f"**Confidence Score**: {score}%")
        st.subheader("🧐 Why this result?")
        for reason in reasons:
            st.markdown(f"- {reason}")
        st.subheader("📚 Trusted Sources for Comparison")
        for s in sources:
            st.markdown(f"- [{s['title']}]({s['url']})")

st.markdown("---")
st.caption("FAKEtector © 2025 — Built with ❤️ using Streamlit + TextBlob")
