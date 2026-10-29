---
name: human-writing
description: >-
  Bộ luật viết như người thật (tiếng Việt và tiếng Anh), bắt buộc cho mọi văn bản giao người khác đọc: caption, bài social, quảng cáo, kịch bản, email, tin nhắn khách, proposal, báo cáo, nội dung slide, bài học tập. Cấm dấu hiệu văn AI (mở bài sáo, song song phủ định, gạch ngang dài, bộ ba, lời chatbot, giọng chăm sóc khách hàng, câu hỏi móc rồi trấn an). Có check.py chấm điểm AI 0 đến 100 theo 6 thể loại và giọng riêng (voices/), hook chặn khi lưu file sản phẩm, bộ kiểm thử trên kho văn AI và văn người. Dùng cả khi Tài nói 'viết cho tự nhiên', 'nghe như AI', 'humanize', 'soát giọng AI', 'điểm AI'.
metadata:
  version: "2.0.0"
  created: "2026-10-08"
  updated: "2026-10-29"
---

# Human writing: viết như người thật

Mục tiêu là văn tốt cho người đọc: cụ thể, thẳng, có nhịp. Không phải để qua mặt máy dò AI. Máy dò sai nhiều, và người đọc mới là người quyết định.

Bản 2.0.0 có ba thứ mới: điểm AI 0 đến 100 đo trên kho văn thật, sáu thể loại với ngưỡng riêng, và giọng riêng cho từng kênh (`voices/`). Mọi mã luật trong file này khớp với kết quả của `scripts/check.py`.

## LUẬT 0: NỘI DUNG THẬT TRƯỚC, CÂU CHỮ SAU

Wikipedia nhấn mạnh: các dấu hiệu chỉ là *triệu chứng*. Bệnh thật là thông tin bịa, nguồn không kiểm chứng, phân tích rỗng. Sửa câu chữ mà giữ lại một con số bịa là vi phạm nặng nhất của skill này.

- Không thêm sự kiện, tên, số liệu, ngày, trích dẫn, nguồn nào không có trong tài liệu hoặc lời người dùng.
- Thiếu dữ kiện thì hỏi, hoặc viết câu đơn giản hơn. Không lấp chỗ trống bằng `có lẽ`, `được cho là`.
- Ý kiến, cảm xúc được phép khi giọng văn cần. Khẳng định sự thật thì phải có căn cứ.

## QUY TRÌNH (bắt buộc, theo thứ tự)

1. Chọn thể loại và giọng. Thể loại là một trong `doc`, `social`, `script`, `email`, `academic`, `report` (mục "Thể loại"). Có giọng riêng (`voices/<tên>.toml`, Voice Profile của `assp-brand-voice`, bài cũ của người dùng) thì đọc trước và bám theo: độ dài câu, cách xưng hô, từ ngữ, dấu câu. Giọng riêng được nới nhóm CẢNH BÁO, không được nới nhóm LỖI.
2. Viết nháp theo LUẬT NÊN LÀM, đừng viết bừa rồi mới sửa.
3. Quét bằng máy: lưu bản nháp ra file rồi chạy
   `python3 -I ~/.claude/skills/human-writing/scripts/check.py <file> [--kind social] [--voice <giọng>]`
   Truyền nhiều file một lần cũng được. Không có cờ thì script đọc `kind:` và `voice:` trong frontmatter, rồi đoán thể loại theo đường dẫn. Văn bản ngắn (dưới 40 chữ, ví dụ một dòng hook) thì tự soát theo bảng luật, khỏi chạy script.
4. Sửa bằng cách viết lại cả câu, không vá từng chữ. Xóa `đóng vai trò quan trọng` mà để lại câu cụt là chưa sửa. Hỏi: câu này thật ra muốn nói gì? Rồi nói đúng điều đó.
5. Quét lại tới 0 LỖI và điểm AI dưới 20. Điểm 20 đến 49 thì đọc lại từng CẢNH BÁO; mỗi cảnh báo còn giữ phải nói được lý do bằng một câu. Điểm từ 50 là bài còn giống AI, viết lại đoạn bị bắt nhiều nhất.
6. Đọc to trong đầu. Có câu nào phải dừng lại đọc lần hai không? Có câu nào xóa đi mà người đọc không mất gì không? Có thêm hay mất sự kiện nào so với bản gốc không?

## ĐIỂM AI

`check.py` in một dòng tóm tắt: số chữ, số LỖI, số CẢNH BÁO, điểm AI và kết luận.

| Điểm | Kết luận | Việc cần làm |
|---|---|---|
| 0 đến 19 | sạch | giao được |
| 20 đến 49 | nghi | đọc lại chỗ bị cảnh báo, sửa hoặc nêu lý do giữ |
| 50 đến 100 | giống AI | viết lại, không vá |

Điểm tính từ mật độ: mỗi LỖI nặng gấp ba CẢNH BÁO, chia cho số chữ (tối thiểu 80 chữ để bài ngắn không bị phạt oan), rồi ép về thang 0 đến 100. Một bài 200 chữ có 1 LỖI và 2 CẢNH BÁO được khoảng 63 điểm; cùng bài đó chỉ còn 2 CẢNH BÁO thì khoảng 33.

Số đo trên kho mẫu (`evals/`, bản 2.0.0): văn AI sinh mặc định (80 bài từ Gemini, Claude, GPT-OSS, đủ 6 thể loại) có 82% file dính LỖI, điểm trung vị 76; văn người (Wikipedia tiếng Việt bản cũ, truyện trên Wikisource, tin nhắn tự gõ của Tài) có 1,4% file dính LỖI, điểm trung vị 0, 94% file dưới 20. Bản 1.0.0 đo trên 27 bài AI đầu tiên chỉ bắt được 37%. Bảng đầy đủ nằm trong `evals/baseline.json` và CHANGELOG.

## THỂ LOẠI

Thể loại đổi ngưỡng emoji, hashtag, Markdown và vài luật chỉ bật ở văn social. Ghi `kind: social` trong frontmatter, hoặc truyền `--kind`, hoặc để script đoán theo đường dẫn (`caption`, `ads`, `social`, `post` thành `social`; `script`, `kich-ban`, `storyboard` thành `script`; `email`, `mail`, `zalo`, `tin-nhan` thành `email`; `hoc-tap`, `tieu-luan`, `bai-tap` thành `academic`; `bao-cao`, `report`, `proposal` thành `report`; còn lại `doc`).

| Thể loại | Giọng | Luật thêm |
|---|---|---|
| `social`: caption, bài social, quảng cáo | Như người thật nói với một người cụ thể | Hook là một sự thật, con số, hoặc tình huống. Một CTA, cụ thể. Tối đa 3 hashtag, 3 emoji cuối dòng. Không Markdown (D12). Câu hỏi móc rồi trấn an là LỖI (B11). |
| `script`: kịch bản video, VSL | Văn nói: câu ngắn, có ngập ngừng, có `à`, `thì` | Đọc to được một hơi. Không dàn bài `Thứ nhất… Thứ hai… Cuối cùng` (B10). Không câu chốt truyền cảm hứng theo mẫu (C13). Dòng viết hoa toàn bộ chỉ dùng cho chữ trên màn hình, và phải khai trong giọng riêng. |
| `email`: email, tin nhắn khách | Thẳng, lịch sự, ngắn | Mục E. Câu đầu là việc chính, có ngày giờ. Giọng chăm sóc khách hàng theo mẫu từ 3 câu là LỖI (C17). |
| `academic`: bài học tập, tiểu luận | Trang trọng nhưng không sáo | Thuật ngữ chuyên ngành, từ `là` và câu bị động khi chủ thể không quan trọng đều hợp lệ. Tiêu đề dạng câu hỏi lặp (D13) và kết bài `Hiểu rõ X giúp chúng ta…` (C19) là dấu hiệu AI rõ nhất ở thể loại này. Giọng `hoc-thuat` nới C2-SUM, C11, D13, D6. |
| `report`: proposal, báo cáo nội bộ | Trung tính, rõ | Kết luận trước. Mọi tính từ khen phải đi kèm số liệu. Không đoạn `Thách thức và Triển vọng` (C8). |
| `doc`: blog, tài liệu, nội dung slide, mọi thứ còn lại | Theo người đọc | Luật chung. Emoji và hashtag tính là văn bản công việc: 0. |
| Văn bản tiếng Anh | Theo cùng luật, cùng thể loại | C4 (từ vựng AI) và C18 (mẫu câu avoid-ai-writing 3.38) chỉ bật với tiếng Anh. Đọc thêm `references/upstream/humanizer/SKILL.md`. |

## GIỌNG RIÊNG (`voices/`)

Mỗi kênh có một file TOML. Nạp bằng `--voice <tên>` hoặc frontmatter `voice: <tên>`. Có sẵn:

| Giọng | Kênh | Luật riêng chính |
|---|---|---|
| `mau-kenh` | Mẫu cho kênh video ngắn | xưng `tui`, cấm `tôi`, `mày`, `tao`; chỉ một link bio; bắt buộc thẻ cuối `Follow kênh, mai tui …`; nới B13 (chữ trên màn hình) và D12 |
| `hoc-thuat` | Bài học tập, tiểu luận | nới C2-SUM, C11, D13, D6; cấm `nhiều tài liệu cho rằng` |
| `email-khach` | Email, tin nhắn gửi khách | cảnh báo `Kính gửi quý khách hàng`; cần mốc thời gian |

Giọng thương hiệu riêng (trên máy tác giả có `kp3`, `nghia-kk`, `miduda`) nằm trong `.gitignore`, không lên repo công khai. Mở file trong `voices/` để xem luật của từng giọng.

Cấu trúc file:

```toml
name = "ten-giong"
kind = "social"            # thể loại mặc định
emoji_max = 2              # ngưỡng cảnh báo D8 (LỖI cứng vẫn là 8 với social, 5 với còn lại)
hashtag_max = 3            # ngưỡng cảnh báo D7
allow = ["D12-MARKDOWN"]   # mã được bỏ qua trong giọng này (chỉ nên là mã CẢNH BÁO)
promo_extra = ["siêu", "cực hot"]   # thêm vào danh sách từ quảng cáo C10

[[ban]]                    # cụm cấm riêng
code = "V-XX-TEN"
pattern = "regex"
msg = "Giải thích và cách thay"
level = "error"            # hoặc "warn"

[[require]]                # cụm bắt buộc phải có
code = "V-XX-CTA"
pattern = "regex"
msg = "Thiếu gì"
level = "error"
```

Mã giọng riêng bắt đầu bằng `V-`. Giọng mới thì chép một file có sẵn, đổi tên, thêm một ca thử trong `evals/cases/` rồi chạy `scripts/test_check.py`. Giọng chép từ bộ nhận diện thương hiệu thì ghi nguồn ở dòng đầu file TOML, sửa bên nào thì sửa cả bên kia.

## LỐI THOÁT

Hai chỉ thị viết trong file, hook và script đều hiểu:

- `<!-- human-writing: off -->`: bỏ qua cả file. Dùng cho tài liệu trích nguyên văn, mẫu đối thủ, bảng luật liệt kê cụm cấm.
- `<!-- hw-allow: B5-NEG, D1-DASH -->`: cho phép các mã này trong file. Dùng khi người dùng yêu cầu rõ (slogan brand có `không chỉ… mà còn`).

Dùng lối thoát thì phải báo người dùng một dòng. Không tự nới LỖI vì thấy bài "cũng ổn".

## BẢNG LUẬT CẤM

Mã ở cột đầu khớp với kết quả của `check.py`. **LỖI** là cấm tuyệt đối, hook chặn không cho lưu. **CẢNH BÁO** là sửa, trừ khi có lý do. Mã **TS** là tự soát, script không bắt được. Ví dụ trong dấu `nháy đơn` là nguyên văn cụm bị bắt.

### A. Rác của chatbot (LỖI, xóa thẳng)

| Mã | Cấm | Ví dụ |
|---|---|---|
| A1-CHAT | Lời giao tiếp của chatbot | `Hy vọng bài viết này hữu ích!`, `Chúc bạn thành công!`, `Nếu bạn cần thêm…`, `Bạn có muốn tôi…`, `Câu hỏi rất hay!`, `Rất vui được hỗ trợ`, `Đừng ngần ngại liên hệ`, `Bạn có thể tùy chỉnh…`, `Lưu ý: bạn…` |
| A2-LEAK, A2-UTM | Mã trích dẫn của chatbot, tham số URL của AI | `oaicite`, `turn0search0`, `[cite: 1]`, `【】`, `utm_source=chatgpt.com` |
| A3-HOLE | Chỗ trống chưa điền | `[Tên khách hàng]`, `[Chèn link]`, `2026-xx-xx`, `(Thêm số liệu vào đây)` |
| A4-META | Nói về chính văn bản, rò rỉ cách làm | `Bài viết đã được tối ưu…`, `…trong khi vẫn giữ nguyên ý gốc`, `Hãy suy nghĩ từng bước` |
| A5-GUESS | Đoán mò khi thiếu nguồn, nhắc mốc kiến thức | `Thông tin chưa được công bố rộng rãi, có lẽ…`, `ít xuất hiện trước công chúng`, `tính đến lần cập nhật cuối` |
| A7-PREAMBLE | Câu mào đầu của chatbot trước bài | `Dưới đây là gợi ý caption phù hợp để…`, `Tôi đã viết lại theo giọng…` |
| A6-LIST (CẢNH BÁO) | Câu dẫn vào danh sách | `Dưới đây là…` thường bỏ được |

### B. Dàn dựng thay vì nói thẳng

| Mã | Mức | Cấm | Trước, sau |
|---|---|---|---|
| B1-OPEN | LỖI | Mở bài sáo, báo trước nội dung | `Trong thời đại số, marketing đóng vai trò quan trọng. Hãy cùng khám phá…`, `Với sự phát triển của…` thành `Shop nhỏ chạy ads 5 triệu/tháng thường lỗ ở landing page chứ không phải ở quảng cáo.` |
| B2-HOOK | LỖI | Móc câu kiểu quảng cáo truyền hình, "tiết lộ" giả | `Kết quả? Doanh thu tăng vọt.` thành `Doanh thu tháng 9 tăng 38%.` Cùng nhóm: `Đây chính là lý do…`, `Chìa khóa nằm ở…`, `Sự thật là,`, `Bạn đã sẵn sàng chưa?`, `Tưởng tượng một thế giới…` |
| B3-DEEP | LỖI | Câu triết lý rỗng | `Suy cho cùng, điều thực sự quan trọng là con người.` thành nói cụ thể người nào, làm gì |
| B4-EMO | LỖI | Khai báo cảm xúc suông | `Điều khiến mình bất ngờ nhất là…` thành kể điều đó ra, để người đọc tự bất ngờ |
| B11-QHOOK | LỖI (social, script, email) | Mở bằng câu hỏi dò vấn đề rồi trấn an | `Bạn có đang mệt mỏi vì tóc rụng? Đừng lo!` thành mở bằng sự thật, con số hoặc tình huống. Ở `doc` chỉ là CẢNH BÁO B12. |
| B5-NEG | CẢNH BÁO, lần thứ hai là LỖI | Song song phủ định | `không chỉ… mà còn`, `không phải… mà là`, `chứ không đơn thuần là`, `hơn cả một`. `Đây không chỉ là sản phẩm, mà là phong cách sống.` thành `Bộ này có 3 món dùng được cả đi làm lẫn đi chơi.` Chỉ giữ khi vế phủ định sửa một hiểu lầm người đọc thật sự đang có. |
| B14-CORRECT | CẢNH BÁO (từ 2 lần một bài) | Khung "sửa sai" cho ý không ai nói. Dấu hiệu mới của mô hình từ giữa 2026 | `không đồng nghĩa với`, `không nên nhầm với`, `chưa đủ để khẳng định`, `should be treated as X rather than Y`, `does not establish`. Bỏ, hoặc nói thẳng ý khẳng định. |
| B12-REASSURE | CẢNH BÁO | Câu trấn an theo mẫu quảng cáo | `Đừng lo!`, `Đã đến lúc…`, `Yên tâm nhé` thành nói thẳng giải pháp |
| B6-SOCIAL | CẢNH BÁO | CTA chung chung | `Đừng bỏ lỡ!`, `Inbox ngay để được tư vấn`, `Lưu video này lại`, `Theo dõi mình để biết thêm mẹo` thành CTA nói rõ làm gì, được gì: `Inbox 'SIZE' để shop gửi bảng size trong 5 phút.` |
| B10-SKELETON | CẢNH BÁO | Bộ xương bài văn mẫu | `Trước hết… Thứ hai… Cuối cùng`, `Cách đầu tiên… Cách thứ hai…` thành bỏ số thứ tự, để ý tự nối |
| B15-TEMPLATE | CẢNH BÁO | Câu nối theo mẫu bài văn | `Để làm được điều này`, `Chính vì vậy`, `Nói cách khác` thành bỏ, hoặc nối bằng ý |
| B13-CAPSLINE | CẢNH BÁO | Dòng viết hoa toàn bộ | Hạ xuống chữ thường, giữ đúng một ý nhấn. Kịch bản có chữ trên màn hình thì khai `allow` trong giọng riêng. |
| B7-TRIAD | CẢNH BÁO | Bộ ba từ trừu tượng cho đủ bộ | `sáng tạo, hấp dẫn và giá trị`. Giữ bộ ba khi thật có 3 ý khác nhau. Còn lại dùng 1, 2 hoặc 4 ý, hoặc một câu. |
| B8-RHYTHM | CẢNH BÁO | Nhịp đều như máy: câu dài bằng nhau, đoạn dài bằng nhau | Trộn câu 5 chữ với câu 25 chữ. Có đoạn một câu, có đoạn năm câu. Chỉ đo khi bài từ 8 câu và 120 chữ. |
| TS | LỖI | Câu chốt một dòng nhắc lại đoạn trên: `Và đó là sức mạnh của dữ liệu.` Chuỗi mảnh câu: `Không màu mè. Không rườm rà. Chỉ hiệu quả.` Câu hỏi tu từ rồi tự trả lời làm chuyển đoạn: `Vậy làm sao để tăng đơn? Câu trả lời rất đơn giản.` Cãi với người không ai nói: `Mình không nói rằng ads vô dụng, nhưng…` | Xóa. Hoặc gộp thành một câu có thông tin mới. |

### C. Thổi phồng, mượn uy tín, giọng mẫu

| Mã | Mức | Cấm | Thay bằng |
|---|---|---|---|
| C1-INFL | LỖI | `đóng vai trò quan trọng`, `minh chứng cho`, `đánh dấu bước ngoặt`, `dấu ấn khó phai`, `mở ra chương mới`, `khẳng định vị thế`, `nâng tầm`, `góp phần không nhỏ`, `không thể phủ nhận`, `mang tính cách mạng` | Nói nó làm gì, kèm số nếu có. `Kênh TikTok đóng vai trò then chốt` thành `62% đơn tháng 9 đến từ TikTok.` |
| C2-TEACH | LỖI | Rào đón dạy dỗ, đuôi phân tích hời hợt | `Điều quan trọng là`, `Cần lưu ý rằng`, `Không thể không nhắc`, `Điều này cho thấy`, `…, qua đó cho thấy…` thành nói luôn điều cần lưu ý |
| C2-SUM | CẢNH BÁO | Từ tổng kết sáo | `Có thể nói`, `Có thể thấy`, `Nhìn chung`, `Tóm lại`, `Như vậy, có thể…` Kết bài bằng dữ kiện hoặc việc cần làm cuối cùng. Văn người thỉnh thoảng dùng nên chỉ cảnh báo. |
| C19-WRAP | CẢNH BÁO | Kết bài rộng kiểu sách giáo khoa | `Hiểu rõ X giúp chúng ta…`, `Nắm vững X sẽ giúp bạn…`, `Bài viết này dành cho bạn` thành kết bằng ý cụ thể cuối cùng |
| C3-AUTH | LỖI | Nguồn vô danh | `Các chuyên gia cho rằng`, `Nhiều nghiên cứu chỉ ra`, `Nhiều người cho rằng`, `duy trì sự hiện diện mạnh mẽ trên mạng xã hội` thành nêu tên người, tổ chức, năm, hoặc bỏ câu. Một nguồn thì đừng viết `nhiều nguồn`. |
| C17-CS | CẢNH BÁO, từ 3 câu một bài là LỖI | Giọng nhân viên chăm sóc khách hàng theo mẫu | `Chúng tôi đã xem xét kỹ lưỡng`, `Xin lỗi vì sự bất tiện này`, `Chúng tôi luôn nỗ lực`, `Sự hài lòng của quý khách là…`, `I hope this email finds you well`, `Please don't hesitate to…`, `After a thorough review` thành nói việc đã làm, việc sẽ làm, có ngày giờ. |
| C16-TREND | CẢNH BÁO | Câu "xu hướng chung" thay cho dữ kiện | `ngày càng trở nên phổ biến`, `đang là xu hướng` thành nêu số hoặc bỏ |
| C13-MOTIV | CẢNH BÁO | Câu chốt truyền cảm hứng theo mẫu ở 3 dòng cuối | `Hãy bắt đầu ngay hôm nay!`, `…cùng chúng mình nhé!`, `Bạn xứng đáng…` thành kết bằng việc cụ thể |
| C4-WORD | LỖI (tiếng Anh) | Từ vựng AI theo danh sách Wikipedia | `delve`, `tapestry`, `testament`, `pivotal`, `underscore`, `showcase`, `intricate`, `meticulous`, `boast`, `bolster`, `garner`, `interplay`, `vibrant`, `nestled`, `groundbreaking`, `renowned` thành từ thường: is, has, shows, uses, important |
| C18-EN | CẢNH BÁO (tiếng Anh) | Mẫu câu theo avoid-ai-writing 3.38 | `In today's fast-paced world`, `It's worth noting that`, `At the end of the day` thành nói thẳng |
| C5-COPULA | CẢNH BÁO | Né `là`, `có` | `đóng vai trò là`, `được xem là`, `sở hữu thiết kế`, `tự hào mang đến`. `Sản phẩm sở hữu thiết kế tối giản` thành `Sản phẩm có thiết kế tối giản.` |
| C6-STIFF | CẢNH BÁO | Động từ rườm | `tiến hành phân tích`, `thực hiện việc đánh giá`, `tiến hành xác minh` thành `phân tích`, `đánh giá`, `xác minh` |
| C7-VAGUE | CẢNH BÁO | Liên hệ mơ hồ | `gắn liền với`, `có liên quan đến` thành nói rõ quan hệ: `là nhà sáng lập`, `đã tài trợ` |
| C8-CHALL | CẢNH BÁO | Đoạn `Dù còn thách thức… vẫn đầy triển vọng` | Nêu khó khăn cụ thể. Bỏ câu lạc quan chung chung. |
| C9-HEDGE | CẢNH BÁO | Rào chồng rào | `có thể sẽ có khả năng` thành chọn một từ rào |
| C10-PROMO | 2 từ một đoạn: CẢNH BÁO; 3 từ và từ 2% số chữ của đoạn: LỖI; rải đều cả bài từ 3 từ mỗi 100 chữ: LỖI | Từ quảng cáo, từ AI dồn cục | `đột phá`, `vượt trội`, `hàng đầu`, `đẳng cấp`, `tinh hoa`, `toàn diện`, `tối ưu`, `bền vững`, `hệ sinh thái`, `hành trình`, `kiến tạo`, `lan tỏa`, `chạm đến`, `bức tranh`, `điểm nhấn`, `sống động`, `bứt phá`, `đồng hành`, `uy tín`, `chuyên nghiệp`, `vô cùng`, `tuyệt vời`, `trải nghiệm`, `mang đến`, `chính thức ra mắt`, `nâng cao hiệu quả`, `chinh phục`. Thay bằng dữ kiện: `chất lượng hàng đầu` thành `vải cotton 250gsm, giặt 50 lần không xù`. Giọng riêng thêm từ qua `promo_extra`. |
| C11-TRANS | CẢNH BÁO | Từ nối đầu câu dày hoặc lặp | `Bên cạnh đó`, `Ngoài ra`, `Thêm vào đó`, `Hơn nữa`, `Đặc biệt`, `Không chỉ vậy`, `Đồng thời`. Bỏ phần lớn. Không dùng một từ nối hai lần trong bài. |
| C12-TRANSL | CẢNH BÁO | Văn dịch | `một cách nhanh chóng` lặp nhiều lần, `được… bởi…` lặp. `Lỗi được sửa bởi đội kỹ thuật` thành `Đội kỹ thuật sửa lỗi`. |
| TS | LỖI | Xoay vòng từ đồng nghĩa để tránh lặp: `khách hàng… người tiêu dùng… thượng đế… quý khách` cho cùng một nhóm | Lặp lại đúng từ rõ nhất. |

### D. Trình bày

| Mã | Mức | Cấm | Ghi chú |
|---|---|---|---|
| D1-DASH | LỖI | Gạch ngang dài (em dash, en dash) dùng làm dấu nối câu | Thay bằng dấu phẩy, chấm, hai chấm, ngoặc đơn. Gạch nối giữa hai số (`2020–2024`) được giữ. Wikipedia 10/2026 đã chuyển dấu này xuống "dấu hiệu cũ" vì mô hình mới bị khóa không dùng; skill vẫn giữ làm luật nhà theo ý Tài. Trên kho văn người, luật này bắt 4 chỗ trong 2 bài Wikipedia và Wikisource (ký hiệu toán, dòng ghi nguồn), là tỉ lệ bắt nhầm đã biết. |
| D2-EMOJIHEAD | LỖI | Emoji trong tiêu đề | |
| D4-BOLDLIST | LỖI | Danh sách `- **Nhãn:** mô tả` từ 3 dòng | Viết thành câu, hoặc bỏ nhãn đậm. Nhãn chỉ giữ khi người đọc cần dò nhanh (bảng giá, thông số). |
| D10-EMOJIBULLET | CẢNH BÁO ở social, LỖI ở còn lại | Emoji làm đầu dòng từ 3 dòng | `✅ Giao nhanh` `✅ Giá tốt` thành câu có dữ kiện |
| D3-TITLECASE | LỖI khi tiêu đề có dấu tiếng Việt, CẢNH BÁO với tiếng Anh | Tiêu Đề Viết Hoa Mọi Chữ | `Chiến lược nội dung quý 4`, không phải `Chiến Lược Nội Dung Quý 4` |
| D5-HR | CẢNH BÁO | Đường kẻ ngang giữa mọi mục | |
| D6-BOLD | CẢNH BÁO | In đậm dày | Tối đa 1 cụm mỗi mục, hoặc không. |
| D7-HASHTAG | quá 5: LỖI; social quá 3 (hoặc `hashtag_max` của giọng): CẢNH BÁO | Hashtag dồn cục | Tối đa 3 hashtag cụ thể, có người thật tìm. |
| D8-EMOJI | quá 8 ở social, quá 5 ở còn lại: LỖI; quá `emoji_max` (3 social, 0 còn lại): CẢNH BÁO | Emoji | Văn bản công việc: 0. Social: tối đa 3, đặt cuối dòng, không thay chữ. |
| D11-NPLIST | CẢNH BÁO | Danh sách 5 dòng trở lên toàn cụm danh từ không động từ | `Chất lượng cao / Giá hợp lý / Giao nhanh` thành câu kiểm chứng được: `Giao nội thành 2 giờ, phí 15 nghìn.` |
| D12-MARKDOWN | CẢNH BÁO (social) | Markdown dán vào nơi không hiển thị Markdown | Facebook, Zalo, TikTok, email thường, tin nhắn: không `**`, không `##`, không `[chữ](link)`. Google Docs, Slides: dùng định dạng của chính công cụ. |
| D13-QHEAD | CẢNH BÁO | Từ 2 tiêu đề dạng câu hỏi | `X là gì?`, `Tại sao cần X?` là dàn bài FAQ của AI. Đặt tiêu đề là ý chính. |
| D9-QUOTE | CẢNH BÁO (yếu) | Ngoặc kép cong | Theo chuẩn của nơi đăng. |
| TS | LỖI | Bảng 2 đến 3 dòng đáng lẽ là một câu; tiêu đề lặp lại ngay ở câu đầu; tiêu đề chỉ chứa tiêu đề con | Viết thành câu. |
| TS | LỖI | `5 điều bạn cần biết`, `3 bí quyết vàng` khi nội dung không thật sự có đúng 5 hay 3 ý song song | Đếm ý thật trước, đặt tiêu đề sau. |

### E. Viết cho sai người đọc (tin nhắn, email, trả lời)

| Cấm | Thay bằng |
|---|---|
| Kể lại vấn đề người kia đã biết, rồi mới tới quyết định ở dòng cuối | Câu đầu là quyết định hoặc câu trả lời. Chỉ giữ lý do nào làm người đọc đổi ý. |
| Giọng nhân viên chăm sóc khách hàng (C17) | Nói việc đã làm và việc sẽ làm, có ngày giờ. Xin lỗi thì xin lỗi đúng lỗi cụ thể. |
| Tường thuật thiện chí: `Thật lòng mà nói…`, `Mình muốn minh bạch rằng…` | Nói luôn điều cần minh bạch. |
| `Kính gửi quý khách hàng` cho một người cụ thể | Gọi tên: `Chào chị Lan`. |

Mã đã bỏ trong bản 2.0.0 vì bắt văn người nhiều hơn văn AI: B9-OPENERS (ba câu liền cùng chữ đầu; truyện và tin nhắn lặp chủ ngữ là bình thường) và C15-SPECIFIC (thiếu chi tiết cụ thể; đo được ngược chiều). Số hiệu không dùng lại.

## LUẬT NÊN LÀM (dấu hiệu văn người, Wikipedia đo trên 25 năm)

- Cụ thể hơn chung chung: số, tên, địa điểm, thời gian, một chi tiết lạ chỉ người trong cuộc mới biết. `Khách hàng hài lòng` yếu hơn `chị Lan ở Thủ Đức đặt lại lần thứ ba`.
- Dùng `là`, `có` và động từ thường: viết, dùng, thử, chuyển, bán. Không `sở hữu`, `tiến hành`, `kiến tạo`.
- Khẳng định mạnh khi đúng: `duy nhất`, `đầu tiên`, `rẻ nhất khu` nếu có căn cứ.
- Giữ từ rào, từ nhấn của người: `rất`, `khá`, `có lẽ`, `thường`, `hình như`. Wikipedia ghi nhận người dùng các từ này nhiều hơn AI. Đừng gọt sạch.
- Cụm dài dòng lẻ tẻ là bình thường: `để mà`, `do là`, `tất cả những`. Không cần chuốt từng câu tới mức vô trùng.
- Lặp lại từ đúng thay vì xoay vòng từ đồng nghĩa.
- Nhịp không đều: câu ngắn xen câu dài, đoạn ngắn xen đoạn dài. Dấu câu đa dạng: chấm phẩy, hai chấm, ngoặc đơn đều dùng được. Mô hình mới từ 9/2026 chỉ còn dấu phẩy và dấu chấm, và đó đã thành một dấu hiệu AI mới.
- Mở bằng ý chính, bối cảnh để sau. Kết bằng dữ kiện hoặc việc cần làm, không tóm tắt.
- Không đính chính cho hiểu lầm không ai nêu. Mô hình từ giữa 2026 hay chèn `nên xem là X chứ không phải Y`, `chưa đủ để kết luận`. Người viết chỉ đính chính khi người đọc thật sự đang hiểu sai.
- Có quan điểm khi thể loại cho phép: thích, không thích, còn băn khoăn, kèm lý do.
- Văn thân mật được mở câu bằng `Mà`, `Nhưng`, `Còn`, được có câu cụt cố ý, được tự sửa giữa chừng `(à không, thứ Ba mới đúng)`.

## KHÔNG GỌT QUÁ TAY

Wikipedia liệt kê những thứ không chứng minh văn là AI: ngữ pháp hoàn hảo, trộn giọng thân mật và trang trọng, văn hơi nhạt, văn học thuật, một hai từ nối, không có nguồn. Đừng phá một câu tốt chỉ vì nó "nghe hơi trơn". Kho văn người của skill xác nhận điều này: Wikipedia tiếng Việt và truyện cũ có từ nối, câu tổng kết, bộ ba, mà vẫn là văn người; vì thế các mã đó chỉ ở mức CẢNH BÁO.

**Xung đột với skill khác:** `writing-professional` (references/editing-checklist.md) bắt xóa `rất`, `khá`, `có lẽ`, `nhằm để`. Về câu chữ, skill này thắng: giữ các từ đó khi chúng tự nhiên và đúng ý. Phần cấu trúc (kết luận trước, một người một việc một hạn chót) vẫn theo `writing-professional`.

## CÁCH TRẢ KẾT QUẢ

- Tự viết sản phẩm (skill khác đang chạy, hoặc người dùng nhờ viết): chỉ giao bản cuối đã sạch. Không ghi "đã humanize", không kể đã sửa gì.
- Người dùng dán văn bản nhờ soát: trả bản viết lại cộng một dòng `Đã sửa N lỗi: [mã ngắn]`, kèm điểm AI trước và sau nếu người dùng hỏi "điểm AI". Chỉ đưa bảng chi tiết khi được hỏi.
- Sửa file: chỉ sửa phần văn xuôi. Giữ nguyên code, đường dẫn, số liệu, link, YAML.
- Không giữ được 0 LỖI vì người dùng yêu cầu rõ (brand bắt buộc dùng slogan có song song phủ định): thêm `<!-- hw-allow: B5-NEG -->` và ghi một dòng cho người dùng biết.

## HOOK, KIỂM THỬ, BẢO TRÌ

Hook `scripts/hook.py` đăng ký ở `~/.claude/settings.json` (PostToolUse cho Write, Edit, MultiEdit). Chỉ xét file `.md`, `.txt` trong thư mục sản phẩm (`outputs/`, `projects/`, `courses/`, `research/`, `team/`, `deliverables/`, `drafts/`), bỏ `.agents/`, `.claude/`, `docs/`, `prompts/`, `_archive/`, `evals/corpus/`. Write thì quét cả file và báo điểm; Edit chỉ quét đoạn mới thêm và chỉ ép LỖI. Còn LỖI thì hook trả `decision: block` kèm danh sách, Claude phải viết lại rồi lưu lại. Lỗi trong hook không bao giờ làm hỏng phiên.

Kiểm thử `python3 -I scripts/test_check.py`: chạy 14 ca đơn vị trong `evals/cases/` (frontmatter nêu `kind`, `voice`, `expect_errors`, `expect_warnings`, `expect_no`, `expect_clean`, `max_score`, `min_score`), rồi in bảng đo trên kho. Thêm `--codes` để xem từng mã bắt bao nhiêu ở văn AI và văn người; `--baseline` để so với `evals/baseline.json` và báo mã nào bắt nhầm người nhiều hơn trước; `--impl <check_cu.py>` để so hai bản.

Kho văn `scripts/corpus.py`: `gen` sinh văn AI mặc định bằng `agy` (Gemini, Claude) vào `evals/corpus/ai/` (commit được); `fetch` tải văn người công khai (Wikipedia tiếng Việt bản trước 2020, Wikisource) vào `evals/corpus/cache/` theo `manifest.json` có sha256; `private` trích tin nhắn tự gõ của người dùng từ lịch sử phiên vào cache, bỏ tin dán lại lời AI. Văn người không bao giờ commit: văn công khai có sha256 trong `manifest.json` để tải lại đúng bản, tin nhắn riêng chỉ nằm trên máy.

Thêm một luật mới theo đúng thứ tự: gặp mẫu trong việc thật; thêm regex vào `check.py` ở mức CẢNH BÁO; thêm một ca trong `evals/cases/`; chạy `test_check.py --codes`; mã bắt văn người từ 1 LỖI trở lên hoặc tỉ lệ AI/người dưới 3 thì hạ mức hoặc bỏ; đạt rồi mới thêm dòng vào bảng trên và CHANGELOG. Đối chiếu Wikipedia lần tới: 2027-01-28 (cách làm ở mục 12 của `references/wikipedia-signs-full.md`).

## NGUỒN

- `references/wikipedia-signs-full.md`: kiểm kê đầy đủ dấu hiệu của [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (đọc 2026-10-08, đối chiếu lại 2026-10-28, CC BY-SA 4.0), có bảng ánh xạ sang mã của skill.
- `references/upstream/humanizer/`: blader/humanizer 3.1.0 (MIT), bản gốc tiếng Anh.
- `references/upstream/avoid-ai-writing/`: conorbronsdon/avoid-ai-writing 3.38.0 (MIT), mẫu social, email, bảng từ theo tầng, cách giữ kho văn người bằng hash.
- Phần tiếng Việt (mẫu câu, từ cấm) là Claude chuyển từ mẫu tiếng Anh rồi đo lại trên kho văn AI tiếng Việt sinh thử tháng 10/2026 và kho văn người của Tài. Chưa có nghiên cứu công bố đo trên văn AI tiếng Việt; mọi ngưỡng ở đây là số đo nội bộ, ghi trong `evals/baseline.json`.
