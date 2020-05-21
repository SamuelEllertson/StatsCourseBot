Authors: Samuel Ellertson, Noah Stapp, Max Barshay

Style guidline:
    4 space indentation

components:
    
    filename: ClassName

    main.py: no class
        parse arguments
        create DataStore
        create IOHandler object
        tell IOHandler to listen for messages

    iohandler.py: IOHandler
        platform agnostic
            terminal
            ircbot
        recieves messages
            provides prompt for terminal use
            message_Answerer provides responses
        can send responses
        can ask follow up questions

    ircbot.py: IRCBot
        interacts with irc service
        relays recieved messages to IOHandler
        can send messages

    responder.py: Responder
        recieves raw text queries from IOHandler
        generates response text to send back
        can ask IOHandler additional questions to help narrow down options

        determines type of question
        extracts relevant information
        consults dataStorage for answers
        crafts response and gives it to IOHandler

    datastore.py: DataStore
        handles interaction with database
        provides high level access to data
            class names
            class discriptions
            lookups (ie: class name -> terms offered)
            etc
    
    db.json
        database credential and config file, JSON format

    dataupdater.py: implement as you desire
        independant component
        periodically scrapes calpoly website(s)
        updates database

