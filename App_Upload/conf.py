import os
ABS_PATH = os.path.abspath(__file__)
APP_BASE_DIR = os.path.dirname(ABS_PATH)
PROJECT_BASE_DIR = os.path.dirname(APP_BASE_DIR)
DATA_DIR = os.path.join(PROJECT_BASE_DIR, 'media')
VIDEO_DIR = os.path.join(DATA_DIR, 'upload_video')
THUMBNAIL_DIR = os.path.join(DATA_DIR, 'upload_thumbnail')