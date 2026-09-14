<!--
Source for the CurseForge project description. There is no API for it, so it
is pasted by hand into the Description editor with the format set to Markdown.
-->

**Accepts your resurrection. Your battle res too, if you say so.**

AutoAcceptRes takes a resurrection offer the moment it arrives and closes the
popup, so a wipe recovery is one click shorter for everyone who was waiting on
you. Two files, no libraries, one command.

## What it does

When a caster offers you a resurrection out of combat, the addon accepts it.
That is all.

## Battle res

**A battle res is left to you by default.** Taking one is a call about
positioning and cooldowns. `/aar combat` turns auto-accepting it on.

"In combat" is judged three ways, because a dead player is not in combat
lockdown even while the fight carries on around them:

- combat lockdown,
- an encounter in progress,
- any party or raid member in combat, which catches a dungeon pull where
  neither of the other two answers true.

## Commands

| Command | Effect |
| --- | --- |
| `/aar` | Toggle on or off |
| `/aar combat` | Toggle accepting a battle res |

## Support

Bugs and ideas go to the
[issue tracker on GitHub](https://github.com/JoesphG/AutoAcceptRes/issues).

Source: [github.com/JoesphG/AutoAcceptRes](https://github.com/JoesphG/AutoAcceptRes) — MIT licensed.
