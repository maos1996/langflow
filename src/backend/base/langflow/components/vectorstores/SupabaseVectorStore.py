from typing import List

from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.retrievers import BaseRetriever
from supabase.client import Client, create_client

from langflow.custom import Component
from langflow.helpers.data import docs_to_data
from langflow.io import HandleInput, IntInput, Output, StrInput
from langflow.schema import Data


class SupabaseVectorStoreComponent(Component):
    display_name = "Supabase"
    description = "Supabase Vector Store with search capabilities"
    documentation = "https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/supabase"
    icon = "Supabase"

    inputs = [
        StrInput(name="supabase_url", display_name="Supabase URL", required=True),
        StrInput(name="supabase_service_key", display_name="Supabase Service Key", required=True),
        StrInput(name="table_name", display_name="Table Name", advanced=True),
        StrInput(name="query_name", display_name="Query Name"),
        HandleInput(name="embedding", display_name="Embedding", input_types=["Embeddings"]),
        HandleInput(
            name="vector_store_inputs",
            display_name="Vector Store Inputs",
            input_types=["Document", "Data"],
            is_list=True,
        ),
        StrInput(name="search_input", display_name="Search Input"),
        IntInput(
            name="number_of_results",
            display_name="Number of Results",
            info="Number of results to return.",
            value=4,
            advanced=True,
        ),
    ]

    outputs = [
        Output(
            display_name="Vector Store",
            name="vector_store",
            method="build_vector_store",
            output_type=SupabaseVectorStore,
        ),
        Output(
            display_name="Base Retriever",
            name="base_retriever",
            method="build_base_retriever",
            output_type=BaseRetriever,
        ),
        Output(display_name="Search Results", name="search_results", method="search_documents"),
    ]

    def build_vector_store(self) -> SupabaseVectorStore:
        return self._build_supabase()

    def _build_supabase(self) -> SupabaseVectorStore:
        supabase: Client = create_client(self.supabase_url, supabase_key=self.supabase_service_key)

        documents = []
        for _input in self.vector_store_inputs or []:
            if isinstance(_input, Data):
                documents.append(_input.to_lc_document())
            else:
                documents.append(_input)

        if documents:
            supabase_vs = SupabaseVectorStore.from_documents(
                documents=documents,
                embedding=self.embedding,
                query_name=self.query_name,
                client=supabase,
                table_name=self.table_name,
            )
        else:
            supabase_vs = SupabaseVectorStore(
                client=supabase,
                embedding=self.embedding,
                table_name=self.table_name,
                query_name=self.query_name,
            )

        return supabase_vs

    def search_documents(self) -> List[Data]:
        vector_store = self._build_supabase()

        if self.search_input and isinstance(self.search_input, str) and self.search_input.strip():
            docs = vector_store.similarity_search(
                query=self.search_input,
                k=self.number_of_results,
            )

            data = docs_to_data(docs)
            self.status = data
            return data
        else:
            return []
