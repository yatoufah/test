from extract import extract_data
import pandas as pd

def transform_data(data): 
    # Convert 'active_date' column to datetime
    data['active_date'] = pd.to_datetime(data['active_date'])
    # Calculate the longest streak for each user
    data['active_date_diff'] = data.groupby('user_id')['active_date'].diff().dt.days.fillna(0)
    data['streak_group'] = (data['active_date_diff'] != 1).cumsum()
    data['longest_streak'] = data.groupby(['user_id', 'streak_group'])['active_date_diff'].cumsum().max(level=0)
    # Find the top workspace for each user
    top_workspace_df = data.groupby('user_id')['total_activity'].idxmax()
    top_workspace_data = data.loc[top_workspace_df, ['user_id', 'workspace_id']].rename(columns={'workspace_id': 'top_workspace'})

    # Calculate the longest streak for each user
    longest_streak_data = data.groupby('user_id')['longest_streak'].max().reset_index()

    # Merge the top workspace and longest streak data
    user_activity_df = pd.merge(top_workspace_data, longest_streak_data, on='user_id', how='left')
    return user_activity_df


