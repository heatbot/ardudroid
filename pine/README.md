# 6-Tap indicator (Pine Script v6)

`6-tap.pine` is a TradingView overlay that detects and marks the 6-tap sequence
(taps 1–6, the supply/demand zone and its 50% line), colored by direction.

## Install
1. In TradingView, open the Pine Editor, paste the contents of `6-tap.pine`, and click **Add to chart**.
2. Alerts: create an alert on the indicator and choose **Any alert() function call**
   for the JSON messages (`armed`, `filled`, `invalidated`, `target`, `stop`),
   or pick one of the named `alertcondition` entries from the dropdown.

## Notes
- The engine only changes state on confirmed bars, and pivots are drawn back on
  their pivot bar after confirmation, so drawings do not repaint.
- Taps 3 and 5 track the extreme after their break until the next tap locks them,
  so those two labels can slide right while the sequence is still forming.
- `alert()` messages fill in `symbol`/`tf` from `syminfo.ticker` / `timeframe.period`
  (TradingView placeholders such as `{{ticker}}` only work in `alertcondition` messages).
- `invalidated` fires only for sequences that reached tap 3; unbroken tap 1/2
  candidates are dropped silently.
