from detect.up_detector import UpDetector
import cv2
from calculate.utils import show_point


def main():
    ud = UpDetector(device="cuda")
    up_image = cv2.imread("D:/Downloads/g2.jpg")
    up_points = ud.detect(up_image)
    image = show_point(up_image, up_points, if_show=False)
    cv2.imwrite("D:/Downloads/g2_2.jpg", image)
    print(up_points)


if __name__ == "__main__":
    main()
