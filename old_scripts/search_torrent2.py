from ddgs import DDGS
results = DDGS().text("L'isola degli smemorati torrent", max_results=10)
for r in results:
    print(r['title'], "-", r['href'])
