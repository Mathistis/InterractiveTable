IP=172.16.0.20
USRNAME=ubuntu
WORK_FOLDER=~/LedTable/

kube: 
	rsync -ar /home/mathis/workspace/LedTable/kubernetes $(USRNAME)@$(IP):$(WORK_FOLDER)

www:
	rsync -ar /home/mathis/workspace/LedTable/www $(USRNAME)@$(IP):$(WORK_FOLDER)

shutdown:
	ssh -t $(USRNAME)@$(IP) 'microk8s stop'

start:
	ssh -t $(USRNAME)@$(IP) 'microk8s start'

clean_www:
	ssh -t $(USRNAME)@$(IP) 'cd $(WORK_FOLDER)/www; rm -rf *'
clean_kube:
	ssh -t $(USRNAME)@$(IP) 'cd $(WORK_FOLDER)/kubernetes; rm -rf *'

clean_all:
	ssh -t $(USRNAME)@$(IP) 'cd $(WORK_FOLDER)/www; rm -rf *'
	ssh -t $(USRNAME)@$(IP) 'cd $(WORK_FOLDER)/kubernetes; rm -rf *'
