import os
import logging
import uuid
import shutil

class FileSizeLimitError(Exception):
    def __init__(self, *args, **kwargs):
        if args:
            self.message = args[0]
        else:
            self.message = 'File size to large!'
    
    def __str__(self):
        return 'FileSizeLimitError exception, {}'.format(self.message)

class FileExtensionError(Exception):
    def __init__(self, *args, **kwargs):
        if args:
            self.message = args[0]
        else:
            self.message = 'Unsupported file extension!'
    
    def __str__(self):
        return 'FileExtensionError exception, {}'.format(self.message)

class FileMimeTypeError(Exception):
    def __init__(self, *args, **kwargs):
        if args:
            self.message = args[0]
        else:
            self.message = 'Unsupported mime type!'
    
    def __str__(self):
        return 'FileMimeTypeError exception, {}'.format(self.message)

FILE_UPLOADS = {
    'PARENT_FOLDER': os.getenv('FILE_UPLOADS_PARENT_FOLDER'),
    'TEMP_FOLDER': 'tmp',
    'FILE_SETS': {
        'AVATAR': {
            'FOLDER': 'avatars',
            'MAX_SIZE': 8 * 1024 * 1024, # Максимальный размер аватара 8 Мб, спизженно у дискорда,
            'ALLOWED_EXTENSIONS': ('jpg', 'png'),
            'ALLOWED_MIME_TYPES': ('image/jpeg', 'image/jpg', 'image/png')
        },
        'PRESENTATIONS': {
            'FOLDER': 'presentations',
        }
    }
}

for K, V in FILE_UPLOADS['FILE_SETS'].items():
    path = os.path.join(FILE_UPLOADS['PARENT_FOLDER'], V['FOLDER'])
    if not os.path.exists(path):
        os.makedirs(path)
    FILE_UPLOADS['FILE_SETS'][K]['FOLDER'] = path

tmp_path = os.path.join(FILE_UPLOADS['PARENT_FOLDER'], FILE_UPLOADS['TEMP_FOLDER'])

if not os.path.exists(tmp_path):
    os.makedirs(tmp_path)
FILE_UPLOADS['TEMP_FOLDER'] = tmp_path

def saveAvatar(file, filename):
    file_set = FILE_UPLOADS['FILE_SETS']['AVATAR']
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    if file_extension not in file_set['ALLOWED_EXTENSIONS']:
        raise FileExtensionError
    if file.mimetype not in file_set['ALLOWED_MIME_TYPES']:
        raise FileMimeTypeError
    if file.content_length > file_set['MAX_SIZE']:
        raise FileSizeLimitError
    if file:
        path = os.path.join(FILE_UPLOADS['TEMP_FOLDER'], str(uuid.uuid4()))
        file.save(path)
        size = os.stat(path).st_size
        logging.debug('File size is {}'.format(size))
        if size > file_set['MAX_SIZE']:
            os.remove(path)
            raise FileSizeLimitError
        new_path = os.path.join(file_set['FOLDER'], filename)
        shutil.move(path, new_path)
        return True
    return False