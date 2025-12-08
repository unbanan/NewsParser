import asyncio
import os
from Extraction.NewsGetter import NewsGetter
from Notification.TelegramBot import TelegramNotifier

async def parse_and_notify():
    news_getter = NewsGetter()
    telegram_notifier = TelegramNotifier()
    
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not chat_id:
        print("TELEGRAM_CHAT_ID не найден в .env файле")
        return
    
    await telegram_notifier.set_chat_id(chat_id)
    
    try:
        print("Получение новых новостей...")
        new_records = await news_getter.get_new_records()
        
        if not new_records:
            print("No new news found")
            return
        
        print(f"Found {len(new_records)} new news items")
        
        print("Sending to Telegram...")
        success = await telegram_notifier.send_news(
            new_records,
            save_callback=news_getter.save_record
        )
        
        if success:
            print(f"Sent {len(new_records)} news items to Telegram")
        else:
            print("Error sending news items")
        
        await news_getter.close_connection()
            
    except Exception as e:
        print(f"Error in parse_and_notify: {e}")
        await news_getter.close_connection()

if __name__ == "__main__":
    asyncio.run(parse_and_notify())
