#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEzsvcadm
License:             CDDL
Summary:             A Zenity based GUI for vieweing SMF services
Version:             0.2
URL:                 http://blogs.sun.com/darren/entry/i_recently_saw_a_libcurses
Source:              zsvcadm.sh
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWgnome-base-libs
BuildRequires:       SUNWgnome-base-libs-devel

%prep
rm -rf zsvcadm-${version}
mkdir zsvcadm-${version}

%build
exe=`basename %{SOURCE}`
cp %{SOURCE} zsvcadm-${version}
cp zsvcadm-${version}/${exe} zsvcadm-${version}/zsvcadm

%install
mkdir -p ${RPM_BUILD_ROOT}/%{_basedir}/bin
cp zsvcadm-${version}/zsvcadm ${RPM_BUILD_ROOT}/%{_basedir}/bin
chmod a+x ${RPM_BUILD_ROOT}/%{_basedir}/bin/zsvcadm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Sun Mar 09 2008 - moinakg@gmail.com
- Initial spec.
