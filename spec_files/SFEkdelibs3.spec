#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define kde_version 3.5.9

%define SUNWaspell      %(/usr/bin/pkginfo -q SUNWaspell && echo 1 || echo 0)

Name:                SFEkdelibs3
Summary:             Base KDE3 libraries
Version:             %{kde_version}
Source:              http://mirrors.isc.org/pub/kde/stable/%{kde_version}/src/kdelibs-%{version}.tar.bz2

Patch1:              kdelibs-01-doxygen.diff
Patch2:              kdelibs-02-libart.diff
Patch4:              kdelibs-04-kmenuapps.diff
Patch5:              kdelibs-05-kdeinit-wrapper.diff
Patch6:              kdelibs-06-ktimezones.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEgawk
Requires: SFEqt3
BuildRequires: SFEqt3-devel
Requires: SFEarts
BuildRequires: SFEarts-devel
Requires: SUNWgnu-idn
Requires: SUNWzlib
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWgccruntime
Requires: FSWxwpft
Requires: FSWxorg-clientlibs
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2
BuildRequires: FSWxorg-headers
BuildRequires: SFEdoxygen
Requires: SUNWgnu-coreutils
Requires: SFEcups
BuildRequires: SFEcups-devel
Requires: SUNWbzip
Requires: SUNWlxml
BuildRequires: SUNWlxml-devel
Requires: SUNWlxsl
BuildRequires: SUNWlxsl-devel
Requires: SUNWTiff
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWgnome-common-devel
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgamin
BuildRequires: SUNWgamin-devel
Requires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
Requires: SUNWopensslr
Requires: SUNWkrbu
Requires: SUNWpcre
%if %SUNWaspell
Requires: SUNWaspell
BuildRequires: SUNWaspell-devel
%else
Requires: SFEaspell
BuildRequires: SFEaspell-devel
%endif
Requires: SFEopenexr
BuildRequires: SFEopenexr-devel
BuildRequires: oss
Requires: %{name}-root

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEqt3-devel
Requires: SFEarts-devel
Requires: SUNWpng-devel
Requires: SUNWjpg-devel
Requires: SFEdoxygen
Requires: SFEcups-devel
Requires: SUNWlxml-devel
Requires: SUNWlxsl-devel
Requires: SUNWTiff-devel
Requires: SUNWgnome-common-devel
Requires: SUNWgnome-base-libs-devel
Requires: SUNWgamin-devel
Requires: SUNWopenssl-include
%if %SUNWaspell
Requires: SUNWaspell-devel
%else
Requires: SFEaspell-devel
%endif
Requires: SFEopenexr-devel
Requires: oss

%prep
%setup -q -n kdelibs-%version
%patch1 -p1
%patch2 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

if [ "x`basename $CC`" != xgcc ]
then
	%error This spec file requires Gcc, set the CC and CXX env variables
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -I/usr/include/pcre `/usr/bin/libart2-config --cflags` -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%_ldflags %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path} -lc -lsocket -lnsl `/usr/bin/libart2-config --libs` -lartsflow -lartsflow_idl"

export QTDOCDIR=%{_datadir}/qt3/doc/html
extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}:/usr/include/pcre"
sfw_prefix=`dirname %{sfw_bin}`

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-ssl-dir="${sfw_prefix}" \
           --with-extra-includes="${extra_inc}" \
           --with-gssapi=no \
           --disable-debug


make -j$CPUS
make -j$CPUS apidox

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# KDE requires the .la and the .a files

# Rename to avoid conflict with Gnome's applications.menu
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/menus/applications.menu \
   ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/menus/kapplications.menu

rm -f ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/index.theme

# Generate binfiles list since we have to specify
# setuid perms for three files.
#
(cd ${RPM_BUILD_ROOT}; find ./%{_bindir}/* | \
    egrep -v "fileshareset|kgrantpty|kpac_dhcp_helper" | sed 's/^\.\///' \
    > %{_builddir}/kdelibs-%version/klibs_binfiles)

%clean
rm -rf $RPM_BUILD_ROOT

%files -f klibs_binfiles
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (4755, root, bin) %{_bindir}/fileshareset
%attr (4755, root, bin) %{_bindir}/kgrantpty
%attr (4755, root, bin) %{_bindir}/kpac_dhcp_helper
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.la*
%dir %attr (0755, root, other) %{_libdir}/kde3
%{_libdir}/kde3/*

%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/apps
%{_datadir}/apps/*
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/*
%dir %attr (0755, root, other) %{_datadir}/services
%{_datadir}/services/*
%dir %attr (0755, root, other) %{_datadir}/servicetypes
%{_datadir}/servicetypes/*
%dir %attr (0755, root, other) %{_datadir}/mimelnk
%{_datadir}/mimelnk/*
%dir %attr (0755, root, other) %{_datadir}/emoticons
%{_datadir}/emoticons/*
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.a
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sat Jun 14 2008 - moinakg@gmail.com
- Bump to KDE 3.5.9
- Remove upstream patch.
* Tue Mar 18 2008 - moinakg@gmail.com
- Add missing dependency on root package.
- Update LDFLAGS.
* Sun Feb 24 2008 - moinakg@gmail.com
- Fix aspell dependency.
- Use gamin instead of FAM.
* Fri Feb 01 2008 - moinakg@gmail.com
- Add patch to fix timezone handing on Solaris.
* Thu Jan 24 2008 - moinakg@gmail.com
- Set QTDOCDIR to satisfy internal doxygen script.
- Use predefined macros instead of hardcoding pathnames.
* Tue Jan 22 2008 - moinakg@gmail.com
- Fixed typo in configure options.
* Sun Jan 20 2008 - moinakg@gmail.com
- Add dependencies to devel package. Added oss dependency.
* Sat Jan 19 2008 - moinakg@gmail.com
- Fix some startkde/kdeinit nits, disable debug to avoid filling up log file.
* Wed Jan 16 2008 - moinakg@gmail.com
- Get rid of custom kde3-prefixed datadir and includedir. Unsettles KDE3.
- Handle setting setuid attributes for non-root builds.
* Tue Jan 12 2008 - moinakg@gmail.com
- Initial spec.
