import cv2
import os


def extractImages(input_path, output_path="images"):
    os.makedirs(output_path, exist_ok=True)
    vid_cap = cv2.VideoCapture(input_path)
    success, image = vid_cap.read()
    count = 0

    while success:
        if not success:
            break
        else:
            cv2.imwrite(
                output_path + "/frame%d.jpg" % count, image
            )  # save frame as JPEG file
            success, image = vid_cap.read()
            print("Read a new frame: ", success)
            count += 1


extractImages("./video.mp4", "images")
