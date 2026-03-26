import cv2
import cvzone
import numpy as np

# ================== CẤU HÌNH GIAO DIỆN ==================
KEY_WIDTH = 80
KEY_HEIGHT = 80
GAP = 10
BOTTOM_OFFSET = 50

COLOR_NORMAL = (204, 204, 204)   # xám (#CCCCCC)
COLOR_HOVER = (173, 216, 230)    # xanh nhạt (#ADD8E6)
COLOR_CLICK = (0, 0, 255)        # xanh đậm (#0000FF)
TEXT_COLOR = (0, 0, 0)

# ================== CLASS BUTTON ==================
class Button:
    def __init__(self, pos, text, size=(KEY_WIDTH, KEY_HEIGHT)):
        self.pos = pos
        self.size = size
        self.text = text

# ================== TẠO LAYOUT BÀN PHÍM ==================
def create_keyboard_layout(frame_height=720, frame_width=1280):
    keys = [
        ["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M"],
        ["Space","Back","Enter"]
    ]
    button_list = []

    # Vị trí bắt đầu để bàn phím nằm phía dưới màn hình
    num_rows = len(keys)
    keyboard_height = num_rows * (KEY_HEIGHT + GAP)
    start_y = frame_height - keyboard_height - BOTTOM_OFFSET

    for i, row in enumerate(keys):
        # canh giữa bàn phím theo chiều ngang
        row_width = len(row) * (KEY_WIDTH + GAP) - GAP
        start_x = (frame_width - row_width) // 2

        for j, key in enumerate(row):
            x = start_x + j * (KEY_WIDTH + GAP)
            y = start_y + i * (KEY_HEIGHT + GAP)
            button_list.append(Button((x, y), key))
    return button_list

# ================== VẼ BÀN PHÍM VỚI TRANSPARENCY ==================
def draw_keyboard(img, button_list, hover_button=None, clicked_button=None):
    overlay = img.copy()
    for button in button_list:
        x, y = button.pos
        w, h = button.size

        # Xác định màu nền của phím
        if clicked_button == button:
            color = COLOR_CLICK
        elif hover_button == button:
            color = COLOR_HOVER
        else:
            color = COLOR_NORMAL

        # Vẽ khung bo góc
        cvzone.cornerRect(overlay, (x, y, w, h), 20, rt=0)

        # Vẽ nền phím
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, cv2.FILLED)

        # Vẽ text
        text = button.text
        font_scale = 2
        if text == "Space":
            font_scale = 1.5
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, font_scale, 3)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(overlay, text, (text_x, text_y),
                    cv2.FONT_HERSHEY_PLAIN, font_scale, TEXT_COLOR, 3)

    # Áp hiệu ứng alpha (transparency)
    cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)
    return img
