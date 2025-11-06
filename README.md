# Allow container to access host X server
xhost +local:docker

How to run container with display

docker run -it     --env="DISPLAY"     --env="QT_X11_NO_MITSHM=1"     --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw"     <your_image_name>

OR

docker run -it --volume /dev/bus/usb:/dev/bus/usb --volume $HOME/l4t_dev:/app --workdir /app --runtime nvidia --network host --name jetson_dev_wDisplay --env="DISPLAY=$DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" nvcr.io/nvidia/l4t-ml:r35.2.1-py3

Then, inside docker container:

apt update && apt install -y python3 python3-pip python3-opencv x11-apps

Test:

import cv2
import numpy as np

img = np.zeros((400, 400, 3), dtype=np.uint8)
cv2.putText(img, 'Hello Jetson!', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2.imshow('Test Window', img)
cv2.waitKey(3000)
cv2.destroyAllWindows()
