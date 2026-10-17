# 6-Tap indicator (Pine Script v6)

`6-tap.pine` is a TradingView overlay that detects and marks the 6-tap sequence
(taps 1–6, the supply/demand zone and its 50% line), colored by direction, with
at most one armed order per direction.

## Install
1. In TradingView, open the Pine Editor, paste the contents of `6-tap.pine`, and click **Add to chart**.
2. Alerts: create an alert on the indicator and choose **Any alert() function call**
   for the JSON messages (`armed`, `cancelled` with `reason`, `filled`, `target`, `stop`),
   or pick one of the named `alertcondition` entries from the dropdown.

## Sequence states
`0` await tap 3 → `1` await tap 4 → `2` await tap 5 → `3` tap 5 trailing →
`4` armed (limit order) → `5` in trade → `6` done or cancelled.

Cancel reasons: `close>2`, `stale`, `superseded`, `mid`, `expiry`, `bias`, `evict`.
Turn on **Debug mode** to see the reason next to each dead sequence and a stats table.

## Notes
- The engine only changes state on confirmed bars, and pivots are drawn back on
  their pivot bar after confirmation, so drawings do not repaint.
- Taps 3 and 5 slide right while they trail; tap 5 stops moving once it locks.
- The `cancelled` alert fires only for armed sequences (the ones with a limit order).
- Candidates that never reached tap 3 are deleted on cancel instead of faded,
  unless Debug mode is on.
- `alert()` messages fill in `symbol`/`tf` from `syminfo.ticker` / `timeframe.period`
  (TradingView placeholders such as `{{ticker}}` only work in `alertcondition` messages).
