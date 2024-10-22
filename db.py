import psycopg2
def connect():
    conn = psycopg2.connect(
    host ="kashin.db.elephantsql.com",
    user ="vjhcmtzq",
    password ="hOpz0dC5TlzI98g6gu4KnuKH2nWsYvgy",
    database="vjhcmtzq",
    port="5432")
    return conn
