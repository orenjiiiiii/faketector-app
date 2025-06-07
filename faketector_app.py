import streamlit as st

emotional_words = [
    'breaking', 'shocking', 'secret', 'betrayal', 'outrage',
    'doomed', 'conspiracy', 'share before they delete', 'exposed', 'reveal'
]

fake_keywords = [
    'global conspiracy', 'secret meeting', 'hidden agenda',
    'they don’t want you to know', 'truth exposed', 'leaked documents'
]

def analyze_article(text):
    text_lower = text.lower()
    emotional_hits = sum(1 for word in emotional_words if word in text_lower)
    fake_hits = sum(1 for phrase in fake_keywords if phrase in text_lower)
    total_flags = emotional_hits + fake_hits

    if total_flags >= 4:
        credibility = ("Likely Fake", "🛑", "#FF4B4B")
    elif total_flags >= 2:
        credibility = ("Needs Review", "⚠️", "#FFC107")
    else:
        credibility = ("Likely True", "✅", "#4CAF50")

    explanation = []
    if emotional_hits:
        explanation.append(f"💬 Emotionally charged language detected ({emotional_hits} instance(s)).")
    if fake_hits:
        explanation.append(f"🔍 Suspicious conspiracy-like phrases found ({fake_hits} instance(s)).")
    if not explanation:
        explanation.append("👍 No major warning signs found.")

    credible_sources = [
        {"title": "Fact Check: School Closure Rumors", "source": "Vera Files", "url": "https://verafiles.org"},
        {"title": "DepEd Official Statement", "source": "Philippine Star", "url": "https://philstar.com"},
        {"title": "How Fake News Spreads", "source": "Rappler", "url": "https://rappler.com"}
    ]

    return credibility, explanation, credible_sources

st.set_page_config(page_title="🕵️‍♀️ FAKEtector", page_icon="🕵️‍♀️", layout="centered")

st.title("🕵️‍♀️ FAKEtector")
st.markdown("### Your AI-powered assistant to spot fake news and keep you informed")

article = st.text_area("Paste article or URL here...", height=220)

if st.button("🔍 Analyze"):
    if not article.strip():
        st.warning("⚠️ Please paste some text before analyzing.")
    else:
        (credibility_text, icon, color), explanation, sources = analyze_article(article)
        st.markdown(f"<h2 style='color:{color};'>{icon} {credibility_text}</h2>", unsafe_allow_html=True)
        explanation_md = "\n\n".join([f"> {line}" for line in explanation])
        st.markdown("### Why?")
        st.markdown(explanation_md)
        st.markdown("### Trusted Sources to Check:")
        for source in sources:
            st.markdown(f"- [{source['title']}]({source['url']}) — *{source['source']}*")

st.markdown("---")
st.markdown("<small>FAKEtector © 2025 — Empowering Truth, One Article at a Time</small>", unsafe_allow_html=True)
