import cv2
from database import sql_database
import numpy as np
from pyzbar.pyzbar import decode


class inserter(object):
    def __init__(self, device_id):
        self.device_id = device_id
        self.video = cv2.VideoCapture(self.device_id)
        self.video.set(4, 480)
        self.empty_list = []
        self.item_to_remove = []
        self.i = 0

    def __del__(self):
        self.video.release()

    def add_product(self):
        ret, frame = self.video.read()
        sql_con = sql_database()  # connecting to db
        myDataList = sql_con.get_data()  # getting data from db
        for barcode in decode(frame):  #  decoding the frame captured
            if self.i > 50:  # after 50 frames it enters this loop
                myOutput = "Sucess"
                myColor = (0, 255, 0)
                pts = np.array(
                    [barcode.polygon], np.int32
                )  # using polygon for the shape of the barcode
                pts = pts.reshape((-1, 1, 2))  # reshaping it
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
                product_id = max(self.empty_list)
                if product_id not in self.item_to_remove:
                    self.item_to_remove.append(product_id)
                # we are only selcting item which has max repeatation of barcode id in the list
            else:
                myData = barcode.data.decode("utf-8")
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (255, 0, 255), 5)
                pts2 = barcode.rect
                cv2.putText(
                    frame,
                    myData,
                    (pts2[0], pts2[1]),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 0, 255),
                    2,
                )
                self.empty_list.append(
                    myData
                )  # this will append all 50 iteration text barcode id
                self.i += 1
        ret, jpg = cv2.imencode(".jpg", frame)
        return jpg.tobytes(), self.item_to_remove
