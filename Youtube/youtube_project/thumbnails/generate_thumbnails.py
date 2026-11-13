from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

thumb_dir = r"E:\AI_Videos\Youtube\youtube_project\thumbnails"
os.makedirs(thumb_dir, exist_ok=True)

# THUMBNAIL 1: "THE $3,500,000 SCAM" (Aged Box + Red Warning Stamp + Bold Yellow Typography)
base_img_path = r"E:\AI_Videos\Youtube\youtube_project\assets\images\shot-01.png"
if os.path.exists(base_img_path):
    im = Image.open(base_img_path).convert("RGBA")
else:
    im = Image.new("RGBA", (1920, 1080), (15, 17, 21, 255))

draw = ImageDraw.Draw(im)

# Dark gradient vignette on left side for text readability
for x in range(0, 950):
    alpha = int(220 * (1.0 - x/950))
    draw.line([(x, 0), (x, 1080)], fill=(8, 10, 14, alpha), width=1)

# Giant Bold Yellow Headline
draw.text((100, 120), "THE $3,500,000", fill=(255, 215, 0), font=None)
draw.text((100, 220), "POKEMON SCAM", fill=(255, 255, 255), font=None)

# Red Warning Badge
draw.rectangle([100, 360, 680, 480], fill=(220, 35, 45, 240), outline=(255, 95, 86), width=4)
draw.text((130, 400), "100% COUNTERFEIT", fill=(255, 255, 255), font=None)

# Subtitle callout
draw.rectangle([100, 520, 780, 620], fill=(20, 26, 36, 220), outline=(0, 229, 255), width=3)
draw.text((130, 555), "HOW INTERNET SLEUTHS CAUGHT IT", fill=(0, 229, 255), font=None)

# Golden arrow pointing to box tape
draw.text((1150, 780), "FAKED TAPE SEAM ->", fill=(255, 215, 0), font=None)

im.save(os.path.join(thumb_dir, "thumbnail_concept_01.png"))
im.save(os.path.join(thumb_dir, "thumbnail_master.png"))
print("Generated thumbnail_concept_01.png and thumbnail_master.png")

# THUMBNAIL 2: "G.I. JOE?!" (The Unboxing Shock)
base_img_16 = r"E:\AI_Videos\Youtube\youtube_project\assets\images\shot-16.png"
if os.path.exists(base_img_16):
    im2 = Image.open(base_img_16).convert("RGBA")
else:
    im2 = Image.new("RGBA", (1920, 1080), (15, 17, 21, 255))

draw2 = ImageDraw.Draw(im2)
# Dark bottom overlay
for y in range(650, 1080):
    alpha = int(240 * ((y - 650) / 430))
    draw2.line([(0, y), (1920, y)], fill=(8, 10, 14, alpha), width=1)

# Giant Shock Quote
draw2.rectangle([80, 700, 1840, 980], fill=(16, 20, 28, 230), outline=(255, 45, 60), width=5)
draw2.text((120, 740), "\"G.I. JOE?! IT WAS G.I. JOE?!\"", fill=(255, 95, 86), font=None)
draw2.text((120, 840), "WHAT REALLY HAPPENED TO LOGAN PAUL'S $3.5M CASE", fill=(255, 255, 255), font=None)

im2.save(os.path.join(thumb_dir, "thumbnail_concept_02.png"))
print("Generated thumbnail_concept_02.png")
