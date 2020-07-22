import pymysql.cursors
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='pwdmysql',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cur:
    # Create database
    print("\nCreating database basketball if it does not already exists\n")
    cur.execute('CREATE DATABASE IF NOT EXISTS basketball')

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='pwdmysql',
                                 db='basketball',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cur.execute('use basketball')

    # cur.execute("DROP TABLE IF EXISTS teams")
    # cur.execute("DROP TABLE IF EXISTS players")
    # cur.execute("DROP TABLE IF EXISTS drafts")
    # cur.execute("DROP TABLE IF EXISTS teams_to_players")

    # Create table players
    print("\nCreating table players if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS players ("
                "id_player INT NOT NULL AUTO_INCREMENT,"
                "name_player VARCHAR(30),"
                "number_of_games_career INT,"
                "total_points_career INT,"
                "total_rebounds_career VARCHAR(5),"
                "total_assists_career INT,"
                "PRIMARY KEY (id_player)"
                ")")

    # Create table teams
    print("\nCreating table teams if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS teams ("
                "id_team INT NOT NULL AUTO_INCREMENT,"
                "team_name VARCHAR(30),"
                "PRIMARY KEY (id_team)"
                ")")

    # Create table teams_to_players
    print("\nCreating table teams_to_players if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS teams_to_players ("
                "id_teamp INT NOT NULL,"
                "id_playert INT NOT NULL,"
                "year INT,"
                "FOREIGN KEY(id_teamp) REFERENCES teams(id_team),"
                "FOREIGN KEY(id_playert) REFERENCES players(id_player)"
                ")")

    # Create table drafts
    print("\nCreating table drafts if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS drafts ("
                "id INT NOT NULL AUTO_INCREMENT,"
                "year INT,"
                "number_draft INT,"
                "name VARCHAR(30),"
                "number_of_games INT,"
                "total_minutes_played INT,"
                "total_points INT,"
                "total_rebounds INT,"
                "total_assists INT,"
                "minutes_per_game INT,"
                "points_per_game INT,"
                "rebounds_per_game INT,"
                "assists_per_game INT,"
                "PRIMARY KEY (id)"
                ")")