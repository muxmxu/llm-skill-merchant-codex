# tg-ask teardown

Script: `T="<tg-ask skill base directory>/scripts/tgask.py"`.

1. Show what exists: `python3 "$T" health` and `ls` of the state directory it
   reports under `setup`. Count open requests; if any are `sent` or
   `answered`, warn that their sessions will never get an answer.
2. Ask the human which level they want (skip the question when $ARGUMENTS
   already says it):
   - **stop** (default): stop the relay, make the hooks no-ops. History, token
     and allowlist stay; `tg-ask setup` brings it back in one step.
   - **purge**: also delete requests and hook event logs (`--purge`).
   - **forget-bot**: also delete the bot token and allowlist (`--forget-bot`).
     These files are shared with the official Telegram plugin; say so.
3. Run `python3 "$T" uninstall [--purge] [--forget-bot]` and verify:
   `tmux has-session -t tg-relay` must fail and `pgrep -f "tgask.py relay"`
   must print nothing.
4. Tell the human the steps only they can do, as applicable:
   - Remove the hooks entirely: `disable the tg-ask plugin in Codex`.
   - Retire the bot: `/revoke` (new token) or `/deletebot` in @BotFather.
