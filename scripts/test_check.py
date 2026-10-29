#!/usr/bin/env python3
"""Bộ kiểm thử cho check.py: đo trên kho văn mẫu và chạy ca đơn vị.

Dùng:
  python3 -I test_check.py                      # ca đơn vị evals/cases + bảng đo kho (exit 1 nếu ca nào sai)
  python3 -I test_check.py --impl path/check_v1.py   # đo một bản check.py khác (so bản cũ, bản mới)
  python3 -I test_check.py --save-baseline      # ghi evals/baseline.json
  python3 -I test_check.py --baseline           # so với evals/baseline.json, báo mã nào tăng bắt nhầm
  python3 -I test_check.py --codes              # bảng từng mã: hit/1000 chữ ở AI và ở người

Kho văn:
  evals/corpus/ai/            văn AI sinh sẵn (commit)                        label: ai
  evals/corpus/cache/         văn người tải về theo manifest + kho riêng       label: human (gitignore)
  evals/cases/*.md            ca đơn vị, frontmatter: kind, expect_errors, expect_no, expect_warnings, max_score, min_score

Ca đơn vị sai = exit 1. Số đo kho chỉ in ra; so baseline chỉ cảnh báo khi bắt nhầm ở người tăng.
"""
import argparse
import glob
import importlib.util
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EVALS = os.path.join(ROOT, "evals")


def load_impl(path):
    spec = importlib.util.spec_from_file_location("check_impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_one(mod, raw, path):
    """Chạy một file qua bản check đã nạp; bản 1 không có run()/score nên tự ghép."""
    if hasattr(mod, "run"):
        return mod.run(raw, path)
    kind = "social" if any(k in path for k in ("caption", "ads", "social")) else "doc"
    errs, warns, words = mod.check(raw, kind)
    return {"errors": errs, "warnings": warns, "words": words, "score": None, "kind": kind}


def corpus_files():
    out = []
    for p in sorted(glob.glob(os.path.join(EVALS, "corpus", "ai", "*.md"))):
        out.append(("ai", p))
    for p in sorted(glob.glob(os.path.join(EVALS, "corpus", "cache", "**", "*.md"), recursive=True)):
        out.append(("human", p))
    return out


def measure(mod):
    rows = {"ai": [], "human": []}
    for label, p in corpus_files():
        raw = open(p, encoding="utf-8").read()
        r = run_one(mod, raw, p)
        r["file"] = p
        rows[label].append(r)
    return rows


def summarize(rows):
    s = {}
    for label, rs in rows.items():
        if not rs:
            continue
        words = sum(r["words"] for r in rs)
        with_err = sum(1 for r in rs if r["errors"])
        scores = [r["score"] for r in rs if r["score"] is not None]
        per_code = {}
        for r in rs:
            for f in r["errors"]:
                per_code.setdefault(f["code"], [0, 0])[0] += 1
            for f in r["warnings"]:
                per_code.setdefault(f["code"], [0, 0])[1] += 1
        s[label] = {"files": len(rs), "words": words, "files_with_error": with_err,
                    "pct_files_with_error": round(100 * with_err / len(rs), 1),
                    "errors_per_1000w": round(1000 * sum(len(r["errors"]) for r in rs) / max(words, 1), 2),
                    "warns_per_1000w": round(1000 * sum(len(r["warnings"]) for r in rs) / max(words, 1), 2),
                    "score_median": statistics.median(scores) if scores else None,
                    "score_mean": round(statistics.mean(scores), 1) if scores else None,
                    "pct_score_ge_50": round(100 * sum(1 for x in scores if x >= 50) / len(scores), 1) if scores else None,
                    "pct_score_lt_20": round(100 * sum(1 for x in scores if x < 20) / len(scores), 1) if scores else None,
                    "per_code": {k: {"errors": v[0], "warnings": v[1], "per_1000w": round(1000 * (v[0] + v[1]) / max(words, 1), 2)} for k, v in sorted(per_code.items())}}
    return s


def print_summary(s, title):
    print(f"\n== {title}")
    print(f"{'kho':<7}{'file':>6}{'chữ':>8}{'%file LỖI':>11}{'LỖI/1k':>8}{'CB/1k':>8}{'điểm TV':>9}{'%≥50':>7}{'%<20':>7}")
    for label in ("ai", "human"):
        if label not in s:
            continue
        x = s[label]
        med = "-" if x["score_median"] is None else f"{x['score_median']:.0f}"
        ge = "-" if x["pct_score_ge_50"] is None else f"{x['pct_score_ge_50']:.0f}"
        lt = "-" if x["pct_score_lt_20"] is None else f"{x['pct_score_lt_20']:.0f}"
        print(f"{label:<7}{x['files']:>6}{x['words']:>8}{x['pct_files_with_error']:>11}{x['errors_per_1000w']:>8}{x['warns_per_1000w']:>8}{med:>9}{ge:>7}{lt:>7}")


def print_codes(s):
    codes = sorted(set(s.get("ai", {}).get("per_code", {})) | set(s.get("human", {}).get("per_code", {})))
    print(f"\n{'mã':<16}{'AI lỗi':>7}{'AI cb':>7}{'AI/1k':>7}{'Ng lỗi':>8}{'Ng cb':>7}{'Ng/1k':>7}  tỉ lệ AI/Ng")
    for c in codes:
        a = s.get("ai", {}).get("per_code", {}).get(c, {"errors": 0, "warnings": 0, "per_1000w": 0})
        h = s.get("human", {}).get("per_code", {}).get(c, {"errors": 0, "warnings": 0, "per_1000w": 0})
        ratio = "∞" if h["per_1000w"] == 0 and a["per_1000w"] > 0 else (f"{a['per_1000w'] / h['per_1000w']:.1f}" if h["per_1000w"] else "-")
        flag = "  ← bắt nhầm người" if h["errors"] > 0 else ""
        print(f"{c:<16}{a['errors']:>7}{a['warnings']:>7}{a['per_1000w']:>7}{h['errors']:>8}{h['warnings']:>7}{h['per_1000w']:>7}  {ratio}{flag}")


def parse_fm(raw):
    fm = {}
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        for l in raw[3:end].split("\n"):
            if ":" in l:
                k, v = l.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def run_cases(mod):
    """Ca đơn vị: mỗi file evals/cases/*.md nêu kỳ vọng trong frontmatter."""
    fails, n = [], 0
    for p in sorted(glob.glob(os.path.join(EVALS, "cases", "*.md"))):
        raw = open(p, encoding="utf-8").read()
        fm = parse_fm(raw)
        n += 1
        r = run_one(mod, raw, p)
        if fm.get("kind") and hasattr(mod, "run"):
            r = mod.run(raw, p, fm["kind"], fm.get("voice") or None)
        got_e = {f["code"] for f in r["errors"]}
        got_w = {f["code"] for f in r["warnings"]}
        got = got_e | got_w
        name = os.path.basename(p)
        for c in [c.strip() for c in fm.get("expect_errors", "").split(",") if c.strip()]:
            if c not in got_e:
                fails.append(f"{name}: thiếu LỖI {c} (có: {sorted(got_e)})")
        for c in [c.strip() for c in fm.get("expect_warnings", "").split(",") if c.strip()]:
            if c not in got:
                fails.append(f"{name}: thiếu CẢNH BÁO {c} (có: {sorted(got)})")
        for c in [c.strip() for c in fm.get("expect_no", "").split(",") if c.strip()]:
            if c in got or (c.split("-")[0] in {g.split("-")[0] for g in got} and "-" not in c):
                fails.append(f"{name}: không được bắt {c} nhưng có {[f['found'] for f in r['errors'] + r['warnings'] if f['code'].startswith(c)]}")
        if fm.get("expect_clean") == "true" and (got_e or got_w):
            fails.append(f"{name}: phải sạch nhưng có {sorted(got)}")
        if fm.get("expect_no_errors") == "true" and got_e:
            fails.append(f"{name}: không được có LỖI nhưng có {sorted(got_e)}: {[f['found'] for f in r['errors']]}")
        if fm.get("max_score") and r["score"] is not None and r["score"] > int(fm["max_score"]):
            fails.append(f"{name}: điểm {r['score']} > {fm['max_score']}")
        if fm.get("min_score") and r["score"] is not None and r["score"] < int(fm["min_score"]):
            fails.append(f"{name}: điểm {r['score']} < {fm['min_score']}")
    return n, fails


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--impl", default=os.path.join(HERE, "check.py"))
    ap.add_argument("--save-baseline", action="store_true")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--codes", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-cases", action="store_true")
    a = ap.parse_args()
    mod = load_impl(a.impl)

    rc = 0
    if not a.no_cases and os.path.isdir(os.path.join(EVALS, "cases")):
        n, fails = run_cases(mod)
        print(f"Ca đơn vị: {n - len({f.split(':')[0] for f in fails})}/{n} đạt")
        for f in fails:
            print("  SAI", f)
        if fails:
            rc = 1

    rows = measure(mod)
    s = summarize(rows)
    if a.json:
        print(json.dumps(s, ensure_ascii=False, indent=1))
    else:
        print_summary(s, f"kho văn mẫu, bản {getattr(mod, 'VERSION', '?')} ({os.path.relpath(a.impl, ROOT)})")
        if a.codes:
            print_codes(s)

    bpath = os.path.join(EVALS, "baseline.json")
    if a.save_baseline:
        json.dump(s, open(bpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nĐã ghi {os.path.relpath(bpath, ROOT)}")
    elif a.baseline and os.path.exists(bpath):
        b = json.load(open(bpath, encoding="utf-8"))
        worse = []
        hb, hn = b.get("human", {}), s.get("human", {})
        if hn.get("errors_per_1000w", 0) > hb.get("errors_per_1000w", 0) + 0.05:
            worse.append(f"LỖI/1000 chữ ở văn người tăng {hb.get('errors_per_1000w')} → {hn.get('errors_per_1000w')}")
        for c, v in hn.get("per_code", {}).items():
            old = hb.get("per_code", {}).get(c, {"errors": 0})
            if v["errors"] > old["errors"]:
                worse.append(f"{c}: LỖI ở văn người {old['errors']} → {v['errors']}")
        ab, an = b.get("ai", {}), s.get("ai", {})
        if an.get("pct_files_with_error", 0) < ab.get("pct_files_with_error", 0) - 5:
            worse.append(f"% file AI có LỖI giảm {ab.get('pct_files_with_error')} → {an.get('pct_files_with_error')}")
        print("\nSo baseline:", "không xấu đi." if not worse else "")
        for w in worse:
            print("  XẤU ĐI", w)
        if worse:
            rc = 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
