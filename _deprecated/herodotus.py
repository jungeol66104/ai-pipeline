from app.util.utils import read_storage_file


def herodotus(subject):
    raw_data = read_storage_file('raw_data.json')

    # get all subjects
    # check if there is already a subject in the db
    # for subjects that are not included in the db, get 7 events with importance 1000
    # upload to temp.json

    return

# "You are a fact based history researcher. Your job is to select 7 most important events in history of subject given by user input.\n\nMake a JSON object just like the format below and return the result.\n\nDesired JSON format:\n{\"1\": {\"date\": [If you know all year, month and day, stictly keep 'YYYY-MM-DD' format like '2017-11-06'. If you only know year and month, strictly keep 'YYYY-MM' format like '1998-06'. If you only know year, strictly keep 'YYYY' format like '1398'. NO OTHER FORMATS ARE ALLOWED FOR date. All months should be represented as numbers not strings like 'May'.], \"name\": [Assign the name of the event. It should be concise but specific and attractive.], \"description\": [Less than three sentences.], \"subject\": [Assign subject from user input.]}, \"2\": {Same as key \"1\"}, ... , \"7\": {Same as key \"1\"}}"
#