import argparse
import datetime
import os
import sys

import cv2


def do_main(dir_out):
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
                now = datetime.datetime.now()
                filename = now.strftime('%Y-%m-%d_%H-%M-%S')
                cv2.imwrite(os.path.join(dir_out, filename + '.png'), image)
        else:
            print('error')

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # parsing arguments
    parser = argparse.ArgumentParser(description='Command line argument')
    parser.add_argument('-o', '--output-directory', type=str,
                        default='img-captured', help='specify directory to save captured images')
    args = parser.parse_args()

    # check and initialize
    if not os.path.isdir(args.output_directory):
        os.mkdir(args.output_directory)

    # run main job for image cropping
    do_main(args.output_directory)
