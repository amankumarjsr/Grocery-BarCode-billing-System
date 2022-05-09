import cv2
from database import sql_database
import numpy as np
from pyzbar.pyzbar import decode


class reader:
    def __init__(self, device_id):
        self.device_id = device_id
        self.video = cv2.VideoCapture(self.device_id)
        self.video.set(3, 640)
        self.video.set(4, 480)
        self.selected_data = []

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        sql_con = sql_database()  # connecting to db
        myDataList = sql_con.get_data()  # getting data from db
        for barcode in decode(frame):
            myData = barcode.data.decode("utf-8")  # decoding frame
            if myData in myDataList:  # if barcode is present the database
                myOutput = "Sucess"
                myColor = (0, 255, 0)
                if myData not in self.selected_data:
                    self.selected_data.append(myData)
            else:
                myOutput = "Failed"  # if barcode not present the database
                myColor = (0, 0, 255)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, myColor, 5)
            pts2 = barcode.rect
            cv2.putText(
                frame,
                myOutput,
                (pts2[0], pts2[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                myColor,
                2,
            )
        ret, jpg = cv2.imencode(".jpg", frame)
        return jpg.tobytes(), self.selected_data
