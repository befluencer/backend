import random

# Sample words related to Bible locations and themes
places = [
    "Bethel", "Gibeon", "Zion", "Salem", "Hebron", "Shiloh", "Jericho", "Nazareth", "Canaan", "Eden",
    "Sinai", "Ararat", "Babylon", "Zarephath", "Shechem", "Joppa", "Golgotha", "Emmaus", "Antioch", "Damascus",
    "Galilee", "Samaria", "Patmos", "Tarsus", "Cyrene", "Thyatira", "Smyrna", "Pergamum", "Laodicea", "Philippi"
]

prefixes = [
    "Mount", "River", "Hill", "Valley", "Lake", "Well", "Camp", "Fort", "Tower", "Land", "Bay", "Port"
]

# Generate combinations with two words and total max length 12
def generate_locations(num=3000):
    results = set()
    while len(results) < num:
        word2 = random.choice(prefixes)
        word1 = random.choice(places)
        combined = f"{word1} {word2}"
        if len(combined.replace(" ", "")) <= 12:
            results.add(combined)
    return sorted(results)

bible_locations = generate_locations(1000)

print(bible_locations)