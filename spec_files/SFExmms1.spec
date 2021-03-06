#
# spec file for package SFExmms2
#
# includes module(s): xmms2
#

%include Solaris.inc

Name:                    SFExmms1
Summary:                 X Multimedia System
Version:                 1.2.11
Source:                  http://www.xmms.org/files/1.2.x/xmms-%{version}.tar.bz2
Source1:                 xmms.desktop

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWGtku
Requires: SUNWGtkr
Requires: SUNWgnome-audio
BuildRequires: SUNWsfwhea
BuildRequires: SFEmpg321
BuildRequires: SUNWgnome-audio-devel
BuildRequires: oss

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWsfwhea
Requires: oss

%package encumbered
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEmpg321

%prep
%setup -q -n xmms-%{version}

%build
export CFLAGS="%optflags -I/usr/X11/include -I/usr/gnu/include -I/usr/gnu/include/sasl -I/usr/sfw/include -D__C99FEATURES__ -D__EXTENSIONS__ -DINSTALLPREFIX=\\\"%{_prefix}\\\""
export LDFLAGS="-Wl,-z -Wl,textoff -L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -lc -lsocket -lnsl -lgdk"

./configure -prefix %{_prefix} \
           --mandir %{_mandir} \
           --sysconfdir %{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no \
           --with-pic \
           --with-extra-includes="/usr/X11/include:/usr/gnu/include:/usr/gnu/include/sasl:/usr/sfw/include:usr/include/pcre"

cat libtool | sed 's/\-shared/\-G/' > libtool.new
cp libtool.new libtool

cat libxmms/libtool | sed 's/\-shared/\-G/' > libxmms/libtool.new
cp libxmms/libtool.new libxmms/libtool

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

# Generate libraries list since we have to separate
# out a few encumbered files.
#
echo "%defattr (-, root, bin)" > %{_builddir}/xmms-%version/xmms_libfiles
echo "%dir %attr (0755, root, bin) %{_libdir}" >> %{_builddir}/xmms-%version/xmms_libfiles
(cd ${RPM_BUILD_ROOT}; find ./%{_libdir}/* \( -type f -o -type l \) | \
    egrep -v "mpg|mpeg" | sed 's/^\.\///' \
    >> %{_builddir}/xmms-%version/xmms_libfiles)

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications

%clean
rm -rf $RPM_BUILD_ROOT

%files -f xmms_libfiles
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xmms
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*
%{_datadir}/aclocal

%files devel
%defattr (-, root, bin)
%{_includedir}

%files encumbered
%defattr (-, root, bin)
%{_libdir}/xmms/Input/libmpg*

%changelog
* Sun Feb 24 2008 - moinakg@gmail.com
- Add desktop entry.
- Fix link flag to avoid -ztext failure when building with Gcc.
* Sun Jan 20 2008 - moinakg@gmail.com
- Initial spec.
