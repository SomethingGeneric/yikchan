test:
	python3 app.py
pip:
	sudo pip3 install -r requirements.txt
deploy: pip
	cp yikchan.service new.service
	python3 sed.py
	sudo mv new.service /etc/systemd/system/yikchan.service
	sudo systemctl daemon-reload
	sudo systemctl enable --now yikchan.service
undeploy:
	sudo systemctl stop yikchan.service
	sudo systemctl disable yikchan.service
	sudo rm /etc/systemd/system/yikchan.service
	sudo systemctl daemon-reload
update: pip undeploy
	git pull
	make deploy