# -*- coding: utf-8 -*-
"""chatgpt.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YpkbZc1CBI0QyCAMg71rFBaiItxTRqld
"""

#pip install openai

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

api_key_tele = config['DEFAULT']['api_key1']
api_key_openai = config['DEFAULT']['api_key2']


TELEGRAM_BOT_TOKEN = api_key_tele
TELEGRAM_BASE_URL = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN


def send_response(chat_id, text):
    url = TELEGRAM_BASE_URL + "/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

import os
import openai
import json

openai_api_key = api_key_openai

openai.api_key = openai_api_key

def get_openai_response(message):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=message,
      temperature=0,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.0)
    return response

import requests
import json
last_update_id = 0
while True:
    # Get updates from Telegram
    try:
      url = TELEGRAM_BASE_URL + "/getUpdates?offset={}".format(last_update_id + 1)
      resp = requests.get(url)
      updates = json.loads(resp.text)["result"]
    except requests.exceptions.RequestException as e:
      print("Error getting updates:", e)
      continue
    except json.JSONDecodeError as e:
      print("Error parsing response:", e)
      continue
    for update in updates:
        # Extract the update ID, message text, and chat ID
        update_id = update["update_id"]
        message = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]

          # Skip this update if it's already been processed
        if update_id > last_update_id:
          last_update_id = update_id

          try:
              # Get a response from OpenAI
              #print(message)
            response = get_openai_response(message)
          except Exception as e:
             print("Error getting response from OpenAI:", e)
             continue
          if response is not None:
            try:
              return_response = response["choices"][0]["text"]
            except KeyError as e:
              print("Error extracting response from OpenAI:", e)
              continue
            try:
              send_response(chat_id, return_response)
            except Exception as e:
              print("Error sending response:", e)
              continue