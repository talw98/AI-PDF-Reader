# 📄 AI PDF & Jupyter Notebook Assistant

A file-aware chatbot interface built with Mistral AI, FAISS, and Gradio. It allows users to upload `.pdf` or `.ipynb` files and ask natural language questions about their contents. The assistant processes the file, embeds the text using `mistral-embed`, performs semantic search via FAISS, and generates contextual responses using Mistral's chat model.

---

## 🚀 Features

- ✅ Supports both **PDF** and **Jupyter Notebook** (`.ipynb`) files.
- ✅ Uses **Mistral AI embeddings** for semantic understanding.
- ✅ RAG-style architecture with **FAISS** for fast similarity search.
- ✅ Beautiful **Gradio web interface**.
- ✅ Designed for local or cloud deployment.

---

## 🔧 Installation

Run the following in a Jupyter/Colab cell **exactly as shown**:

```python
# Install dependencies
!pip install PyPDF2
!pip install "numpy<2.0"  # FAISS is not yet compatible with NumPy 2.x
!pip install faiss-cpu==1.7.4 mistralai==0.0.12 nbformat
!pip install gradio
````

> ⚠️ **Important:** `faiss-cpu` is not compatible with NumPy 2.x. Always install `numpy<2.0` before FAISS.

After installing, restart the runtime or kernel (if you are working in Colab or Jupyter Environment).

---

## 🧠 How It Works

1. The uploaded file is parsed to extract all text.
2. The text is split into chunks (default 2000 characters).
3. Each chunk is embedded via Mistral’s embedding model (`mistral-embed`).
4. All chunk embeddings are indexed using **FAISS**.
5. A user question is embedded and compared with the index.
6. The top 2 most relevant chunks are selected.
7. These are passed to Mistral’s chat model (`mistral-large-2402`) in a prompt.
8. The model responds using the file’s content only (RAG approach).

---

## 🖥️ Gradio Interface

After running the script, a simple UI will appear:

* 📂 **File Input**: Upload a `.pdf` or `.ipynb` file.
* 📝 **Text Input**: Ask a question about the file (e.g., *“What is the main objective of this paper?”*).
* 💬 **Response**: The assistant will provide a contextual answer based on file contents.

You can run the app locally or share it via Gradio's sharing option.

---

## 🗂️ Example Use Case

* Upload a research paper or notebook.
* Ask: *“What is the conclusion section about?”*
* The assistant will return an answer grounded in the content, not generic knowledge.

---

## 🔐 API Key

Make sure to set your Mistral API key:

```python
api_key = "YOUR_MISTRAL_API_KEY"
client = MistralClient(api_key=api_key)
```

Replace `"YOUR_MISTRAL_API_KEY"` with your actual key. You can get it from [Mistral AI](https://console.mistral.ai/).

---

## ✅ To-Do / Improvements

* [ ] Add support for `.txt` and `.docx` files
* [ ] Customize chunk size dynamically
* [ ] Add multi-turn memory to chatbot

---

## 📜 License

MIT License — use, modify, or build on top of this freely.

---

## 🤖 Built With

* [Mistral AI](https://mistral.ai/)
* [FAISS by Facebook](https://github.com/facebookresearch/faiss)
* [Gradio](https://gradio.app/)
* [PyPDF2](https://pypi.org/project/PyPDF2/)
* [nbformat](https://pypi.org/project/nbformat/)

---

## 🙋‍♂️ Questions?

Feel free to open an issue or contact the maintainer.


