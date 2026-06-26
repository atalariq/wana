#!/usr/bin/env bash
# Publish a generated subtree to its standalone private repo (one-way).
#
#   tools/publish.sh yazi      # push themes/yazi -> atalariq/wana.yazi
#   tools/publish.sh nvim      # push themes/nvim -> atalariq/wana.nvim
#   tools/publish.sh all
#
# We only ever author in this repo, so the split history is linear and pushes
# fast-forward. If a push is rejected, re-run with FORCE=1.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

publish() {
	local name="$1" prefix="$2" url="$3" branch="_dist_${1}"
	[ -d "$prefix" ] || {
		echo "skip $name: $prefix missing"
		return 0
	}
	git remote get-url "$name" >/dev/null 2>&1 || git remote add "$name" "$url"
	git subtree split --prefix="$prefix" -b "$branch"
	if [ "${FORCE:-0}" = "1" ]; then
		git push --force "$name" "$branch:main"
	else
		git push "$name" "$branch:main"
	fi
	git branch -D "$branch"
	echo "published $prefix -> $url (main)"
}

case "${1:-all}" in
yazi) publish wana-yazi themes/yazi "git@github.com:atalariq/wana.yazi.git" ;;
nvim) publish wana-nvim themes/nvim "git@github.com:atalariq/wana.nvim.git" ;;
all)
	publish wana-yazi themes/yazi "git@github.com:atalariq/wana.yazi.git"
	publish wana-nvim themes/nvim "git@github.com:atalariq/wana.nvim.git"
	;;
*)
	echo "usage: tools/publish.sh [yazi|nvim|all]" >&2
	exit 2
	;;
esac
