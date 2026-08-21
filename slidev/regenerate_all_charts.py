"""Sinh lại toàn bộ biểu đồ của bộ slide.

Chạy tuần tự 26 script gen_new_ch*_s*.py, mỗi script đọc thẳng CSV trong data/
và ghi PNG vào slidev/public/. Không phụ thuộc thư mục làm việc hiện tại.

    python slidev/regenerate_all_charts.py
"""
import glob
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

SLIDEV_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = SLIDEV_DIR / "public"
SLIDES_MD = SLIDEV_DIR / "slides.md"


def run_script(filepath):
    name = os.path.basename(filepath)
    try:
        subprocess.run(
            [sys.executable, filepath],
            capture_output=True, text=True, encoding='utf-8',
            errors='replace', check=True,
        )
        print(f"  OK   {name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  FAIL {name}")
        print((e.stderr or "").strip()[-500:])
        return False


def required_images():
    """Danh sách ảnh mà slides.md thực sự tham chiếu."""
    import re
    md = SLIDES_MD.read_text(encoding='utf-8-sig')
    return set(re.findall(r'src="\./public/([^"]+)"', md))


def main():
    scripts = sorted(glob.glob(str(SLIDEV_DIR / "gen_new_ch*_s*.py")))
    print(f"Tìm thấy {len(scripts)} script sinh biểu đồ.\n")

    ok = sum(run_script(s) for s in scripts)
    print(f"\nKết quả: {ok}/{len(scripts)} script chạy thành công.")

    need = required_images()
    have = {p.name for p in PUBLIC_DIR.glob("*.png")}
    missing, extra = need - have, have - need

    if missing:
        print(f"\nTHIẾU {len(missing)} ảnh mà slides.md cần:")
        for m in sorted(missing):
            print(f"  - {m}")
    if extra:
        print(f"\nTHỪA {len(extra)} ảnh không slide nào dùng:")
        for x in sorted(extra):
            print(f"  - {x}")
    if not missing and not extra:
        print(f"Khớp chính xác {len(need)} ảnh với slides.md.")

    return 1 if (missing or ok != len(scripts)) else 0


if __name__ == '__main__':
    sys.exit(main())
