<!--
Source for the CurseForge project description. There is no API for it, so it
is pasted by hand into the Description editor with the format set to Markdown.
-->

**Accepts your resurrection the moment it arrives.**

AutoAcceptRes takes a resurrection offer and closes the popup, so a wipe
recovery is one click shorter for everyone waiting on you. Two files, no
libraries, two commands.

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

## Support

Bugs, questions and ideas all go to Discord: **[discord.gg/zHT3bGEQ52](https://discord.gg/zHT3bGEQ52)**

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

Source: [github.com/JoesphG/AutoAcceptRes](https://github.com/JoesphG/AutoAcceptRes) — MIT licensed.
