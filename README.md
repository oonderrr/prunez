# prunez (fork)

> **This is a modified fork of [CrescentKohana/prunez](https://github.com/CrescentKohana/prunez)**
> (originally by Marko Leinikka, zlib License; see `LICENSE`, unchanged).
> It is not the original software.

## Changes in this fork

- Reuses a single HTTP client for all requests instead of opening a new
  connection per delete. Fixes frequent `connection closed via error` crashes.
- Retries failed requests (up to 10 times, 10 s apart) instead of panicking.
- Adds `scripts/merge_listens.py`, which converts ListenBrainz's newer export
  format (zip with `listens/<year>/<month>.jsonl`) into the single
  `listens.json` that prunez expects.

## Using the new export format

1. On listenbrainz.org, go to Settings → Export data, request an export and unzip the download.
2. Merge the listens into the single file prunez expects:

```
   python3 scripts/merge_listens.py <unzipped export>/listens listens.json
```

3. Run prunez as described below.

# ListenBrainz Prune

[![Rust Build](https://github.com/Luukuton/prunez/actions/workflows/rust.yml/badge.svg)](https://github.com/Luukuton/prunez/actions/workflows/rust.yml)

At the time of writing ListenBrainz doesn't have the option to mass delete listens. This alleviates that. 

## Usage

- Copy and rename `example.env` to `.env` and change LISTENBRAINZ_API_KEY to the one found in: [listenbrainz.org/profile](https://listenbrainz.org/profile)
- Export ListenBrainz listens: [listenbrainz.org/profile/export](https://listenbrainz.org/profile/export)
- Place the exported .json with the executable. Rename it to listens.json or set a different source filename with --filename.
- Run the executable with options below.

```prunez [options]```

- `--filename, -f` sets source filename. Default: **listens.json**
- `--url, -u` sets API URL. Default: **https://api.listenbrainz.org**
- `--artists, -a` list of artists. All listens associated with them will be pruned. Separated by `;;`.
- `--songs, -s` list of song titles. Separated by `;;`.
- `--recids, -r` list of recording msids. Separated by `;`.

## Development

- Format with `cargo fmt`
- Build with `cargo build`
- Run with `cargo run -- [options]`
- Build for release with `cargo build --release`
