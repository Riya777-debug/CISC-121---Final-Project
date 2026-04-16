import gradio as gr
import matplotlib.pyplot as plt

# groups all the attributes of a song together
class song:
    def __init__(self, title, artist, duration, tempo, streams):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.tempo = tempo
        self.streams = streams

#list of songs to sort
songs = [song("Swim", "BTS", 159, 94, 248.3), song("Firework", "Katy Perry", 228, 124, 1499.1)]

def add_song(title, artist, duration, tempo, streams):
    songs.append(song(title, artist, duration, tempo, streams))
    return f"Added {title} by {artist}"


def remove_song(title):
    global songs
    for s in songs:
        if s.title.lower() == title.lower():
            songs.remove(s)
            return f"Removed {title}"
    return f"{title} not found!"


def view_playlist():
    return ", ".join([s.title for s in songs])

#merge sort
#splits the list into half repeatedly
def merge_sort(arr, key):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return merge(left, right, key)
#mergess the sorted smaller lists together
def merge(left, right, key):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if getattr(left[i], key) < getattr(right[j], key):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
#plots the songs based on the selected key
def plot_songs(key):
    sorted_songs = merge_sort(songs, key)
    titles = [s.title for s in sorted_songs]
    values = [getattr(s, key) for s in sorted_songs]

    plt.figure()
    plt.bar(titles, values)
    plt.xticks(rotation=45)
    return plt

#gradio - creates a user interface for the program
with gr.Blocks() as demo:
    gr.Markdown("# Playlist Manager 🎵")

    # Add songs
    gr.Markdown("### Add a Song")
    add_title = gr.Textbox(label="Title")
    artist = gr.Textbox(label="Artist")
    duration = gr.Number(label="Duration")
    tempo = gr.Number(label="Tempo")
    streams = gr.Number(label="Streams")
    add_btn = gr.Button("Add Song")

    # Remove songs
    gr.Markdown("### Remove a Song")
    remove_title = gr.Textbox(label="Title to remove")
    remove_btn = gr.Button("Remove Song")

    # Outputs
    output = gr.Textbox(label="Output")
    playlist = gr.Textbox(label="Playlist")

    # Chart
    gr.Markdown("### Visual Sort")
    key_dropdown = gr.Dropdown(
        choices=["title", "artist", "duration", "tempo", "streams"],
        label="Sort by"
    )
    chart = gr.Plot()

    gr.Button("Show Chart").click(
        plot_songs,
        inputs=key_dropdown,
        outputs=chart
    )

    # Buttons the user can click on to impliment the functions
    add_btn.click(add_song, inputs=[add_title, artist, duration, tempo, streams], outputs=output)
    remove_btn.click(remove_song, inputs=remove_title, outputs=output)
    gr.Button("View Playlist").click(view_playlist, outputs=playlist)

demo.launch()