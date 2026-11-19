#!/usr/bin/env python3
"""Render a local photo shot list to silent clips and a review sequence.

Media stays outside version control. Requires ffmpeg on PATH; no cloud calls.
Shot boundaries are rounded once to the 30 fps grid. This does not validate
music synchronization, visual comedy or media reuse rights.
"""
import argparse
import concurrent.futures
import json
import shutil
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shots', required=True, type=Path)
    parser.add_argument('--assets', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--community-badge', type=Path)
    args = parser.parse_args()
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        parser.error('ffmpeg is required')
    shots = json.loads(args.shots.read_text())['shots']
    root = args.assets.resolve()
    end_frame = 0
    for shot in shots:
        start = round(shot['start_seconds'] * 30)
        end = round(shot['end_seconds'] * 30)
        source = (root / shot['asset_file']).resolve()
        if start != end_frame or end <= start:
            parser.error('shot list must be continuous and have positive frame durations')
        if not source.is_relative_to(root) or not source.is_file():
            parser.error('asset is missing or outside the asset directory')
        end_frame = end
    if args.output.exists():
        parser.error('use a new output directory; existing output is never overwritten')
    clips_dir = args.output / 'shot-clips'
    clips_dir.mkdir(parents=True)

    def render(item):
        index, shot = item
        frames = round(shot['end_seconds'] * 30) - round(shot['start_seconds'] * 30)
        output = clips_dir / f'{index:03d}.mp4'
        # Preserve the complete source picture; blurred copies fill only its margins.
        crop = shot.get('crop')
        source_filter = ''
        if crop:
            x, y, width, height = crop
            source_filter = f'crop=iw*{width}:ih*{height}:iw*{x}:ih*{y},'
        fit_height = shot.get('fit_height', 720)
        labeled = shot.get('community_reference') and args.community_badge
        badge_inputs = ['-i', str(args.community_badge)] if labeled else []
        if shot.get('fit_mode') == 'fill':
            # Only opt in after checking that a center crop preserves the reaction.
            filters = ('[0:v]' + source_filter +
                       'scale=1280:720:force_original_aspect_ratio=increase,'
                       'crop=1280:720,setsar=1[base];')
        else:
            filters = ('[0:v]' + source_filter + 'split=2[b][f];'
                       '[b]scale=1280:720:force_original_aspect_ratio=increase,'
                       'crop=1280:720,boxblur=24:2,eq=brightness=-0.25[bg];'
                       f'[f]scale=1280:{fit_height}:force_original_aspect_ratio=decrease[fg];'
                       f'[bg][fg]overlay=(W-w)/2:({fit_height}-h)/2,setsar=1[base];')
        filters += '[base][1:v]overlay=0:0,format=yuv420p[v]' if labeled else '[base]format=yuv420p[v]'
        subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-n',
                        '-loop', '1', '-i', str(root / shot['asset_file']),
                        *badge_inputs,
                        '-filter_complex', filters, '-map', '[v]', '-an',
                        '-r', '30', '-frames:v', str(frames), '-c:v', 'libx264',
                        '-preset', 'ultrafast', '-crf', '22', '-threads', '2',
                        str(output)], check=True)
        return output

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        clips = list(pool.map(render, enumerate(shots, 1)))
    listing = clips_dir / 'concat.txt'
    listing.write_text(''.join(f"file '{p.name}'\n" for p in clips))
    output = args.output / 'reference-sequence.mp4'
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-n',
                    '-f', 'concat', '-safe', '0', '-i', str(listing),
                    '-c', 'copy', '-movflags', '+faststart', str(output)], check=True)
    print(f'{len(clips)} shots, {end_frame / 30:.3f} seconds: {output}')


if __name__ == '__main__':
    main()
