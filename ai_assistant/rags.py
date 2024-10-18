import os
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    SimpleDirectoryReader,
    PromptTemplate,
    Settings,
)
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from ai_assistant.config import get_agent_settings

SETTINGS = get_agent_settings()

llm = OpenAI(model="gpt-4o-mini", api_key=SETTINGS.OPENAI_API_KEY)
embed_model = HuggingFaceEmbedding(model_name=SETTINGS.hf_embeddings_model)
Settings.embed_model = embed_model
Settings.llm = llm


class TravelGuideRAG:
    def __init__(
        self,
        store_path: str,
        data_dir: str | None = None,
        qa_prompt_tpl: PromptTemplate | None = None,
    ):
        self.store_path = store_path

        if not os.path.exists(store_path) and data_dir is not None:
            self.index = self.ingest_data(store_path, data_dir)
        else:
            self.index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=store_path)
            )

        self.qa_prompt_tpl = qa_prompt_tpl

    def ingest_data(self, store_path: str, data_dir: str) -> VectorStoreIndex:
        documents = SimpleDirectoryReader(data_dir).load_data()
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        index.storage_context.persist(persist_dir=store_path)
        return index

    def get_query_engine(self) -> RetrieverQueryEngine:
        query_engine = self.index.as_query_engine()

        if self.qa_prompt_tpl is not None:
            query_engine.update_prompts(
                {"response_synthesizer:text_qa_template": self.qa_prompt_tpl}
            )

        return query_engine
