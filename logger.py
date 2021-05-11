from datetime import datetime

class log():

    def __init__(self):
        pass

    def startup(self):
        with open("resources/log.txt", "a") as log:
            log.write("\n--------------------iSeek Log--------------------\n")
            log.write("Application started at " + str(datetime.now()) + "\n")
    
    def endpointReached(self, name, ip):
        with open("resources/log.txt", "a") as log:
            log.write(name + " endpoint reached at " + str(datetime.now()) + "\n")
            log.write("User IP: " + ip + "\n")

    def success(self):
        with open("resources/log.txt", "a") as log:
            log.write("Successfully performed method\n")
    
    def fail(self, message):
        with open("resources/log.txt", "a") as log:
            log.write("Failed to perform method\n")
            log.write("Error Code:\n")
            log.write(message + "\n")
    
    def write(self, message):
        with open("resources/log.txt", "a") as log:
            log.write(message + "\n")