# rag_chain
Multi-user document retrival system that is using RAG and LangChain.

---

FastAPI web that can handle different users and with users it also
handles per-user document upload where each document is fed into 
RAG system and then is able to be contextually retrieved with a query
later on with relevant documents and generated response.

---

---

### Depends on

- Ollama: for easy model pulling.
- LangChain: building block for text and llm manipulation. 
- FAISS: vector database used in this project.

---

### Installation

---

... TODO ...

cloning, docker pulling, docker running, docker should automatically do stuff for us.

---

### To use somewhere:
```
curl -fsSL https://ollama.com/install.sh | sh

ollama pull llama3
ollama pull bge-m3

```
