# Deployment Guide

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Git
- Virtual environment (recommended)
- SSL certificate (for production)

## Environment Setup

### 1. Development Environment

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/telecomdb1.git
   cd telecomdb1
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   python scripts/setup.py
   ```

5. **Initialize Database**
   ```bash
   alembic upgrade head
   ```

6. **Run Development Server**
   ```bash
   python api/app.py
   ```

### 2. Staging Environment

1. **Server Requirements**
   - Ubuntu 20.04 LTS or higher
   - 2GB RAM minimum
   - 20GB storage
   - Public IP address

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx
   ```

3. **Configure PostgreSQL**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE telecomdb;
   CREATE USER telecomuser WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE telecomdb TO telecomuser;
   \q
   ```

4. **Deploy Application**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/telecomdb1.git
   cd telecomdb1

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Configure environment
   python scripts/setup.py

   # Initialize database
   alembic upgrade head
   ```

5. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

6. **Configure Systemd Service**
   ```ini
   [Unit]
   Description=Telecom Billing API
   After=network.target

   [Service]
   User=your_user
   WorkingDirectory=/path/to/telecomdb1
   Environment="PATH=/path/to/telecomdb1/venv/bin"
   ExecStart=/path/to/telecomdb1/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 api.app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Services**
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   sudo systemctl start telecom-api
   sudo systemctl enable telecom-api
   ```

### 3. Production Environment

1. **Server Requirements**
   - Ubuntu 20.04 LTS or higher
   - 4GB RAM minimum
   - 50GB storage
   - Public IP address
   - SSL certificate

2. **Security Setup**
   ```bash
   # Configure firewall
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable

   # Install SSL certificate
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your_domain.com
   ```

3. **Database Setup**
   ```bash
   # Configure PostgreSQL
   sudo -u postgres psql
   CREATE DATABASE telecomdb;
   CREATE USER telecomuser WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE telecomdb TO telecomuser;
   \q

   # Configure PostgreSQL for production
   sudo nano /etc/postgresql/12/main/postgresql.conf
   # Set:
   # max_connections = 100
   # shared_buffers = 1GB
   # effective_cache_size = 3GB
   # maintenance_work_mem = 256MB
   ```

4. **Application Deployment**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/telecomdb1.git
   cd telecomdb1

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Configure environment
   python scripts/setup.py

   # Initialize database
   alembic upgrade head
   ```

5. **Configure Nginx with SSL**
   ```nginx
   server {
       listen 443 ssl;
       server_name your_domain.com;

       ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }

   server {
       listen 80;
       server_name your_domain.com;
       return 301 https://$server_name$request_uri;
   }
   ```

6. **Configure Systemd Service**
   ```ini
   [Unit]
   Description=Telecom Billing API
   After=network.target

   [Service]
   User=your_user
   WorkingDirectory=/path/to/telecomdb1
   Environment="PATH=/path/to/telecomdb1/venv/bin"
   Environment="PYTHONPATH=/path/to/telecomdb1"
   Environment="FLASK_ENV=production"
   ExecStart=/path/to/telecomdb1/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 api.app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Services**
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   sudo systemctl start telecom-api
   sudo systemctl enable telecom-api
   ```

## Monitoring and Maintenance

### 1. Logging

1. **Application Logs**
   ```bash
   sudo journalctl -u telecom-api -f
   ```

2. **Nginx Logs**
   ```bash
   sudo tail -f /var/log/nginx/access.log
   sudo tail -f /var/log/nginx/error.log
   ```

3. **Database Logs**
   ```bash
   sudo tail -f /var/log/postgresql/postgresql-12-main.log
   ```

### 2. Backup

1. **Database Backup**
   ```bash
   # Create backup
   python scripts/backup_db.py

   # Restore backup
   psql -U telecomuser -d telecomdb < backup_file.sql
   ```

2. **Configuration Backup**
   ```bash
   # Backup .env file
   cp .env .env.backup

   # Backup Nginx configuration
   sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup
   ```

### 3. Updates

1. **Application Update**
   ```bash
   # Pull latest changes
   git pull origin main

   # Update dependencies
   pip install -r requirements.txt

   # Run migrations
   alembic upgrade head

   # Restart service
   sudo systemctl restart telecom-api
   ```

2. **SSL Certificate Renewal**
   ```bash
   sudo certbot renew
   ```

### 4. Performance Monitoring

1. **System Resources**
   ```bash
   # CPU and Memory
   top
   htop

   # Disk Usage
   df -h
   du -sh /path/to/telecomdb1
   ```

2. **Database Performance**
   ```sql
   -- Check active connections
   SELECT * FROM pg_stat_activity;

   -- Check slow queries
   SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
   ```

## Troubleshooting

### Common Issues

1. **Application Not Starting**
   - Check logs: `sudo journalctl -u telecom-api -f`
   - Verify environment variables
   - Check file permissions

2. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check connection string
   - Verify user permissions

3. **SSL Certificate Issues**
   - Check certificate expiration
   - Verify Nginx configuration
   - Check file permissions

4. **Performance Issues**
   - Monitor system resources
   - Check database indexes
   - Review application logs

### Getting Help

1. **Internal Resources**
   - Check application logs
   - Review system logs
   - Consult team members

2. **External Resources**
   - Stack Overflow
   - GitHub Issues
   - Documentation 