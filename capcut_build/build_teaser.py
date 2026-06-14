#!/usr/bin/env python3
"""Render a FIFA World Cup 2026 hype teaser (typography style) to MP4 with ffmpeg.
Usage: python3 build_teaser.py seg   # render segments
       python3 build_teaser.py final # xfade + audio + encode
"""
import os, subprocess, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
SEGDIR = os.path.join(HERE, "segments"); os.makedirs(SEGDIR, exist_ok=True)
OUT = os.path.join(HERE, "..", "FIFA_World_Cup_2026_Hype.mp4")
T = 0.45

SEGS = [
    ("FIFA WORLD CUP", "2026",                          3.2, "0x111418","0x05303A", 0,0,1080,1920, 0.010, "0xE8C547"),
    ("THREE NATIONS",  "ONE CUP",                        3.0, "0x0B6E4F","0x041410", 200,0,900,1920, 0.012, "0xE8C547"),
    ("48 TEAMS",       "104 MATCHES",                    3.0, "0xB11226","0x2A0408", 0,300,1080,1700, 0.012, "0xFFFFFF"),
    ("USA - CANADA - MEXICO","FIRST EVER 3-HOST CUP",    3.4, "0x0B3D91","0x04122B", 900,0,200,1920, 0.011, "0xE8C547"),
    ("16 HOST CITIES", "MEXICO CITY  TO  NEW YORK",      3.0, "0x4A1B6D","0x140720", 0,0,1080,1920, 0.013, "0xE8C547"),
    ("THE BIGGEST",    "WORLD CUP EVER",                 2.8, "0xC8551B","0x2A1004", 0,1920,1080,0, 0.012, "0xFFFFFF"),
    ("JUNE 11 - JULY 19","2026",                         3.0, "0x0E7C7B","0x041F1F", 200,1920,900,0, 0.011, "0xE8C547"),
    ("ARE YOU READY?", "",                               2.6, "0x8B0000","0x140000", 0,0,1080,1920, 0.016, "0xFFFFFF"),
    ("WORLD CUP 2026", "USA - CANADA - MEXICO",          4.0, "0xC8A24B","0x1A1205", 0,0,1080,1920, 0.010, "0xFFFFFF"),
]

def esc(t):
    return t.replace("\\","\\\\").replace(":","\\:").replace("'","\\'")

def render_segments():
    for i, s in enumerate(SEGS):
        main, sub, dur, c0, c1, x0,y0,x1,y1, speed, accent = s
        out = os.path.join(SEGDIR, f"seg_{i:02d}.mp4")
        vf = [
            f"drawbox=x=(w-360)/2:y=h/2-150:w='min(360,720*t)':h=8:color={accent}@1:t=fill",
            (f"drawtext=fontfile={FONT}:text='{esc(main)}':fontcolor=white:fontsize=100:"
             f"x=(w-text_w)/2:y=(h-text_h)/2-40-6*t:alpha='if(lt(t\\,0.45)\\,t/0.45\\,1)'"),
        ]
        if sub:
            vf.append(f"drawtext=fontfile={FONT}:text='{esc(sub)}':fontcolor={accent}:fontsize=56:"
                      f"x=(w-text_w)/2:y=(h-text_h)/2+90:alpha='if(lt(t\\,0.8)\\,max(0\\,(t-0.35)/0.45)\\,1)'")
        vf += [f"fade=t=in:st=0:d=0.3", f"fade=t=out:st={dur-0.3:.2f}:d=0.3", "format=yuv420p"]
        src = (f"gradients=s=1080x1920:r=30:c0={c0}:c1={c1}:x0={x0}:y0={y0}:x1={x1}:y1={y1}:"
               f"speed={speed}:d={dur}")
        subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","lavfi","-i",src,
                        "-vf",",".join(vf),"-t",str(dur),"-r","30","-pix_fmt","yuv420p",
                        "-c:v","libx264","-preset","ultrafast","-crf","20",out], check=True)
        print("seg", i, "ok")

def encode_final():
    inputs = []
    durs = []
    for i, s in enumerate(SEGS):
        inputs += ["-i", os.path.join(SEGDIR, f"seg_{i:02d}.mp4")]
        durs.append(s[2])
    fc = []; running = durs[0]; prev = "0:v"
    for i in range(1, len(SEGS)):
        off = running - T; lbl = f"v{i}"
        fc.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={T}:offset={off:.3f}[{lbl}]")
        prev = lbl; running += durs[i] - T
    total = running; vlast = prev
    abed = (f"sine=frequency=55:duration={total:.2f}[s1];"
            f"sine=frequency=110:duration={total:.2f}[s2];"
            f"sine=frequency=220:duration={total:.2f}[s3];"
            f"[s1]volume=0.16[a1];[s2]volume=0.07[a2];[s3]volume=0.03[a3];"
            f"[a1][a2][a3]amix=inputs=3:normalize=0,"
            f"afade=t=in:st=0:d=1.2,afade=t=out:st={total-1.2:.2f}:d=1.2,"
            f"volume='1+0.6*sin(2*PI*t/{total:.2f})':eval=frame,alimiter=limit=0.9[abed]")
    cmd = ["ffmpeg","-y","-hide_banner","-loglevel","error", *inputs,
           "-filter_complex", ";".join(fc) + ";" + abed,
           "-map", f"[{vlast}]", "-map","[abed]",
           "-r","30","-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p",
           "-profile:v","high","-crf","20","-c:a","aac","-b:a","192k","-shortest", OUT]
    subprocess.run(cmd, check=True)
    print(f"DONE total={total:.2f}s -> {os.path.abspath(OUT)}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("seg","all"): render_segments()
    if mode in ("final","all"): encode_final()
