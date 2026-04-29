import os

from agents import set_default_openai_key
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("Please set OPENAI_API_KEY.")

openai_client = OpenAI(api_key=api_key)
set_default_openai_key(api_key)

FILE_PATH = "./data_lines.txt"

#  transient vector store
vs = openai_client.vector_stores.create(name="Data Lines Vector Store")

# 1) Upload to Files API
uploaded = openai_client.files.create(
    file=open(FILE_PATH, "rb"),
    purpose="assistants",
)

# 2) Attach & poll on the vector store
vs_file = openai_client.vector_stores.files.create_and_poll(
    vector_store_id=vs.id,
    file_id=uploaded.id,
)
print("vs_file.status:", vs_file.status)
print("vs_file.last_error:", getattr(vs_file, "last_error", None))

# import os
# from pathlib import Path
#
# from agents import set_default_openai_key
# from openai import OpenAI
#
# api_key = os.environ.get("OPENAI_API_KEY")
# if not api_key:
#     raise RuntimeError("OPENAI_API_KEY is not set.")
#
# client = OpenAI(api_key=api_key)
# set_default_openai_key(api_key)
#
#
# corpus_path = Path("./data_lines.txt")
#
# if not corpus_path.is_file():
#     raise FileNotFoundError(f"Corpus file not found: {corpus_path}")
#
#
# # --- Create transient vector store ---
# vector_store = client.vector_stores.create(
#     name="Data Lines Vector Store",
#     expires_after={
#         "anchor": "last_active_at",
#         "days": 1,
#     },
# )
#
#
# with corpus_path.open("rb") as file_stream:
#     file_batch = client.vector_stores.file_batches.upload_and_poll(
#         vector_store_id=vector_store.id,
#         files=[file_stream],
#     )
#
#
# print("vector_store_id:", vector_store.id)
# print("file_batch.status:", file_batch.status)
# print("file_batch.file_counts:", file_batch.file_counts)
#
# if file_batch.status != "completed":
#     raise RuntimeError(
#         f"Vector store ingestion failed or incomplete: {file_batch.status}"
#     )
