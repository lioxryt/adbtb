import subprocess
import os
import re
os.system("clear")

def run_adb_command(command):
    try:
        result = subprocess.check_output(["adb"] + command.split(), universal_newlines=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {e}")
        return None

def main():
    print("Welcome to the Android Debug Bridge Toolbox")
    while True:
        result = run_adb_command(f"devices")
        device_id = result.split("\n")[1].split("\t")[0] if len(result.split("\n")) > 1 else None
        if device_id:
            print(f"Currently Connected to {device_id}")
        else:
            print("No device connected.")
        menu_options = """\n 1. Device Options\n 2. Power Options\n 3. Device Settings\n 4. Interact\n 5. Edit Files\n 6. Open URL\n 7. App Options\n 8. Phone Options\n 9. Device Shell\n exit"""
        print(menu_options)
        choice = input("Select an option: ")
        if choice == "1":
            while True:
                menu_options = """\n 1. Show Devices\n 2. Connect Device\n 3. Disconnect Device\n 4. Switch to TCP/IP mode\n back"""
                print(menu_options)
                choice = input("Select an option: ")
                if choice == "1":
                    devices_output = run_adb_command("devices")
                    if devices_output:
                        print(devices_output)
                    else:
                        print("No connected devices.")
                elif choice == "2":
                    device_id = input("Enter the device ID to connect: ")
                    # Disconnect all connected devices
                    result = run_adb_command(f"disconnect")

                    # Connect to the specified device
                    result = run_adb_command(f"connect {device_id}")
                    if result and "connected" in result:
                           print(f"Device {device_id} connected successfully.")
                    else:
                           print(f"Failed to connect device {device_id}.")
                elif choice == "3":
                    device_id = input("Enter the device ID to disconnect: ")
                    result = run_adb_command(f"disconnect {device_id}")
                    if result and "disconnected" in result:
                        print(f"Device {device_id} disconnected successfully.")
                    else:
                        print(f"Failed to disconnect device {device_id}.")
                elif choice == "4":
                    port = input("Enter the port for TCP/IP mode (default: 5555): ")
                    port = int(port) if port.isdigit() else 5555
                    result = run_adb_command(f"tcpip {port}")
                    if result and "restarting in TCP mode port" in result:
                            print(f"ADB restarted in TCP/IP mode on port {port}.")
                    else:
                        print(f"Failed to switch ADB to TCP/IP mode on port {port}.")        
                elif choice == "back":
                    os.system("clear")
                    break
                else:
                    print("Invalid choice.")
        elif choice == "2":
         while True:
            power_menu_options = """\n 1. Toggle Screen\n 2. Shutdown\n 3. Restart\n back"""
            print(power_menu_options)
            power_choice = input("Select an option: ")

            if power_choice == "1":
                result = run_adb_command("shell input keyevent 26")
                print("Screen toggled.")               
            elif power_choice == "2":
                result = run_adb_command("shell shell reboot -p")
                print("Device shutdown initiated.")
            elif power_choice == "3":
                result = run_adb_command("shell reboot")
                print("Device restart initiated.")
            elif power_choice == "back":
                os.system("clear")
                break
            else:
                print("Invalid choice.")
        elif choice == "3":
            while True:
                setting_options = """\n 1. Connections\n 2. Resolution\n back"""
                print(setting_options)

                settings_choice = input("Select an option: ")
                if settings_choice == "1":
                            connect_options = """
                        1. Wifi
                        2. Bluetooth
                        """
                            print(connect_options)
                            connect_choice = input("Select an option: ")  
                            if connect_choice == "1":   
                                wifi_options = """
                                1. Enable
                                2. Disable
                                """
                                print(wifi_options) 
                                wifi_choice = input("Select an option: ")  
                                if wifi_choice == "1": 
                                    result = run_adb_command(f"shell svc wifi enable")
                                if wifi_choice == "2": 
                                    result = run_adb_command(f"shell svc wifi disable")
                            if connect_choice == "2":   
                                bt_options = """
                                1. Enable
                                2. Disable
                                """
                                print(bt_options) 
                                bt_choice = input("Select an option: ")  
                                if bt_choice == "1": 
                                    result = run_adb_command(f"shell svc bluetooth enable")
                                if bt_choice == "2": 
                                    result = run_adb_command(f"shell svc bluetooth disable")
                if settings_choice == "2":
                            res_options = """
                        1. Current Resolution
                        2. Set Resolution
                        3. Reset Resolution
                        """
                            print(res_options)
                            res_choice = input("Select an option: ")  
                            if res_choice == "1": 
                                result = run_adb_command(f"shell wm size")
                                print(result)
                            if res_choice == "2":
                                size = input("Input a Custom Resolution (ex:WxH): ") 
                                result = run_adb_command(f"shell wm size {size}")
                                print(result)
                            if res_choice == "3":
                                result = run_adb_command(f"shell wm size reset")
                                print(result)
                elif settings_choice == "back":
                    os.system("clear")
                    break
                else:
                    print("Invalid choice.")
        elif choice == "4":
         while True:
            menu_options = """\n 1. Home Button\n 2. Back Button\n 3. Recent Button\n 4. Run Scrcpy\n back"""
            print(menu_options)
            choice = input("Select an option: ")
            if choice == "1":
                result = run_adb_command(f"shell input keyevent KEYCODE_HOME")
            if choice == "2":
                result = run_adb_command(f"shell input keyevent KEYCODE_BACK")
            if choice == "3":
                result = run_adb_command(f"shell input keyevent KEYCODE_APP_SWITCH")
            if choice == "4":
                command = 'osascript -e \'tell application "Terminal" to do script "clear; scrcpy; exit"\''
                subprocess.call(command, shell=True)
            elif choice == "back":
                os.system("clear")
                break
            else:
                print("Invalid choice.")
        elif choice == "5":
         while True:
            menu_options = """\n 1. Push File\n 2. Pull File\n back"""
            print(menu_options)
            choice = input("Select an option: ")
            if choice == "1":
                local = input("Select a Local File: ")
                remote = input("Select a Remote Path: ")
                result = run_adb_command(f"push {local} {remote}")
                if result:
                    print(result)
            elif choice == "2":
                remote = input("Select a Remote File: ")
                local = input("Select a Local Path: ")
                result = run_adb_command(f"pull {remote} {local}")
                if result:
                    print(result)
            elif choice == "back":
                    os.system("clear")
                    break
            else:
                print("Invalid choice.")
        elif choice == "6":
            url = input("Enter ULR: ")
            result = run_adb_command(f"shell am start -a android.intent.action.VIEW -d {url}")
        elif choice == "7":
         while True:
            app_menu_options = """\n 1. List Installed Apps\n 2. Install App\n 3. Extract APK from App\n 4. Uninstall App\n 5. Open App\n back"""
            print(app_menu_options)
            app_choice = input("Select an option: ")

            if app_choice == "1":
                result = run_adb_command("shell pm list packages")
                if result:
                    print("Installed Apps:")
                    print(result)
                else:
                    print("No installed apps found.")
            elif app_choice == "2":
                app_path = input("Enter the path to the APK file: ")
                result = run_adb_command(f"install -r {app_path}")
                if result:
                    print("App installed successfully.")
                else:
                    print("Failed to install the app.")
            elif app_choice == "3":         
                package_name = input("Enter the package name of the app: ")
                local = input("Enter where you want the APK to go: ")
                result = run_adb_command(f"shell pm path {package_name}")
                if result:
                    apk_path = result.split(":")[1].strip()
                    result = run_adb_command(f"pull {apk_path} {local}/{package_name}.apk")
                    print("APK extracted successfully.")
                else:
                    print("Failed to retrieve APK information.")
            elif app_choice == "4":
                package_name = input("Enter the package name of the app: ")
                result = run_adb_command(f"uninstall {package_name}")
                if result:
                    print("App uninstalled successfully.")
                else:
                    print("Failed to uninstall the app.")
            elif app_choice == "5":
                package_name = input("Enter the package name of the app: ")
                result = run_adb_command(f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
                if result:
                    print("App opened successfully.")
                else:
                    print("Failed to open the app.")
            elif app_choice == "back":
                os.system("clear")
                break
            else:
                print("Invalid choice.")
        elif choice == "8":
         while True:
            menu_options = """\n 1. Make Phone Call\n 2. Send SMS\n 3. View All Contacts\n back"""
            print(menu_options)
            choice = input("Select an option: ")
            if choice == "1":
                country_code = input("Enter the country code: ")
                phone_number = input("Enter the phone number: ")
                run_adb_command(f"shell am start -a android.intent.action.CALL -d tel:+{country_code}{phone_number}")
                print(f"Calling {country_code}{phone_number}...")
            elif choice == "2":
                phone_number = input("Enter the phone number: ")
                message = input("Enter the message: ")
                result = run_adb_command(f'shell am start -a android.intent.action.SENDTO -d sms:{phone_number} --es sms_body "{message}" --ez exit_on_sent true')
            elif choice == "3":
                result = run_adb_command(f"shell content query --uri content://com.android.contacts/data --projection display_name:data1")
                print(result)
            elif choice == "back":
                os.system("clear")
                break
            else:
                print("Invalid choice.")
        elif choice == "9":
            command = 'osascript -e \'tell application "Terminal" to do script "clear; adb shell; exit"\''
            subprocess.call(command, shell=True)
            print(f"Accessing device shell. To exit, type 'exit'.")
        elif choice == "exit":
            os.system("clear")
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main() 
