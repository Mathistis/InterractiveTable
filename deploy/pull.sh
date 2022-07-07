echo "please use it only if you know what you do ..."
read A
echo "Well...."
rsync -ar ubuntu@172.16.0.20:~/LedTable/docker/conf/default.conf /home/mathis/workspace/LedTable/docker/conf
