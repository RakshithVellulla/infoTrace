import os
import chromadb
from sentence_transformers import SentenceTransformer
from newsapi import NewsApiClient
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Initialize all models once
embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    return_all_scores=True
)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))

def run_infotrace_pipeline(topic, platform_posts):
    # Setup fresh ChromaDB
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(
        name="infotrace_live",
        metadata={"hnsw:space": "cosine"}
    )

    # Fetch and store verified facts
    verified_facts = fetch_verified_facts(topic)
    for i, article in enumerate(verified_facts):
        embedding = embedding_model.encode(article["content"]).tolist()
        collection.add(
            embeddings=[embedding],
            documents=[article["content"]],
            metadatas=[{"source": article["source"], "title": article["title"]}],
            ids=[f"verified_{i}"]
        )

    # Analyze each platform
    results = {}
    for platform, posts in platform_posts.items():
        if not posts:
            continue

        platform_scores = []
        sentiments = []
        
        for post in posts:
            # Similarity
            post_embedding = embedding_model.encode(post["content"]).tolist()
            query_results = collection.query(
                query_embeddings=[post_embedding],
                n_results=1
            )
            distance = query_results["distances"][0][0]
            similarity = round(1 - distance, 4)

            # Sentiment
            raw = sentiment_analyzer(post["content"][:512])
            scores = raw[0] if isinstance(raw[0], list) else raw
            sentiment_dict = {s["label"]: round(s["score"], 4) for s in scores}
            dominant = max(sentiment_dict, key=sentiment_dict.get)

            platform_scores.append({
                "post": post["content"][:100],
                "similarity": similarity,
                "sentiment": dominant,
                "likes": post.get("likes", 0),
                "shares": post.get("shares", 0)
            })
            sentiments.append(dominant)

        # Topic keywords
        docs = [p["content"] for p in posts]
        try:
            vectorizer = CountVectorizer(
                ngram_range=(1, 2),
                stop_words="english",
                max_features=5
            )
            vectorizer.fit_transform(docs)
            keywords = list(vectorizer.get_feature_names_out())
        except:
            keywords = []

        avg_similarity = round(
            sum(p["similarity"] for p in platform_scores) / len(platform_scores), 4
        )
        dominant_sentiment = max(set(sentiments), key=sentiments.count)

        results[platform] = {
            "posts": platform_scores,
            "average_similarity": avg_similarity,
            "dominant_sentiment": dominant_sentiment,
            "keywords": keywords
        }

    # Generate report
    summary = ""
    for platform, data in results.items():
        summary += f"\n{platform.upper()}:\n"
        summary += f"  Average similarity: {data['average_similarity']}\n"
        summary += f"  Dominant sentiment: {data['dominant_sentiment']}\n"
        summary += f"  Top keywords: {', '.join(data['keywords'])}\n"

    prompt = f"""
You are InfoTrace, an intelligent information analysis system.
Topic: "{topic}"
{summary}
Provide a concise 3-4 sentence analysis comparing how each platform 
is discussing this topic, which is most aligned with facts, 
and what misinformation patterns exist.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "results": results,
        "report": response.content
    }

def fetch_verified_facts(topic):
    try:
        response = newsapi.get_everything(
            q=topic,
            language="en",
            sort_by="relevancy",
            page_size=5
        )
        articles = []
        for article in response["articles"]:
            if article["content"] and len(article["content"]) > 50:
                articles.append({
                    "source": article["source"]["name"],
                    "title": article["title"],
                    "content": article["content"],
                    "url": article["url"]
                })
        return articles
    except:
        return [{
            "source": "Default",
            "title": topic,
            "content": f"Verified information about {topic}",
            "url": ""
        }]