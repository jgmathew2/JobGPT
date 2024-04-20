from ChatGPTPrompter import *
import asyncio
import json

user_data = {}


def load_user_info():



    asyncio.run(upload_resume())
    user_data["address"] = asyncio.run(get_response("Address?"))
    user_data["city"] = asyncio.run(get_response("City?"))
    user_data["state"] = asyncio.run(get_response("Which state am I from?"))
    user_data["zipcode"] = asyncio.run(get_response("zipcode?"))
    user_data["phone_number"] = asyncio.run(get_response("phone number?"))

    job_data = {}
    numJobs = int(asyncio.run(get_response("how many jobs have I had? (Just number in numerical form)")))

    for i in range(numJobs):
        single_job = {}

        single_job["start_month"] = asyncio.run(get_response("start month of job " + str(i) + "?"))
        single_job["end_month"] = asyncio.run(get_response("end month of job " + str(i) + "?"))

        single_job["start_year"] = asyncio.run(get_response("start year of job " + str(i) + "?(just year)"))
        single_job["end_year"] = asyncio.run(get_response("end year of job " + str(i) + "?(just year)"))

        job_data[str(i)] = single_job

    user_data["job_data"] = job_data
    user_data["school_start_year"] = asyncio.run(get_response("school start year?(just year)"))
    user_data["school_start_month"] = asyncio.run(get_response("school start month?"))
    user_data["school_end_month"] = asyncio.run(get_response("school end month?"))
    user_data["school_end_year"] = asyncio.run(get_response("school end year?(just year)"))

    user_data["skills"] = asyncio.run(get_response("List all of my skills separated by commas")).split(",")

    user_data["linkedin"] = asyncio.run(get_response("What is my LinkedIn id (content after /in/ in href)"))

    write_to_file()


def write_to_file():

    with open("user_info_table.json", "w") as outfile: 
        json.dump(user_data, outfile)



def get_user_data():
    global user_data
    return user_data
