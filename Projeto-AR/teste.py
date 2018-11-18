import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import numpy as np

def get_markers(frame):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters = parameters)

    return corners, ids, rejectedImgPoints


def draw_img(frame, img_superfice, homography):
    altura, largura , _ = img_superfice.shape
    
    for i in range(altura):
        for j in range(largura):
            
            p_pixel = np.array([[j], [i], [1]])

            mult = np.dot(homography[0], p_pixel).ravel()
                        
            x = int(mult[0]/mult[2])
            y = int(mult[1]/mult[2])
            
            try:
                frame[y][x] = img_superfice[j][i]
                
            except:
                pass

    return frame
 
        
def detect():
    img_reference = cv2.imread("board_aruco.png")
    img_superfice = cv2.imread("t.png")
  
    corners_l, ids_l, rejectedImgPoints_l = get_markers(img_reference)
    
    video = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video.read()

        corners, ids, rejectedImgPoints = get_markers(frame)
    
        if len(corners) > 0 :        
            frame = aruco.drawDetectedMarkers(frame, corners, ids)
                                
            ar_l = []
            ar   = []

            for n_id in ids:
                for i in range(4):
                    ar.append(corners[0][0][i].tolist())
                    ar_l.append(corners_l[0][0][i].tolist())

            homography = cv2.findHomography(np.array(ar_l), np.array(ar))

            frame = draw_img(frame, img_superfice, homography)
            
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

detect()