# Nhật ký thay đổi

Theo dạng Keep a Changelog, số phiên bản theo SemVer. Mã luật (A1-CHAT, B5-NEG…) là mã do `scripts/check.py` in ra.

## 2.1.1 (2026-10-29)

Sửa cách `corpus.py fetch` làm sạch văn người tải về. Không đổi luật trong `check.py`.

- Lỗi cũ: khi cắt bài theo số chữ, script nối mọi dòng bằng dấu cách, nên cả 12 bài Wikipedia và Wikisource trong kho chỉ còn một dòng. Các luật đo theo dòng (lời thoại đầu dòng, nhịp câu, dòng ghi nguồn) chấm sai trên các bài này. Giờ `cut_words()` cắt đủ số chữ mà vẫn giữ xuống dòng.
- Giải mã đủ ký tự HTML bằng `html.unescape` cho cả hai đường tải (trước đây còn sót `&#32;`, `&nbsp;`, `&ast;`).
- Bỏ khung đầu trang Wikisource (tên, năm, ghi chú trích Wikipedia), chỉ giữ phần truyện. Hàm mới `strip_ws_header()`.
- Đã tải lại 12 bài và ghi sha256 mới vào manifest. Văn người dính LỖI từ 1,4% xuống 0,7%: bài Lão Hạc hết bắt nhầm, chỉ còn bài ma trận có gạch ngang dài chèn ý thật. CẢNH BÁO trên 1.000 chữ của văn người từ 0,62 lên 0,75 vì các luật đo theo dòng giờ mới chạy được trên 12 bài này. Văn AI không đổi.

## 2.1.0 (2026-10-29)

Tài duyệt từng trường hợp gạch ngang dài. D1-DASH giờ cho qua các chỗ gạch là ký hiệu, vẫn bắt chỗ gạch nối câu.

- Được phép: mũi tên, khoảng số (gạch dài hay gạch ngắn vừa, có hay không có dấu cách), số âm, ô trống trong bảng, dòng ghi nguồn ngắn sau trích dẫn, lời thoại đầu dòng trong kịch bản và truyện.
- Vẫn bắt: bảng giá kiểu tên rồi gạch rồi giá (kể cả gạch ngắn vừa, bản cũ để lọt), tiêu đề có phần phụ, câu ngắt giữa chừng, cặp gạch chèn ý, gạch nối hai vế câu, văn tiếng Anh. Tên riêng gốc có gạch thì đổi sang gạch ngắn.
- File truyện nhận theo đường dẫn (`truyen`, `story`, `tieu-thuyet`) hoặc frontmatter `the-loai: truyen`, `genre: story`. Hàm mới `is_story()`, hook truyền cờ này vào `check()`.
- Thêm ca 16 (các chỗ được phép), 17 (các chỗ vẫn bắt), 18 (lời thoại trong kịch bản). Văn AI: LỖI trên 1.000 chữ từ 9,59 lên 10,04, điểm trung vị từ 76 lên 78. Văn người giữ 1,4%.

## 2.0.1 (2026-10-29)

- D1-DASH cho phép gạch ngang dài dùng làm mũi tên: `—>`, `–>`, `<—`. Máy Mac tự đổi `-->` thành dạng này khi gõ, và người viết dùng nó để trả lời xen từng ý. Gạch ngang dài nối câu vẫn là LỖI.
- Thêm ca `evals/cases/15-mui-ten.md`. Số đo trên kho không đổi.

## 2.0.0 (2026-10-29)

Bản viết lại lớn: từ một bảng luật tự soát thành bộ công cụ có số đo. Mọi ngưỡng được đo trên kho văn AI sinh thử và kho văn người thật (`evals/`), và mọi mã trong SKILL.md khớp với mã script in ra.

### Thêm

- Điểm AI 0 đến 100 cho mỗi file: tính từ mật độ LỖI (nặng gấp ba) và CẢNH BÁO trên số chữ, tối thiểu 80 chữ để bài ngắn không bị phạt oan. Kết luận `sạch` (dưới 20), `nghi` (20 đến 49), `giống AI` (từ 50).
- Sáu thể loại `doc`, `social`, `script`, `email`, `academic`, `report`, đọc từ frontmatter `kind:`, cờ `--kind`, hoặc đoán theo đường dẫn. Thể loại đổi ngưỡng emoji, hashtag, Markdown và bật tắt vài luật.
- Giọng riêng trong `voices/*.toml`: `mau-kenh` (mẫu), `hoc-thuat`, `email-khach`; giọng thương hiệu riêng để ngoài repo. Mỗi giọng có `emoji_max`, `hashtag_max`, `allow` (chỉ nới CẢNH BÁO), `promo_extra`, bảng `[[ban]]` và `[[require]]` với mã `V-`.
- Hai chỉ thị trong file: `<!-- human-writing: off -->` và `<!-- hw-allow: MÃ -->`. Chỉ thị nằm trong khối code hoặc nháy đơn là ví dụ, không tính.
- Mã mới: A7-PREAMBLE (câu mào đầu của chatbot), B10-SKELETON, B11-QHOOK (câu hỏi móc rồi trấn an, LỖI ở social, script, email), B12-REASSURE, B13-CAPSLINE, B14-CORRECT (khung đính chính cho ý không ai nêu, dấu hiệu mô hình giữa 2026), B15-TEMPLATE, C2-SUM, C13-MOTIV, C16-TREND, C17-CS (giọng chăm sóc khách hàng theo mẫu, từ 3 câu là LỖI), C18-EN, C19-WRAP, D10-EMOJIBULLET, D11-NPLIST, D12-MARKDOWN, D13-QHEAD.
- C10-PROMO chia tầng: 2 từ một đoạn là CẢNH BÁO; 3 từ và từ 2% số chữ của đoạn, hoặc từ 3 từ mỗi 100 chữ cả bài, là LỖI.
- Cờ dòng lệnh: `--kind`, `--voice`, `--json`, `--dir` (bảng cả thư mục), `--fail-score N` (exit 1 khi điểm từ N), đọc stdin bằng `-`, nhận nhiều file một lần. Không có `--voice` thì đọc `voice:` trong frontmatter, giống hook.
- Hook `scripts/hook.py` bản 2: Write quét cả file và báo điểm, Edit chỉ quét đoạn mới và chỉ ép LỖI. Phạm vi `outputs/`, `projects/`, `courses/`, `research/`, `team/`, `deliverables/`, `drafts/`; bỏ `.claude/`, `evals/corpus/`.
- Bộ kiểm `scripts/test_check.py`: 14 ca đơn vị trong `evals/cases/` (frontmatter `expect_errors`, `expect_warnings`, `expect_no`, `expect_clean`, `max_score`, `min_score`), bảng đo trên kho, `--codes`, `--baseline`, `--save-baseline`, `--impl` để so hai bản script.
- Kho văn `scripts/corpus.py`: `gen` sinh văn AI mặc định qua `agy` (Gemini, Claude, GPT-OSS; 80 bài, 6 thể loại, 2 ngôn ngữ), `fetch` tải văn người công khai theo `manifest.json` có sha256, `private` trích tin nhắn tự gõ. Văn người chỉ nằm trong `evals/corpus/cache/` (gitignore); phần công khai có sha256 trong `manifest.json`, tin nhắn riêng không có hash, chỉ ở máy Tài.
- Bảy kịch bản thử skill trong `evals/evals.json`.
- `references/wikipedia-signs-full.md` đối chiếu lại bản Wikipedia ngày 2026-10-28: thêm mục 2.6 (khung đính chính), 9.8 (gạch ngang dài thành dấu hiệu cũ), mục 12 bảo trì và bảng ánh xạ sang mã skill. Lần đối chiếu tới: 2027-01-28.
- `references/upstream/avoid-ai-writing/` nâng từ 3.22.3 lên 3.38.0, kèm CHANGELOG, NOTICE và LICENSE gốc.

### Bỏ

- B9-OPENERS (ba câu liền cùng chữ đầu) và C15-SPECIFIC (thiếu chi tiết cụ thể): trên kho văn người hai mã này bắt người nhiều hơn AI. Số hiệu không dùng lại.

### Đổi

- SKILL.md viết lại hoàn toàn: ví dụ cụm cấm đặt trong nháy đơn để script bỏ qua, mỗi luật ghi rõ mức LỖI hay CẢNH BÁO và điều kiện leo thang (B5-NEG lần hai, B14-CORRECT từ 2, C17-CS từ 3).
- D3-TITLECASE là LỖI khi tiêu đề có dấu tiếng Việt, CẢNH BÁO với tiếng Anh.
- D1-DASH giữ làm luật nhà dù Wikipedia đã chuyển gạch ngang dài xuống nhóm dấu hiệu cũ.
- Từ tổng kết (`Có thể nói`, `Nhìn chung`) hạ từ LỖI C2-TEACH xuống CẢNH BÁO C2-SUM vì văn người cũng dùng.

### Số đo (`evals/baseline.json`)

| Kho | File | % file có LỖI | LỖI/1k chữ | CB/1k chữ | Điểm trung vị | % từ 50 | % dưới 20 |
|---|---|---|---|---|---|---|---|
| Văn AI, bản 1.0.0 chấm (27 bài đầu) | 27 | 37 | | | | | |
| Văn người, bản 1.0.0 chấm (kho cũ chưa dọn) | 176 | 4,5 | | | | | |
| Văn AI, bản 2.0.0 | 80 | 82,5 | 9,59 | 10,94 | 76 | 69 | 4 |
| Văn người, bản 2.0.0 (kho đã dọn) | 142 | 1,4 | 0,13 | 0,62 | 0 | 0 | 94 |

Hai dòng đầu lấy từ lần đo ngày 2026-10-28 trên 27 bài AI đầu tiên; script 1.0.0 không còn giữ nên chưa đo lại trên đủ 80 bài.

Kho văn người dọn ngày 2026-10-29: bỏ 34 tin nhắn lẫn văn AI, gồm tin dán lại lời Claude rồi trả lời xen bằng `-->` và tin dán nguyên báo cáo AI có gạch ngang dài hay mũi tên. `corpus.py private` giờ tự lọc kiểu tin này. Trên kho cũ 176 bài, bản 2.0.0 bắt 2,8%.

Bắt nhầm văn người đã biết: D1-DASH 4 chỗ trong 2 bài Wikipedia và Wikisource (ký hiệu toán, dòng ghi nguồn trích). Các chỗ D1-DASH và A3-HOLE từng thấy trong tin nhắn đều nằm ở tin lẫn văn AI và đã ra khỏi kho. C16-TREND chưa bắt được bài AI nào trong kho (0 so với 1 cảnh báo ở văn người), giữ ở CẢNH BÁO và theo dõi ở lần đo sau.

## 1.0.0 (2026-10-08)

- Bảng luật A đến E tự soát, mã A1 đến D9, kịch bản dùng cho caption, kịch bản, email, tài liệu.
- `scripts/check.py` bản đầu: regex tiếng Việt và tiếng Anh, một mức ngưỡng chung, hook chặn khi lưu file trong thư mục sản phẩm.
- Nguồn: Wikipedia Signs of AI writing (đọc 2026-10-08), blader/humanizer 3.1.0, conorbronsdon/avoid-ai-writing 3.22.3.
