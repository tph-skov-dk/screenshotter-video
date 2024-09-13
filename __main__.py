#!/usr/bin/env python3
import time
import argparse
import sys
import signal
import subprocess
import os

frames_written = 0
start = time.time()
tmp_dir = f"tmp-{int(start)}"

def take_screenshot(cmd):
    try:
        os.mkdir(tmp_dir)
    except:
        pass
    subprocess.run(cmd, cwd=tmp_dir)
    global frames_written
    frames_written += 1
    print("took screenshot")

def combine(fps, out):
    subprocess.run(["ffmpeg", "-f", "image2", "-r", f"{int(fps)}", "-pattern_type", "glob", "-i", f"{tmp_dir}/*", "-vcodec", "mpeg4", out])

def signal_handler(out):
    elapsed = time.time() - start
    fps = frames_written / elapsed
    print(f"wrote {frames_written} frame(s) over {elapsed:0.4f} seconds for a total {fps:0.4f} frames/sec")
    print(f"output available in {tmp_dir}")
    print(f"attempting to combine into {out}")
    combine(fps, out)
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser("screenshotter-video")
    parser.add_argument("-c", "--cmd", help="Command to execute to take screenshot", required=True)
    parser.add_argument("-o", "--out", help=f"Output video file. Default: '{tmp_dir}.mp4'", default=f"{tmp_dir}.mp4")
    args = parser.parse_args()
    cmd = args.cmd.split()
    out = args.out.split()
    signal.signal(signal.SIGINT, lambda: signal_handler(out))
    while True:
        take_screenshot(cmd)

if __name__ == "__main__":
    main()
