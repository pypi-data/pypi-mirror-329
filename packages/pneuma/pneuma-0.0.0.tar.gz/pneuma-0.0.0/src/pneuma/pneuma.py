import logging
import os
from typing import Any, Optional

import fire
from huggingface_hub import login
from index_generator.index_generator import IndexGenerator
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from summarizer.summarizer import Summarizer
from torch import bfloat16
from utils.pipeline_initializer import initialize_pipeline
from utils.storage_config import get_storage_path

from query_processor.query_processor import QueryProcessor
from registrar.registrar import Registrar
from utils.logging_config import configure_logging

configure_logging()
logger = logging.getLogger("Pneuma")


class Pneuma:
    def __init__(
        self,
        out_path: Optional[str] = None,
        hf_token: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        use_local_model: bool = True,
        llm_path: str = "Qwen/Qwen2.5-7B-Instruct",
        embed_path: str = "BAAI/bge-base-en-v1.5",
        max_llm_batch_size: int = 50,
    ):
        if out_path is None:
            out_path = get_storage_path()
        os.makedirs(out_path, exist_ok=True)

        self.out_path = out_path
        self.db_path = os.path.join(out_path, "storage.db")
        self.index_location = os.path.join(out_path, "indexes")

        self.hf_token = hf_token
        self.openai_api_key = openai_api_key
        self.use_local_model = use_local_model
        self.llm_path = llm_path
        self.embed_path = embed_path
        self.max_llm_batch_size = max_llm_batch_size

        self.__hf_login()

        self.registrar: Optional[Registrar] = None  # Handles dataset registration
        self.summarizer: Optional[Summarizer] = None  # Summarizes table contents
        self.index_generator: Optional[IndexGenerator] = None  # Generates document indexes
        self.query_processor: Optional[QueryProcessor] = None  # Handles user queries
        self.llm: Optional[Any] = None  # Placeholder for LLM
        self.embed_model: Optional[Any] = None  # Placeholder for embedding model

    def __hf_login(self):
        """Logs into Hugging Face if a token is provided."""
        if self.hf_token:
            try:
                login(self.hf_token)
            except ValueError as e:
                logger.warning(f"HF login failed: {e}")

    def __init_registrar(self):
        """Initializes the Registrar module."""
        self.registrar = Registrar(db_path=self.db_path)

    def __init_summarizer(self):
        """Initializes the Summarizer module."""
        self.__init_llm()
        self.__init_embed_model()
        self.summarizer = Summarizer(
            llm=self.llm,
            embed_model=self.embed_model,
            db_path=self.db_path,
            max_llm_batch_size=self.max_llm_batch_size,
        )

    def __init_index_generator(self):
        """Initializes the IndexGenerator module."""
        self.__init_embed_model()
        self.index_generator = IndexGenerator(
            embed_model=self.embed_model,
            db_path=self.db_path,
            index_path=self.index_location,
        )

    def __init_query_processor(self):
        self.__init_llm()
        self.__init_embed_model()
        self.query_processor = QueryProcessor(
            llm=self.llm,
            embed_model=self.embed_model,
            db_path=self.db_path,
            index_path=self.index_location,
        )

    def __init_llm(self):
        if self.llm is None:
            if self.use_local_model:
                self.llm = initialize_pipeline(
                    self.llm_path, bfloat16, context_length=32768,
                )
                # Specific setting for batching
                self.llm.tokenizer.pad_token_id = self.llm.model.config.eos_token_id
                self.llm.tokenizer.padding_side = "left"
            else:
                self.llm = OpenAI(api_key=self.openai_api_key)


    def __init_embed_model(self):
        if self.embed_model is None:
            if self.use_local_model:
                self.embed_model = SentenceTransformer(self.embed_path)
            else:
                self.embed_model = OpenAI(api_key=self.openai_api_key)

    def setup(self) -> str:
        if self.registrar is None:
            self.__init_registrar()
        return self.registrar.setup()

    def add_tables(
        self,
        path: str,
        creator: str,
        source: str = "file",
        s3_region: str = None,
        s3_access_key: str = None,
        s3_secret_access_key: str = None,
        accept_duplicates: bool = False,
    ) -> str:
        if self.registrar is None:
            self.__init_registrar()
        return self.registrar.add_tables(
            path,
            creator,
            source,
            s3_region,
            s3_access_key,
            s3_secret_access_key,
            accept_duplicates,
        )

    def add_metadata(
        self,
        metadata_path: str,
        metadata_type: str = "",
        table_id: str = "",
    ) -> str:
        if self.registrar is None:
            self.__init_registrar()
        return self.registrar.add_metadata(metadata_path, metadata_type, table_id)

    def summarize(self, table_id: str = "") -> str:
        if self.summarizer is None:
            self.__init_summarizer()
        return self.summarizer.summarize(table_id)

    def purge_tables(self) -> str:
        if self.summarizer is None:
            self.__init_summarizer()
        return self.summarizer.purge_tables()

    def generate_index(self, index_name: str, table_ids: list | tuple = None) -> str:
        if self.index_generator is None:
            self.__init_index_generator()
        return self.index_generator.generate_index(index_name, table_ids)

    def query_index(
        self,
        index_name: str,
        query: str,
        k: int = 1,
        n: int = 5,
        alpha: int = 0.5,
    ) -> str:
        if self.query_processor is None:
            self.__init_query_processor()
        return self.query_processor.query(index_name, query, k, n, alpha)


def main():
    print("Hello from Pneuma's main method!")
    fire.Fire(Pneuma)


if __name__ == "__main__":
    main()
