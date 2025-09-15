# ogg2mp3
Ogg格式转换成MP3格式

# OGG to MP3 Converter (ogg2mp3)

A simple command-line tool written in Python to convert **OGG audio files** into **MP3** format using `ffmpeg`.

## Features
- 🎵 Convert single `.ogg` files or entire directories  
- 📂 Preserve folder structure when batch converting  
- ⚡ Support both **VBR (Variable Bitrate)** and **CBR (Constant Bitrate)**  
- 🔄 Option to overwrite existing files  
- 🛠 Powered by `ffmpeg` and `libmp3lame`

## Requirements
- Python 3.7+  
- [ffmpeg](https://ffmpeg.org/) installed and available in your PATH  

Check with:
```bash
ffmpeg -version
```

Installation

Clone the repository and make the script executable:
```
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
chmod +x ogg2mp3.py
(Or just run with python3 ogg2mp3.py)
```

Usage
Convert a single file:
```
python3 ogg2mp3.py input.ogg
```

Convert a single file with VBR quality level 2 (recommended):
```
python3 ogg2mp3.py input.ogg --vbr 2
```
Convert with CBR 192 kbps:
```
python3 ogg2mp3.py input.ogg --bitrate 192k
```
Batch convert a whole directory, saving results in another folder:
```
python3 ogg2mp3.py ./music --output ./mp3_output --vbr 2
```
Overwrite existing files:
```
python3 ogg2mp3.py ./music --overwrite
```

Example

Input:
```
music/
 ├── track1.ogg
 ├── track2.oga
 └── album/
      └── track3.ogg

Run:
python3 ogg2mp3.py music --output mp3 --vbr 2

Output:
mp3/
 ├── track1.mp3
 ├── track2.mp3
 └── album/
      └── track3.mp3

```
