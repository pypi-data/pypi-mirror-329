from ..fpcli_settings import CONFIG_FOLDER
def get_init_content():
    return f'''from {CONFIG_FOLDER}.database import Database
database= Database()
db=database.get_db
'''