#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                SFEgambas
Summary:             IDE based on a basic interpreter with object extensions
Version:             2.16.0
License:             GPL+
URL:                 http://gambas.sourceforge.net/en/main.html
Source:              %{sf_download}/gambas/gambas-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWglib2
Requires: SUNWxwsvr
Requires: FSWxorg-clientlibs
Requires: SUNWxorg-clientlibs
Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWgnome-desktop-prefs
Requires: SUNWxorg-mesa
Requires: SFEfreeglut
Requires: SUNWgnu-gettext
Requires: SFEgtkglext
Requires: SFElua
BuildRequires: SUNWglib2-devel
BuildRequires: FSWxorg-headers
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWpng-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWgnome-desktop-prefs-devel
BuildRequires: SFEfreeglut-devel
BuildRequires: SUNWgnu-gettext-devel
BuildRequires: SFEgtkglext-devel

%description
Celestia is a real-time space simulation which lets you experience the
universe in three dimensions. Celestia does not confine you to the
surface of the Earth, it allows you to travel throughout the solar
system, to any of over 100,000 stars, or even beyond the galaxy.

Travel in Celestia is seamless; the exponential zoom feature lets
you explore space across a huge range of scales, from galaxy clusters
down to spacecraft only a few meters across. A 'point-and-goto'
interface makes it simple to navigate through the universe to the
object you want to visit.

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd gambas-%version
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd gambas-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
	    --with-gtk

gmake -j$CPUS

cd ..


%install
rm -rf $RPM_BUILD_ROOT
cd gambas-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/gambas
%{_datadir}/gambas/*
%dir %attr(0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr(0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Oct 03 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
