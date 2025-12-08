all: clean-cache run

clean-cache:
	rm -rf src/*/__pycache__

clean-xml:
	rm -rf XMLS/*

clean-db:
	sudo -u postgres psql -c "DROP DATABASE IF EXISTS news_base;"
	sudo -u postgres psql -c "CREATE DATABASE news_base;"
	sudo -u postgres psql -c "DROP USER IF EXISTS news_parser;"
	sudo -u postgres psql -c "CREATE USER news_parser WITH PASSWORD 'news_parser123';"
	sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE news_base TO news_parser;"
	sudo -u postgres psql -d news_base -c "CREATE TABLE IF NOT EXISTS Records (id SERIAL PRIMARY KEY, title VARCHAR(500) NOT NULL, description TEXT, link VARCHAR(1000) UNIQUE NOT NULL, pub_date VARCHAR(100), guid VARCHAR(500) UNIQUE, categories TEXT[], created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
	sudo -u postgres psql -d news_base -c "GRANT ALL PRIVILEGES ON TABLE Records TO news_parser;"
	sudo -u postgres psql -d news_base -c "GRANT USAGE, SELECT ON SEQUENCE records_id_seq TO news_parser;"

reset-db: clean-db

run:
	./.venv/bin/python src/main.py