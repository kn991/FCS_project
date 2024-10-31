@echo off

set PGPASSWORD=%POSTGRES_PASSWORD%

psql -U postgres -c "CREATE DATABASE ecommerce;"

psql -U postgres -d ecommerce -v ON_ERROR_STOP=1 --file create_tables.sql  