import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse


def init_page():
    st.set_page_config(
        page_title="Youtube Summarizer",
        page_icon="🤗"
    )
    st.header("Youtube Summarizer 🤗")
    st.sidebar.title("Options")
    st.session_state.costs = []


def select_model():
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo"
        price_per_1k = 0.0015
    else:
        model_name = "gpt-4o-mini"
        price_per_1k = 0.003

    return ChatOpenAI(temperature=0, model=model_name), price_per_1k


def get_url_input():
    url = st.text_input("Youtube URL: ", key="input")
    return url


def get_document(url):
    with st.spinner("Fetching Content ..."):
        video_id = extract_video_id(url)

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            raise ValueError("この動画には字幕がありません（自動生成字幕も含む）。") from e

        full_text = "\n".join([t["text"] for t in transcript])
        return full_text





def summarize(llm, docs, price_per_1k):
    prompt_template = """Write a concise Japanese summary of the following transcript of Youtube Video.

============
    
{text}

============

ここから日本語で書いてね
必ず3段落以内の200文字以内で簡潔にまとめること:
"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

    chain = PROMPT | llm

    response = chain.invoke({"text": docs})

    tokens = llm.get_num_tokens(docs)
    cost = (tokens / 1000) * price_per_1k

    return response, cost


def main():
    init_page()
    llm, price_per_1k = select_model()

    container = st.container()
    response_container = st.container()

    with container:
        url = get_url_input()
        if url:
            document = get_document(url)
            with st.spinner("ChatGPT is typing ..."):
                output_text, cost = summarize(llm, document, price_per_1k)
            st.session_state.costs.append(cost)
        else:
            output_text = None

    if output_text:
        with response_container:
            st.markdown("## Summary")
            st.write(output_text)
            st.markdown("---")
            st.markdown("## Original Text")
            st.write(document)

    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")

def extract_video_id(url):
    parsed = urlparse.urlparse(url)

    # 1. watch?v=xxxx
    if parsed.query:
        qs = urlparse.parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]

    # 2. youtu.be/xxxx
    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")

    # 3. /embed/xxxx
    if "/embed/" in parsed.path:
        return parsed.path.split("/embed/")[1]

    # 4. /shorts/xxxx
    if "/shorts/" in parsed.path:
        return parsed.path.split("/shorts/")[1]

    raise ValueError("動画IDを抽出できませんでした")



if __name__ == '__main__':
    main()
