from moviepy.editor import VideoFileClip
videoClipe = VideoFileClip
def video_to_gif(videopath): 
    videoClipe = VideoFileClip(videopath)
    inicio = 5
    fim = 10
    fps = 24

    videoClipe.subclip(inicio, fim).write_gif(videopath.replace('.mp4', '.gif'))

#video_to_gif("video.mp4")