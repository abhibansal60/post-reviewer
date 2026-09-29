# Usage: python3 score.py <variant>  - per-case table, means with 95% CI over cases, rep noise, cost/latency.
import json, statistics as st, math, collections, sys
V = sys.argv[1] if len(sys.argv) > 1 else "baseline"
D = f".claude/hillclimb/reviewer/{V}"
rows = [json.loads(l) for l in open(f"{D}/results.jsonl")]
by = collections.defaultdict(list)
for r in rows: by[r["prompt_id"]].append(r)
def verdict(k, rep): return json.loads(json.load(open(f"{D}/traces/{k}_rep{rep}.json"))[-1]["content"])["verdict"]
print("case  recall        verdict_ok  clean   verdicts")
for k in sorted(by):
    g = [r["grade"] for r in by[k]]
    print(f"{k:4}  {[round(x['flag_recall'], 2) for x in g]}  {[x['verdict_ok'] for x in g]}  {[x['clean'] for x in g]}  {[verdict(k, r['rep']) for r in by[k]]}")
for m in ("flag_recall", "verdict_ok", "clean"):
    per = [st.mean(r["grade"][m] for r in by[k]) for k in by]
    print(f"{m}: {st.mean(per):.3f} ± {1.96 * st.stdev(per) / math.sqrt(len(per)):.3f}")
d = [by[k][0]["grade"]["flag_recall"] - by[k][1]["grade"]["flag_recall"] for k in by if len(by[k]) > 1]
if d: print(f"rep-to-rep recall sd per case: {st.pstdev(d) / math.sqrt(2):.3f}")
print(f"reviewer list $/case median {st.median(r['list_cost_usd'] for r in rows):.3f}, latency median {st.median(r['latency_s'] for r in rows):.0f}s, n={len(rows)}")
