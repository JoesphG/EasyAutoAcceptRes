local FILE = "AutoAcceptRes.lua"

local frame
CreateFrame = function()
    frame = {
        events = {},
        RegisterEvent = function(s, e)
            s.events[e] = true
        end,
        SetScript = function(s, k, fn)
            s[k] = fn
        end,
    }
    return frame
end

local state = {
    lockdown = false,
    encounter = false,
    inRaid = false,
    members = 0,
    combat = {}, -- unit -> true
    exists = {},
}

InCombatLockdown = function()
    return state.lockdown
end
IsEncounterInProgress = function()
    return state.encounter
end
IsInRaid = function()
    return state.inRaid
end
GetNumGroupMembers = function()
    return state.members
end
UnitExists = function(u)
    return state.exists[u] == true
end
UnitAffectingCombat = function(u)
    return state.combat[u] == true
end

local accepted, hidden = 0, {}
AcceptResurrect = function()
    accepted = accepted + 1
end
StaticPopup_Hide = function(n)
    hidden[n] = true
end

SlashCmdList = {}
local printed = {}
print = function(...)
    local t = {}
    for i = 1, select("#", ...) do
        t[#t + 1] = tostring((select(i, ...)))
    end
    printed[#printed + 1] = table.concat(t, " ")
end

assert(loadfile(FILE))("AutoAcceptRes")

local out = io.write
local fails = 0
local function check(n, ok, extra)
    if ok then
        out("  ok   " .. n .. "\n")
    else
        fails = fails + 1
        out("  FAIL " .. n .. (extra and (" -- " .. tostring(extra)) or "") .. "\n")
    end
end
out("AutoAcceptRes test\n")

check("registered both events", frame.events.ADDON_LOADED and frame.events.RESURRECT_REQUEST)

-- Someone else's ADDON_LOADED must not build our defaults.
frame.OnEvent(frame, "ADDON_LOADED", "SomeOtherAddon")
check("ignores another addon loading", AutoAcceptResDB == nil)

frame.OnEvent(frame, "ADDON_LOADED", "AutoAcceptRes")
check("defaults on", AutoAcceptResDB.enabled == true)

local function res()
    local before = accepted
    frame.OnEvent(frame, "RESURRECT_REQUEST")
    return accepted > before
end

check("accepts out of combat", res() == true)
check("hides every popup name", hidden.RESURRECT and hidden.RESURRECT_NO_SICKNESS and hidden.RESURRECT_NO_TIMER)

-- A battle res is refused unless asked for.
check("battle res off by default", AutoAcceptResDB.inCombat == false)
state.lockdown = true
check("refuses in combat lockdown", res() == false)
state.lockdown = false

-- The case InCombatLockdown misses: the player is dead, so out of combat, while
-- the encounter carries on around them.
state.encounter = true
check("refuses during an encounter, dead and out of lockdown", res() == false)
state.encounter = false

-- And a dungeon pull, where neither of the above answers true.
state.exists.party2, state.combat.party2 = true, true
check("refuses while a party member is fighting", res() == false)
state.combat.party2 = false
check("accepts once the pull is over", res() == true)

state.inRaid, state.members = true, 25
state.exists.raid17, state.combat.raid17 = true, true
check("scans the raid, not just the party", res() == false)

-- /aar combat opens the door to a battle res, and only that.
SlashCmdList.AUTOACCEPTRES("combat")
check("/aar combat turns it on", AutoAcceptResDB.inCombat == true)
check("accepts a battle res when asked to", res() == true)
state.lockdown = true
check("in lockdown too", res() == true)
state.lockdown = false
SlashCmdList.AUTOACCEPTRES("combat")
check("/aar combat turns it off again", AutoAcceptResDB.inCombat == false)
check("and the refusal is back", res() == false)
state.combat.raid17 = false

-- A profile from before the setting existed gets the default, not nil.
AutoAcceptResDB.inCombat = nil
frame.OnEvent(frame, "ADDON_LOADED", "AutoAcceptRes")
check("old profile gets combat off", AutoAcceptResDB.inCombat == false)

SlashCmdList.AUTOACCEPTRES("nonsense")
check("unknown command prints help", printed[#printed]:find("/aar combat") ~= nil, printed[#printed])
check("and changed nothing", AutoAcceptResDB.inCombat == false and AutoAcceptResDB.enabled == true)

SlashCmdList.AUTOACCEPTRES("")
check("slash turns it off", AutoAcceptResDB.enabled == false)
check("disabled means no accept", res() == false)
SlashCmdList.AUTOACCEPTRES("")
check("slash turns it back on", res() == true)

out(fails == 0 and "\nall checks passed\n" or ("\n" .. fails .. " failed\n"))
os.exit(fails == 0 and 0 or 1)
