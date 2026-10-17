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

Cancel reasons: `close>2`, `runaway`, `superseded`, `mid`, `expiry`, `bias`, `evict`, `minTap5Ext`, `session`.
`bias` only applies when "Cancel sequences when bias flips" is on (off by default); bias otherwise just filters which direction new sequences spawn in, using its own longer pivot length (15).
Turn on **Debug mode** to see the reason next to each dead sequence and a stats table: counts, cancel reasons, and trade magnitude in R (avg win/loss, payoff ratio, profit factor, expectancy vs breakeven win rate, max drawdown, loss streak, MFE on stopped trades, long/short split) plus net points and net $ after `commissionPerSide` × 2 × `contracts`.

## Shadow filters
The model's own invalidation, a close beyond tap 2, is always enforced. Each
invented rule has a mode: **Off** (not applied), **Shadow** (never cancels; the
sequence is tagged, removed from the chart so the chart shows the Enforce view,
and keeps running hidden until it resolves) or **Enforce** (cancels).

| Filter | Checked | Default |
|---|---|---|
| `runaway` (tap 5 > `maxTap5Ext` zone heights past mid) | while tap 5 trails | Off |
| `expiry` (`expiryBars` after arming) | armed | Off |
| `superseded` (newer same-direction order arms) | arming | Off |
| `minZoneATR` / `maxZoneATR` (zone height vs ATR) | spawn | Shadow |
| `minTap5Ext` (tap 5 < 2 zone heights past mid) | arming | Shadow |
| `session` (skip fills NY 09:30–16:00 ET) | would-be fill bar | Shadow |

With superseded off, up to `maxArmedPerDir` (3) armed orders per direction get
pending lines; extra ones still count in stats and alerts.

**R:R flag.** Planned R:R at arming (`|target − entry| ÷ |entry − stop|`). Outside
`minRR`..`maxRR` (`maxRR` 0 = no upper bound) the order is not cancelled but
marked *optional*: faded dashed lines, entry text `Long 30472.50 (opt 1.2R)`.
Every armed order shows its R:R (`Short 30683.50 · 2.4R`); the `armed` alert carries
`"rr"` and `"optional"`.

**Daily loss limit.** Day starts 18:00 ET; only non-optional trades count.
Shadow compares no limit vs stopping after 2 or 3 losses. Enforce draws later
setups that day as optional (`limit`).

## Debug tables
Turn on **Debug mode**. Positions are inputs; a table that asks for a corner
already taken moves to the next free one. Text size defaults to tiny.

- **Stats** (chart view): counts, cancel reasons, magnitude in R, median R,
  expectancy without the top 5 wins, net $ after commissions, max concurrent open trades.
- **Filter impact** (all trades, shadow included): per filter and the `rr` flag,
  removed vs kept expectancy and a verdict for the whole sample and each half;
  then n / win / expectancy / median / ex-top-5 by session, tap 5 extension, zone
  height, bars arm→fill and planned R:R.
- **Exit variants** (chart trades): A tap 5 (the chart), B 1.5R, C 2R, D 3R,
  E/F tap 5 with breakeven at 1R / 1.5R MFE, G half off at 1R then breakeven and
  tap 5. Plus the daily-limit comparison and MFE / MAE excursion shares.

## Notes
- The engine only changes state on confirmed bars, and pivots are drawn back on
  their pivot bar after confirmation, so drawings do not repaint.
- Taps 3 and 5 slide right while they trail. If price runs past a locked tap 5 before the fill, tap 5 re-trails and the target moves (entry and stop stay); the order is cancelled as `runaway` once tap 5 is more than `maxTap5Ext` zone heights past the 50% line.
- Recommended setup: 1-minute chart with Bias timeframe = 5.
- The `cancelled` alert fires only for armed sequences (the ones with a limit order).
- Candidates that never reached tap 3 are deleted on cancel instead of faded,
  unless Debug mode is on.
- `alert()` messages fill in `symbol`/`tf` from `syminfo.ticker` / `timeframe.period`
  (TradingView placeholders such as `{{ticker}}` only work in `alertcondition` messages).
