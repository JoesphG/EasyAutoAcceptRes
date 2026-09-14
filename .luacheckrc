-- Every WoW global the addon reads is declared here, so real problems stand out.

local wow_api = {
    "AcceptResurrect",
    "CreateFrame",
    "GetNumGroupMembers",
    "InCombatLockdown",
    "IsEncounterInProgress",
    "IsInRaid",
    "StaticPopup_Hide",
    "UnitAffectingCombat",
    "UnitExists",
}

std = "lua51"
max_line_length = 120
codes = true
exclude_files = { ".release/" }

globals = {
    "AutoAcceptResDB", -- SavedVariables
    "SlashCmdList",
    "SLASH_AUTOACCEPTRES1",
}

read_globals = wow_api

-- The stubs define the client API, so there it is writable.
files["tests/"] = {
    globals = wow_api,
    ignore = { "212" }, -- stub signatures mirror Blizzard's, unused args and all
}
