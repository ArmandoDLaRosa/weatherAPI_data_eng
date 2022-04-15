# Weather Data Data Engineering Mini Project
Context: Work with a weather API to store data within certain date range in an influx DB, to later do aggregations and visualizations. 

## Tools 
---
### Data Source
* [Open Weather FREE API](https://openweathermap.org/)
###  Dev Environment
* WSL (Ubuntu 20.04)
* Vscode (Remote Wsl, Python Extension)
* Postman
* [Influx Data](influxdata.com)
### Languages and Libraries
* Python
  * configparser, Helps to work with config.ini files
  * python3-virtualenv, Create python environments
### Database
* Influx DB
### Cron Jobs
### Important Files
* [DataRequest.py]()
* [Python Requirements]()
* [Variables Template]()
* [Python Env Folder]()

## VSCODE SETUP 
---
0) Make sure you've WSL working in VSCODE and your USER/Root passwords in hand. 
1) Create python environment (venv files should be good inside the project folder)
    ```
    sudo apt install python3-virtualenv
    virtualenv open_weather_project_env
    ```
2) Activate python environment
    ``` 
    source open_weather_project_env/bin/activate
    ```
3) Change in vscode the interpreter to the python inside open_weather_project_env/bin/python3.8 
   1) This way you can run the .py with the extension RUN button with the env activated.
   2) Otherwise, you'll have to run it like `python3 fileName.py` and the env activated.

## CRON JOB SETUP 
---

## SQLite SETUP  (Store the logs of the cron job)
---

## Influx SETUP  (Store the Time Series and aggregations)
---


## CLOSE / RESTART / START  THE PROJECT
---
### Repository
  * Create 1 in github and a 7 days token
  * Clone it in vscode
  * Create a branch to develop
  * Create a `config.ini` file, below is just an example
    ```
      [DATABASE]
      NAME: dbName
      USER: wslConnection
      PASSWORD: ________
      HOST: windows Ipv4

      [DJANGO]
      SECRET_KEY = 
    ```
    * When needed you can read the variables like this:
        ```
        from configparser import ConfigParser

        #Read config.ini file
        config_object = ConfigParser()
        config_object.read("config.ini") #Path

        #Get the password
        userinfo = config_object["DATABASE"]
        print(f'{dataBaseInfo["HOST"]}')
        ```
  * Create a git ignore file, for inspo look at this forked repo [.gitignore examples](https://github.com/ArmandoDLaRosa/gitignore)
    * `nano .gitignore`
    * Paste inside the example + add `config.ini` file's name
### Other
* Save requirements to install (activate the virtual env)
    `pip freeze > requirements.txt`
* Load the requirements (start a virtual env first)
    `sudo apt install python3-pip`
    `virtualenv <envName>`
    `pip install -r requirements.txt`
* Close/Open the virtual env
* Open/Shutdown WSL, Vscode, other .exe
* Commit the changes with a meaninful commit message


## Dealing with security risks related to git commits
---
[Step by Step](https://sethrobertson.github.io/GitFixUm/fixup.html)

[Reset Hard Recovery](https://stackoverflow.com/questions/7374069/undo-git-reset-hard-with-uncommitted-files-in-the-staging-area)

[Reset Commit History](https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github)

## Resources Used
---
[Example Link]()


