from openai import AsyncOpenAI
import asyncio
import sys

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key= "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"
)


# Figure out how to do pathname with python integration
async def upload_resume(pathname):


    with open(pathname, 'r') as file:
        data = file.read()

        f = open("current_gpt_convo.txt", "a")
        f.write((data + "\n"))

        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": data + "\n\nDon't respond to this",
                }
            ],
            model="gpt-3.5-turbo",
        )

async def post_custom_info(info):


    f = open("current_gpt_convo.txt", "a")
    f.write((info + "\n"))

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": info + "\nDon't respond to this",
            }
        ],
        model="gpt-3.5-turbo",
    )

def clear_convo():
    f = open("current_gpt_convo.txt", "w")
    f.write("")

async def get_response(req): 

    f = open("current_gpt_convo.txt", "r")

    previous_convo = f.read()

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": previous_convo + "\n" + req,
            }
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content



if(len(sys.argv) < 2):
    print("Command not found")
else:  

    if(sys.argv[1] == "upload_resume"):
        asyncio.run(upload_resume(sys.argv[2]))
    elif(sys.argv[1] == "get_response"):
        print(asyncio.run(get_response(sys.argv[2])))
    elif(sys.argv[1] == "post_custom_info"):
        asyncio.run(post_custom_info(sys.argv[2]))
    elif(sys.argv[1] == "clear_convo"):
        clear_convo()
    else:
        print("Command not found")

    
