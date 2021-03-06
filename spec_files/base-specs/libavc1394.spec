#
# spec file for package libavc1394
#
# includes module(s): libavc1394
#

%define src_ver 0.5.3
%define src_name libavc1394
%define src_url http://downloads.sourceforge.net/%{src_name}

Name:		libavc1394
Summary:	Programming interface to the 1394 AV/C specification
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libavc1394-01-wall.diff
Patch2:		libavc1394-02-solaris.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %cc_is_gcc
export CFLAGS="%optflags -std=c99"
%else
export CFLAGS="%optflags -xc99=%all"
%endif
export LDFLAGS="%_ldflags"

libtoolize -f -c
aclocal
autoheader
autoconf -f
automake -a -f

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static

#perl -pi -e 's,-shared,-Wl,-G' libtool
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Fixed links
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial base spec file
