import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened:
    print('{0} x {1}'.format(cap.get(3), cap.get(4)))

while True:
    ret, fram = cap.read()
    
    if ret:
        image = cv2.cvtColor(fram, cv2.COLOR_RGB2BGR)
        cv2.imshow('image', image)
        
        k = cv2.waitKey(100) & 0xFF
        if k == 27:
            break
        elif k == ord('s'):
            cv2.imwrite('cap.png', image)
    else:
        print('error')

cv2.destroyAllWindows()
