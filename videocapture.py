import argparse
import datetime
import os
import sys

import cv2
import numpy as np


def do_main(dev_id, dir_out, cap_sz):
    cap = cv2.VideoCapture(dev_id)
    
    p0, p1 = None, None

    if cap.isOpened():
        scr_sz = np.array([cap.get(3), cap.get(4)], dtype=int)

        # make sure capture size are within screen size
        cap_sz = np.minimum(cap_sz, scr_sz)

        # select the area of capture image
        p0 = (scr_sz - cap_sz) // 2
        p1 = p0 + cap_sz

        print('screen size: {0}, capture size: {1}'.format(scr_sz, cap_sz))
    else:
        print('The capture device [{}] is not ready.'.format(dev_id))
        exit(1)

    while True:
        ret, fram = cap.read()
        
        if ret:
            image = cv2.cvtColor(fram, cv2.COLOR_RGBA2RGB)
            cv2.rectangle(image, tuple(p0 - 2), tuple(p1 + 2), (0, 255, 0), 2)
            cv2.imshow('image', image)
            
            k = cv2.waitKey(100) & 0xFF
            if k == ord('q') or cv2.getWindowProperty('image', 0) == -1:
                break
            elif k == ord('s'):
                now = datetime.datetime.now()
                filename = str(dev_id) + '_' + now.strftime('%Y-%m-%d_%H-%M-%S') + '.png'
                cv2.imwrite(os.path.join(dir_out, filename), image[p0[1]:p1[1], p0[0]:p1[0]])
        else:
            print('error')
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # parsing arguments
    parser = argparse.ArgumentParser(description='Command line argument')
    parser.add_argument('-d', '--device-id', type=int,
                        default=0, help='specify device id of webcam')
    parser.add_argument('-o', '--output-directory', type=str,
                        default='img-captured', help='specify directory to save captured images')
    parser.add_argument('-W', '--width', type=int,
                        default=65535, help='specify width of capturing area')
    parser.add_argument('-H', '--height', type=int,
                        default=65535, help='specify height of capturing area')
    args = parser.parse_args()

    # check and initialize
    if not os.path.isdir(args.output_directory):
        os.mkdir(args.output_directory)

    # run main job for image cropping
    do_main(args.device_id, args.output_directory, np.array([args.width, args.height], dtype=int))
