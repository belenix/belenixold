#
# spec file for package SFEaxel
#
%include Solaris.inc

Name:                    SFEaxel
Summary:                 axel - A lightweight and fast download accelerator
Version:                 2.0
Source:			 http://alioth.debian.org/frs/download.php/2605/axel-2.0.tar.gz
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -c -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd axel-%{version}

export CC=${CC32:-$CC}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
	    --etcdir=%{_sysconfdir}             \
	    --mandir=%{_mandir}                 \
	    --strip=0

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

cd axel-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Sat Sep 27 2008 - moinakg@gmail.com
- Initial spec.
