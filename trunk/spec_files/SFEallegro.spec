#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEallegro
Summary:             Game programming library
Version:             4.2.2
Group:               System Environment/Libraries
License:             Giftware
URL:                 http://alleg.sourceforge.net/
Source:              %{sf_download}/alleg/allegro-%{version}.tar.gz
Patch1:              allegro-01-cfg.diff
Patch2:              allegro-02-nostrip.diff
Patch3:              allegro-03-multilib.diff
Patch4:              allegro-04-noexecmod.diff
Patch5:              allegro-05-libdir.diff
Patch6:              allegro-06-fullscreen-viewport.diff

SUNW_BaseDir:        /
SUNW_Copyright:      %{name}.copyright
Group:               Games
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-audio
BuildRequires: SUNWgnome-audio-devel
Requires: SUNWxwplt
Requires: SFEgccruntime
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWzip


%description
Allegro is a cross-platform library intended for use in computer games
and other types of multimedia programming. 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SUNWxorg-headers
Requires: SUNWbash
Requires: SFEgcc
Requires: SUNWgnome-audio-devel

%description devel
Allegro is a cross-platform library intended for use in computer games
and other types of multimedia programming. This package is needed to
build programs written with Allegro. 

%prep
%setup -q -c -n %name-%version
cd allegro-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr allegro-%{version} allegro-%{version}-64
%endif

%build
%ifarch amd64 sparcv9
cd allegro-%{version}-64
# This source is gcc-centric, therefore...
export CC=%{gnu_bin}/gcc
export CFLAGS="-m64 -fPIC -DPIC -I/usr/X11/include"
export CXXFLAGS="-m64 -fPIC -DPIC -I/usr/X11/include"
export LDFLAGS="%{_ldflags64} %{gnu_lib_path64}"
export allegro_cv_processor_type=%{_arch64}

# The following on-the-fly patch is applied because this source's makefile
# uses syntax that works with bash(1) but not sh(1); yet makefile.in
# hardcodes SHELL = /bin/sh (and likely gets away with it because /bin/sh
# on some (all?) Linux systems is symlink'd to /bin/bash.)
# TODO: Report this upstream

perl -i.orig -lpe 's/^(SHELL = \/bin\/sh).*/#$1/ and print "SHELL = /bin/bash"' makefile.in

./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --mandir=%{_mandir}
# GRRR configure insists on adding -fomit-frame-pointer, remove it 
%{gnu_bin}/sed -i 's/-fomit-frame-pointer//g' makefile

# Fix for 64Bit
%{gnu_bin}/sed -i 's/CXXFLAGS =/CXXFLAGS = -m64/g' makefile

gmake
cd ..
%endif

cd allegro-%{version}
# This source is gcc-centric, therefore...
# export CFLAGS="%optflags"
export CFLAGS="-fPIC -DPIC -I/usr/X11/include"
export LDFLAGS="%{_ldflags} %{gnu_lib_path}"
unset allegro_cv_processor_type

# The following on-the-fly patch is applied because this source's makefile
# uses syntax that works with bash(1) but not sh(1); yet makefile.in
# hardcodes SHELL = /bin/sh (and likely gets away with it because /bin/sh
# on some (all?) Linux systems is symlink'd to /bin/bash.)
# TODO: Report this upstream

perl -i.orig -lpe 's/^(SHELL = \/bin\/sh).*/#$1/ and print "SHELL = /bin/bash"' makefile.in

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

gmake
cd ..

%install
rm -rf $RPM_BUILD_ROOT
PDIR=`pwd`
%ifarch amd64 sparcv9
cd allegro-%{version}-64
make install     DESTDIR=$RPM_BUILD_ROOT
make install-man DESTDIR=$RPM_BUILD_ROOT
ginstall -m 755 docs/makedoc $RPM_BUILD_ROOT%{_bindir}/allegro-makedoc
ginstall -Dpm 644 allegro.cfg $RPM_BUILD_ROOT%{_sysconfdir}/allegrorc
ginstall -dm 755 $RPM_BUILD_ROOT%{_datadir}/allegro

mkdir -p $RPM_BUILD_ROOT%{_std_includedir}
cd $RPM_BUILD_ROOT%{_std_includedir}
ln -s ../gnu/include/allegro.h .
ln -s ../gnu/include/allegro .

mkdir -p $RPM_BUILD_ROOT%{_std_bindir}/%{_arch64}
CONFLICTING_COMMANDS="
    :pack:
"

cd $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
for f in *; do
    # don't symlink conflicting commands to /usr/bin
    echo $CONFLICTING_COMMANDS | grep ":${f}:" > /dev/null && continue
    ( cd $RPM_BUILD_ROOT%{_std_bindir}/%{_arch64}; ln -s ../../gnu/bin/%{_arch64}/$f . )
done

mkdir -p $RPM_BUILD_ROOT%{_std_libdir}/%{_arch64}
cd $RPM_BUILD_ROOT%{_std_libdir}/%{_arch64}
ln -s ../../gnu/lib/%{_arch64}/liballeg* .

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/liball{p,d}_unsharable.a
cd ..
%endif

cd ${PDIR}/allegro-%{version}
make install     DESTDIR=$RPM_BUILD_ROOT
ginstall -m 755 docs/makedoc $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/allegro-makedoc

mkdir -p $RPM_BUILD_ROOT%{_std_bindir}
CONFLICTING_COMMANDS="
    :pack:
"

cd $RPM_BUILD_ROOT%{_bindir}
for f in *; do
    # don't symlink conflicting commands to /usr/bin
    echo $CONFLICTING_COMMANDS | grep ":${f}:" > /dev/null && continue
    ( cd $RPM_BUILD_ROOT%{_std_bindir}; ln -s ../gnu/bin/$f . )
done

mkdir -p $RPM_BUILD_ROOT%{_std_libdir}
cd $RPM_BUILD_ROOT%{_std_libdir}
ln -s ../gnu/lib/liballeg* .
chmod 755 `find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.so"`
rm -f $RPM_BUILD_ROOT%{_libdir}/liball{p,d}_unsharable.a
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_std_bindir}
%{_std_bindir}/*
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_std_libdir}
%{_std_libdir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%attr (0644, root, bin) %{_sysconfdir}/allegrorc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_std_includedir}
%{_std_includedir}/*.h
%{_std_includedir}/allegro
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%{_includedir}/allegro
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/allegro
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sat Nov 21 2009 - Moinak Ghosh
- Initial spec
