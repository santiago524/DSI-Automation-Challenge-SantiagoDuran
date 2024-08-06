from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pyautogui
import pytesseract
from typing import Dict

app = FastAPI()
security = HTTPBasic()

# Aquí puedes definir tus credenciales
users_db = {
    "sanalex": "santiago"
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    stored_password = users_db.get(credentials.username)
    if stored_password != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def read_root():
    return {"message": "Welcome to the bot activation API"}

@app.post("/activate_bot", dependencies=[Depends(authenticate)])
def activate_bot(actions: Dict[str, str]):
    # Aquí puedes definir las acciones del bot usando pyautogui y pytesseract
    for action, value in actions.items():
        if action == "click":
            x, y = map(int, value.split(","))
            pyautogui.click(x, y)
        elif action == "write":
            pyautogui.write(value)
        elif action == "screenshot_and_read":
            screenshot = pyautogui.screenshot()
            text = pytesseract.image_to_string(screenshot)
            # Aquí puedes tomar decisiones basadas en el texto extraído
            print(f"Texto extraído: {text}")
            # Por ejemplo, puedes tomar diferentes decisiones basadas en el texto:
            if "example text" in text:
                # Realizar alguna acción específica
                pass
    return {"status": "Bot actions completed"}
