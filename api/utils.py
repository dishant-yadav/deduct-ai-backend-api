from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import os


def extract_images(input_path, output_path="video_frames"):

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


def get_objects_from_image(image_path, threshold_value=0.5):
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model(
        "./api/ml_models/keras_model.h5",
        compile=False,
    )

    # Load the labels
    class_names = open("./api/ml_models/labels.txt", "r").readlines()
    # class_names = ["Dead-Body", "Knives", "Drugs", "Ropes", "Blood Stains", "Firearm"]

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open("./" + image_path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    predictions = model.predict(data)

    # print(predictions[0])

    predicted_objects = []

    for index in range(len(predictions[0])):
        class_name = class_names[index][2 : len(class_names[index]) - 1]
        confidence_score = round(predictions[0][index], 5)

        if confidence_score > threshold_value:
            predicted_objects.append(class_name)

        # Print prediction and confidence score
        print((class_name, confidence_score))

    return predicted_objects


def get_objects_from_video(video_path):
    if os.path.isfile(video_path):
        # extract_images(video_path)
        path = os.path.join("video_frames")
        file_list = os.listdir(path)
        print(file_list, "Length", len(file_list))
        predicted_objects = set()
        for file in file_list:
            image_path = os.path.join(path, file)
            predicted_objects_image = get_objects_from_image(image_path)
            print(predicted_objects_image)
            predicted_objects.update(predicted_objects_image)
            os.remove(image_path)

        if os.path.isdir("video_frames"):
            os.rmdir("video_frames")
        return list(predicted_objects)
    else:
        return "File does not exist"


# print(get_objects_from_video("./../static/video.mp4"))


# get_objects_from_image("image1.jpeg")
