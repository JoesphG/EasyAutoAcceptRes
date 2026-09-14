# AutoAcceptRes

Accepts resurrection offers in World of Warcraft automatically. A battle res
only if you ask for that.

Two files, no libraries. `/aar` toggles it.

## What it does

When a caster offers you a resurrection out of combat, the addon accepts it and
closes the popup. That is all.

## Battle res

**A battle res is left to you by default.** Taking one is a call about
positioning and cooldowns. `/aar combat` turns auto-accepting it on.

"In combat" is judged three ways, because a dead player is not in combat
lockdown even while the fight carries on around them:

- combat lockdown,
- an encounter in progress,
- any party or raid member in combat, which covers a dungeon pull where
  neither of the other two answers true.

## Commands

| Command | Effect |
| --- | --- |
| `/aar` | Toggle on or off |
| `/aar combat` | Toggle accepting a battle res |

## Installation

Download from CurseForge, or clone this repository into
`World of Warcraft/_retail_/Interface/AddOns/AutoAcceptRes`. There is no build
step and nothing to embed.

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
