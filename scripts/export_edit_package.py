#!/usr/bin/env python3
"""Package a rendered shot list, source images, PCM audio and SRT for local transfer."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET

FPS = 30


def node(parent, tag, value=None, **attributes):
    element = ET.SubElement(parent, tag, attributes)
    if value is not None:
        element.text = str(value)
    return element


def rate(parent):
    element = node(parent, 'rate')
    node(element, 'timebase', FPS)
    node(element, 'ntsc', 'FALSE')


def characteristics(parent, stream):
    sample = node(parent, 'samplecharacteristics')
    if stream['codec_type'] == 'video':
        rate(sample)
        node(sample, 'width', stream['width'])
        node(sample, 'height', stream['height'])
        node(sample, 'anamorphic', 'FALSE')
        node(sample, 'pixelaspectratio', 'square')
        node(sample, 'fielddominance', 'none')
    else:
        node(sample, 'depth', stream['bits_per_sample'])
        node(sample, 'samplerate', stream['sample_rate'])


def probe(path):
    streams = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(path),
    ]))['streams']
    if len(streams) != 1:
        raise ValueError(f'Expected one stream in {path}')
    return streams[0]


def clip(track, media_path, identifier, start, end, stream):
    media_type = stream['codec_type']
    item = node(track, 'clipitem', id=f'clip-{identifier}')
    node(item, 'name', media_path.name)
    rate(item)
    for tag, value in [('duration', end-start), ('start', start), ('end', end),
                       ('in', 0), ('out', end-start)]:
        node(item, tag, value)
    source = node(item, 'file', id=f'file-{identifier}')
    node(source, 'name', media_path.name)
    node(source, 'pathurl', media_path.as_uri().replace('file:///', 'file://localhost/', 1))
    node(source, 'duration', end-start)
    rate(source)
    file_stream = node(node(source, 'media'), media_type)
    characteristics(file_stream, stream)
    if media_type == 'audio':
        node(file_stream, 'channelcount', stream['channels'])
        source_track = node(item, 'sourcetrack')
        node(source_track, 'mediatype', 'audio')
        node(source_track, 'trackindex', 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ('shots', 'clips', 'images', 'audio', 'captions', 'preview', 'readme', 'output'):
        parser.add_argument(f'--{argument}', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error('use a new output directory')
    plan = json.loads(args.shots.read_text())
    shots, end_frame = [], 0
    for index, shot in enumerate(plan['shots'], 1):
        start = round(shot['start_seconds'] * FPS)
        end = round(shot['end_seconds'] * FPS)
        source = args.clips / f'{index:03d}.mp4'
        stream = probe(source)
        if (start != end_frame or end <= start or stream['codec_type'] != 'video'
                or stream['r_frame_rate'] != '30/1' or int(stream['nb_frames']) != end-start):
            raise ValueError(f'Shot {index} does not match the continuous 30 fps edit')
        shots.append((shot, source, start, end, stream))
        end_frame = end
    audio = probe(args.audio)
    if not shots or audio['codec_type'] != 'audio' or abs(float(audio['duration']) - end_frame/FPS) > .001:
        raise ValueError('Audio duration and picture edit do not match')

    root = ET.Element('xmeml', version='5')
    sequence = node(root, 'sequence', id='sequence-1')
    node(sequence, 'name', output.name)
    node(sequence, 'duration', end_frame)
    rate(sequence)
    timecode = node(sequence, 'timecode')
    rate(timecode)
    node(timecode, 'string', '00:00:00:00')
    node(timecode, 'frame', 0)
    node(timecode, 'displayformat', 'NDF')
    media = node(sequence, 'media')
    video = node(media, 'video')
    characteristics(node(video, 'format'), shots[0][-1])
    picture_track = node(video, 'track')
    audio_section = node(media, 'audio')
    node(audio_section, 'channelcount', audio['channels'])
    characteristics(node(audio_section, 'format'), audio)
    audio_track = node(audio_section, 'track')

    for folder in ('media/shots', 'source-images'):
        (output / folder).mkdir(parents=True)
    for shot, source, start, end, stream in shots:
        image = Path(shot['asset_file'])
        if image.name != str(image):
            raise ValueError(f'Expected a basename for the source image: {image}')
        target = output / 'media/shots' / f'{shot["shot_id"]}-{image.stem}.mp4'
        shutil.copyfile(source, target)
        clip(picture_track, target, shot['shot_id'], start, end, stream)
        image_target = output / 'source-images' / image
        if not image_target.exists():
            shutil.copyfile(args.images / image, image_target)
    audio_target = output / 'media/song.wav'
    shutil.copyfile(args.audio, audio_target)
    clip(audio_track, audio_target, 'song', 0, end_frame, audio)
    ET.indent(root)
    (output / 'timeline.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                       '<!DOCTYPE xmeml>\n' + ET.tostring(root, encoding='unicode') + '\n')
    for source, target in [(args.shots, 'shots.json'), (args.captions, 'subtitles-en-zh.srt'),
                           (args.preview, 'preview.mp4'), (args.readme, 'README.md')]:
        shutil.copyfile(source, output / target)
    print(f'{len(shots)} cuts, {end_frame} frames, {end_frame/FPS:.3f}s: {output}')


if __name__ == '__main__':
    main()
