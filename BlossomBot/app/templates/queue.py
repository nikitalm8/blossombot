from app.utils.client import Song

from pytube import YouTube


def queue(nowplaying: Song, songs: list, lang: int) -> str:

    if not (songs or nowplaying):

        return noqueue[lang]

    output = (
        (now_song[lang] % (nowplaying.title, nowplaying.duration) if nowplaying else '')
        + (
            queue_template[lang] % (
                '\n'.join([
                    f'{id}. {song.title} ({song.duration})'
                    for id, song in enumerate(songs, 1)
                ])
            )
            if songs else ''
        )
    )

    return output


def add(song: YouTube, lang: int) -> str:

    return add_queue[lang] % song.title


def remove(song: Song, lang: int) -> str:

    return del_queue[lang] % song.title


def skip(song: Song, lang: int) -> str:

    return skipped_song[lang] % song.title


def looped(lang: int, mode: int) -> str:

    return looped_queue[lang][mode]


looped_queue = [
    [
        'Looped the entire queue',
        'Looped the current song',
        'Stopped looping',
    ],
    [
        'Повторяю всю очередь',
        'Повторяю текущую песню',
        'Остановил повтор',
    ]
]

choose = [
    'Choose out of the options',
    'Выберите из вариантов',
]

noqueue = [
    'There is no queue',
    'Очередь пуста',
]

now_song = [
    'Now playing: ``%s (%s)``',
    'Сейчас играет: ``%s (%s)``',
]

queue_template = [
    'Queue: ```\n%s\n```',
    'Очередь: ```\n%s\n```',
]

add_queue = [
    'Added to queue: ``%s``',
    'Добавлено в очередь: ``%s``',
]

del_queue = [
    'Removed from queue: ``%s``',
    'Удалено из очереди: ``%s``',
]

skipped_song = [
    'Skipped: ``%s``',
    'Пропущено: ``%s``',
]

notfound = [
    'Song not found',
    'Песня не найдена',
]

clear = [
    'Queue cleared',
    'Очередь очищена',
]

shuffle = [
    'Queue shuffled',
    'Очередь перемешана',
]
