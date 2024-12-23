import requests

# Define the server URL
url = "http://127.0.0.1:5000/convert"

# Define the text to convert
data = {"text": "Hello, this is a test message for text-to-speech."}

# File path to save the output
output_path = "/home/nim/Flask_app/output.wav"

try:
    # Send a POST request with the text data
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Audio file saved to {output_path}")
    else:
        print(f"Error: {response.status_code} - {response.json()}")

except Exception as e:
    print(f"An error occurred: {str(e)}")