# https://zulko.github.io/moviepy/
from moviepy.editor import VideoFileClip
from moviepy.editor import ImageSequenceClip


def video2gif(input_video_file_location, output_gif_file_location):
    """Takes an video file and converts it to a modestly configured gif file.
    Perfect for quick examples in github repos."""

    video = VideoFileClip(input_video_file_location)

    frames = []
    for index, frame in enumerate(video.iter_frames()):
        if index % 20 == 0:
            frames.append(frame)

    clip = ImageSequenceClip(frames, fps=2)
    clip.write_gif(output_gif_file_location)
    clip.close()


if __name__ == "__main__":
    input_file_name = input("Input file name: ")

    default_output_file_name = ".".join(input_file_name.split(".")[:-1] + ["gif"])
    output_file_name = input(f"Output file name ({default_output_file_name}): ")
    if not output_file_name:
        output_file_name = default_output_file_name

    video2gif(input_file_name, output_file_name)
