import webbrowser
import os
print(os.getcwd())
current_folder = os.getcwd()

# def open_pdf_at_page(pdf_path, page_num):
#     # PDFを開く
#     webbrowser.open_new(f"file://{pdf_path}#page={page_num + 1}")
# a = str('C:\Users\y_nak\mf-research2\7aa6561d-02c9-40b3-820d-09f631987b18.pdf')
# open_pdf_at_page(a, 15)

def open_pdfs_in_browser(folder_path, pdf_file):
    # # フォルダー内のすべてのファイルを取得
    # files = os.listdir(folder_path)
    
    # # PDFファイルをフィルタリング
    # pdf_files = [file for file in files if file.endswith('.pdf')]
    
    # 各PDFファイルをウェブブラウザで開く
    # for pdf in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)
    print(pdf_path)
        # webbrowser.open_new(f"file://{os.path.abspath(pdf_path)}")
    webbrowser.open(f"file://{os.path.abspath(pdf_path)}#page={'15'}")

pdf = '7aa6561d-02c9-40b3-820d-09f631987b18.pdf'
pdf_path = os.path.join(current_folder, pdf)
edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"
print(pdf_path)
#open_pdfs_in_browser(current_folder, '7aa6561d-02c9-40b3-820d-09f631987b18.pdf')

#webbrowser.open('https://www.youtube.com')
browse = webbrowser.get(edge_path)
#browse = webbrowser.get('windows-default')

browse.open(f"file://{os.path.abspath(pdf_path)}#page={15}")