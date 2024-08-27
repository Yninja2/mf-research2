import webbrowser
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import io
import os

SCOPES = ['https://www.googleapis.com/auth/drive']#['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = r'gdrive.json'
#credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

if os.path.exists('./gdrive.json'):
  SERVICE_ACCOUNT_FILE = r'./gdrive.json'
  credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

else:
  print(f" json file is not exit")
  SERVICE_ACCOUNT_INFO = {
    "type": st.secrets["google"]["type"],
    "project_id": st.secrets["google"]["project_id"],
    "private_key_id": st.secrets["google"]["private_key_id"],
    "private_key": st.secrets["google"]["private_key"].replace('\\n', '\n'),
    "client_email": st.secrets["google"]["client_email"],
    "client_id": st.secrets["google"]["client_id"],
    "auth_uri": st.secrets["google"]["auth_uri"],
    "token_uri": st.secrets["google"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["google"]["client_x509_cert_url"]
  }
  print("SERVICE INFO",SERVICE_ACCOUNT_INFO)
  credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO)
    
# Google Drive APIサービスの構築
service = build('drive', 'v3', credentials=credentials)

def download_file(file_id, output_filename):
  request = service.files().get_media(fileId=file_id)
  fh = io.BytesIO()
  downloader = MediaIoBaseDownload(fh, request)
  done = False
  while done is False:
      status, done = downloader.next_chunk()
      print("Download %d%%." % int(status.progress() * 100))
  output_filename = './download_file/' + output_filename
  with open(output_filename, "wb") as f:
    f.write(fh.getbuffer())
  print(f"File downloaded as '{output_filename}'")

def search_file_by_name_download(name):
  try:
    # create drive api client
    service = build("drive", "v3", credentials=credentials)
    files = []
    page_token = None
    q = f"name = '{name}'"
    while True:
      # pylint: disable=maybe-no-member
      response = (
          service.files()
          .list(
              q= q, 
              spaces="drive",
              fields="nextPageToken, files(id, name)",
              pageToken=page_token,
          )
          .execute()
      )
      for file in response.get("files", []):
        # Process change
        print(f'Found file file_name and id on Gdrive: {file.get("name")}, {file.get("id")}')
      files.extend(response.get("files", []))
      page_token = response.get("nextPageToken", None)
      if page_token is None:
        break

  except HttpError as error:
    print(f"An error occurred: {error}")
    files = None

  download_file(files[0]['id'], files[0]['name'])
  return files

def open_pdf_at_page(pdf_path, page_num): # PDFを開く
    edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"
    browse = webbrowser.get(edge_path)
    browse.open(f"file://{os.path.abspath(pdf_path)}#page={page_num + 1}")


# file = search_file_by_name_download('www.pmda.go.jp_review-services_f2f-pre_0001.html000219237.pdf')
# print(file[0]['name'])