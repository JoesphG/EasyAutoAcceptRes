.PHONY: all check lint format test package

all: check test

check: lint
	stylua --check .

lint:
	luacheck .

format:
	stylua .

test:
	lua5.1 tests/run.lua

# Build the CurseForge zip locally without uploading anything.
package:
	curl -sL https://raw.githubusercontent.com/BigWigsMods/packager/v2.5.1/release.sh -o /tmp/easyautoacceptres-release.sh
	chmod +x /tmp/easyautoacceptres-release.sh
	/tmp/easyautoacceptres-release.sh -d -t .
