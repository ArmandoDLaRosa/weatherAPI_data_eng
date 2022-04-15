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
### Database = TSDB
* Influx DB

### Important Files
* [aggs.py](), aggregates stored data
* [main.py](), pulls current data and appends it to influx db
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
1) Execute this in the cmd
  ```
   crontab -e 
  ```
2) Add the cron job like this, so it runs every 10 minutes using a python environment
   */10 * * * * /home/user/project/env/bin/python /home/user/project/main.py 

3) Start the service
  ```
  sudo service cron start
  ```
3.2) Restart the service 
  ```
  sudo service cron reload
  ```
3.3) Start the service
  ```
  sudo service cron stop
  ```

## CLOSE / RESTART / START  THE PROJECT
---
### Repository
  * Create 1 in github and a 7 days token
  * Clone it in vscode
  * Create a branch to develop
  * Create a `config.ini` file, below is just an example
    ```
      [API]
      api_key: alphanumeric
      locations: city,country/city,country/

      [DATABASE]
      token = alphanumeric
      organization = org_name
      bucket = bucket_name
    ```
    * When needed you can read the variables like this:
        ```
        from configparser import ConfigParser

        #Read config.ini file
        config_object = ConfigParser()
        config_object.read("config.ini") #Path

        #Get the password
        api_keys = config_object["API"]
        print(f'{api_keys["apiname_key"]}')
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

[OpenWeather - Current API Doc](https://openweathermap.org/current)

[Requests - timeouts, retries, hooks](https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/)

[Youtube TSDB Intro](https://www.youtube.com/watch?v=OoCsY8odmpM)



