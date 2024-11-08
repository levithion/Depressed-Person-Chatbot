#mental-health-api/ollama_api.py
import requests
import ollama  # Import the Ollama module directly

# Define API endpoints
BASE_URL = "http://127.0.0.1:8877"
LOGIN_URL = f"{BASE_URL}/login"
PROTECTED_URL = f"{BASE_URL}/protected"

# Sample user credentials (replace with actual credentials)
username = "shshank002"
password = "123456"

def get_jwt_token(username, password):
    # Authenticate with the API to obtain JWT token
    response = requests.post(LOGIN_URL, json={"username": username, "password": password})
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)  # Print raw response text

    if response.status_code == 200:
        token = response.json().get("access_token")
        print("JWT token acquired successfully.")
        return token
    else:
        print("Failed to get JWT token:", response.status_code, response.text)
        return None

def access_protected_route(token):
    # Access a protected route using the JWT token
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(PROTECTED_URL, headers=headers)
    return response.json()

def generate_ollama_response(prompt):
    model = "llama3.2"  # Specify the model version
    response = ollama.generate(prompt=prompt, model=model)  # Add model argument
    if 'response' in response:
        return response['response']
    else:
        return "An error occurred while generating the response."

# Main integration function
def main():
    # Step 1: Get JWT token
    token = get_jwt_token(username, password)
    if not token:
        return

    # Step 2: Access a protected route
    protected_data = access_protected_route(token)
    print("Protected route response:", protected_data)

    # Step 3: Use Ollama to generate responses based on user input
    while True:
        # Get prompt from the user
        prompt = input("Enter your prompt for Ollama (or type 'exit' to quit): ")
        if prompt.lower() == "exit":
            break

        # Generate response using Ollama
        ollama_response = generate_ollama_response(prompt)
        print("Ollama response:", ollama_response)

if __name__ == "__main__":
    main()
