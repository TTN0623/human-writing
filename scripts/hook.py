#!/usr/bin/env python3
"""Hook PostToolUse (Write | Edit | MultiEdit) của human-writing: máy ép luật viết như người.

Chạy sau mỗi lần Claude lưu file. Chỉ xét file SẢN PHẨM (.md / .txt trong thư mục sản phẩm, xem SCOPE).
- Write: quét cả file, báo điểm AI. Edit / MultiEdit: chỉ quét đoạn chữ MỚI thêm vào, để sửa một dòng
  trong file cũ không bắt dọn cả file.
- Còn LỖI → trả {"decision": "block"} kèm danh sách lỗi: Claude phải sửa rồi mới đi tiếp.
- Chỉ CẢNH BÁO (với Write) → gửi kèm cho Claude xem, không chặn.
- Thể loại (kind) lấy từ frontmatter `kind:` của file, rồi đoán từ đường dẫn (check.guess_kind).
- Giọng riêng: frontmatter `voice: mau-kenh` nạp voices/mau-kenh.toml.

Lối thoát (ghi trong file):
  <!-- human-writing: off -->               bỏ qua cả file (vd: tài liệu trích nguyên văn, mẫu đối thủ)
  <!-- hw-allow: B5-NEG, D1-DASH -->         cho phép các mã này trong file (vd: slogan brand bắt buộc)
Lỗi trong hook không bao giờ làm hỏng phiên: mọi ngoại lệ đều bị nuốt.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Thư mục sản phẩm (đường dẫn chứa một trong các đoạn này)
SCOPE = ("/outputs/", "/projects/", "/courses/", "/research/", "/team/", "/deliverables/", "/drafts/")
# Không phải văn bản giao cho người đọc
SKIP = ("/.agents/", "/.claude/", "/docs/", "/prompts/", "/_archive/", "/node_modules/", "/materials/",
        "/outputs/browser/", "/_template/", "/.git/", "/evals/corpus/")
SKIP_NAMES = ("PROJECT_REGISTRY.md", "ACTIVE_PROJECT.md")
EXTS = (".md", ".txt")


def in_scope(path):
    p = path.replace("\\", "/")
    if not p.lower().endswith(EXTS) or p.endswith(".transcript.txt"):
        return False
    if os.path.basename(p) in SKIP_NAMES or any(s in p for s in SKIP):
        return False
    return any(s in p for s in SCOPE)


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ""
    if not path or not in_scope(path):
        return

    try:
        whole = open(path, encoding="utf-8").read()
    except OSError:
        whole = ti.get("content", "")

    import check  # cùng thư mục
    off, allow = check.directives(whole)
    if off:
        return

    if tool == "Write":
        text, partial = whole, False
    elif tool == "Edit":
        text, partial = ti.get("new_string", ""), True
    elif tool == "MultiEdit":
        text, partial = "\n\n".join(e.get("new_string", "") for e in ti.get("edits", [])), True
    else:
        return
    if not text.strip():
        return

    fm = check.frontmatter(whole)
    kind = check.guess_kind(path, whole)
    voice = {}
    if fm.get("voice"):
        try:
            voice = check.load_voice(fm["voice"])
        except Exception:
            voice = {}
    errs, warns, words = check.check(text, kind, voice, allow, story=check.is_story(path, whole))
    # Đoạn sửa nhỏ: chỉ ép LỖI; các đo nhịp/độ dày cần cả file mới có nghĩa
    warns = [] if partial else warns
    score = check.score_of(errs, warns, words) if not partial else None

    name = os.path.basename(path)
    where = "đoạn vừa sửa" if partial else "file"
    tag = f"kind={kind}" + (f", voice={voice.get('name', fm.get('voice'))}" if voice else "")

    def fmt(items, n=25):
        lines = [f"- dòng {f['line']} [{f['code']}] «{f['found']}» → {f['fix']}" for f in items[:n]]
        if len(items) > n:
            lines.append(f"- … và {len(items) - n} chỗ nữa (chạy check.py để xem hết)")
        return "\n".join(lines)

    if errs:
        reason = (f"human-writing chặn: {name} ({where}, {tag}) còn {len(errs)} LỖI văn AI. "
                  f"Viết lại các câu này theo ~/.claude/skills/human-writing/SKILL.md rồi lưu lại "
                  f"(số dòng tính trong {where}). Không vá từng chữ.\n{fmt(errs)}"
                  + (f"\n\nCẢNH BÁO kèm theo:\n{fmt(warns, 10)}" if warns else "")
                  + "\nNếu người dùng yêu cầu rõ phải giữ (vd slogan), thêm <!-- hw-allow: MÃ --> vào file và báo người dùng.")
        print(json.dumps({"decision": "block", "reason": reason,
                          "systemMessage": f"human-writing: {name} còn {len(errs)} lỗi văn AI, Claude đang sửa."},
                         ensure_ascii=False))
    elif warns or (score is not None and score >= 20):
        head = f"human-writing: {name} sạch LỖI ({tag}, điểm AI {score} = {check.verdict(score)})."
        body = f" Còn {len(warns)} CẢNH BÁO. Sửa, hoặc giữ nếu có lý do:\n{fmt(warns, 15)}" if warns else ""
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": head + body}},
                         ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
