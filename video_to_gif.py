from moviepy.editor import VideoFileClip
videoClipe = VideoFileClip
def video_to_gif(videopath): 
    videoClipe = VideoFileClip(videopath)
    inicio = 0
    fim = 2
    fps = 24

    gif_path = videopath.replace('.mp4', '.gif').replace('videos', 'gifs')
    videoClipe.subclip(inicio, fim).write_gif(gif_path)
    return gif_path

