import cv2
import tensorflow as tf
import numpy as np


cap = cv2.VideoCapture(0)  # Use 0 for default camera
model = tf.saved_model.load('C:\Users\gauri\AppData\Roaming\Python\Python312\site-packages\tensorflow')


def is_wearing_cap(frame):
    image_np = np.array(frame)
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]

    detections = model(input_tensor)

    for score, box in zip(detections['detection_scores'][0].numpy(), detections['detection_boxes'][0].numpy()):
        if score > 0.5 and detections['detection_classes'][0][0].numpy() == 1:
            return True

    return False

while True:
    ret, frame = cap.read()
    if not is_wearing_cap(frame):
        # Highlight person
        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 2)
        # Capture image
        cv2.imwrite('captured_image.jpg', frame)
        # Save or send image via email
        # Implement this part based on your requirements
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

import smtplib
from email.message import EmailMessage

def send_email(image_path):
    msg = EmailMessage()
    msg.set_content('Someone is not wearing a cap!')
    msg['Subject'] = 'Cap Detection Alert'
    msg['From'] = 'gaurisharma702722@gmail.com'
    msg['To'] = 'ritikjind2018@gmail.com'

    with open(image_path, 'rb') as f:
        img_data = f.read()
    msg.add_attachment(img_data, maintype='image', subtype='jpg', filename='captured_image.jpg')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('your_email@example.com', 'your_password')
        smtp.send_message(msg)

# Use send_email('captured_image.jpg') to send the email

cap.release()
cv2.destroyAllWindows()
