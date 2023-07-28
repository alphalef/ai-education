import os
import gptauth
import llama_index as ll
from langchain import OpenAI
import openai


os.environ["OPENAI_API_KEY"] = gptauth.apikey
openai.api_key = os.environ["OPENAI_API_KEY"]


def loaddocs(dir):
    SimpleDirectoryReader = ll.download_loader("SimpleDirectoryReader")
    loader = SimpleDirectoryReader(dir, recursive=True, exclude_hidden=True)
    documents = loader.load_data()
    return documents

def indexdocs(docs):
    llm_predictor = ll.LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))

    max_input_size=3900
    num_output=256
    max_chunk_overlap=0.2
    prompt_helper=ll.PromptHelper(max_input_size, num_output, max_chunk_overlap)

    service_context = ll.ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index = ll.GPTVectorStoreIndex.from_documents(docs, service_context=service_context)

    index.storage_context.persist(persist_dir="./indexed") 

# docs = loaddocs('./data')
# indexdocs(docs)

storage_context = ll.StorageContext.from_defaults(persist_dir="./indexed")
index = ll.load_index_from_storage(storage_context)

query_engine = index.as_query_engine()
response = query_engine.query("성서를 읽어야 하는 이유는 무엇입니까?")

print(response.response)
