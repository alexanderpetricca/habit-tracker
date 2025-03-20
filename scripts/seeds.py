from config.settings import DEBUG


# python manage.py runscript seeds

def run():
    """
    Replace all database data with test data for development.
    """

    confirm = input('Replace all existing data on database with test data?')

    if (confirm.lower() == 'y') and (DEBUG):
        pass