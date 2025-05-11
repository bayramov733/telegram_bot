from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio
import time

# Evləri çəkmək üçün Selenium + BeautifulSoup
def evleri_getir():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://bina.az/")

    time.sleep(5)  # JS yüklənsin deyə gözləyirik

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    evler = []

    elanlar = soup.find_all("div", class_="title_block")[:5]
    qiymetler = soup.find_all("div", class_="price")[:5]

    for basliq_div, qiymet_div in zip(elanlar, qiymetler):
        try:
            basliq = basliq_div.get_text(strip=True)
            qiymet = qiymet_div.get_text(strip=True)
            evler.append(f"{basliq} — {qiymet}")
        except:
            continue

    return evler if evler else ["Heç bir elan tapılmadı."]

# Telegram komandası
async def evler(update, context):
    if update.effective_user.id != 1502078472:
        await update.message.reply_text("Bu botdan istifadə etməyə icazən yoxdur.")
        return

    await update.message.reply_text("Evlər yüklənir, zəhmət olmasa gözləyin...")
    loop = asyncio.get_event_loop()
    ev_list = await loop.run_in_executor(None, evleri_getir)

    for ev in ev_list:
        await update.message.reply_text(ev)

# Botu işə sal
if __name__ == '__main__':
    TOKEN = "7805677448:AAFvjnopHMKaabZ9oR8OpE0ZgU-_V8CwI1A"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("evler", evler))
    print("Bot işə düşdü...")
    app.run_polling()
