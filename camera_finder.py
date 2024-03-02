import cv2

def list_available_cameras():
    available_cameras = []
    index = 0
    while True:
        print("checking camera ", index)
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        ret, _ = cap.read()
        if ret:
            available_cameras.append(index)
        cap.release()
        index += 1
    return available_cameras

# List available cameras
cameras = list_available_cameras()
if cameras:
    print("Available cameras:")
    for index in cameras:
        print(f"Camera {index}")
else:
    print("No cameras available.")
