IP=172.16.0.20
USRNAME=ubuntu
WORK_FOLDER=~/LedTable
APINAME=table-api
API_DEPL_NAME=table-api-depl
.PHONY: all
all:	kube www api


# --------------------
# --	deploy 		--
# --------------------

.PHONY: kube
kube: 
	rsync -ar /home/mathis/workspace/LedTable/kubernetes $(USRNAME)@$(IP):$(WORK_FOLDER)

.PHONY: www
www:
	rsync -ar /home/mathis/workspace/LedTable/www $(USRNAME)@$(IP):$(WORK_FOLDER)

.PHONY: api
api:
	rsync -ar /home/mathis/workspace/LedTable/api $(USRNAME)@$(IP):$(WORK_FOLDER)
	ssh -t $(USRNAME)@$(IP) 'microk8s kubectl rollout restart deployment $(API_DEPL_NAME)'

.PHONY: docker
docker:
	rsync -ar /home/mathis/workspace/LedTable/docker $(USRNAME)@$(IP):$(WORK_FOLDER)


# --------------------
# --	clean 		--
# --------------------
clean_www:
	ssh -t $(USRNAME)@$(IP) 'cd $(WORK_FOLDER)/www; rm -rf *'
clean_kube:
	ssh -t $(USRNAME)@$(IP) 'cd $(WORK_FOLDER)/kubernetes; rm -rf *'
clean_api:
	ssh -t $(USRNAME)@$(IP) 'cd $(WORK_FOLDER)/api; rm -rf *'

clean_all: clean_www clean_kube clean_api


# --------------------
# --	manage 		--
# --	cluster		--
# --------------------
shutdown:
	ssh -t $(USRNAME)@$(IP) 'microk8s stop'

.PHONY: start
start:
	ssh -t $(USRNAME)@$(IP) 'microk8s start'


# --------------------
# --	build 		--
# --	remote 		--
# --------------------

build_api:
	ssh -t $(USRNAME)@$(IP) 'cd $(WORK_FOLDER)/docker/api; docker build -t $(APINAME) .; sudo docker save $(APINAME) > $(APINAME).tar; microk8s ctr image import $(APINAME).tar; rm $(APINAME).tar'