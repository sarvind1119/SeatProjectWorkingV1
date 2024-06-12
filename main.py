import cv2
import os
import time
def process(img_name):
    import os
    import google.generativeai as genai
    #genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    genai.configure(api_key='AIzaSyD0xo5s6zt1X4z9OCoIcuHAcbA7Z3bNQCc')


    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    generation_config = {
    "temperature": 0.15,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="You will receive an image of a classroom. There will be some empty chairs , some non empty chairs. Give a number to each chair, irrespective of whether it is filled or empty. Mark the empty chairs as empty. I need the following information//nChair Number(C1, C2, C3...), Status(present/absent), Colour of Cloth of people sitting on chair, Sleeping(Y?N).",
    )

    files = [
    upload_to_gemini(img_name, mime_type="image/jpeg"),
    ]
    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            files[0],
            "Give the result in JSON format",
        ],
        }
        # {
        # "role": "model",
        # "parts": [
        #     "```json\n[\n  {\n    \"Chair Number\": \"C1\",\n    \"Status\": \"present\",\n    \"Colour of Cloth\": \"light blue\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C2\",\n    \"Status\": \"present\",\n    \"Colour of Cloth\": \"light blue\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C3\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C4\",\n    \"Status\": \"present\",\n    \"Colour of Cloth\": \"Green\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C5\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C6\",\n    \"Status\": \"present\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C7\",\n    \"Status\": \"present\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C8\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C9\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C10\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C11\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C12\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C13\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C14\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  },\n  {\n    \"Chair Number\": \"C15\",\n    \"Status\": \"empty\",\n    \"Colour of Cloth\": \"Beige\",\n    \"Sleeping\": \"N\"\n  }\n]\n```",
        # ],
        # },
    ]
    )

    response = chat_session.send_message("img")

    print(response.text)

def upload_to_gemini(path, mime_type=None):
    import os
    import google.generativeai as genai
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    print(path)
    return file

# Create a directory to store images if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Create a VideoCapture object to capture video from the webcam
cap = cv2.VideoCapture(0)

# Set the width and height of the capture
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize a counter to keep track of captured images
img_counter = 0

# Set the time to start capturing images
start_time = time.time()

# Main loop to capture and save images
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Display the captured frame (optional)
    cv2.imshow('frame', frame)

    # Check if 60 seconds have passed
    if time.time() - start_time >= 30:
        img_name = "images/img_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        process(img_name)

        # Reset the start time
        start_time = time.time()
        img_counter += 1

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()