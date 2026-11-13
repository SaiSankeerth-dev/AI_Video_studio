from PIL import Image
import glob
import os

frames = glob.glob(r"E:\AI_Videos\Youtube\youtube_project\reference\reference_frames\*.jpg")
print(f"Total reference frames: {len(frames)}")
for f in sorted(frames):
    im = Image.open(f)
    print(f"{os.path.basename(f)}: size={im.size}, mode={im.mode}")
