import time
import json
import os
import sys
import signal
import logging
import subprocess
import platform
import shutil
from datetime import datetime, date
from pathlib import Path

# ── Dynamic Notification Support ───────────────────────────────────────────
try:
    from plyer import notification
    HAS_PLYER = True
except (ImportError, Exception):
    HAS_PLYER = False

# ── Paths & Constants ──────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent.absolute()
CONFIG_FILE   = BASE_DIR / "screen_config.json"
LOG_FILE      = BASE_DIR / "mindbalance.log"
PID_FILE      = BASE_DIR / "guard.pid"

POLL_INTERVAL = 15          # Check more frequently for better accuracy
IDLE_THRESHOLD = 300        # 5 mins idle gap
ALERT_COOLDOWN = 900        # 15 mins for repeat alerts

# ── Logging Configuration ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("MindBalance")

# ── Cross-Platform Uptime ──────────────────────────────────────────────────
def get_system_uptime_ms() -> float:
    os_name = platform.system()
    try:
        if os_name == "Windows":
            import ctypes
            return float(ctypes.windll.kernel32.GetTickCount64())
        elif os_name == "Linux":
            with open("/proc/uptime", "r") as f:
                return float(f.readline().split()[0]) * 1000.0
        elif os_name == "Darwin":
            output = subprocess.check_output(["sysctl", "-n", "kern.boottime"]).decode()
            import re
            match = re.search(r'sec = (\d+)', output)
            if match:
                boot_time = int(match.group(1))
                return (time.time() - boot_time) * 1000.0
    except Exception as e:
        log.debug(f"Uptime error: {e}")
    return 0.0

# ── Graceful Shutdown ──────────────────────────────────────────────────────
_running = True
def _handle_signal(sig, frame):
    global _running
    log.info(f"Signal {sig} received. Cleaning up...")
    _running = False

signal.signal(signal.SIGINT,  _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)

# ── Config Persistence (with atomic write & locking attempt) ──────────────
def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open("r") as f:
                return json.load(f)
        except Exception as e:
            log.warning(f"Config read failed: {e}")
    return {}

def save_config(cfg: dict):
    # Use a temporary file for atomic write (prevents corruption if power cut resets)
    tmp_path = CONFIG_FILE.with_suffix(".tmp")
    try:
        with tmp_path.open("w") as f:
            json.dump(cfg, f, indent=2)
        # On some systems, os.replace is needed for atomic update
        os.replace(str(tmp_path), str(CONFIG_FILE))
    except Exception as e:
        log.error(f"Save failed: {e}")

# ── Notification Provider (Cross-Platform) ─────────────────────────────────
def send_alert(title: str, message: str):
    log.info(f"NOTIFICATION >> {title}: {message}")
    if HAS_PLYER:
        try:
            notification.notify(title=title, message=message, app_name="MindBalance", timeout=12)
            return
        except: pass
    
    # Fallbacks
    try:
        sys_name = platform.system()
        if sys_name == "Linux":
            subprocess.run(["notify-send", "-i", "dialog-warning", title, message], check=False)
        elif sys_name == "Darwin":
            subprocess.run(["osascript", "-e", f'display notification "{message}" with title "{title}"'], check=False)
    except:
        print(f"\a[{title}] {message}\n")

# ── Tracking Logic ──────────────────────────────────────────────────────────
def monitor():
    # 1. PID Check
    if PID_FILE.exists():
        try:
            old_pid = int(PID_FILE.read_text().strip())
            if old_pid != os.getpid():
                # Check if process is still alive
                if platform.system() != "Windows":
                    os.kill(old_pid, 0)
                else:
                    import ctypes
                    h = ctypes.windll.kernel32.OpenProcess(1, False, old_pid)
                    if h: ctypes.windll.kernel32.CloseHandle(h)
                    else: raise ProcessLookupError
                
                log.error(f"Ghost instance detected (PID {old_pid}). Aborting.")
                return
        except (ProcessLookupError, ValueError, OSError):
            PID_FILE.unlink(missing_ok=True)

    PID_FILE.write_text(str(os.getpid()))
    log.info(f"Monitor Started (PID: {os.getpid()})")

    try:
        while _running:
            now_ts = time.time()
            today = date.today().isoformat()
            uptime_ms = get_system_uptime_ms()

            # Load config at the start of loop to catch UI changes
            cfg = load_config()
            if not cfg: 
                time.sleep(5)
                continue

            # Check Status
            if cfg.get("status") != "active":
                cfg["last_heartbeat"] = now_ts
                save_config(cfg)
                time.sleep(10)
                continue

            # Day Change Reset
            if cfg.get("date") != today:
                log.info(f"Resetting for new day: {today}")
                if cfg.get("date"):
                    cfg.setdefault("history", {})[cfg["date"]] = cfg.get("elapsed_secs", 0.0)
                cfg.update({"date": today, "elapsed_secs": 0.0, "alert_sent": {}})

            # Time Progress
            last_update = cfg.get("last_update", now_ts)
            delta = now_ts - last_update

            if 0 < delta < IDLE_THRESHOLD:
                cfg["elapsed_secs"] = cfg.get("elapsed_secs", 0.0) + delta
            elif delta >= IDLE_THRESHOLD:
                log.info(f"Wakeup detected (Gap: {int(delta)}s). Skipping idle time.")

            cfg["last_update"] = now_ts
            cfg["last_uptime_ms"] = uptime_ms
            cfg["last_heartbeat"] = now_ts # Signal to UI that we are alive

            # Alert Logic
            limit_s = cfg.get("limit_hours", 4.0) * 3600
            elapsed = cfg.get("elapsed_secs", 0.0)
            ratio = elapsed / limit_s if limit_s > 0 else 0
            
            alerts = cfg.setdefault("alert_sent", {})
            levels = [(1.0, "100%", "Limit Reached! Stay healthy, take a break."),
                      (0.9, "90%", "Almost there! 90% reached."),
                      (0.75, "75%", "75% of limit used."),
                      (0.5, "50%", "Halfway mark reached.")]
            
            for thr, label, msg in levels:
                if ratio >= thr:
                    last_sent = alerts.get(label, 0)
                    cooldown = ALERT_COOLDOWN if label == "100%" else 86400
                    if now_ts - last_sent > cooldown:
                        send_alert(f"MindBalance: {label}", msg)
                        alerts[label] = now_ts
                        cfg["total_alerts_count"] = cfg.get("total_alerts_count", 0) + 1

            save_config(cfg)
            
            # Precise sleep with exit check
            for _ in range(POLL_INTERVAL):
                if not _running: break
                time.sleep(1)

    except Exception as e:
        log.exception(f"Monitor Crashed: {e}")
    finally:
        PID_FILE.unlink(missing_ok=True)
        log.info("Monitor Stopped Cleanly.")

if __name__ == "__main__":
    monitor()
