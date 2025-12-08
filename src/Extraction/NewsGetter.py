import requests
import asyncio
import bs4
import asyncpg
import os
from dotenv import load_dotenv
from Extraction.XMLParser import XMLParser
from Extraction.utils import form_xml_file_name
from Constants import Constants

class NewsGetter:

    def __init__(self):
        load_dotenv()
        self.db_connection = None
    
    async def connect_db(self):
        self.db_connection = await asyncpg.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
    
    async def getRSS(self) -> str:
        r = requests.get(Constants.RSS_URL)
        return r.text

    async def write_xml_file(self, xml: str) -> str:
        current_record = form_xml_file_name()
        with open(current_record, "w") as f:
            f.write(xml)
        return current_record

    async def main(self):
        await self.connect_db()
        req: str = await self.getRSS()
        file_path: str = await self.write_xml_file(req)
        feed = XMLParser.parse(file_path)
        new_records = []
        
        for news in feed:
            exists = await self.db_connection.fetchval("SELECT COUNT(*) FROM Records WHERE link = $1 OR guid = $2", news.link, news.guid)
            if not exists:
                await self.db_connection.execute("INSERT INTO Records (title, description, link, pub_date, guid, categories) VALUES ($1, $2, $3, $4, $5, $6)", news.title, news.description, news.link, news.pubDate, news.guid, news.categories)
                new_records.append(news)
        
        await self.db_connection.close()
        return new_records
    
    async def get_new_records(self) -> list:
        req: str = await self.getRSS()
        file_path: str = await self.write_xml_file(req)
        feed = XMLParser.parse(file_path)
        new_records = []
        
        if not self.db_connection:
            await self.connect_db()
        
        for news in feed:
            exists = await self.db_connection.fetchval("SELECT COUNT(*) FROM Records WHERE link = $1 OR guid = $2", news.link, news.guid)
            if not exists:
                new_records.append(news)
        return new_records
    
    async def save_record(self, record):
        if not self.db_connection:
            await self.connect_db()
        
        try:
            await self.db_connection.execute(
                """
                INSERT INTO Records (title, description, link, pub_date, guid, categories)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (link) DO NOTHING
                """,
                record.title,
                record.description,
                record.link,
                record.pubDate,
                record.guid,
                record.categories
            )
            print(f"Saved to database: {record.title[:50]}...")
        except Exception as e:
            print(f"Error saving to database: {e}")
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                print(f"Record already exists: {record.title[:50]}...")
            else:
                raise
    
    async def close_connection(self):
        if self.db_connection:
            await self.db_connection.close()
            self.db_connection = None
            print("Connection closed.")

if __name__ == "__main__":
    getter = NewsGetter()
    asyncio.run(getter.main())



