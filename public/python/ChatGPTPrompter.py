from openai import AsyncOpenAI
import pathlib

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key= "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"
)

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

    print(info)

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
