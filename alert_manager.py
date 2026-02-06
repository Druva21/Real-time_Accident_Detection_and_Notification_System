import time
from datetime import datetime
try:
    from tkinter import messagebox
except Exception:
    messagebox = None

class AlertManager:
    def __init__(self, cooldown_seconds=30):
        self.last_alert_time = 0
        self.cooldown = cooldown_seconds

    def can_alert(self):
        import time as _time
        return (_time.time() - self.last_alert_time) > self.cooldown

    def trigger_alert(self, severity, alert_type="Collision", gui=True):
        now = time.time()
        if not self.can_alert():
            return False
        msg = (f"🚨 Accident Detected!\n"
               f"Type: {alert_type}\n"
               f"Severity: {severity:.2f}\n"
               f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(msg)
        if gui and messagebox:
            try:
                messagebox.showwarning("Emergency Alert", msg)
            except Exception as e:
                print("Popup failed:", e)
        self.last_alert_time = now
        return True
