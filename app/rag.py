import asyncio

from vector_db import add_document, query_documents, load_or_create_index
from langchain_ollama import OllamaLLM
from langchain.chains.retrieval_qa.prompt import PROMPT
from langchain.text_splitter import RecursiveCharacterTextSplitter

K = 5
MODEL_NAME = "llama3"
LLM = OllamaLLM(model=MODEL_NAME)
TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
    add_start_index=True,
)


async def add_user_document(user_id: int, text: str):
    await asyncio.to_thread(add_document, user_id, text)


async def process_query(user_id: int, query: str):
    user_index = await asyncio.to_thread(load_or_create_index, user_id)

    docs = query_documents(user_index, query, k=K)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = PROMPT.format(context=context, question=query)

    answer = await asyncio.to_thread(LLM.invoke, prompt)
    return answer, docs


def split_document(document):
    return TEXT_SPLITTER.create_documents([document])


if __name__ == "__main__":
    import lorem

    def test_splitting():
        text = lorem.paragraph() * 100
        docs = TEXT_SPLITTER.create_documents([text])
        return docs

    def test_f(user_id, query):
        user_index = load_or_create_index(user_id)

        docs = query_documents(user_index, query, k=K)
        context = "\n".join(docs)
        prompt = PROMPT.format(context=context, question=query)

        answer = LLM.invoke(prompt)
        return answer, docs

    print(test_splitting())
    answer, docs = test_f(0, "Cars?")
