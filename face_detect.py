import numpy as np
import cv2
import logging

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def scale_jeff_to_face(face_w, face_h, overlay):
    o_h, o_w = overlay.shape[:2]
    new_h = face_h / (o_h * 0.78)
    new_w = face_w / (o_w * 0.78)
    return cv2.resize(overlay, None, fx =new_w, fy =new_h, interpolation = cv2.INTER_CUBIC)



def jeffify(img_folder ="imgs",name = "un",img_fmt = "jpg",overlay_folder="imgs", overlay_png="jeffface"):
    image = "{}/{}.{}".format(img_folder,name, img_fmt)

    print(image)
    img = cv2.imread(image)
    # logging.warn(img.shape)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)


    # cv2.imwrite('what_mid.jpg',img)

    dst = cv2.resize(img, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
    overlay_raw = cv2.imread('{}/{}.png'.format(overlay_folder, overlay_png) , -1)

    logging.info("found {} faces".format(len(faces)))

    for (x,y,w,h) in faces:
        overlay = scale_jeff_to_face(w, h, overlay_raw)
        x_offset=x - 20
        y_offset=y - 20
        for c in range(0,3):
            img[y_offset:y_offset+overlay.shape[0], x_offset:x_offset+overlay.shape[1], c] = overlay[:,:,c] * (overlay[:,:,3]/255.0) +  img[y_offset:y_offset+overlay.shape[0], x_offset:x_offset+overlay.shape[1], c] * (1.0 - overlay[:,:,3]/255.0)


    final_img = "{}_fin.{}".format(name, img_fmt)
    cv2.imwrite("{}/{}".format(img_folder, final_img),img)
    return final_img


if __name__ == "__main__":
    jeffify(img_folder='imgs',name = "un",img_fmt = "jpg", overlay_png="jeffface")