# OpenCV GUI Smoke Test (Jetson + Docker)

A tiny, reproducible **smoke test** to verify that GUI windows from **inside a Docker container** appear on the Jetson desktop (X11), and that basic OpenCV HighGUI works. This is meant to be committed to your GitHub as a reference/diagnostic.

---

## What this proves
- Your container can access the Jetson display via X11 (`xhost`, `DISPLAY`, `/tmp/.X11-unix` mount).
- OpenCV is installed and can open a window (`cv2.imshow`).
- (Optional) Camera devices can be mapped if you add `--device /dev/videoN` to `docker run`.

> This does **not** run pose estimation or your social-distancing logic. It’s a basic pre-flight check so the real app won’t fail on GUI/display.

---

## Prerequisites (Host)
- Jetson with JetPack (Docker + NVIDIA runtime installed)
- You’re logged in to the Jetson **desktop** (for X11 display)

```bash
# (optional) verify docker works
docker --version
sudo docker info | grep -i runtime
```

---

## 1) Start a display-enabled container (Host)
Use **one** of the following commands:

### A) Plain bash shell (recommended)
```bash
xhost +local:docker

docker run -it --rm --name jetson_dev_wDisplay \
  --runtime nvidia --network host \
  -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v /dev/bus/usb:/dev/bus/usb \
  -v "$HOME/l4t_dev:/app" \
  --workdir /app \
  --entrypoint /bin/bash \
  nvcr.io/nvidia/l4t-ml:r35.2.1-py3
```

### B) If you already have Jupyter running
```bash
# From a *host* terminal, attach a shell into the running container:
docker exec -it jetson_dev_wDisplay bash
```

> Replace the container name if yours differs.

---

## 2) Install minimal deps (Inside the container)
```bash
apt update && apt install -y python3 python3-pip python3-opencv x11-apps
```

---

## 3) Run the smoke test (Inside the container)
Either run the inline block:

```bash
python3 - << 'PY'
import cv2, numpy as np
img = np.zeros((400,400,3), dtype=np.uint8)
cv2.putText(img,'Hello Jetson!',(50,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
cv2.imshow('Test Window', img)
cv2.waitKey(3000)
cv2.destroyAllWindows()
PY
```

**or** run the script in this repo:
```bash
python3 test_opencv_gui.py
```

Expected: a window titled **"Test Window"** appears for ~3 seconds and closes.

---

## Troubleshooting
- **No window / cannot connect to X server**
  - On **host**: `xhost +local:docker`
  - Ensure `-e DISPLAY=$DISPLAY` and `-v /tmp/.X11-unix:/tmp/.X11-unix:rw` are in `docker run`
  - Make sure you’re on X11 desktop (not headless SSH-only session)
- **Wayland session**: log out and select **Xorg/X11** session
- **Need camera later**: add `--device /dev/video0:/dev/video0` (and `/dev/video1` if needed)

---

## GitHub: how to add & push

### New repo
```bash
cd ~/l4t_dev
mkdir -p opencv-gui-smoke-test && cd opencv-gui-smoke-test
# copy files from this folder into here (or unzip the download directly)
git init
git add .
git commit -m "Add OpenCV GUI smoke test for Jetson + Docker"
git branch -M main
git remote add origin https://github.com/<your-username>/opencv-gui-smoke-test.git
git push -u origin main
```

### Existing repo (add as a folder)
```bash
cd ~/l4t_dev/<your-repo>
mkdir -p tools/opencv-gui-smoke-test
# copy these files into tools/opencv-gui-smoke-test
git add tools/opencv-gui-smoke-test
git commit -m "Add OpenCV GUI smoke test (Jetson Docker X11)"
git push
```

---

## Next steps
Once this passes, proceed to build `jetson-inference` and run the pose/DetectNet demos, then your social-distancing script. This smoke test serves as a **baseline**: if later your GUI breaks, you can run this to isolate whether it’s a display/container issue or your app code.
