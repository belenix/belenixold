#
# spec file for package SFEpstoedit
#
# includes module(s): pstoedit
#

%include Solaris.inc
%include base.inc


Name:         SFEpstoedit
Summary:      Translates PostScript and PDF graphics into other vector formats
Group:        Applications/Productivity
Version:      3.45
License:      GPLv2+
BuildRoot:    %{_tmppath}/pstoedit-%{version}-build
Source:       http://download.sourceforge.net/pstoedit/pstoedit-%{version}.tar.gz
Patch1:       pstoedit-01-cxxflags.diff
Patch2:       pstoedit-02-quiet.diff
Patch3:       pstoedit-03-gcc4.diff
Patch4:       pstoedit-04-asy.diff
Patch5:       pstoedit-05-elif.diff
Patch6:       pstoedit-06-build.diff

URL:          http://www.pstoedit.net/
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:      SUNWghostscriptu
Requires:      SUNWgd2
Requires:      SUNWpng
Requires:      SUNWesu
Requires:      SFElibEMF
Requires:      SFEplotutils
BuildRequires: SUNWgd2
BuildRequires: SUNWpng-devel
BuildRequires: SFElibEMF-devel
BuildRequires: SFEplotutils-devel

%description
Pstoedit converts PostScript and PDF files to various vector graphic
formats. The resulting files can be edited or imported into various
drawing packages. Pstoedit comes with a large set of integrated format
drivers.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWghostscriptu
Requires: SUNWgd2
Requires: SUNWpng-devel
Requires: SFElibEMF-devel
Requires: SFEplotutils-devel

%prep
%setup -q -c -n %name-%version
cd pstoedit-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
cd ..

%build
cd pstoedit-%{version}
export CPPFLAGS="-I%{_includedir}/gd2"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
        ./configure                     \
                --prefix=%{_prefix}     \
                --infodir=%{_datadir}/info \
                --mandir=%{_mandir}     \
                --libdir=%{_libdir}     \
                --disable-static        \
                --with-emf              \
                --without-swf
make
cd ..

%install
rm -rf $RPM_BUILD_ROOT
cd pstoedit-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/pstoedit
%{_libdir}/pstoedit/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/pstoedit
%{_datadir}/pstoedit/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Sat Sep 26 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
