# Server deployment (Ubuntu + systemd + Nginx)

This guide runs the app with Uvicorn behind Nginx.

## 1) Server packages

```bash
sudo apt update
sudo apt install -y python3-venv nginx
```

## 2) App setup

```bash
cd /opt
sudo mkdir -p portfolio
sudo chown $USER:$USER /opt/portfolio

git clone <your-repo-url> /opt/portfolio
cd /opt/portfolio

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## 3) systemd service

Copy the service file and adjust paths/user if needed.

```bash
sudo cp /opt/portfolio/deploy/portfolio.service /etc/systemd/system/portfolio.service
sudo systemctl daemon-reload
sudo systemctl enable --now portfolio
sudo systemctl status portfolio
```

## 4) Nginx

Copy the Nginx config, set your domain, and reload Nginx.

```bash
sudo cp /opt/portfolio/deploy/nginx-portfolio.conf /etc/nginx/sites-available/portfolio
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/portfolio
sudo nginx -t
sudo systemctl reload nginx
```

## 5) Optional: HTTPS

If you have a domain pointing to the server:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```

