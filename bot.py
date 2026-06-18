import os
import time
from qxbroker_api.stable_api import Quotex

# --- আপনার Quotex অ্যাকাউন্টের তথ্য ---
EMAIL = "আপনার_Quotex_ইমেইল"
PASSWORD = "আপনার_Quotex_পাসওয়ার্ড"
# -----------------------------------

# Quotex সার্ভারের সাথে কানেক্ট করা
client = Quotex(email=EMAIL, password=PASSWORD)
status, message = client.connect()

if status:
    print("✅ Quotex অ্যাকাউন্টে সফলভাবে লগইন হয়েছে!")
    
    # ডেমো নাকি রিয়েল অ্যাকাউন্ট সিলেক্ট করবেন (নিচের যেকোনো একটি অন রাখুন)
    client.change_balance("PRACTICE")  # ডемо অ্যাকাউন্টের জন্য
    # client.change_balance("REAL")      # রিয়েল অ্যাকাউন্টের জন্য
    
    print(f"💰 বর্তমান ব্যালেন্স: {client.get_balance()}$")

    # একটি টেস্ট ট্রেড নেওয়া (Asset, Amount, Direction, Duration)
    asset = "EURUSD"
    amount = 10
    direction = "call"  # "call" মানে আপ, "put" মানে ডাউন
    duration = 60       # ৬০ সেকেন্ড বা ১ মিনিট
    
    print(f"⏳ {asset} মার্কেটে {amount}$ এর একটি {direction.upper()} ট্রেড নেওয়া হচ্ছে...")
    status, buy_info = client.buy(asset, amount, direction, duration)
    
    if status:
        print("💰 ট্রেড সফলভাবে প্লেস হয়েছে!")
    else:
        print("❌ ট্রেড প্লেস করা যায়নি।")

else:
    print(f"❌ লগইন ব্যর্থ হয়েছে! কারণ: {message}")
