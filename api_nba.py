from nba_api.stats.endpoints import draftcombinestats

columns = ['PLAYER_NAME', 'POSITION', 'HEIGHT_WO_SHOES', 'WEIGHT', 'WINGSPAN']

def get_info_draft_api(player, year):
    """Get all draft infos of player from NBA API,
    using the method draftcombinestats"""
    season = str(year) + '-' + str(year+1)[2:]
    print(season)
    draft_combine_stats_2018 = draftcombinestats.DraftCombineStats(league_id='00', season_all_time=season)
    df_drafts_nba_2018 = draft_combine_stats_2018.get_data_frames()[0]

    # Choosing the columns of the table that we will keep
    red_df = df_drafts_nba_2018[columns]
    print(red_df[red_df['PLAYER_NAME'] == player])

get_info_draft_api('Rawle Alkins', 2018)
