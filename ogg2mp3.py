#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

def convert_file(src: Path, dst: Path, bitrate: str=None, vbr: int=None, overwrite: bool=False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not overwrite:
        print(f"Skip (exists): {dst}")
        return

    # 基本 ffmpeg 命令：输入 src，输出 dst，拷贝元数据
    cmd = ["ffmpeg", "-y" if overwrite else "-n", "-i", str(src), "-map_metadata", "0"]

    # 选择编码参数：VBR 优先，没给就用 CBR 比特率
    if vbr is not None:
        # LAME VBR 质量等级 0(最好)-9(最差)。常用 2 或 3
        cmd += ["-q:a", str(vbr)]
    elif bitrate:
        # CBR 比特率，如 192k / 256k / 320k
        cmd += ["-b:a", bitrate]
    else:
        # 默认：中等质量
        cmd += ["-q:a", "2"]

    # 强制 mp3 编码器
    cmd += ["-codec:a", "libmp3lame", str(dst)]

    print(f"Converting: {src} -> {dst}")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to convert {src}:\n{e.stdout.decode('utf-8', errors='ignore')}", file=sys.stderr)

def is_ogg(p: Path):
    return p.suffix.lower() in {".ogg", ".oga", ".ogv"}  # .ogv 也常是 Ogg 容器

def main():
    ap = argparse.ArgumentParser(description="Convert OGG to MP3 (single file or whole directory).")
    ap.add_argument("input", type=Path, help="OGG file or a directory containing OGG files")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Output file or directory")
    ap.add_argument("--bitrate", help="CBR bitrate for MP3, e.g. 192k / 256k / 320k")
    ap.add_argument("--vbr", type=int, help="VBR quality 0(best)-9(worst). Example: --vbr 2")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing output files")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"[ERROR] Input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 参数合法性
    if args.vbr is not None and not (0 <= args.vbr <= 9):
        print("[ERROR] --vbr must be between 0 (best) and 9 (worst).", file=sys.stderr)
        sys.exit(1)

    if args.input.is_file():
        if not is_ogg(args.input):
            print(f"[ERROR] Not an OGG file: {args.input}", file=sys.stderr)
            sys.exit(1)
        # 输出路径
        if args.output:
            out_path = args.output
            if out_path.is_dir():
                out_path = out_path / (args.input.stem + ".mp3")
        else:
            out_path = args.input.with_suffix(".mp3")

        convert_file(args.input, out_path, args.bitrate, args.vbr, args.overwrite)

    else:
        # 目录批量转换
        in_dir = args.input
        out_dir = args.output if args.output else in_dir
        if args.output and args.output.is_file():
            print("[ERROR] Output must be a directory when input is a directory.", file=sys.stderr)
            sys.exit(1)

        ogg_files = [p for p in in_dir.rglob("*") if p.is_file() and is_ogg(p)]
        if not ogg_files:
            print("No OGG files found.")
            return

        for src in ogg_files:
            rel = src.relative_to(in_dir)
            dst = (out_dir / rel).with_suffix(".mp3")
            convert_file(src, dst, args.bitrate, args.vbr, args.overwrite)

if __name__ == "__main__":
    main()
