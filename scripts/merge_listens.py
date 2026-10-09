#!/usr/bin/env python3
"""Merge a ListenBrainz export (listens/<year>/<month>.jsonl) into a
single listens.json in the format prunez expects."""
import glob, json, os, sys


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: merge_listens.py <export>/listens <output listens.json>")
    src, out = sys.argv[1], sys.argv[2]

    listens = []
    for path in sorted(glob.glob(os.path.join(src, "*", "*.jsonl"))):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                e = json.loads(line)
                if e.get("listened_at") is None:
                    continue
                tm = e.get("track_metadata") or {}
                ai = tm.get("additional_info") or {}
                mm = tm.get("mbid_mapping")
                listens.append({
                    "track_metadata": {
                        "artist_name": tm.get("artist_name"),
                        "release_name": tm.get("release_name"),
                        "track_name": tm.get("track_name"),
                        "additional_info": {
                            "artist_msid": ai.get("artist_msid"),
                            "release_msid": ai.get("release_msid"),
                            "recording_msid": ai.get("recording_msid"),
                        },
                        "mbid_mapping": {
                            "artist_mbids": mm.get("artist_mbids", []),
                            "release_mbid": mm.get("release_mbid"),
                            "recording_mbid": mm.get("recording_mbid"),
                        } if mm else None,
                    },
                    "listened_at": e["listened_at"],
                    "recording_msid": e.get("recording_msid") or "",
                })

    with open(out, "w", encoding="utf-8") as f:
        json.dump(listens, f)
    print(f"Merged {len(listens)} listens into {out}")


if __name__ == "__main__":
    main()