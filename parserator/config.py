########################################
####### TOKEN LABEL CONFIG #############
########################################

# these are the labels for tagging tokens
# example: LABELS = [ 'GivenName', 'MiddleName', 'Surname', 'Nickname' ]

LABELS = []



########################################
######## OPTIONAL CONFIG ###############
########################################

NULL_LABEL = 'Null'

# this is the xml tag for each string in training data. example: PARENT_LABEL = 'Name'
PARENT_LABEL = 'TokenSequence'

# this is the tag for a group of strings. example: GROUP_LABEL = 'NameCollection'
GROUP_LABEL = 'Collection'

# filename for settings file
MODEL_FILE = 'learned_settings.crfsuite'

# filename for training data (from which the model is produced)
TRAINING_FILE = 'labeled.xml' ########## should this be set here?