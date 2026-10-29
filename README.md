# human-writing

Skill cho Claude Code để văn bản tiếng Việt (và tiếng Anh) đọc như người thật viết. Gồm bộ luật trong `SKILL.md`, script chấm điểm AI, hook chặn khi lưu file, giọng riêng cho từng kênh, và bộ kiểm thử đo trên kho văn AI và văn người. Bản 2.1.1, ngày 2026-10-29. Phần tiếng Anh ở cuối.

## Có gì trong đây

```
SKILL.md                 bộ luật, quy trình, bảng mã (Claude đọc file này)
scripts/check.py         chấm một hay nhiều file, in LỖI, CẢNH BÁO, điểm AI
scripts/hook.py          PostToolUse hook cho Write, Edit, MultiEdit
scripts/test_check.py    ca đơn vị + bảng đo trên kho
scripts/corpus.py        sinh văn AI, tải văn người, trích tin nhắn riêng
voices/*.toml            giọng riêng: mau-kenh, hoc-thuat, email-khach
LICENSE                  MIT cho bộ luật và script
evals/cases/             18 ca đơn vị có frontmatter kỳ vọng
evals/corpus/ai/         văn AI sinh mặc định (commit được)
evals/corpus/manifest.json  sha256 của văn người công khai, bản thân văn người không commit
evals/baseline.json      số đo chuẩn của bản hiện tại
evals/evals.json         7 kịch bản thử skill
references/              Wikipedia Signs of AI writing (kiểm kê + ánh xạ), humanizer, avoid-ai-writing
```

## Cài

1. Chép hoặc clone thư mục này vào `~/.claude/skills/human-writing`. Cần Python 3.11 trở lên (dùng `tomllib`), không cần thư viện ngoài.
2. Muốn hook chặn khi lưu file thì thêm vào `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -I \"$HOME/.claude/skills/human-writing/scripts/hook.py\"",
            "timeout": 15,
            "statusMessage": "human-writing: soát văn AI"
          }
        ]
      }
    ]
  }
}
```

Hook chỉ xét file `.md`, `.txt` trong thư mục sản phẩm (`outputs/`, `projects/`, `courses/`, `research/`, `team/`, `deliverables/`, `drafts/`). Sửa danh sách `SCOPE` và `SKIP` ở đầu `scripts/hook.py` cho hợp cây thư mục của bạn.

## Dùng

```bash
# một hay nhiều file, tự đoán thể loại và giọng theo frontmatter hoặc đường dẫn
python3 -I scripts/check.py bai.md
python3 -I scripts/check.py SKILL.md README.md CHANGELOG.md

# ép thể loại và giọng
python3 -I scripts/check.py caption.md --kind social --voice mau-kenh

# cả thư mục, bảng tóm tắt
python3 -I scripts/check.py --dir outputs/

# JSON cho máy đọc, exit 1 khi điểm từ 50
python3 -I scripts/check.py bai.md --json --fail-score 50

# đọc stdin
pbpaste | python3 -I scripts/check.py -
```

Kết quả có ba phần: dòng tóm tắt (số chữ, LỖI, CẢNH BÁO, điểm AI, kết luận), danh sách LỖI bắt buộc sửa, danh sách CẢNH BÁO sửa hoặc nêu lý do giữ. Mỗi dòng ghi mã, số dòng, đoạn bị bắt và cách thay.

Điểm AI: dưới 20 là sạch, 20 đến 49 là nghi, từ 50 là giống AI. Trên kho mẫu của bản này, 80 bài văn AI sinh mặc định có điểm trung vị 78, 142 bài văn người có điểm trung vị 0.

## Thể loại và giọng

Thể loại: `doc`, `social`, `script`, `email`, `academic`, `report`. Ghi `kind: social` trong frontmatter hoặc truyền `--kind`. Thể loại đổi ngưỡng emoji, hashtag, Markdown và bật vài luật riêng (ví dụ câu hỏi móc rồi trấn an là LỖI ở social, chỉ là cảnh báo ở tài liệu).

Giọng: một file TOML trong `voices/`. Giọng được nới nhóm CẢNH BÁO bằng `allow`, thêm cụm cấm bằng `[[ban]]`, cụm bắt buộc bằng `[[require]]`. Giọng không được nới nhóm LỖI. Tạo giọng mới bằng cách chép một file có sẵn rồi thêm một ca trong `evals/cases/`.

Hai chỉ thị viết trong file khi cần: `<!-- human-writing: off -->` bỏ qua cả file, `<!-- hw-allow: B5-NEG -->` cho phép mã nêu tên. Chỉ thị nằm trong code chỉ là ví dụ, không tính.

## Kiểm thử và kho văn

```bash
python3 -I scripts/test_check.py              # 18 ca đơn vị + bảng đo
python3 -I scripts/test_check.py --codes      # từng mã bắt bao nhiêu ở AI và người
python3 -I scripts/test_check.py --baseline   # so với evals/baseline.json
python3 -I scripts/corpus.py fetch            # tải văn người theo manifest (cần mạng)
python3 -I scripts/corpus.py gen --parallel 2 # sinh thêm văn AI (cần lệnh agy)
```

Luật thêm mã mới: thêm ở mức CẢNH BÁO, thêm một ca, chạy `--codes`; mã nào bắt văn người từ 1 LỖI hoặc tỉ lệ AI trên người dưới 3 thì hạ mức hoặc bỏ.

## Nguồn và giấy phép

- Bộ luật tiếng Việt, script, giọng mẫu và ca thử: giấy phép MIT, xem `LICENSE`. Giấy phép này không phủ thư mục `references/`, phần đó theo giấy phép của từng nguồn bên dưới.
- `references/wikipedia-signs-full.md` trích và kiểm kê [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), giấy phép CC BY-SA 4.0.
- `references/upstream/humanizer/` là blader/humanizer 3.1.0, giấy phép MIT.
- `references/upstream/avoid-ai-writing/` là conorbronsdon/avoid-ai-writing 3.38.0, giấy phép MIT, giữ nguyên LICENSE và NOTICE.
- Văn người trong kho đo không nằm trong kho này. Phần công khai (Wikipedia tiếng Việt bản cũ, Wikisource) có sha256 trong `evals/corpus/manifest.json` để tải lại đúng bản; phần tin nhắn riêng chỉ nằm trên máy tác giả.

## English summary

`human-writing` is a Claude Code skill that makes Vietnamese (and English) text read like a person wrote it. `SKILL.md` holds the rules; `scripts/check.py` scores a file from 0 to 100 (under 20 is clean, 50 and above reads like AI) across six kinds (`doc`, `social`, `script`, `email`, `academic`, `report`) and optional voice profiles in `voices/*.toml`. A PostToolUse hook blocks saves that still contain hard errors. `scripts/test_check.py` runs 18 unit cases and reports metrics on an AI corpus (generated, committed) and a human corpus (public Vietnamese Wikipedia and Wikisource, kept out of the repo and pinned by sha256, plus private messages that never leave the author's machine). Rules are kept only when they hit AI text far more often than human text. Code, rules and examples are MIT licensed (`LICENSE`); `references/` keeps its upstream licenses: Wikipedia Signs of AI writing (CC BY-SA 4.0), blader/humanizer (MIT), conorbronsdon/avoid-ai-writing (MIT).
