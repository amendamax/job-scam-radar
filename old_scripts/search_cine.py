from ddgs import DDGS
results = DDGS().text('site:cinemagia.ro "Insula amintirilor"', max_results=5)
open('res.txt', 'w', encoding='utf-8').write('\n'.join(r['title'] + ' - ' + r['href'] for r in results))
