import requests
import hashlib
import time
from discord_webhook import DiscordWebhook

# Configuration
url = 'https://example.com'  # Replace with your website URL
discord_webhook_url = 'https://discord.com/api/webhooks/your-webhook-url'  # Replace with your Discord webhook URL
check_interval_seconds = 300  # Check every 5 minutes (adjust as needed)

# Function to fetch website content
def fetch_website_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to fetch {url}. Exception: {str(e)}")
        return None

# Function to send Discord webhook notification
def send_discord_notification(content):
    webhook = DiscordWebhook(url=discord_webhook_url, content=content)
    response = webhook.execute()
    print(f"Notification sent to Discord: {response}")

# Main monitoring loop
def monitor_website():
    previous_content = None

    while True:
        current_content = fetch_website_content(url)
        
        if current_content:
            current_hash = hashlib.sha256(current_content.encode()).hexdigest()
            
            if previous_content is not None:
                previous_hash = hashlib.sha256(previous_content.encode()).hexdigest()
                
                if current_hash != previous_hash:
                    change_detected_msg = f"Change detected on {url}!"
                    send_discord_notification(change_detected_msg)
            
            previous_content = current_content
        
        time.sleep(check_interval_seconds)

# Start monitoring
if __name__ == "__main__":
    monitor_website()
