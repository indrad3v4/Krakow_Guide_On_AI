import json, random

candidates = [
    ("Wawel Castle", ["castle","royal","UNESCO"], "Wawel Castle is a royal castle and museum in Krakow. It was the seat of Polish kings for centuries."),
    ("Main Market Square", ["square","old town","shops"], "The Main Market Square in Krakow is one of the largest medieval town squares in Europe, bustling with cafes and shops."),
    ("St. Mary's Basilica", ["church","bugle","basilica"], "St. Mary's Basilica is famous for its Hejnal bugle call played every hour from the taller tower."),
    ("Kazimierz District", ["jewish","district","culture"], "Kazimierz is the historic Jewish district of Krakow, known for synagogues, street art, and vibrant nightlife."),
    ("Wieliczka Salt Mine", ["salt","mine","UNESCO"], "The Wieliczka Salt Mine is a UNESCO World Heritage Site near Krakow with chapels carved from salt rock."),
    ("Planty Park", ["park","green","walk"], "Planty is a ring of green space surrounding Krakow's Old Town, perfect for walking and jogging."),
    ("Cloth Hall", ["market","souvenirs","renaissance"], "The Cloth Hall in the center of Main Square offers souvenirs and reflects Krakow's Renaissance trading heritage."),
    ("Wawel Cathedral", ["church","crypt","royal"], "Wawel Cathedral is the coronation church of Polish monarchs, located on Wawel Hill next to the Castle."),
    ("Schindler Factory", ["museum","WWII","factory"], "Oskar Schindler's Enamel Factory is now a museum about Krakow during World War II."),
    ("Rynek Underground", ["museum","medieval","underground"], "Rynek Underground is a modern museum beneath the Main Market Square showing Krakow's medieval trade routes."),
]

descriptors = [
    "historic", "cultural", "scenic", "family-friendly", "nightlife", "artistic", "culinary", "religious",
    "academic", "green", "modern", "bohemian", "royal", "underground", "panoramic", "cozy", "lively",
    "peaceful", "ancient", "trendy"
]

extra = []
for i in range(500):
    base_title, tags, desc = random.choice(candidates)
    variant = f"{base_title} Area {i+1}"
    tags_v = tags + [random.choice(descriptors)]
    desc_v = desc + f" Location {i+1} offers a unique perspective on Krakow's heritage."
    extra.append({"title": variant, "tags": tags_v, "text": desc_v, "source": variant, "uri": f"krakow://{variant.lower().replace(' ','-')}"})

combined = candidates + extra
with open("locations.json","w",encoding="utf-8") as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)
print("Generated", len(combined), "locations")
