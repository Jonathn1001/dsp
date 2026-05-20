"""Build a Jupyter notebook from CODE_CAU."""
import os, json, importlib.util
spec = importlib.util.spec_from_file_location("gr", os.path.join(os.path.dirname(__file__), "generate_report.py"))
gr = importlib.util.module_from_spec(spec); spec.loader.exec_module(gr)

cells = []

def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)})

def code(text):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                  "source": text.splitlines(keepends=True)})

md("""# DSP Giữa kỳ — Biến đổi Fourier — Mã đề DSP-FOURIER-2026-01

Notebook giải đầy đủ 7 câu kiểm tra giữa kỳ.

**Yêu cầu:** đặt file `EEGrestingState.mat` và `Lenna.png` trong cùng thư mục với notebook (hoặc sửa đường dẫn ở Câu 6, Câu 7).

## Mục lục
1. DFT vòng lặp và chuẩn hoá biên độ
2. So sánh DFT vòng lặp vs FFT
3. Định lý Nyquist và aliasing
4. Lọc Gauss trong miền tần số (bandpass 14 Hz)
5. STFT cho chirp 5→50 Hz
6. Phân tích phổ EEG thực tế
7. Lọc ảnh Gauss 2D
""")

TITLES = {
    1: "Câu 1 (1.0đ) — DFT vòng lặp và chuẩn hoá biên độ",
    2: "Câu 2 (1.5đ) — So sánh DFT vòng lặp và FFT",
    3: "Câu 3 (1.5đ) — Định lý Nyquist và aliasing",
    4: "Câu 4 (1.5đ) — Lọc tuyến tính trong miền tần số",
    5: "Câu 5 (1.5đ) — Phân tích thời gian–tần số bằng STFT",
    6: "Câu 6 (1.5đ) — Phân tích phổ EEG thực tế",
    7: "Câu 7 (1.5đ) — Lọc ảnh trong miền tần số 2D",
}

for k in range(1, 8):
    md(f"## {TITLES[k]}\n\n**Tóm tắt:** {gr.TOMTAT[k]}\n")
    code(gr.CODE_CAU[k])
    md(f"**Phân tích:**\n\n{gr.PHANTICH[k]}\n")

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.x"},
    },
    "nbformat": 4, "nbformat_minor": 5,
}

out = os.path.join(os.path.dirname(__file__), "DSP_BienDoiFourier_GiaiBai.ipynb")
with open(out, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("Saved:", out)
