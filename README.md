# ⌨️ AI Virtual Keyboard

A real-time virtual keyboard system controlled entirely by hand gestures — no physical contact required. Built with Computer Vision and AI, achieving **~90% key detection accuracy** on standard consumer hardware.

Presented at **FIT IUH 2025 Faculty Research Conference** → [View Paper](https://ssrc.fit.iuh.edu.vn/conf/article/view/209)

---

## 📸 Demo

> Point your index finger at a key → pinch index + middle finger to press

---

## ✨ Features

- 🖐 Real-time hand tracking via **MediaPipe** (21 landmarks)
- ⌨️ Full **QWERTY layout** with hover and click visual feedback
- 📊 Live metrics overlay: **Accuracy, Char/min, Latency, FPS**
- ⚡ Low-latency inference **< 100ms** on standard laptop hardware
- 🎯 **~90% key detection accuracy** under standard lighting
- 🧠 Optional deep learning gesture model (`gesture_model_improved.h5`)

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `opencv-python` | Video capture & frame rendering |
| `mediapipe` | Hand landmark detection & tracking |
| `cvzone` | UI overlay and keyboard rendering |
| `numpy` | Numerical operations |

---

## ⚙️ Installation

**Requirements:** Python 3.8+

```bash
git clone https://github.com/vohuynhdatpy/AIVirtualKeyboard.git
cd AIVirtualKeyboard
pip install -r requirements.txt
python main.py
```

---

## 🕹️ How to Use

1. Position your hand facing the camera
2. **Move your index finger** over the target key (hover highlight turns blue)
3. **Pinch index + middle finger** together to register a key press
4. Press `ESC` to exit

---

## 📐 Keyboard Layout

```
[ Q ][ W ][ E ][ R ][ T ][ Y ][ U ][ I ][ O ][ P ]
[ A ][ S ][ D ][ F ][ G ][ H ][ J ][ K ][ L ]
[ Z ][ X ][ C ][ V ][ B ][ N ][ M ]
[     Space     ][ Backspace ][ Enter ]
```

- Key size: 80×80px with 10px spacing
- Hover color: light blue | Press color: dark blue | Default: gray
- Transparent overlay (alpha = 0.8), centered at bottom of frame

---

## 📊 Performance

| Metric | Target | Achieved |
|---|---|---|
| Key detection accuracy | ≥ 90% | ~90% |
| Latency per keypress | < 100ms | < 100ms |
| FPS | ≥ 30 FPS | 30+ FPS |
| Typing speed | ≥ 20 char/min | ✅ |

---

## 📁 Project Structure

```
AIVirtualKeyboard/
├── main.py                         # Main application entry point
├── requirements.txt                # Dependencies
├── modules/
│   ├── hand_detector.py            # MediaPipe hand landmark detection
│   ├── gesture_recognizer.py       # Click gesture detection (index + middle pinch)
│   ├── keyboard_layout.py          # QWERTY keyboard rendering
│   └── collision_detector.py       # Key collision / hit detection
├── models/
│   └── gesture_model_improved.h5   # Optional trained gesture model
└── data/                           # Training data (if extending)
```

---

## 🔑 Core Implementation

```python
# Click detection: distance between index tip (8) and middle tip (12)
if distance(landmark[8], landmark[12]) < CLICK_THRESHOLD:
    trigger_key_press(hovered_key)

# Hover detection: index fingertip proximity to key bounding box
for key in keyboard_layout:
    if key.is_hovered(landmark[8]):
        highlight(key)
```

---

## 📄 Research Publication

This project was developed and presented as a research paper at the **FIT IUH 2025 Faculty Research Conference**:

> *AI Virtual Keyboard using Hand Gesture Recognition*
> Võ Huỳnh Đạt, Hoàng Việt Khoa, Dương Xuân Nguyên
> Industrial University of Ho Chi Minh City, 2025
> [📖 Read the paper](https://ssrc.fit.iuh.edu.vn/conf/article/view/209)

---

## 👤 Author

**Võ Huỳnh Đạt** — Computer Science, IUH
- GitHub: [@vohuynhdatpy](https://github.com/vohuynhdatpy)
- LinkedIn: [linkedin.com/in/nimbid](https://www.linkedin.com/in/nimbid/)

---

## 📄 License

MIT License — free to use and modify.
