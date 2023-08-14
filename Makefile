COMPONENT?=gescraft
VERSION:=src/$(COMPONENT)/version.py

include make/ci.mk
include make/install.mk
include make/lint.mk
include make/test.mk
include make/version.mk
