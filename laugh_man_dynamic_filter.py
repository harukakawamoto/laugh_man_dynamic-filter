import cv2
import numpy as np
from overlay import CvOverlayImage


#gifをpngに直した24つのファイルが入っているフォルダをpathに指定
path = "./laugh_man_list/"

#フォルダに入っているpngファイルをRGBAで読み込む
laugh_man_list = [cv2.imread(path+str(i)+".png",cv2.IMREAD_UNCHANGED) for i in range(24)]

#caskedeの設定
#顔の正面を捉えるcascade
face_cascade_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)

#カメラの読み込み
#Webカメラを指定
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))

#動画終了まで繰り返し
count = 0
while(cap.isOpened()):
        if count==24:
                count=0
        
        #webカメラの読み込み
        ret, frame = cap.read()

        #読み込んだ画像をグレースケースにする
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        #設定したcascadeで画像内の顔の検出を行う
        faces = face_cascade.detectMultiScale(gray)
        
        #検出した分だけ笑い男のフィルターをかける
        for (x,y,w,h) in faces:

                #笑い男フィルターの倍率を設定
                fx = 1.8*w/200

                #倍率分笑い男の画像をリサイズ
                laugh_man = cv2.resize(laugh_man_list[count],dsize=None,fx=fx,fy=fx)

                #笑い男の透過素材をwebカメラでキャプチャした画像に重ねる
                frame = CvOverlayImage.overlay(frame, laugh_man,(x+int(w/2-(200*fx/2)),y+int(h/2-(185*fx/2))))

                #合成結果を出力
                cv2.imshow("Frame",frame)
                cv2.waitKey(10)
        count+=1


        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()    




