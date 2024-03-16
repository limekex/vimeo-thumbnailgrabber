from cryptography.fernet import Fernet
import os
import requests

# File paths for configuration and encryption key
config_file_path = 'config.txt'
key_file_path = 'key.key'

def generate_key():
    """
    Generates a key and saves it into a file.
    """
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the previously generated key.
    """
    return open(key_file_path, 'rb').read()

def encrypt_message(message):
    """
    Encrypts a message using Fernet symmetric encryption.
    """
    key = load_key()
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message.
    """
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def validate_access_token(access_token):
    """
    Validates the Vimeo access token by making a test API call.
    Returns True if the token is valid, False otherwise.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    test_url = "https://api.vimeo.com/me"
    try:
        response = requests.get(test_url, headers=headers)
        response.raise_for_status()
        return True  # Token is valid
    except requests.exceptions.RequestException:
        return False  # Token is not valid

def get_or_create_access_token():
    """
    Gets the Vimeo access token from the user, validates it, and if valid,
    saves it for future use.
    """
    if not os.path.exists(key_file_path):
        generate_key()

    access_token = None
    if os.path.exists(config_file_path):
        with open(config_file_path, 'rb') as file:
            encrypted_token = file.read()
            access_token = decrypt_message(encrypted_token)
            if not validate_access_token(access_token):
                print("Stored access token is invalid. Please enter a valid access token.")
                access_token = None

    while access_token is None:
        access_token = input("Enter your Vimeo access token: ").strip()
        if validate_access_token(access_token):
            with open(config_file_path, 'wb') as file:
                encrypted_token = encrypt_message(access_token)
                file.write(encrypted_token)
            print("Access token is valid and has been saved.")
        else:
            print("Access token is invalid. Please try again.")
            access_token = None

    return access_token

    if not os.path.exists(key_file_path):
        generate_key()

    if os.path.exists(config_file_path):
        with open(config_file_path, 'rb') as file:
            encrypted_token = file.read()
            access_token = decrypt_message(encrypted_token)
    else:
        print("Hi and welcome to BeTA iTs Vimeo thumbnail grabber. This is the first time you use this application, please provide us with your Vimeo access token. Need help with this, visit our GitHub repository at https://github.com/limekex/vimeo-thumbnailgrabber")
        access_token = input("Enter your Vimeo access token: ").strip()
        with open(config_file_path, 'wb') as file:
            encrypted_token = encrypt_message(access_token)
            file.write(encrypted_token)
    return access_token

def sanitize_filename(filename):
    """
    Removes or replaces characters not allowed in filenames.
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    return filename

def download_video_thumbnails(access_token, channel_id, channel_name):
    """
    Downloads all video thumbnails from the specified Vimeo channel and saves them to a 'downloads' folder.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    base_url = "https://api.vimeo.com"
    url = f"{base_url}/channels/{channel_id}/videos?per_page=50"
    try:
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            sanitized_channel_name = sanitize_filename(channel_name).replace(" ", "_")
            for video in data.get("data", []):
                thumbnail_url = video["pictures"]["sizes"][-1]["link"]
                video_title = f"{sanitized_channel_name}_{sanitize_filename(video['name']).replace(' ', '_')}"
                # Ensure the filename path includes the 'downloads' folder
                file_path = os.path.join('downloads', f"{video_title}.jpg")
                img_data = requests.get(thumbnail_url).content
                with open(file_path, 'wb') as handler:
                    handler.write(img_data)
                    print(f"Downloaded {file_path}")
            
            # Prepare the URL for the next page
            next_page = data["paging"].get("next")  # This is a path, not a complete URL
            if next_page:
                url = base_url + next_page  # Correctly append the base URL
            else:
                break  # Exit the loop if there's no next page

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def main():
    # Create 'downloads' directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    access_token = get_or_create_access_token()

    while True:
        channel_id = input("Enter the Vimeo channel ID or name to download thumbnails: ")
        download_video_thumbnails(access_token, channel_id, channel_id)
        
        continue_download = input("Do you want to download thumbnails from another channel? (yes/no): ")
        if continue_download.lower() != 'yes':
            print("Thank you for using BeTA iTs Vimeo Thumbnail Grabber. Goodbye!")
            break

if __name__ == "__main__":
    main()
