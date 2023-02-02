import lyricsgenius
import nltk

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import string
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from wordcloud import WordCloud
import matplotlib.pyplot as plt

#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('words')

geniusToken = 'MUtakF0ShKREXrR5MSC1_vrsCpWwcx0MBh5k9GINn2WT2tYqqsQ9kfJy5C8Lr2Gv'
genius = lyricsgenius.Genius(geniusToken, verbose=False, remove_section_headers=True, skip_non_songs=True,
                             excluded_terms=["(Remix)", "(Live)"])
# spotify auth:
client_id = "d57ce86eacaf4f4282d1da003edc2275"
client_secret = "1e8652aa32dc4c4a94bab6613bf8f085"

analyzer = SentimentIntensityAnalyzer()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                               redirect_uri='http://127.0.0.1:9090',
                                               scope="user-library-read, user-top-read"))

# results = sp.current_user_top_tracks()['items']


def get_words():
    words_all = {}

    for idx, track in enumerate(results, start=1):
        try:
            track = track['track']
            lyrics = genius.search_song(track['name'], track['artists'][0]['name']).lyrics.replace("Lyrics", '') \
                .replace("3Embed", "") \
                .replace("Embed", "") \
                .replace(track['name'], '', 1)

            stop_words = set(stopwords.words('english'))
            exclude = set(string.punctuation)
            lemma = WordNetLemmatizer()

            stopwordremoval = " ".join([i for i in lyrics.lower().split() if i not in stop_words])
            punctuationremoval = ''.join(ch for ch in stopwordremoval if ch not in exclude)
            normalized = " ".join(lemma.lemmatize(word) for word in punctuationremoval.split())
            words_all[f"{idx}) {track['artists'][0]['name']} - {track['name']}"] = normalized

        except AttributeError:
            pass

    return words_all


def get_analysis():
    all_words = get_words().items()
    analysis = {}

    for title, words in all_words:
        vs = analyzer.polarity_scores(words)
        analysis[title] = vs

    return analysis


def show_info():
    negative = []
    neutral = []
    positive = []
    compound = []

    for i in get_analysis().values():
        negative.append(i['neg'])
        neutral.append(i['neu'])
        positive.append(i['pos'])
        compound.append(i['compound'])

    if sum(negative) > sum(positive):
        return 'Music is mostly negative!'
    else:
        return 'Music is mostly positive!'


def get_wordcloud():
    stopwords_wc = ('im', 'ill', 'll', 'i m', 'it s', 'ive got', 'm', 'verdurin', 'albertine')

    wc = WordCloud(background_color="white", colormap="Dark2",
                   max_font_size=100, min_font_size=10, stopwords=stopwords_wc,
                   width=1024, height=480, min_word_length=4)

    every_word = [i for i in get_words().values()]
    listToStr = ' '.join(map(str, every_word))

    wc_img = wc.generate(listToStr)

    plt.imshow(wc_img, interpolation='bilinear')
    plt.axis("off")
    plt.title(show_info())
    plt.show()


playlist = 'https://open.spotify.com/playlist/37i9dQZF1F0sijgNaJdgit'
playlist.replace('https://open.spotify.com/playlist/', '')
results = sp.playlist_items(playlist, fields='items', limit=50)['items']

print(get_wordcloud())




