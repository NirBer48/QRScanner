from msilib.schema import Error
import sys
import cv2
import numpy as np
import webbrowser

class QRDecoder:

    def __init__(self, cap = None, CVDetector = None):

        if cap is None:
           cap = None
        self.cap = cap
        self.CVDetector = cv2.QRCodeDetector()

    def FindCamera(self):
        # Open the device at the ID 0
        self.cap = cv2.VideoCapture(0)
        # Check whether user selected camera is opened successfully.
        if not (self.cap.isOpened()):
            print("Could not open video device")
            
            return False
        else:

            return True

    def DetectAndDecode(self, frame):
        retval, decoded_info, points, straight_qrcode = self.CVDetector.detectAndDecodeMulti(frame)

        if retval: 

            img = cv2.polylines(frame, points.astype(int), True, (0, 0, 255), 3)

            if '' not in decoded_info:
                img = cv2.polylines(frame, points.astype(int), True, (0, 255, 0), 3)
                cv2.imshow("Detected_Image", img)
                cv2.waitKey(1)
                print("~~~~~~~~~~~~~~~~~~~~")
                for i in range(len(decoded_info)):
                    print(f"QR Code {i+1}: {decoded_info[i]}")
                self.Redirect(decoded_info)

            return True, img, None
        else:

            return False, frame, None

    def Capture(self):
        while (True):
            ret, frame = self.cap.read()

            if ret:
                if cv2.waitKey(1) & 0xFF == ord('q'):

                    break

                Detected, img, detected_info = self.DetectAndDecode(frame)

                if (Detected):
                    print("Detected")
                else:
                    print("QR Code Not Detected")
                
                cv2.imshow("Detected_Image", img)

        self.cap.release()
        cv2.destroyAllWindows()

    def Redirect(self, detected_info):
        print(f"{len(detected_info)} QR Codes found, enter the QR code you would like to search")
        index = int(input())

        try:
            webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(detected_info[index - 1])
        except Error:
            print(Error)

        sys.exit()

if __name__ == "__main__":
    detector = QRDecoder()

    if detector.FindCamera():
        detector.Capture()

