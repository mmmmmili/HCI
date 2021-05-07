import os
import sys
import threading
import webbrowser
import time

import speech_recognition as sr
from PyQt5 import QtWidgets

# from SiriInterface import Ui_MainWindow
from Interface import Ui_MainWindow

class myWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.flag=False

    # 五个功能函数
    def openWeatherWeb(self):
        webbrowser.open("http://sh.weather.com.cn/")
        self.ui.openWeatherWeb()

    def openCalculator(self):
        os.system("calc.exe")
        self.ui.openCalculator()

    def openNotebook(self):
        os.system("notebook.txt")
        self.ui.openNotebookUi()

    def playMusic(self):
        os.system("resource\\file\\music.wav")
        self.ui.playMusicUi()

    def openWeChat(self):
        os.startfile("C:\Program Files (x86)\Tencent\WeChat\WeChat.exe")
        self.ui.openWeChat()

    def noCatch(self):
        # application.ui.notCatchUi()
        time.sleep(3)
        self.ui.notCatchUi()

    # 语音识别函数
    def recognize_speech_from_mic(self):
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # 根据环境噪音调整识别器的灵敏度并记录音频
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # 试着识别录音中的声音
        # 如果RequestError或UnknownValueError异常被捕获，
        # 相应地更新响应对象
        try:
            response["transcription"] = recognizer.recognize_sphinx(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive# API不可达或无响应
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response

    def waitForInput(self):
        while True:
            print("recognizing")
            self.ui.listeningUi()

            guess = self.recognize_speech_from_mic()
            if guess["transcription"]:
                command=guess["transcription"]
                print(command)
                if "music" in command:
                    self.playMusic()
                elif "note" in command\
                        or "no" in command\
                        or "net" in command:
                    self.openNotebook()
                elif "calculator" in command\
                        or "counted" in command\
                        or "eggs" in command:
                    self.openCalculator()
                elif "weather" in command \
                        or "whether" in command\
                        or "when that" in command:
                    self.openWeatherWeb()
                elif "chat" in command\
                        or "check" in command:
                    self.openWeChat()
                else:
                    self.noCatch()
            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                self.noCatch()

    #点击时开始识别
    def mousePressEvent(self, event):
        if(self.flag==True):
            return

        self.flag = True
        global timer
        timer = threading.Thread(target=self.waitForInput)
        timer.start()


app = QtWidgets.QApplication([])
application = myWindow()
recognizer = sr.Recognizer()
microphone = sr.Microphone()
application.show()
sys.exit(app.exec())


