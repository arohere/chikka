# Kartus, a bot for the VITC discord server

### Requirements:

- Python
- MySql

### Structure

- kartus/main/main.py 
        imports kartus/main/initdb.py if Storage.db dosen't exist 
        imports kartus/main/cogs/setup_commands.py as an extension/cog 
        imports kartus/main/cogs/sign_up.py as an extension/cog
        imports kartus/main/cogs/resources/selects_for_course.py for selects


### Commands & Features


- <b>!signup</b> - signup with kartus and you will be able to do the following
<br>⭐ Find Peers with similar Courses
<br>⭐ Conduct a short survey to rate faculties
<br>⭐ To View or Add Faculties to Blacklist/Whitelist
<br>⭐ Notify before a class starts (optional) <br>
![Welcome Screen](https://imgur.com/pSkS3J8.png)
![Details](https://imgur.com/Q0H6xRX.png)
![Schedule Upload](https://imgur.com/nKZ9PS6.png)

- <b>!rate</b> - rate your current semester's faculties
- <b>!report</b> - attach screenshots and report bugs
- <b>!fetchintro</b> - Fetches your Introduction from the <mark style="background-color: lightgrey;">#intro</mark> Channel
- <b>!weeklyschedule</b> - After Uploading your schedule using !signup you can view your weekly schedule using this command


![Schedule Upload](https://imgur.com/aQvjiOw.png)


### To-Add Commands

- help
- uploadschedule
- deleteschedule
- listschedules
- weekschedule
- dayschedule
- scanschedule
- task(first message in the morning, view classes)
- message log
- logs channel
- fetchinvite
- ping vc members
- votepin feature
- roomfeature
- add/change guild prefix
- blacklist / whitelist with recordings link  / leaderboard for faculty
- prefix change/add
- fetchintro

### Features to be Implemented

    1. Create a rating embed/interaction
        i. create another table to store clients last rated date and last notified date ✔
        ii. ask for rating after sign up 
        iii. check every monday for clients who have not rated for one month or have been notified two weeks before ✔
        iv. create global check to see if user has rated past one month 
        v. to display the rating, find the mean and mean deviation and mention lesser the deviation more accurate the value is ✔
        vi. check campus while rating and use semester ID to find current semester ✔
    2. Add a change semester feature with update schedule feature
    3. fetch data from table_2 html, format, cpickle and store in mysql table with semester_id. 
        i. to retrive current sem data, from current sem fetch current_semester and use to reference schedule_data
    4. add reloading commands permissions only for kartus devs
    5. Create Roles for each department, give verified role to signups and add checks to kartus such that only verified ppl can use commands
    6. Make a copy of the HTML files
    7. convert normal sqlite3 to asynciosqlite3


### To Host and Test the discord bot.
Add python to PATH if you haven't already

Powershell

```
python -m venv .venv
.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

CMD

```
python -m venv .venv
.venv/Scripts/activate.bat
pip install -r requirements.txt
```

Add bot token to .env file in ./main.py
