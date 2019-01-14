import os
import numpy
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import praw
from PIL import Image
from nltk.corpus import stopwords

text = ''
subreddit = os.environ.get('SUB') or 'memes'
def get_reddit_content(text):
    # https://praw.readthedocs.io/en/latest/getting_started/authentication.html#oauth
    reddit = praw.Reddit(client_id='blah',
                         client_secret='blah',
                         user_agent='testscript for wordcloud by /u/prateekkish')

    
    print('Wordcloud for {subreddit}'.format(subreddit=subreddit))

    for a,submission in enumerate(reddit.subreddit(subreddit).hot(limit=100)):
        print(a)
        # collecting words from title and comments on the post
        text += submission.title
        for comment in submission.comments:
            try:
                text += comment.body
            except AttributeError:
                pass
    return text

mask = numpy.array(Image.open("india-source.png"))
text = get_reddit_content(text)

file = open("{filename}".format(filename=subreddit),"w+")
file.write(text)
file.close()
stopwords = set(STOPWORDS).union(set(stopwords.words()))
background_color = os.environ.get("BG_COLOR") or 'white'
max_words = os.environ.get("MAX_WORDS") or 200
canvas_width = os.environ.get("CANVAS_WIDTH") or 400

wordcloud = WordCloud(width=int(canvas_width),stopwords=stopwords,background_color= background_color,max_words= int(max_words),mask= mask).generate(str(text))

plt.figure(figsize=(20,10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("{filename}.jpg".format(filename=subreddit), quality=99)
plt.show()


