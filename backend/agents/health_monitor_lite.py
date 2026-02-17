#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 CODEX Health Monitor Lite
Простий агент моніторингу без хмарних залежностей
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.system('chcp 65001 >nul 2>&1')

import time
import json
import socket
import psutil
import requests
from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class HealthMonitorLite:
    def __init__(self):
        self.services = {
            "frontend": {"port": 3001, "url": "http://localhost:3001"},
            "backend": {"port": 8001, "url": "http://localhost:8001/health"},
            "database": {"port": 5433, "url": None},
            "minio": {"port": 9002, "url": None},
            "redis": {"port": 6379, "url": None},
            "flower": {"port": 5555, "url": "http://localhost:5555"}
        }
        
        self.log_file = Path("monitor_logs.json")
        self.status_file = Path("current_status.json")
        self.alert_email = None  # Встановимо пізніше
        
        print("🤖 Health Monitor Lite initialized")
        print(f"📝 Logs: {self.log_file.absolute()}")
        print(f"📊 Status: {self.status_file.absolute()}")
    
    def check_port(self, port: int) -> bool:
        """Перевірити чи порт доступний"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except:
            return False
    
    def check_http(self, url: str) -> dict:
        """Перевірити HTTP endpoint"""
        try:
            response = requests.get(url, timeout=5)
            return {
                "status": "ok" if response.status_code == 200 else "error",
                "code": response.status_code,
                "time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {
                "status": "error",
                "code": 0,
                "error": str(e)
            }
    
    def check_system_resources(self) -> dict:
        """Перевірити системні ресурси"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu": {
                    "percent": cpu_percent,
                    "status": "ok" if cpu_percent < 80 else "warning"
                },
                "memory": {
                    "percent": memory.percent,
                    "used_gb": round(memory.used / (1024**3), 2),
                    "total_gb": round(memory.total / (1024**3), 2),
                    "status": "ok" if memory.percent < 80 else "warning"
                },
                "disk": {
                    "percent": disk.percent,
                    "used_gb": round(disk.used / (1024**3), 2),
                    "total_gb": round(disk.total / (1024**3), 2),
                    "status": "ok" if disk.percent < 80 else "warning"
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    def check_all_services(self) -> dict:
        """Перевірити всі сервіси"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "system": self.check_system_resources(),
            "overall_status": "ok"
        }
        
        for service_name, config in self.services.items():
            print(f"🔍 Checking {service_name}...")
            
            service_status = {
                "port_open": self.check_port(config["port"]),
                "timestamp": datetime.now().isoformat()
            }
            
            if config["url"]:
                service_status["http"] = self.check_http(config["url"])
            
            # Визначити статус
            if not service_status["port_open"]:
                service_status["status"] = "down"
                results["overall_status"] = "error"
            elif config["url"] and service_status["http"]["status"] == "error":
                service_status["status"] = "warning"
                if results["overall_status"] == "ok":
                    results["overall_status"] = "warning"
            else:
                service_status["status"] = "ok"
            
            results["services"][service_name] = service_status
            
            # Вивести результат
            status_emoji = "✅" if service_status["status"] == "ok" else "❌"
            print(f"  {status_emoji} {service_name}: {service_status['status']}")
        
        return results
    
    def log_results(self, results: dict):
        """Зберегти результати в лог"""
        # Додати до історії
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(results)
        
        # Зберігати тільки останні 100 записів
        logs = logs[-100:]
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        # Зберегти поточний статус
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    def send_email_alert(self, subject: str, message: str):
        """Відправити email сповіщення"""
        if not self.alert_email:
            return
        
        try:
            # Використовуємо Gmail SMTP (безкоштовно)
            # Потрібно створити App Password в Google Account
            
            msg = MIMEMultipart()
            msg['From'] = self.alert_email
            msg['To'] = self.alert_email
            msg['Subject'] = f"🤖 CODEX Alert: {subject}"
            
            body = f"""
            CODEX Health Monitor Alert
            
            {message}
            
            Timestamp: {datetime.now()}
            
            Check dashboard: http://localhost:8000/monitor
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            # server.login(self.alert_email, app_password)
            # server.send_message(msg)
            server.quit()
            
            print(f"📧 Email alert sent: {subject}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
    
    def check_for_problems(self, results: dict):
        """Перевірити чи є проблеми"""
        problems = []
        
        # Перевірити сервіси
        for service_name, status in results["services"].items():
            if status["status"] == "down":
                problems.append(f"❌ {service_name} is DOWN!")
            elif status["status"] == "warning":
                problems.append(f"⚠️ {service_name} has issues")
        
        # Перевірити ресурси
        system = results["system"]
        if system.get("cpu", {}).get("status") == "warning":
            problems.append(f"⚠️ High CPU usage: {system['cpu']['percent']}%")
        
        if system.get("memory", {}).get("status") == "warning":
            problems.append(f"⚠️ High memory usage: {system['memory']['percent']}%")
        
        if system.get("disk", {}).get("status") == "warning":
            problems.append(f"⚠️ High disk usage: {system['disk']['percent']}%")
        
        # Відправити alert якщо є проблеми
        if problems:
            message = "\n".join(problems)
            print(f"\n🚨 PROBLEMS DETECTED:\n{message}\n")
            self.send_email_alert("Problems Detected", message)
        
        return problems
    
    def run_once(self):
        """Одна перевірка"""
        print("\n" + "="*50)
        print(f"🤖 Health Check: {datetime.now()}")
        print("="*50)
        
        results = self.check_all_services()
        self.log_results(results)
        self.check_for_problems(results)
        
        print(f"\n📊 Overall Status: {results['overall_status'].upper()}")
        print("="*50 + "\n")
        
        return results
    
    def run_forever(self, interval: int = 300):
        """Запустити постійний моніторинг"""
        print(f"🚀 Starting continuous monitoring (every {interval}s)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.run_once()
                print(f"💤 Sleeping for {interval} seconds...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Monitor stopped by user")


def main():
    """Головна функція"""
    import sys
    
    monitor = HealthMonitorLite()
    
    # Опціонально: встановити email для сповіщень
    # monitor.alert_email = "your_email@gmail.com"
    
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        # Одна перевірка
        monitor.run_once()
    else:
        # Постійний моніторинг (кожні 5 хвилин)
        monitor.run_forever(interval=300)


if __name__ == "__main__":
    main()
