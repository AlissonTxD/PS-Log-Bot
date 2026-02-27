import discord
from discord.ext import tasks
import pygetwindow as gw
import os
from PIL import Image, ImageEnhance
import mss
import mss.tools
import cv2
import pytesseract
import re
import logging

# Configurações globais de imagem
IMG_FACTORS = (2.0, 0.5, 1.0, 2.5)
LOG_SUBIMAGE_PATH = "temp/subimage.png"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class tesseractfail(Exception):
    pass

DELEY_BETWEEN_MESSAGES_SECONDS = 15

class LogBotModel:
    def __init__(self, config: dict):
        self.event_counter = 0
        self.reset_counter = 0
        self.client = None
        self.printer = None
        self.events = []
        self.token = None
        self.CHANNEL_ID = None
        self.cut_coords = None
        self.testmode = None
        self.__load_config(config)

    # ----------------------- Início do Bot -----------------------
    def run(self):
        self._focus_in_window("ArkAscended")

        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            logging.info(f"Login as {self.client.user}")
            channel = self.client.get_channel(self.CHANNEL_ID)
            try:
                await channel.send("Log Bot Started!")
            except Exception as e:
                logging.error(f"Bot sem acesso ao canal: {e}")
                return

            if not self.printer.is_running():
                self.printer.start()

        @tasks.loop(seconds=DELEY_BETWEEN_MESSAGES_SECONDS)
        async def printer():
            loops_for_minute = 60 // DELEY_BETWEEN_MESSAGES_SECONDS
            channel = self.client.get_channel(self.CHANNEL_ID)

            self.__generate_image_from_coords(self.cut_coords)
            text = self.__read_img_ocr()

            if text is None or not text.strip():
                text = "No text detected"
            
            logging.info(f"Texto OCR: {text}")
            is_new_event = self.__validate_log(text)

            logging.info(f"Test mode: {self.testmode}")
            if self.testmode:
                is_new_event = True
                text = f"Test Event: {text}"

            if is_new_event:
                message = text
                if self.event_counter > 5:
                    message = f"@everyone {text}"
                    self.event_counter = 0
                elif self.event_counter >= 3:
                    message = f"@here {text}"

                try:
                    await channel.send(f"{message}", file=discord.File(LOG_SUBIMAGE_PATH))
                except Exception as e:
                    logging.error(f"Erro enviando mensagem: {e}")

                self.event_counter += 1
                self.reset_counter = loops_for_minute * 10

            if self.reset_counter >= (loops_for_minute * 20):
                self.event_counter = 0
                self.reset_counter = 0

            self.reset_counter += 1

        self.printer = printer
        self.client.run(self.token)

    # ----------------------- OCR -----------------------
    def __read_img_ocr(self):
        try:
            img = cv2.imread(LOG_SUBIMAGE_PATH)
            text = pytesseract.image_to_string(img, config="--psm 6")
            text = text.replace("\n", " ").replace("\r", "")
            text = re.sub(r"\s+", " ", text)
            return text
        except Exception as e:
            logging.error(f"Erro no OCR: {e}")
            raise tesseractfail(f"OCR failed: {e}")
            return ""

    # ----------------------- Config -----------------------
    def __load_config(self, config: dict):
        try:
            self.token = config.get("token")
            self.CHANNEL_ID = config.get("channel_id")
            self.cut_coords = config.get("cut_coords")
            self.testmode = config.get("testmode")
            if not self.cut_coords or len(self.cut_coords) != 4:
                raise ValueError("cut_coords inválido. Use (left, top, right, bottom).")
        except Exception as e:
            logging.error(f"Erro carregando config: {e}")

    # ----------------------- Captura e Processamento de Imagem -----------------------
    def __generate_image_from_coords(self, cut_coords):
        try:
            os.makedirs("temp", exist_ok=True)

            with mss.mss() as sct:
                monitor_full = sct.monitors[1]  # monitor principal
                left = monitor_full["left"] + cut_coords[0]
                top = monitor_full["top"] + cut_coords[1]
                width = cut_coords[2] - cut_coords[0]
                height = cut_coords[3] - cut_coords[1]

                if width <= 0 or height <= 0:
                    raise ValueError("Coordenadas inválidas ou fora do monitor")

                monitor = {"left": left, "top": top, "width": width, "height": height}
                screenshot = sct.grab(monitor)

                mss.tools.to_png(
                    screenshot.rgb,
                    screenshot.size,
                    output=LOG_SUBIMAGE_PATH
                )

            # Ajustes de imagem para OCR
            img = Image.open(LOG_SUBIMAGE_PATH).convert("RGB")
            img = ImageEnhance.Contrast(img).enhance(IMG_FACTORS[0])
            img = ImageEnhance.Color(img).enhance(IMG_FACTORS[1])
            img = ImageEnhance.Brightness(img).enhance(IMG_FACTORS[2])
            img = ImageEnhance.Sharpness(img).enhance(IMG_FACTORS[3])
            img.save(LOG_SUBIMAGE_PATH)
            img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
            img.save(LOG_SUBIMAGE_PATH)

            logging.info(f"Imagem gerada em {LOG_SUBIMAGE_PATH}")

        except Exception as e:
            logging.error(f"Erro ao gerar imagem: {e}")

    # ----------------------- Foco na Janela -----------------------
    def _focus_in_window(self, window_name: str = "ArkAscended") -> None:
        try:
            windows = gw.getWindowsWithTitle(window_name)
            if not windows:
                logging.warning(f"Janela '{window_name}' não encontrada.")
                return

            window = windows[0]
            if gw.getActiveWindow() != window:
                window.activate()
            else:
                logging.info(f"Janela '{window_name}' já está ativa.")
        except Exception as e:
            logging.error(f"Erro ao focar a janela '{window_name}': {e}")

    # ----------------------- Validação de Logs -----------------------
    def __validate_log(self, text):
        try:
            match = re.match(r"Day (\d+), (\d{2}:\d{2}:\d{2}): (.+)", text)
            if match:
                day = match.group(1)
                hour = match.group(2)
                message = match.group(3)

                ignore_words = ["Baby", "decay", "Karkinos"]

                if ("Your" in message and ("destroyed" in message or "killed" in message)
                        and not any(word in message for word in ignore_words)):
                    event_id = f"{day} {hour}"
                    if event_id not in self.events:
                        self.events.append(event_id)
                        logging.info(f"New Event: {text}")
                        return True
                    else:
                        logging.warning(f"Event already registered: {text}")
                        return False
                else:
                    logging.info(f"Event ignored: {text}")
                    return False
            else:
                logging.warning(f"Invalid log format: {text}")
                return False
        except Exception as e:
            logging.error(f"Erro validando log: {e}")
            return False

    def stop(self):
        try:
            print("Encerrando bot...")
            if self.printer and self.printer.is_running():
                self.printer.cancel()

            if self.client:
                import asyncio
                asyncio.run_coroutine_threadsafe(
                    self.client.close(),
                    self.client.loop
                )
        except Exception as e:
            print("Erro ao parar bot:", e)

# ----------------------- Uso -----------------------
if __name__ == "__main__":
    pass