# InterractiveTable
Summer projet made because of interrest of technologie. The only goal is to learn more kuberneter and design a full architecture with embedded system and mecanical job.

## Table creation
User interract with website to draw some patterns. Once the pattern is ready, it is displayed on a table which contains matrix of LED RGB.

## Trobbleshooting
- If the load balancer do not work, (curl 172.16.0.49) make sure you have enabled metallb (microk8s enable metallb)
- If previous step is correct, test the dns redirection through the double home's routes (curl raemylab.ch)
    - make sure the configuration of router in DMZ (172.16.0.1) is correct telnet --> (configure --> pinhole --> view)
    - reboot router.
- restart cluster
- check config kubectl describe "ressource_name"