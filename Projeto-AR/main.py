import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import numpy as np
import sys

def get_new_frame(frame, img): 
    mask = img > [0, 0, 0]
    frame = np.where(mask == True, img, frame)
   
    return frame

def create_dic(corners, ids):
    dic = {}
    for i, c in zip(ids, corners):
        dic[i[0]] = c[0].tolist()
    return dic


def get_markers(frame):
    '''Função que pega os marcadores da frame passada como argumento e retorna três listas
    corners (com as coordenadas de cada ID detectado), ids (com o ID detectado) e rejectedImgPoints
    (com as coordenadas rejeitada)'''
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters = parameters)

    return corners, ids, rejectedImgPoints


def draw_img(frame, img_superfice, homography):
    img_superfice[img_superfice == 0] = 1
        
    h, w, _ = frame.shape
    draw   = cv2.warpPerspective(img_superfice, homography, (w, h))
    return draw
    ### https://sublimerobots.com/2015/02/dancing-mustaches/                


def detect(img_name):
    img_reference = cv2.imread("./imgs_board/board_aruco.png")
    img_superfice = cv2.imread("./imgs/" + img_name)
    img_superficie = cv2.resize(img_reference, (img_reference.shape[0], img_reference.shape[1]),  )

    corners_r, ids_r, rejectedImgPoints_r = get_markers(img_reference)
    dic_r = create_dic(corners_r, ids_r)

    video = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video.read()

        corners, ids, rejectedImgPoints = get_markers(frame)

        if len(corners) > 0 :        
            dic = create_dic(corners, ids)
            #frame = aruco.drawDetectedMarkers(frame, corners, ids)
            points_reference = []
            points_frame     = []

            for n_id in ids:
                
                v_r = dic_r[n_id[0]]
                v   = dic[n_id[0]]

                for p in range (4):
                    points_reference.append(v_r[p]) 
                    points_frame.append(v[p])

            homography = cv2.findHomography(np.array(points_reference), np.array(points_frame))
            img = draw_img(frame, img_superfice, homography[0])
            frame = get_new_frame(frame, img)
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect(sys.argv[1])

