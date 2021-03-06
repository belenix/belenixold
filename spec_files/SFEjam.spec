#
# spec file for package SFEjam.spec
#
# includes module(s): jam
#
%include Solaris.inc

%define src_name	jam
%define src_url		ftp://ftp.perforce.com/pub/jam

Name:                   SFEjam
Summary:                make-like program
Version:                2.5
Source:                 %{src_url}/%{src_name}-%{version}.tar
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/jam
cp ./bin.solaris/jam $RPM_BUILD_ROOT%{_bindir}
cp README *.html $RPM_BUILD_ROOT%{_datadir}/doc/jam


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/jam

%changelog
* Sun May  6 2007 - dougs@truemail.co.th
- Fixed doc directory
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
