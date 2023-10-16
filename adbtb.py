import subprocess
import os
import time
os.system("cls")

debug_mode = False

def toggle_debug_mode():
    global debug_mode
    debug_mode = not debug_mode

def run_adb_command(command):
    try:
        adb_command = ["adb"]
        adb_command.extend(command.split())
        
        result = subprocess.check_output(adb_command, universal_newlines=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        if debug_mode:
            print(f"Error executing ADB command: {e}")
        return None

def main():
    print("""\n░█████╗░██████╗░██████╗░████████╗██████╗░  ██████╗░██╗░░░██╗\n██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗  ██╔══██╗╚██╗░██╔╝\n███████║██║░░██║██████╦╝░░░██║░░░██████╦╝  ██████╦╝░╚████╔╝░\n██╔══██║██║░░██║██╔══██╗░░░██║░░░██╔══██╗  ██╔══██╗░░╚██╔╝░░\n██║░░██║██████╔╝██████╦╝░░░██║░░░██████╦╝  ██████╦╝░░░██║░░░\n╚═╝░░╚═╝╚═════╝░╚═════╝░░░░╚═╝░░░╚═════╝░  ╚═════╝░░░░╚═╝░░░\n\n██╗░░░░░██╗░█████╗░██╗░░██╗██████╗░██╗░░░██╗████████╗\n██║░░░░░██║██╔══██╗╚██╗██╔╝██╔══██╗╚██╗░██╔╝╚══██╔══╝\n██║░░░░░██║██║░░██║░╚███╔╝░██████╔╝░╚████╔╝░░░░██║░░░\n██║░░░░░██║██║░░██║░██╔██╗░██╔══██╗░░╚██╔╝░░░░░██║░░░\n███████╗██║╚█████╔╝██╔╝╚██╗██║░░██║░░░██║░░░░░░██║░░░\n╚══════╝╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░""")
    print("Welcome to the Android Debug Bridge Toolbox")
    while True:
        result = run_adb_command(f"devices")
        device_id = result.split("\n")[1].split("\t")[0] if len(result.split("\n")) > 1 else None
        if device_id:
            print(f"Currently Connected to {device_id}")
        else:
            print("No device connected.")
        menu_options = """\n 1. Device Options\n 2. Power Options\n 3. Device Settings\n 4. Interact\n 5. View\n 6. Edit Files\n 7. Remote Open\n 8. App Options\n 9. Phone Options\n 10. Device Shell\n 99. Toggle Debug\n 0. exit\n"""
        print(menu_options)
        choice = input("Select an option: ")
        if choice == "1":
            while True:
                menu_options = """\n 1. Show Devices\n 2. Connect Device\n 3. Disconnect Device\n 4. Switch to TCP/IP mode\n 5. Kill Server\n 0. back\n"""
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
                elif choice == "5":
                    result = run_adb_command("kill-server")
                    if result:
                        print("successfully killed ADB Server")
                elif choice == "0":
                    os.system("cls")
                    break
                else:
                    print("Invalid choice.")
        elif choice == "2":
         while True:
            power_menu_options = """\n 1. Toggle Screen\n 2. Shutdown\n 3. Restart\n 0. back\n"""
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
            elif power_choice == "0":
                os.system("cls")
                break
            else:
                print("Invalid choice.")
        elif choice == "3":
            while True:
                setting_options = """\n 1. Connections\n 2. Volume\n 3. Battery\n 4. Resolution\n 5. Rotation\n 0. back\n"""
                print(setting_options)

                settings_choice = input("Select an option: ")
                if settings_choice == "1":
                            connect_options = """\n 1. Wifi\n 2. Bluetooth\n"""
                            print(connect_options)
                            connect_choice = input("Select an option: ")  
                            if connect_choice == "1":   
                                wifi_options = """
                                1. Enable
                                2. Disable
                                \n"""
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
                                \n"""
                                print(bt_options) 
                                bt_choice = input("Select an option: ")  
                                if bt_choice == "1": 
                                    result = run_adb_command(f"shell svc bluetooth enable")
                                if bt_choice == "2": 
                                    result = run_adb_command(f"shell svc bluetooth disable")
                elif settings_choice == "2":
                    while True:
                        volume_options = """\n 1. Increase Volume\n 2. Decrease Volume\n 3. Mute\n 0. back\n"""
                        print(volume_options)

                        volume_choice = input("Select an option: ")
                        if volume_choice == "1":
                            increase_times = int(input("Enter the number of times to increase the volume: "))
                            for _ in range(increase_times):
                                result = run_adb_command("shell input keyevent KEYCODE_VOLUME_UP")
                                print(result)
                        elif volume_choice == "2":
                            decrease_times = int(input("Enter the number of times to decrease the volume: "))
                            for _ in range(decrease_times):
                                result = run_adb_command("shell input keyevent KEYCODE_VOLUME_DOWN")
                                print(result)
                        elif volume_choice == "3":
                            result = run_adb_command("shell input keyevent KEYCODE_MUTE")
                            print(result)
                        elif volume_choice == "0":
                            os.system("cls")
                            break
                        else:
                            print("Invalid choice.")
                elif settings_choice == "3":
                            batt_options = """\n 1. Set Battery Level\n 2. Reset Battery Level\n"""
                            print(batt_options)
                            batt_choice = input("Select an option: ")
                            if batt_choice == "1":
                                battery_level = input("Enter the battery level: ")
                                result = run_adb_command(f"shell dumpsys battery set level {battery_level}")
                            elif batt_choice == "2":
                                result = run_adb_command("shell dumpsys battery reset")
                elif settings_choice == "4":
                            res_options = """\n 1. Current Resolution\n 2. Set Resolution\n 3. Reset Resolution\n"""
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
                elif settings_choice == "5":
                    choices = """\n 1. Auto Rotate ON\n 2. Auto Rotate OFF\n 3. Set Rotation\n"""
                    print(choices)
                    choice = input("Select an option: ")
                    if choice == "1":
                        result = run_adb_command("shell settings put system accelerometer_rotation 1")
                        print(result)
                    if choice == "2":
                        result = run_adb_command("shell settings put system accelerometer_rotation 0")
                        print(result)
                    if choice == "3":
                     run_adb_command("shell settings put system accelerometer_rotation 0")
                     while True:
                        choices = """\n 1. 0°\n 2. 90°\n 3. 180°\n 4. 270\n back°\n"""  
                        print(choices)
                        choice = input("Select an option: ")
                        if choice == "1":
                            result = run_adb_command("shell settings put system user_rotation 0")
                            print(result)
                        if choice == "2":
                            result = run_adb_command("shell settings put system user_rotation 1")
                            print(result)
                        if choice == "3":
                            result = run_adb_command("shell settings put system user_rotation 2")
                            print(result)
                        if choice == "4":
                            result = run_adb_command("shell settings put system user_rotation 3")
                            print(result)
                        if choice == "0":
                            os.system("cls")
                            break
                elif settings_choice == "0":
                    os.system("cls")
                    break
                else:
                    print("Invalid choice.")
        elif choice == "4":
         while True:
            menu_options = """\n 1. Home Button\n 2. Back Button\n 3. Recent Button\n 4. Play Video\n 5. Open Photo\n 0. back\n"""
            print(menu_options)
            choice = input("Select an option: ")
            if choice == "1":
                result = run_adb_command(f"shell input keyevent KEYCODE_HOME")
            if choice == "2":
                result = run_adb_command(f"shell input keyevent KEYCODE_BACK")
            if choice == "3":
                result = run_adb_command(f"shell input keyevent KEYCODE_APP_SWITCH")
            elif choice == "0":
                os.system("cls")
                break
            else:
                print("Invalid choice.")
        elif choice == "5":
         while True:
            menu_options = """\n 1. Screenshot\n 2. Screen Record\n 3. Live Feed\n 4. Front Camera Picture\n 0. back\n"""
            print(menu_options)
            choice = input("Select an option: ")
            if choice == "1":
                screenshot_path = input("Enter the directory to save the screenshot (leave blank for photos\\): ")
                if not screenshot_path:
                    screenshot_path = "photos\\"
                elif not screenshot_path.endswith("/"):
                    screenshot_path += "/"
                result = run_adb_command("shell screencap -p /sdcard/screenshot.png")
                pull_path = f"{screenshot_path}screenshot.png"
                result = run_adb_command(f"pull /sdcard/screenshot.png {pull_path}")
                if result:
                    print("Screenshot saved successfully.")
                else:
                    print("Failed to save the screenshot.")
            elif choice == "2":
                duration = int(input("Enter the duration of the screen recording in seconds: "))
                recording_path = input("Enter the directory to save the screen recording (leave blank for videos\\): ")
                if not recording_path:
                    recording_path = "videos\\"
                elif not recording_path.endswith("/"):
                    recording_path += "/"       
                result = run_adb_command(f"shell screenrecord --time-limit {duration} /sdcard/screenrecord.mp4")        
                pull_path = f"{recording_path}screenrecord.mp4"
                result = run_adb_command(f"pull /sdcard/screenrecord.mp4 {pull_path}")
                if result:
                    print("Screen recording saved successfully.")
                else:
                    print("Failed to save the screen recording.")
            elif choice == "3":
                print(
                    f"""
                1. Default Mode   (Best quality)
                2. Silent Mode   (No Sound)
                3. Fast Mode      (Low quality but high performance)
                4. Custom Mode    (Tweak settings to increase performance)
                """
                )
                mode = input("> ")
                if mode == "1":
                    os.system("start cmd /k scrcpy")
                elif mode == "2":
                    os.system("start cmd /k scrcpy --no-audio")
                elif mode == "3":
                    os.system("start cmd /k scrcpy -m 1024 -b 1M")
                elif mode == "4":
                    print(f"\nEnter size limit (e.g. 1024)")
                    size = input("> ")
                    if not size == "":
                        size = "-m " + size

                    print(
                        f"\nEnter bit-rate (e.g. 2)   (Default : 8 Mbps)"
                    )
                    bitrate = input("> ")
                    if not bitrate == "":
                        bitrate = "-b " + bitrate + "M"

                    print(f"\nEnter frame-rate (e.g. 15)")
                    framerate = input("> ")
                    if not framerate == "":
                        framerate = "--max-fps=" + framerate

                    os.system(f"start cmd /k scrcpy {size} {bitrate} {framerate}")
                else:
                    print(
                        f"\n Invalid selection\n Going back to Main Menu"
                    )
                    return
                print("\n")
            elif choice == "4":
                front_camera_path = input("Enter the directory to save the front camera picture (leave blank for photos/): ")
                if not front_camera_path:
                    front_camera_path = "photos/"
                elif not front_camera_path.endswith("/"):
                    front_camera_path += "/"
                result = run_adb_command("shell am start -a android.media.action.IMAGE_CAPTURE --ez android.intent.extra.USE_FRONT_CAMERA true")
                time.sleep(1)
                result = run_adb_command("shell screencap -p /sdcard/front_camera_picture.png")
                pull_path = f"{front_camera_path}front_camera_picture.png"
                result = run_adb_command(f"pull /sdcard/front_camera_picture.png {pull_path}")
                result = run_adb_command("shell input keyevent KEYCODE_BACK")
                if result:
                    print("Front camera picture saved successfully.")
                else:
                    print("Failed to save the front camera picture.")
            elif choice == "0":
                os.system("cls")
                break
            else:
                print("Invalid choice.")
        elif choice == "6":
         while True:
            menu_options = """\n 1. Push File\n 2. Pull File\n 3. Remove Folder or File\n 0. back\n"""
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
            elif choice == "3":
                remote = input("Select a Remote Folder or File: ")
                result = run_adb_command(f"shell rm -r {remote}")
                if result:
                    print(result)
            elif choice == "0":
                    os.system("cls")
                    break
            else:
                print("Invalid choice.")
        elif choice == "7":
            menu_options = """\n 1. Open URL\n 2. Open Video\n 3. Open Photo\n 0. back\n"""
            print(menu_options)
            choice = input("Select an option: ")
            if choice == "1":
                url = input("Enter URL: ")
                result = run_adb_command(f"shell am start -a android.intent.action.VIEW -d {url}")
            if choice == "2":
                video = input("Video: ")
                result = run_adb_command(f"shell am start -a android.intent.action.VIEW  -t video/* -d file:///storage/emulated/0/DCIM/" + video)            
            if choice == "3":
                photo = input("Photo: ")
                result = run_adb_command(f"shell am start -a android.intent.action.VIEW  -t image/* -d file:///storage/emulated/0/DCIM/" + photo)                
        elif choice == "8":
         while True:
            app_menu_options = """\n 1. List Installed Apps\n 2. List Running Apps\n 3. Install App\n 4. Extract APK from App\n 5. Uninstall App\n 6. Uninstall All Apps (Dangerous)\n 7. Kill App\n 8. Open App\n 0. back\n"""
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
                result = run_adb_command("shell dumpsys activity recents | grep 'Recent #' | awk '{print $6}'")
                print(result)
            elif app_choice == "3":
                app_path = input("Enter the path to the APK file: ")
                result = run_adb_command(f"install -r {app_path}")
                if result:
                    print("App installed successfully.")
                else:
                    print("Failed to install the app.")
            elif app_choice == "4":         
                package_name = input("Enter the package name of the app: ")
                local = input("Enter where you want the APK to go (default: apks/): ")
                if not local:
                    local = "apks/"
                elif not local.endswith("/"):
                    local += "/"
                result = run_adb_command(f"shell pm path {package_name}")
                if result:
                    apk_path = result.split(":")[1].strip().replace("package", "")
                    result = run_adb_command(f"pull {apk_path} {local}{package_name}.apk")
                    print(f"Successfully extracted APK from {apk_path} to {local}.")
                else:
                    print("Failed to retrieve APK information.")
            elif app_choice == "5":
                package_name = input("Enter the package name of the app: ")
                result = run_adb_command(f"uninstall {package_name}")
                if result:
                    print("App uninstalled successfully.")
                else:
                    print("Failed to uninstall the app.")
            elif app_choice == "6":
                st = run_adb_command("shell pm list packages")
                package_list = st.split('\n')
                packages = []
                for package in package_list:
                    if package.startswith("package:"):
                        packages.append(package.split("package:")[1])

                if packages:
                    confirmation = input("Are you sure you want to uninstall all apps? (Y/n): ")
                    if confirmation.lower() == "y":
                        for package_name in packages:
                            result = run_adb_command(f"uninstall {package_name}")
                            if result:
                                print(f"App {package_name} uninstalled successfully.")
                            else:
                                print(f"Failed to uninstall app {package_name}.")
                    else:
                        print("App uninstallation canceled.")
                else:
                    print("No apps found on the device.")
            elif app_choice == "7":
                package_name = input("Enter the package name of the app: ")
                result = run_adb_command(f"shell am force-stop {package_name}")
            elif app_choice == "8":
                package_name = input("Enter the package name of the app: ")
                result = run_adb_command(f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
                if result:
                    print("App opened successfully.")
                else:
                    print("Failed to open the app.")
            elif app_choice == "0":
                os.system("cls")
                break
            else:
                print("Invalid choice.")
        elif choice == "9":
         while True:
            menu_options = """\n 1. Make Phone Call\n 2. Send SMS\n 3. View All Contacts\n 0. back\n"""
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
            elif choice == "0":
                os.system("cls")
                break
            else:
                print("Invalid choice.")
        elif choice == "10":
            os.system("start cmd /k adb shell")
        elif choice == "99":
            toggle_debug_mode()
            print(f"Debug mode toggled. Debug mode is now {'ON' if debug_mode else 'OFF'}.")
        elif choice == "0":
            os.system("cls")
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main() 
