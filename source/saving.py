import cv2
import time
from datetime import datetime
import os
import simplejson
from azure.storage.blob import BlobServiceClient, __version__
from azure.core.exceptions import ResourceExistsError

imageFolderPath = '/home/pi/Desktop/TK25/PiFinal/image/'
jsonFolderPath = '/home/pi/Desktop/TK25/PiFinal/json/'
jsonFilePath = ''
imageFilePath = ''
now = datetime.now()
# -------------------- Configure Parameters -------------------- #

AccountName = "gndevstorage"
AccountKey = "rfsKLF1aCLmPcFsFYsHmWjK1fsOyL5gnkGZ9YRB36ElCtL8wDah02VRUY31FDeCcLzwPWKA3xseIprWHW7GjgA=="
connectionString = "DefaultEndpointsProtocol=http;" + "AccountName=" + AccountName + ";" + "AccountKey=" + AccountKey + ";"
localPath = "./data"

containerNameCAM = "cam-detection"
containerNameDATA = "data-storage"
containerNameUSER = "user-data"

# -------------------- Connect to Azure Storage Service -------------------- #

blobServiceClient = BlobServiceClient.from_connection_string(connectionString)
containerClientCAM = blobServiceClient.get_container_client(containerNameCAM)
containerClientDATA = blobServiceClient.get_container_client(containerNameDATA)
containerClientUSER = blobServiceClient.get_container_client(containerNameUSER)

def create_containers():
    try:
        containerClientCAM.create_container()
    except ResourceExistsError:
        pass
    try:
        containerClientDATA.create_container()
    except ResourceExistsError:
        pass
    try:
        containerClientUSER.create_container()
    except ResourceExistsError:
        pass
    print("Server OK!")

def upload_package(uploadContainer, uploadFolderPath, uploadJsonFile):
    global now
    uploadContainer += "/" + now.strftime("%d%m%Y")
    blob_client = blobServiceClient.get_blob_client(container=uploadContainer, blob=uploadJsonFile)

    upload_file_path = os.path.join(uploadFolderPath, uploadJsonFile)
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)

def handle_image(text, img):
    global now
    now = datetime.now()
    os.chdir(imageFolderPath)
    imagePath = text + now.strftime("_%H%M%S") + ".jpg"
    cv2.imwrite(imagePath, img)
    imageFilePath = os.path.join(imageFolderPath, imagePath)
    upload_package(containerNameDATA, imageFolderPath, imagePath)    
    
def handle_json(text):
    global now
    dataTime = now.strftime("%d/%m/%Y, %H:%M:%S")
    dataType = "CAM"
    dataDeviceID = "0001"
    lengthText = len(text)
    while (lengthText < 9):
        text += "X"
        lengthText += 1
        
    dataPlate = text

    package = {
            'time': dataTime,
            'type': dataType,
            'deviceID': dataDeviceID,
            'data': dataPlate
        }
    
    dataJson = simplejson.dumps(package)
    localFileName = dataPlate + now.strftime("_%H%M%S") + ".json"
    jsonFilePath = os.path.join(jsonFolderPath, localFileName)

    file = open(jsonFilePath, 'w')
    file.write(dataJson)
    file.close()
    
    upload_package(containerNameCAM, jsonFolderPath, localFileName)
    