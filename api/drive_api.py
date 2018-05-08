import io

from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from httplib2 import Http
from oauth2client import file
from apiclient.discovery import build

from DatShiroShop.models import Song
from api.auth import Auth

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
store = file.Storage('credentials.json')
auth = Auth(SCOPES, store)
creds = auth.getCredentials()
shiro_store_folder_id = '1E1_y5_-vW6Qwvh0aXkQ3DK5cYq2ZaVY2'
service = build('drive', 'v3', http=creds.authorize(Http()))


def list_files(size=10):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)", q="'{0}' in parents".format(shiro_store_folder_id)).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))


def get_file(fileID):
    results = service.files().get(fileId=fileID).execute()
    return results


def load_files_to_sqlite():
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)", q="'{0}' in parents".format(shiro_store_folder_id)).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
            name = item['name']
            id = item['id']
            author = name.rsplit(' - ')[1]
            name = name.rsplit(' - ')[0]
            song = Song(name=name, id=id, author=author)
            song.save()
            print('Saved to database')


def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


def downloadFile(file_id,filepath):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())


def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))


def searchFile(size,query):
    results = service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))
