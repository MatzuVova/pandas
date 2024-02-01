import pandas as pd
import os

full_with_odds = pd.DataFrame()

def update_xscore_files_with_odds(odds_file, base_folder):
    # Read the odds file
    odds_df = pd.read_csv(odds_file)
    # Standardize the date format in odds_df
    odds_df['date'] = pd.to_datetime(odds_df['date'], dayfirst=True)

    # Columns from odds_df to be included in the final merged dataframes
    odds_columns = ['open_1', 'closed_1', 'open_X', 'closed_X', 'open_2', 'closed_2', 
                    'open_over', 'closed_over', 'open_under', 'closed_under']

    # Traverse through the directories starting from the base_folder
    for folder, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith('_updated.csv') or file.endswith('_with_odds.csv'):
                continue
            if file.endswith('.csv'):
                # Assuming the league_id can be extracted from the filename
                league_id = int(file.split('.')[0])
                full_xscore_path = os.path.join(folder, file)
                # Read the xscore file
                xscore_df = pd.read_csv(full_xscore_path)
                # Standardize the date format in xscore_df
                xscore_df['date'] = pd.to_datetime(xscore_df['date'])

                # Filter odds_df for the specified league_id
                odds_df_filtered = odds_df[odds_df['league_id'] == league_id]

                # Merge the dataframes on date, home_team, and away_team
                merged_df = pd.merge(xscore_df, odds_df_filtered[odds_columns + ['date', 'home_team', 'away_team']],
                                        on=['date', 'home_team', 'away_team'], how='left')

                # Concatenate the merged_df with the full_with_odds dataframe
                global full_with_odds
                full_with_odds = pd.concat([full_with_odds, merged_df], ignore_index=True)

    # Write the full_with_odds dataframe to a csv file (moved outside the loop)
    full_with_odds.to_csv('full_df.csv', index=False)

# Example usage of the function
update_xscore_files_with_odds('odds.csv', 'xscore')
    
