# Running GUI Applications inside Docker on Jetson (with OpenCV Test)

This guide explains how to run graphical (GUI) applications — like OpenCV’s `cv2.imshow()` — **inside a Docker container** on a Jetson device.  
Normally, containers are isolated from your system’s display, so you have to manually allow them to access the host X server.  
These steps let you view OpenCV windows or run graphical ML demos (like your Jetson mini‑project) directly on the Jetson desktop.

---

## 🧠 What This Does
- **Allows** the container to display GUI windows (by connecting it to your host’s X server).  
- **Runs** an NVIDIA Docker container that has GPU access for ML tasks.  
- **Installs** Python, OpenCV, and basic GUI tools inside the container.  
- **Tests** the setup by showing a “Hello Jetson!” image to confirm display works.

Once this works, you can safely run your real projects (e.g., social‑distancing pose estimation) in the same container.

---

## 🪟 1. Allow container to access host X server
The host’s X server controls your screen. By default, Docker containers can’t open windows on it.  
This command temporarily gives permission for local Docker containers to use your display:

```bash
xhost +local:docker
```

If you ever want to revoke it later:
```bash
xhost -local:docker
```

---

## 🧩 2. How to run a container with display access

### Option A — Basic form
This minimal command attaches the container to your display so GUI windows can open.

```bash
docker run -it     --env="DISPLAY"     --env="QT_X11_NO_MITSHM=1"     --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw"     <your_image_name>
```

### Option B — Full NVIDIA Jetson setup
This command mounts your camera, USB devices, and a shared folder (`~/l4t_dev` → `/app`) and gives GPU access.

```bash
docker run -it   --volume /dev/bus/usb:/dev/bus/usb   --volume $HOME/l4t_dev:/app   --workdir /app   --runtime nvidia   --network host   --name jetson_dev_wDisplay   --env="DISPLAY=$DISPLAY"   --env="QT_X11_NO_MITSHM=1"   --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw"   nvcr.io/nvidia/l4t-ml:r35.2.1-py3
```

**What this does:**
- `--runtime nvidia` → enables GPU acceleration inside container  
- `--env DISPLAY` → passes display variable from host  
- `--volume /tmp/.X11-unix` → connects container to host X server socket  
- `--network host` → shares Jetson’s network (useful for streaming, Jupyter, etc.)  
- `--volume $HOME/l4t_dev:/app` → mounts a shared folder for your work  
- `nvcr.io/nvidia/l4t-ml:r35.2.1-py3` → official NVIDIA ML image for Jetson (includes CUDA, cuDNN, PyTorch, TensorFlow, etc.)  

---

## 🧰 3. Inside the Docker container

Once the container shell opens (prompt looks like `root@<id>:/app#`), install the basic dependencies:

```bash
apt update && apt install -y python3 python3-pip python3-opencv x11-apps
```

**Why:**  
- `python3` → ensures Python runtime is installed  
- `python3-pip` → allows installing extra Python packages if needed  
- `python3-opencv` → provides OpenCV with GUI support  
- `x11-apps` → includes simple GUI tools (for testing X11 setup)  

---

## 🧪 4. Test your setup (Hello Jetson!)

Run this small OpenCV script inside the container:

```bash
import cv2
import numpy as np

img = np.zeros((400, 400, 3), dtype=np.uint8)
cv2.putText(img, 'Hello Jetson!', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2.imshow('Test Window', img)
cv2.waitKey(3000)
cv2.destroyAllWindows()
```

Expected result: a small window appears for ~3 seconds with green “Hello Jetson!” text.

If you see that window, your **display configuration, Docker permissions, and OpenCV GUI** are all working perfectly.

---

## 🎥 5. Output Screenshot

<p align="center">
  <img src="test_command.jpg" alt="Commands on Docker container" width="49%">
  <img src="test_output.jpg" alt="OpenCV window showing Hello Jetson" width="49%">
</p>

---

## 🧠 Why This Matters
This smoke test ensures that:
- Your Docker container can open windows on the Jetson display.  
- OpenCV (and by extension, your ML applications) can render video frames.  
- The setup is ready for advanced scripts like **pose estimation** and **social distancing detection**.

Once confirmed, you can replace this simple test with your actual project code inside the same environment.

---
