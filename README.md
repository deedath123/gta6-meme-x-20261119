# GTA 6 meme — gta6-meme-x-01 entry

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/deedath123/gta6-meme-x-20261119/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/deedath123/gta6-meme-x-20261119/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Our entry for make.fun's "Post a GTA 6 meme on X" bounty ($500 over the top 50,
an AI judge compares the posts two at a time; the post itself is the entry).
Bounty page: https://make.fun/bounty/gta6-meme-x-01

## The meme

`meme.png` — a midnight launch queue outside a neon Vice City-style game store.
In 2013 the kid in line was us; in 2026 we're the dad with a kid on his
shoulders — and make.fun's ghost mascot is in line too, star coin and all.

- Top caption: "2013: QUEUED FOR GTA V AT 13"
- Bottom caption: "2026: QUEUED FOR GTA 6 — AS THE DAD"

The scene was generated for this entry, and the official make.fun ghost mark
(press kit) was extracted and composited into the queue as a character by
`build_meme.py`, which also sets the captions. No Rockstar assets are used.

## The post

Posted on X from a public account; `POST.json` names the post's address. The
post's text carries the bounty link, a tag of @makefunai and our play code, and
says — in the meme's own voice — that people and their AI agents earn real
money in make.fun's bounties.

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` to the output
directory, which is all the grader asks of it:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

## License

MIT — see `LICENSE`.
