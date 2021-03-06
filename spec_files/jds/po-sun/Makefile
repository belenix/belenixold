## 
# Makefile for generateing .po tarballs for Sun UI strings.
# 
# Generates  : $(PACKAGE)-po-sun-$(PO_VERSION).tar.bz2
#              e.g. po-sun-tarballs/*.tar.bz2
#
# Usage :
#           "make clean" : Remove previous tarballs
#
#           "make" : Update all .po tarballs
#
#           "make check-used" : Outputs list of .po not being used.
#
#           "make check-version" : Prints current .po tarball version
#
#           "make $(PACKAGE)-po-sun-$(PO_VERSION).tar.bz2
#               e.g. "make gnome-panel-po-sun-0.1.tar.bz2"
#                    will only generate gnome-panel's .po tarball
#
# For each package that contains .po files.
#  - Ensure all .po files for your package are located under the 
#    correct .po package dir i.e.
#    $package/ja.po
#
#  - Add Package name to PACKAGES Variable
#    e.g. PACKAGES = \
#             gnome-panel \
#             your-package
#
#  - Add two package specific variables 
#      PACKAGE_PAGES - Full path of all po for this package
#                      e.g.  gnome-panel_PAGES = gnome-panel
#      PACKAGE.PAGES - Assigned to $(PACKAGE_PAGES).
#                      e.g.   gnome-panel.PAGES: $(gnome-panel_PAGES)
#
#
# To Add new .po files to existing packages
# -----------------------------------------
# Put very simply, all that is required from engineers is to make some changes 
# and commit in SVN.
#
# - Ensure the .po file exists in SVN under the relevant package dir
# - Add .po files to the <package> directory
#      e.g. For a new gnome-panel de.po file it would be added in 
#      gnome-panel/de.po
# - Remake tarballs
#      $ make clean
#      $ make
#   This will re-generate all .po tarballs. 
# - Copy newly generated tarball from po-sun-tarballs to package build 
#   sources e.g. /jds/packages/SOURCES, and ensure package builds and po
#   install correctly.
# - New .po tarball will be generated by RE for each nightly, and for each
#   milestone build.
# - Commit change back to subverison, e.g. new/amended man pagees, 
#   po-sun/Makefile, po-sun/package/*.po files if affected.
#
#
# PO_VERSION is maintained by L10N and only gets bumped when spec-files gets
# branched. PLEASE do not change this.
# %po_sun_version is also updated in l10n.inc
#

PO_VERSION=0.1
PO_DIR=po-sun
TARBALL_DIR=po-sun-tarballs
BZIP2=/usr/bin/bzip2
TAR=/usr/bin/tar
AWK=/usr/bin/awk
MAKE=/usr/sfw/bin/gmake
NULL=

PACKAGES = \
	alacarte			\
	brasero				\
	dasher				\
	devhelp				\
	ekiga				\
	eog				\
	evince				\
	evolution			\
	file-roller			\
	gcalctool			\
	gdesklets			\
	gdm				\
	gedit				\
	ghex				\
	gimp				\
	gksu				\
	glade				\
	gnome-control-center		\
	gnome-desktop			\
	gnome-media			\
	gnome-menus			\
	gnome-netstatus			\
	gnome-panel			\
	gnome-pilot			\
	gnome-power-manager		\
	gnome-session			\
	gnome-system-monitor		\
	gnome-system-tools		\
	gnome-terminal			\
	gnome-utils			\
	gnome-vfs			\
	gnome-volume-manager		\
	gok				\
	gthumb				\
	gtk2				\
	gtkam				\
	gucharmap			\
	libgksuui			\
	libwnck				\
	metacity			\
	nautilus			\
	orca				\
	pidgin				\
	printman			\
	sound-juicer			\
	system-config-printer		\
	totem				\
	tracker				\
	vino				\
	xdg-user-dirs			\
	yelp				\
	$(NULL)

all: TARBALLS

alacarte_PAGES = alacarte/po-sun
alacarte.PAGES: $(alacarte_PAGES)

brasero_PAGES = brasero/po-sun
brasero.PAGES: $(brasero_PAGES)

dasher_PAGES = dasher/po-sun
dasher.PAGES: $(dasher_PAGES)

devhelp_PAGES = devhelp/po-sun
devhelp.PAGES: $(devhelp_PAGES)

ekiga_PAGES = ekiga/po-sun
ekiga.PAGES: $(ekiga_PAGES)

eog_PAGES = eog/po-sun
eog.PAGES: $(eog_PAGES)

evince_PAGES = evince/po-sun
evince.PAGES: $(evince_PAGES)

evolution_PAGES = evolution/po-sun
evolution.PAGES: $(evolution_PAGES)

file-roller_PAGES = file-roller/po-sun
file-roller.PAGES: $(file-roller_PAGES)

gcalctool_PAGES = gcalctool/po-sun
gcalctool.PAGES: $(gcalctool_PAGES)

gdesklets_PAGES = gdesklets/po-sun
gdesklets.PAGES: $(gdesklets_PAGES)

gdm_PAGES = gdm/po-sun
gdm.PAGES: $(gdm_PAGES)

gedit_PAGES = gedit/po-sun
gedit.PAGES: $(gedit_PAGES)

ghex_PAGES = ghex/po-sun
ghex.PAGES: $(ghex_PAGES)

gimp_PAGES = gimp/po-sun
gimp.PAGES: $(gimp_PAGES)

gksu_PAGES = gksu/po-sun
gksu.PAGES: $(gksu_PAGES)

glade_PAGES = glade/po-sun
glade.PAGES: $(glade_PAGES)

gnome-control-center_PAGES = gnome-control-center/po-sun
gnome-control-center.PAGES: $(gnome-control-center_PAGES)

gnome-desktop_PAGES = gnome-desktop/po-sun
gnome-desktop.PAGES: $(gnome-desktop_PAGES)

gnome-media_PAGES = gnome-media/po-sun
gnome-media.PAGES: $(gnome-media_PAGES)

gnome-menus_PAGES = gnome-menus/po-sun
gnome-menus.PAGES: $(gnome-menus_PAGES)

gnome-netstatus_PAGES = gnome-netstatus/po-sun
gnome-netstatus.PAGES: $(gnome-netstatus_PAGES)

gnome-panel_PAGES = gnome-panel/po-sun
gnome-panel.PAGES: $(gnome-panel_PAGES)

gnome-pilot_PAGES = gnome-pilot/po-sun
gnome-pilot.PAGES: $(gnome-pilot_PAGES)

gnome-power-manager_PAGES = gnome-power-manager/po-sun
gnome-power-manager.PAGES: $(gnome-power-manager_PAGES)

gnome-session_PAGES = gnome-session/po-sun
gnome-session.PAGES: $(gnome-session_PAGES)

gnome-system-monitor_PAGES = gnome-system-monitor/po-sun
gnome-system-monitor.PAGES: $(gnome-system-monitor_PAGES)

gnome-system-tools_PAGES = gnome-system-tools/po-sun
gnome-system-tools.PAGES: $(gnome-system-tools_PAGES)

gnome-terminal_PAGES = gnome-terminal/po-sun
gnome-terminal.PAGES: $(gnome-terminal_PAGES)

gnome-utils_PAGES = gnome-utils/po-sun
gnome-utils.PAGES: $(gnome-utils_PAGES)

gnome-vfs_PAGES = gnome-vfs/po-sun
gnome-vfs.PAGES: $(gnome-vfs_PAGES)

gnome-volume-manager_PAGES = gnome-volume-manager/po-sun
gnome-volume-manager.PAGES: $(gnome-volume-manager_PAGES)

gok_PAGES = gok/po-sun
gok.PAGES: $(gok_PAGES)

gthumb_PAGES = gthumb/po-sun
gthumb.PAGES: $(gthumb_PAGES)

gtk2_PAGES = gtk2/po-sun
gtk2.PAGES: $(gtk2_PAGES)

gtkam_PAGES = gtkam/po-sun
gtkam.PAGES: $(gtkam_PAGES)

gucharmap_PAGES = gucharmap/po-sun
gucharmap.PAGES: $(gucharmap_PAGES)

libgksuui_PAGES = libgksuui/po-sun
libgksuui.PAGES: $(libgksuui_PAGES)

libwnck_PAGES = libwnck/po-sun
libwnck.PAGES: $(libwnck_PAGES)

metacity_PAGES = metacity/po-sun
metacity.PAGES: $(metacity_PAGES)

nautilus_PAGES = nautilus/po-sun
nautilus.PAGES: $(nautilus_PAGES)

orca_PAGES = orca/po-sun
orca.PAGES: $(orca_PAGES)

pidgin_PAGES = pidgin/po-sun
pidgin.PAGES: $(pidgin_PAGES)

printman_PAGES = printman/po-sun
printman.PAGES: $(printman_PAGES)

sound-juicer_PAGES = sound-juicer/po-sun
sound-juicer.PAGES: $(sound-juicer_PAGES)

system-config-printer_PAGES = system-config-printer/po-sun
system-config-printer.PAGES: $(system-config-printer_PAGES)

totem_PAGES = totem/po-sun
totem.PAGES: $(totem_PAGES)

tracker_PAGES = tracker/po-sun
tracker.PAGES: $(tracker_PAGES)

vino_PAGES = vino/po-sun
vino.PAGES: $(vino_PAGES)

xdg-user-dirs_PAGES = xdg-user-dirs/po-sun
xdg-user-dirs.PAGES: $(xdg-user-dirs_PAGES)

yelp_PAGES = yelp/po-sun
yelp.PAGES: $(yelp_PAGES)

TARBALL_DIR_SUFFIX = po-sun-$(PO_VERSION)

.SUFFIXES: -$(TARBALL_DIR_SUFFIX).tar.bz2 .PAGES
.SUFFIXES: .check-used .PAGES

TARBALLS = $(TARBALL_DIR)/$(addsuffix -$(TARBALL_DIR_SUFFIX).tar.bz2, $(PACKAGES))


TARBALLS: 
	@test -d $(TARBALL_DIR) ||  mkdir -p "$(TARBALL_DIR)"
	@test -x $(BZIP2) || echo "bzip2 utility not found"
	@for package in $(PACKAGES); do \
		if test ! -f $(TARBALL_DIR)/$$package-$(TARBALL_DIR_SUFFIX).tar.bz2; then \
			$(MAKE) MAKE=\"$(MAKE)\" $$package-$(TARBALL_DIR_SUFFIX).tar.bz2; \
		fi; \
	done

%-$(TARBALL_DIR_SUFFIX).tar.bz2: %.PAGES
	@test -d $(TARBALL_DIR) ||  mkdir -p "$(TARBALL_DIR)"
	@if test -f $(TARBALL_DIR)/$@; then \
		rm -f $(TARBALL_DIR)/$@; \
	fi
	@test -d $(PO_DIR) ||  mkdir -p "$(PO_DIR)"
	@rm -rf $(PO_DIR)/*
	@for po_dir in $($(subst .PAGES,_PAGES,$<)); do \
		cp -R $$po_dir "$(PO_DIR)"; \
		base_po_dir=`basename $$po_dir`; \
		cp Makefile.template "$(PO_DIR)"/$$base_po_dir/Makefile; \
	done;
	@cd "$(PO_DIR)"; \
		tarball=`basename "$@" .bz2`; echo "Making tarball $$tarball"; \
		$(TAR) -cf ../$(TARBALL_DIR)/$$tarball *; \
		$(BZIP2) ../$(TARBALL_DIR)/$$tarball; \
		cd ..
	@rm -rf $(PO_DIR)

check-used: 
	@test -d check-used-po-sun ||  mkdir -p "check-used-po-sun"
	@test -d check-all-po-sun ||  mkdir -p "check-all-po-sun"
	@rm -f unused-po-sun.txt
	@for package in $(PACKAGES); do \
		$(MAKE) MAKE=\"$(MAKE)\" $$package.check-used; \
	done
	@rm -rf check-all-po-sun
	@rm -rf check-used-po-sun

%.check-used: %.PAGES
	@for package in $($(subst .PAGES,_PAGES,$<)); do \
		touch check-used-po-sun/$$package; \
	done

check-version:
	@echo $(PO_VERSION)

clean:
	rm -rf $(PO_DIR)
	rm -rf $(TARBALL_DIR)

