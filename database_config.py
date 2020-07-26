from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
from functions import setup_logger
import pymysql.cursors
import logging


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='pwdmysql',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = setup_logger('first_logger', 'database_management.log', formatter)

with connection.cursor() as cur:
    # Create database
    logger.info("\nCreating database basketball_ref if it does not already exists\n")
    cur.execute('CREATE DATABASE IF NOT EXISTS basketball_ref_scrap4')
    cur.execute('use basketball_ref_scrap4')
    # cur.execute('\W')

    # cur.execute("DROP TABLE IF EXISTS teams")
    # cur.execute("DROP TABLE IF EXISTS players")
    # cur.execute("DROP TABLE IF EXISTS drafts")
    # cur.execute("DROP TABLE IF EXISTS teams_to_players")

    # cur.execute('DELETE FROM teams_to_players')
    # cur.execute('DELETE FROM teams')
    # cur.execute('DELETE FROM players')
    #
    # cur.execute('ALTER TABLE teams AUTO_INCREMENT = 1')
    # cur.execute('ALTER TABLE teams_to_players AUTO_INCREMENT = 1')
    # cur.execute('ALTER TABLE players AUTO_INCREMENT = 1')


    # Create table players
    logger.info("\nCreating table players if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS players ("
                "id_player INT NOT NULL AUTO_INCREMENT,"
                "name_player VARCHAR(30),"
                "year_draft INT,"
                "number_of_games_career FLOAT,"
                "total_points_career FLOAT,"
                "total_rebounds_career FLOAT,"
                "total_assists_career FLOAT,"
                "PRIMARY KEY (id_player)"
                ")")

    # Create table teams
    logger.info("\nCreating table teams if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS teams ("
                "id_team INT NOT NULL AUTO_INCREMENT,"
                "team_name VARCHAR(30),"
                "PRIMARY KEY (id_team)"
                ")")

    # Create table teams_to_players
    logger.info("\nCreating table teams_to_players if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS teams_to_players2 ("
                "id_table_inter INT NOT NULL AUTO_INCREMENT,"
                "id_team INT NOT NULL,"
                "id_player INT NOT NULL,"
                "year INT,"
                "PRIMARY KEY (id_table_inter),"
                "FOREIGN KEY(id_team) REFERENCES teams(id_team),"
                "FOREIGN KEY(id_player) REFERENCES players(id_player)"
                ")")

    # Create table drafts (FROM NBA API)
    logger.info("\nCreating table drafts from API if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS drafts_api ("
                "id INT NOT NULL AUTO_INCREMENT,"
                "id_player INT NOT NULL,"
                "PLAYER_NAME VARCHAR(30),"
                "POSITION VARCHAR(5),"
                "HEIGHT_WO_SHOES FLOAT,"
                "WEIGHT FLOAT,"
                "WINGSPAN FLOAT,"
                "PRIMARY KEY (id),"
                "FOREIGN KEY(id_player) REFERENCES players(id_player)"
                ")")

    # OLD DRAFT TABLE
    # logger.info("\nCreating table drafts if it does not already exists...\n")
    # cur.execute("CREATE TABLE IF NOT EXISTS drafts ("
    #             "id INT NOT NULL AUTO_INCREMENT,"
    #             "year INT,"
    #             "number_draft FLOAT,"
    #             "name VARCHAR(30),"
    #             "number_of_games FLOAT,"
    #             "total_minutes_played FLOAT,"
    #             "total_points FLOAT,"
    #             "total_rebounds FLOAT,"
    #             "total_assists FLOAT,"
    #             "minutes_per_game FLOAT,"
    #             "points_per_game FLOAT,"
    #             "rebounds_per_game FLOAT,"
    #             "assists_per_game FLOAT,"
    #             "PRIMARY KEY (id)"
    #             ")")
