import urllib

def digitalRead(port, url='http://127.0.0.1/arduino'):
    return urllib.urlopen(url + "/digital/" + str(port)).read()

def digitalWrite(port, state, url='http://127.0.0.1/arduino'):
    return urllib.urlopen(url + "/digital/" + str(port) + "/" + str(state)).read()

def analogRead(port, url='http://127.0.0.1/arduino'):
    return urllib.urlopen(url + "/analog/" + str(port)).read()

def analogWrite(port, value, url='http://127.0.0.1/arduino'):
    return urllib.urlopen(url + "/analog/" + str(port) + "/" + str(value)).read()

def pinMode(port, mode, url='http://127.0.0.1/arduino'):
    return urllib.urlopen(url + "/mode/" + str(port) + "/" + str(mode)).read()
