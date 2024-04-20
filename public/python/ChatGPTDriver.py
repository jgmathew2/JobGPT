import sys
import asyncio

from ChatGPTPrompter import *
from UserInfoTable import *

if(len(sys.argv) < 2):
    print("Command not found")
else:  
    if(sys.argv[1] == "upload_resume"):
        asyncio.run(load_user_info())
    elif(sys.argv[1] == "get_response"):
        print(asyncio.run(get_response(sys.argv[2])))
    elif(sys.argv[1] == "post_custom_info"):
        asyncio.run(post_custom_info(sys.argv[2]))

    elif(sys.argv[1] == "clear_convo"):
        clear_convo()
    else:
        print("Command not found")

    