#
# spec file for package SUNWgnome-foo-bar
#
# includes module(s): gnome-foo, libgnomebar
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

############################################################################
# The example in this template builds 2 GNOME components, gnome-foo and
# libgnomebar and packages them together into a Solaris package called
# SUNWgnome-foo-bar that is split by file system boundaries [Solaris rule],
# so it has a "subpackage" called SUNWgnome-foo-bar-root.
# gnome-foo.spec and libgnomebar.spec are the JDS linux spec files for
# the corresponding RPMs.
# 
# See SUNWtemplate-standalone.spec for an example where Linux spec files 
# are not used
############################################################################

%include Solaris.inc
# The Solaris.inc file sets up some defaults: compiler options,
# default locations and extra info needed for building Solaris pkgs.
# See the file itself for more details, it's located in this directory.
# Note that this line should appear before any %use lines so that 
# macros in Solaris.inc are used by the %use'd spec files

%use gfoo = gnome-foo.spec
%use libgnomebar = libgnomebar.spec
# Declare that this spec file will use information (tags, scriptlets, etc.)
# from another spec file or files. Assign a name (gfoo/libgnomebar) to the
# spec file for future reference.
# In this case gnome-foo

Name:                    SUNWgnome-foo-bar
# This is the name (PKG) of the Solaris package.

Summary:                 GNOME foo bar libraries
# This will become the one-line description of the Solaris package

Version:                 %{default_pkg_version}
# This is the version of the Solaris package that has little to do with
# the version of the gnome components included, since several gnome
# components may be packaged together.
# In case of non-GNOME components, however, we prefer to use the
# tarball version number of the component.
# Note: package version numbers must be numeric.  Things like 1.0.5beta
# and v6b are not allowed
#  %{default_pkg_version} is defined in Solaris.inc.

SUNW_BaseDir:            %{_basedir}
# The base directory of the Solaris package (normally /usr, / or
# /opt/<product>)
# You need to define the basedir for each package and subpackage.
# For now, the basedir of "-root" packages should be /, everything
# else it should be %{_basedir} (defined in Solaris.inc)

SUNW_Copyright:          %{name}.copyright
# Use the copyright-extractor script to create a copyright file.

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
# Same as with linux specs. Note that in this case this will be
# /var/tmp/SUNWgnome-foo-bar-2.6.0-build

%include default-depend.inc
# There's a list of packages that all GNOME packages depend on
# These are really just the Solaris core, devices, system libs.
# We could include them in all spec files but it's nicer and shorter
# to %include them from a common file.

Requires: SUNWgnome-base-libs
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWpng
Requires: SUNWTiff
Requires: SUNWjpg
# These are the additional [to the default ones %include'd above]
# dependencies of this package. Please don't use version checks in
# Solaris dependencies. They are not usually used and not properly
# implemented in the build scripts either.
# Try to identify the dependencies of the package the best you can.
# Missing dependencies may cause broken installs, but unnecessary deps
# are a pain too.

BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWsfwhea
# These lines define what package need to be installed at build time.

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
# This defines the "-root" subpackage, i.e. SUNWgnome-foo-bar-root.
# Solaris packages must be split by usual filesystem boundaries, so
# root filesystem (e.g. /etc) files must be separated from the rest of
# the package.  According to Solaris packaging rules, development and
# runtime files must also be separated..
#
# The naming convention used in GNOME is this:
#
## runtime pkgs:
#
# SUNWgnome-package-name:             the main package, binaries, libs,
#                                     files in %{_datadir} needed at runtime
# SUNWgnome-package-name-root:        /etc, /var stuff
#
## development pkgs:
#
# SUNWgnome-package-name-devel:       header files, pkgconfig files,
#                                     binaries only needed for development,
#                                     developer docs, man pages, aclocal
#                                     macros, etc.
# SUNWgnome-package-name-devel-root:  any root files that are only needed
#                                     for development (rarely needed)
#

%if %build_l10n
%package l10n
Summary:                 foo - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
# start with a clean source directory.

%gfoo.prep -d %name-%version
# prepare the sources of gnome-foo in the %name-%version subdir.
# This will run the %prep section in the gfoo (gnome-foo.spec) spec file
# (see %use above).
# It will result in something like SUNWgnome-foo-bar-2.6.0/gnome-foo-x.y/

%libgnomebar.prep -d %name-%version
# The same thing again with libgnomebar.

%build
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"
# Set any environment variables that may be needed.
# Note that the linux spec files usually set CFLAGS to $RPM_OPT_FLAGS
# before running configure, so if you want to add something to the
# CFLAGS defined in the linux spec file, the above trick will do
# (i.e. set RPM_OPT_FLAGS to be the same as the CFLAGS you want)
# ((RPM_OPT_FLAGS is normally defined by rpm as %optflags))

%gfoo.build -d %name-%version
%libgnomebar.build -d %name-%version
# run the %build section of the linux spec files after cd'ing into 
# %name-%version.

%install
# This section installs the files in what ON/SFW folks would call a
# "proto area", which is a directory where files are staged for packaging
# In the case of rpm/pkgbuild, we have a separate proto area for each
# spec file, called $RPM_BUILD_ROOT.
rm -rf $RPM_BUILD_ROOT
# start with a clean proto dir
%gfoo.install -d %name-%version
%libgnomebar.install -d %name-%version

#
# when not building -l10n packages, remove anything l10n related from
# $RPM_BUILD_ROOT
#
%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT
# remove the build root dir once packaging succeeds

%iclass myclass [-f script]
%rclass myclass [-f script]
# use these to define a class and associate installation and removal class
# action scripts.  The script can be inline or in an external file identified
# by "script".  In an external script is used, put it in spec-files/ext-sources

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
# Make sure you define the Solaris default file attributes for system
# directories.
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%class(myclass) %{_libdir}/foo/bar
# This make /usr/lib/foo/bar 'f myclass' type and adds myclass to CLASSES

%files root
%defattr (-, root, sys)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfig}/gconf/schemas/foo.schemas

#
# The files included here should match the ones removed in %install
#
%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Fri Jun  2 2006 - laca@sun.com
- update to remove info about -share pkgs and add some more comments
* Fri Feb 27 2004 - laszlo.peter@sun.com
- add info about %changelog to the template
# Although pkgbuild doesn't currently do anything with %changelog, it's
# still a good idea to use changelog entries.

# To build a Solaris package from this spec file, copy all referenced
# spec files and include files to %topdir/SPECS, copy all sources & patches
# referenced in this or any of the %use'd spec files to %topdir/SOURCES
# and run pkgbuild -ba <this spec file>
# Alternatively, run
#       pkgtool build <spec-file>
# in this directory.
