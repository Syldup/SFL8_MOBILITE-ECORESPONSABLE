import cv2
import piexif
import time
import numpy as np
from capteur import Capteur


class Camera(Capteur):
    def __init__(self):
        Capteur.__init__(self)
        self.cam = cv2.VideoCapture(0)

    def run(self):
        cv2.namedWindow("Camera")
        while True:
            ret, frame = cam.read()
            cv2.imshow("Camera", frame)
            if not ret:
                break
            k = cv2.waitKey(1)

            if k%256 == 27: # ESC pressed
                print("Escape hit, closing...")
                break

            elif k%256 == 32: # SPACE pressed
                str_time = time.strftime("%Y-%m-%d %H:%M:%S")
                img_name = "{}.jpg".format(str_time)
                if not cv2.imwrite(img_name, frame):
                    raise IOError('Could not write image')
                print("{} written!".format(img_name))

                exif_dict = piexif.load(img_name)
                exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = str_time
                exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = b'N'
                exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = ((47, 1), (13, 1), (57597656, 1000000))
                exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = b'W'
                exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = ((1, 1), (33, 1), (33807678, 1000000))

                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, img_name)

        cam.release()
        cv2.destroyAllWindows()

    def get_value(self):
        ret, frame = cam.read()
        if not ret:
            return None
        self.last_value = self.value
        self.value = None
        return self.value

if __name__=="__main__":
    cam = Camera()
    cam.start()
    cam.join()
