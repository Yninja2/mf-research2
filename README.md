# LlamaIndexを使用したRAG検索
　厚生労働省・PMDAの公式文書をもとにしたQ&Aシステム。
　　マスターファイルに関係するWEB文、PDFをインデックスした。
# 目的
 　公式文書をもとに簡潔な答えを得て、その根拠文書を確認する
# 特徴
 　質問のレスポンスから参考にした文章とそのPDFを表示
  インデックスは71個の文書から作成、容量は200MBを超える
  インデックスの保存にLarge file strageを使用
   質問には日本語で回答するようにプロンプトを変更
   WEBの表示にはstreamlitを使用
   LLMはOpenai　3.5を使用
# 使用方法　
　　質問欄に入力し、回答ボタンを押す
# WebCrawler.ipynb
　Openaiのチュートリアルを参考にPDFの自動ダウンロードを実行する
# RAG_eval.ipynb
  https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/
  を参考にQ＆Aの精度を評価
# インストールと実行方法
`conda create --name llama_index python=3.11

pip install -r requirements.txt

streamlit run test2.py`
