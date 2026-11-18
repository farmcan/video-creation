#!/usr/bin/env python3
"""Assemble provisional full-phrase captions after actual local audio rechecks.

v1's matched-word bounding boxes are deliberately not reused as cue extents.
The phrase boundaries below come from section-local unprompted whisper.cpp
runs (tiny.en-q5_1, -dtw tiny.en -nfa) plus documented phrase assembly.
They remain candidates for native playback and human listening acceptance.
"""
import argparse
import hashlib
import json
import textwrap
from pathlib import Path

from prepare_jianying_subtitles import CASE, PRIVATE, read_lines, timestamp

# (start, last phrase boundary, source window, assembly note)
PHRASES = [
    (32.90, 39.20, "verse1", "first detected vocal phrase"),
    (39.20, 41.18, "verse1", "adlib split before gens/street token group"),
    (41.18, 48.40, "verse1", "street and wedding-vows segments combined"),
    (48.40, 52.17, "verse1", "charts/clicks phrase ends before oh token"),
    (52.17, 56.74, "verse1", "adlib spans source segment split"),
    (56.74, 61.80, "verse1", "prime-time plus drama/screen; recovered by new local probe"),
    (64.00, 68.00, "full", "prechorus1 phrase"),
    (68.00, 72.00, "full", "export-control and bless-his-soul segments combined"),
    (72.00, 76.00, "full", "wife/truth and press-release segments combined"),
    (76.00, 79.30, "chorus1", "preceding morals-police phrase detected in crop"),
    (79.30, 83.56, "chorus1", "save/fill plus got-his-back; split before Jensen DTW centre"),
    (83.56, 87.38, "chorus1", "both names plus get-back-on-track, not only matched tail words"),
    (87.38, 90.86, "chorus1", "fast-chips plus late-night-show"),
    (90.86, 95.02, "chorus1", "tweet and explain segments combined"),
    (95.02, 98.66, "chorus1", "big-suits plus blame-game segments combined"),
    (98.66, 102.82, "chorus1", "cloud/pile-of-shame phrase"),
    (102.82, 107.06, "chorus1", "clone-voice and brain phrase; split before let token group"),
    (107.06, 111.40, "chorus1", "let-him-cook plus back-in-game, then interlude blank"),
    (127.00, 133.00, "verse2", "comments phrase; old ~114s occurrence was not confirmed"),
    (133.00, 136.00, "verse2", "adlib"),
    (136.00, 141.00, "verse2", "PhD phrase recovered by new local probe"),
    (142.00, 149.00, "verse2", "race/chips phrase"),
    (149.00, 151.00, "verse2", "adlib split before open/source DTW group"),
    (151.00, 157.00, "verse2", "open-source/lips phrase"),
    (157.00, 161.00, "verse2", "China and code-free segments combined"),
    (161.00, 165.00, "verse2", "proof and extra-fee segments combined"),
    (165.00, 169.00, "verse2", "open-weights/source and closed-code segments combined"),
    (169.00, 173.30, "verse2", "saved-seat/share-load phrase to next chorus entrance"),
    (173.30, 177.48, "choruses23", "save/fill plus got-his-back; name split from DTW centres"),
    (177.48, 181.36, "choruses23", "both names plus back-on-track"),
    (181.36, 184.76, "choruses23", "fast-chips plus late-night-show"),
    (184.76, 188.94, "choruses23", "tweet and explain segments combined"),
    (188.94, 192.82, "choruses23", "big-suits and blame-game; split before you/cant token group"),
    (192.82, 196.76, "choruses23", "cloud/pile-of-shame phrase"),
    (196.76, 200.64, "choruses23", "voice/brain segments combined"),
    (200.64, 205.64, "choruses23", "cook/game segments combined"),
    (205.64, 208.77, "choruses23", "final chorus starts without a long interlude"),
    (208.77, 212.64, "choruses23", "both names plus back-on-track"),
    (212.64, 216.04, "choruses23", "fast-chips plus late-night-show"),
    (216.04, 220.12, "choruses23", "tweet and explain segments combined"),
    (220.12, 224.04, "choruses23", "big-suits/blame-game split before you/cant token group"),
    (224.04, 228.04, "choruses23", "cloud/pile-of-shame phrase"),
    (228.04, 231.96, "choruses23", "voice/brain segments combined"),
    (231.96, 238.00, "choruses23", "cook/game and short release buffer, then instrumental outro"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="NEW output directory; existing v2 SRT/diagnosis are never overwritten")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    srt = args.output / "lyrics-bilingual-v2.srt"
    diagnosis = args.output / "lyrics-bilingual-v2.diagnosis.json"
    if srt.exists() or diagnosis.exists():
        raise FileExistsError("v2 output exists; choose a new output directory")
    en, zh = read_lines(CASE / "lyrics-en-v2.txt"), read_lines(CASE / "lyrics-zh-v1.txt", True)
    assert len(en) == len(zh) == len(PHRASES) == 44
    old = json.loads((PRIVATE / "jianying-import/lyrics-bilingual-draft.cues.json").read_text())
    sources = {"verse1": "verse1-tiny-dtw-nfa.json", "verse2": "verse2-tiny-dtw-nfa.json",
               "chorus1": "chorus-tiny-dtw-nfa.json", "choruses23": "choruses23-tiny-dtw-nfa.json",
               "full": "full-tiny-dtw-nfa.json"}
    evidence = {}
    for key, name in sources.items():
        path = PRIVATE / "jianying-import/subtitle-v2-diagnostics" / name
        data = json.loads(path.read_text())
        assert any(token.get("t_dtw", -1) >= 0 for segment in data["transcription"] for token in segment["tokens"])
        evidence[key] = {"file_name": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "storage": "private_local_evidence_not_exported",
                         "dtw_enabled": True, "lyrics_prompt_supplied": False}
    cues = []
    for i, ((start, boundary, key, note), english, chinese) in enumerate(zip(PHRASES, en, zh)):
        end = round(boundary - .04, 3)
        assert 0 <= start < end <= 252.502
        v1 = old["cues"][i]
        cues.append({"id": i + 1, "start": start, "end": end, "duration": round(end-start, 3),
                     "english": english, "chinese": chinese, "evidence_window": key,
                     "assembly_note": note, "confidence": "provisional_local_audio_alignment",
                     "needs_native_playback_acceptance": True, "v1_start": v1["start"], "v1_end": v1["end"],
                     "v1_duration": round(v1["end"]-v1["start"], 3)})
    assert all(a["end"] < b["start"] for a,b in zip(cues,cues[1:]))
    content = "\n\n".join(
        f"{c['id']}\n{timestamp(c['start'])} --> {timestamp(c['end'])}\n"
        + "\n".join(textwrap.wrap(c["english"], width=78)) + "\n" + c["chinese"] for c in cues) + "\n"
    report = {"status": "v2_candidate_after_v1_playback_rejection_not_yet_accepted", "cue_count": 44,
              "v1_failure": "Matched-word boxes truncated names and sentence tails; old whole-song ASR also placed first chorus about four seconds early.",
              "method": "Fresh actual-audio local recognition with real DTW (-nfa); section phrase assembly and hold until following entrance, with interlude/outro blanks.",
              "actual_audio_run_evidence": evidence,
              "source_files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in [CASE / "lyrics-en-v2.txt", CASE / "lyrics-zh-v1.txt"]},
              "model_acquisition": {"requested_model": "small.en", "outcome": "historical_attempt_not_acquired_not_used",
                                    "actual_model_used": "tiny.en-q5_1_existing_local",
                                    "source": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin",
                                    "official_source_documentation": "https://github.com/ggml-org/whisper.cpp/blob/master/models/download-ggml-model.sh",
                                    "curl_attempt": "TLS failure after approximately 5 seconds, 0 bytes",
                                    "python_tls_attempt": "read timeout after 165.66 seconds",
                                    "download_time_limit_seconds": 280},
              "first_chorus_v1_visible_seconds": round(sum(c["v1_duration"] for c in cues[10:18]),3),
              "first_chorus_v2_visible_seconds": round(sum(c["duration"] for c in cues[10:18]),3),
              "review_priorities": [6, 12, 19, 21, 23, 24, 29, 33, 37, 41, 44],
              "limits": ["New timings are local-model/DTW candidates, not human-verified singing alignment.",
                         "Target lyric text is retained; it is not proof of the exact generated singing.",
                         "small.en download failed within the bounded attempt; model was not used.",
                         "No native Jianying project or UI was changed by this script."], "cues": cues}
    report["srt_sha256"] = hashlib.sha256(content.encode("utf-8")).hexdigest()
    with srt.open("x", encoding="utf-8") as file:
        file.write(content)
    with diagnosis.open("x", encoding="utf-8") as file:
        json.dump(report,file,ensure_ascii=False,indent=2)
        file.write("\n")
    print(json.dumps({"srt": str(srt), "diagnosis": str(diagnosis), "cue_count":44,
                      "first_chorus_visible_seconds":report["first_chorus_v2_visible_seconds"],
                      "cue12_duration":cues[11]["duration"],"end_seconds":cues[-1]["end"]},indent=2))


if __name__ == "__main__":
    main()
