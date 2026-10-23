"""Sujood v5 with a new opening (owner, 23 Oct 2026: hook idea 3, "one flash, one hit"), at 1.25x and 5% closer. The red flicker
(0-2.6 s) goes: his talking shot from subhana.mp4 instead, graded and pushed exactly as the master (template grade.txt, the first
section's slow push), "AT YOUR" behind his head from frame 0 and "LOWEST" slamming down on the word with one white flash and one
deep boom (the owner's n03). His voice is the recording as it is (owner: don't raise the volume); from 2.75 s the master as it was.
  python3 hook3.py WORK      (WORK has subhana.mp4 and the master sujood-v5.mp4) → WORK/sujood-v6.mp4"""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
W = os.path.abspath(sys.argv[1]); FPS = 30; END = 2.6; JOIN = 2.75   # the flicker's end; the sound switches just before the title's tap at 2.8
HIT = 1.86                                                         # "lowest" (wordtimes.json)
sh = lambda *a: subprocess.run(list(a), check=True)
G = open(os.path.join(REPO, "brag-quiz/reels/template/grade.txt")).read().strip(); Z = "1+0.055*(t/7.660)"   # the master's first section
sh("ffmpeg", "-v", "error", "-y", "-t", f"{END}", "-i", f"{W}/subhana.mp4", "-vf", f"{G},scale=1404:2496:flags=lanczos,fps=30,format=yuv420p,"
   f"scale=w='trunc(1080*({Z})/2)*2':h='trunc(1920*({Z})/2)*2':eval=frame:flags=lanczos,crop=1080:1920:'(iw-1080)*0.5':'(ih-1920)*0.35',setsar=1,format=yuv420p",
   "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast", f"{W}/seg.mov")
N = round(END * FPS)
for d in ("frames", "mask", "back", "front", "fonts"): os.makedirs(f"{W}/{d}", exist_ok=True)
sh("ffmpeg", "-v", "error", "-y", "-i", f"{W}/seg.mov", "-vf", "scale=540:960", "-q:v", "3", f"{W}/frames/%05d.jpg")
from rembg import remove, new_session                              # him, cut out, so the title sits behind his head
from PIL import Image
s = new_session("u2net_human_seg")
for i in range(N):
    remove(Image.open(f"{W}/frames/{i + 1:05d}.jpg"), session=s, only_mask=True).resize((1080, 1920), Image.BILINEAR).save(f"{W}/mask/{i:05d}.png")
shutil.copy(os.path.join(REPO, "brag-quiz/fonts/anton-latin-400-normal.woff2"), f"{W}/fonts/")
shutil.copy(os.path.join(HERE, "hook3.html"), f"{W}/hook3.html")
C = dict(hit=HIT, end=END + .3, caps=[[0.0, 1.38, [["When", 0.0, False], ["your", 0.24, False], ["head", 0.5, False], ["is", 0.88, False]]],
                                      [1.38, END + .3, [["at", 1.38, False], ["its", 1.64, False], ["lowest", HIT, True]]]])
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"); p = b.new_page(viewport={"width": 1080, "height": 1920})
    p.goto(f"file://{W}/hook3.html"); p.evaluate(f"C = {json.dumps(C)}"); p.evaluate("document.fonts.ready.then(() => true)"); p.wait_for_timeout(400)
    for i in range(N):
        for L in ("back", "front"): p.evaluate(f"update({i / FPS}, '{L}')"); p.screenshot(path=f"{W}/{L}/{i:05d}.png", omit_background=True)
    b.close()
# the opening's picture: scene + title, him on top (mask), captions and the flash in front
sh("ffmpeg", "-v", "error", "-y", "-i", f"{W}/seg.mov", "-framerate", "30", "-i", f"{W}/back/%05d.png", "-framerate", "30", "-i", f"{W}/mask/%05d.png",
   "-framerate", "30", "-i", f"{W}/front/%05d.png", "-filter_complex",
   "[0:v]split=2[v0][v1];[v0][1:v]overlay=0:0:format=auto[bb];[2:v]format=gray[m];[v1][m]alphamerge[fg];[bb][fg]overlay=0:0:format=auto[sc];"
   "[sc][3:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]", "-c:v", "libx264", "-crf", "14", "-preset", "fast", f"{W}/open.mov")
# the sound: his voice as recorded up to JOIN, one boom on the word, then the master's (no gain anywhere)
boom = os.path.join(REPO, "brag-quiz/sfx/owner/n03.wav"); M = f"{W}/sujood-v5.mp4"
sh("ffmpeg", "-v", "error", "-y", "-i", M, "-i", f"{W}/open.mov", "-i", f"{W}/subhana.mp4", "-i", boom, "-filter_complex",
   f"[1:v]fps=30[o];[0:v]trim=start={END},setpts=PTS-STARTPTS,fps=30[r];[o][r]concat=n=2:v=1:a=0[v];"
   f"[2:a]atrim=0:{JOIN},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st={JOIN - .03}:d=0.03[va];"
   f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.35,adelay={int(HIT * 1000)}|{int(HIT * 1000)},apad[bm];"
   f"[va][bm]amix=inputs=2:normalize=0:duration=first[op];"
   f"[0:a]atrim=start={JOIN},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.03[ra];[op][ra]concat=n=2:v=0:a=1[a]",
   "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "pcm_s16le", f"{W}/v6-1x.mov")
# 1.25x (his pitch kept) and 5% closer, as the owner asked
sh("ffmpeg", "-v", "error", "-y", "-i", f"{W}/v6-1x.mov", "-filter_complex",
   "[0:v]setpts=PTS/1.25,fps=30,scale=1134:2016:flags=lanczos,crop=1080:1920:27:48,format=yuv420p[v];[0:a]atempo=1.25[a]",
   "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{W}/sujood-v6.mp4")
print("ok")
