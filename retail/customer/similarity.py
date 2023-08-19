import gensim.downloader
import sys

# print(list(gensim.downloader.info()['models'].keys())) # to see the list of available models
product = sys.argv[1]
user_current_data = str(product)

# purpose is more demonstrate the idea and application needs more carefull analysis on the items
pretrained_model = 'word2vec-google-news-300'
vectors = gensim.downloader.load(pretrained_model)

results = vectors.most_similar(positive=user_current_data, topn=10)

# print the results
for res in results:
    print(res)



