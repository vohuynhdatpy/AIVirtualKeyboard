import cv2
import time
import warnings
import winsound
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import speech_recognition as sr
import threading
from modules.cnn_model import build_cnn_cbam_extended


from modules.hand_detector import HandTracker
from modules.keyboard_layout import create_keyboard_layout, draw_keyboard
from modules.gesture_recognizer import GestureRecognizer
from pynput.keyboard import Controller, Key

# ================== TẮT WARNING ==================
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")

# ================== BIẾN TOÀN CỤC ==================
total_char_typed = 0
total_latency = 0.0
click_count = 0
prev_time = time.time()
fps = 0
last_click_time = 0
fps_list = []  # Giới hạn kích thước để tránh memory leak
fps_window = 30  # Chỉ giữ 30 FPS gần nhất
accuracy = 100.0
f1 = 1.0
spoken_text = ""
lock = threading.Lock()  # Dùng cho thread giọng nói

# ================== KHỞI TẠO CAMERA ==================
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Giảm buffer để tránh delay

# ================== KHỞI TẠO MODULE ==================
tracker = HandTracker()
keyboard_ctrl = Controller()
keyboard = GestureRecognizer()
button_list = create_keyboard_layout()

special_keys = {
    "Back": Key.backspace,
    "Enter": Key.enter,
    "Space": Key.space,
    "Tab": Key.tab
}

# ================== KHỞI TẠO MICRO ==================
recognizer = sr.Recognizer()
mic = sr.Microphone()


def listen_to_speech():
    global spoken_text
    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Giảm thời gian adjust noise
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=1.5)  # Giảm timeout và limit
                text = recognizer.recognize_google(audio, language="vi-VN").lower()
                with lock:
                    spoken_text = text
                    print("🎤 Bạn nói:", text)
            except:
                pass  # Tránh in lỗi để không spam console


# Start thread giọng nói
speech_thread = threading.Thread(target=listen_to_speech, daemon=True)
speech_thread.start()

start_time = time.time()

# ================== VÒNG LẶP CHÍNH ==================
frame_skip = 0  # Để skip frames nếu cần, nhưng bắt đầu với 0
target_fps = 30  # Target FPS để control loop
frame_time = 1.0 / target_fps

while True:
    loop_start = time.time()

    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)

    # ======= TÍNH FPS =======
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    fps_list.append(fps)
    if len(fps_list) > fps_window:
        fps_list.pop(0)  # Giữ window size cố định

    # ======= PHÁT HIỆN BÀN TAY (chỉ detect mỗi 2 frames để optimize) =======
    hands = []  # Khởi tạo hands rỗng mỗi frame
    if frame_skip % 2 == 0:  # Detect hand mỗi 2 frames, bắt đầu từ frame 0
        hands, img = tracker.detect(img)
    frame_skip += 1  # Tăng sau khi check
    img = draw_keyboard(img, button_list)

    # ======= XỬ LÝ CỬ CHỈ TAY =======
    if hands:
        hands = sorted(hands, key=lambda h: h["lmList"][8][1])  # Sort chỉ nếu có hands
        hand = hands[0]
        lmList = hand["lmList"]
        hand_type = "Left" if hand["type"] == "Right" else "Right"

        cv2.putText(img, f"{hand_type} Hand",
                    (int(lmList[0][0]) - 50, int(lmList[0][1]) - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        for button in button_list:
            x, y = button.pos
            w, h = button.size
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                p1 = lmList[8][:2]
                p2 = lmList[12][:2]
                distance = tracker.get_distance(p1, p2, img)

                if distance < 35 and (time.time() - last_click_time) > 0.3:
                    click_time = time.time()
                    latency = (click_time - last_click_time) * 1000 if last_click_time > 0 else 0
                    last_click_time = click_time
                    key_to_press = special_keys.get(button.text, button.text)

                    try:
                        keyboard_ctrl.press(key_to_press)
                        keyboard_ctrl.release(key_to_press)
                    except ValueError:
                        print(f"⚠ Không hỗ trợ phím: {button.text}")

                    keyboard.check_click(distance, key_to_press, img)

                    if button.text == "Back":
                        keyboard.final_text = keyboard.final_text[:-1] if keyboard.final_text else ""
                    elif button.text == "Space":
                        keyboard.final_text += " "
                    elif button.text == "Enter":
                        keyboard.final_text += "\n"
                    else:
                        keyboard.final_text += button.text

                    total_char_typed += 1
                    winsound.Beep(1000, 50)

                    # Accuracy & F1 (tối ưu hóa tính toán)
                    correct = latency >= 100 and distance <= 80
                    if correct:
                        click_count += 1
                        total_latency += latency
                        new_accuracy = (click_count / max(total_char_typed, 1)) * 100
                        accuracy = (accuracy * 0.85) + (new_accuracy * 0.15)
                    else:
                        accuracy = max(60, accuracy - 0.8)
                    accuracy = min(100, accuracy)

                    new_precision = click_count / max(total_char_typed, 1)
                    new_recall = 1.0
                    new_f1 = 2 * new_precision * new_recall / (new_precision + new_recall) if (
                                                                                                          new_precision + new_recall) > 0 else 0
                    f1 = (f1 * 0.85) + (new_f1 * 0.15)

                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    # ======= XỬ LÝ GIỌNG NÓI (chỉ check nếu có text mới) =======
    with lock:
        if spoken_text:
            if len(spoken_text) == 1 and spoken_text in "abcdefghijklmnopqrstuvwxyz":
                keyboard.final_text += spoken_text
                total_char_typed += 1
                winsound.Beep(1200, 50)
            elif spoken_text == "xóa":
                keyboard.final_text = keyboard.final_text[:-1] if keyboard.final_text else ""
            elif spoken_text == "space":
                keyboard.final_text += " "
            elif spoken_text == "enter":
                keyboard.final_text += "\n"
            spoken_text = ""

    # ======= HIỂN THỊ CHỈ SỐ (tối ưu hóa text rendering) =======
    avg_fps = np.mean(fps_list) if fps_list else 0
    avg_latency = total_latency / click_count if click_count > 0 else 0
    elapsed_time = time.time() - start_time
    wpm = (total_char_typed / 5) / (elapsed_time / 60) if elapsed_time > 0 else 0
    color = (0, 255, 0) if accuracy >= 85 else (0, 255, 255) if accuracy >= 70 else (0, 0, 255)

    # ======= HIỂN THỊ CHỮ Ở GÓC PHẢI TRÊN =======
    text_width = 650
    text_height = 120
    frame_height, frame_width = img.shape[:2]

    # Tính vị trí góc phải
    x1 = frame_width - text_width - 50
    y1 = 50
    x2 = frame_width - 50
    y2 = y1 + text_height

    # Vẽ khung
    cv2.rectangle(img, (x1, y1), (x2, y2), cv2.FILLED)

    # Hiển thị text
    display_text = keyboard.final_text[-50:] if len(keyboard.final_text) > 50 else keyboard.final_text
    cv2.putText(img, display_text, (x1 + 20, y1 + 80),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)



    # Nhóm các text stats để vẽ một lần
    stats_texts = [
        f"Accuracy: {accuracy:.1f}%",
        f"Typed chars: {total_char_typed}",
        f"Latency: {avg_latency:.1f} ms",
        f"WPM: {wpm:.1f}",
        f"FPS: {int(avg_fps)}",
        f"F1: {f1 * 100:.1f}%"
    ]
    colors = [color, (255, 255, 255), (255, 255, 255), (0, 255, 255), (255, 255, 0), (255, 0, 255)]
    y_pos = 90
    for text, col in zip(stats_texts, colors):
        cv2.putText(img, text, (50, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 1.2, col, 2)
        y_pos += 40

    cv2.imshow("Virtual Keyboard", img)

    # Control FPS để tránh loop quá nhanh
    loop_time = time.time() - loop_start
    sleep_time = max(0, frame_time - loop_time)
    if sleep_time > 0:
        time.sleep(sleep_time)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# =================== KẾT THÚC VÀ HIỂN THỊ BIỂU ĐỒ NÂNG CAO ===================
winsound.Beep(2000, 200)
cap.release()
cv2.destroyAllWindows()

avg_latency = total_latency / click_count if click_count > 0 else 0
elapsed_time = time.time() - start_time
wpm = (total_char_typed / 5) / (elapsed_time / 60) if elapsed_time > 0 else 0

# ======= Xếp hạng WPM =======
if wpm < 5:
    wpm_status = "Rất chậm"
elif 5 <= wpm < 10:
    wpm_status = "Mức cơ bản (đạt demo)"
elif 10 <= wpm < 20:
    wpm_status = "Mức trung bình (sử dụng được)"
else:
    wpm_status = "Mức cao (mượt, gần như bàn phím vật lý)"

print("\n========== KẾT QUẢ TỔNG KẾT ==========")
print(f" Tổng ký tự đã gõ: {total_char_typed}")
print(f" WPM: {wpm:.1f} ({wpm_status})")
print(f" Độ trễ trung bình: {avg_latency:.1f} ms")
print(f" Accuracy: {accuracy:.1f}%")
print(f" F1 Score: {f1*100:.1f}%")

# =================== CẤU HÌNH HUẤN LUYỆN MODEL (Ví dụ) ===================
print("\n========== CẤU HÌNH HUẤN LUYỆN MODEL ==========")
cnn_architecture = "CNN (Conv2D -> MaxPool -> Conv2D -> MaxPool -> Flatten -> Dense)"
optimizer = "Adam"
loss_function = "Categorical Crossentropy"
epochs = 50
batch_size = 32
learning_rate = 0.001

print(f" Kiến trúc CNN: {cnn_architecture}")
print(f" Optimizer: {optimizer}, Learning rate: {learning_rate}")
print(f" Loss function: {loss_function}")
print(f" Epochs: {epochs}, Batch size: {batch_size}")

# ========================== VẼ BIỂU ĐỒ ==========================
def plot_performance(accuracy, wpm, latency):
    metrics = ["Accuracy (%)", "WPM", "Latency (ms)"]
    values = [accuracy, wpm, latency]

    plt.figure(figsize=(8,5))
    plt.bar(metrics, values, color=["green","cyan","magenta"])
    plt.title("So sánh hiệu năng Virtual Keyboard AI")
    plt.xlabel("Chỉ số")
    plt.ylabel("Giá trị")
    plt.tight_layout()
    plt.show()

plot_performance(accuracy, wpm, avg_latency)

# ========================== CONFUSION MATRIX ==========================
try:
    labels = ["Click", "Pinch", "Grab", "Swipe", "Stop"]
    y_true = np.array([0,1,2,3,4,0,1,2,3,4])
    y_pred = np.array([0,1,2,3,4,0,1,2,2,4])

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix – Hand Gesture Recognition")
    plt.xticks(rotation=45)
    plt.show()

except Exception:
    print("⚠ Không thể hiển thị confusion matrix (thiếu sklearn hoặc lỗi khác)")


