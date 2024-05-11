import time
# import pyautogui
import pyaudio
import pvporcupine
import struct
import os

# porcupine := Porcupine{
#   AccessKey: "6R+qJMqUy7Pfv8aw5oPkMMroE4WTExVGQRnkUGWpL1ByXQ5BCgxpXw=="
#     KeywordPaths:[]string{"C:\Users\Girish\OneDrive\Desktop\Alita-AI\Alita AI\www\\assets\\alita keyword\\alita_en_windows_v3_0_0.ppn"}
# }
#
# err:= porcupine.Init()

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:

        # pre trained keywords
        porcupine = pvporcupine.create(access_key='6R+qJMqUy7Pfv8aw5oPkMMroE4WTExVGQRnkUGWpL1ByXQ5BCgxpXw==',keyword_paths=['C:\\Users\Girish\OneDrive\Desktop\Alita-AI\Alita AI\www\\assets\\alita keyword\\alita_en_windows_v3_0_0.ppn'])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                                 frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # processing keyword comes from mic
            keyword_index = porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index >= 0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

hotword()