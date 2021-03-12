# snap-pac
# https://github.com/wesbarnett/snap-pac
# Copyright (C) 2016-2021 James W. Barnett

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,

PKGNAME = snap-pac
PREFIX ?= /usr

SHARE_DIR = $(DESTDIR)$(PREFIX)/share

.PHONY: install

install:
	@install -Dm755 scripts/snap_pac.py $(SHARE_DIR)/libalpm/scripts/snap-pac
	@install -Dm644 hooks/* -t $(SHARE_DIR)/libalpm/hooks/
	@install -Dm644 LICENSE -t $(SHARE_DIR)/licenses/$(PKGNAME)/
	@install -Dm644 man8/* -t $(SHARE_DIR)/man/man8/
	@install -Dm644 README.md -t $(SHARE_DIR)/doc/$(PKGNAME)/
	@install -Dm644 extra/snap-pac.ini $(DESTDIR)/etc/snap-pac.ini.example

test:
	@python -m pytest -v .
