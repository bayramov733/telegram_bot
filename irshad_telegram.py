from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio
import time

# Evləri çəkmək üçün Selenium + BeautifulSoup
def telefonlari_getir():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://irshad.az/mehsullar?q=iphone")

    time.sleep(5)  # JS yüklənsin deyə gözləyirik

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    phone = []

    elanlar = soup.find_all("div", class_="product__flex__left-right")[:5]
    qiymetler = soup.find_all("div", class_="product__flex-right")[:5]

    for basliq_div, qiymet_div in zip(elanlar, qiymetler):
        try:
            basliq = basliq_div.get_text(strip=True)
            qiymet = qiymet_div.get_text(strip=True)
            phone.append(f"{basliq} — {qiymet}")
        except:
            continue

    return phone if phone else ["Heç bir elan tapılmadı."]

# Telegram komandası
async def phone(update, context):
    if update.effective_user.id != 1502078472:
        await update.message.reply_text("Bu botdan istifadə etməyə icazən yoxdur.")
        return

    await update.message.reply_text("telefonlar yüklənir, zəhmət olmasa gözləyin...")
    loop = asyncio.get_event_loop()
    telefon_list = await loop.run_in_executor(None, telefonlari_getir)

    for telefon in telefon_list:
        await update.message.reply_text(telefon)

# Botu işə sal
if __name__ == '__main__':
    TOKEN = "7805677448:AAFvjnopHMKaabZ9oR8OpE0ZgU-_V8CwI1A"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("phone", phone))
    print("Bot işə düşdü...")
    app.run_polling()