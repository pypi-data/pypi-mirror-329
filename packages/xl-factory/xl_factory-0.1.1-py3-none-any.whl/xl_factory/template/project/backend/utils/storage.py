from xl_storage import Storage
from backend.config import MINIO_CONFIG


def get_instance():
    return Storage(MINIO_CONFIG)
                   
def upload_file(bucket, uri, file):
    storage = get_instance()
    storage.upload_file(bucket, uri, file)
    return f'{bucket}/{uri}'

