import cv2

def list_available_cameras():
    available_cameras = []
    index = 0
    while index<10:
        print("checking camera ", index)
        try:
            cap = cv2.VideoCapture(index)
        except:
            print("camera ", index, " not found")
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
