# webtools-lib.sh: shared helpers for the web tools in this folder.
# The tools load this file themselves; you never need to. It is plain bash and works on bash 3.2 (macOS) and later.
#
# Your keys live in ONE file that only you can read:  ~/.config/webtools/keys.env  (mode 600)
# This library PARSES that file line by line. It never sources it, never runs anything in it, and never prints a value.
# Set WEBTOOLS_KEYS=/other/path to use a different file with the same rules.

WT_KEYS="${WEBTOOLS_KEYS:-$HOME/.config/webtools/keys.env}"

wt_die() {  # wt_die <exit-code> <message...>
  local rc="$1"; shift
  echo "[webtools] $*" >&2
  exit "$rc"
}

wt_check_keyfile() {  # refuse a missing, linked, shared or foreign key file
  [ -e "$WT_KEYS" ] || wt_die 66 "no key file at $WT_KEYS. Create it with: mkdir -p ~/.config/webtools && touch ~/.config/webtools/keys.env && chmod 600 ~/.config/webtools/keys.env  (then add your keys with a text editor; see README.md)"
  [ -L "$WT_KEYS" ] && wt_die 66 "$WT_KEYS is a symbolic link. Use a regular file."
  [ -f "$WT_KEYS" ] || wt_die 66 "$WT_KEYS is not a regular file."
  local perms owner
  perms="$(ls -ln "$WT_KEYS" | cut -c1-10)"
  owner="$(ls -ln "$WT_KEYS" | awk '{print $3}')"
  case "$perms" in
    -rw-------|-r--------) ;;
    *) wt_die 66 "$WT_KEYS can be read by other users ($perms). Fix it with: chmod 600 $WT_KEYS" ;;
  esac
  [ "$owner" = "$(id -u)" ] || wt_die 66 "$WT_KEYS belongs to another user. Use your own key file."
}

wt_get() {  # wt_get <KEY_NAME> <shell-variable>: read one key into a shell variable; returns 1 when absent or empty
  local _wt_want="$1" _wt_var="$2" _wt_line _wt_k _wt_v="" _wt_found=0
  case "$_wt_want" in ''|*[!A-Za-z0-9_]*) wt_die 64 "bad key name: $_wt_want" ;; esac
  case "$_wt_var" in ''|*[!A-Za-z0-9_]*) wt_die 64 "bad variable name: $_wt_var" ;; esac
  while IFS= read -r _wt_line || [ -n "$_wt_line" ]; do
    _wt_line="${_wt_line%$'\r'}"
    _wt_line="${_wt_line#"${_wt_line%%[![:space:]]*}"}"
    case "$_wt_line" in ''|'#'*) continue ;; esac
    case "$_wt_line" in 'export '*) _wt_line="${_wt_line#export }"; _wt_line="${_wt_line#"${_wt_line%%[![:space:]]*}"}" ;; esac
    case "$_wt_line" in *=*) ;; *) continue ;; esac
    _wt_k="${_wt_line%%=*}"; _wt_k="${_wt_k%"${_wt_k##*[![:space:]]}"}"
    [ "$_wt_k" = "$_wt_want" ] || continue
    _wt_v="${_wt_line#*=}"; _wt_v="${_wt_v#"${_wt_v%%[![:space:]]*}"}"; _wt_v="${_wt_v%"${_wt_v##*[![:space:]]}"}"
    case "$_wt_v" in
      \"*\") _wt_v="${_wt_v#\"}"; _wt_v="${_wt_v%\"}" ;;
      \'*\') _wt_v="${_wt_v#\'}"; _wt_v="${_wt_v%\'}" ;;
    esac
    _wt_found=1
  done < "$WT_KEYS"
  [ "$_wt_found" = 1 ] && [ -n "$_wt_v" ] || return 1
  printf -v "$_wt_var" '%s' "$_wt_v"
}

wt_require() {  # wt_require <KEY_NAME> <shell-variable>: like wt_get, but stop with a clear message when missing
  wt_get "$1" "$2" || wt_die 66 "key $1 is missing or empty in $WT_KEYS. Add a line: $1=<value>  (see README.md)"
}

wt_check_token_chars() {  # wt_check_token_chars <KEY_NAME> <value>: tokens go into a curl config line, so allow only safe characters
  case "$2" in *[!A-Za-z0-9._~+/=:-]*) wt_die 65 "key $1 contains unexpected characters (quotes, spaces or backslashes). Re-copy it from the provider." ;; esac
}

wt_scrub_env() {  # drop every CLOUDFLARE_* and CF_* variable inherited from your shell, so another account cannot leak in
  local v
  for v in $(compgen -e); do
    case "$v" in CLOUDFLARE_*|CF_*) unset "$v" ;; esac
  done
}

wt_tail4() {  # wt_tail4 <value>: the last four characters, for banners that show WHICH account without showing it
  local s="$1"
  if [ "${#s}" -gt 4 ]; then printf '%s' "${s: -4}"; else printf '%s' "????"; fi
}
