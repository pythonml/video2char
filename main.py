import sys
import numpy as np
import time
import curses
import cv2

class VideoConverter(object):
    def __init__(self, video_path):
        self.video_path = video_path
        self.fps = None
        self.pixels = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:oa+>!:+. "

    def video2imgs(self, size=None):
        img_list = []
        cap = cv2.VideoCapture(self.video_path)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
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

    def img2chars(self, img):
        res = []

        height, width = img.shape
        new_img = np.zeros([height*4, width*4])
        new_img.fill(255)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        for row in range(0, height, 2):
            for col in range(0, width, 2):
                percent = img[row][col] / 255
                gray = int(img[row][col])
                index = int(percent * (len(self.pixels) - 1))
                char = self.pixels[index]
                cv2.putText(new_img, char, (col*4, row*4), font, 0.5, gray, 1, cv2.LINE_AA)

        return np.uint8(new_img)

    def imgs2chars(self, imgs):
        video_chars = []
        for img in imgs:
            video_chars.append(self.img2chars(img))

        return video_chars

    def to_char_video(self, video_chars):
        width, height = len(video_chars[0][0]), len(video_chars[0])
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter("out.mp4", fourcc, self.fps, (width, height))
        for img in video_chars:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            out.write(img)
        out.release()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <video path>".format(sys.argv[0]))
        sys.exit(1)
    video_path = sys.argv[1]
    cvt = VideoConverter(video_path)
    imgs = cvt.video2imgs()
    video_chars = cvt.imgs2chars(imgs)
    cvt.to_char_video(video_chars)
