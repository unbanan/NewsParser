import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv
from Extraction.Record import Record

class TelegramNotifier:
    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.bot = Bot(token=self.bot_token)
        self.chat_id = None
    
    async def set_chat_id(self, chat_id: str):
        self.chat_id = chat_id
    
    def format_news_message(self, record: Record) -> str:
        message = f"*{record.title}*\n\n"
        
        if record.description:
            import re
            clean_desc = re.sub(r'<[^>]+>', '', record.description)
            if len(clean_desc) > 500:
                clean_desc = clean_desc[:500] + "..."
            message += f"{clean_desc}\n\n"
        
        message += f"[Читать статью]({record.link})\n\n"
        
        if record.categories and len(record.categories) > 0:
            hashtags = " ".join([f"#{cat.replace('-', '').replace(' ', '')}" for cat in record.categories[:5]])
            message += hashtags
        
        return message
    
    async def send_news(self, records: list[Record], save_callback=None) -> bool:
        if not self.chat_id:
            print("Chat ID not set. Please use set_chat_id()")
            return False
        
        success_count = 0
        for record in reversed(records):
            try:
                message = self.format_news_message(record)
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
                success_count += 1
                print(f"Sent news: {record.title[:50]}...")
                
                if save_callback:
                    await save_callback(record)
                
                await asyncio.sleep(5)
            except TelegramError as e:
                print(f"Error sending message: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error: {e}")
                continue
        
        print(f"Sent {success_count} out of {len(records)} news items")
        return success_count > 0
    
    async def get_updates(self):
        try:
            updates = await self.bot.get_updates()
            if updates:
                last_update = updates[-1]
                if last_update.message:
                    return last_update.message.chat.id
        except Exception as e:
            print(f"Error getting updates: {e}")
        return None

if __name__ == "__main__":
    async def test_bot():
        notifier = TelegramNotifier()
        
        chat_id = await notifier.get_updates()
        if chat_id:
            await notifier.set_chat_id(chat_id)
            print(f"Chat ID set: {chat_id}")
            
            from src.Extraction.Record import Record
            test_record = Record(
                title="Test news",
                link="https://example.com",
                description="This is a test news description for testing the Telegram bot functionality.",
                pubDate="Tue, 02 Dec 2025 15:00:00 GMT",
                guid="test-guid",
                categories=["test", "news", "automation"]
            )
            
            await notifier.send_news([test_record])
        else:
            print("Failed to get chat_id. Send any message to the bot to set it up.")
    
    asyncio.run(test_bot())
