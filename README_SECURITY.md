# Security Configuration

## Database Credentials

For security reasons, database credentials have been removed from the source code.
You must configure the following environment variables before running the application:

*   `DB_IP`: The IP address of the SQL Server (e.g., `192.168.0.100`)
*   `DB_USER`: The database user (e.g., `debo`)
*   `DB_PASS`: The database password
*   `DB_NAME`: The database name (e.g., `DEBO`)

### How to set environment variables

#### Linux / macOS
```bash
export DB_IP="192.168.0.100"
export DB_USER="debo"
export DB_PASS="your_secure_password"
export DB_NAME="DEBO"
python3 iniciarVentaW.py
```

#### Windows (PowerShell)
```powershell
$env:DB_IP="192.168.0.100"
$env:DB_USER="debo"
$env:DB_PASS="your_secure_password"
$env:DB_NAME="DEBO"
python iniciarVentaW.py
```

#### Windows (CMD)
```cmd
set DB_IP=192.168.0.100
set DB_USER=debo
set DB_PASS=your_secure_password
set DB_NAME=DEBO
python iniciarVentaW.py
```
