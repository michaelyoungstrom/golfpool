SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help
.PHONY: requirements

help:
	  @echo ''
	  @echo 'Makefile for '
	  @echo '     make help            show this information'
	  @echo '     make requirements    install requirements for this project'

requirements:
	  pip install -r requirements.txt
