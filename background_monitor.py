import time
import json
import os
import ctypes
from datetime import datetime
from plyer import notification

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'screen_config.json')

def get_uptime_ms():
    """Returns system uptime in milliseconds (Windows specific)."""
    try:
        return ctypes.windll.kernel32.GetTickCount64()
    except:
        return 0

def get_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")

def send_alert(pct, message):
    try:
        notification.notify(
            title=f"MindBalance Guard | {pct}% Limit Reached",
            message=message,
            app_icon=None,
            timeout=10,
        )
    except Exception as e:
        print(f"Notification error: {e}")

def monitor():
    print("MindBalance Background Guard Started...")
    
    while True:
        config = get_config()
        if not config or config.get("status") != "active":
            time.sleep(30)
            continue
            
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_ts = datetime.now().timestamp()
        current_uptime = get_uptime_ms()
        
        # 1. Reboot Detection Reset
        last_uptime = config.get("last_uptime_ms", 0)
        # If current uptime is less than last recorded, system was switched off/on
        if current_uptime < last_uptime:
            print("Reboot detected! Resetting session timer.")
            config["elapsed_secs"] = 0.0
            config["alert_sent"] = {}
        
        config["last_uptime_ms"] = current_uptime

        # 2. New Day Reset
        if config.get("date") != current_date:
            old_date = config.get("date")
            history = config.get("history", {})
            if old_date and config.get("elapsed_secs", 0) > 0:
                history[old_date] = config.get("elapsed_secs", 0.0)
            
            config.update({
                "date": current_date,
                "elapsed_secs": 0.0,
                "last_update": current_ts,
                "alert_sent": {},
                "history": history
            })
            save_config(config)
            
        # Update Elapsed Time
        last_update = config.get("last_update", current_ts)
        delta = current_ts - last_update
        
        # Only add time if the gap is reasonable (within 5 mins)
        if 0 < delta < 300: 
            config["elapsed_secs"] = config.get("elapsed_secs", 0.0) + delta
        
        config["last_update"] = current_ts
        
        # Goal Checks
        limit_h = config.get("limit_hours", 4.0)
        limit_s = limit_h * 3600
        elapsed_s = config.get("elapsed_secs", 0.0)
        
        progress = elapsed_s / limit_s if limit_s > 0 else 1.0
        alert_sent = config.get("alert_sent", {})
        
        thresholds = [
            (1.00, "100%", "⚠️ Daily Limit Reached! Time to disconnect and rest."),
            (0.90, "90%", "🏃 Almost there. You have reached 90% of your daily limit."),
            (0.75, "75%", "🕒 Attention: 75% of your screen limit has been consumed."),
            (0.50, "50%", "📅 Halfway mark: You have used 50% of your daily allowance.")
        ]
        
        for frac, label, msg in thresholds:
            if progress >= frac and label not in alert_sent:
                send_alert(label, msg)
                alert_sent[label] = True
                config["alert_sent"] = alert_sent
        
        save_config(config)
        time.sleep(60) # Check every minute

if __name__ == "__main__":
    monitor()