import cv2
import time
import piexif
import pathlib
from Classe.capteur import Capteur
from threading import Thread


class Camera(Capteur):
    def __init__(self, source="."):
        Capteur.__init__(self)
        self.cam = cv2.VideoCapture(0)
        self.frame = None
        self.windows_open = False
        self.source = source
        directory = pathlib.Path(source)
        directory.mkdir(parents=True, exist_ok=True)

    def open_win(self):
        if not self.update_frame():
            return None

        def func():
            self.windows_open = True
            cv2.namedWindow("Camera")
            while True:
                if not self.update_frame():
                    break
                cv2.imshow("Camera", self.frame)
                k = cv2.waitKey(1)

                if k % 256 == 27 or k % 256 == ord('q'):  # ESC pressed
                    print("Escape hit, closing...")
                    break

                elif k % 256 == 32:  # SPACE pressed
                    path = self.get_value()
                    Camera.set_metadata(path)

            self.cam.release()
            cv2.destroyAllWindows()
            self.windows_open = False

        Thread(target=func).start()

    @staticmethod
    def set_metadata(path):
        exif_dict = piexif.load(path)
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = time.strftime("%Y-%m-%d %H:%M:%S")
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = b'N'
        exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = ((47, 1), (13, 1), (57597656, 1000000))
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = b'W'
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = ((1, 1), (33, 1), (33807678, 1000000))

        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, path)

    def set_source(self, source):
        self.source = source

    def update_frame(self):
        ret, frame = self.cam.read()
        if not ret:
            return False

        frame = cv2.flip(frame, 1)
        self.frame = cv2.flip(frame, -1)
        return True

    def get_value(self):
        if not self.windows_open:
            if not self.update_frame():
                return None

        str_time = time.strftime("%Y-%m-%d_%H%M%S")
        img_name = "{}/{}.jpg".format(self.source, str_time)
        if not cv2.imwrite(img_name, self.frame):
            raise IOError('Camera:get_value : Could not write image')
        print("{} written!".format(img_name))

        Camera.set_metadata(img_name)

        self.last_value = self.value
        self.value = img_name
        return self.value


if __name__ == "__main__":
    import os
    import __main__

    main_path = os.path.dirname(__main__.__file__)
    cam = Camera(main_path + "/IMG")

    cam.open_win()

    for i in range(10):
        print(cam.get_value())
        time.sleep(1)
