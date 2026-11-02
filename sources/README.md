# sources/ — primary materials (INPUT ONLY once landed; never generated)

## lectures/ — the teacher (archive voice; filled at intake)
| path | what lands here |
|---|---|
| `audio/` | lecture mp3s (single mic/room preferred; symlinks allowed if tracked) |
| `transcripts/` | timestamped JSONs `{t, end, text}` (CF-whisper schema) |
| `yt-subs/` | YT cue JSONs for lectures without native transcripts (anchor-mapped at render) |
| `ds-full/` `ds-mp3/` | distributor originals (if audio/ holds symlinks) |
| `cutplans/` | era-1 keep-lists + cutplans (method history once built) |

## text/ — the work (verbatim home)
| path | what lands here |
|---|---|
| `excavations/` | quote pools per chapter/section = THE verbatim home (G5 anchors here) |
| `readings/` | timestamped reading transcripts (the verbatim heard aloud) |

Rule: verbatim fields are extracted with {file,start,end} provenance —
never typed (axiom 1). No provenance = the quote does not exist.
