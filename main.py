import sys
import numpy as np
import time
import curses
import cv2

def video2imgs(video_name, size=None):
    img_list = []
    cap = cv2.VideoCapture(video_name)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if size:
                img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
            img_list.append(img)
        else:
            break
    cap.release()
    return img_list[:1000]

pixels = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:oa+>!:+. "
def img2chars(img):
    res = []

    height, width = img.shape
    new_img = np.zeros([height*4, width*4])
    new_img.fill(255)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    for row in range(0, height, 2):
        for col in range(0, width, 2):
            percent = img[row][col] / 255
            gray = int(img[row][col])
            index = int(percent * (len(pixels) - 1))
            char = pixels[index]
            cv2.putText(new_img, char, (col*4, row*4), font, 0.5, gray, 1, cv2.LINE_AA)

    return np.uint8(new_img)

def imgs2chars(imgs):
    video_chars = []
    for img in imgs:
        video_chars.append(img2chars(img))

    return video_chars

def play_video(video_chars):
    width, height = len(video_chars[0][0]), len(video_chars[0])
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("out.mp4", fourcc, 20.0, (width, height))
    for img in video_chars:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        out.write(img)
    out.release()

def create_video():
    height = 150
    width = 200
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("out.mp4", fourcc, 20.0, (width, height))
    for i in range(10):
        filename = "{}.png".format(i)
        im = cv2.imread(filename)
        out.write(im)
    out.release()

if __name__ == "__main__":
    imgs = video2imgs("/home/linushen/Downloads/a.mp4")
    video_chars = imgs2chars(imgs)
    play_video(video_chars)
