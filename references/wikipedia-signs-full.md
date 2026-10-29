<!-- human-writing: off -->
<!-- File này trích nguyên văn các cụm bị cấm làm ví dụ, nên tắt kiểm tự động. Văn giải thích vẫn viết theo SKILL.md. -->
## TL;DR, đọc cái này trước
- **STATUS:** Kiểm kê đầy đủ, đọc trang ngày 2026-10-08 (bản wikitext gốc, ~225 KB); đối chiếu lại bản ngày 2026-10-28 (mục 2.6, 3.4, 9.8, 12)
- **PURPOSE:** liệt kê TOÀN BỘ dấu hiệu văn AI mà Wikipedia ghi nhận, để skill `human-writing` dựa vào
- **KEY FINDING:** Wikipedia tự nhận danh sách là *mô tả triệu chứng*, không phải luật. Vấn đề thật nằm sâu hơn: thông tin bịa, nguồn không kiểm chứng, phân tích hời hợt. Sửa triệu chứng mà để nguyên bệnh thì chỉ làm văn AI khó phát hiện hơn.
- **DECISION:** Skill lấy mục 1–9 làm luật cấm; mục 10 (dấu hiệu của người) làm luật nên làm; mục 11 (dấu hiệu không đáng tin) để KHÔNG gọt quá tay
- **NEXT ACTION:** đối chiếu lại ngày 2027-01-28 theo cách ở mục 12 (trang sửa liên tục, mục 2 và 3 đổi nhiều nhất)

Nguồn: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup. Nội dung trang theo giấy phép CC BY-SA 4.0; file này là bản tóm lược tiếng Việt. `[SOURCE CONFIRMED]` cho mọi mục, trừ ghi chú *(áp dụng VN)* là diễn giải của Claude `[WORKING ASSUMPTION]`.

---

## 0. Gốc rễ: vì sao văn AI có "giọng"

Mô hình đoán chữ tiếp theo theo xác suất, nên **trôi về mức trung bình**: chi tiết cụ thể, hiếm gặp bị thay bằng câu chung chung, tích cực, áp được cho mọi chủ đề. Ví dụ "người phát minh ra khớp nối toa tàu đầu tiên" thành "một người khổng lồ đầy tính cách mạng của ngành công nghiệp". Chủ thể vừa **mờ đi** vừa **bị thổi phồng**. Sau đó RLHF (học từ phản hồi người) lại đẩy văn về kiểu "dễ nghe với đông người nhất".

---

## 1. NỘI DUNG

| # | Dấu hiệu | Từ/cụm cần soi (EN) | Mô tả |
|---|---|---|---|
| 1.1 | **Thổi phồng tầm quan trọng, di sản, xu hướng lớn** | stands/serves as, is a testament/reminder, a crucial/pivotal/vital/significant/key role/moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted, "distinction matters because" | Gắn chi tiết bình thường vào "một phong trào rộng lớn hơn", "đánh dấu bước ngoặt". Đặt chủ đề vào "các cuộc tranh luận", "khơi gợi suy ngẫm". Làm cả với chủ đề tầm thường (từ nguyên, dân số), đôi khi rào "dù ít được ứng dụng" rồi vẫn khen. Viết về sinh vật thì cứ nhắc "vai trò trong hệ sinh thái", "bảo tồn". |
| 1.2 | **Nhấn mạnh độ nổi tiếng, nguồn đưa tin** | independent coverage, local/regional/national media outlets, trade publications, cited/featured/profiled in, written by a leading expert, **active social media presence**, was identified by | Liệt kê báo chí đã đưa tin thay vì nói báo viết gì. Phân loại nguồn ("báo chuyên ngành", "truyền thông khu vực"). Gán phân tích hời hợt của chính nó cho nguồn. "Duy trì sự hiện diện mạnh mẽ trên mạng xã hội" là cụm rất đặc trưng. |
| 1.3 | **Phân tích hời hợt bằng đuôi "-ing"** | highlighting/underscoring/emphasizing, ensuring, reflecting/symbolizing, contributing to, cultivating/fostering, encompassing, enhancing, valuable insights, align/resonate with | Gắn cụm phân từ cuối câu để tỏ ra sâu sắc. Chatbot có tìm web còn gán cho người thật ("Roger Ebert nhấn mạnh…") dù nguồn không nói. *(áp dụng VN: "…, qua đó cho thấy…", "…, góp phần…", "…, khẳng định…", "…, thể hiện…")* |
| 1.4 | **Giọng quảng cáo / cẩm nang du lịch** | boasts a, vibrant, rich, profound, enhancing, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking, renowned, featuring, diverse array | Kể cả khi được yêu cầu viết trung lập. Hai dạng con: (a) di sản văn hóa thì liên tục nhắc "tầm quan trọng"; (b) người/công ty thì giọng thông cáo báo chí. Mô hình mới khen tinh vi hơn, ít dùng "tốt nhất". |
| 1.5 | **Liên hệ mơ hồ** | in connection with/to, connected with/to, in association with, associated with | Không nói rõ quan hệ ("là CEO") mà nói "gắn liền với ban lãnh đạo". Hay đi kèm "particularly/widely associated". |
| 1.6 | **Quy về nguồn mơ hồ, khái quát quá đà** | Industry reports, Observers have cited, Experts argue, Some critics argue, several sources (khi chỉ có ít nguồn), such as (trước danh sách thật ra đã đủ) | Viện "chuyên gia", "giới phê bình" vô danh. Biến ý của 1–2 nguồn thành "nhiều người cho rằng". Dùng "như là…" để ngụ ý còn nhiều ví dụ khác dù nguồn không nói vậy. |
| 1.7 | **Kết luận rập khuôn "Thách thức & Triển vọng"** | Despite its… faces several challenges…, Despite these challenges, Challenges and Legacy, Future Outlook | Mục "Thách thức" mở bằng "Dù [khen], X vẫn đối mặt thách thức…", kết bằng lạc quan mơ hồ hoặc đoán sáng kiến tương lai. Lỗi là *công thức cứng*, không phải việc nhắc đến khó khăn. |
| 1.8 | **Tiêu đề "X và Y", mục "Giải thưởng và ghi nhận"** | Awards and recognition, Recognition | Tiêu đề ghép đôi "X và Y" và mục "Giải thưởng và sự ghi nhận" gần như luôn có trong bài AI. |

## 2. NGÔN NGỮ & NGỮ PHÁP

| # | Dấu hiệu | Chi tiết |
|---|---|---|
| 2.1 | **Mật độ "từ vựng AI" cao** | Additionally (nhất là đầu câu), align with, boasts (= has), bolstered, crucial, deep dive, delve, emphasizing, enduring, enhance, fostering, garner, highlight (động từ), interplay, intricate/intricacies, key (tính từ), landscape (nghĩa trừu tượng), meticulous/meticulously, pivotal, robust, showcase, tapestry (trừu tượng), testament, underscore (động từ), valuable, vibrant. Các từ này đi thành cụm: thấy một thì thường có thêm. **Theo thời kỳ:** 2023–giữa 2024 (GPT-4): delve, tapestry, testament, intricate… · giữa 2024–giữa 2025 (GPT-4o): align with, enhance, fostering, highlighting, showcasing, underscore… · giữa 2025 trở đi (GPT-5): emphasizing, enhance, highlighting, showcasing + cụm "nhấn mạnh nguồn đưa tin" (1.2). Grok: causal, empirical, correlate, underscore. **Chỉ tính đúng từ đó**, từ đồng nghĩa không bị tính. |
| 2.2 | **Né "là / có"** | serves as / stands as / marks / functions as / operates as / represents [a], boasts / features / maintains / offers [a], refers to. Một nghiên cứu đo được tần suất "is/are" trong văn học thuật giảm hơn 10% năm 2023. Bản mới còn rườm hơn: "ventured into politics as a candidate" thay vì "was a candidate". Câu mở đầu hay né bằng "X refers to…" như thể bài viết về *thuật ngữ*. |
| 2.3 | **Song song phủ định** | (a) "Not only… but…", "It is not just…, it's…" · (b) "It's not…, it's…", "no…, no…, just…" · (c) đảo ngược "Y rather than X" (rất phổ biến ở bản mới) · (d) trải qua nhiều câu ("Gia đình nổi tiếng… Tuy nhiên, cuộc đời anh lại…"). Giọng như đang "đính chính hiểu lầm" mà không ai hiểu lầm. |
| 2.4 | **Coi tiêu đề danh sách như danh từ riêng** | Câu mở đầu định nghĩa tên bài kiểu danh sách ("Danh sách X là…") như một thực thể có thật. |
| 2.6 | **Rào đính chính, khung "sửa sai" (giữa 2026 trở đi)** | *should be treated as [tradition] rather than [explanation]*, *does not establish [kết luận]*, *should not be confused with* (dạng này yếu hơn hai dạng trên) | Chatbot từ khoảng 7/2026 (GPT-5.6) hay chèn câu đính chính cho một hiểu lầm không ai nêu: "nên xem là truyền thống tôn giáo chứ không phải lời giải khảo cổ", "tài liệu không đủ để kết luận rằng…". Gần như không có trong văn AI trước giữa 2026, nên văn cũ hơn mốc đó có câu này thì ít khả năng là AI. Nguồn Wikipedia dẫn: Graphite, "AI Tells" (9/2026). *(áp dụng VN: "không đồng nghĩa với", "không nên nhầm với", "chứ không phải là", "chưa đủ để khẳng định"; skill bắt bằng B14-CORRECT khi gặp từ 2 lần một bài)* |
| 2.5 | **Luật bộ ba** | "tính từ, tính từ, tính từ", "cụm ngắn, cụm ngắn, và cụm ngắn". Dùng để làm phân tích hời hợt trông đầy đủ. Càng đáng ngờ khi xuất hiện ở chỗ người ta chẳng buồn trau chuốt (tóm tắt chỉnh sửa, tin nhắn). |

## 3. TRÌNH BÀY

| # | Dấu hiệu | Chi tiết |
|---|---|---|
| 3.1 | **Viết hoa mọi từ trong tiêu đề** (Title Case) | "Impact Of Technology And Digitalization". |
| 3.2 | **Lạm dụng chữ đậm** | Tô đậm máy móc, kiểu "key takeaways", tô đậm mọi lần xuất hiện của một cụm. Thừa hưởng từ README, slide, listicle. |
| 3.3 | **Danh sách có tiêu đề đậm + dấu hai chấm** | "- **Tiêu đề:** mô tả". Ký tự đầu dòng giả (•, -, –, #, emoji), số "1." gõ tay. |
| 3.4 | **Gạch ngang dài (em dash)** | Bản 2026-10-28 của Wikipedia đã chuyển mục này xuống "Dấu hiệu cũ" với mốc 2022 đến 9/2026 (xem 9.8). Skill vẫn giữ D1-DASH làm luật nhà vì Tài không muốn dấu này trong văn giao đi; chi tiết và tỉ lệ bắt nhầm ở 9.8. |
| 3.5 | **Lỗi tiêu đề** | Đặt tiêu đề trùng tên bài ở đầu; nhảy cấp tiêu đề; lạm dụng cấp 1; tiêu đề chỉ chứa tiêu đề con, không có chữ. |
| 3.6 | **Emoji làm định dạng** | Emoji trước tiêu đề hoặc gạch đầu dòng. |
| 3.7 | **Bảng nhỏ không cần thiết** | Bảng 2–3 dòng đáng lẽ viết thành câu. |
| 3.8 | **Ngoặc kép cong** (“ ” ‘ ’) | ChatGPT, DeepSeek. Lẫn cong và thẳng trong một văn bản. *Yếu khi đứng một mình*: Word, macOS tự đổi sang cong. Claude và Gemini thường không dùng ngoặc cong. |

## 4. LỜI NÓI VỚI NGƯỜI DÙNG BỊ SÓT LẠI

| # | Dấu hiệu | Chi tiết |
|---|---|---|
| 4.1 | **Lời giao tiếp của chatbot** | a Wikipedia-style article, I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like…, is there anything else, let me know, more detailed breakdown, here is a… Ghi chú gửi người dùng ("Xóa mục này trước khi nộp…") sót lại trong bài. |
| 4.2 | **Rào đón về nguồn và cách dùng** | While specific details are limited/scarce, not widely available/documented/disclosed, in the provided/available sources, based on available information, "[claim] should be treated as… rather than…", "…does not by itself establish…". Khi không tìm được nguồn, chatbot nói "thông tin không công khai" rồi **đoán** thông tin "có lẽ" là gì. Về đời tư: "giữ kín đời tư", "ít xuất hiện trước công chúng", cũng là đoán. Từ giữa 2026 hay kèm câu dạy dỗ "nên xem đây là… chứ không phải…". |
| 4.3 | **Khung điền chỗ trống bị bỏ quên** | [Entertainer's Name], (Add your channel URL here), (If available), ngày "2025-xx-xx", chú thích "Add if available with citation". |

## 5. MÃ ĐỊNH DẠNG

| # | Dấu hiệu | Chi tiết |
|---|---|---|
| 5.1 | **Markdown sai chỗ** | `**đậm**`, `## tiêu đề`, `[chữ](link)` dán vào nơi không dùng Markdown (Wikipedia, Facebook, Zalo, Word). Markdown *một mình* không phải dấu hiệu mạnh. |
| 5.2 | **Đường kẻ ngang giữa mọi mục** | `---` hoặc `----` ngăn mọi phần. |
| 5.3 | **Mã wikitext lỗi** | Cú pháp hỏng, template bịa. |
| 5.4 | **Rò rỉ mã trích dẫn nội bộ** *(bằng chứng gần như chắc chắn)* | ChatGPT: `:contentReference[oaicite:0]{index=0}`, `oai_citation`, `Example+1`, `turn0search0`, `attributableIndex` · Gemini: `[cite: 1]`, `[span_1](start_span)` · Grok: `grok_card`, `grok_render_citation_card_json` · DeepSeek: ngoặc 【 】, dấu † · Perplexity: `attached_file`, `ppl-ai-file-upload` · Khác: `:::writing`. |
| 5.5 | **Danh mục, template không tồn tại** | Gắn category hoặc template bịa. |

## 6. TRÍCH DẪN

| # | Dấu hiệu | Chi tiết |
|---|---|---|
| 6.1 | **Nhiều link chết** | Không có trong Internet Archive, nghĩa là có lẽ chưa từng tồn tại. |
| 6.2 | **DOI/ISBN sai** | ISBN sai checksum; DOI không phân giải được. |
| 6.3 | **DOI dẫn tới bài không liên quan** | DOI có thật nhưng thuộc bài khác; tác giả đã mất 30 năm vẫn "viết". |
| 6.4 | **Trích sách không số trang, không URL** | Hoặc có số trang nhưng trang đó không chứa nội dung. Sách chủ đề chung, hay được trích. |
| 6.5 | **Dùng tham chiếu sai cách** | Cú pháp tái dùng sai; ký tự ↩ quanh chú thích; PMID số nhỏ không liên quan. |
| 6.6 | **Tham số URL của công cụ AI** | `utm_source=openai`, `utm_source=chatgpt.com`, `utm_source=copilot.com`, `referrer=grok.com`. |
| 6.7 | **Link tới trang kết quả tìm kiếm** | Trích "nguồn" là một URL tìm kiếm. |
| 6.8 | **Tham chiếu khai báo nhưng không dùng** | |

## 7. BÌNH LUẬN & TÓM TẮT CHỈNH SỬA

| # | Dấu hiệu | Chi tiết |
|---|---|---|
| 7.1 | **Bình luận viết bằng AI** | Trích sai quy định, bịa đường tắt; chia bình luận thành nhiều mục có tiêu đề; nói giảm ("tôi có tự chỉnh sửa"); xin góp ý chung chung; gạt đi nghi ngờ là "suy đoán thiếu căn cứ"; kêu gọi "hãy tập trung vào nội dung". |
| 7.2 | **Giọng nhân viên chăm sóc khách hàng** | "đã xem xét kỹ lưỡng", "xin lỗi vì bất tiện có thể đã gây ra", "Nếu có vấn đề cụ thể cần giải quyết, vui lòng chỉ ra, tôi sẽ cố gắng khắc phục." |
| 7.3 | **Tóm tắt chỉnh sửa rập khuôn** | Ngôi thứ nhất, kể lể. Cam đoan tuân thủ quy định ("để trung lập và tuân thủ Manual of Style", "cải thiện nguồn và tính trung lập"). Kể điều *không* làm: "…while preserving the original meaning", "đã giữ nguyên tài liệu tham khảo". Nhấn việc "có nguồn" thay vì nói thêm *nội dung gì*. Liệt kê tên tham số kỹ thuật. "theo góp ý của người duyệt". |

## 8. KHÁC

| # | Dấu hiệu | Chi tiết |
|---|---|---|
| 8.1 | **Giọng văn đổi đột ngột** | Ngữ pháp bỗng hoàn hảo so với tin nhắn thường ngày; dùng tiếng Anh-Mỹ dù người viết và chủ đề là Ấn/Anh *(áp dụng VN: chữ hoàn hảo, giọng Bắc chuẩn sách vở trong khi người viết vốn nói giọng địa phương hoặc nhắn tin xuề xòa)*. |
| 8.2 | **"Lời nhắn cho người duyệt" trong bản nháp** | Tự giải thích vì sao bài đạt chuẩn. |
| 8.3 | **Đặt sẵn template bảo trì** | Ví dụ template "đã bị từ chối" có sẵn. |
| 8.4 | **Trang cá nhân rập khuôn** | "Welcome To My User Page!", "About Me", "My Interests", "Let's Connect!", emoji, chữ đậm. |
| 8.5 | **Cày lượt sửa bằng AI** | Nhiều sửa đổi vô hại, rời rạc để lên quyền. |
| 8.6 | **Mỗi mô hình một "giọng" riêng** | Dấu hiệu của GPT-5 khác GPT-4, Gemini, Claude. |
| 8.7 | **Thiên kiến nội dung** | Một số câu hỏi, mô hình Mỹ vẫn nghiêng thân chính quyền độc đoán. Câu trả lời tiếng Trung nghiêng nhiều hơn. |

## 9. DẤU HIỆU CŨ (mô hình đời cũ, nay hiếm)

| # | Dấu hiệu | Chi tiết |
|---|---|---|
| 9.1 | Nhắc mốc kiến thức | "tính đến lần cập nhật cuối của tôi…" |
| 9.2 | Rào đón dạy dỗ (11/2022–2024) | it's important/critical/crucial to note/remember/consider, worth noting, may vary. |
| 9.3 | Tóm tắt cuối mục, "Kết luận" | Mỗi đoạn/mục kết bằng việc nhắc lại ý chính. |
| 9.4 | Từ chối yêu cầu | "As an AI language model, I can't…" |
| 9.5 | Cắt ngang giữa chừng | Hết token. |
| 9.6 | Ngày truy cập cũ bất thường | |
| 9.7 | **Xoay vòng từ đồng nghĩa** | Phạt lặp từ nên đổi liên tục: "các nghệ sĩ phi chính thống / nghệ sĩ cùng chí hướng / nghệ sĩ tiên phong Nga" cho cùng một nhóm. |
| 9.8 | **Lạm dụng gạch ngang dài (2022 đến 9/2026)** | Mô hình cũ dùng em dash nhiều hơn người không chuyên, ở chỗ người ta dùng dấu phẩy, ngoặc, hai chấm; thường có dấu cách hai bên. Nghiên cứu 7/2026 (The Economist): chỉ Claude còn dùng nhiều hơn người viết chuyên nghiệp, ChatGPT dùng ít hơn. Từ 9/2026 các mô hình mới bị khóa cứng không dùng dấu này, và hệ quả ngược là **độ đa dạng dấu câu giảm hẳn**: chỉ còn dấu phẩy và dấu chấm, nhiều hơn cả văn người (Wikipedia ghi "cần nguồn", 10/2026). Dấu hiệu này mạnh nhất khi đi cùng dấu hiệu khác, và ở trang thảo luận nhiều hơn bài viết. *(Skill: D1-DASH giữ ở mức LỖI làm luật nhà. Trên kho văn người 176 file, luật này bắt 10 chỗ trong 4 file, đều là gạch đầu lời thoại trong truyện, ký hiệu toán và bảng giá dán; đây là tỉ lệ bắt nhầm đã biết và chấp nhận.)* |

---

## 10. DẤU HIỆU CỦA NGƯỜI VIẾT (đo trên 25 năm văn Wikipedia)

Văn người viết **nhiều hơn** văn AI ở các điểm:
- Câu "là / có" đơn giản: *there is a*, *it has a*.
- Động từ thường thay vì từ trang trọng/uyển ngữ: *wrote* (không phải *authored*), *moved* (không phải *relocated*), *used* (không phải *utilized*), *tried* (không phải *attempted*), *died* (không phải *passed away*).
- Khẳng định tuyệt đối, so sánh nhất: *one of the best*, *is the only*, *was the first*.
- **Từ rào và từ nhấn: *very*, *perhaps*, *tends to*.**
- **Cụm dài dòng lẻ tẻ: *as a result of*, *in order to*, *all of the*, *a part of*, *the fact that*.**
- Văn bản trước 30/11/2022 (ChatGPT ra mắt) thì không phải AI.
- Người viết giải thích được vì sao mình chọn cách viết đó.

## 11. DẤU HIỆU KHÔNG ĐÁNG TIN (đừng gọt vì những thứ này)

Ngữ pháp hoàn hảo · trộn giọng thân mật và trang trọng · văn "nhạt", "như robot" · văn "sang", học thuật · từ nối đứng một mình (*Additionally, Consequently, Notably* chỉ là dấu hiệu yếu) · không có nguồn · wikitext kỳ quặc · wikitext đúng.

Người phân biệt bằng cảm giác chỉ hơn tung đồng xu một chút. Một nghiên cứu luận văn tiếng Đức: người nhận đúng 57% văn AI và 64% văn người. Công cụ dò AI (GPTZero, Pangram) có tỉ lệ sai không nhỏ. Và văn người đang ngấm dần thói quen của AI.

---

## 12. BẢO TRÌ VÀ ÁNH XẠ SANG MÃ CỦA SKILL

Cách đối chiếu lại (lần tới 2027-01-28, hoặc khi gặp mẫu mới trong việc thật):

1. Tải wikitext hiện hành, chậm và có liên hệ trong User-Agent: `curl -A "human-writing-skill/2.0 (lien he: email cua Tai)" "https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&action=raw" -o signs.wikitext`.
2. Liệt kê tiêu đề: `grep -n "^==" signs.wikitext`. So với mục 1 đến 11 ở đây; mục mới thì thêm dòng, mục bị chuyển xuống "Historical indicators" thì chuyển sang mục 9 như đã làm với em dash.
3. Mỗi dấu hiệu mới cân nhắc thành mã trong `scripts/check.py`, thêm ca ở `evals/cases/`, chạy `scripts/test_check.py --baseline`; mã nào bắt văn người nhiều hơn văn AI thì bỏ (B9, C15 đã bỏ vì lý do này).
4. Ghi ngày đối chiếu vào STATUS ở đầu file và vào CHANGELOG.

| Mục Wikipedia | Mã trong check.py | Ghi chú |
|---|---|---|
| 1.1, 1.3 | C1-INFL, C2-TEACH | thổi phồng, đuôi "qua đó cho thấy" |
| 1.2, 1.6 | C3-AUTH | nguồn vô danh, "hiện diện mạnh mẽ trên mạng xã hội" |
| 1.4 | C10-PROMO | đếm từ quảng cáo theo đoạn, chuẩn hóa theo độ dài đoạn |
| 1.5 | C7-VAGUE | |
| 1.7 | C8-CHALL | |
| 2.1 | C4-WORD, C18-EN | từ vựng AI tiếng Anh, mẫu câu avoid-ai-writing 3.38 |
| 2.2 | C5-COPULA | |
| 2.3 | B5-NEG, B14-CORRECT | song song phủ định; khung sửa sai giữa 2026 |
| 2.5 | B7-TRIAD | chỉ bắt bộ ba từ trừu tượng |
| 3.1, 3.2, 3.3 | D3-TITLECASE, D6-BOLD, D4-BOLDLIST | |
| 3.4 (nay 9.8) | D1-DASH | luật nhà |
| 3.5 | D13-QHEAD | tiêu đề dạng câu hỏi lặp; lỗi cấp tiêu đề thì tự soát |
| 3.6 | D2-EMOJIHEAD, D10-EMOJIBULLET | |
| 3.7 | tự soát | bảng 2 đến 3 dòng |
| 3.8 | D9-QUOTE | yếu, chỉ cảnh báo |
| 4 | A1-CHAT, A7-PREAMBLE, A4-META, A5-GUESS | |
| 5 | A2-LEAK, A2-UTM, D12-MARKDOWN | |
| 7.2 | C17-CS | giọng chăm sóc khách hàng, ba câu một bài là LỖI |
| 9.2, 9.3 | C2-TEACH, C2-SUM | |
| 9.7 | tự soát | xoay vòng từ đồng nghĩa |
| 10 | LUẬT NÊN LÀM trong SKILL.md | từ rào, "là/có", lặp từ đúng |
| 11 | KHÔNG GỌT QUÁ TAY trong SKILL.md | |

Dấu hiệu chỉ có trong skill, không có trong Wikipedia (lấy từ văn AI tiếng Việt sinh thử 10/2026): B6-SOCIAL, B10-SKELETON, B11-QHOOK, B12-REASSURE, B13-CAPSLINE, B15-TEMPLATE, C13-MOTIV, C16-TREND, C19-WRAP, D7-HASHTAG, D8-EMOJI, D11-NPLIST.
