#!/usr/bin/env python3
"""Quét văn bản tìm dấu hiệu văn AI (tiếng Việt + tiếng Anh). Luật lấy từ SKILL.md của human-writing.

Dùng:
  python3 -I check.py <file>                       # .md / .txt; kind tự đoán từ frontmatter `kind:` hoặc tên đường dẫn
  python3 -I check.py - < bai.txt                  # đọc từ stdin
  python3 -I check.py <file> --kind social         # doc | social | script | email | academic | report
  python3 -I check.py <file> --voice mau-kenh      # nạp voices/mau-kenh.toml: mã được miễn, từ cấm, từ bắt buộc
  python3 -I check.py <thư mục> --dir              # quét mọi .md/.txt trong thư mục, in bảng điểm
  python3 -I check.py <file> --json
  python3 -I check.py <file> --fail-score 60       # exit 1 cả khi điểm AI >= 60 dù không có LỖI

Mức:
  LỖI      bắt buộc sửa hết trước khi giao (exit code 1)
  CẢNH BÁO sửa, hoặc giữ nếu có lý do nói được thành lời
  ĐIỂM AI  0-100, gộp mật độ LỖI và CẢNH BÁO trên 100 chữ. Dưới 20: sạch. 20-49: nghi. Từ 50: giống AI.

Lối thoát ghi trong file (check.py và hook.py đều hiểu):
  <!-- human-writing: off -->          bỏ qua cả file
  <!-- hw-allow: B5-NEG, D1 -->        miễn các mã này (ghi mã đầy đủ hoặc chỉ phần trước gạch)

Bỏ qua: khối code ```...```, `code` trong dòng, dòng trích dẫn bắt đầu bằng ">", frontmatter YAML, bảng Markdown khi đo nhịp.
Sửa danh sách mẫu ở đây thì cập nhật bảng luật trong SKILL.md và chạy scripts/test_check.py.
"""
import argparse
import json
import math
import os
import re
import statistics
import sys

VERSION = "2.0.0"
I = re.IGNORECASE | re.MULTILINE
KINDS = ("doc", "social", "script", "email", "academic", "report")
HERE = os.path.dirname(os.path.abspath(__file__))
VOICE_DIR = os.path.join(os.path.dirname(HERE), "voices")

# ---------------------------------------------------------------- LỖI (cấm tuyệt đối)
HARD = [
    # A. Rác chatbot, rò rỉ, chỗ trống
    ("A1-CHAT", r"hy vọng (bài viết|thông tin|nội dung|những chia sẻ|chia sẻ|hướng dẫn) (này|trên)", "Lời chatbot. Xóa."),
    ("A1-CHAT", r"chúc (bạn|các bạn|anh|chị) (thành công|áp dụng thành công)", "Lời chatbot kết bài. Xóa."),
    ("A1-CHAT", r"nếu (bạn|anh|chị|quý khách) cần (thêm|hỗ trợ thêm|giải đáp thêm)", "Lời chatbot mời hỏi tiếp. Xóa."),
    ("A1-CHAT", r"(bạn|anh|chị) có muốn (tôi|mình|em) ", "Lời chatbot đề nghị. Xóa."),
    ("A1-CHAT", r"(tất nhiên|chắc chắn|dĩ nhiên) rồi\s*!", "Lời chatbot. Xóa."),
    ("A1-CHAT", r"câu hỏi (rất|thật|cực kỳ) (hay|thú vị)", "Khen người hỏi. Xóa."),
    ("A1-CHAT", r"(bạn|anh|chị) hoàn toàn (đúng|chính xác)", "Nịnh. Xóa."),
    ("A1-CHAT", r"rất vui (được|khi được) (giúp|hỗ trợ|chia sẻ)", "Lời chatbot. Xóa."),
    ("A1-CHAT", r"đừng ngần ngại (liên hệ|hỏi|để lại)", "Lời chatbot. Xóa hoặc thay bằng CTA cụ thể."),
    ("A1-CHAT", r"(là|như) một (mô hình ngôn ngữ|trợ lý AI|AI)", "Lời tự xưng AI. Xóa."),
    ("A1-CHAT", r"(bạn|anh|chị) có thể (tùy chỉnh|thay đổi|điều chỉnh|thay thế) (lại )?(nội dung|tên|số liệu|thông tin|các chi tiết|phần)", "Ghi chú của chatbot cho người dùng. Xóa, điền thật."),
    ("A1-CHAT", r"^\W*lưu ý\W*:\s*(bạn|anh|chị|hãy|có thể|nên|cần) (thay|điền|tùy chỉnh|cập nhật|bổ sung)", "Ghi chú của chatbot cho người dùng. Xóa."),
    ("A1-CHAT", r"\b(I hope this helps|Certainly!|Of course!|Great question|You'?re absolutely right|let me know if|feel free to|Would you like me to|Is there anything else|as an AI( language model)?)\b", "Chatbot residue. Delete."),
    ("A2-LEAK", r"oaicite|contentReference|oai_citation|turn\d+search\d+|attributableIndex|\[cite: ?\d+\]|start_span|grok_card|grok_render|ppl-ai-file-upload|attached_file|【|】|:::writing", "Mã nội bộ của chatbot bị sót. Xóa, thay bằng nguồn thật."),
    ("A2-UTM", r"utm_source=(openai|chatgpt\.com|copilot\.com|claude\.ai|perplexity(\.ai)?)|referrer=grok\.com", "Tham số URL của công cụ AI. Xóa tham số, giữ link."),
    ("A3-HOLE", r"\[(tên|chèn|thêm|điền|nhập|mô tả|link|đường dẫn|số|ngày|địa chỉ|your|insert|add|enter|describe|name)\b[^\]]*\]", "Chỗ trống chưa điền."),
    ("A3-HOLE", r"\b20\d\d-(xx|XX)-(xx|XX)\b|\bxx/xx\b|\(\s*(thêm|chèn|điền|add|insert)\b[^)]*(vào đây|ở đây|nếu có|here|if available)[^)]*\)", "Chỗ trống chưa điền."),
    ("A4-META", r"(bài viết|văn bản|nội dung|đoạn văn) (này )?(đã được|được) (viết lại|chỉnh sửa|tối ưu|humanize)", "Kể chuyện về văn bản thay vì nói nội dung. Xóa."),
    ("A4-META", r"(trong khi |vẫn )?(giữ nguyên|bảo toàn) (ý nghĩa|nội dung|ý) (gốc|ban đầu)|while preserving", "Tường thuật cách làm. Xóa."),
    ("A4-META", r"(hãy|để tôi|để mình) (cùng )?(suy nghĩ|phân tích|đi) từng bước|let me think step by step|here'?s my thought process", "Rò rỉ chuỗi suy luận. Xóa."),
    ("A5-GUESS", r"(tính đến|theo) (lần cập nhật|dữ liệu|kiến thức) (cuối|mới nhất) của (tôi|mình)|as of my last (update|training)", "Nhắc mốc kiến thức của mô hình. Xóa."),
    ("A5-GUESS", r"chưa được công bố( rộng rãi)?,? (nên |và |vì vậy )?(có lẽ|có thể|dường như|nhiều khả năng)|(giữ kín|kín tiếng về) (đời tư|đời sống riêng)|ít xuất hiện trước công chúng|maintains? a low profile", "Đoán mò khi thiếu nguồn. Xóa hoặc ghi 'chưa có nguồn'."),
    ("A7-PREAMBLE", r"^\W*(dưới đây|sau đây) là (một |bản |bài |mẫu |gợi ý |nội dung |kịch bản |email |caption )+[^\n]{0,100}(cho bạn|theo yêu cầu|phù hợp|bạn có thể|văn phong|giọng)", "Câu mào đầu của chatbot ('Dưới đây là gợi ý… phù hợp để…'). Xóa, bắt đầu bằng bài."),
    ("A7-PREAMBLE", r"^\W*(tôi|mình) (đã|sẽ|xin) (viết|soạn|chuẩn bị|tổng hợp|gợi ý|đề xuất) [^\n]{0,60}(cho bạn|dưới đây|sau đây|như sau)", "Chatbot kể mình đã làm gì. Xóa."),

    # B. Dàn dựng thay vì nói thẳng
    ("B1-OPEN", r"trong (thời đại|kỷ nguyên) (số|công nghệ|4\.0|số hóa|ngày nay|hiện nay|AI|trí tuệ nhân tạo)", "Mở bài sáo. Vào thẳng ý chính."),
    ("B1-OPEN", r"trong bối cảnh (hiện nay|ngày nay|hiện tại)\b", "Mở bài sáo. Nêu bối cảnh cụ thể hoặc bỏ."),
    ("B1-OPEN", r"trong thế giới (hiện đại|ngày nay|đầy biến động|số|kinh doanh hiện đại)", "Mở bài sáo."),
    ("B1-OPEN", r"với sự (phát triển|bùng nổ|gia tăng|lên ngôi|xuất hiện) (mạnh mẽ |không ngừng |vượt bậc |nhanh chóng |chóng mặt |ngày càng )?(của|về)", "Mở bài sáo 'Với sự phát triển của…'. Bỏ, vào thẳng."),
    ("B1-OPEN", r"\bhãy cùng\b|\bcùng (nhau )?(khám phá|tìm hiểu|điểm qua)\b", "'Hãy cùng khám phá': dàn dựng. Nói luôn nội dung."),
    ("B1-OPEN", r"trong bài viết này,? (chúng ta|mình|tôi|chúng tôi) sẽ", "Báo trước nội dung. Bỏ, viết luôn."),
    ("B1-OPEN", r"\b(let'?s (dive|explore|break (this|it) down|take a look)|in today'?s (fast-paced|digital|world)|in an era (where|of)|without further ado|in this (post|article),? (we|I)'?(ll| will))\b", "Staged opener. Start with the point."),
    ("B2-HOOK", r"(kết quả|bí quyết|điều bất ngờ|điều tuyệt vời nhất|mấu chốt|vấn đề|lý do)\s*(là\s*)?\?", "Móc câu kiểu quảng cáo truyền hình ('Kết quả?'). Nói thẳng."),
    ("B2-HOOK", r"\b(sự thật là|thực tế là),", "Dàn dựng 'sự thật là'. Nói thẳng sự thật."),
    ("B2-HOOK", r"câu trả lời (là|nằm ở|chính là)|(đây|đó) chính là (lý do|bí mật|chìa khóa)|chìa khóa (nằm ở|chính là)|(là|chính là) (chìa khóa|bí quyết|chìa khoá)|và đó chính là", "Màn 'tiết lộ' giả. Nói thẳng."),
    ("B2-HOOK", r"(bạn|các bạn) đã sẵn sàng (chưa|để)|tưởng tượng (một thế giới|một tương lai)", "Móc câu sáo."),
    ("B2-HOOK", r"\b(here'?s the (thing|kicker|catch)|the (catch|kicker|result|best part)\?|plot twist|imagine a world|what nobody tells you|the part nobody talks about|here'?s what (most people|nobody) (miss|get wrong|tell)|meet \w+, your new (favorite|go-to))\b", "Infomercial hook. State it."),
    ("B3-DEEP", r"(suy cho cùng|về bản chất|cốt lõi của vấn đề|điều thực sự quan trọng) (là|chính là)", "Câu triết lý rỗng. Thay bằng nhận định cụ thể."),
    ("B3-DEEP", r"\b(at its core|the real question is|what really matters)\b", "Fake-deep saying."),
    ("B4-EMO", r"điều khiến (tôi|mình|chúng tôi) (bất ngờ|ấn tượng|thích thú) nhất|thật (thú vị|bất ngờ) khi|điều thú vị (là|nhất là)", "Khai báo cảm xúc suông. Để nội dung tự gây bất ngờ."),

    # C. Thổi phồng, mượn uy tín
    ("C1-INFL", r"đóng vai trò (vô cùng |cực kỳ |rất |hết sức )?(quan trọng|then chốt|chủ chốt|trọng yếu|không thể thiếu|cốt lõi|chủ đạo)", "Thổi phồng vai trò. Nói nó LÀM gì."),
    ("C1-INFL", r"giữ (một )?vai trò (quan trọng|then chốt|chủ chốt)|(phần|yếu tố|công cụ|kênh|bước) không thể thiếu", "Thổi phồng vai trò."),
    ("C1-INFL", r"minh chứng (rõ nét|sống động|hùng hồn|rõ ràng)?\s*(cho|rằng)|là (một )?minh chứng", "'Minh chứng cho…': thổi phồng."),
    ("C1-INFL", r"đánh dấu (một )?(bước ngoặt|cột mốc|chương mới|bước tiến|sự chuyển mình)", "Thổi phồng thành 'bước ngoặt'. Nêu sự kiện."),
    ("C1-INFL", r"dấu ấn (khó phai|đậm nét|sâu đậm)|(mở ra|mở đầu) (một )?(chương|kỷ nguyên|trang) mới|kỷ nguyên mới", "Thổi phồng."),
    ("C1-INFL", r"khẳng định (vững chắc )?vị thế|\bnâng tầm\b|góp phần (không nhỏ|quan trọng|to lớn|tích cực|đáng kể)", "Thổi phồng."),
    ("C1-INFL", r"không thể phủ nhận|mang tính (bước ngoặt|cách mạng)|phản ánh (một )?xu hướng (rộng lớn|chung|lớn)", "Thổi phồng."),
    ("C1-INFL", r"\b(stands as|serves as a testament|a testament to|plays? a (crucial|pivotal|key|vital|significant) role|pivotal moment|marking a (pivotal|significant)|evolving landscape|indelible mark|setting the stage for|enduring legacy|game[- ]changer)\b", "Significance inflation."),
    ("C2-TEACH", r"điều (quan trọng|cần lưu ý|đáng chú ý|đáng nói) (là|nhất là)|cần lưu ý (rằng|là)|(xin )?lưu ý rằng|không thể không (nhắc|kể) đến", "Rào đón dạy dỗ. Nói luôn điều đó."),
    ("C2-TEACH", r"điều này cho thấy|qua đó (cho thấy|có thể thấy|thể hiện|khẳng định)|từ đó góp phần", "Đuôi 'qua đó cho thấy…': phân tích hời hợt."),
    ("C2-TEACH", r"\b(it'?s (important|crucial|worth) (to note|noting|remembering)|it should be noted|worth noting|in conclusion|in summary)\b", "Didactic filler."),
    ("C3-AUTH", r"(các|nhiều|giới) chuyên gia (cho rằng|nhận định|đánh giá|khuyên|khẳng định|chỉ ra)|theo (các|nhiều) chuyên gia", "Chuyên gia vô danh. Nêu tên người/nguồn hoặc bỏ."),
    ("C3-AUTH", r"(nhiều|các) (nghiên cứu|khảo sát|báo cáo|thống kê) (đã )?(cho thấy|chỉ ra|chứng minh)|giới (chuyên môn|phân tích) (cho rằng|nhận định)|nhiều người cho rằng", "Nguồn vô danh. Nêu nghiên cứu cụ thể hoặc bỏ."),
    ("C3-AUTH", r"\b(experts (argue|believe|say|agree)|studies (show|suggest)|research (shows|suggests)|observers have (cited|noted)|industry reports)\b", "Vague attribution."),
    ("C3-AUTH", r"(duy trì|có) sự hiện diện (mạnh mẽ|tích cực) trên (các )?(mạng xã hội|nền tảng số)|active social media presence", "Cụm đặc trưng AI. Nêu kênh + số liệu thật."),
    ("C4-WORD", r"\b(delv(e|es|ed|ing)|tapestry|testament|pivotal|underscor(e|es|ed|ing)|showcas(e|es|ed|ing)|intricac(y|ies)|intricate|meticulous(ly)?|boast(s|ed|ing)?|bolster(s|ed|ing)?|garner(s|ed|ing)?|interplay|vibrant|nestled|groundbreaking|renowned)\b", "AI vocabulary (Wikipedia list). Replace with a plain word."),

    # D. Trình bày
    ("D1-DASH", r"—|\s--\s|\s–\s|–\s|\s–", "Gạch ngang dài. Thay bằng dấu phẩy, chấm, hai chấm, ngoặc đơn, hoặc viết lại câu."),
]

# ---------------------------------------------------------------- CẢNH BÁO
WARN = [
    ("B5-NEG", r"không (chỉ|những|đơn thuần|đơn giản)\s+(là\s+)?[^.!?\n]{1,80}?mà (còn|là)|không phải (là\s+)?[^.!?\n]{1,60}?,?\s*mà (là|chính là)|chứ không (chỉ |đơn thuần |phải )?là|\bhơn cả (một|là)\b", "Song song phủ định ('không chỉ… mà còn'). Nói thẳng vế sau. >1 lần/bài = LỖI."),
    ("B5-NEG", r"\bnot (just|only|merely)\b[^.!?\n]{1,80}\bbut\b|\bit'?s not\b[^.!?\n]{1,60}[,;]\s*it'?s\b|\bno [^.!?\n]{1,30}, no [^.!?\n]{1,30}, just\b", "Negative parallelism. >1 per text = LỖI."),
    ("B6-SOCIAL", r"đừng bỏ lỡ|lưu (lại|ngay) (bài|post|ngay)|(bạn|ai) cũng nên (đọc|xem|lưu)|(tag|share) ngay", "Câu chốt social chung chung. CTA phải nói làm gì, được gì."),
    ("B6-SOCIAL", r"(inbox|nhắn tin|liên hệ|đăng ký|gọi|đặt lịch|ghé|book|đặt hàng|mua) (ngay|liền)( hôm nay)?[^\n]{0,40}?(để (được|nhận|giữ|trải nghiệm|tư vấn)|nhé|!)|để được tư vấn( miễn phí| chi tiết)?", "CTA chung chung ('Inbox ngay để được tư vấn'). Nói rõ làm gì, nhận gì, trong bao lâu."),
    ("B6-SOCIAL", r"(lưu|save) (ngay )?(video|bài|bài viết|post) (này )?(lại|ngay)|theo dõi (mình|chúng mình|tụi mình|kênh|page|fanpage|shop) để (biết|xem|cập nhật|nhận|không bỏ lỡ|đón)|để (biết|xem) thêm (nhiều )?(mẹo|tips|bí quyết|thông tin)", "CTA mẫu ('lưu video này lại', 'theo dõi mình để biết thêm mẹo'). Hứa cụ thể: mai đăng gì, tập sau nói gì."),
    ("B6-SOCIAL", r"\b(worth (your time|a read|reading|checking out)|don'?t sleep on|thank me later|save this)\b", "Generic social closer."),
    ("B10-SKELETON", None, "Bộ xương bài văn mẫu: 'Trước hết… Thứ hai… Cuối cùng'. Bỏ số thứ tự, để ý tự nối."),
    ("B12-REASSURE", r"yên tâm (nhé|nha|đi)\b|đừng lo( lắng)?( nữa)?[!,.]|bạn không (hề )?(đơn độc|cô đơn|một mình)|đã đến lúc (bạn |để )|tin vui( là| cho bạn)|(hãy|cứ) yên tâm|không cần (phải )?lo", "Câu trấn an theo mẫu quảng cáo ('Đừng lo!', 'Đã đến lúc…'). Nói thẳng giải pháp."),
    ("B13-CAPSLINE", None, "Dòng viết hoa toàn bộ. Hạ xuống chữ thường, giữ đúng một ý nhấn."),
    ("B14-CORRECT", r"chưa đủ để (khẳng định|kết luận)|không (hề )?đồng nghĩa với( việc)?|không nên nhầm (lẫn )?(với|giữa)|điều này không có nghĩa (là|rằng)|\b(should not be confused with|does not (establish|constitute|imply|mean that)|this is not to say|rather than (simply|merely|just))\b", "Khung 'sửa sai' cho ý không ai nói ('không đồng nghĩa với', 'rather than'). Mid-2026: ≥2 lần/bài là dấu hiệu."),
    ("B15-TEMPLATE", r"nói cách khác,|để (làm|đạt|thực hiện|có) được (điều|mục tiêu|những điều|kết quả) (này|đó|trên)|chính vì (vậy|thế|lý do đó)|với những (lợi ích|ưu điểm|lý do) (trên|kể trên|đó)", "Câu nối theo mẫu bài văn ('Để làm được điều này', 'Chính vì vậy'). Bỏ hoặc nối bằng ý."),
    ("C5-COPULA", r"đóng vai trò (là|như)|được (xem|coi) (là|như)|sở hữu (thiết kế|tính năng|vị trí|không gian|đội ngũ)|tự hào (là|sở hữu|mang đến)", "Né 'là / có'. Dùng 'là', 'có'."),
    ("C5-COPULA", r"\b(serves as|stands as|functions as|refers to)\b", "Copula avoidance. Use is/has."),
    ("C6-STIFF", r"(tiến hành|thực hiện) (việc )?(phân tích|đánh giá|triển khai|nghiên cứu|kiểm tra|xây dựng|xác minh|rà soát|xử lý|khắc phục|sửa chữa|kiểm điểm|đào tạo)", "Động từ rườm ('tiến hành phân tích'). Dùng thẳng 'phân tích'."),
    ("C6-STIFF", r"\b(utiliz(e|es|ed|ing)|leverag(e|es|ed|ing)|facilitat(e|es|ed|ing)|commence[sd]?)\b", "Stiff verb. use / start / help."),
    ("C7-VAGUE", r"gắn liền với|có liên quan (mật thiết )?đến|\b(associated with|in connection with|connected to)\b", "Liên hệ mơ hồ. Nói rõ quan hệ (là CEO, đã dạy, đã tài trợ…)."),
    ("C8-CHALL", r"(dù|mặc dù|bất chấp) (còn |vẫn )?(đối mặt|gặp|tồn tại) (với )?(không ít |nhiều )?(thách thức|khó khăn)|triển vọng (tương lai|phát triển)|\b(despite these challenges|future outlook)\b", "Đoạn 'Thách thức & Triển vọng' rập khuôn. Nêu khó khăn cụ thể, bỏ lạc quan chung."),
    ("C9-HEDGE", r"(có thể|có lẽ) (sẽ )?(có khả năng|tiềm năng)|\b(could potentially|may eventually|might ultimately)\b", "Rào chồng rào. Chọn một."),
    ("C13-MOTIV", None, "Câu chốt truyền cảm hứng theo mẫu ('Hãy bắt đầu ngay hôm nay!', '…cùng chúng mình nhé!'). Kết bằng việc cụ thể hoặc dữ kiện."),
    ("C16-TREND", r"đang là (một )?xu hướng|ngày càng (trở nên )?(phổ biến|quan trọng|cần thiết|cấp thiết|được ưa chuộng|khắt khe)|trong (những|các) năm gần đây|(đang )?trở thành (một )?xu hướng", "Câu 'xu hướng chung' thay cho dữ kiện ('ngày càng trở nên phổ biến'). Nêu số hoặc bỏ."),
    ("C17-CS", r"chúng tôi (luôn|sẽ luôn|không ngừng) (nỗ lực|cố gắng)|chúng tôi (rất |thật sự |thực sự |vô cùng )?(lấy làm tiếc|xin lỗi vì (sự|những|mọi) bất tiện)|(sự|những|mọi) bất tiện (này |có thể )?(đã |mà )?(gây ra|mang lại|xảy ra)|mong (quý khách|anh|chị|bạn|quý anh chị) (thông cảm|hiểu cho|bỏ qua)|chúng tôi (đã|sẽ|luôn) (xem xét|ghi nhận|tiếp thu) (một cách )?(kỹ lưỡng|nghiêm túc|cẩn thận)|cảm ơn [^\n.]{0,30}(đã|vì đã) (tin tưởng|đồng hành|ủng hộ|lựa chọn)|cam kết (mang đến|mang lại|cung cấp|đem đến) (dịch vụ|trải nghiệm|sản phẩm) tốt nhất|rất mong (nhận được|tiếp tục nhận được)|(sự )?hài lòng của (quý khách|khách hàng) là|(chân thành|vô cùng|thành thật|thực sự) xin lỗi (về|vì)|không phù hợp với (tiêu chuẩn|giá trị) (phục vụ|dịch vụ|mà chúng tôi)|mà chúng tôi (luôn )?(hướng đến|theo đuổi|đặt ra)|để bày tỏ (sự áy náy|thiện chí|lòng thành|sự trân trọng)|một lần nữa,? (chúng tôi|xin)|giúp chúng tôi (ngày càng )?(hoàn thiện|cải thiện|phục vụ tốt) hơn|\b(I hope this (email|message) finds you well|I am writing to (inform|provide|update|let you know|follow up)|I'm writing to (inform|provide|update|let you know|follow up)|we sincerely apologize for any inconvenience|please (do not|don't) hesitate to (reach out|contact)|thank you for your (understanding|patience|continued (trust|support))|we remain (fully )?committed to|at your (earliest )?convenience|rest assured|we (truly |greatly )?(value|appreciate) your (business|feedback|patience|understanding)|after a thorough review|please know that)\b", "Giọng nhân viên chăm sóc khách hàng theo mẫu. Nói việc đã làm, việc sẽ làm, có ngày giờ. ≥3 câu/bài = LỖI."),
    ("C2-SUM", r"(^|[.!?]\s+)(có thể nói|có thể thấy|nhìn chung|tóm lại|nói tóm lại|tổng kết lại|kết luận lại|tựu trung lại|như vậy, có thể)\b", "Từ tổng kết sáo. Bỏ, kết bằng dữ kiện cuối (văn người thỉnh thoảng dùng nên chỉ CẢNH BÁO)."),
    ("C19-WRAP", r"(hiểu rõ|nắm (vững|rõ|được)|việc (hiểu|nắm|áp dụng|vận dụng)) [^\n.]{0,60}(giúp|sẽ giúp) (chúng ta|bạn|người đọc|doanh nghiệp|mỗi người)|(video|bài viết|bài) này (dành|là dành) cho bạn|\b(this (one|video|post|article) is for you)\b", "Kết bài rộng kiểu sách giáo khoa ('Hiểu rõ X giúp chúng ta…') hoặc 'bài này dành cho bạn'. Kết bằng ý cụ thể cuối cùng."),
    ("C18-EN", r"\b(I keep coming back to|while everyone else (is|was) still|\*checks notes\*|\(yes, really\)|\(no, seriously\)|to be clear,|I'?m confident that|it'?s worth (mentioning|pointing out)|the beauty of this|in a world where|at the end of the day)\b", "English template phrase (avoid-ai-writing 3.38). Cut or say it plainly."),
    ("A6-LIST", r"^(dưới đây|sau đây) là", "Câu dẫn 'Dưới đây là…'. Thường bỏ được."),
]

# Từ quảng cáo sáo: ≥2 trong 1 đoạn = CẢNH BÁO, ≥3 = LỖI. Cả bài: ≥5 hit và ≥3 hit/100 chữ = LỖI
PROMO_VI = ["đột phá", "vượt trội", "hàng đầu", "đẳng cấp", "tinh hoa", "đỉnh cao", "hoàn hảo", "tuyệt hảo", "sang trọng",
            "độc đáo", "ấn tượng", "toàn diện", "tối ưu", "bền vững", "hệ sinh thái", "hành trình", "kiến tạo", "lan tỏa",
            "chạm đến", "thúc đẩy", "tối đa hóa", "tiềm năng", "giá trị cốt lõi", "bức tranh", "điểm nhấn",
            "đa dạng", "phong phú", "sống động", "đầy cảm hứng", "nép mình", "tọa lạc", "trái tim của", "hòa quyện",
            "thăng hoa", "vươn tầm", "đồng hành", "tận tâm", "uy tín", "chất lượng cao", "vô cùng", "cực kỳ",
            "tuyệt vời", "hoàn toàn mới", "chuyên nghiệp", "khác biệt",
            # thêm 2026-10-28 từ kho văn AI social (Claude, Gemini): sáo quảng cáo Việt
            "mang đến", "trải nghiệm", "chính thức ra mắt", "chính thức khai trương", "chính thức lên sóng", "chính thức mở cửa", "tâm huyết", "tràn đầy", "mọi lúc mọi nơi", "cam kết", "giải pháp",
            "tiện lợi", "linh hoạt", "tận tình", "chu đáo", "an tâm", "thư thái", "khỏe khoắn", "năng động", "phong cách",
            "tinh tế", "ấm cúng", "thoáng đãng", "xinh xắn", "ngập tràn", "rực rỡ", "ngọt ngào", "tươi ngon", "lý tưởng",
            "thỏa sức", "trọn vẹn", "đậm đà", "chuẩn vị", "nâng cao hiệu quả", "nâng cao trải nghiệm", "nâng cao chất lượng cuộc sống", "chinh phục", "bứt phá"]
PROMO_EN = ["crucial", "enhance", "robust", "valuable", "highlight", "emphasiz", "landscape", "seamless", "harness",
            "navigate", "empower", "elevate", "unleash", "streamline", "transformative", "cutting-edge",
            "comprehensive", "ensure", "foster", "align with", "enduring", "key", "dynamic", "innovative", "holistic",
            "vibrant", "cozy", "unforgettable", "perfect blend", "curated", "handcrafted"]

TRANSITIONS = r"^(bên cạnh đó|ngoài ra|thêm vào đó|hơn nữa|đặc biệt|không chỉ vậy|không những thế|quan trọng hơn|mặt khác|đồng thời|additionally|moreover|furthermore|notably)\b"
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF⭐⬆✅❌✔✨]")
VI_CHARS = r"ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
SKELETON = [r"(trước hết|trước tiên|đầu tiên|thứ nhất|một là|first(ly)?)", r"(thứ hai|tiếp theo|tiếp đến|kế đến|hai là|second(ly)?)",
            r"(thứ ba|ba là|third(ly)?)", r"(cuối cùng|sau cùng|finally|lastly)"]
MOTIV = r"bạn xứng đáng (được|có)|^(hãy|cùng|đừng chần chừ|đừng chờ|nhanh tay|còn chờ gì)[^\n]{0,90}(ngay|nhé|thôi|hôm nay|nào|bạn nhé)[!.]*$|(cùng|với) (chúng mình|chúng tôi|tụi mình|tụi mình) nhé[!.]*$|(chúc|hẹn gặp) [^\n]{0,40}(nhé|!)$|^(hãy|cùng) (bắt đầu|để|trải nghiệm|biến|tận hưởng|nâng niu|chăm sóc|dành)[^\n]{0,80}$"
ABSTRACT = {"sáng tạo", "hấp dẫn", "giá trị", "hiệu quả", "chuyên nghiệp", "tiện lợi", "nhanh chóng", "an toàn", "chất lượng", "uy tín",
            "hiện đại", "thân thiện", "linh hoạt", "bền vững", "tối ưu", "toàn diện", "mạnh mẽ", "tự tin", "thoải mái", "năng động",
            "phong cách", "tinh tế", "độc đáo", "ấn tượng", "sang trọng", "tiết kiệm", "đơn giản", "dễ dàng", "minh bạch", "rõ ràng",
            "cụ thể", "thiết thực", "ý nghĩa", "cảm hứng", "đam mê", "nhiệt huyết", "trách nhiệm", "tận tâm", "chu đáo", "tận tình",
            "effective", "efficient", "engaging", "scalable", "reliable", "innovative", "creative", "seamless", "secure", "robust",
            "flexible", "powerful", "intuitive", "sustainable", "meaningful", "authentic", "valuable", "actionable", "practical"}
OPENER_SKIP = {  # giữ cho giọng riêng muốn bật lại B9
    "tôi", "mình", "em", "anh", "chị", "bạn", "chúng", "nó", "họ", "và", "nhưng", "mà", "còn", "the", "i", "we", "you",
               "it", "this", "that", "they", "he", "she", "a", "an", "nếu", "khi", "if", "when", "tui", "ông", "bà", "cậu", "bây"}
PROPER_SKIP = {"Bạn", "Anh", "Chị", "Em", "Quý", "Tôi", "Mình", "Chúng", "Shop", "Fanpage", "Inbox", "Hotline", "Zalo", "Facebook",
               "TikTok", "Instagram", "Youtube", "YouTube", "Google", "Chúc", "Hãy", "Đừng", "Lưu", "Tin", "Có", "Không"}


FENCE_OPEN = re.compile(r"^\s{0,3}(`{3,}|~{3,})")


def fence_step(line, fence):
    """Theo dõi khối code theo CommonMark: trả (fence đang mở hoặc None, dòng này có phải dòng fence không).
    Khối mở bằng ``` hay ~~~ (3 dấu trở lên) chỉ đóng bằng cùng ký tự, dài bằng hoặc hơn."""
    if fence:
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})\s*$", line)
        if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
            return None, True
        return fence, False
    m = FENCE_OPEN.match(line)
    return (m.group(1), True) if m else (None, False)


def fm_end(lines):
    """Chỉ số dòng --- đóng frontmatter, hoặc -1. Khối đầu file chỉ là frontmatter khi đóng lại và có dòng key: value
    (một đường kẻ --- mở đầu đoạn sửa Edit thì không phải frontmatter)."""
    if not lines or lines[0].strip() != "---":
        return -1
    for j in range(1, min(len(lines), 80)):
        if lines[j].strip() == "---":
            return j if any(re.match(r"^\s*[A-Za-z_][\w-]*\s*:", lines[k]) for k in range(1, j)) else -1
    return -1


def strip(text):
    """Bỏ frontmatter, code, trích dẫn, HTML comment; giữ số dòng."""
    lines = text.split("\n")
    end = fm_end(lines)
    out, fence = [], None
    for i, l in enumerate(lines):
        if i <= end:
            out.append("")
            continue
        fence, is_fence = fence_step(l, fence)
        if is_fence or fence or l.lstrip().startswith(">"):
            out.append("")
            continue
        l = re.sub(r"<!--.*?-->", "", l)
        out.append(re.sub(r"`[^`]*`", "", l))
    return out


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def snippet(s, n=60):
    s = s.replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def frontmatter(raw):
    """Đọc frontmatter YAML đơn giản (key: value) thành dict."""
    fm = {}
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end > 0:
            for l in raw[3:end].split("\n"):
                m = re.match(r"^\s*([A-Za-z_][\w-]*)\s*:\s*(.+?)\s*$", l)
                if m:
                    fm[m.group(1).lower()] = m.group(2).strip().strip('"').strip("'")
    return fm


def guess_kind(path="", raw=""):
    """Đoán thể loại: frontmatter `kind:` thắng, rồi tên đường dẫn, rồi doc."""
    k = frontmatter(raw).get("kind", "").lower()
    if k in KINDS:
        return k
    p = (path or "").lower().replace("\\", "/")
    rules = [("social", r"caption|social|\bads?\b|[-_/]ads?[-_/.]|\bposts?\b|bai-dang|tiktok|facebook|\bfb\b|instagram|\big\b|reels|threads|fanpage"),
             ("script", r"script|kich-ban|kịch bản|storyboard|\bvsl\b|\bvoice|loi-doc"),
             ("email", r"e-?mail|\bmail\b|thu-gui|tin-nhan|zalo|reply|tra-loi|inbox|dm[-_]"),
             ("report", r"report|bao-cao|proposal|de-xuat|ke-hoach|plan\b"),
             ("academic", r"hoc-tap|essay|tieu-luan|academic|bai-hoc|thesis|luan-van|khoa-hoc|bai-tap|courses?/")]
    for kind, pat in rules:
        if re.search(pat, p):
            return kind
    return "doc"


def directives(raw):
    """<!-- human-writing: off --> và <!-- hw-allow: ... --> trong file.
    Chỉ thị nằm trong code (``` hoặc ~~~, dòng thụt 4 dấu cách), trong `nháy đơn`, dòng trích dẫn > hay frontmatter chỉ là ví dụ, không tính."""
    lines = raw.split("\n")
    end = fm_end(lines)
    keep, fence = [], None
    for i, l in enumerate(lines):
        if i <= end:
            continue
        fence, is_fence = fence_step(l, fence)
        if is_fence or fence or l.lstrip().startswith(">") or l.startswith("    ") or l.startswith("\t"):
            continue
        keep.append(re.sub(r"`[^`]*`", "", l))
    raw = "\n".join(keep)
    off = bool(re.search(r"<!--\s*human-writing:\s*off\s*-->", raw, re.I))
    allow = set()
    for m in re.finditer(r"<!--\s*hw-allow:\s*([^>]*?)\s*-->", raw, re.I):
        allow |= {c.strip().upper() for c in m.group(1).split(",") if c.strip()}
    return off, allow


def load_voice(name):
    """Nạp voices/<name>.toml (hoặc đường dẫn .toml). Trả dict rỗng nếu không có."""
    if not name:
        return {}
    import tomllib
    path = name if name.endswith(".toml") else os.path.join(VOICE_DIR, name + ".toml")
    if not os.path.isfile(path):
        have = sorted(f[:-5] for f in os.listdir(VOICE_DIR) if f.endswith(".toml")) if os.path.isdir(VOICE_DIR) else []
        raise FileNotFoundError(f"không có giọng '{name}' (tìm ở {path}). Giọng có sẵn: {', '.join(have) or 'không'}")
    with open(path, "rb") as f:
        v = tomllib.load(f)
    v["_path"] = path
    return v


def score_of(errs, warns, words):
    """Điểm AI 0-100: mật độ (3·LỖI + CẢNH BÁO) trên 100 chữ, nén bằng 1 - e^(-d/2.5)."""
    base = max(words, 80)
    d = (3 * len(errs) + len(warns)) / base * 100
    return int(round(100 * (1 - math.exp(-d / 2.5))))


def verdict(score):
    return "sạch" if score < 20 else ("nghi" if score < 50 else "giống AI")


def check(raw, kind="doc", voice=None, allow=None):
    """Trả (errs, warns, words). Mỗi mục: {code, line, found, fix}. `allow` là tập mã được miễn (ghép với hw-allow trong file)."""
    voice = voice or {}
    kind = kind if kind in KINDS else "doc"
    off, allow_file = directives(raw)
    allow = {c.upper() for c in (allow or set())} | allow_file | {c.upper() for c in voice.get("allow", [])}
    if off:
        return [], [], len(raw.split())
    lines = strip(raw)
    text = "\n".join(lines)
    errs, warns = [], []
    social = kind == "social"

    def add(bucket, code, line, found, msg):
        bucket.append({"code": code, "line": line, "found": snippet(found), "fix": msg})

    for code, pat, msg in HARD:
        for m in re.finditer(pat, text, I):
            if code == "D1-DASH" and "–" in m.group(0):
                a, b = text[max(0, m.start() - 1): m.start()], text[m.end(): m.end() + 1]
                if a.isdigit() or b.isdigit():
                    continue
            add(errs, code, line_of(text, m.start()), m.group(0), msg)

    for code, pat, msg in WARN:
        if pat is None:
            continue
        hits = list(re.finditer(pat, text, I))
        if code == "B14-CORRECT" and len(hits) < 2:
            continue
        bucket = errs if (code == "B5-NEG" and len(hits) > 1) or (code == "C17-CS" and len(hits) >= 3) else warns
        for m in hits:
            add(bucket, code, line_of(text, m.start()), m.group(0), msg)

    # Giọng riêng: từ cấm, từ bắt buộc
    for b in voice.get("ban", []):
        for m in re.finditer(b["pattern"], text, I):
            add(errs if b.get("level", "error") == "error" else warns, b.get("code", "V-BAN"), line_of(text, m.start()), m.group(0), b.get("msg", "Từ cấm của giọng này."))
    for r in voice.get("require", []):
        if not re.search(r["pattern"], text, I):
            add(errs if r.get("level", "warn") == "error" else warns, r.get("code", "V-REQ"), 1, r["pattern"], r.get("msg", "Thiếu phần bắt buộc của giọng này."))

    # Đoạn văn
    paras, start = [], 0
    for block in re.split(r"\n\s*\n", text):
        if block.strip():
            paras.append((line_of(text, text.find(block, start)), block))
            start = text.find(block, start) + len(block)

    promo_vi = PROMO_VI + list(voice.get("promo_extra", []))
    total_promo = 0
    for ln, p in paras:
        low = p.lower()
        hits = [w for w in promo_vi if w in low] + [w for w in PROMO_EN if re.search(r"\b" + w, low)]
        total_promo += len(hits)
        pw = max(len(p.split()), 1)
        if len(hits) >= 3 and len(hits) / pw * 100 >= 2:
            add(errs, "C10-PROMO", ln, ", ".join(hits), "Dồn từ quảng cáo/từ AI trong 1 đoạn. Thay bằng dữ kiện cụ thể.")
        elif len(hits) >= 2 and len(hits) / pw * 100 >= 1:
            add(warns, "C10-PROMO", ln, ", ".join(hits), "2 từ quảng cáo/từ AI trong 1 đoạn. Giữ tối đa 1.")
    words = len(text.split())
    if total_promo >= 5 and total_promo / max(words, 1) * 100 >= 3 and not any(e["code"] == "C10-PROMO" for e in errs):
        add(errs, "C10-PROMO", 1, f"{total_promo} từ quảng cáo / {words} chữ", "Từ quảng cáo rải đều cả bài (≥3 từ/100 chữ). Thay bằng dữ kiện: giá, giờ, số, tên.")

    # Câu
    sents = [(line_of(text, m.start()), m.group(0).strip()) for m in re.finditer(r"[^.!?\n]+[.!?…]*", text) if len(m.group(0).split()) >= 3]

    # Từ nối đầu câu
    trans = [(ln, s) for ln, s in sents if re.match(TRANSITIONS, s, re.I)]
    if trans:
        used = [re.match(TRANSITIONS, s, re.I).group(0).lower() for _, s in trans]
        if len(trans) > max(2, words // 150) or len(set(used)) < len(used):
            for ln, s in trans:
                add(warns, "C11-TRANS", ln, s, "Từ nối đầu câu dày hoặc lặp. Bỏ bớt, để ý tự nối ý.")

    # Bộ xương bài văn mẫu
    groups = [g for g in SKELETON if re.search(r"(^|\n|[.!?;:\"“*\-]\s*)(\*\*)?(cách |bước |điều |lý do |phần |mẹo |thứ |step |tip )?" + g + r"\b", text, re.I)]
    if len(groups) >= 3:
        add(warns, "B10-SKELETON", 1, ", ".join(re.search(g, text, re.I).group(0) for g in groups), "Bộ xương bài văn mẫu: 'Trước hết… Thứ hai… Cuối cùng'. Bỏ số thứ tự, để ý tự nối.")

    # Bộ ba "A, B và C": chỉ bắt bộ ba trừu tượng (từ ngắn, không tên riêng, không số), bỏ dòng bảng và danh sách
    prose = "\n".join(l for l in lines if not l.lstrip().startswith(("|", "- ", "* ", "#")) and not re.match(r"^\s*\d+[.)]", l))
    triads = []
    for m in re.finditer(r"([^\W\d_]+(?: [^\W\d_]+){0,2}), ([^\W\d_]+(?: [^\W\d_]+){0,2}),? (và|hoặc|cùng|and|or) ([^\W\d_]+(?: [^\W\d_]+){0,2})", prose):
        items = [m.group(1), m.group(2), m.group(4)]
        if any(w[:1].isupper() for it in items for w in it.split()[1:]) or any(it.split()[0][:1].isupper() for it in items[1:]):
            continue
        if not any(it.lower() in ABSTRACT or it.lower().split()[-1] in ABSTRACT for it in items):
            continue
        triads.append(m)
    if len(triads) > 2:
        for m in triads:
            add(warns, "B7-TRIAD", line_of(prose, m.start()), m.group(0), f"{len(triads)} bộ ba tính từ trong bài. Chỉ giữ bộ ba nào thật sự có 3 ý.")

    # Nhịp câu, nhịp đoạn
    body = [s for _, s in sents if not s.lstrip().startswith(("#", "-", "*", "|")) and not re.match(r"^\d+\.", s.lstrip())]
    lens = [len(s.split()) for s in body]
    if len(lens) >= 8 and words >= 120:
        cv = statistics.pstdev(lens) / max(1, statistics.mean(lens))
        if cv < 0.35:
            add(warns, "B8-RHYTHM", 1, f"độ lệch nhịp câu = {cv:.2f}", "Câu dài gần bằng nhau, đều như máy. Trộn câu ngắn và câu dài.")
    plens = [len(p.split()) for _, p in paras if not p.lstrip().startswith(("#", "-", "*", "|"))]
    if len(plens) >= 4 and words >= 120 and statistics.pstdev(plens) / max(1, statistics.mean(plens)) < 0.25:
        add(warns, "B8-RHYTHM", 1, "các đoạn dài gần bằng nhau", "Đoạn văn đều tăm tắp. Có đoạn 1–2 câu, có đoạn dài hơn.")

    # Câu hỏi móc + trấn an (mẫu quảng cáo AI): chỉ social, script, email
    if kind in ("social", "script", "email"):
        head = "\n".join(l for l in lines if l.strip())[:400]
        q = re.search(r"(bạn|anh|chị|các bạn|mọi người)[^?\n]{0,12}(có )?(đang|đã|từng|vẫn|muốn|cảm thấy|thấy|biết|hay)[^?\n]{3,120}\?", head, re.I)
        rea = [w for w in warns if w["code"] == "B12-REASSURE"]
        if q and rea:
            for w in rea:
                warns.remove(w)
            add(errs, "B11-QHOOK", line_of(text, text.find(q.group(0))) if q.group(0) in text else 1, q.group(0), "Mở bằng câu hỏi dò vấn đề rồi trấn an ('Bạn có đang…? Đừng lo!'): mẫu quảng cáo AI. Mở bằng sự thật, con số hoặc tình huống.")

    # Câu chốt truyền cảm hứng (3 dòng chữ cuối)
    tail = [(n, l.strip()) for n, l in enumerate(lines, 1) if l.strip() and not l.strip().startswith("#")][-3:]
    for n, l in tail:
        l = re.sub(r"^(\*\*[^*]{1,30}\*\*\s*|[-*•]\s+|[\"“']+\s*)+", "", l).strip()
        m = re.search(MOTIV, l, re.I)
        if m:
            add(warns, "C13-MOTIV", n, m.group(0), "Câu chốt truyền cảm hứng theo mẫu ('Hãy bắt đầu ngay hôm nay!', '…cùng chúng mình nhé!'). Kết bằng việc cụ thể hoặc dữ kiện.")

    # Dòng viết hoa toàn bộ (≥5 từ chữ)
    for n, l in enumerate(lines, 1):
        ws = [w for w in re.findall(r"[^\W\d_]{2,}", l) if not EMOJI.search(w)]
        if len(ws) >= 5 and all(w.isupper() for w in ws) and not l.strip().startswith("#"):
            add(warns, "B13-CAPSLINE", n, l.strip(), "Dòng viết hoa toàn bộ. Hạ xuống chữ thường, giữ đúng một ý nhấn.")

    # Khối TL;DR (mẫu bắt buộc của workspace: "- **STATUS:** …") được miễn luật D4
    tldr, in_t = set(), False
    for n, l in enumerate(lines, 1):
        if l.lstrip().startswith("#"):
            in_t = "TL;DR" in l.upper()
        elif in_t:
            tldr.add(n)

    # Trình bày theo dòng
    bold_list_run, hr, emoji_bullets, np_run, md_social = 0, 0, 0, 0, 0
    for n, l in enumerate(lines, 1):
        s = l.strip()
        if s.startswith("#"):
            if EMOJI.search(s):
                add(errs, "D2-EMOJIHEAD", n, s, "Emoji trong tiêu đề. Xóa.")
            ws = [w for w in re.sub(r"^#+\s*", "", s).split() if w[:1].isalpha()]
            if len(ws) >= 3 and all(w[:1].isupper() for w in ws) and not all(w.isupper() for w in ws):
                vi = re.search(f"[{VI_CHARS}]", s, re.I)
                add(errs if vi else warns, "D3-TITLECASE", n, s, "Viết Hoa Mọi Chữ trong tiêu đề. Chỉ hoa chữ đầu (và tên riêng).")
            if social:
                md_social += 1
        if n not in tldr and re.match(r"^([-*•–]|\d+[.)])\s+\*\*[^*]+[:.]\*\*|^([-*•–]|\d+[.)])\s+\*\*[^*]+\*\*\s*[:.]", s):
            bold_list_run += 1
            if bold_list_run == 3:
                add(errs, "D4-BOLDLIST", n, s, "Danh sách '- **Nhãn:** mô tả' ≥3 dòng. Bỏ nhãn đậm hoặc viết thành câu.")
        elif s:
            bold_list_run = 0
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s):
            hr += 1
        if s and EMOJI.match(s):
            emoji_bullets += 1
        m = re.match(r"^([-*•]|\d+[.)])\s+(.+)$", s)
        if m and len(m.group(2).split()) <= 4 and not re.search(r"\d|:", m.group(2)):
            np_run += 1
            if np_run == 5:
                add(warns, "D11-NPLIST", n, s, "5+ dòng danh sách toàn cụm ngắn không động từ ('Chất lượng cao / Giá hợp lý'). Viết thành câu có thông tin kiểm được.")
        elif s:
            np_run = 0
    qheads = [l.strip() for l in lines if l.strip().startswith("#") and re.search(r"(là gì|như thế nào|ra sao|tại sao|vì sao|what is|why|how)\s*\??\s*$", l.strip(), re.I)]
    if len(qheads) >= 2:
        add(warns, "D13-QHEAD", 1, " / ".join(qheads[:3]), "Tiêu đề dạng câu hỏi ('X là gì?') lặp: dàn bài FAQ của AI. Đặt tiêu đề là ý chính.")
    if hr >= 2:
        add(warns, "D5-HR", 1, f"{hr} đường kẻ ngang", "Kẻ ngang giữa mọi mục. Bỏ, để tiêu đề tự phân đoạn.")
    if emoji_bullets >= 3:
        add(warns if social else errs, "D10-EMOJIBULLET", 1, f"{emoji_bullets} dòng mở đầu bằng emoji", "Emoji làm dấu đầu dòng. Viết thành câu; social thì tối đa 3 emoji, đặt cuối dòng.")
    if social and (md_social or re.search(r"\*\*[^*\n]+\*\*|\[[^\]\n]+\]\(https?://", text)):
        add(warns, "D12-MARKDOWN", 1, "**đậm**, ## tiêu đề hoặc [chữ](link)", "Markdown trong bài social: Facebook, Zalo, TikTok không hiển thị. Bỏ ký hiệu.")

    bolds = len(re.findall(r"\*\*[^*\n]+\*\*", text))
    if bolds > max(2, words // 250):
        add(warns, "D6-BOLD", 1, f"{bolds} cụm in đậm / {words} chữ", "In đậm dày. Tối đa 1 cụm mỗi mục, hoặc không.")

    tags = re.findall(r"(?:^|(?<=\s))#[^\s#\d)\]][\w]*", re.sub(r"\]\([^)]*\)", "]", text), re.M)
    tag_max = int(voice.get("hashtag_max", 3))
    if len(tags) > 5:
        add(errs, "D7-HASHTAG", 1, " ".join(tags[:8]), "Quá 5 hashtag. Tối đa 3 hashtag cụ thể.")
    elif len(tags) > tag_max and social:
        add(warns, "D7-HASHTAG", 1, " ".join(tags), f"Nhiều hơn {tag_max} hashtag.")

    emojis = EMOJI.findall(text)
    limit = int(voice.get("emoji_max", 3 if social else 0))
    hard_limit = 8 if social else 5
    if len(emojis) > hard_limit:
        add(errs, "D8-EMOJI", 1, "".join(emojis[:10]), f"{len(emojis)} emoji. Văn bản thường: 0; social: tối đa 3, đặt cuối dòng.")
    elif len(emojis) > limit:
        add(warns, "D8-EMOJI", 1, "".join(emojis[:10]), f"{len(emojis)} emoji. Văn bản thường: 0; social: ≤{limit}, đặt cuối dòng.")

    if re.search(r"[“”‘’]", text):
        add(warns, "D9-QUOTE", line_of(text, re.search(r"[“”‘’]", text).start()), "“ ” ‘ ’", "Ngoặc kép cong. Đổi sang \" \" nếu đích dùng ngoặc thẳng (dấu hiệu yếu).")

    mc = re.findall(r"\bmột cách \w+", text, I)
    if len(mc) > 2:
        add(warns, "C12-TRANSL", 1, ", ".join(mc[:5]), "'một cách + tính từ' lặp: văn dịch. 'xử lý một cách nhanh chóng' → 'xử lý nhanh'.")
    pb = re.findall(r"được [^.!?\n,]{1,40} bởi\b", text, I)
    if len(pb) > 1:
        add(warns, "C12-TRANSL", 1, ", ".join(snippet(x, 30) for x in pb[:3]), "Bị động 'được… bởi…' lặp: văn dịch. Đưa người làm lên đầu câu.")

    def keep(f):
        return f["code"] not in allow and f["code"].split("-")[0] not in allow

    key = lambda f: (f["line"], f["code"])
    return sorted([e for e in errs if keep(e)], key=key), sorted([w for w in warns if keep(w)], key=key), words


def run(raw, path="", kind=None, voice=None):
    """Chạy đủ một lượt: đoán kind, nạp giọng, trả dict kết quả có điểm."""
    v = voice if isinstance(voice, dict) else load_voice(voice)
    note = ""
    fv = frontmatter(raw).get("voice")
    if not v and fv:
        try:
            v = load_voice(fv)
        except (FileNotFoundError, ValueError) as e:
            note = f"frontmatter voice: {e}. Chấm không giọng."
    k = kind or v.get("kind") or guess_kind(path, raw)
    errs, warns, words = check(raw, k, v)
    off, _ = directives(raw)
    s = 0 if off else score_of(errs, warns, words)
    return {"file": path or "stdin", "kind": k, "voice": v.get("name", ""), "words": words, "off": off,
            "errors": errs, "warnings": warns, "score": s, "verdict": "bỏ qua" if off else verdict(s), "note": note, "version": VERSION}


def fmt(res):
    out = [f"human-writing {VERSION} · {res['file']} · kind={res['kind']}" + (f" · voice={res['voice']}" if res["voice"] else "")
           + f" · {res['words']} chữ · {len(res['errors'])} LỖI · {len(res['warnings'])} CẢNH BÁO · điểm AI {res['score']} ({res['verdict']})"]
    for title, items in (("LỖI (bắt buộc sửa)", res["errors"]), ("CẢNH BÁO (sửa hoặc nói được lý do giữ)", res["warnings"])):
        if items:
            out.append(f"\n{title}")
            for f in items:
                out.append(f"  dòng {f['line']:<4} {f['code']:<14} «{f['found']}»  → {f['fix']}")
    if res.get("note"):
        out.append("Lưu ý: " + res["note"])
    if res["off"]:
        out.append("File có <!-- human-writing: off -->: bỏ qua.")
    elif not res["errors"] and not res["warnings"]:
        out.append("Sạch.")
    return "\n".join(out)


def iter_dir(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ("node_modules", ".git", "_archive", "_trash_quarantine")]
        for f in sorted(fn):
            if f.lower().endswith((".md", ".txt")):
                yield os.path.join(dp, f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="+", help="một hay nhiều file, - (stdin), hoặc thư mục (với --dir)")
    ap.add_argument("--kind", choices=KINDS, default=None, help="mặc định: đoán từ frontmatter `kind:` hoặc đường dẫn")
    ap.add_argument("--voice", default=None, help="tên file trong voices/ (không đuôi) hoặc đường dẫn .toml; mặc định đọc `voice:` trong frontmatter")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dir", action="store_true", help="quét thư mục, in bảng điểm từng file")
    ap.add_argument("--fail-score", type=int, default=None, help="exit 1 nếu điểm AI >= ngưỡng này")
    a = ap.parse_args()
    try:
        voice = load_voice(a.voice)
    except (FileNotFoundError, ValueError) as e:
        print(f"human-writing: {e}", file=sys.stderr)
        return 2

    def bad(r):
        return bool(r["errors"]) or (a.fail_score is not None and r["score"] >= a.fail_score)

    if a.dir:
        rows = []
        for root in a.file:
            if not os.path.isdir(root):
                print(f"human-writing: --dir cần thư mục, không có: {root}", file=sys.stderr)
                return 2
            for p in iter_dir(root):
                try:
                    raw = open(p, encoding="utf-8").read()
                except (OSError, UnicodeDecodeError):
                    continue
                rows.append(run(raw, p, a.kind, voice))
        n_bad = sum(bad(r) for r in rows)
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            print(f"{'điểm':>4} {'LỖI':>4} {'CB':>4} {'chữ':>6}  {'kind':<8} file")
            for r in sorted(rows, key=lambda r: -r["score"]):
                print(f"{r['score']:>4} {len(r['errors']):>4} {len(r['warnings']):>4} {r['words']:>6}  {r['kind']:<8} {r['file']}")
            print(f"{len(rows)} file, {n_bad} file cần sửa")
        return 1 if n_bad else 0

    results = []
    for f in a.file:
        if f == "-":
            raw, path = sys.stdin.read(), ""
        else:
            try:
                raw = open(f, encoding="utf-8").read()
            except OSError as e:
                print(f"human-writing: không đọc được {f}: {e.strerror}", file=sys.stderr)
                return 2
            path = f
        results.append(run(raw, path, a.kind, voice))
    if a.json:
        print(json.dumps(results[0] if len(results) == 1 else results, ensure_ascii=False, indent=1))
    else:
        print("\n\n".join(fmt(r) for r in results))
    return 1 if any(bad(r) for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
