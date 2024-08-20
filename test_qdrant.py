from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import fitz #pyMuPDF
import os
import webbrowser

try:
    qdrant_key = os.environ["qdrant_key"]
except KeyError:
    print(f"キー は環境変数に存在しません。")

qdrant_client = QdrantClient(
    url="https://c5c4eea7-3717-4878-a79e-25946e0c048d.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key= qdrant_key)

print(qdrant_client.get_collections())

vector_store = QdrantVectorStore(client=qdrant_client, collection_name="MFdatabase")
#storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store,)
query_engine = index.as_query_engine()

response = query_engine.query("残留溶媒について教えてください。日本語で回答してください")

def highlight_text_in_pdf(pdf_path, output_path, search_text):    # PDFを開く
    doc = fitz.open(pdf_path)
    highlighted_pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text_instances = page.search_for(search_text)
        
        if text_instances:
            highlighted_pages.append(page_num)
            for inst in text_instances:
                # テキストの位置をハイライト
                highlight = page.add_highlight_annot(inst)
                highlight.update()

    # ハイライトされたPDFを保存
    doc.save(output_path)
    print(highlighted_pages)
    return highlighted_pages

def open_pdf_at_page(pdf_path, page_num): # PDFを開く
    edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"
    browse = webbrowser.get(edge_path)
    browse.open(f"file://{os.path.abspath(pdf_path)}#page={page_num + 1}")

for item in response.source_nodes:
    print(item)
    file_name = item.node.metadata['file_name']
    print('f, name', file_name)
    url = 'https://' + file_name.replace('_', '/')
    print('url', url)
    #url = 'https://www.pmda.go.jp/files/' + name + '.pdf'
    text = item.node.text[0:10] # extract source text
    point_id = item.node.id_
    print('id, text,', point_id, text )

    highlighted_pages = highlight_text_in_pdf(file_name, point_id + '.pdf', text)
    pdf_path = os.path.join(os.getcwd(), point_id + '.pdf')

    if highlighted_pages:
        # 最初にハイライトされたページを開く
        open_pdf_at_page(pdf_path, highlighted_pages[0])
        print(f"ハイライトと表示が完了しました。最初のハイライトされたページは {highlighted_pages[0] + 1} ページ目です。")
    else:
        print("指定した文字列はPDF内に見つかりませんでした。")

    print('###########################')

print(response)