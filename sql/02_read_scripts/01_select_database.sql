-- Selects a database name
select 1 
from pg_database
where datname = %s;