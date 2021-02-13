from gauss._utils import load_obj, save_obj
from gauss.brain.memes import Meme

members = load_obj("gauss/_obj/members.pkl")

for member in members.keys():
    members[member]["recent_memes"] = [Meme("", "0")] * 30

print(members)
save_obj(members, "gauss/_obj/members.pkl")



