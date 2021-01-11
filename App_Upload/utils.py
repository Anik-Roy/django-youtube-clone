from App_Upload.conf import VIDEO_DIR, THUMBNAIL_DIR
import os
from moviepy.editor import *
from PIL import Image

# print(VIDEO_DIR, THUMBNAIL_DIR)

def generate_thumbnail(video_file_source):
    video_file_name = video_file_source.replace('upload_video/', '')
    source_path = os.path.join(VIDEO_DIR, video_file_name)
    # thumbnails_dir = os.path.join(DATA_DIR, 'media/upload_thumbnail')
    # os.makedirs(thumbnails_dir, exist_ok=True)

    clip = VideoFileClip(source_path)
    fbs = clip.reader.fps
    nframes = clip.reader.nframes
    duration = clip.duration
    max_duration = int(clip.duration) + 1
    print(max_duration)
    frame_at_second = 3
    frame = clip.get_frame(frame_at_second)
    new_image_filepath = os.path.join(THUMBNAIL_DIR, f"{video_file_name}_{frame_at_second}.jpg")
    new_image = Image.fromarray(frame)
    new_image.save(new_image_filepath)
    return 'upload_thumbnail/'+f'{video_file_name}_{frame_at_second}.jpg'

    # for i in range(0, max_duration):
    #     frame = clip.get_frame(i)
    #     new_image_filepath = os.path.join(thumbnails_dir, f"{i}.jpg")
    #     new_image = Image.fromarray(frame)
    #     new_image.save(new_image_filepath)
