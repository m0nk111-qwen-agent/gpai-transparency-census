#!/usr/bin/env python3
"""gpai-transparency-census: snapshot + diff tool for the Art. 53(1)(d) provider census.

Data model: one JSON object per line in data/providers.jsonl (see README.md).
Snapshots are dated copies of that file under snapshots/YYYY-MM-DD.jsonl.
A diff compares two snapshots and reports per-provider changes:
  - added / removed providers
  - field-level changes (tier, url, summary_location, template_sections, doc_date, models_checked)

Usage:
  python3 census.py snapshot [--date YYYY-MM-DD]   # writes snapshots/<date>.jsonl
  python3 census.py diff <old.jsonl> <new.jsonl>   # table + JSON diff
  python3 census.py stats <snapshot.jsonl>         # tier counts + summary
"""
import argparse, json, sys
from datetime import date, datetime

FIELDS = ["tier", "url", "summary_location", "template_sections", "doc_date", "models_checked"]


def load(path):
    rows = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            rows[r["provider"]] = r
    return rows


def snapshot(args):
    d = args.date or date.today().isoformat()
    datetime.strptime(d, "%Y-%m-%d")  # validate
    rows = load(args.data)
    out = f"snapshots/{d}.jsonl"
    with open(out, "w") as f:
        for p in sorted(rows):
            f.write(json.dumps(rows[p], ensure_ascii=False, sort_keys=True) + "\n")
    print(f"wrote {out} ({len(rows)} providers)")


def diff(args):
    old, new = load(args.old), load(args.new)
    d = {
        "old": args.old, "new": args.new,
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "changed": [], "unchanged": sorted(set(old) & set(new) - set()),
    }
    d["unchanged"] = sorted(set(old) & set(new))
    lines = []
    for p in sorted(set(old) | set(new)):
        if p in d["added"] or p in d["removed"] or p not in old or p not in new:
            continue
        o, n = old[p], new[p]
        changes = {k: {"old": o.get(k), "new": n.get(k)} for k in FIELDS if o.get(k) != n.get(k)}
        if changes:
            d["changed"].append({"provider": p, "changes": changes})
            lines.append(f"{p}:")
            for k, v in changes.items():
                ov, nv = v["old"], v["new"]
                if isinstance(ov, (list, type(None))) or isinstance(nv, (list, type(None))):
                    ov = json.dumps(ov) if not isinstance(ov, str) else ov
                    nv = json.dumps(nv) if not isinstance(nv, str) else nv
                lines.append(f"  {k}: {ov} -> {nv}")
    d["n_added"], d["n_removed"], d["n_changed"] = len(d["added"]), len(d["removed"]), len(d["changed"])
    d["n_unchanged"] = len(d["unchanged"])
    print("\n".join(lines) if lines else "no field-level changes")
    if args.json:
        print(json.dumps(d, indent=1))


def stats(args):
    rows = load(args.snapshot)
    from collections import Counter
    c = Counter(r["tier"] for r in rows.values())
    print(f"snapshot {args.snapshot}: {len(rows)} providers")
    order = ["T3", "T3-candidate", "T2+", "T2", "T2-gated", "T1-2", "UNVERIFIED"]
    seen = [t for t in order if t in c] + sorted(t for t in c if t not in order)
    for t in seen:
        print(f"  {t}: {c[t]}")
    t3 = [p for p, r in rows.items() if r["tier"] == "T3"]
    t3c = [p for p, r in rows.items() if r["tier"] == "T3-candidate"]
    print(f"  headline: {len(t3)} of {len(rows)} at T3 ({', '.join(sorted(t3))})")
    if t3c:
        print(f"  + {len(t3c)} T3-candidate ({', '.join(sorted(t3c))})")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("snapshot")
    s.add_argument("--data", default="data/providers.jsonl")
    s.add_argument("--date", default=None)
    s.set_defaults(fn=snapshot)
    s = sub.add_parser("diff")
    s.add_argument("old"); s.add_argument("new")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=diff)
    s = sub.add_parser("stats")
    s.add_argument("snapshot")
    s.set_defaults(fn=stats)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
