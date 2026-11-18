#!/usr/bin/env python3
"""Make provisional target-lyric subtitles from existing ASR; never runs ASR.

All times require listening review. Text is the intended lyric, not a verified
transcription. Monotonic word alignment preserves repeated chorus order. Only
unanchored individual lines use interpolation between neighbouring anchors.
"""
import argparse
import difflib
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "projects/jensen-song-2026-11-17"
PRIVATE = Path.home() / "Movies/AI-Music/2026-11-18-jensen"
WORD = re.compile(r"[a-z]+(?:'[a-z]+)?", re.I)
HEADINGS_ZH = {"主歌一", "推进一", "副歌", "主歌二", "推进二", "最后一遍副歌"}
STOP = {"a", "the", "on", "in", "of", "to", "my", "his", "her", "it", "is", "and", "for", "that", "they", "we", "he", "got", "can"}


def words(text):
    return [w.lower().replace("'", "") for w in WORD.findall(text)]


def read_lines(path, chinese=False):
    return [s for line in path.read_text().splitlines()
            if (s := line.strip()) and not s.startswith("[") and (not chinese or s not in HEADINGS_ZH)]


def source_words(data):
    result = []
    for segment in data["transcription"]:
        if "♪" not in segment["text"]:
            continue
        chars, times = [], []
        for token in segment.get("tokens", []):
            text = token["text"]
            if text.startswith("[_"):
                continue
            chars.extend(text)
            times.extend([(token["offsets"]["from"] / 1000,
                           token["offsets"]["to"] / 1000,
                           token.get("p", 0))] * len(text))
        text = "".join(chars)
        for m in WORD.finditer(text):
            spans = times[m.start():m.end()]
            result.append({"word": m.group().lower().replace("'", ""),
                           "start": min(t[0] for t in spans), "end": max(t[1] for t in spans),
                           "p": sum(t[2] for t in spans) / len(spans)})
    return result


def align(target, source):
    """Global dynamic programming with fuzzy substitutions and word gaps."""
    m, n = len(target), len(source)
    previous = [j * .85 for j in range(n + 1)]
    trace = [bytearray(n + 1) for _ in range(m + 1)]
    for j in range(1, n + 1):
        trace[0][j] = 2
    for i in range(1, m + 1):
        current = [i * 1.0] + [0.] * n
        trace[i][0] = 1
        for j in range(1, n + 1):
            similarity = difflib.SequenceMatcher(None, target[i - 1], source[j - 1]["word"]).ratio()
            substitution = 0 if similarity == 1 else 1.15 - similarity * .85
            choices = [previous[j - 1] + substitution, previous[j] + 1.0, current[j - 1] + .85]
            direction = min(range(3), key=choices.__getitem__)
            current[j], trace[i][j] = choices[direction], direction
        previous = current
    pairs = []
    i, j = m, n
    while i or j:
        direction = trace[i][j]
        if direction == 0:
            similarity = difflib.SequenceMatcher(None, target[i - 1], source[j - 1]["word"]).ratio()
            pairs.append((i - 1, j - 1, similarity))
            i -= 1
            j -= 1
        elif direction == 1:
            i -= 1
        else:
            j -= 1
    return list(reversed(pairs))


def timestamp(seconds):
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3600000)
    minute, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return f"{h:02}:{minute:02}:{sec:02},{ms:03}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--english", type=Path, default=CASE / "lyrics-en-v2.txt")
    parser.add_argument("--chinese", type=Path, default=CASE / "lyrics-zh-v1.txt")
    parser.add_argument("--asr", type=Path, default=PRIVATE / "take-a-local-asr-unprompted.json")
    parser.add_argument("--output", type=Path, default=PRIVATE / "jianying-import")
    args = parser.parse_args()
    english, chinese = read_lines(args.english), read_lines(args.chinese, True)
    assert len(english) == len(chinese) == 44, (len(english), len(chinese))
    out_srt = args.output / "lyrics-bilingual-draft.srt"
    out_json = args.output / "lyrics-bilingual-draft.cues.json"
    for path in [out_srt, out_json]:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite {path}")
    source = source_words(json.loads(args.asr.read_text()))
    target, line_indices = [], []
    for index, line in enumerate(english):
        ws = words(line)
        target.extend(ws)
        line_indices.extend([index] * len(ws))
    grouped = [[] for _ in english]
    for target_index, source_index, similarity in align(target, source):
        if similarity >= .64:
            grouped[line_indices[target_index]].append({"target_word": target[target_index],
                                                      "source_word": source[source_index]["word"],
                                                      "similarity": round(similarity, 3), **source[source_index]})
    cues = []
    for index, (en, zh, anchors) in enumerate(zip(english, chinese, grouped)):
        coverage = len(anchors) / len(words(en))
        content_matches = sum(a["target_word"] not in STOP for a in anchors)
        usable = len(anchors) >= 2 and (content_matches >= 2 or en == "Oh, yeah, yeah!")
        confidence = "medium" if usable and coverage >= .65 else "low"
        cues.append({"id": index + 1, "english": en, "chinese": zh,
                     "start": min(a["start"] for a in anchors) if usable else None,
                     "end": max(a["end"] for a in anchors) if usable else None,
                     "timing_method": "automatic_monotonic_word_anchors" if usable else "missing_line_neighbour_interpolation",
                     "confidence": confidence, "matched_word_fraction": round(coverage, 3),
                     "needs_listening_review": True, "anchors": anchors})
    for index, cue in enumerate(cues):
        if cue["start"] is not None:
            continue
        left = next((cues[k] for k in range(index - 1, -1, -1) if cues[k]["start"] is not None), None)
        right = next((cues[k] for k in range(index + 1, len(cues)) if cues[k]["start"] is not None), None)
        assert left and right, "Cannot infer outside detected vocal extent"
        missing = [c for c in cues[left["id"]:right["id"] - 1] if c["start"] is None]
        slot = missing.index(cue)
        # Local gap only: never distribute all lyrics uniformly over the song.
        a, b = left["end"], right["start"]
        assert b > a, (cue["id"], a, b)
        width = (b - a) / len(missing)
        cue["start"], cue["end"] = a + slot * width, a + (slot + 1) * width
    for index in range(len(cues) - 1):
        left, right = cues[index:index + 2]
        if left["end"] >= right["start"]:
            boundary = (left["end"] + right["start"]) / 2
            left["end"], right["start"] = boundary - .01, boundary + .01
            left["boundary_adjusted"] = right["boundary_adjusted"] = True
        if left["end"] <= left["start"]:
            left["end"] = min(right["start"] - .01, left["start"] + .25)
            left["confidence"] = "low"
    for cue in cues:
        assert 0 <= cue["start"] < cue["end"] <= 252.502, cue
        cue["start"], cue["end"] = round(cue["start"], 3), round(cue["end"], 3)
    assert all(a["end"] < b["start"] for a, b in zip(cues, cues[1:])), "Subtitle cues overlap"
    args.output.mkdir(parents=True, exist_ok=True)
    body = "\n\n".join(f"{c['id']}\n{timestamp(c['start'])} --> {timestamp(c['end'])}\n{c['english']}\n{c['chinese']}" for c in cues) + "\n"
    manifest = {"status": "provisional_target_lyrics_not_verified_transcription", "cue_count": 44,
                "source_files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [args.english, args.chinese, args.asr]},
                "method": "monotonic fuzzy word alignment to existing local unprompted ASR token offsets; only missing lines locally interpolated",
                "limitations": ["All timings require listening review; source singing-ASR token times can be compressed or offset.",
                                "Caption text is the intended lyric and Chinese adaptation, not proof of exact sung words.",
                                "No ASR, generation, payment or new media acquisition was performed."],
                "cues": cues}
    # Exclusive create is deliberate: repeated runs must use a new output folder.
    with out_srt.open("x", encoding="utf-8") as file:
        file.write(body)
    with out_json.open("x", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(json.dumps({"srt": str(out_srt), "cues_json": str(out_json), "cue_count": 44,
                      "first_start": cues[0]["start"], "last_end": cues[-1]["end"],
                      "low_confidence_ids": [c["id"] for c in cues if c["confidence"] == "low"],
                      "interpolated_ids": [c["id"] for c in cues if c["timing_method"] != "automatic_monotonic_word_anchors"]}, indent=2))


if __name__ == "__main__":
    main()
