import os
from dotenv import load_dotenv

load_dotenv()

word = os.environ["GREETING_WORD"]
print(word)