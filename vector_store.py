from config import client


def get_vector_store_id_by_name(name: str) -> str:
    print(f"[vector_store]  Searching for vector store: {name}")

    cursor = None
    page_num = 1

    while True:
        print(f"[vector_store]  Fetching page {page_num}")

        page = (
            client.vector_stores.list(limit=50, after=cursor)
            if cursor
            else client.vector_stores.list(limit=50)
        )

        for vs in page.data:
            print(f"[vector_store]   ↳ Found: {vs.name}")
            if vs.name == name:
                print(f"[vector_store]  Match found: {vs.id}")
                return vs.id
        if not page.has_more:
            break
        cursor = page.last_id
        page_num += 1

    raise RuntimeError(f"[vector_store]  Vector store '{name}' not found")
