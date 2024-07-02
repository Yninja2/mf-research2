# LlamaIndexを使用したRAG検索
　厚生労働省・PMDAが管理するマスターファイル登録について申請方法、FAQ、通知を検索するために作成した。
　関係するWEB文、PDFをインデックスした。　今後GMP管理についても拡張していきたい。
# 目的
 　PMDAの公式文書を元にした簡潔なQ&A
# 特徴
 　引用した文書のPDF名と引用文章を表示
　　インデックスの容量は200MB

# Local Setup
`conda create --name llama_index python=3.11

pip install -r requirements.txt

streamlit test2.py`
