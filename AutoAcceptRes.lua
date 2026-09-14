-- Accepts resurrection offers automatically, but never a battle res.
--
-- RESURRECT_REQUEST fires for a caster's resurrect, in and out of combat. The
-- popup is raised by Blizzard's own handler, so it is hidden after accepting
-- rather than suppressed beforehand.

local ADDON = ...

-- Blizzard raises one of these depending on whether the res carries sickness
-- and whether a timer is running.
local POPUPS = {
    "RESURRECT",
    "RESURRECT_NO_SICKNESS",
    "RESURRECT_NO_TIMER",
}

local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("RESURRECT_REQUEST")

-- Taking a battle res is a call about positioning and cooldowns that only the
-- player can make, so it is never automatic and there is no setting for it.
--
-- InCombatLockdown() is not enough on its own: a dead player is out of combat,
-- which is precisely the battle res case. IsEncounterInProgress covers a boss
-- fight, and the group scan covers a dungeon pull, where neither of the other
-- two answers true.
local function CombatIsHappening()
    if InCombatLockdown() or IsEncounterInProgress() then
        return true
    end

    local prefix, count = "party", 4
    if IsInRaid() then
        prefix, count = "raid", GetNumGroupMembers() or 0
    end

    for i = 1, count do
        local unit = prefix .. i
        if UnitExists(unit) and UnitAffectingCombat(unit) then
            return true
        end
    end

    return false
end

local function Accept()
    AcceptResurrect()
    for _, popup in ipairs(POPUPS) do
        StaticPopup_Hide(popup)
    end
end

f:SetScript("OnEvent", function(_, event, arg1)
    if event == "ADDON_LOADED" and arg1 == ADDON then
        AutoAcceptResDB = AutoAcceptResDB or {}
        if AutoAcceptResDB.enabled == nil then
            AutoAcceptResDB.enabled = true
        end
        -- Retired setting. Cleared so an old profile cannot re-enable a
        -- behaviour that no longer exists.
        AutoAcceptResDB.inCombat = nil
        return
    end

    if event == "RESURRECT_REQUEST" then
        if not AutoAcceptResDB.enabled then
            return
        end
        if CombatIsHappening() then
            return
        end
        Accept()
    end
end)

SLASH_AUTOACCEPTRES1 = "/aar"
SlashCmdList.AUTOACCEPTRES = function(msg)
    msg = (msg or ""):lower():match("^%s*(.-)%s*$")
    if msg == "" or msg == "toggle" then
        AutoAcceptResDB.enabled = not AutoAcceptResDB.enabled
        print("AutoAcceptRes: " .. (AutoAcceptResDB.enabled and "on" or "off") .. ".")
    else
        print("AutoAcceptRes: /aar toggles. A battle res is never auto-accepted.")
    end
end
