from operator import truediv

import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import json
import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import os

class LeaderBoard:
    def __init__(self):
        load_dotenv()

        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        self.supabase: Client = create_client(url, key)

        #for deployment ####################################

        kaggle_username = os.getenv('KAGGLE_USERNAME')
        kaggle_key = os.getenv('KAGGLE_KEY')

        if not kaggle_username or not kaggle_key:
            raise EnvironmentError('KAGGLE_USERNAME and KAGGLE_KEY must be set in the environment variables.')

        kaggle_config = {
            'username': kaggle_username,
            'key': kaggle_key
        }

        with open('kaggle.json', 'w') as f:
            json.dump(kaggle_config, f)

        os.environ['KAGGLE_CONFIG_DIR'] = os.getcwd()

        ####################################################


        self.api = KaggleApi()
        self.api.authenticate()

    def get_kaggle_leaderboard(self, competition_name):
        leaderboard = kaggle.api.competition_leaderboard_view(competition_name)
        my_data = []
        members = self.get_competition_members()

        for row in leaderboard:
            my_row = vars(row)
            if my_row['teamName'] in members:
                extended_row = my_row.copy()

                if isinstance(extended_row['submissionDate'], datetime.datetime):
                    time_elapsed = datetime.datetime.now() - extended_row['submissionDate']
                    extended_row['submissionDate'] = extended_row['submissionDate'].strftime('%Y-%m-%d %H:%M:%S')

                extended_row['teamMembers'] = members[extended_row['teamName']]
                members.pop(my_row['teamName'])
                days = time_elapsed.days
                seconds = time_elapsed.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                if days != 0:
                    extended_row['last'] = f"{days}d {hours}h {minutes}m {seconds}s"
                elif hours != 0:
                    extended_row['last'] = f"{hours}h {minutes}m {seconds}s"
                else:
                    extended_row['last'] = f"{minutes}m {seconds}s"
                my_data.append(extended_row)

        if len(members) > 0:
            for team_name, members in members.items():
                row = {'teamNameNullable': team_name, 'scoreNullable': 0, 'teamId': -1, 'teamName': team_name,
                       'hasTeamName': True, 'submissionDate': -1, 'score': 0, 'hasScore': False, 'last': -1,
                       'teamMembers': members}
                my_data.append(row)
        return my_data

    def get_competition_members(self):
        
        response = self.supabase.table('users').select('*').execute()
        teams = {}
        if response.data:
            for user in response.data:
                team_name = user.get('team_name')  # Replace with the actual column name for team name
                if team_name not in teams:
                    teams[team_name] = []
                team_member = {
                    'first_name': user.get('first_name'),  # Replace with column name for first name
                    'last_name': user.get('last_name'),    # Replace with column name for last name
                    'email': user.get('email'),            # Replace with column name for email
                }
                teams[team_name].append(team_member)

        return teams
        
        # scopes = ['https://www.googleapis.com/auth/spreadsheets']
        # creds = Credentials.from_service_account_file("sheet.config.json", scopes=scopes)
        # client = gspread.authorize(creds)
        # 
        # sheet = client.open_by_key(self.sheet_id).sheet1
        # 
        # teams = {}
        # for fn, ln, email, tn in sheet.get_all_values()[1:]:
        #     if tn not in teams:
        #         teams[tn] = []
        #         team_member = {
        #             'first_name': fn,
        #             'last_name': ln,
        #             'email': email,
        #         }
        #         teams[tn].append(team_member)
        #     else:
        #         team_member = {
        #             'first_name': fn,
        #             'last_name': ln,
        #             'email': email,
        #         }
        #         teams[tn].append(team_member)
        # return teams



