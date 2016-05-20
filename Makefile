# snap-pac
# https://github.com/wesbarnett/snap-pac
# Copyright (C) 2016 James W. Barnett

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

.DEFAULT = install

SCRIPTS_DIR=$(DESTDIR)/usr/share/libalpm/scripts/
HOOKS_DIR=$(DESTDIR)/usr/share/libalpm/hooks/

.PHONY: install
install:
	install -d $(HOOKS_DIR)
	install -d $(SCRIPTS_DIR)
	install -Dm 755 snap-pac $(SCRIPTS_DIR)
	install -Dm 644 00_snapper-pre.hook $(HOOKS_DIR)
	install -Dm 644 zz_snapper-post.hook $(HOOKS_DIR)
	install -Dm 644 LICENSE $(DESTDIR)/usr/share/licenses/snap-pac/LICENSE
