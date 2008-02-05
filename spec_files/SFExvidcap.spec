#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define dir_vers 1.1.6
%define sunw_gnu_iconv %(pkginfo -q SUNWgnu-libiconv && echo 1 || echo 0)

Name:                SFExvidcap
Summary:             Personal Imformation Management tool from official KDE release
Version:             1.1.7rc1
Source:              http://jaist.dl.sourceforge.net/sourceforge/xvidcap/xvidcap-%{version}.tar.gz
Patch1:              xvidcap-01-makefile.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWlibtheora
BuildRequires: SUNWlibtheora-devel
#Requires: SFEffmpeg
#BuildRequires: SFEffmpeg-devel
Requires: SFEfaad2
BuildRequires: SFEfaad2-devel
Requires: SFElame
BuildRequires: SFElame-devel

%if %sunw_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SFElibiconv
BuildRequires: SFElibiconv-devel
Requires: SFEgettext
BuildRequires: SFEgettext-devel
%endif


%prep
%setup -q -n xvidcap-%dir_vers
%patch1 -p1

%build
if [ "x`basename $CC`" != xgcc ]
then
        %error This spec file requires Gcc, set the CC and CXX env variables
fi

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -D__C99FEATURES__ -D__EXTENSIONS__"

export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -D__C99FEATURES__ -D__EXTENSIONS__"

export LDFLAGS="%_ldflags %{xorg_lib_path} %{gnu_lib_path} -liconv -lintl %{sfw_lib_path} -lc -lsocket -lnsl"

export PATH="${PATH}:/usr/openwin/bin"
extra_inc="%{xorg_inc}:%{gnu_inc}:%{sfw_inc}"

./configure --prefix=%{_prefix} \
           --sysconfdir=%{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --enable-final \
           --with-extra-includes="${extra_inc}" \
           --enable-libtheora \
           --without-forced-embedded-ffmpeg \
           --enable-libmp3lame



make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# KDE requires the .la files

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/omf
%{_datadir}/omf/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%{_datadir}/dbus-1/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/xvidcap
%{_datadir}/xvidcap/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Thu Jan 24 2008 - moinak.ghosh@sun.com
- Use perl-depend definitions
- Use predefined macros instead of hardcoding pathnames
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Initial spec.
