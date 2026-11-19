#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow>=11"]
# ///
"""Render original text overlays and an audio-backed local review video.

Uses an existing picture track and an edit-relative English-above-Chinese SRT.
Each cue ends with one Chinese line. Keep source and rendered media local.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FONT_CN = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
FONT_EN = '/System/Library/Fonts/Supplemental/Arial.ttf'


def seconds(s):
    h, m, rest = s.replace(',', '.').split(':')
    return int(h)*3600 + int(m)*60 + float(rest)


def read_srt(path):
    result = []
    for block in re.split(r'\n\s*\n', path.read_text().strip()):
        lines = block.splitlines()
        a, b = lines[1].split(' --> ')
        if len(lines) < 4 or not re.search(r'[\u3400-\u9fff]', lines[-1]):
            raise ValueError(f'Cue {lines[0]} must end with a Chinese translation')
        result.append({'start':seconds(a), 'end':seconds(b),
                       'en':' '.join(lines[2:-1]), 'zh':lines[-1]})
    return result


def wrap(text, font, width, chinese=False):
    parts = list(text) if chinese else text.split()
    lines, current = [], ''
    for part in parts:
        candidate = current + ('' if chinese or not current else ' ') + part
        if font.getlength(candidate) > width and current:
            lines.append(current)
            current = part
        else:
            current = candidate
    return lines + ([current] if current else [])


def caption(path, zh, en):
    # Original typography only: keep 80 px side margins and readable size floors.
    layer = Image.new('RGBA',(W,H),(0,0,0,0))
    draw = ImageDraw.Draw(layer)
    cn = ImageFont.truetype(FONT_CN,31)
    english = ImageFont.truetype(FONT_EN,38)
    zlines = wrap(zh,cn,1120,True)
    elines = wrap(en,english,1120)
    if len(zlines)>2 or len(elines)>2:
        raise ValueError('Rewrite/wrap explicitly instead of shrinking unreadably')
    total = len(elines)*45 + len(zlines)*38 + 8
    top = 680-total
    for y in range(max(460,top-30),H):
        alpha = min(225, int((y-(top-30))*3))
        if alpha > 0:
            draw.line((0,y,W,y),fill=(8,10,13,alpha))
    y=top
    for line in elines:
        draw.text((W/2,y),line,font=english,anchor='mt',fill='#ffffff',
                  stroke_width=2,stroke_fill='#090a0b')
        y+=45
    y+=8
    for line in zlines:
        draw.text((W/2,y),line,font=cn,anchor='mt',fill='#d7dee5',
                  stroke_width=1,stroke_fill='#080a0b')
        y+=38
    layer.save(path)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pictures',type=Path,required=True)
    parser.add_argument('--audio',type=Path,required=True)
    parser.add_argument('--captions',type=Path,required=True)
    parser.add_argument('--audio-start',type=float,required=True,
                        help='Seconds to skip in the input audio; SRT starts on the edit clock')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--name',default='lyric-edit',help='Main MP4 filename without extension')
    args=parser.parse_args()
    if args.output.exists():parser.error('use a new output directory')
    args.output.mkdir(parents=True)
    cues=read_srt(args.captions)
    duration=float(subprocess.check_output(['ffprobe','-v','error',
        '-show_entries','format=duration','-of','csv=p=0',str(args.pictures)]))
    overlays=[]
    preceding_end = 0
    for index,cue in enumerate(cues,1):
        a,b=cue['start'],cue['end']
        if not preceding_end <= a < b <= duration:
            raise ValueError(f'Cue {index} overlaps another cue or falls outside the edit')
        preceding_end = b
        dest=args.output/f'caption-{index:03}.png'
        caption(dest,cue['zh'],cue['en'])
        overlays.append((a,b,dest))
    command=['ffmpeg','-hide_banner','-loglevel','error','-n',
             '-i',str(args.pictures),'-ss',str(args.audio_start),'-i',str(args.audio)]
    for _,_,p in overlays:command+=['-i',str(p)]
    filters=[];prev='0:v'
    for i,(a,b,_) in enumerate(overlays):
        label=f'c{i}'
        filters.append(f'[{prev}][{i+2}:v]overlay=0:0:enable=\'gte(t,{a:.3f})*lt(t,{b:.3f})\'[{label}]')
        prev=label
    filters += [f'[1:a]atrim=duration={duration},asetpts=PTS-STARTPTS,'
                f'afade=t=in:d=0.08,afade=t=out:st={duration-.4}:d=0.4[a]',
                '[a]asplit=2[aud][waveaudio]',
                '[waveaudio]showfreqs=s=1280x24:mode=bar:ascale=sqrt:fscale=log:'
                'colors=0x9baab5:win_size=1024,format=rgba[waves]',
                f'[{prev}][waves]overlay=0:H-24:shortest=1[out]']
    output=args.output/f'{args.name}.mp4'
    subprocess.run(command+['-filter_complex_threads','2','-filter_complex',';'.join(filters),
                    '-map','[out]','-map','[aud]','-t',str(duration),'-r','30',
                    '-c:v','libx264','-preset','veryfast','-crf','21','-threads','4',
                    '-c:a','aac','-b:a','192k','-movflags','+faststart',str(output)],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-i',str(output),
                    '-t','35','-c','copy','-movflags','+faststart',
                    str(args.output/'opening-35s.mp4')],check=True)
    (args.output/'render-receipt.json').write_text(json.dumps({
        'duration_seconds':duration,'audio_trim_seconds':args.audio_start,'cue_count':len(cues),
        'resolution':[W,H],'fps':30,'caption_order':['en','zh'],
        'zh_font_px':31,'en_font_px':38,
        'user_accepted':False},ensure_ascii=False,indent=2)+'\n')
    print(output)


if __name__=='__main__':main()
