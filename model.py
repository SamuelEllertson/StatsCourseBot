from queryspec import Intent
import nltk
import string


"""This is for parsing the intent from a message, as well as extracting the relevant information
from a message based on the intent"""


class Model:
    def __init__(self, args, datastore, iohandler):
        self.args = args
        self.datastore = datastore
        self.iohandler = iohandler

        # -> Tuple[str, typing.List[str]]:

    def extract_variables(self, query: str):
        """Takes in a raw query from the user and extracts the variables from that query, then generalizes the query.
            Returns the list of variables and the generalized form of that query."""
        tokens = nltk.word_tokenize(query)
        tags = nltk.pos_tag(tokens)
        general_query = ""
        terms = ["summer", "spring", "fall", "winter"]
        vars = []
        stop_words = set(nltk.corpus.stopwords.words("english"))
        topic_words = ["on", "about", "covering"]
        i = 0
        while i < len(tags):
            # Class id found
            if tags[i][1] == "CD":
                vars.append(tags[i][0])
                # A list of classes is represented as [CLASSES]
                if "[CLASS]" in general_query:
                    general_query = general_query.replace("[CLASS]", "[CLASSES]")
                elif "[CLASSES]" not in general_query:
                    general_query += "[CLASS] "
            # Term name found
            elif tags[i][0].lower() in terms:
                vars.append(tags[i][0].lower())
                general_query += "[TERM]" #why no space here?
            # Connecting word that introduces a topic found
            elif tags[i][0] in topic_words:
                j = i + 1
                # Get the entire topic
                while j < len(tags):
                    if tags[j][0] in stop_words: # you think that this means the intent is finished?
                        break
                    vars.append(tags[j][0].lower())
                    j += 1
                general_query += tags[i][0] + " "
                general_query += "[TOPIC] "
                i = j - 1
            else:
                general_query += tags[i][0]
                general_query += " "
            i += 1
        return general_query.strip(), vars

    def get_intent(self, message: str) -> Intent:
        """Takes in a raw message, and determines its intent, returning Intent.UNKNOWN
        if it can not determine within some tolerance. It is permitted, and encouraged, to ask 
        additional questions to determine a users intent"""
        return Intent.UNKNOWN

    def get_course_id(self, message: str) -> int:
        """This method is very important, being called on all but one intents. 
        It takes in a raw message, and determines which single course it is refering to.
        It could be in the form of some or parts of its title, or its course id.
        It should aggressively try its options to come up with its best guess, or None if it has no idea"""
        return 312

