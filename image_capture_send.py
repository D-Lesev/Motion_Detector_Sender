import glob
import os
from mailing import email_sender
import cv2
import threading


# Starting video capture
# CAP_DSHOW -> faster opening of the main camera
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

first_frame = None
presence = False
count = 1


def clear_folder():
    """Delete all files in the specific folder"""

    images = glob.glob('images/*.png')
    for pic in images:
        os.remove(pic)


while True:
    check_list = []

    # receiving status and the frame from the camera
    status, frame = video.read()

    # reversing the color frame to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # bluring the gray frame
    gray_gausian = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_gausian

    # comparing the first frame with the next one
    delta_frame = cv2.absdiff(first_frame, gray_gausian)

    # applying threshold to the delta frame
    thresh_frame = cv2.threshold(delta_frame, 65, 255, cv2.THRESH_BINARY)[1]

    # increasing white areas in the frame
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # finding the contours
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # with the following if statement we are checking if we have contours
    # if so, we create image and write it
    # also we found the middle one of all the pictures and it's index for future send via email
    for contour in contours:
        if cv2.contourArea(contour) < 5_000:
            check_list.append(False)
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if rectangle.any():
            check_list.append(True)
            presence = True

            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            cur_picture = all_images[index]

    # checking when we dont have contours(only after we already had it)
    # this condition will be triggered only after the object appeared in the camera
    # if this is the case, then creating Thread for multiprocessing of our tasks
    if not any(check_list) and presence:
        presence = False
        email_thread = threading.Thread(target=email_sender, args=(cur_picture, ))
        email_thread.daemon = True

        email_thread.start()
        print("Email send!")

    cv2.imshow("My frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
clear_folder()
