from nba_api.stats.endpoints import draftcombinestats

columns = ['PLAYER_NAME', 'POSITION', 'HEIGHT_WO_SHOES', 'WEIGHT', 'WINGSPAN']

def get_info_draft_api(player, year):
    """Get all draft infos of player from NBA API,
    using the method draftcombinestats"""
    season = str(year) + '-' + str(year+1)[2:]
    draft_combine_stats = draftcombinestats.DraftCombineStats(league_id='00', season_all_time=season)
    df_drafts_nba = draft_combine_stats.get_data_frames()[0]

    # Choosing the columns of the table that we will keep
    red_df = df_drafts_nba[columns]
    draft_data = red_df[red_df['PLAYER_NAME'] == player]
    # print(draft_data)
    return draft_data.iloc[0, :]

print(get_info_draft_api('Cole Aldrich', 2010))
