
import os
from llama_index.llms.openai import OpenAI
#from llama_index.core.schema import MetadataMode
from llama_index.core import (
    GPTVectorStoreIndex,
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
    Settings,
#    ChatPromptTemplate,
    PromptTemplate,
)
from llama_index.core.callbacks import(
    CallbackManager, LlamaDebugHandler, CBEventType,
)
# from llama_index.core.extractors import (
#     SummaryExtractor,
#     QuestionsAnsweredExtractor,
#     TitleExtractor,
#     KeywordExtractor,
#     BaseExtractor,
# )
#from llama_index.extractors.entity import EntityExtractor
from llama_index.core.node_parser import TokenTextSplitter
from tenacity import ( retry, stop_after_attempt,  wait_random_exponential,)  # for exponential backoff
import streamlit as st

class Index_function:

    # try:
    #     value = os.environ["OPENAI_API_KEY"]
    #     #print(f"キー の値: {value}")
    # except KeyError:
    #     print(f"キー は環境変数に存在しません。")
    #     os.environ["OPENAI_API_KEY"] = st.secrets["api_key"]

    llama_debug_handler = LlamaDebugHandler()
    llama_debug_handler.get_event_pairs()
    #callback_manager = CallbackManager([llama_debug_handler])
    #service_context = ServiceContext.from_defaults(callback_manager=callback_manager)
    Settings.callback_manager = CallbackManager([llama_debug_handler])
    
    ##Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2)

    input_dir = "./documents/MF"
    index_name = "./saved_index"

    qa_prompt_tmpl_str = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query in Japanese always.\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

    text_splitter = TokenTextSplitter(
        separator="。 ", chunk_size=512, chunk_overlap=128)

    extractors = [
        #TitleExtractor(nodes=1, llm=llm), #5
        #QuestionsAnsweredExtractor(questions=1, llm=llm), #3
        # EntityExtractor(prediction_threshold=0.5),
        # SummaryExtractor(summaries=["prev", "self"], llm=llm),
        # KeywordExtractor(keywords=10, llm=llm),
        # CustomExtractor()
    ]

    transformations = extractors + [text_splitter]

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def make_index(self, documents):
        index = GPTVectorStoreIndex.from_documents(documents, transformations=self.transformations)
        return index 

    def make_query_engine(self):
        if os.path.exists(self.index_name):
            print('loding index .....')
            index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=self.index_name),
                #service_context=service_context,
            )
            print('reload index')
        else:
            print('making index .....')
            documents = []
            print(self.input_dir)
            documents = SimpleDirectoryReader(input_dir=self.input_dir).load_data()
            #index = GPTVectorStoreIndex.from_documents(documents, transformations=self.transformations)
            index = self.make_index(documents)
            index.storage_context.persist(persist_dir=self.index_name)
            print("made index")

        query_engine = index.as_query_engine(
            response_mode = 'compact',
            similarity_top_k = 2,
            text_qa_template = self.qa_prompt_tmpl,
            verbose = True,)
            #service_context = service_context)
        
        return query_engine
