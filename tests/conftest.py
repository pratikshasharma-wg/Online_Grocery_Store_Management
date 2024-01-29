from config.config import Config
from database.database_queries import db_query_config
from config.logs_stmts import Logs

Config.load()
db_query_config.Config.load()
Logs.load()