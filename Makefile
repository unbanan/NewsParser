.PHONY: all clean-cache clean-xml clean-db reset-db run

all: run

clean-cache:
	rm -rf src/*/__pycache__

clean-xml:
	rm -rf XMLS/*

clean-db:
	psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS news_base;"
	psql -h localhost -U postgres -c "CREATE DATABASE news_base;"
	psql -h localhost -U postgres -c "DROP USER IF EXISTS news_parser;"
	psql -h localhost -U postgres -c "CREATE USER news_parser WITH PASSWORD 'news_parser123';"
	psql -h localhost -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE news_base TO news_parser;"
	psql -h localhost -U postgres -d news_base -c "CREATE TABLE IF NOT EXISTS Records (id SERIAL PRIMARY KEY, title VARCHAR(500) NOT NULL, description TEXT, link VARCHAR(1000) UNIQUE NOT NULL, pub_date VARCHAR(100), guid VARCHAR(500) UNIQUE, categories TEXT[], created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
	psql -h localhost -U postgres -d news_base -c "GRANT ALL PRIVILEGES ON TABLE Records TO news_parser;"
	psql -h localhost -U postgres -d news_base -c "GRANT USAGE, SELECT ON SEQUENCE records_id_seq TO news_parser;"

prepare: clean-cache clean-xml clean-db
	airflow db reset
	airflow db migrate
	
run: prepare
	airflow standalone