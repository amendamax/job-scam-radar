from ddgs import DDGS
results = DDGS().text("Oblivion Island Haruka and the Magic Mirror ita torrent", max_results=10)
for r in results:
    print(r['title'], "-", r['href'])
