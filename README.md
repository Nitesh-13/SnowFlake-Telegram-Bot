# SnowFlake

An attendance telegram bot to manage attendance over telegram.
The following commands are currently implemented in the bot :
- '**/start**' - Displays welcome message.
- '**/startatt**' - Start the attendance.
- '**/showatt**' - Show the attendance list.
- '**/clearatt**' - Clears the attendance list.
- '**/photo**' - Sends a random dog image
- '**/fact**' - Sends a random fact.

## Installation
Firstly we need to install all the required libraries required for the bot to use its different functions properly.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries.

Step 1 : Open terminal or command prompt and type the command :
```bash
pip install -r /path/to/requirements.txt
```
Step 2 : Open telegram and search [@BotFather](https://telegram.me/BotFather) and click start.

Step 3 : Now send the command '**/newbot**' and follow the instructions given by the bot.

Step 4 : After that note down the api of the bot and edit it inside the bot.py
```python
bot = telebot.TeleBot("BOT_API_HERE")
```

Step 5 : Now create a remote mysql database and add the credentials inside the bot.py
```python
stud_db = mysql.connector.connect(
  host="hostname_here",
  user="username_here",
  password="password_here",
  database="database_name_here"
)
```

Step 6 : Run the python script

```bash
python bot.py
```


>Note : You can run the script in a virtual environment on a cloud system, so that the bot can stay online for long period.



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
