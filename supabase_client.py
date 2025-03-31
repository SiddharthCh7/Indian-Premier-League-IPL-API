from supabase import Client, create_client
from dotenv import load_dotenv
from collections import defaultdict
import os

load_dotenv()

class Data:
    def __init__(self):
        #supabase setup
        self.url: str = os.getenv("PROJECT_URL")
        self.key: str = os.getenv("API_KEY")
        self.supabase: Client = create_client(self.url, self.key)
    
    def get_all_matches_data(self):
        try:
            data = self.supabase.table("IPL").select("*").execute()
            return data
        except Exception as e:
            print("Exception in 'get_all_matches_data': {}".format(str(e)))
            raise

    def get_teams(self):
        try:
            teams_data = self.supabase.table("IPL").select("Team1, Team2").execute()
            result = list(set([t['Team1'] for t in teams_data.data if t['Team1'] is not None]))
            return {"teams":result}
        except Exception as e:
            print("Exception in 'get_teams': {}".format(str(e)))
            raise
    
    def team_vs_team_info(self, team1, team2):
        try:
            data1 = self.supabase.table("IPL").select("*").eq("Team1", team1).eq("Team2", team2).execute()
            data2 = self.supabase.table("IPL").select("*").eq("Team1", team2).eq("Team2", team1).execute()
            result = data1.data + data2.data
            return {
                "teams": [team1, team2],
                "total_matches": len(result),
                "matches": result
            }

        except Exception as e:
            print("Exception in 'team_vs_team_info': {}".format(str(e)))
            raise

    def team_vs_team_stats(self, team1: str, team2: str):
        try:
            data1 = self.supabase.table("IPL").select("*").eq("Team1", team1).eq("Team2", team2).execute()
            data2 = self.supabase.table("IPL").select("*").eq("Team1", team2).eq("Team2", team1).execute()
            combined_data = data1.data + data2.data

            winning_count = defaultdict(int)
            for i in combined_data:
                winning_count[i["Match_Winner"]] += 1

            return {
                "teams": [team1, team2],
                "total_matches": len(combined_data),
                team1: {
                    "wins": winning_count[team1],
                    "win_percentage": round((winning_count[team1] / len(combined_data)) * 100, 2) if len(combined_data) else 0
                },
                team2: {
                    "wins": winning_count[team1],
                    "win_percentage": round((winning_count[team2] / len(combined_data)) * 100, 2) if len(combined_data) else 0
                }
            }
            
        except Exception as e:
            print("Exception in 'get_team_vs_team_stats': {}".format(str(e)))
            raise
    
    def team_vs_all(self, team):
        try:
            data = self.supabase.table("IPL").select("*").eq("Team1", team).execute()
            result = {
                "team" : team,
                "total_matches" : len(data.data),
                "matches" : data
            }
            return result
        except Exception as e:
            print("Exception in 'team_against_all': {}".format(str(e)))
            raise
    
    def batsman_record(self, batsman):
        try:
            data = self.supabase.table("IPL_stats").select("bowler, non-striker, total_run, BattingTeam").eq("batter", batsman).execute()
            res = {
                "batsman" : batsman,
                "total_runs" : 0,
                "total_balls_played" : len(data.data),
                "non_striker" : defaultdict(int),
                "bowler" : defaultdict(int),
                "batting_team" : defaultdict(int)
            }
            for i in data.data:
                res['total_runs'] += i['total_run']
                res["non_striker"][i["non-striker"]] += 1
                res["bowler"][i["bowler"]] += 1
                res["batting_team"][i["BattingTeam"]] += 1
    
            res['non_striker'] = dict(res['non_striker'])
            res['bowler'] = dict(res['bowler'])
            res['bowler'] = dict(res['bowler'])

            return res
        except Exception as e:
            print("Exception in 'batsman_record': {}".format(str(e)))
            raise
    
    def bowler_record(self, bowler):
        try:
            data = self.supabase.table("IPL_stats").select("batter, non-striker, isWicketDelivery, BattingTeam").eq("bowler", bowler).execute()
            res = {
                "bowler" : bowler,
                "wicket_delivery" : 0,
                "total_balls_played" : len(data.data),
                "non_striker" : defaultdict(int),
                "batter" : defaultdict(int),
                "batting_team" : defaultdict(int)
            }
            for i in data.data:
                res["wicket_delivery"] += i["isWicketDelivery"]
                res["non_striker"][i["non-striker"]] += 1
                res["batter"][i["batter"]] += 1
                res["batting_team"][i["BattingTeam"]] += 1
            
            res["non_striker"] = dict(res["non_striker"])
            res["batter"] = dict(res["batter"])
            res["batting_team"] = dict(res["batting_team"])
            return res
        except Exception as e:
            print("Exception in 'bowler_record': {}".format(str(e)))
            raise

    def batsman_vs_bowler(self, batsman, bowler):
        try:
            data = self.supabase.table("IPL_stats").select("ID, total_run, isWicketDelivery").eq("batter", batsman).eq("bowler", bowler).execute()
            s = set()
            res = {
                "batsman" : batsman,
                "bowler" : bowler,
                "total_matches_played" : 0,
                "total_runs_by_batsman" : 0,
                "total_wickets_by_bowler" : 0
            }
            for i in data.data:
                if i['ID'] not in s:
                    s.add(i['ID'])
                    res['total_matches_played'] += 1
                res['total_runs_by_batsman'] += i['total_run']
                res['total_wickets_by_bowler'] += i['isWicketDelivery']
            return res
        except Exception as e:
            print("Exception in 'batter_against_bowler': {}".format(str(e)))
            raise        

    def team_in_venue(self, team):
        try:
            data = (
                self.supabase.table("IPL")
                .select("Venue, Match_Winner, Win_Margin")
                .or_(f"Team1.eq.{team},Team2.eq.{team}")
                .execute()
            )

            venue_stats = defaultdict(lambda: {
                "matches_played": 0,
                "matches_won": 0,
                "total_win_margin": 0,
                "average_win_margin": 0.0
            })

            for match in data.data:
                venue = match['Venue']
                venue_stats[venue]["matches_played"] += 1
                if match["Match_Winner"] == team:
                    venue_stats[venue]["matches_won"] += 1
                    venue_stats[venue]["total_win_margin"] += match.get('Win_Margin', 0)

            for stats in venue_stats.values():
                if stats["matches_won"] > 0:
                    stats["average_win_margin"] = round(stats["total_win_margin"] / stats["matches_won"], 2)
                else:
                    stats["average_win_margin"] = 0.0

            return dict(venue_stats)

        except Exception as e:
            print(f"Exception in 'team_in_venue': {str(e)}")
            raise
            
            
