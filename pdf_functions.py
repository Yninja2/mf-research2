import fitz #pyMuPDF
import os
import webbrowser
import test_gDrive

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
    print('highlighted pages', highlighted_pages)
    return highlighted_pages

def open_pdf_at_page(pdf_path, page_num): # PDFを開く
    edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"
    browse = webbrowser.get(edge_path)
    browse.open(f"file://{os.path.abspath(pdf_path)}#page={page_num + 1}")

#for item in response.source_nodes:
def file_search_highlight_open(item): # item in response.source_nodes
    #print(item)
    file_name = item.node.metadata['file_name']
    #print('file name', file_name)
    text = item.node.text[0:10] # extract source text
    point_id = item.node.id_
    print('point_id, text !!!!!!!!!!!!!!!!!', point_id, text )

    files = test_gDrive.search_file_by_name_download(file_name)
    if files == []:
        print('file is not found in gDrive.')
        return 'no file'

    file_path = os.path.join(os.getcwd(), files[0]['name'])
    highlighted_pages = highlight_text_in_pdf(file_path, point_id + '.pdf', text)
    pdf_path = os.path.join(os.getcwd(), point_id + '.pdf')

    if highlighted_pages:
        # 最初にハイライトされたページを開く
        open_pdf_at_page(pdf_path, highlighted_pages[0])
        print(f"ハイライトと表示が完了しました。最初のハイライトされたページは {highlighted_pages[0] + 1} ページ目です。")
    else:
        print("指定した文字列はPDF内に見つかりませんでした。")

    print('########################### ############################ ################################# #########################')


def file_search_highlight_open_forStreamlit(item): # item in response.source_nodes
    #print(item)
    file_name = item.node.metadata['file_name']
    #print('file name', file_name)
    text = item.node.text[0:10] # extract source text
    point_id = item.node.id_
    print('point_id, text !!!!!!!!!!!!!!!!!', point_id, text )

    files = test_gDrive.search_file_by_name_download(file_name)
    if files == []:
        print('file is not found in gDrive.')
        return 'no file'

    file_path = os.path.join(os.getcwd(), files[0]['name'])
    highlighted_pages = highlight_text_in_pdf(file_path, point_id + '.pdf', text)
    pdf_path = os.path.join(os.getcwd(), point_id + '.pdf')

    # if highlighted_pages:
    #     # 最初にハイライトされたページを開く
    #     open_pdf_at_page(pdf_path, highlighted_pages[0])
    #     print(f"ハイライトと表示が完了しました。最初のハイライトされたページは {highlighted_pages[0] + 1} ページ目です。")
    # else:
    #     print("指定した文字列はPDF内に見つかりませんでした。")
    print(pdf_path, highlighted_pages)
    print('########################### ############################ ################################# #########################')
    return pdf_path, highlighted_pages
