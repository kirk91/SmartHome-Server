# start socket_server
python socket_server.py 1>>/var/log/raspberry-pi-wechat/socket_server.log 2>>/var/log/raspberry-pi-wechat/socket_server.log &

# start wechat_server
python wechat_server.py 1>>/var/log/raspberry-pi-wechat/wechat_server.log 2>>/var/log/raspberry-pi-wechat/wechat_server.log &
