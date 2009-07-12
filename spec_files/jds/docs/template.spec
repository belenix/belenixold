#
# spec file for package [package-name]
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# Use the base name of the tarball to generate the RPM package name
# Exceptions are glib2 and gtk2 [since these are already available under SLEC]

Name:			[package-name]

# GPL				Applications, Utilities and Data
# LGPL				Libraries
# There may be exceptions, so best to check tarball/COPYING file

License:		[package-license]

# System/Libraries		non GNOME specific libraries eg. gtk2, glib2, vte
# System/Libraries/GNOME	GNOME specific libraries
# Development/Libraries		non GNOME specific devel libraries eg. gtk2-devel, glib2-devel, vte-devel
# Development/Libraries/GNOME   GNOME specific 
# System/GUI			non GNOME specific user interface components
# System/GUI/GNOME		GNOME specific user interface components
# There will be exceptions, so use your own judgement eg. intltool, scrollkeeper

Group:			[package-group]

# Include only if the component doesn't contain any architecture dependant files eg. gnome-icon-theme

BuildArchitectures:	[noarch]

# The version from the tarball. If updating the spec file for a new tarball version, reset the Release number to 1

Version:		[package-version]

# Any time you modify the spec file, you need to increment the Release number. New tarball versions should start with
# the Release number to 1

Release:		[package-release]

# Standard values. Do not change.
Distribution:		Java Desktop System, Release 3

Vendor:			Sun Microsystems, Inc.

# Should be terse, yet descriptive eg. GNOME Terminal, GNOME Window Manager, Print Library for GNOME, GNOME Component
# Library

Summary:		[package-summary]

# Should represent the location of the bzip2 tarball on ftp.gnome.org 
# eg. http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.2/%{name}-%{version}.tar.bz2
# If further sources are to be added, then should have a SourceN: format, where N = 1, 2, 3 ...

Source:			[package-source]

# Should represent the component project URL
# eg. http://www.gnome.org for GNOME components

URL:			[project-url]

# Standard value. You should not need to change this.

BuildRoot:		%{_tmppath}/%{name}-%{version}-build

# Any files flagged with %doc in the %files directive get installed here. Need to decide if we should use this
# for GNOME components or not. README, COPYING, ChangeLog, NEWS are usually typical examples are files being
# flagged. Until that decision is made, do not change this.

Docdir:			%{_defaultdocdir}/doc

# Should represent any patches applied to the original source tarball, where the format is PatchN, N = 1, 2, 3, ...
# Do not add if there are no patches.

Patch1:			[package-patch]

# Standard value. Do not change.

Autoreqprov:		on

# You generally use %defines for tracking Requires and BuildRequires. If you need to add more %defines, then you'd
# better have a good reason. Use '_' where neccessary rather than '-'
# eg. %define libgnomeui_version 2.2.1

%define			[package_define]	[package_definition]

# When you need to track runtime dependancies, Requires, use the rule -
#	o Find the list of packages the application/library links against
#       o Find the Highest Common Factors
# We have been using 'jhbuild dot package' to do this. This also applies for buildtime dependancies,
# BuildRequires. There doesn't seem to be a 'correct' solution, so you may have to use your own 
# judgement here - avoid listing dozens of dependancies.
#
# eg. libgnomeui
# Requires:		libbonoboui	  >= %{libbonoboui_version}
# Requires:		libglade	  >= %{libglade_version}
# BuildRequires:	libbonoboui-devel >= %{libbonoboui_version}
# BuildRequires:	libglade-devel    >= %{libglade_version}
# BuildRequires:	popt		  >= %{popt_version}
# BuildRequires:	gtk-doc		  >= %{gtk_doc_version}
#

Requires:		[package_required]	 >= [package_required_version]
BuildRequires:		[package_build_required] >= [package_required_version]

# Include a paragraph for the description. Be as concise as possible. Do not list authors names or email addresses

%description
[package_description]

# If your package provides a development package use a terse Summary eg. VTE Terminal Emulation Development Library
# The Group should follow the guidelines as above.
# Requires should mention the base package, plus any other required headers, right down to glib2. Make sure that you
# don't add duplicated requirements eg. gtk2-devel requires glib2, libgnome-devl requires gtk2 but *not* glib2
# The description should follow the guidelines as above

%package devel
Summary:		[package_summary]
Group:			[package_group]
Requires:		%{name} = %{version}
Requires:		[package_required] >= [package_required_version]

%description devel
[package_devel_description]

# Standard values. You should not need to change, unless you have good reason eg. the package name is different from
# the tarball name.

%prep
%setup -q

# Include only if you have patches to apply. All patches should be 'p1'. N can be values of 1, 2, 3, ...

%patchN -p1

# Standard value. Do not change unless neccessary.
# If package contains man pages, add --mandir=%{_mandir}.
# If package contains libexec binaries, add --libexec=%{_libexecdir}
# If package has specific options, please include
#
# If package contains gconf schemas, it will be neccessary to disable them until the post-install phase. You
# can do this by the following -
# export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
# make DESTDIR=$RPM_BUILD_ROOT
# unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%build
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# Include only if package needs some special steps taken eg.
#
#	scrollkeeper-update -q			package installs scrollkeeper 'omf' files
#						package removes scrollkeeper 'omf' files
#
#	/sbin/ldconfig				package contains libraries
#						package removes libraries
#
#						package installs gconf schemas
#	export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
#	SCHEMAS="package.schemas"
#	for S in $SCHEMAS; do
#		gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S > /dev/null
#	done

%post
[package_post_install_steps]

%postun
[package_post_uninstall_steps]

# Should list the files to be packaged into the RPM.
# Do not change the 'defattr'.
# The base RPM should include binaries, libraries [.so.* only], man pages and other data files.
# The devel RPM should include binaries, libraries [.so only], pkgconfig files, developer 
# documentation, but should not duplicate anything that has been already packaged into the base RPM.
# Static libs should not be included in any package unless absolutely necessary.
# In that case, include them in the -devel pkg.
# Libtool's .la files should not be included in any package.
#
# Avoid using %{_prefix} and stick to the following macros
#	{_bindir}		/usr/bin
#	{_libdir}		/usr/lib
#	{_libexecdir}		/usr/libexec
#	{_mandir}		/usr/share/man
#	{_datadir}		/usr/share
#	{_sysconfdir}		/etc		[note, you need to specify this at the %build stage]
#	{_includedir}		/usr/include
#
# Use globs where possible eg. %{_bindir}/*
#
# Do not include directives %doc, %config, %docdir, %verify until we figure out a standard for these.

%files
%defattr(-,root,root)
[package_files]

# Include only if there is a devel package.

%files devel
%defattr(-,root,root)
[package_devel_files]

# Include a changelog entry with correct format eg. * Mon May 26 2004 - email@sun.com

%changelog
* [package_changelog_date_author]
- [package_changelog_entry]
