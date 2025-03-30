from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi import Path
from supabase_client import Data

app = FastAPI()
data = Data()

@app.get("/")
async def index():
    return FileResponse("index.html")

# Endpoint to get all matches data
@app.get("/sid/all", response_class=JSONResponse)
def teams():
    result = data.get_all_matches_data()
    return result

# Endpoint to get all teams ever played
@app.get("/sid/teams", response_class=JSONResponse)
def teams():
    result = data.get_teams()
    return result

# Endpoint to get team vs team info
@app.get("/sid/team_vs_team_info/{team1},{team2}", response_class=JSONResponse)
def teams(team1: str = Path(...), team2 :str = Path(...)):
    result = data.team_vs_team_info(team1, team2)
    return result

# Endpoint to get team vs team stats
@app.get("/sid/team_vs_team_stats/{team1},{team2}", response_class=JSONResponse)
def teams(team1: str = Path(...), team2 :str = Path(...)):
    result = data.team_vs_team_stats(team1, team2)
    return result

# Endpoint to get team vs all data
@app.get("/sid/team_vs_all/{team}", response_class=JSONResponse)
def teams(team: str = Path(...)):
    result = data.team_vs_all(team)
    return result

# Endpoint to get batsman record
@app.get("/sid/batsman_record/{batsman}", response_class=JSONResponse)
def teams(batsman: str = Path(...)):
    result = data.batsman_record(batsman)
    return result

# Endpoint to get bowler record
@app.get("/sid/bowler_record/{bowler}", response_class=JSONResponse)
def teams(bowler: str = Path(...)):
    result = data.bowler_record(bowler)
    return result

# Endpoint to get batsman vs bowler data
@app.get("/sid/batsman_vs_bowler/{batsman},{bowler}", response_class=JSONResponse)
def teams(batsman: str = Path(...), bowler: str = Path(...)):
    result = data.batsman_vs_bowler(batsman, bowler)
    return result

# Endpoint to get team played in each venue data
@app.get("/sid/batsman_record/{team}", response_class=JSONResponse)
def teams(team: str = Path(...)):
    result = data.team_in_venue(team)
    return result
