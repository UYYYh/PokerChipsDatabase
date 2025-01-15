from sqlalchemy import create_engine, text
from contextlib import contextmanager
from CashGame import CashGame
from Player import Player
from datetime import datetime
import os, uuid

from Tournament import Tournament

noOne = Player("No One")
engine = "Uninitialised"

def InitialiseMySQL() -> engine:
    global engine
    if engine == "Uninitialised":
        # Fetch MySQL credentials from environment variables
        mySQLPassword = os.environ.get("CHATAPIADMINPASSWORD")
        mySQLUsername = os.environ.get("CHATAPIADMINUSERNAME")
        
        # Specify the new database name ('poker_game_db')
        engine = create_engine(f"mysql+pymysql://{mySQLUsername}:{mySQLPassword}@localhost:3306/poker_chips_db", pool_size=20, max_overflow=10)
        
    return engine

engine = InitialiseMySQL()

@contextmanager
def get_db_connection():
    try:
        connection = engine.connect()
        yield connection
    finally:
        connection.close()

def execute_sql(query: str, params: dict, fetch: bool = False):
    with get_db_connection() as connection:
        result = connection.execute(text(query), params)
        connection.commit()
        return result if fetch else None


def test_connection():
    try:
        # Initialise the engine
        engine = InitialiseMySQL()
        
        # Establish connection
        with engine.connect() as connection:
            # Test with a simple query (selecting from an existing table or running a small SQL command)
            result = connection.execute(text("SELECT 1"))
            print("Connection successful:", result.scalar())
            
    except Exception as e:
        print("Error connecting to the database:", str(e))
        

def create_player(name: str, chips: int = 20000) -> None:
    query = "INSERT INTO player (name, chips) VALUES (:name, :chips)"
    params = {"name": name, "chips": chips}
    execute_sql(query, params)
  

def change_chip_count(name: str, change: int):
    query = "UPDATE player SET chips = chips + :change WHERE name = :name"
    params = {"name": name, "change": change}
    execute_sql(query, params)
    
def player_exists(name: str) -> bool:
    query = "SELECT COUNT(*) FROM player WHERE name = :name"
    params = {"name": name}
    result = execute_sql(query, params, fetch=True)
    return result.scalar() == 1

def get_player_chips(name: str) -> int:
    query = "SELECT chips FROM player WHERE name = :name"
    params = {"name": name}
    result = execute_sql(query, params, fetch=True)
    return result.scalar()

def _create_tournament(buy_in : int, date : str) -> str:
    tournament_id = str(uuid.uuid4())
    query = "INSERT INTO tournament (tournament_id, date, buy_in) VALUES (:tournament_id, :date, :buy_in)"
    params = {"tournament_id": tournament_id, "date": date, "buy_in": buy_in}
    execute_sql(query, params)
    return tournament_id

def _create_cash_game(buy_in : int, date : str) -> str:
    cash_game_id = str(uuid.uuid4())
    query = "INSERT INTO cash_game (cash_game_id, date, buy_in) VALUES (:cash_game_id, :date, :buy_in)"
    params = {"cash_game_id": cash_game_id, "date": date, "buy_in": buy_in}
    execute_sql(query, params)
    return cash_game_id
    
def record_tournament(tournament : Tournament) -> str:
    tournament_id = _create_tournament(tournament.buy_in, tournament.date)
    chip_changes = tournament.calculate_change()
    for player in tournament.players:
        if not player_exists(player.name):
            create_player(player.name)
    
    for player in tournament.players:     
        chip_change = chip_changes[player]
        
        query = """
        INSERT INTO tournament_player (name, tournament_id, busted_by, no_buy_ins, placement, change_in_chips)
        VALUES (:name, :tournament_id, :busted_by, :buy_ins, :placement, :change_in_chips)
        """
        params = {"tournament_id": tournament_id, "name": player.name, "placement": player.placement, "buy_ins": player.buy_ins, "busted_by": player.busted_by.name, "change_in_chips": chip_change}
        execute_sql(query, params)
        change_chip_count(player.name, chip_change)
        
    return tournament_id

def record_cash_game(cash_game : CashGame) -> None:
    cash_game_id = _create_cash_game(cash_game.buy_in, cash_game.date)    
    chip_changes = cash_game.calculate_change()

    for player in cash_game.players:
        if not player_exists(player.name):
            create_player(player.name)

    for player in cash_game.players:
        chip_change = chip_changes[player]
        
        query = """
        INSERT INTO cash_game_player (name, cash_game_id, no_buy_ins, change_in_chips)
        VALUES (:name, :cash_game_id, :no_buy_ins, :change_in_chips)
        """
        params = {"cash_game_id": cash_game_id, "name": player.name, "no_buy_ins": player.buy_ins, "change_in_chips": chip_change}
        execute_sql(query, params)
        change_chip_count(player.name, chip_change)

def revert_cash_game(cash_game_id: str):
    query = "SELECT name, change_in_chips FROM cash_game_player WHERE cash_game_id = :cash_game_id"
    params = {"cash_game_id": cash_game_id}
    result = execute_sql(query, params, fetch=True)
    for row in result.fetchall():
        change_chip_count(row[0], -row[1])
        
    query = "DELETE FROM cash_game WHERE cash_game_id = :cash_game_id"
    execute_sql(query, params)

def revert_tournament(tournament_id: str):
    
    query = "SELECT name, change_in_chips FROM tournament_player WHERE tournament_id = :tournament_id"
    params = {"tournament_id": tournament_id}
    result = execute_sql(query, params, fetch=True)
    for row in result.fetchall():
        change_chip_count(row[0], -row[1])
        
    query = "DELETE FROM tournament WHERE tournament_id = :tournament_id"
    execute_sql(query, params)

def get_leaderboard():
    query = """
    SELECT name, chips FROM player
    ORDER BY chips DESC
    """
    result = execute_sql(query, {}, fetch=True)
    return result.fetchall()


