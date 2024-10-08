from dotenv import load_dotenv
from supabase import create_client
import os

# Funkcja do połączenia z Supabase
def init_supabase():
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)

# Funkcja do pobierania danych z tabeli "Test"
def get_data_from_zjazdy():
    supabase = init_supabase()
    data = supabase.table("Test").select("*").execute()
    return data
