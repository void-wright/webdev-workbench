# shell_env.sh: per-call shell setup for this package's SETUP_GUIDE (setup folder .webdev-workbench-setup).
# P0.4 copies it, unchanged, to ~/.webdev-workbench-setup/shell.sh, and every later Bash call starts with
# `. ~/.webdev-workbench-setup/shell.sh`.
# It PARSES Voidloom's env file instead of sourcing it (a sourced file can echo a stray line into stderr), reads only
# PATH, WIZARD_* and CUDA_VISIBLE_DEVICES, strips one layer of matching quotes exactly as Voidloom's writer emits them,
# and never exports a name holding TOKEN, KEY, SECRET or PASSWORD, even under the WIZARD_ prefix.
# Safe to source any number of times. No secrets here.
[ -f "$HOME/.webdev-workbench-setup/pkg_path" ] && { PKG="$(cat "$HOME/.webdev-workbench-setup/pkg_path")"; export PKG; }
export PAGER=cat GIT_PAGER=cat
if [ -f "$HOME/.voidloom/wizard-library-env" ]; then
  _vl_prev_path="$PATH"
  while IFS= read -r _vl_line || [ -n "$_vl_line" ]; do
    case "$_vl_line" in
      PATH=*|WIZARD_[A-Z0-9_]*=*|CUDA_VISIBLE_DEVICES=*)
        _vl_k="${_vl_line%%=*}"; _vl_v="${_vl_line#*=}"
        case "$_vl_k" in *TOKEN*|*KEY*|*SECRET*|*PASSWORD*) continue ;; esac   # no secret enters an agent's environment
        case "$_vl_v" in
          \"*\") _vl_v="${_vl_v#\"}"; _vl_v="${_vl_v%\"}" ;;
          \'*\') _vl_v="${_vl_v#\'}"; _vl_v="${_vl_v%\'}" ;;
        esac
        export "$_vl_k=$_vl_v" ;;
    esac
  done < "$HOME/.voidloom/wizard-library-env"
  case "$_vl_prev_path" in "$PATH"|"$PATH":*) PATH="$_vl_prev_path" ;; *) PATH="$PATH:$_vl_prev_path" ;; esac
  export PATH; unset _vl_prev_path _vl_line _vl_k _vl_v
fi
true
