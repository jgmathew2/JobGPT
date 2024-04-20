from openai import AsyncOpenAI
import pathlib
import base64

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key= str(base64.b64decode(b'c2stSlk4bTNzcFdqaFY2UFBNRHBEM0hUM0JsYmtGSmJVQ3JTTmhiWlo5MXdiTW1HbHQw'), "utf-8")
)

pre_prompts = ["If you don't have the information to answer a question, answer single word: NO"] 


# Figure out how to do pathname with python integration
async def upload_resume():

    pathname = str(pathlib.Path(__file__).parent.resolve())


    pathname = pathname + "/../uploads/resume.txt"

    with open(pathname, 'r') as file:
        data = file.read()

        f = open("current_gpt_convo.txt", "a")
        f.write((data + "\n\n"))

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
                "content": info + "\n\nDon't respond to this",
            }
        ],
        model="gpt-3.5-turbo",
    )

def clear_convo():
    f = open("current_gpt_convo.txt", "w")
    f.write("")

async def get_response(req):

    await do_preprompts()

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

async def do_preprompts():

    global pre_prompts

    pathname = "current_gpt_convo.txt"


    if(("pre-prompted" in open(pathname, "r").read()) == False): 

        f = open("current_gpt_convo.txt", "a")
        f.write(("pre-prompted" + "\n"))

        for prompt in pre_prompts:
            await post_custom_info("Don't respond to this command:\n" + prompt)
