# AutoAcceptRes

Accepts resurrection offers in World of Warcraft the moment they arrive, so a
wipe recovery is one click shorter for everyone waiting on you.

Two files, no libraries, two commands.

## Features

- **Accepts the res and closes the popup.** Whichever of Blizzard's three
  resurrect dialogs came up, it is gone before you see it.
- **Battle res is your call.** Out of the box the addon steps aside whenever a
  fight is on, because taking a battle res is a decision about positioning and
  cooldowns. `/aar combat` hands that decision to the addon too.
- **Knows when a fight is on.** A dead player is not in combat lockdown, so the
  addon also checks for an encounter in progress and for any party or raid
  member still fighting. That last one catches a dungeon pull, where the other
  two answer no.
- **One toggle to switch it off.** `/aar` and the addon is quiet until you
  turn it back on.

## Commands

| Command | Effect |
| --- | --- |
| `/aar` | Toggle the addon on or off |
| `/aar combat` | Toggle accepting a battle res |

Both settings are saved per account.

## Installation

Download from [CurseForge](https://www.curseforge.com/projects/1695734),
or clone this repository into
`World of Warcraft/_retail_/Interface/AddOns/AutoAcceptRes`. There is no build
step and nothing to embed.

## Support

Bugs, questions and ideas all go to Discord: **https://discord.gg/zHT3bGEQ52**

`#support` for bugs and help, `#ideas` for feature requests, `#announcements`
for release notes. The
[GitHub issue tracker](https://github.com/JoesphG/AutoAcceptRes/issues) works
too.

A bug report gets fixed faster with:

```
Addon version:      (Escape -> AddOns, or the CurseForge app)
Game version:       (bottom of the character select screen)
What I expected:
What happened:
Steps to reproduce:
Lua error (if any):
```

If there is a Lua error, paste the full text from BugSack rather than the
first line.

## Development

```
make check     # luacheck + stylua --check
make test      # lua5.1 tests/run.lua
make format    # stylua .
make package   # BigWigsMods packager, local zip, uploads nothing
```

The tests run the addon against a stubbed client under plain Lua 5.1; no game
needed.

## License

MIT — see [LICENSE](LICENSE).
