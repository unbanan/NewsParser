from datetime import datetime, timedelta
from airflow.sdk import dag
from airflow.sdk import task
from airflow.providers.standard.operators.bash import BashOperator
import sys
import os

sys.path.append('/home/unbanan/Documents/news_parser/src')

@dag(
    'news_parser_dag',
    default_args={
        'owner': 'news_parser',
        'depends_on_past': False,
        'start_date': datetime(2025, 12, 2),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Parse news from Habr and send to Telegram',
    schedule='*/10 * * * *',
    catchup=False,
    max_active_runs=1,
)
def news_parser_dag():
    
    @task
    def parse_and_notify():
        import asyncio
        import os
        from dotenv import load_dotenv
        
        load_dotenv('/home/unbanan/Documents/news_parser/src/.env')
        
        import sys
        sys.path.append('/home/unbanan/Documents/news_parser/src')
        
        from Extraction.NewsGetter import NewsGetter
        from Notification.TelegramBot import TelegramNotifier
        
        async def main():
            news_getter = NewsGetter()
            telegram_notifier = TelegramNotifier()
            
            chat_id = os.getenv('TELEGRAM_CHAT_ID')
            if not chat_id:
                print("TELEGRAM_CHAT_ID not found in .env file")
                return
            
            await telegram_notifier.set_chat_id(chat_id)
            
            try:
                print("Fetching new news...")
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
                
                await news_getter.close_connection()
                
                if success:
                    print(f"Successfully sent {len(new_records)} news items to Telegram")
                else:
                    print("Error sending news items to Telegram")
                    
            except Exception as e:
                print(f"Error in process: {e}")
                await news_getter.close_connection()
        
        asyncio.run(main())
    
    clean_task = BashOperator(
        task_id='clean_cache',
        bash_command='cd /home/unbanan/Documents/news_parser && make clean-cache && make clean-xml'
    )
    
    parse_task = parse_and_notify()
    
    clean_task >> parse_task

news_parser_dag()
