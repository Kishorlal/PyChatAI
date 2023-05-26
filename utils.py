'''
************************************************************************************************************************
Name: Utility file
Purpose: Provides utility function for PyChatbotAI
************************************************************************************************************************
'''

import os
import json
import openai


def read_json(path):
    '''
    Purpose: Read config file and memory data
    '''
    try:
        with open(path, "r") as fhandler:
            json_data = json.load(fhandler)
        return json_data
    except Exception as error:
        print("Error due to %s" % error)

def save_memory(path, data):
    '''
    Purpose: Save conversation of each session upon user request
    '''
    try:
        if os.path.exists(path) and len(data.values()) == 0:
            os.remove(path)
        with open(path, "w") as fhandler:
            json.dump(data, fhandler)
    except Exception as error:
        print("Error due to %s" % error)

def recall_memory(history, start_date_time=None, end_date_time=None):
    '''
    Purpose: load history data upon user request
    '''
    try:
        recall_data = []
        if start_date_time != None or end_date_time != None:
            for date in history.keys():
                if date >= start_date_time and date <= end_date_time:
                    recall_data.extend(history[date])
        else:
            recall_data = [item for data in history.values() for item in data]
        return recall_data
    except Exception as error:
        print("Error due to %s" % error)

def gpt_responder(config, messages, history_flg=False):
    '''
    Purpose: open ai instance to start chat
    '''
    try:
        query = ""
        latest_data = []

        while query.lower() != "exit":
            query = input('\nAsk me a question: ')
            if history_flg:
                latest_data.append(
                    {
                        'role': 'user',
                        'content': query
                    })

            messages.append(
                {
                    'role': 'user',
                    'content': query
                })
            openai_instance = openai.ChatCompletion.create(
                model=config["model"],
                messages=messages)

            response = openai_instance.choices[0].message.content
            print(response)
            messages.append(
                {
                    'role': 'assistant',
                    'content': response
                })

            if history_flg:
                latest_data.append(
                    {
                        'role': 'assistant',
                        'content': response
                    })

        if history_flg:
            return latest_data[:-2]
        else:
            return messages[:-2]
    except Exception as error:
        print("Error due to %s" % error)