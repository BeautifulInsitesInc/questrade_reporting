import sqlite3

conn = sqlite3.connect(riskmit.db)

# Create cursor
c = comm.cursor()

# Create table
c.execute("""CREATE TABLE accounts (
		user_id text,
		account_name text
		)""")