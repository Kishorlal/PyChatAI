'''
************************************************************************************************************************
Name: PyChatAI
Purpose: Creates an interactive chat session using model provided by openai.
         Provides capability to recollect data from its memory after sesion is closed based on user request.
         Provides capability to recall conversations that are specific to particular date time range as per the request from user
         Probvides capability to save conversation on user request thereby optimizing memory and not storing unwanted information
************************************************************************************************************************
'''
import os
from datetime import datetime
from utils import *


def main():
    try:
        OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        openai.api_key = OPENAI_API_KEY
        config = read_json(r"./config.json")
        memory_file = config["data_library"]
        date_time_format = config["date_time_format"]
        data_in_memory = {}
        if os.path.exists(memory_file):
            data_in_memory = read_json(memory_file)
            history_flg = True
        else:
            history_flg = False
        query = input('\nPlease let us know if you would like me to recall previous conversations : yes / no ')
        if query.lower() == "yes":
            if len(data_in_memory.keys()) == 0:
                print("History data is not available as this is our first interaction")
                messages = []
                memory_data =  gpt_responder(config, messages)
                data_in_memory[datetime.strptime(datetime.now().strftime(date_time_format), date_time_format).__str__()] = memory_data

            else:
                print("I have stored data between %s and %s"%(min(data_in_memory.keys()), max(data_in_memory.keys())))
                history_data = [item for data in data_in_memory.values() for item in data]
                query = input('\nPlease let us know if you want me to recall memory within any date range - yes/no ')
                query = input('\nPlease let us know if you want me to recall memory within any date range - yes/no ')
                if query.lower() == "yes":
                    start_date_time = input('\nPlease let us know start date time from when you  want me to recall memory ')
                    end_date_time = input('\nPlease let us know end date time till when you  want me to recall memory ')
                    print("Recalling data between given date time range")
                    messages = recall_memory(data_in_memory, start_date_time, end_date_time)
                    memory_data =  gpt_responder(config, messages,history_flg)
                    data_in_memory[datetime.strptime(datetime.now().strftime(date_time_format), date_time_format).__str__()] = memory_data

                else:
                    print("Recalling my memory from the start!")
                    messages = recall_memory(data_in_memory)
                    memory_data =  gpt_responder(config, messages,history_flg)
                    data_in_memory[datetime.strptime(datetime.now().strftime(date_time_format), date_time_format).__str__()] = memory_data

        else:
            messages = []
            memory_data =  gpt_responder(config, messages)
            data_in_memory[datetime.strptime(datetime.now().strftime(date_time_format), date_time_format).__str__()] = memory_data

        feedback = input('\nPlease let us know if you want us to store the conversation: yes / no ')
        if feedback.lower()=="yes":
            save_memory(memory_file, data_in_memory)
            print("Conversation saved successfully!!")
            print("Thanks!!!")
        else:
            print("Not storing current conversation!!")
            print("Thanks!!!")
    except Exception as error:
        print("Error in main function due to %s"%error)


main()
