from dotenv import load_dotenv
import os
load_dotenv()

class Constants:
    XML_PREFIX: str = os.getenv("XML_PREFIX")
    XML_DIR: str = os.getenv("XML_DIR")
    RSS_URL: str = os.getenv("RSS_URL")
