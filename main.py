import os.path
import pickle
import threading
import time
from os import path
import random
import io
import telebot
from googleapiclient.http import MediaIoBaseDownload
import yaml
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from telebot import types


def set(mar, num, x, y):
    smile = smiles[x][y]
    if num:
        mar.keyboard[x][y].text = smile + " " + str(num)
    else:
        mar.keyboard[x][y].text = smile
    return mar


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
    if not pageToken:
        break
    results = service.files().list(q="'1u8CwWx_kErN5aZ-S-5L1Q6fP92tJR7XI' in parents",
                                   spaces='drive', pageToken=pageToken, pageSize=1000,
                                   fields="nextPageToken, files(id, name)"
                                   ).execute()
    items += results.get('files', [])
    pageToken = results.get('nextPageToken', None)
print('indexed')
a = {}
ma = []
token = "768083727:AAGifgRsDxB1ZY-4jkHPXd89Ag5fe_Zl87w"
bot = telebot.TeleBot(token, num_threads=10)
erex_data = {}
love_data = {}
cat_data = {}
smiles = [['❤', '💔'], ['😄', '😳'], ['No 😸', '😸']]

if path.exists(r'cat_erek.yaml'):
    with open(r'cat_erek.yaml') as file:
        cat_data = yaml.load(file, Loader=yaml.FullLoader)
    with open(r'data_erek.yaml') as file:
        erex_data = yaml.load(file, Loader=yaml.FullLoader)
    with open(r'data_love.yaml') as file:
        love_data = yaml.load(file, Loader=yaml.FullLoader)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    drive_id = call.data.split()[0]
    x = call.data.split()[-1]
    if x == '0':
        if love_data.get(drive_id):
            for i in love_data.get(drive_id):
                if (i.data.split()[0] == drive_id) & (i.from_user.id == call.from_user.id):
                    love_data[drive_id].remove(i)

            if love_data.get(drive_id):
                love_data[drive_id] += [call]
            else:
                love_data[drive_id] = [call]
        else:
            love_data[drive_id] = [call]
        bot.answer_callback_query(call.id)
    elif x == '1':
        if erex_data.get(drive_id):
            for i in erex_data.get(drive_id):
                if (i.data.split()[0] == drive_id) & (i.from_user.id == call.from_user.id):
                    erex_data[drive_id].remove(i)
            if erex_data.get(drive_id):
                erex_data[drive_id] += [call]
            else:
                erex_data[drive_id] = [call]
        else:
            erex_data[drive_id] = [call]

        bot.answer_callback_query(call.id)

    elif x == '2':
        if cat_data.get(drive_id):
            for i in cat_data.get(drive_id):
                if (i.data.split()[0] == drive_id) & (i.from_user.id == call.from_user.id):
                    cat_data[drive_id].remove(i)

            if cat_data.get(drive_id):
                cat_data[drive_id] += [call]
            else:
                cat_data[drive_id] = [call]
        else:
            cat_data[drive_id] = [call]

        bot.answer_callback_query(call.id)

    c = {'0': 0, '1': 0}
    for i in love_data.get(drive_id, []):
        c[i.data.split()[-2]] += 1
    mar = set(call.message.reply_markup, c['0'], 0, 0)
    mar = set(mar, c['1'], 0, 1)
    c = {'0': 0, '1': 0}
    for i in erex_data.get(drive_id, []):
        c[i.data.split()[-2]] += 1
    mar = set(mar, c['0'], 1, 0)
    mar = set(mar, c['1'], 1, 1)
    c = {'0': 0, '1': 0}
    for i in cat_data.get(drive_id, []):
        c[i.data.split()[-2]] += 1
    mar = set(mar, c['0'], 2, 0)
    mar = set(mar, c['1'], 2, 1)
    bot.edit_message_media(types.InputMediaPhoto(call.message.photo[0].file_id), chat_id=call.message.chat.id,
                           message_id=call.message.id, reply_markup=mar)


def fun1():
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)
        x.start()


print('0')
x = threading.Thread(target=fun1)
x.start()

print('1')
while True:
    try:
        with open(r'data_love.yaml', 'w') as file:
            documents = yaml.dump(love_data, file)
        with open(r'data_erek.yaml', 'w') as file:
            documents = yaml.dump(erex_data, file)
        with open(r'cat_erek.yaml', 'w') as file:
            documents = yaml.dump(cat_data, file)

        with open(r'data_love.yaml', 'r') as file:
            bot.send_document('-447680338', file)
        with open(r'data_erek.yaml', 'r') as file:
            bot.send_document('-447680338', file)
        with open(r'cat_erek.yaml', 'r') as file:
            bot.send_document('-447680338', file)
        time.sleep(60)
        for _ in range(10):
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
                types.InlineKeyboardButton('❤️', callback_data=f"{item['id']} {item['name']} 0 0"),
                types.InlineKeyboardButton('💔', callback_data=f"{item['id']} {item['name']} 1 0"),
                types.InlineKeyboardButton('😄', callback_data=f"{item['id']} {item['name']} 0 1"),
                types.InlineKeyboardButton('😳', callback_data=f"{item['id']} {item['name']} 1 1"),
                types.InlineKeyboardButton('No 😸', callback_data=f"{item['id']} {item['name']} 0 2"),
                types.InlineKeyboardButton('😸', callback_data=f"{item['id']} {item['name']} 1 2"),
                row_width=2
            )
            bot.send_photo("-1001473134565", fh, reply_markup=markup)
            fh.close()
        time.sleep(60 * 60 * 24)
    except:
        time.sleep(60 * 60 * 12)
