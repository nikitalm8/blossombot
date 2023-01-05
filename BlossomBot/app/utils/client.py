from random import shuffle
from pytube import YouTube


class Song:

    def __init__(self, title: str, url: str, duration: int) -> None:

        self.title = title
        self.url = url
        self.duration = duration


class VoiceClient:

    queue = []
    nowplaying = None
    loop = False
    singleloop = False
    afkcount = 0
    suppress = True
    message_id = 0

    def __init__(self, channel, **kwargs) -> None:

        self.channel = channel

        for key, value in kwargs.items():

            setattr(self, key, value)


    def add(self, song: YouTube):

        self.queue.append(
            Song(song.title, song.watch_url, song.length)
        )


    def addfirst(self, song: YouTube):

        self.queue.insert(
            0,
            Song(song.title, song.watch_url, song.length)
        )


    def remove(self, index: int):

        self.queue.pop(index - 1)


    def clear(self):

        self.queue.clear()


    def shuffle(self):

        if self.singleloop:

            temp = self.queue[1:]
            shuffle(temp)
            self.queue = [
                self.queue[0],
                *temp,
            ]

        else:

            queue = self.queue
            shuffle(queue)
            self.queue = queue


    def next(self) -> Song | bool:

        if self.singleloop:

            next_song = self.nowplaying

        elif self.loop:

            self.queue.append(self.nowplaying)
            next_song = self.queue.pop(0)

        elif self.queue:

            next_song = self.queue.pop(0)

        else:

            return False

        self.nowplaying = next_song
        return next_song


    def checkafk(self):

        if self.afkcount > 12:

            return True

        print(self.afkcount)

        self.afkcount += 1
        return False
