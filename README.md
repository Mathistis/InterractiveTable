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
- check config **kubectl describe "ressource_name"**

## Dependencies
- cert-manager has to be installed to generate and serve certificate tls
    - i used the following commande to install:
    > microk8s kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.8.2/cert-manager.yaml
    **Important** check the current version and replace in url: https://cert-manager.io/docs/installation/supported-releases/

- http server : nginx:latest

- Microk8s addon: 
  - DNS         (to resolv some dns for exemple to contact let's encrypt api)
  - Ingress     (to have multiple services running in 1 URL)
  - Metallb     (to have type LoadBalancer to be able to specify a specific ip address for ingress entry point)

  > microk8s enable dns ingress metallb