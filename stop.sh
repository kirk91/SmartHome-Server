# kill wechat_server
ps -ef | grep wechat_server | grep -v grep | awk '{print $2}'  | sed -e "s/^/kill -9 /g" | sh -

# kill socket_server
ps -ef | grep socket_server | grep -v grep | awk '{print $2}'  | sed -e "s/^/kill -9 /g" | sh -

