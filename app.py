import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from chat_ui import css, bot_template, user_template
import boto3
import os


# Load embeddings using Google's Gemini model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def save_file_to_s3(file):
    s3 = boto3.client('s3', aws_access_key_id=os.getenv("aws_access_key"), aws_secret_access_key=os.getenv("aws_secret_access_key"))
    file.seek(0)
    s3.upload_fileobj(file, os.getenv("aws_bucket"), file.name)

def get_pdf_text(pdf_docs):
    text = ""
    pdf_reader = PdfReader(pdf_docs)
    for page in pdf_reader.pages:
        text += page.extract_text()

    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", convert_system_message_to_human=True)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')
    retriever = vector_store.as_retriever()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        return_source_documents=True,
        retriever=retriever,
        memory=memory
    )

    return conversation_chain

def handle_user_question(user_question):
    st.write("User Question: ", user_question)
    response = st.session_state.conversation({'question': user_question})
    print("Response: ", response)
    
    # Separate the 'answer' and 'source_documents'
    answer = response.get('answer', None)
    source_documents = response.get('source_documents', None)
    
    # Store them in Streamlit state
    st.session_state.answer = answer
    st.session_state.source_documents = source_documents
    st.session_state.chat_history = response['chat_history']

    # Log the response
    st.write("LLM Response: ", answer)
    # Display source documents inside a collapsible expander
    if source_documents:
        with st.expander("Source Documents (Click to expand)"):
            st.write(source_documents)
    # Display the chat history with alternating user and bot messages
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="PDF Data analyzer - using RAG.", page_icon=":books:")

    # Apply the custom CSS from chat_ui.py
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Header and input area for user question
    st.header("PDF Data analyzer - using RAG.")
    user_question = st.text_input("Ask a question about the inputted PDFs:")

    if user_question:
        handle_user_question(user_question)

    # Sidebar for PDF upload
    with st.sidebar:
        st.subheader("Your PDFs")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", type=["pdf"], accept_multiple_files=True)
        if st.button("Process"):
            if pdf_docs is not None:
                with st.spinner("Processing"):
                    raw_text = ""
                    for pdf in pdf_docs:
                        raw_text += get_pdf_text(pdf)

                    text_chunks = get_text_chunks(raw_text)
                    vector_store = get_vector_store(text_chunks)

                    st.session_state.conversation = get_conversation_chain(vector_store)
                    print("state: ", st.session_state.conversation)

if __name__ == '__main__':
    main()
