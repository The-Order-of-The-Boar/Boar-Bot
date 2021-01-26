<h1 align="center">Boar Bot</h1>
 
 <p align="center"><i> Official discord bot for The Order of The Boar Discord server.<br>
 Join us and call it's commands at: https://discord.gg/rpUv8fe </i></p>  
 
 <h3><b>How to run on your machine</b></h3>
 <br>1 - Pip install all libaries listed on "requirements.txt"
 <br>2 - Install PostgreSQL on your machine.
 <br>3 - Fill "localCreds.json" with the credentials of your database
 <br>4 - Run "setup.py" in order to create the tables
 <br>5 - Create a app in the Discord Developer Portal and paste it's token into "localToken.txt"
 <br>6 - Run "bot.py", then the bot will be up and running if everything is fine
 <br>7 - Add the bot to a server and test it's commands
 <br>
 <h3><b>How to run on Heroku</b></h3>
 <br>1 - Setup the PostgreSQL Add-On on your app, the code will read the credentials from the environment variables
 <br>2 - Create a new environment variable on Heroku called "TOKEN" and place your token there
 <br>3 - Upload the project files on your Heroku repository then run it
 <br>4 - Add the bot to a server and test it's commands
 <br>5 - (opt) - You'll probabily need to change the timezone from your app in order to collect the data precisely, create a environment variable called "TZ" and fill it with your timezone name from this list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
 
 <p>
 <br><i>(PS) You can change how the credentials are read at line 218 from "CRUD.py" and the token at line 87 from "bot</i>
 <br><i>(PS) There are some additional steps to make the C modules work, this will be covered in the future.</i>

 </p>

