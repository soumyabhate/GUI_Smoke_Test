#!/usr/bin/env python3
import cv2, numpy as np

def main():
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    cv2.putText(img, 'Hello Jetson!', (50, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Test Window', img)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
