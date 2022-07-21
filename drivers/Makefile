

IP=192.168.1.115
USRNAME=pi
WORK_FOLDER=~/LedTable
.PHONY: all
all:	kube www api

# --------------------
# --	deploy 		--
# --------------------

.PHONY: driver
driver: 
	rsync -ar /home/mathis/workspace/LedTable/drivers $(USRNAME)@$(IP):$(WORK_FOLDER)
	# ssh -t $(USRNAME)@$(IP) 'sudo systemctl restart Led_table.service'


# --------------------
# --	manage 		--
# --------------------

.PHONY: stop
stop: 
	ssh -t $(USRNAME)@$(IP) 'sudo systemctl stop Led_table.service'


# --------------------
# --	clean 		--
# --------------------
clean_driver:
	ssh -t $(USRNAME)@$(IP) 'cd $(WORK_FOLDER); rm -rf *'

clean_all: clean_driver

