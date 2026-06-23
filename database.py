import sqlite3

connection = sqlite3.connect("mydatabase.db")
curr = connection.cursor()

username = input("Enter your username: ")
name = input("Enter your name: ")
location = input("Enter your location: ")

#if the username is already in the databse it ask the user if their location
# is the current one assoicated with the username 
# yes - same user
#no new user and tell me that username is already taken
curr.execute(
  "INSERT INTO usersInfo (username, name, location) VALUES (?, ?, ?)",
  (username,name,location)
)

connection.commit()
connection.close()

