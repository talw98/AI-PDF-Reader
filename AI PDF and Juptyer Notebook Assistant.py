import PyPDF2
import nbformat
import numpy as np
import faiss
import requests
from mistralai.client import MistralClient, ChatMessage
import gradio as gr

api_key="iDPfYbSUtOv1D3czJkN3QhiU4dRXlCdE"
client = MistralClient(api_key=api_key)

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        return text

def extract_text_from_ipynb(file_path):
    with open(file_path, 'r') as file:
        notebook = nbformat.read(file, as_version=4)
        text = ''
        for cell in notebook.cells:
            if cell.cell_type == 'markdown':
                text += ' '.join(cell.source.split('\n'))
            elif cell.cell_type == 'code':
                text += ' '.join(cell.source.split('\n'))
        return text

def get_text_embedding(input):
    embeddings_batch_response = client.embeddings( model="mistral-embed", input=input )
    return embeddings_batch_response.data[0].embedding

def get_file_type(file_path):
    if file_path.endswith('.pdf'):
        return 'pdf'
    elif file_path.endswith('.ipynb'):
        return 'ipynb'
    else:
        raise ValueError('Unsupported file type')

def get_chunks(text, chunk_size=2000):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def create_index(text_embeddings):
    d = text_embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(text_embeddings)
    return index

def retrieve_similar_chunks(index, question_embeddings, chunks):
    D, I = index.search(question_embeddings, k=2)
    retrieved_chunk = [chunks[i] for i in I.tolist()[0]]
    return retrieved_chunk

def run_mistral(user_message, model="mistral-large-2402", temperature=0.7):
    messages = [ ChatMessage(role="user", content=user_message) ]
    chat_response = client.chat( model=model, messages=messages, temperature=temperature )
    return chat_response.choices[0].message.content

def chatbot(file, question):
    file_type = get_file_type(file.name)
    if file_type == 'pdf':
        text = extract_text_from_pdf(file.name)
    elif file_type == 'ipynb':
        text = extract_text_from_ipynb(file.name)
    chunks = get_chunks(text)
    text_embeddings = np.array([get_text_embedding(chunk) for chunk in chunks])
    index = create_index(text_embeddings)
    question_embeddings = np.array([get_text_embedding(question)])
    retrieved_chunk = retrieve_similar_chunks(index, question_embeddings, chunks)
    prompt = f""" Context information is below. {' '.join(retrieved_chunk)} Given the context information and not prior knowledge, answer the query. Query: {question} Answer: """
    return run_mistral(prompt)

def chatbot(file, question):
    file_type = get_file_type(file.name)
    if file_type == 'pdf':
        text = extract_text_from_pdf(file.name)
    elif file_type == 'ipynb':
        text = extract_text_from_ipynb(file.name)
    chunks = get_chunks(text)
    text_embeddings = np.array([get_text_embedding(chunk) for chunk in chunks])
    index = create_index(text_embeddings)
    question_embeddings = np.array([get_text_embedding(question)])
    retrieved_chunk = retrieve_similar_chunks(index, question_embeddings, chunks)
    prompt = f""" Context information is below. {' '.join(retrieved_chunk)} Given the context information and not prior knowledge, answer the query. Query: {question} Answer: """
    return run_mistral(prompt)

gr.Interface(fn=chatbot, inputs=["file", "text"], outputs= "text", title="AI PDF & Jupyter Notebook Assistant").launch()
