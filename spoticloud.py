import lyricsgenius
import nltk

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from wordcloud import WordCloud

import enchant
import multiprocessing
import string

from config import geniusToken, client_secret, client_id


# For the first use you need to download this:
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('words')

d = enchant.Dict("en")
analyzer = SentimentIntensityAnalyzer()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                               redirect_uri='http://127.0.0.1:9090',
                                               scope="user-library-read, user-top-read"))

genius = lyricsgenius.Genius(geniusToken, verbose=False, remove_section_headers=True, skip_non_songs=True,
                             excluded_terms=["(Remix)", "(Live)"])


def get_playlist(playlist):
    playlist.replace('https://open.spotify.com/playlist/', '')
    playlist = playlist.split("?")[0]
    return playlist


def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    stopwordremoval = " ".join([i for i in text.lower().split() if i not in stop_words])
    punctuationremoval = ''.join(ch for ch in stopwordremoval if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punctuationremoval.split())

    return normalized


def get_lyrics(track, shared_dict, lock):
    track_key = f"{track['artists'][0]['name']} - {track['name']}"
    if track_key in shared_dict:
        lyrics = shared_dict[track_key]
    else:
        lyrics = ""
        try:
            lyrics = genius.search_song(track['name'], track['artists'][0]['name']).lyrics.replace("Lyrics", '') \
                .replace("3Embed", "") \
                .replace("Embed", "") \
                .replace(track['name'], '', 1)
            with lock:
                shared_dict[track_key] = preprocess_text(lyrics)
        except AttributeError:
            pass


def get_words(playlist):
    results = sp.playlist_items(get_playlist(playlist), fields='items', limit=50)['items']

    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    lock = multiprocessing.Lock()

    processes = []
    for idx, track in enumerate(results, start=1):
        process = multiprocessing.Process(target=get_lyrics, args=(track['track'], shared_dict, lock))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return shared_dict


def get_analysis(playlist):
    all_words = get_words(playlist).items()
    analysis = []

    for title, words in all_words:
        vs = analyzer.polarity_scores(words)
        analysis.append({'title': title, 'sentiment': vs})

    return analysis


def show_info(playlist):
    negative_sum = sum(a['sentiment']['neg'] for a in get_analysis(playlist))
    positive_sum = sum(a['sentiment']['pos'] for a in get_analysis(playlist))

    return 'Music is mostly negative!' if negative_sum > positive_sum else 'Music is mostly positive!'


def get_wordcloud(playlist):
    import time
    start_time = time.time()

    stopwords_wc = ('im', 'ill', 'll', 'i m', 'it s', 'ive got', 'm')
    wc = WordCloud(background_color="white", colormap="Dark2",
                   max_font_size=100, min_font_size=10, stopwords=stopwords_wc,
                   width=1024, height=480, min_word_length=4)

    words = list(get_words(playlist).values())
    words_to_string = ' '.join(word for word in words)

    english_words = [word for word in words_to_string.split() if d.check(word)]
    text = ' '.join(english_words)

    wc = wc.generate(text)
    pl = get_playlist(playlist).replace("https://open.spotify.com/playlist/", "")

    wc.to_file(f'static/img/wc-{pl}.jpg')

    print("--- %s seconds ---" % (time.time() - start_time))

    return f'static/img/wc-{pl}.jpg'
