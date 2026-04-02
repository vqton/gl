# DEPLOYMENT GUIDE - Kế toán SME

## Prerequisites
- Windows Server 2019+ or Windows 10/11
- Python 3.12+
- .NET Framework 4.8+ (for Waitress)

## Quick Start (Development)
```powershell
# 1. Clone and setup
cd E:\gl
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 2. Configure environment
copy .env.example .env
# Edit .env and set SECRET_KEY, ENCRYPTION_KEY

# 3. Initialize database
python manage.py migrate
python manage.py loaddata apps/danh_muc/fixtures/seed_accounts.json
python manage.py createsuperuser

# 4. Run development server
python manage.py runserver 0.0.0.0:8000
```

## Production Deployment (Waitress)

### 1. Install Waitress
```powershell
pip install waitress
```

### 2. Start Production Server
```powershell
waitress-serve --listen=0.0.0.0:8000 --threads=8 --call core.wsgi:application
```

### 3. Windows Service (NSSM)
```powershell
# Download NSSM: https://nssm.cc/
nssm install KeToanSME "E:\gl\venv\Scripts\waitress-serve.exe"
nssm set KeToanSME AppParameters "--listen=0.0.0.0:8000 --threads=8 --call core.wsgi:application"
nssm set KeToanSME AppDirectory "E:\gl"
nssm set KeToanSME Start SERVICE_AUTO_START
nssm start KeToanSME
```

### 4. Scheduled Tasks
```powershell
# Daily backup at 23:00
schtasks /Create /TN "KeToanSME_Backup" /TR "E:\gl\deploy\backup.bat" /SC DAILY /ST 23:00 /RL HIGHEST

# Nightly inventory recalculation at 23:30
schtasks /Create /TN "KeToanSME_Recalculate" /TR "E:\gl\deploy\recalculate.bat" /SC DAILY /ST 23:30 /RL HIGHEST
```

### 5. Firewall Configuration
```powershell
# Open port 8000 for internal network only
New-NetFirewallRule -DisplayName "KeToan SME" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow -RemoteAddress 192.168.1.0/24
```

## Backup & Recovery

### Manual Backup
```powershell
# Stop service
nssm stop KeToanSME

# Copy database
copy E:\gl\db.sqlite3 E:\backup\db_$(Get-Date -Format 'yyyyMMdd').sqlite3

# Restart service
nssm start KeToanSME
```

### Restore from Backup
```powershell
# Stop service
nssm stop KeToanSME

# Restore database
copy E:\backup\db_YYYYMMDD.sqlite3 E:\gl\db.sqlite3

# Restart service
nssm start KeToanSME
```

## Monitoring

### Health Check
```powershell
# Check if server is running
curl http://localhost:8000/admin/

# Check database integrity
python manage.py dbshell
> PRAGMA integrity_check;
```

### Log Files
- Application logs: `E:\gl\logs\app.log`
- Waitress logs: Console output (redirect to file if needed)

## Security Checklist
- [ ] Set `DEBUG=False` in `.env`
- [ ] Set strong `SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to internal IPs only
- [ ] Set `ENCRYPTION_KEY` for sensitive data
- [ ] Configure Windows Firewall for internal network only
- [ ] Set up daily automated backups
- [ ] Use HTTPS with reverse proxy (optional)
- [ ] Regular Windows Updates
