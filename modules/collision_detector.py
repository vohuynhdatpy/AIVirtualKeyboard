import cv2

def is_finger_on_button(lmList, button):
    x, y = button.pos
    w, h = button.size
    if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
        cv2.rectangle(None, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
        return True
    return False
