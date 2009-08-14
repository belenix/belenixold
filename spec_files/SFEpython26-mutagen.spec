#
# spec file for package SFEpython26-mutagen
#
# includes module(s): mutagen
#
%include Solaris.inc
%include base.inc

%define python_version 2.6

Name:			SFEpython26-mutagen
Summary:		Mutagen is a Python module to handle audio metadata
License:		GPLv2
Version:		1.16
Source:			http://mutagen.googlecode.com/files/mutagen-%{version}.tar.gz
URL:			http://code.google.com/p/mutagen
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
SUNW_Copyright:         %{name}.copyright
%include default-depend.inc
Requires: SUNWPython26
BuildRequires: SUNWPython26-devel

%description
Mutagen is a Python module to handle audio metadata. It supports
reading ID3 (all versions), APEv2, FLAC, and Ogg Vorbis/FLAC/Theora.
It can write ID3v1.1, ID3v2.4, APEv2, FLAC, and Ogg Vorbis/FLAC/Theora
comments. It can also read MPEG audio and Xing headers, FLAC stream
info blocks, and Ogg Vorbis/FLAC/Theora stream headers. Finally, it
includes a module to handle generic Ogg bitstreams.

%prep
%setup -q -c -n %name-%version

%build
cd mutagen-%{version}
export PYTHON="/usr/bin/python%{python_version}"
${PYTHON} setup.py build
cd ..


%install
rm -rf $RPM_BUILD_ROOT
cd mutagen-%{version}
export PYTHON="/usr/bin/python%{python_version}"

${PYTHON} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
mv  ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages  \
    ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*

%changelog
* Fri Aug 14 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
