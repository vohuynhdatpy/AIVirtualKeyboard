🧠 AI Virtual Keyboard — 95% Accuracy Target

Hệ thống bàn phím ảo sử dụng thị giác máy tính (Computer Vision) và trí tuệ nhân tạo (AI), được thiết kế nhằm đạt độ chính xác 95%+ trong việc nhận dạng thao tác gõ phím bằng cử chỉ tay.

🎯 Tính năng chính

✅ Độ chính xác ≥ 95% khi gõ ký tự.

🖐 Nhận dạng tay chính diện (tay phải – tay phải, tay trái – tay trái).

📐 Phát hiện phím chính xác với khoảng cách tolerance.

⏱️ Latency thấp (< 100 ms).

🧮 Hiển thị real-time metrics: Accuracy, WPM (ký tự/phút), Latency, FPS.

🖼️ Bàn phím QWERTY layout trực quan, hiệu ứng hover & click.

🪶 Giao diện nhẹ, mượt — phù hợp real-time camera.

🚀 Cài đặt và chạy
1. Cài đặt dependencies
pip install -r requirements.txt

2. Chạy chương trình chính
python main.py

📐 Giao diện bàn phím

Layout QWERTY:

Hàng 1: Q W E R T Y U I O P

Hàng 2: A S D F G H J K L

Hàng 3: Z X C V B N M

Hàng 4: Space Backspace Enter

Thiết kế phím:

Kích thước: 80×80 pixels

Khoảng cách: 10 pixels

Màu nền: #CCCCCC (xám)

Màu hover: #ADD8E6 (xanh nhạt)

Màu nhấn: #0000FF (xanh đậm)

Hiển thị transparent overlay (alpha = 0.8)

Căn giữa, đặt phía dưới màn hình, offset 50px từ đáy.

🧠 Công nghệ sử dụng

OpenCV — Xử lý ảnh real-time từ camera.

cvzone — Vẽ giao diện UI cho phím.

Mediapipe — Nhận dạng và tracking tay.

Gesture detection (ngón trỏ – ngón giữa) để kích hoạt click.

📊 Real-time Metrics hiển thị
Thông số	Ý nghĩa	Mục tiêu
Accuracy	Độ chính xác ký tự được gõ	≥ 95%
Char/min (WPM)	Số ký tự gõ mỗi phút	≥ 20 ký tự/phút
Latency	Độ trễ trung bình mỗi lần nhấn phím	< 100 ms
FPS	Số khung hình/giây	≥ 30 FPS
Total Typed	Tổng số ký tự đã gõ	≥ 20 để đạt yêu cầu
🕹️ Cách sử dụng

Mở camera:

python main.py


Đặt tay chính diện trong khung camera.

Di chuyển ngón trỏ đến phím cần gõ.

Gập ngón trỏ lại gần ngón giữa để nhấn phím.

Khi gõ, hệ thống hiển thị:

Accuracy

Char/min

Latency trung bình

FPS real-time

Phím tắt:

ESC: Thoát chương trình.

📂 Cấu trúc project
├── main.py                        # Ứng dụng chính
├── modules/
│   ├── hand_detector.py           # Phát hiện tay bằng Mediapipe
│   ├── gesture_recognizer.py     # Nhận dạng cử chỉ click
│   ├── keyboard_layout.py        # Vẽ layout bàn phím QWERTY
│   └── collision_detector.py     # Xử lý va chạm phím (nếu mở rộng)
├── models/
│   └── gesture_model_improved.h5 # Model AI (tuỳ chọn nếu dùng DL)
├── data/
│   └── ...                       # Training data (nếu train thêm)
├── requirements.txt              # Thư viện cần cài
└── README.md

🧪 Điều kiện đạt yêu cầu

Tổng số ký tự gõ ≥ 20 ký tự ✅

Accuracy ≥ 95% ✅

Latency trung bình ≤ 100ms ✅

FPS ≥ 30 ✅

🛠️ Troubleshooting
❌ Accuracy không đạt 95%

Kiểm tra khoảng cách tay và camera

Điều chỉnh ánh sáng → tăng tracking ổn định

Gõ chậm và chính xác hơn để tránh double click

📷 Camera không hoạt động

Kiểm tra camera máy tính (driver/permission)

Thử thay đổi index trong cv2.VideoCapture(0)

🐢 FPS thấp

Giảm độ phân giải camera

Tối ưu số phép vẽ trên frame

Tắt các hiệu ứng không cần thiết

🏆 Kết quả kỳ vọng

📈 Accuracy thực tế ≥ 95%

⚡ Latency trung bình < 100ms

⌨️ Tốc độ gõ ≥ 20 ký tự/phút

🪄 Trải nghiệm thực tế mượt, trực quan, chính xác.

👨‍💻 Tác giả

Tên: Võ Huỳnh Đạt(Nhóm Trưởng)

Trường: Đại học Công nghiệp TP.HCM

Ngành: Khoa học Máy tính-22725911

Tên:Hoàng Việt Khoa(Thành viên)

Trường:Đại học Công nghiệp TP.HCM

Ngành: Khoa học máy tính-22697781

Tên: Dương Xuân Nguyên

Trường:Đại học Công nghiệp TP.HCM

Ngành:Khoa học máy tính-22697951


Năm: 2025-2026

Dự án: AI Virtual Keyboard — Real-time Accuracy 