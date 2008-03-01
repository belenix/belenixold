#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:			terminal
Summary:		Xfce terminal
URL:			http://www.xfce.org/
%define src_name	Terminal
Version:		0.2.8
Source0:		%{xfce_src_url}/%{src_name}-%{version}.tar.bz2
Patch1:			xfce-terminal-01-fixheaders.diff
Patch2:         xfce-terminal-02-fixgccism.diff

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

   config=./configure

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lX11"
$config	--prefix=%{_prefix}		\
	--bindir=%{_bindir}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	%{gtk_doc_option}		\
	--enable-debug=no		\
	--disable-static
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Dec 9 2007 - sobotkap@centrum.cz
- Bump to 0.2.8
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Thu Feb  1 2007 - dougs@truemail.co.th
- Initial version
