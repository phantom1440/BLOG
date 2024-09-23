from werkzeug.utils import secure_filename
from config import app
import uuid as uuid
import os

def get_file_name(file_name):

    picture_name = secure_filename(file_name.filename)
    unique_name = str(uuid.uuid1())+"_"+picture_name
    return unique_name

def upload_file_to_folder(pict, file_name):
    return pict.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file_name))



