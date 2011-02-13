#### TODO TODO TODO - WORK IN PROGRESS ####

Summary: The eXtensible ARchiver
Name: xar
Version: 1.5.2
Release: 1%{?dist}
License: BSD
Group: Applications/Archiving
URL: http://code.google.com/p/xar/
Source: http://xar.googlecode.com/files/xar-%{version}.tar.gz
Patch0: xar-solaris-acl.patch
Patch1: xar-1.5.2-CVE-2010-0055.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libxml2-devel
#BuildRequires: openssl-devel
BuildRequires: zlib-devel
#BuildRequires: bzip2-devel
#BuildRequires: /usr/bin/awk

%description
The XAR project aims to provide an easily extensible archive format. Important
design decisions include an easily extensible XML table of contents for random
access to archived files, storing the toc at the beginning of the archive to
allow for efficient handling of streamed archives, the ability to handle files
of arbitrarily large sizes, the ability to choose independent encodings for
individual files in the archive, the ability to store checksums for individual
files in both compressed and uncompressed form, and the ability to query the
table of content's rich meta-data.


%package devel
Summary: Development files for the eXtensible ARchiver
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files for the eXtensible ARchiver.


%prep
%bsetup
cd xar-%{version}
%patch0 -p1 -b .xar-solaris-acl
%patch1 -p1 -b .CVE-2010-0055

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

cd xar-%{version}
./configure --prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--enable-shared --disable-static
gmake -j 2

%install
rm -rf ${RPM_BUILD_ROOT}
gmake install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/libxar.la


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,bin)
%doc LICENSE TODO
%{_bindir}/xar
%{_libdir}/libxar.so*
%{_mandir}/man1/xar.1*

%files devel
%defattr(-,root,bin)
%{_includedir}/xar/


%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 28 2010 Matthias Saou <http://freshrpms.net/> 1.5.2-6
- Include patch to fix CVE-2010-0055 (#570678).

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.5.2-5
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> 1.5.2-2
- rebuild with new openssl

* Tue Dec 23 2008 Matthias Saou <http://freshrpms.net/> 1.5.2-1
- Update to 1.5.2.
- Remove no longer needed install and memset patches.
- Disable newly built-by-default static lib and remove useless .la file.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 
- Autorebuild for GCC 4.3

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> 
- Rebuild for deps

* Thu Aug 23 2007 Matthias Saou <http://freshrpms.net/> 1.5.1-4
- Rebuild for new BuildID feature.
- Add /usr/bin/awk build requirement, needed for the libxml configure check.

* Wed Aug  8 2007 Matthias Saou <http://freshrpms.net/> 1.5.1-2
- Patch memset call with swapped arguments (Dave Jones).

* Wed Jul 11 2007 Matthias Saou <http://freshrpms.net/> 1.5.1-1
- Update to 1.5.1.

* Wed May 30 2007 Matthias Saou <http://freshrpms.net/> 1.5-1
- Update to 1.5.
- Include patch to remove rpath.
- Include patch to fix file modes, and get the lib properly stripped.

* Sun Feb 25 2007 Matthias Saou <http://freshrpms.net/> 1.4-1
- Initial RPM release.


