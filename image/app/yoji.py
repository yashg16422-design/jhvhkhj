
 
from langchain_community.embeddings import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  
)

import chromadb
import os
from openai import OpenAI
GITHUB_TOKEN = "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"
# token = os.environ["GITHUB_TOKEN"]
token = "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"
# token = st.secrets["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
    
)
from langchain_chroma import Chroma




def query_rag(query_text: str):
    vector_store = Chroma(
    collection_name="my_pdf_folder_collection",
    embedding_function=embeddings,
    chroma_cloud_api_key='ck-D62fQu4qShVTRt3PiDtKDSPoatSe1ZUbUeo8Xsipqsf9',
    tenant='69f6dd83-4a6c-41b4-b572-430aad7079be',
    database='sihshatapp',
    )
    results = vector_store.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": f"You are an expert assistant. Please answer the user's question based only on the following context:\n\n---\n{context_text}\n---"

        },
        {
            "role": "user",
            "content": query_text,


        }
    ],
    temperature=1,
    top_p=1,
    model=model
)

    response_text = response.choices[0].message.content
    sources = [doc.metadata.get("source", "unknown") for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}" 
    response = {"query_text":query_text,"answer":formatted_response}
    return response
text = "what is rainwater harvesting"
final_model = query_rag(text)
print(final_model)

# from langchain_openai.chat_models import ChatOpenAI

# st.title("🦜🔗 Quickstart App")

# # openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


# def generate_response(input_text):
#     # model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
#     st.info(query_rag(input_text))


# with st.form("my_form"):
#     text = st.text_area(
#         "Enter text:",
#         "What are the three key pieces of advice for learning how to code?",
#     )
#     submitted = st.form_submit_button("Submit")
#     if submitted :
#         generate_response(text)
# !pip install --upgrade --force-reinstall chromadb opentelemetry-api opentelemetry-sdk

# !zip -r vector_db.zip /content/sample_data/chroma/
