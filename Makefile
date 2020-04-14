REQUIREMENTS=requirements.txt
ENV=env

help:
	@echo "init-db           - init database "
	@echo "run               -  run  project"
	@echo "env               - create envioroment"
	@echo "clean env         - remove enviroment"
	@echo "pip-install_req   - install requirements"

env:
	virtualenv -p python3 $@
	$(MAKE) pip_install REQUIREMENTS=$(REQUIREMENTS)


pip_install:
	env/bin/pip install -r $(REQUIREMENTS)

pip-install-req:
	env/bin/pip install -r requirements.txt

clean_env:
	rm -rdf env

pip_freeze:
	env/bin/pip freeze > $(REQUIREMENTS)

update_requirements:
	$(MAKE) pip_freeze
	$(MAKE) pip_install REQUIREMENTS=$(REQUIREMENTS)