import os
from dotenv import load_dotenv
from llama_index.llms.gradient import GradientBaseModelLLM
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.gradient import GradientEmbedding
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex

load_dotenv(dotenv_path="./../.env")


def get_evidence_from_object(query):

    llm = GradientBaseModelLLM(
        base_model_slug="llama2-7b-chat",
        max_tokens=400,
    )

    documents = SimpleDirectoryReader("PDF").load_data()
    print(f"Loaded {len(documents)} document(s).")

    embed_model = GradientEmbedding(
        gradient_access_token=os.getenv("GRADIENT_ACCESS_TOKEN"),
        gradient_workspace_id=os.getenv("GRADIENT_WORKSPACE_ID"),
        gradient_model_slug="bge-large",
    )

    Settings.embed_model = embed_model
    Settings.llm = llm
    Settings.chunk_size = 1024

    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    response = query_engine.query(query)
    print(response)


get_evidence_from_object("What would be the punishment for attempt to murder?")
