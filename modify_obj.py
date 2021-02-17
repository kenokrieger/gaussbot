from gauss._utils import load_obj, save_obj
from gauss.brain.memes import Meme
from datetime import datetime

today = datetime.now().date()

memes = load_obj("gauss/_obj/memes.pkl")

for tag in memes.keys():
    for meme in memes[tag]:
        old_rating = meme.rating
        if 2021 in old_rating:
            rating = 0
            total_ratings = 0
            for wk in old_rating[2021].keys():
                rating += old_rating[2021][wk][0]
                total_ratings += old_rating[2021][wk][1]
            meme.rating = {2021: {2: [rating, total_ratings]}}
print(memes)
print(memes["physics"][0].rating)



save_obj(memes, "gauss/_obj/memes.pkl")




