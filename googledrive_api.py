from __future__ import print_function
import pickle
import io
import os.path
import random
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


def delete_file(service, file_id):
    """Permanently delete a file, skipping the trash.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to delete.
  """
    try:
        service.files().delete(fileId=file_id).execute()
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


# If modifying these scopes, delete the file token.pickle.


SCOPES = ['https://www.googleapis.com/auth/drive']

if True:
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)

# Call the Drive v3 API
results = service.files().list(q="'1u8CwWx_kErN5aZ-S-5L1Q6fP92tJR7XI' in parents",
                               spaces='drive', pageToken=None, pageSize=1000,
                               fields="nextPageToken, files(id, name)"
                               ).execute()
items = results.get('files', [])
while True:
    pageToken = results.get('nextPageToken', None)
    print(pageToken)
    if not pageToken:
        break
    print(items.__len__())
    results = service.files().list(q="'1u8CwWx_kErN5aZ-S-5L1Q6fP92tJR7XI' in parents",
                                   spaces='drive', pageToken=pageToken, pageSize=1000,
                                   fields="nextPageToken, files(id, name)"
                                   ).execute()
    items += results.get('files', [])
    pageToken = results.get('nextPageToken', None)
print(items)

a = {}
ma = []

from os import walk
import os

'''
file_metadata = {
    'name': 'Spice',
    'mimeType': 'application/vnd.google-apps.folder'
}
file = service.files().create(body=file_metadata,
                              fields='id').execute()
fold_id = file.get('id')
print('Folder ID: %s' % file.get('id'))

for (dirpath, dirnames, filenames) in walk("/home/nick/File/photo/anime/hentai/Spice/"):
    for k in filenames:
        ex = k.split('.')[-1]
        file_metadata = {'name': k,
                         'parents': [fold_id]
                         }
        media = MediaFileUpload('/home/nick/File/photo/anime/hentai/Spice/' + k,

                                resumable=True)
        file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
        print('File ID: %s' % file.get('id'))


if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        a[item['id']] = item['name']
        if (item['name'].split('.')[-1] != 'jpg') & (item['name'].split('.')[-1] != 'png') & (
                item['name'].split('.')[-1] != 'gif') & (item['name'].split('.')[-1] != ''):
            print(item['name'])
            print(item['id'])

print(a)

file_id = '1K3T5Ct7VdwvauOwExd4-xhfnahVcI7t_'
request = service.files().get_media(fileId=file_id)
fh = io.fh = io.FileIO('x.txt', 'wb')
downloader = MediaIoBaseDownload(fh, request)
done = False

while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))
'''
