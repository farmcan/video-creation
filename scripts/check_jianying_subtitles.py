#!/usr/bin/env python3
"""Check exported target text, timings, archive hashes and privacy (not sync)."""
import hashlib
import json
import re
from pathlib import Path

from prepare_jianying_subtitles import CASE, read_lines

CAPTIONS = CASE / "captions"
TIME = re.compile(r"^(\d\d):(\d\d):(\d\d),(\d{3}) --> (\d\d):(\d\d):(\d\d),(\d{3})$")


def seconds(parts):
    h, m, s, ms = map(int, parts)
    assert m < 60 and s < 60
    return h * 3600 + m * 60 + s + ms / 1000


def check_srt(path, expected_en, expected_zh):
    blocks = path.read_text(encoding="utf-8").strip().split("\n\n")
    assert len(blocks) == len(expected_en) == len(expected_zh), path
    times = []
    for index, (block, en, zh) in enumerate(zip(blocks, expected_en, expected_zh), 1):
        lines = block.splitlines()
        assert int(lines[0]) == index, (path, index)
        match = TIME.fullmatch(lines[1])
        assert match, (path, index, "invalid SRT time")
        start, end = seconds(match.groups()[:4]), seconds(match.groups()[4:])
        assert 0 <= start < end <= 252.502, (path, index)
        assert " ".join(" ".join(lines[2:-1]).split()) == " ".join(en.split()), (path, index, "English changed")
        assert lines[-1] == zh, (path, index, "Chinese changed")
        times.append((start, end))
    assert all(a[1] < b[0] for a, b in zip(times, times[1:])), (path, "overlap")
    return times


def main():
    en, zh = read_lines(CASE / "lyrics-en-v2.txt"), read_lines(CASE / "lyrics-zh-v1.txt", True)
    manifest = json.loads((CAPTIONS / "manifest.json").read_text())
    assert manifest["versions"]["v1"]["status"] == "failed_timing"
    assert manifest["current_candidate"] == "v2"
    for version in ["v1", "v2"]:
        record = manifest["versions"][version]
        path = CAPTIONS / record["srt_file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["srt_sha256"]
        times = check_srt(path, en, zh)
        if version == "v2":
            assert all(b-a >= 1.5 for a,b in times), "Truncated cue reintroduced"
    report_path = CAPTIONS / "lyrics-bilingual-v2.diagnosis.json"
    report_text = report_path.read_text()
    assert all(marker not in report_text for marker in ["/Users/", "audio_url", "base64"]), "Private diagnostic data exported"
    report = json.loads(report_text)
    v2_times = check_srt(CAPTIONS / manifest["current_srt"], en, zh)
    assert len(report["cues"]) == 44
    for cue, (start, end) in zip(report["cues"], v2_times):
        assert cue["start"] == start and cue["end"] == end
    for name, digest in report["source_files"].items():
        assert hashlib.sha256((CASE / name).read_bytes()).hexdigest() == digest
    chorus = check_srt(CAPTIONS / "lyrics-bilingual-chorus-v2.srt", en[10:18], zh[10:18])
    assert chorus == v2_times[10:18]
    assert v2_times[17][1] < 112 and v2_times[18][0] >= 126, "Interlude blank lost"
    assert sum(line.startswith("Save a seat") for line in en) == 3
    assert sum(line == "Oh, yeah, yeah!" for line in en) == 4
    print("Validated archived v1, v2/chorus target text, hashes, cue times and redaction; playback sync remains separate")


if __name__ == "__main__":
    main()
