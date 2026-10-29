#!/usr/bin/env python3
"""Kho văn mẫu để đo check.py (human-writing).

  python3 -I corpus.py gen   [--out evals/corpus/ai] [--models a,b,c] [--parallel 3]
      Sinh văn AI "mặc định" bằng lệnh `agy` (Gemini, Claude, GPT-OSS qua Antigravity), không dặn giọng.
      Mỗi mẫu một file .md có frontmatter (model, genre, kind, lang, prompt). File đã có thì bỏ qua (chạy lại được).
  python3 -I corpus.py fetch [--manifest evals/corpus/manifest.json] [--cache evals/corpus/cache]
      Tải văn người từ nguồn công khai ghi trong manifest (Wikipedia tiếng Việt bản cũ, Wikisource) vào cache
      (gitignore), ghi sha256 vào manifest lần đầu, lần sau kiểm khớp. Văn người không commit, chỉ giữ hash.
  python3 -I corpus.py private [--cache evals/corpus/cache]
      Trích tin nhắn người dùng tự gõ trong lịch sử phiên Claude Code (~/.claude/projects) làm văn người,
      lọc văn dán, thay tên khách bằng bộ lọc anonkhach nếu có. Chỉ nằm trong cache.

Văn AI commit được (do mình sinh). Văn người chỉ nằm trong cache + hash, theo cách của avoid-ai-writing/corpus.
"""
import argparse, hashlib, html as htmlmod, json, os, re, subprocess, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------ gen
TOPICS = {
    "caption":  ("social",   "Viết một caption Facebook khoảng 120 chữ cho {t}.",
                 ["khóa học marketing online dành cho chủ shop nhỏ", "quán cà phê mới mở ở quận 7 có bánh mì chảo", "dịch vụ chụp ảnh gia đình dịp Tết"]),
    "ads":      ("social",   "Viết một bài quảng cáo Facebook khoảng 200 chữ cho {t}.",
                 ["app quản lý thời gian cho sinh viên", "lớp học bơi cho trẻ 5 đến 10 tuổi", "gói bảo dưỡng xe máy tận nhà"]),
    "email":    ("email",    "Viết một email khoảng 150 chữ gửi khách hàng để {t}.",
                 ["báo đơn hàng giao trễ hai ngày và đề nghị cách bù", "mời gia hạn gói dịch vụ sắp hết hạn", "trả lời khiếu nại về sản phẩm bị lỗi"]),
    "report":   ("report",   "Viết một báo cáo nội bộ khoảng 300 chữ về {t}.",
                 ["kết quả chiến dịch quảng cáo tháng 9 của một shop quần áo", "tình hình tuyển dụng quý 3 của một công ty 40 người", "đề xuất đổi phần mềm kế toán"]),
    "script":   ("script",   "Viết kịch bản video TikTok 60 giây về {t}.",
                 ["ba sai lầm khi chạy quảng cáo Facebook", "cách pha cà phê phin ngon tại nhà", "một ngày của nhân viên marketing"]),
    "academic": ("academic", "Viết một bài giải thích khoảng 300 chữ cho sinh viên năm nhất về {t}.",
                 ["đạo hàm là gì và dùng để làm gì", "hạng của ma trận", "thuật toán sắp xếp nổi bọt"]),
}
TOPICS_EN = {
    "caption":  ("social", "Write a 120-word Facebook caption for {t}.", ["an online marketing course for small shop owners"]),
    "email":    ("email",  "Write a 150-word email to a customer to {t}.", ["apologise for a two-day delivery delay and offer a remedy"]),
    "report":   ("report", "Write a 300-word internal report on {t}.", ["the results of a September ad campaign for a clothing shop"]),
    "academic": ("academic", "Write a 300-word explanation for first-year students of {t}.", ["what a derivative is and what it is used for"]),
}


def slug(s):
    s = s.lower()
    s = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", s); s = re.sub(r"[èéẹẻẽêềếệểễ]", "e", s); s = re.sub(r"[ìíịỉĩ]", "i", s)
    s = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", s); s = re.sub(r"[ùúụủũưừứựửữ]", "u", s); s = re.sub(r"[ỳýỵỷỹ]", "y", s); s = s.replace("đ", "d")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:48]


def run_agy(model, prompt, timeout=240):
    cmd = ["agy", "-p", prompt + "\n\n(Trả lời trực tiếp bằng văn bản thuần, không dùng công cụ, không hỏi lại.)", "--model", model, "--output-format", "text", "--print-timeout", f"{timeout - 20}s"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    out = (r.stdout or "").strip()
    if r.returncode != 0 or len(out.split()) < 30:
        return None, (r.stderr or out)[-300:]
    return out, ""


def gen(a):
    out = os.path.join(ROOT, a.out)
    os.makedirs(out, exist_ok=True)
    jobs = []
    for lang, table in (("vi", TOPICS), ("en", TOPICS_EN)):
        for genre, (kind, tpl, topics) in table.items():
            for t in topics:
                for model in (a.models if lang == "vi" else a.models[:1]):
                    name = f"{lang}--{genre}--{slug(t)}--{model}.md"
                    path = os.path.join(out, name)
                    if os.path.exists(path):
                        continue
                    jobs.append((path, model, genre, kind, lang, tpl.format(t=t)))
    print(f"gen: {len(jobs)} mẫu cần sinh, {a.parallel} luồng", file=sys.stderr)

    def work(job):
        path, model, genre, kind, lang, prompt = job
        t0 = time.time()
        text, err = run_agy(model, prompt)
        if text is None:
            print(f"  LỖI {os.path.basename(path)}: {err}", file=sys.stderr)
            return False
        fm = {"model": model, "genre": genre, "kind": kind, "lang": lang, "prompt": prompt,
              "generated_at": time.strftime("%Y-%m-%d"), "label": "ai"}
        with open(path, "w", encoding="utf-8") as f:
            f.write("---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in fm.items()) + "---\n\n" + text + "\n")
        print(f"  ok {os.path.basename(path)} ({time.time() - t0:.0f}s, {len(text.split())} chữ)", file=sys.stderr)
        return True

    with ThreadPoolExecutor(max_workers=a.parallel) as ex:
        res = list(ex.map(work, jobs))
    print(f"gen xong: {sum(res)}/{len(jobs)} thành công", file=sys.stderr)


# ------------------------------------------------------------------ fetch
def sha(b):
    return hashlib.sha256(b).hexdigest()


def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": "human-writing-skill/2.1 (corpus fetch for local tests; contact: github.com/TTN0623)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def clean_wikitext(w):
    w = re.sub(r"<ref[^>]*/>", "", w); w = re.sub(r"<ref[^>]*>.*?</ref>", "", w, flags=re.S)
    w = re.sub(r"\{\{[^{}]*\}\}", "", w); w = re.sub(r"\{\{[^{}]*\}\}", "", w)
    w = re.sub(r"\[\[(?:Tập tin|File|Hình|Image):[^\]]*\]\]", "", w, flags=re.I)
    w = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", w); w = re.sub(r"\[\[([^\]]*)\]\]", r"\1", w)
    w = re.sub(r"\[https?://\S+ ([^\]]*)\]", r"\1", w); w = re.sub(r"<[^>]+>", "", w)
    w = re.sub(r"'{2,}", "", w); w = re.sub(r"^==+\s*(.*?)\s*==+$", r"## \1", w, flags=re.M)
    w = re.sub(r"^\s*\|.*$", "", w, flags=re.M); w = re.sub(r"^[*#:;].*$", "", w, flags=re.M)
    w = htmlmod.unescape(w).replace("\u00a0", " ")
    w = re.sub(r"\n{3,}", "\n\n", w)
    return w.strip()


def strip_ws_header(html):
    """Bỏ khung đầu trang Wikisource (tên, năm, ghi chú trích Wikipedia): chỉ giữ phần truyện."""
    k = html.find('class="prose"')
    if k >= 0:
        return html[html.rfind("<", 0, k):]
    k = html.find('id="headerContainer"')
    if k >= 0:
        e = html.find('class="ws-noexport"', k)
        if e >= 0:
            return html[:html.rfind("<", 0, k)] + html[html.rfind("<", 0, e):]
    return html


def cut_words(text, n, max_lines=400):
    """Cắt còn n chữ nhưng giữ xuống dòng (bản 2.1.0 trở về trước nối hết thành một dòng)."""
    out, k = [], 0
    for line in text.split("\n")[:max_lines]:
        ws = line.split()
        if k + len(ws) > n:
            if ws[: n - k]:
                out.append(" ".join(ws[: n - k]))
            break
        out.append(" ".join(ws)); k += len(ws)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def fetch(a):
    mpath = os.path.join(ROOT, a.manifest); cache = os.path.join(ROOT, a.cache)
    os.makedirs(cache, exist_ok=True)
    m = json.load(open(mpath, encoding="utf-8"))
    changed = False
    for d in m["documents"]:
        if d.get("source") != "public":
            continue
        path = os.path.join(cache, d["file"])
        if os.path.exists(path):
            b = open(path, "rb").read()
            if d.get("sha256") and sha(b) != d["sha256"]:
                print(f"KHÁC HASH: {d['file']} (đã đổi so với manifest)", file=sys.stderr); sys.exit(2)
            continue
        try:
            raw = http(d["url"]).decode("utf-8", "replace")
        except Exception as e:
            print(f"  không tải được {d['id']}: {e}", file=sys.stderr); continue
        if d.get("format") == "wikitext":
            text = clean_wikitext(raw)
        elif d.get("format") == "mw-html":
            html = json.loads(raw)["parse"]["text"]
            if isinstance(html, dict):
                html = html.get("*", "")
            html = strip_ws_header(html)
            html = re.sub(r"<(script|style|table)[^>]*>.*?</\1>", "", html, flags=re.S | re.I)
            html = re.sub(r"<(span|div)[^>]*class=\"[^\"]*(pagenum|ws-noexport|noprint|mw-editsection|reference)[^\"]*\"[^>]*>.*?</\1>", "", html, flags=re.S | re.I)
            html = re.sub(r"</(p|div|h\d|li|br)>", "\n\n", html, flags=re.I)
            text = re.sub(r"<[^>]+>", "", html)
            text = htmlmod.unescape(text).replace("\u00a0", " ")
            text = re.sub(r"[ \t]+", " ", text); text = re.sub(r"\n{3,}", "\n\n", text).strip()
        else:
            text = raw
        if d.get("max_words"):
            text = cut_words(text, d["max_words"])
        body = f"---\nid: {d['id']}\nlabel: human\nkind: {d.get('kind','doc')}\nlang: {d.get('lang','vi')}\nsource: {d['url']}\nlicense: {d.get('license','')}\n---\n\n{text}\n"
        open(path, "w", encoding="utf-8").write(body)
        h = sha(body.encode("utf-8"))
        if not d.get("sha256"):
            d["sha256"] = h; changed = True
        elif d["sha256"] != h:
            print(f"KHÁC HASH sau khi tải lại: {d['id']}", file=sys.stderr)
        print(f"  ok {d['file']} ({len(text.split())} chữ)", file=sys.stderr)
        time.sleep(3)
    if changed:
        json.dump(m, open(mpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("manifest: đã ghi sha256 mới", file=sys.stderr)


# ------------------------------------------------------------------ private
VI = re.compile(r"[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệịỉĩọỏõốồổỗộớờởỡợụủũứừửữựỳỵỷỹ]")
# Tin nhắn do máy hoặc phiên Claude khác gửi vào kênh "user": không phải văn người
MACHINE = re.compile(r"another Claude session|Cross-session|idle notice|harness|^\s*\[|teammate|task-notification|Artifact comment|Co-Authored|hookSpecificOutput|SendMessage|\[Agent |\bsubagent\b|\[Artifact|^\s*#{1,3} |claude\.ai/|\bTL;DR\b|^\s*(STATUS|DONE|NEXT)\b", re.I | re.M)
# Tin Tài dán lại lời Claude rồi trả lời xen ("câu của Claude --> ý của Tài"), hoặc dán nguyên báo cáo AI: văn lẫn, bỏ cả tin
QUOTED = re.compile(r"-->|\u2014|\u2192|USER CONFIRMED")
NOISE = re.compile(r"(agy-run|codex|python3|~/|\.py\b|\.mjs\b|--[a-z]|https?://|\$\(|\bgit\b|npm|launchctl|\bPID\b|\.json\b|\.jsonl\b)")


def private(a):
    import glob
    cache = os.path.join(ROOT, a.cache, "human-private"); os.makedirs(cache, exist_ok=True)
    anon = os.path.expanduser(os.environ.get("HW_ANON_SCRIPT", "~/.kp3-tools/bin/loc-ten-khach.py"))  # script ẩn tên khách, không có thì bỏ qua
    seen, keep = set(), []
    for p in sorted(glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))):
        try:
            for line in open(p, encoding="utf-8", errors="ignore"):
                if '"type":"user"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                c = (d.get("message") or {}).get("content")
                if isinstance(c, list):
                    c = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
                if not isinstance(c, str):
                    continue
                s = c.strip()
                if s.startswith("<") or "system-reminder" in s or "<pasted_content" in s or "<ide_selection" in s:
                    continue
                if MACHINE.search(s) or QUOTED.search(s):
                    continue
                w = len(s.split())
                if not (60 <= w <= 350) or len(VI.findall(s)) < 8 or s.count("\n") > 12:
                    continue
                if re.search(r"^#{1,6} |\*\*|```|^\|.*\||^\s*[-*] |\{\"", s, re.M) or len(NOISE.findall(s)) > 1:
                    continue
                h = hashlib.md5(s[:200].encode()).hexdigest()
                if h in seen:
                    continue
                seen.add(h); keep.append((d.get("timestamp", ""), s))
        except Exception:
            pass
    keep.sort()
    n = 0
    for ts, s in keep:
        if os.path.exists(anon):
            try:
                s = subprocess.run([sys.executable, "-I", anon], input=s, capture_output=True, text=True, timeout=20).stdout or s
            except Exception:
                pass
        body = f"---\nid: private-{n:04d}\nlabel: human\nkind: email\nlang: vi\nsource: tin nhắn người dùng tự gõ trong phiên Claude Code {ts[:10]}\n---\n\n{s}\n"
        open(os.path.join(cache, f"private-{n:04d}.md"), "w", encoding="utf-8").write(body); n += 1
    print(f"private: {n} mẫu vào {cache}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen"); g.add_argument("--out", default="evals/corpus/ai")
    g.add_argument("--models", default="gemini-3.8-flash-medium,claude-sonnet-4-6,gpt-oss-120b-medium"); g.add_argument("--parallel", type=int, default=3)
    f = sub.add_parser("fetch"); f.add_argument("--manifest", default="evals/corpus/manifest.json"); f.add_argument("--cache", default="evals/corpus/cache")
    p = sub.add_parser("private"); p.add_argument("--cache", default="evals/corpus/cache")
    a = ap.parse_args()
    if a.cmd == "gen":
        a.models = [m.strip() for m in a.models.split(",") if m.strip()]; gen(a)
    elif a.cmd == "fetch":
        fetch(a)
    else:
        private(a)


if __name__ == "__main__":
    main()
