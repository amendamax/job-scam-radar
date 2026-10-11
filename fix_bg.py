with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace(
    ".hero { padding: 60px 20px; text-align: center; background: linear-gradient(to bottom, rgba(15,23,42,0.8), rgba(2,6,23,1)), url('/dev_bg.webp') center/cover; }",
    ".hero { padding: 100px 20px; min-height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: linear-gradient(to bottom, rgba(15,23,42,0.85), rgba(2,6,23,1)), url('/dev_bg.webp') center top / cover no-repeat; }"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('server.py', 'r', encoding='utf-8') as f:
    server_code = f.read()

server_code = server_code.replace(
    ".hero { padding: 60px 20px; text-align: center; background: linear-gradient(to bottom, rgba(15,23,42,0.8), rgba(2,6,23,1)), url('/dev_bg.webp') center/cover; }",
    ".hero { padding: 100px 20px; min-height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: linear-gradient(to bottom, rgba(15,23,42,0.85), rgba(2,6,23,1)), url('/dev_bg.webp') center top / cover no-repeat; }"
)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(server_code)
