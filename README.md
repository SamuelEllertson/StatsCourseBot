

## Authors: Samuel Ellertson, Noah Stapp, Max Barshay, Matthew Bennin

### Setup: Create a virtual environment, activate it, and do 'pip install -r requirements.txt'

# Style guideline:
- 4 space indentation (not tabs)
- Function/method names: snake_case
- Please use descriptive, non-shortened variable names, unless their meaning is obvious enough
- keep your 'public' methods near the top, seperated from your internal logic methods, so that things remain clear
- Add docstrings to all your 'public' methods, documenting purpose, param types, and return types
    - type hints on params and return types, for 'public' methods, is prefered

# TODO:
- Assign questions and create 120 variations total
- Divide work among us
    - datastore.py    - SQL stuff
    - responder.py    - parsing messages and discovering user intent
    - dataupdater.py  - Scraping and parsing course data
- Create presentation

# Components:
    
filename: ClassName

- main.py: no class
    - parse arguments
    - create DataStore
    - create IOHandler object
    - tell IOHandler to listen for messages

- iohandler.py: IOHandler
    - platform agnostic
        - terminal
        - ircbot
    - recieves messages
        - provides prompt for terminal use
        - Responder provides responses
    - can send responses
    - can ask follow up questions

- ircbot.py: IRCBot
    - interacts with irc service
    - relays recieved messages to IOHandler
    - can send messages

- responder.py: Responder
    - recieves raw text queries from IOHandler
    - generates response based on Intent returned from Model
    - can ask IOHandler additional questions to help narrow down options

- model.py: Model
    - determines a messages intent based on its raw content
    - has access to the DataStore

- queryspec.py: Intent(Enum), QueryPattern(Enum)
    - canonical list of all the defined intents
    - also maps an intent to its corresponding query pattern
        - a query pattern is the format of variables in the question

- datastore.py: DataStore
    - handles interaction with database
    - provides high level access to data
        - class names
        - class discriptions
        - lookups (ie: class name -> terms offered)
        - etc
    - defines the Course object

- db.json
    - database credential and config file for the production database (hosted on frank)
    - a db(EXAMPLE).json file is provided, the real db.json is excluded from git to avoid posting the password publically.

- db_dev.json
    - database credential and config file for local development database.

- dataupdater.py: implement as you desire
    - independant component
    - periodically scrapes calpoly website(s)
    - updates database

# Commandline argument spec:
    format: -flag "destination name" purpose

    -v            "verbose"     toggles additional output for debugging purposes
    --dev         "dev_mode"    turns on development mode, which uses a local database as defined in db_dev.json
    --irc         "use_irc"     with this flag set, use irc instead of the terminal
    --irc-host    "irc_host"    sets which irc host to connect to, defaults to irc.freenode.net
    --irc-channel "irc_channel" sets irc channel to use, defaults to '#CSC466'
    --bot-name    "bot_name"    sets the bots name, defaults to 'StatsCourseBot'


# Course listing terminology:
    Always use these names as specified to keep things consistent across our code

    Example listing: (modified)
        STAT 427. Mathematical Statistics.   1-4 units
        Prerequisite: STAT 426. Recommended: STAT 302.
        Continuation of STAT 426. The theory of hypothesis testing and its applications. Power and uniformly 
        most powerful tests. Categorical data and nonparametric methods. Other selected topics. 4 lectures.
        Substantial use of statistical software

    format: term: relevant portion -> type(extracted information)

        id:              STAT 427.                  -> int(427)
        title:           Mathematical Statistics.   -> str(Mathematical Statistics)
        prereqs:         STAT 426.                  -> str(STAT 426. Recommended: STAT 302.)  
        units:           1-4 units                  -> str(1-4)
        about:           Continuation ... lectures  -> str(Continuation ... lectures)
        coding_involved  use of ... software        -> bool(true)
        elective                                    -> bool(false)
        terms                                       -> set("fall", "winter", "spring", "summer")

# Other
- Work on a git branch. **DO NOT PUSH BROKEN CODE TO MASTER**
- I highly recommend using pyflakes to inspect your code before commiting, and generally as part of your dev cycle
