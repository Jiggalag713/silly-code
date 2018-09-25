import argparse
from target_parser import TargetParser
from table_cloner import TableCloner
from delta import Delta
from py_scripts.helpers.dbHelper import DbConnector
from py_scripts.helpers.logging_helper import Logger
from sqlalchemy import create_engine

parser = argparse.ArgumentParser(description='Make forecast great again')
parser.add_argument('liquibase_password', type=str,
                    help='cli location (default: "cli")')

args = parser.parse_args()

server = 'samaradb03.maxifier.com'
user = 'liquibase'
password = args.liquibase_password
source_db = 'rick'
target_db = 'rick_quality'
logger = Logger('DEBUG')
engine = create_engine('mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4'.format(user, password, server, source_db))

connection_params = {
    'host': server,
    'user': user,
    'password': password,
    'db': None
}

tables = [
    'rickcampaign',
    'rickcreative',
    # 'rickcreativesiteplacereport',
    'rickformat',
    # 'rickformat_rickplace',
    'rickformattype',
    'rickgender',
    'rickgeo',
    # 'rickgeo_rickgeo',
    'rickincome',
    'rickinsertionorder',
    'rickinterest',
    'rickplace',
    'rickplacereport',
    'rickposition',
    'ricksection',
    'ricktarget'
]

connection = DbConnector(connection_params, logger).get_connection()
parser = TargetParser(connection, source_db, logger)
targeting = parser.get_targeting()
cloner = TableCloner(connection, source_db, target_db, tables, logger)
check_deltas = cloner.create_tables()
delta = Delta(tables, connection, source_db, target_db, logger)
# delta.calculate_deltas()
# TODO: remove after debugging
check_deltas = True
if check_deltas:
    result = delta.calculate_deltas()
    delta.write_deltas(engine, result)
cloner.drop_tables()
print('debug...')
