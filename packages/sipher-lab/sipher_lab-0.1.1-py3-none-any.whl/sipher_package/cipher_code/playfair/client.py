import socket
import json

def send_request(task, message, keyword=""):
    """Sends a request to the server and receives the response."""
    try:
        request = {"task": task, "message": message, "keyword": keyword}
        
        # Establish the socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 65432))
        
        # Send request to server
        client_socket.send(json.dumps(request).encode())
        
        # Receive the response from the server
        response = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        
        return response
    except ConnectionRefusedError:
        return "Server is unavailable. Please check the connection."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    while True:
        print("Playfair Cipher Client")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            message = input("Enter the message to encrypt (letters only): ").replace(" ", "").upper()
            keyword = input("Enter the keyword (letters only): ").replace(" ", "").upper()
            if not message.isalpha() or not keyword.isalpha():
                print("Invalid input. Only letters are allowed.")
                continue
            response = send_request("encrypt", message, keyword)
            print("Encrypted message:", response)
        elif choice == '2':
            message = input("Enter the message to decrypt (letters only): ").replace(" ", "").upper()
            keyword = input("Enter the keyword (letters only): ").replace(" ", "").upper()
            if not message.isalpha() or not keyword.isalpha():
                print("Invalid input. Only letters are allowed.")
                continue
            response = send_request("decrypt", message, keyword)
            print("Decrypted message:", response)
        elif choice == '3':
            print("Exiting the client.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
