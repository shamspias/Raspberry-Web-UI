from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2


def doorLockSystem():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    found = set()
    res = ""

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            res = barcodeData
            if res:
                break
        if res:
            vs.stop()
            break
    if len(res) != 0:
        return res
    else:
        return res
