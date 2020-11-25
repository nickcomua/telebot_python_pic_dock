import time
import logging
import threading
import telebot
import pickle
import io
import os.path
import random
from telebot import types
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import yaml


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


SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
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
token = "768083727:AAGifgRsDxB1ZY-4jkHPXd89Ag5fe_Zl87w"
bot = telebot.TeleBot(token)
erex_data = {}
love_data = {}
cat_data = {}

# TODO

with open(r'cat_erek.yaml') as file:
    cat_data = yaml.load(file, Loader=yaml.FullLoader)

with open(r'data_erek.yaml') as file:
    erex_data = yaml.load(file, Loader=yaml.FullLoader)

with open(r'data_love.yaml') as file:
    love_data = yaml.load(file, Loader=yaml.FullLoader)
print(cat_data, erex_data, love_data)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    print(call.data)
    if call.data.split()[-1] == '0':
        print(call)
        if love_data.get(call.data.split()[0]):
            for i in love_data.get(call.data.split()[0]):
                if (i.data.split()[0] == call.data.split()[0]) & (i.from_user.id == call.from_user.id):
                    print('deb')
                    love_data[call.data.split()[0]].remove(i)
            if love_data.get(call.data.split()[0]):
                love_data[call.data.split()[0]] += [call]
            else:
                love_data[call.data.split()[0]] = [call]
        else:
            love_data[call.data.split()[0]] = [call]
        print(love_data)
        with open(r'data_love.yaml', 'w') as file:
            documents = yaml.dump(love_data, file)
        with open(r'data_love.yaml', 'r') as file:
            bot.send_document('-447680338', file)
        bot.answer_callback_query(call.id)
    elif call.data.split()[-1] == '1':
        print(call)
        if erex_data.get(call.data.split()[0]):
            for i in erex_data.get(call.data.split()[0]):
                if (i.data.split()[0] == call.data.split()[0]) & (i.from_user.id == call.from_user.id):
                    print('deb')
                    erex_data[call.data.split()[0]].remove(i)
            if erex_data.get(call.data.split()[0]):
                erex_data[call.data.split()[0]] += [call]
            else:
                erex_data[call.data.split()[0]] = [call]
        else:
            erex_data[call.data.split()[0]] = [call]
        print(erex_data)
        with open(r'data_erek.yaml', 'w') as file:
            documents = yaml.dump(erex_data, file)
        with open(r'data_erek.yaml', 'r') as file:
            bot.send_document('-447680338', file)
        bot.answer_callback_query(call.id)
    elif call.data.split()[-1] == '2':
        print(call)
        if cat_data.get(call.data.split()[0]):
            for i in cat_data.get(call.data.split()[0]):
                if (i.data.split()[0] == call.data.split()[0]) & (i.from_user.id == call.from_user.id):
                    print('deb')
                    cat_data[call.data.split()[0]].remove(i)
            if cat_data.get(call.data.split()[0]):
                cat_data[call.data.split()[0]] += [call]
            else:
                cat_data[call.data.split()[0]] = [call]
        else:
            cat_data[call.data.split()[0]] = [call]
        print(cat_data)
        with open(r'cat_erek.yaml', 'w') as file:
            documents = yaml.dump(cat_data, file)
        with open(r'cat_erek.yaml', 'r') as file:
            bot.send_document('-447680338', file)
        bot.answer_callback_query(call.id)


def fun1():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=0)
        except:
            time.sleep(10)


x = threading.Thread(target=fun1)
x.start()
while True:
    try:
        while True:
            for _ in range(10):
                print("sth")
                item = random.choice(items)
                request = service.files().get_media(fileId=item['id'])
                fh = io.FileIO('file.' + item['name'].split('.')[-1], 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))
                fh.close()
                fh = io.FileIO('file.' + item['name'].split('.')[-1], 'rb')
                # bot.send_message("-1001473134565", "123", disable_notification=True)
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton('❤️', callback_data=f"{item['id']} {item['name']} 1 0"),
                    types.InlineKeyboardButton('💔', callback_data=f"{item['id']} {item['name']} 0 0"),
                    types.InlineKeyboardButton('😄', callback_data=f"{item['id']} {item['name']} 1 1"),
                    types.InlineKeyboardButton('😳', callback_data=f"{item['id']} {item['name']} 0 1"),
                    types.InlineKeyboardButton('No 😸', callback_data=f"{item['id']} {item['name']} 0 2"),
                    types.InlineKeyboardButton('😸', callback_data=f"{item['id']} {item['name']} 1 2"),
                    row_width=2
                )
                bot.send_photo("-1001473134565", fh, reply_markup=markup)
                fh.close()
            time.sleep(60 * 60 * 2)
    except:
        time.sleep(60 * 60 * 2)
