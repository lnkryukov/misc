1. Selinux nginx Permission denied
sudo setsebool -P httpd_can_network_connect on 
sudo chcon -Rt httpd_sys_content_t /path/to/www

2. npm
 
scripts {
  ...
  "deploy": "npm install && npm run build && mv build/* $DEPLOY_LOCATION"
}
