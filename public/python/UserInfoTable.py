from ChatGPTPrompter import *
import asyncio
import json

user_data = {}


async def load_user_info():

    await upload_resume()

    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(get_response("phone number?"))
        task2 = tg.create_task(get_response("What's my first name?"))
        task3 = tg.create_task(get_response("What's my last name?"))
        task4 = tg.create_task(get_response("Address?"))
        task5 = tg.create_task(get_response("City?"))
        task6 = tg.create_task(get_response("Which state am I from?"))
        task7 = tg.create_task(get_response("zipcode?"))
        task8 = tg.create_task(get_response("phone_number"))
        task9 = tg.create_task(get_response("What is my college major?"))
        task10 = tg.create_task(get_response("Which school am I studying at?"))
        task11 = tg.create_task(get_response("school start year?(just year)"))
        task12 = tg.create_task(get_response("school start month?"))
        task13 = tg.create_task(get_response("school end month?"))
        task14 = tg.create_task(get_response("school end year?(just year)"))
        task15 = tg.create_task(get_response("List all of my skills separated by commas"))
        task16 = tg.create_task(get_response("What is my LinkedIn id (content after /in/ in href)"))


    user_data["phone_number"] = task1.result()
    user_data["first_name"] = task2.result()
    user_data["last_name"] = task3.result()
    user_data["address"] = task4.result()
    user_data["city"] = task5.result()
    user_data["state"] = task6.result()
    user_data["zipcode"] = task7.result()
    user_data["phone_number"] = task8.result()
    user_data["studying"] = task9.result()
    user_data["school"] = task10.result()
    user_data["school_start_year"] = task11.result()
    user_data["school_start_month"] = task12.result()
    user_data["school_end_month"] = task13.result()
    user_data["school_end_year"] = task14.result()
    user_data["skills"] = task15.result().split(",")
    user_data["linkedin"] = task16.result()



    job_data = {}
    numJobs = 0
    for i in range(3):
        try:
            numJobs = int( await get_response("how many jobs have I had? (Just number in numerical form)"))
            break
        except:
            pass

    for i in range(numJobs):
        single_job = {}

        async with asyncio.TaskGroup() as tg:
            job1 = tg.create_task(get_response("start month of job " + str(i) + "?"))
            job2 = tg.create_task(get_response("end month of job " + str(i) + "?"))
            job3 = tg.create_task(get_response("start year of job " + str(i) + "?(just year)"))
            job4 = tg.create_task(get_response("end year of job " + str(i) + "?(just year)"))
            job5 = tg.create_task(get_response("company of job" + str(i) + "?"))
            job6 = tg.create_task(get_response("position title of job" + str(i) + "?"))
            job7 = tg.create_task(get_response("What was the location of company" + str(i) + " that I worked at?"))
            job8 = tg.create_task(get_response("What is the description for my job" + str(i) + "?"))


        single_job["start_month"] = job1.result()
        single_job["end_month"] = job2.result()
        single_job["start_year"] = job3.result()
        single_job["end_year"] = job4.result()
        single_job["company"] = job5.result()
        single_job["position"] = job6.result()
        single_job["location"] = job7.result()
        single_job["description"] = job8.result()

        job_data[str(i)] = single_job
    
    user_data["job_data"] = job_data

    write_to_file()


def write_to_file():

    with open("user_info_table.json", "w") as outfile: 
        json.dump(user_data, outfile)



def get_user_data():
    global user_data
    return user_data
