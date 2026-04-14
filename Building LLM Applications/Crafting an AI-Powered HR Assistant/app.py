import os
from pathlib import Path
from typing import List, Tuple

import gradio as gr
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "data" / "1728286846_the_nestle_hr_policy_pdf_2012.pdf"
CHROMA_DIR = BASE_DIR / "chroma_db"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini")
EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")

SYSTEM_PROMPT = """You are an HR policy assistant for Nestle.
Answer the user's question using only the retrieved policy context.
If the answer is not available in the context, say that the document does not provide enough information.
Keep the answer clear, concise, and professional.
Always mention the source page numbers when possible.
"""


def build_vectorstore() -> Chroma:
    if not AZURE_OPENAI_API_KEY:
        raise ValueError("Set AZURE_OPENAI_API_KEY in your environment before starting the app.")
    if not AZURE_OPENAI_ENDPOINT:
        raise ValueError("Set AZURE_OPENAI_ENDPOINT in your environment before starting the app.")

    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(documents)

    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=EMBEDDING_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION,
    )
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
    )


def format_context(documents) -> str:
    context_parts = []
    for index, document in enumerate(documents, start=1):
        page = document.metadata.get("page", "unknown")
        context_parts.append(f"Source {index} | page {page}\n{document.page_content}")
    return "\n\n".join(context_parts)


def answer_question(question: str, vectorstore: Chroma) -> str:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    documents = retriever.invoke(question)
    context = format_context(documents)

    llm = AzureChatOpenAI(
        azure_deployment=CHAT_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION,
        temperature=0,
    )
    prompt = f"""{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)
    return response.content


VECTORSTORE = build_vectorstore()


def chat(message: str, history: List[Tuple[str, str]]):
    if not message.strip():
        return "", history

    answer = answer_question(message, VECTORSTORE)
    history = history + [(message, answer)]
    return "", history


demo = gr.Blocks(title="Nestle HR Assistant")

with demo:
    gr.Markdown("# Nestle HR Policy Assistant")
    gr.Markdown(
        "Ask questions about the Nestle HR policy document. "
        "The assistant retrieves relevant sections from the PDF before answering."
    )

    chatbot = gr.Chatbot(label="Conversation", height=450)
    user_input = gr.Textbox(
        label="Your question",
        placeholder="Example: What does the policy say about employee conduct?",
    )
    clear_button = gr.Button("Clear Chat")

    user_input.submit(chat, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
    clear_button.click(lambda: ("", []), outputs=[user_input, chatbot])


if __name__ == "__main__":
    demo.launch()
