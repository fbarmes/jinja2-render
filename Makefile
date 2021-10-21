#!/usr/bin/make -f

#-------------------------------------------------------------------------------
# Main variables
#-------------------------------------------------------------------------------

#--
# artifact name
ARTIFACT=jinja2-render


#--
# where to generate the artifacts
TARGET_DIR=target

#--
# artifact coordinates
PROJECT_VERSION=$(shell cat VERSION)

#--
# package name
PACKAGE=${ARTIFACT}-${PROJECT_VERSION}.zip

#--
# define the list of objects at project root that should be included in artifact
ROOT_OBJECTS=
ROOT_OBJECTS+=$(shell ls *.py )
ROOT_OBJECTS+=VERSION README.md


#-------------------------------------------------------------------------------
.PHONY: echo
echo:
	@echo ""
	@echo "--------------------------------------------"
	@echo " Makefile parameters"
	@echo "--------------------------------------------"
	@echo ""
	@echo "PROJECT_VERSION=${PROJECT_VERSION}"
	@echo "ARTIFACT=${ARTIFACT}"
	@echo "PACKAGE=${PACKAGE}"


#-------------------------------------------------------------------------------
.PHONY: init
init:
	@echo "init - START"
	mkdir -p ${TARGET_DIR}
	mkdir -p ${TARGET_DIR}/${ARTIFACT}
	@echo "init - DONE"

#-------------------------------------------------------------------------------
.PHONY: clean
clean:
	rm -rf ${TARGET_DIR}


#-------------------------------------------------------------------------------
${TARGET_DIR}/deps.touch:
	@echo "deps - START"
	pip3 install -r requirements.txt -t ${TARGET_DIR}/${ARTIFACT}
	touch ${TARGET_DIR}/deps.touch
	@echo "deps - DONE"

#-------------------------------------------------------------------------------
.PHONY: deps
deps: init ${TARGET_DIR}/deps.touch
	@echo "deps - DONE"


#-------------------------------------------------------------------------------
.PHONY: package
package: init
	@echo "package - START"
	cp ${ROOT_OBJECTS} ${TARGET_DIR}/${ARTIFACT}


#-------------------------------------------------------------------------------
# Targets run inside builder image
#-------------------------------------------------------------------------------
