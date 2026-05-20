# DSP Giữa kỳ — Biến đổi Fourier (Mã đề DSP-FOURIER-2026-01)

Bài làm 7 câu kiểm tra giữa kỳ môn Xử lý tín hiệu số (DSP), chương Biến đổi Fourier.
HVCN BCVT — Khoa Kỹ thuật Điện tử 2.

## Cấu trúc

| File | Mô tả |
|------|-------|
| `DSP_BienDoiFourier_GiaiBai.ipynb` | Notebook đầy đủ 7 câu, đã chạy có output |
| `solve_all.py` | Script chạy toàn bộ 7 câu, sinh file PNG kết quả |
| `generate_report.py` | Script sinh file báo cáo Word từ template |
| `build_notebook.py` | Script tạo notebook từ code các câu |
| `DSP_BienDoiFourier_BaoCao_HoanChinh.docx` | Báo cáo hoàn chỉnh (chưa điền MSSV/Họ tên) |
| `cau{1..7}_*.png` | Hình kết quả của 7 câu (dpi=150) |
| `EEGrestingState.mat`, `Lenna.png` | Dataset (do giảng viên cung cấp) |

## Tóm tắt 7 câu

| Câu | Nội dung | Kết quả chính |
|-----|----------|---------------|
| 1 | DFT vòng lặp + chuẩn hoá biên độ | Đỉnh 5 Hz = 3.000, 9 Hz = 1.200 (khớp lý thuyết) |
| 2 | So sánh DFT vòng lặp vs FFT | DFT ~ O(N^1.88), FFT ~ O(N^0.01); tại N=8000 FFT nhanh hơn ~12000× |
| 3 | Nyquist & aliasing | fs=40→alias 5 Hz, fs=60→alias 25 Hz; fs=100, 500 không alias |
| 4 | Lọc Gauss bandpass 14 Hz | SNR cải thiện -6.60 dB → 23.51 dB (+30.12 dB) |
| 5 | STFT chirp 5→50 Hz (L=256, hop=32) | So sánh 3 L với cùng hop=32, thấy rõ đánh đổi Heisenberg |
| 6 | Phổ EEG nghỉ | Delta 43%, Alpha 18% — chứng tỏ trạng thái nghỉ mắt nhắm |
| 7 | Lọc Gauss 2D Lenna | σ=0.05/0.10/0.20: RMSE=22.5/16.4/11.4; giữ 94.4/96.9/98.3% E |

## Chạy lại

```bash
# Yêu cầu: numpy, scipy, matplotlib, pillow, jupyter, python-docx
pip install numpy scipy matplotlib pillow jupyter python-docx

# Chạy toàn bộ 7 câu (sinh PNG)
python solve_all.py

# Build báo cáo Word
python generate_report.py

# Build notebook
python build_notebook.py
```

## Môi trường

- Python 3.12, numpy 2.x, scipy 1.x, matplotlib 3.x
- Linux (đã test), nhưng code chạy được trên Windows/Mac (chỉ cần sửa đường dẫn nếu cần)
