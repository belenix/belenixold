## 
# Convenience Makefile.
# 
# Usage :
# 
#     "make clean" : Clean up sun-po and manpages directories
#     "make" :       Build the po and manpage files
#

all: subdirectories

subdirectories:
	$(MAKE) -C po-sun
	$(MAKE) -C manpages
	@echo
	@echo "NOTE:"
	@echo " This Makefile just builds its dependencies. It isn't meant to"
	@echo " build the all packages in the repository."
	@echo

clean:
	$(MAKE) -C po-sun clean
	$(MAKE) -C manpages clean

