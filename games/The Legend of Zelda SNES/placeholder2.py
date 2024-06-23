def time_left(filesize,speed):
    minutes = round(((int(filesize)*1000)/int(speed))/60,2)
    print(f"Your download will take {minutes} minutes")
    choice = input("Would you like to go again? Enter '1' for yes, anything else for no: ")
    if choice == '1':
        start()
    else:
        stop()

def start():
    filesize = input("How big is the file in GB?: ")
    speed = input("How fast are you downloading in MB/s?: ")
    time_left(filesize,speed)

def stop():
    quit()

start()