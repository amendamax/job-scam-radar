import os

base_dir = r"C:\Users\bratu\Documents\antigravity\amazing-borg\job-scam-radar"

style_css = os.path.join(base_dir, "style.css")
with open(style_css, "r", encoding="utf-8") as f:
    css = f.read()

# Replace dating background
css = css.replace("dating_bg.webp", "dev_bg.webp")

# Replace pink colors with orange
css = css.replace("#ec4899", "#f59e0b")
css = css.replace("#db2777", "#d97706")
css = css.replace("#be185d", "#b45309")
css = css.replace("#f472b6", "#fbbf24")
css = css.replace("#f9a8d4", "#fcd34d")
css = css.replace("rgba(236, 72, 153", "rgba(245, 158, 11")
css = css.replace("rgba(219, 39, 119", "rgba(217, 119, 6")
css = css.replace("rgba(190, 24, 93", "rgba(180, 83, 9")
css = css.replace("rgba(236,72,153", "rgba(245,158,11")

with open(style_css, "w", encoding="utf-8") as f:
    f.write(css)

print("style.css colors fixed.")
