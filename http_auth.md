[root@www ~]# vi /etc/httpd/conf.d/auth_basic.conf
# create new
<Directory /var/www/html/auth-basic>
    AuthType Basic
    AuthName "Basic Authentication"
    AuthUserFile /etc/httpd/conf/.htpasswd
    require valid-user
</Directory>
# add a user : create a new file with "-c" ( add the "-c" option only for the initial registration )
[root@www ~]# htpasswd -c /etc/httpd/conf/.htpasswd fedora 
New password:     # set password
Re-type new password:
Adding password for user fedora
[root@www ~]# mkdir /var/www/html/auth-basic 
[root@www ~]# vi /var/www/html/auth-basic/index.html
# create a test page
 <html>
<body>
<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
Test Page for Basic Auth
</div>
</body>
</html>

[root@www ~]# systemctl restart httpd