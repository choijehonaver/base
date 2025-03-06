import subprocess
import re
import cv2

def get_video_device_by_port(target_port):
    """
    특정 USB 포트에 연결된 카메라의 /dev/videoX 번호를 반환
    """
    # v4l2-ctl을 사용하여 장치 목록 가져오기
    output = subprocess.run(["v4l2-ctl", "--list-devices"], capture_output=True, text=True).stdout
    
    camera_devices = {}
    current_camera = None

    for line in output.split("\n"):
        if line.strip() == "":
            continue

        # 카메라 이름 가져오기
        if not line.startswith("\t"):
            current_camera = line.strip()

        # /dev/videoX 찾기
        match = re.search(r"(/dev/video\d+)", line)
        if match and current_camera:
            camera_devices[current_camera] = match.group(1)

    # lsusb -t를 사용하여 포트별 정보 가져오기
    usb_output = subprocess.run(["lsusb", "-t"], capture_output=True, text=True).stdout
    for line in usb_output.split("\n"):
        match = re.match(r"\s*\|__ Port (\d+): Dev (\d+), .* Product=(.*)", line)
        if match:
            port, dev, product = match.groups()
            port_id = f"Port {port}"  # 포트 번호

            # 원하는 포트와 제품명이 일치하면 해당 카메라의 /dev/videoX 반환
            if port_id == target_port and product in camera_devices:
                return camera_devices[product]

    return None  # 해당 포트의 카메라를 찾지 못한 경우

# 📌 특정 포트에 연결된 카메라 열기
target_port = "Port 1"  # 원하는 USB 포트 번호 설정
video_device = get_video_device_by_port(target_port)

if video_device:
    print(f"Opening camera at {video_device}")
    cap = cv2.VideoCapture(video_device)

    if cap.isOpened():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Camera Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"Failed to open camera at {video_device}")
else:
    print(f"No camera found at {target_port}")
