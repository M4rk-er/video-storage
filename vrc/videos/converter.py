import ffmpeg


def change_video_resolution(file_path, new_filename, width, height):
    new_resolution = str(width) + 'x' + str(height)

    ffmpeg.input(
        file_path
    ).output(
        new_filename,
        vf=f'scale={new_resolution}',
        acodec='copy'
    ).run()
