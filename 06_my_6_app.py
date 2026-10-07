import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore   # ← 修正

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate


QDRANT_PATH = "./local_qdrant"
COLLECTION_NAME = "my_collection"


def init_page():
    st.set_page_config(
        page_title="Ask My PDF(s)",
        page_icon="🤗"
    )
    st.sidebar.title("Nav")

    if "emb_model_name" not in st.session_state:
        st.session_state.emb_model_name = "text-embedding-3-large"
    if "costs" not in st.session_state:
        st.session_state.costs = []


def get_pdf_text():
    uploaded_file = st.file_uploader(
        label='Upload your PDF here😇',
        type='pdf'
    )
    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        text = '\n\n'.join([page.extract_text() for page in pdf_reader.pages])
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name=st.session_state.emb_model_name,
            chunk_size=250,
            chunk_overlap=0,
        )
        return text_splitter.split_text(text)
    else:
        return None


def load_qdrant():
    client = QdrantClient(path=QDRANT_PATH)

    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]

    if COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )
        print('collection created')

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=OpenAIEmbeddings()
    )


def build_vector_store(pdf_text):
    qdrant = load_qdrant()
    qdrant.add_texts(pdf_text)


def select_model():
    return ChatOpenAI(model="gpt-4o-mini")


def build_qa_model(llm):
    qdrant = load_qdrant()
    retriever = qdrant.as_retriever()

    # system プロンプト
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Use the given context to answer the question.\n"
         "If you don't know, say you don't know.\n\n{context}"
        ),
        ("human", "{question}")
    ])

    # LCEL チェーン構築（RetrievalQA の代替）
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    return chain


def ask(qa, query):
    answer = qa.invoke(query)
    return answer, 0.0   # コスト計測は後で追加可能


def page_pdf_upload_and_build_vector_db():
    st.title("PDF Upload")
    container = st.container()
    with container:
        pdf_text = get_pdf_text()
        if pdf_text:
            with st.spinner("Loading PDF ..."):
                build_vector_store(pdf_text)


def page_ask_my_pdf():
    st.title("Ask My PDF(s)")

    llm = select_model()
    container = st.container()
    response_container = st.container()

    with container:
        query = st.text_input("Query: ", key="input")
        if not query:
            answer = None
        else:
            qa = build_qa_model(llm)
            if qa:
                with st.spinner("ChatGPT is typing ..."):
                    answer, cost = ask(qa, query)
                st.session_state.costs.append(cost)
            else:
                answer = None

        if answer:
            with response_container:
                st.markdown("## Answer")
                st.write(answer)



def main():
    init_page()

    selection = st.sidebar.radio("Go to", ["PDF Upload", "Ask My PDF(s)"])
    if selection == "PDF Upload":
        page_pdf_upload_and_build_vector_db()
    elif selection == "Ask My PDF(s)":
        page_ask_my_pdf()

    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


if __name__ == '__main__':
    main()