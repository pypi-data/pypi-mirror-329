from simplex import Simplex
import os
from dotenv import load_dotenv
import time

load_dotenv()

def login():
    simplex = Simplex(api_key=os.getenv("SIMPLEX_API_KEY"))
    simplex.create_session(proxies=False)
    simplex.goto("https://dropbox.com")
    
    with open("dropbox_com_session_data.json", "r") as f:
        session_data = f.read()
    simplex.restore_login_session(session_data=session_data)

    simplex.wait(1000)
    print(simplex.extract_text("footer texts"))
    print(simplex.wait(5000))

if __name__ == "__main__":
    login()