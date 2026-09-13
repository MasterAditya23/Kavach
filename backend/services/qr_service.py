import cv2


def decode_qr(image_bytes):
    image_array = bytearray(image_bytes)
    image = cv2.imdecode(
        __import__("numpy").frombuffer(image_array, dtype=__import__("numpy").uint8),
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise ValueError("Invalid image file")

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(image)

    if not data:
        raise ValueError("No QR code found in the image")

    return data