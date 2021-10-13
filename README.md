<h1 align="center">Boar Bot</h1>
 
<p align="center"><i> Official discord bot for The Order of The Boar Discord server.<br>
 Join us and call it's commands at: https://discord.gg/rpUv8fe </i></p>  
 
### How to run on your machine
1. Pip install all libaries listed on "requirements.txt"
2. Install PostgreSQL on your machine.
3. Fill "localCreds.json" with the credentials of your database
4. Run "setup.py" in order to create the tables
5. Create a app in the Discord Developer Portal and paste it's token into "localToken.txt"
6. Run "bot.py", then the bot will be up and running if everything is fine
7. Add the bot to a server and test it's commands
 
### How to run on Heroku
1. Setup the PostgreSQL Add-On on your app, the code will read the credentials from the environment variables
2. Create a new environment variable on Heroku called "TOKEN" and place your token there
3. Upload the project files on your Heroku repository then run it
4. Add the bot to a server and test it's commands
5. (opt) - You'll probabily need to change the timezone from your app in order to collect the data precisely, create a environment variable called "TZ" and fill it with your timezone name from this [list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
 
 
 *(PS) You can change how the credentials are read at line 218 from "CRUD.py" and the token at line 87 from "bot\
 (PS) There are some additional steps to make the C modules work, this will be covered in the future.*

 

