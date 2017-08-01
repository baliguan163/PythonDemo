import cv2.cv as cv

filename = "../Video/Wildlife.avi"
win_name = "test"
capture = cv.CaptureFromFile(filename)
cv.NamedWindow(win_name, cv.CV_WINDOW_AUTOSIZE)
while 1:
    image = cv.QueryFrame(capture)
    cv.ShowImage(win_name, image)
    c = cv.WaitKey(33)
    if c == 27:
        break
	cv.DestroyWindow(win_name)