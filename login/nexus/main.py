from ultralytics import YOLO
import cv2


import easyocr





# load models
model1 = YOLO('Yolobest.pt')
reader = easyocr.Reader(['en'])
# load video
cap = cv2.VideoCapture(0)


while True:
                ret,frame=cap.read()
                if not ret:
                        break
                image=frame
                results1 = model1(frame)
                
                # Get the first (and only) result

                r1=results1[0]
                
                # Get the bounding boxes for the detected objects

                boxes1=r1.boxes # for faces
                
                # Iterate over the bounding boxes
                if len(boxes1)>0:
                    for box1 in boxes1:
                        # Get the coordinates of the bounding box
                        x11, y11, x22, y22 = [int(i) for i in box1.xyxy[0]]
                        # crop license plate
                        license_plate_crop = frame[int(y11):int(y22), int(x11): int(x22), :]

                        # process license plate
                        license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                        cv2.imshow('threshold',license_plate_crop_gray)
                    # read license plate number
                        
                        result = reader.readtext(license_plate_crop_gray)
                        if result:
                            text = result[0][-2]

                            if text is not None:
                                    print('---------------------------------------------------------------------------------------------------------------------------',type(text))

                                    cv2.putText(image, text, (x11, y11 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                        cv2.rectangle(image, (x11, y11), (x22, y22 ), (0, 255, 255), 2)
                              
                cv2.imshow('image',image)
                if cv2.waitKey(1)==ord('q'):
                    break
            

cap.release()
cv2.destroyAllWindows()

