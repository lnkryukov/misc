
# Пример конфига для nginx для проксирования запросов

Запрос на сам домен возврващает статику, запрос на поддомен api.* перенаправляет запрос к бекенду. Надо шаманить с DNS чтобы заработало.  
В папках server1 и server2 лежат тупые сервера для тестирования.
Один живет на 4000, другой на 5000 портах.  

## Instructions

1. 
```bash
python3 -m virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
2.
```bash
sudo yum install nginx 
sudo systemctl enable nginx
sudo systemctl start nginx
```

3. Из-за гребанного SELinux нужно делать [так](https://www.digitalocean.com/community/questions/403-forbidden-nginx-13-permission-denied), чтобы не было ошибок с permission denied.
```bash
sudo setsebool -P httpd_can_network_connect on 
sudo chcon -Rt httpd_sys_content_t /path/to/www
```

4. Конфиги класть в `/etc/nginx/conf.d`.

## SSL

```
listen 4000 ssl;
error_page 497 301 =307 https://$http_host$uri;

ssl_certificate "/etc/pki/tls/certs/server.crt";
ssl_certificate_key "/etc/pki/tls/private/server.key";
```

