import os
import re
import subprocess
from AI.SpeakAndListen import speak, get_audio, Input

result = []

def createNewConnection(name, SSID, key):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+SSID+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+key+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
    with open(name+".xml", 'w') as file:
        file.write(config)
    os.system(command)
    os.remove(name+".xml")
    speak("connecting")
def connect(name, SSID):
    try:
        command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
        subprocess.check_output(command, shell = True)
        return True
    except subprocess.CalledProcessError:
        return False

def displayAvailableNetworks():
    dic = ["\\r\\n","6 : ","    N"]
    command = "netsh wlan show networks interface=Wi-Fi"
    output = subprocess.check_output(command,shell=True)
    output = str(output).split("SSID")
    del output[0]
    for group in output:
        group = re.search(r"\d :.*\\r\\n\s*N",group)
        group = str(group.group(0))
        for replace in dic:
            group = group.replace(replace, "")
        for i in range(100):
            group = group.replace(str(i) + " : ", "")
        result.append(group)

def main(name):
    displayAvailableNetworks()
    if name == "":
        speak("Name of the connection")
        name = get_audio()
    for res in result:
        if name.lower() in res.lower():
            if connect(res, res):
                speak("connecting")
                return
            else:
                speak("Password")
                paswd = Input("Password")
                createNewConnection(res, res, paswd)
                speak("trying to connect")
                return
    speak("there is no wifi of your given information")
