import streamlit as st
import sys
import json
sys.path.append("..")

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ai_engine.pipeline import run_infotrace_pipeline

# Page config
st.set_page_config(
    page_title="InfoTrace",
    page_icon="🔍",
    layout="wide"
)

# Header
st.title("🔍 InfoTrace")
st.subheader("Cross-Platform Information Analysis System")
st.markdown("---")

# Search bar
topic = st.text_input(
    "🔎 Enter a topic to trace:",
    placeholder="e.g. flood in Assam, election results, covid vaccine..."
)

# Platform selector
st.markdown("### Select Platforms to Analyze")
col1, col2 = st.columns(2)
with col1:
    facebook = st.checkbox("📘 Facebook", value=True)
with col2:
    instagram = st.checkbox("📸 Instagram", value=True)

# File uploaders
st.markdown("### Upload Platform Data")
fb_file = None
ig_file = None

if facebook:
    fb_file = st.file_uploader("Upload Facebook JSON (from Apify)", type="json")
if instagram:
    ig_file = st.file_uploader("Upload Instagram JSON (from Apify)", type="json")

# Analyze button
analyze = st.button("🚀 Trace Information", type="primary")

if analyze and topic:
    # Load platform posts
    platform_posts = {}

    if fb_file:
        fb_data = json.load(fb_file)
        platform_posts["facebook"] = [
            {
                "content": p.get("text", ""),
                "likes": p.get("likes", 0),
                "shares": p.get("shares", 0)
            }
            for p in fb_data if p.get("text") and len(p.get("text", "")) > 10
        ]

    if ig_file:
        ig_data = json.load(ig_file)
        platform_posts["instagram"] = [
            {
                "content": p.get("caption", ""),
                "likes": p.get("likesCount", 0),
                "shares": p.get("commentsCount", 0)
            }
            for p in ig_data if p.get("caption") and len(p.get("caption", "")) > 10
        ]

    if not platform_posts:
        st.warning("⚠️ Please upload at least one platform data file!")
    else:
        st.markdown("---")
        st.markdown(f"### 📊 Analysis Results for: *{topic}*")

        with st.spinner("🔍 Analyzing information across platforms..."):
            output = run_infotrace_pipeline(topic, platform_posts)
            results = output["results"]
            report = output["report"]

        # Display results per platform
        cols = st.columns(len(results))
        for i, (platform, data) in enumerate(results.items()):
            with cols[i]:
                icon = "📘" if platform == "facebook" else "📸"
                st.markdown(f"#### {icon} {platform.capitalize()}")
                st.metric("Similarity to Facts", data["average_similarity"])
                st.metric("Dominant Sentiment", data["dominant_sentiment"])
                st.metric("Top Keywords", ", ".join(data["keywords"][:3]))

                # Show posts
                with st.expander("View Posts"):
                    for j, post in enumerate(data["posts"]):
                        st.markdown(f"**Post {j+1}**")
                        st.write(post["post"])
                        st.caption(f"Similarity: {post['similarity']} | Likes: {post['likes']}")
                        st.markdown("---")

        # Report
        st.markdown("---")
        st.markdown("### 📄 InfoTrace Report")
        st.info(report)

elif analyze and not topic:
    st.warning("⚠️ Please enter a topic to analyze!")