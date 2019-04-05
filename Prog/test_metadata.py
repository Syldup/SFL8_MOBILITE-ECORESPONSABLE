import cv2
import piexif
import time
import numpy as np

cam = cv2.VideoCapture(0)
cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.jpg".format(img_counter)
        if not cv2.imwrite(img_name, frame):
            raise IOError('Could not write image')
        print("{} written!".format(img_name))

        exif_dict = piexif.load(img_name)

        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = time.strftime("%Y-%m-%d %H:%M:%S")
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = b'N'
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = ((47, 1), (13, 1), (57597656, 1000000))
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = b'W'
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = ((1, 1), (33, 1), (33807678, 1000000))

        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, img_name)

        img_counter += 1

cam.release()
cv2.destroyAllWindows()
