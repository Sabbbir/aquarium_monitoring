import network
import time

ssid = "Puzzled"  # Replace with your actual SSID
password = "1111122222"  # Replace with your actual password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)


def connect_wifi():
    print("Connecting to WiFi...")
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected(): #use isconnected to check connection
            break
        print(".", end="")
        time.sleep(1)
        max_wait -= 1

    if not wlan.isconnected(): #check if not connected
        print("\nFailed to connect to WiFi.")
        return False
    else:
        print("\nWiFi connected")
        ip = wlan.ifconfig()[0]
        print("IP address:", ip)
        return True



if connect_wifi():
    print("WiFi connection successful!")
    import urequests
    try:
        response = urequests.get("http://google.com")
        print(response.text)
        # response.close()
    except Exception as e:
        print(f"Error making request: {e}")
        print("**Possible reasons for ECONNABORTED:**")
        print("* Network connectivity issue (check internet access)")
        print("* DNS resolution problem (check DNS server settings)")
        print("* Firewall restrictions (consider using a different network)")
        print("* Temporary server issue (try again later)")

# ... (rest of your code)


    while True:
        if not wlan.isconnected(): #check if not connected
            print("Wifi disconnected. Reconnecting...")
            if connect_wifi():
                print("Reconnected!")
            else:
                print("Reconnection failed.")
        time.sleep(2)
else:
    print("Initial WiFi connection failed.")

    