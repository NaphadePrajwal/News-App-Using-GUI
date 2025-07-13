import requests
from tkinter import *
from urllib.request import urlopen
import io
import webbrowser
from PIL import ImageTk, Image

class NewsApp:
    def __init__(self):
        # Fetch data
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=0eb43ffd471b4895aba60358ecee1b3e').json()

        # Initial GUI load
        self.load_gui()

        # Load the 1st news item
        self.load_news_items(0)

        # Start the main loop
        self.root.mainloop()

    def load_gui(self):
        self.root = Tk()
        self.root.title('News App')
        self.root.geometry('350x600')
        self.root.resizable(0, 0)
        self.root.configure(background='black')

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_items(self, index):
        # Clear the screen for the new news item
        self.clear()

        # Load image
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://dm0qx8t0i9gc9.cloudfront.net/thumbnails/video/ETDyAQoFeik74vjsi/videoblocks-error-glitch-text-animation-and-loading-bar-rendering-background-with-alpha-channel-loop-4k_boz5ejt_nv_thumbnail-1080_01.png'
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)

        label = Label(self.root, image=photo)
        label.image = photo  # Keep a reference
        label.pack()

        heading = Label(self.root, text=self.data['articles'][index]['title'], bg='black', fg='white', wraplength=350, justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('verdana', 15))

        details = Label(self.root, text=self.data['articles'][index]['description'], bg='black', fg='white', wraplength=350, justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))

        frame = Frame(self.root, bg='black')
        frame.pack(expand=True, fill=BOTH)

        if index != 0:
            prev = Button(frame, text='Prev', width=16, height=3, command=lambda: self.load_news_items(index - 1))
            prev.pack(side=LEFT)

        read = Button(frame, text='Read More', width=16, height=3, command=lambda: self.open_link(self.data['articles'][index]['url']))
        read.pack(side=LEFT)

        if index != len(self.data['articles']) - 1:
            next = Button(frame, text='Next', width=16, height=3, command=lambda: self.load_news_items(index + 1))
            next.pack(side=LEFT)

    def open_link(self, url):
        webbrowser.open(url)

# Create the application object
obj = NewsApp()
