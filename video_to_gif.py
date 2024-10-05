from moviepy.editor import VideoFileClip
videoClipe = VideoFileClip
def video_to_gif (videopath): videoClipe = VideoFileClip("videopath")
inicio = 10
fim = 20
fps = 24

videoClipe.subclip(inicio, fim).write_gif("seu_gif.gif")
