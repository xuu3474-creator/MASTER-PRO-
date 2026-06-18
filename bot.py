import os
import time
from playwright.sync_api import sync_playwright

# --- আপনার Quotex লগইন তথ্য এখানে দিন ---
QUOTEX_EMAIL = "আপনার_Quotex_ইমেইল"
QUOTEX_PASSWORD = "আপনার_Quotex_পাসওয়ার্ড"
TRADE_AMOUNT = "10"  # প্রতিটি ট্রেডের ডলার অ্যামাউন্ট (অবশ্যই কোটেশন চিহ্নের ভেতরে টেক্সট আকারে লিখবেন)
# ----------------------------------------

def run_quotex_bot():
    print("🚀 কুওটেক্স (Quotex) অটোমেশন বট চালু হচ্ছে...")
    
    with sync_playwright() as p:
        # রেন্ডার সার্ভারে ব্যাকএন্ডে ব্রাউজার রান করার জন্য (Headless Mode)
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = browser.new_page()
        
        # Quotex লগইন পেজে যাওয়া
        print("🌐 কুওটেক্স লগইন পেজে প্রবেশ করা হচ্ছে...")
        page.goto("https://qxbroker.com/en/sign-in")
        time.sleep(5)
        
        # ইমেইল এবং পাসওয়ার্ড ইনপুট দেওয়া
        print("🔑 লগইন ডিটেইলস ইনপুট দেওয়া হচ্ছে...")
        page.fill("input[name='email']", QUOTEX_EMAIL)
        page.fill("input[name='password']", QUOTEX_PASSWORD)
        
        # লগইন বাটনে ক্লিক
        page.click("button[type='submit']")
        time.sleep(8)  # পেজ লোড হওয়ার জন্য অপেক্ষা
        
        print("✅ লগইন প্রসেস সম্পন্ন হয়েছে। ট্রেডিং রুমে প্রবেশ করা হচ্ছে...")
        page.goto("https://qxbroker.com/en/trade")
        time.sleep(10)
        
        try:
            # ট্রেড অ্যামাউন্ট সেট করা
            print(f"💰 ট্রেড অ্যামাউন্ট {TRADE_AMOUNT}$ সেট করা হচ্ছে...")
            amount_input = page.locator(".tab-field__input").first
            amount_input.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.type(TRADE_AMOUNT)
            time.sleep(2)
            
            # একটি টেস্ট 'UP' (CALL) ট্রেড নেওয়া
            print("📈 একটি 'UP' (Green Button) ট্রেড প্লেস করা হচ্ছে...")
            # কুওটেক্সের সবুজ (Up) বাটনের ক্লাস বা টেক্সট ডিটেক্ট করে ক্লিক করা
            page.click(".button-call") 
            print("🎯 ট্রেড সফলভাবে নেওয়া হয়েছে!")
            time.sleep(5)
            
        except Exception as e:
            print(f"⚠️ ট্রেড প্লেস করার সময় ত্রুটি ঘটেছে: {e}")
            
        browser.close()
        print("🔌 বট বন্ধ করা হয়েছে।")

if __name__ == "__main__":
    run_quotex_bot()
