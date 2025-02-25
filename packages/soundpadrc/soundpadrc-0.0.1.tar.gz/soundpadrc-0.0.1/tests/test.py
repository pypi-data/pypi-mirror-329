import sys

sys.path.insert(0, "..")
from src.soundpadrc import Soundpad

sp = Soundpad()

print(sp.categories())

print(sp.query_sounds("hobbit"))

print(sp.get_all_sounds())
