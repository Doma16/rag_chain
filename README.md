# RAG Chain
Multi-user document retrieval system using **RAG** and **LangChain**.

---

FastAPI web app that handles multiple users.  
Each user can upload documents, which are fed into the RAG system. Later, queries can retrieve relevant documents and generate contextual responses.

---

## Dependencies

- **Ollama** – for easy model pulling  
- **LangChain** – building blocks for text and LLM manipulation  
- **FAISS** – vector database used in this project


### Installation

---

1. **Clone the repo**
``` bash
git clone git@github.com:Doma16/rag_chain.git
```

2. **Build docker images with docker compose**
```bash 
docker compose build
```

3. **Make sure you don't have local version of ollama (optional)**
```bash
systemctl stop ollama
```

4. **Start the app with**
```bash
docker compose up -d
```

5. **To read logs from docker compose do**
```bash
docker compose logs -f
```

Everything is almost ready!

> ⚠️ **Note:** Ollama needs to download the models used for RAG before full functionality is available.  
> Models included:  
> - `llama3.2` (2.0 GB)  
> - `bge-m3` (1.2 GB)  


App won't start **before the downloads are complete**. Once the models are fully downloaded, you can start using the app normally.

---

### Usage

---

- Access the web interface: [http://localhost:8000](http://localhost:8000)  
- API documentation and routes: [http://localhost:8000/docs](http://localhost:8000/docs)

1. **Register a user and login**  
   - This will generate a JWT token stored in cookies.

2. **Optionally upload sample documents**  
   - You can automatically populate documents for your user with (make sure you use registered user):

```bash
docker exec rag_chain-app-1 bash -c "export PYTHONPATH=. && python data/auto_populate.py --username <username> --password <password>"
```
This uploads 30 documents from 20newsgroup dataset where each document
is considered to be under a category of talk.politics.misc, rec.autos etc.

After you uploaded documents you may 
go to:
- App query path: [http://localhost:8000/query](http://localhost:8000/query)  
Response might be slow since ollama is running on cpu.

---

### Stopping
---

**Stop docker containers with**
```bash
docker compose down
```

---
