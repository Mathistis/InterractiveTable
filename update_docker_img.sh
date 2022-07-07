cd /home/ubuntu/LedTable/docker
sudo docker build -t ssl-https .
sudo docker save ssl-https > ssl-https.tar
sudo microk8s ctr image import ssl-https.tar