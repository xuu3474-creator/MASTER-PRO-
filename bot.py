import os
import json
import ssl
import time
import websocket

# --- রেন্ডার ড্যাশবোর্ড থেকে অটোমেটিক টোকেন রিড করার লজিক ---
API_TOKEN = os.getenv("DERIV_TOKEN", "").strip()
TRADE_AMOUNT = 10  
DURATION = 1  
DURATION_UNIT = "m"  
SYMBOL = "R_100"  
# --------------------------------------------------------

def on_open(ws):
    print("🚀 সার্ভারের সাথে কানেক্ট হয়েছে। অথেনটিকেশন করা হচ্ছে...")
    if not API_TOKEN:
        print("❌ ভুল: রেন্ডার ড্যাশবোর্ডে DERIV_TOKEN সেট করা হয়নি!")
        ws.close()
        return
    auth_request = {"authorize": API_TOKEN}
    ws.send(json.dumps(auth_request))

def on_message(ws, message):
    data = json.loads(message)

    if data.get("msg_type") == "authorize":
        if "error" in data:
            print(f"❌ অথেনটিকেশন ব্যর্থ! কারণ: {data['error']['message']}")
            ws.close()
        else:
            print(f"✅ লগইন সফল! ব্যবহারকারী: {data['authorize']['email']}")
            print("🤖 অটো ট্রেডিং শুরু হচ্ছে...")
            execute_trade(ws, contract_type="CALL")

    elif data.get("msg_type") == "buy":
        if "error" in data:
            print(f"❌ ট্রেড প্লেস করতে ব্যর্থ! কারণ: {data['error']['message']}")
        else:
            print(f"💰 ট্রেড সফলভাবে নেওয়া হয়েছে!")
            print(f"🎯 কন্ট্রাক্ট আইডি (ID): {data['buy']['contract_id']}")
            print(f"📈 ব্যালেন্স এখন: {data['buy']['balance_after']}")
            ws.close()

def on_error(ws, error):
    print(f"⚠️ ত্রুটি (Error) দেখা দিয়েছে: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 বট বন্ধ করা হয়েছে।")

def execute_trade(ws, contract_type="CALL"):
    print(f"⏳ {SYMBOL} মার্কেটে {TRADE_AMOUNT}$ এর একটি {contract_type} ট্রেড পাঠানো হচ্ছে...")
    trade_request = {
        "buy": 1,
        "price": TRADE_AMOUNT,
        "parameters": {
            "amount": TRADE_AMOUNT,
            "basis": "stake",
            "contract_type": contract_type,
            "currency": "USD",
            "duration": DURATION,
            "duration_unit": DURATION_UNIT,
            "symbol": SYMBOL
        }
    }
    ws.send(json.dumps(trade_request))

if __name__ == "__main__":
    # আমরা ডেরিভের অফিশিয়াল ওয়েব ট্রেডার অ্যাপ আইডি ব্যবহার করছি
    socket_url = "wss://ws.binaryws.com/websockets/v3?app_id=11780"
    
    ws = websocket.WebSocketApp(
        socket_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
