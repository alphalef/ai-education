import os
import gptauth
import llama_index as ll
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
import openai
import logging
import sys
from PyKakao import Karlo

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

os.environ["OPENAI_API_KEY"] = gptauth.apikey
openai.api_key = os.environ["OPENAI_API_KEY"]

kakaoapi = Karlo(service_key = gptauth.kakaokey)

def loaddocs(dir):
    SimpleDirectoryReader = ll.download_loader("SimpleDirectoryReader")
    loader = SimpleDirectoryReader(dir, recursive=True, exclude_hidden=True)
    documents = loader.load_data()
    return documents

def indexdocs(docs):
    llm_predictor = ll.LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo"))

    max_input_size=4096
    num_output=512
    max_chunk_overlap=0.2
    prompt_helper=ll.PromptHelper(max_input_size, num_output, max_chunk_overlap)
    service_context = ll.ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = ll.GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
    index.storage_context.persist(persist_dir="./indexed") 

# docs = loaddocs('./data')
# indexdocs(docs)

def gptanswer(query):
    storage_context = ll.StorageContext.from_defaults(persist_dir="./indexed")
    index = ll.load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response.response
    
    # query_engine = index.as_query_engine(streaming=True, similarity_top_k=1)
    # response_stream = query_engine.query(query)
    # response_stream.print_response_stream()
    # print(response.response)

def gptgeneral(query):
    model = "gpt-3.5-turbo"

    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "너는 기독교교양학교수야. 질문에 대해 기독교적인 측면을 잘 고려해서 대답해줘."},
            {"role": "user", "content": query}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']

    print(answer)
    return answer

def createimg(query):
    # 이미지 생성하기 REST API 호출
    img_dict = kakaoapi.text_to_image(query, 1)

    # 생성된 이미지 정보
    img_str = img_dict.get("images")[0].get('image')

    # base64 string을 이미지로 변환
    # img = kakaoapi.string_to_image(base64_string = img_str, mode = 'RGBA')

    return img_str