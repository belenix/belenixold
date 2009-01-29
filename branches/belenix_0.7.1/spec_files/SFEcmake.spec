#
# spec file for package SFEcmake
#
# includes module(s): cmake
#
%include Solaris.inc

Name:                    SFEcmake
Summary:                 Cross platform make system
Version:                 2.4.7
Source:                  http://www.cmake.org/files/v2.4/cmake-%{version}.tar.gz
URL:                     http://www.cmake.org
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
%if %cc_is_gcc
Requires:		SUNWgccruntime
%else
Requires:               SUNWlibC
%endif
Requires:               SUNWlibmsr

%prep
%setup -q -n cmake-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

./configure --prefix=%{_prefix} \
	    --bindir=%{_bindir}	\
	    --libdir=%{_libdir}	\
	    --mandir=%{_mandir}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# Whoops how did the manpages get there!!!
(
    cd $RPM_BUILD_ROOT/usr/usr
    find share | cpio -pdm ..
    cd .. && rm -rf usr
    mv doc share
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/cmake-*
%{_mandir}
%defattr (-, root, other)
%{_datadir}/doc

%changelog
* Tue Apr 01 2008 - moinakg@gmail.com
- Enable building using gcc.
* Mon Oct 22 2007 - nonsea@users.sourceforge.net
- Bump to 2.4.7
* Mon Mar 19 2007 - dougs@truemail.co.th
- Initial spec