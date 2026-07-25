import time
import json
import websocket  # تأكد من استيراد مكتبة الـ websocket إذا لم تكن موجودة

# --- 1. إعداد الاتصال (تأكد من وضع الرابط الصحيح للـ WebSocket هنا) ---
WS_URL = "wss://your-ais-websocket-url"  # استبدل هذا برابط الخدمة لديك

print("🔌 Connecting to AIS WebSocket...")
try:
    ws = websocket.create_connection(WS_URL)
    print("✅ Connected successfully!")
except Exception as e:
    print(f"❌ Connection Error: {e}")
    exit(1)

# --- 2. استقبال وطباعة الرسائل ---
print("⏳ Waiting for AIS messages...")

received = 0
start_time = time.time()

try:
    while time.time() - start_time < 30:
        try:
            # محاولة استقبال الرسالة من الـ WebSocket
            message = ws.recv()
            data = json.loads(message)

            print("=" * 60)
            print("📥 AIS MESSAGE")
            print(json.dumps(data, indent=2))

            received += 1

            # الخروج فور استقبال 5 رسائل ناجحة
            if received >= 5:
                break

        except Exception as e:
            print("Receive Error:", e)
            break

    if received == 0:
        print("⚠️ No AIS messages received within 30 seconds.")

finally:
    # --- 3. إغلاق الاتصال بشكل صحيح وضامن ---
    try:
        ws.close()
        print("🔌 WebSocket connection closed.")
    except Exception as close_error:
        print("Error closing WebSocket:", close_error)
