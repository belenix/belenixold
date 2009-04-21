%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                   SFEicu4c
Summary:                International Components for Unicode
Version:                3.6
%define src_ver         3_6
Source:                 ftp://ftp.software.ibm.com/software/globalization/icu/3.6/icu4c-%{src_ver}-src.tgz
URL:                    http://www.icu-project.org/
Patch0:                 icu4c-mh-solaris.0.diff
Patch1:                 icu4c-cbiditst.h.1.diff
Patch2:                 icu4c-cbididat.c.2.diff
Patch3:                 icu4c-dllmode.c.3.diff
Patch4:                 icu4c-make.c.4.diff
Patch5:                 icu4c-runConfigureICU.5.diff
Patch6:                 icu4c-configure_gcc64.6.diff

SUNW_Copyright:         BSD.icu
SUNW_BaseDir:           %{_basedir}

%include default-depend.inc
BuildRequires:		SFEgcc
Requires:		SFEgccruntime

%prep
%setup -q -n %name-%version -c 
cd icu
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# Fix elif without expression
cd source
[ ! -f layoutex/ParagraphLayout.cpp.orig ] && cp layoutex/ParagraphLayout.cpp layoutex/ParagraphLayout.cpp.orig
cat layoutex/ParagraphLayout.cpp | sed 's/^#elif$/#else/' > layoutex/ParagraphLayout.cpp.new
cp layoutex/ParagraphLayout.cpp.new layoutex/ParagraphLayout.cpp

cd ../..

%ifarch amd64 sparcv9
cp -pr icu icu-64
%endif

%build
%ifarch amd64 sparcv9
cd icu-64/source

export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags -m64 -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"
export CXXFLAGS="%cxx_optflags64"

chmod 0755 ./runConfigureICU

./runConfigureICU Solaris/GCC \
    --prefix=%{_prefix} \
    --bindir=%{_bindir}/%{_arch64} \
    --sbindir=%{_sbindir}/%{_arch64} \
    --libdir=%{_libdir}/%{_arch64} \
    --mandir=%{_mandir} \
    --disable-warnings --disable-debug --disable-dependency-tracking \
    --enable-shared --disable-static \
    --disable-strict \
    --enable-64bit-libs \
    --enable-release --enable-draft --disable-renaming \
    --enable-rpath --enable-threads --enable-extras \
    --enable-icuio --enable-layout --enable-tests --enable-samples

make
cd ../..
%endif

cd icu/source

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export CXXFLAGS="%cxx_optflags"

chmod 0755 ./runConfigureICU

./runConfigureICU Solaris/GCC \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --disable-warnings --disable-debug --disable-dependency-tracking \
    --enable-shared --disable-static \
    --disable-strict \
    --disable-64bit-libs \
    --enable-release --enable-draft --disable-renaming \
    --enable-rpath --enable-threads --enable-extras \
    --enable-icuio --enable-layout --enable-tests --enable-samples

make

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd icu-64/source
make install DESTDIR=$RPM_BUILD_ROOT
cd ../..
%endif

cd icu/source
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/derb
%{_bindir}/genbrk
%{_bindir}/gencnval
%{_bindir}/genctd
%{_bindir}/genrb
%{_bindir}/icu-config
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/icu/3.6/config/mh-solaris-gcc
%{_datadir}/icu/3.6/license.html
%{_datadir}/icu/3.6/mkinstalldirs
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/layout/LEFontInstance.h
%{_includedir}/layout/LEGlyphFilter.h
%{_includedir}/layout/LEGlyphStorage.h
%{_includedir}/layout/LEInsertionList.h
%{_includedir}/layout/LELanguages.h
%{_includedir}/layout/LEScripts.h
%{_includedir}/layout/LESwaps.h
%{_includedir}/layout/LETypes.h
%{_includedir}/layout/LayoutEngine.h
%{_includedir}/layout/ParagraphLayout.h
%{_includedir}/layout/RunArrays.h
%{_includedir}/unicode/brkiter.h
%{_includedir}/unicode/calendar.h
%{_includedir}/unicode/caniter.h
%{_includedir}/unicode/chariter.h
%{_includedir}/unicode/choicfmt.h
%{_includedir}/unicode/coleitr.h
%{_includedir}/unicode/coll.h
%{_includedir}/unicode/curramt.h
%{_includedir}/unicode/currunit.h
%{_includedir}/unicode/datefmt.h
%{_includedir}/unicode/dbbi.h
%{_includedir}/unicode/dcfmtsym.h
%{_includedir}/unicode/decimfmt.h
%{_includedir}/unicode/docmain.h
%{_includedir}/unicode/dtfmtsym.h
%{_includedir}/unicode/fieldpos.h
%{_includedir}/unicode/fmtable.h
%{_includedir}/unicode/format.h
%{_includedir}/unicode/gregocal.h
%{_includedir}/unicode/locid.h
%{_includedir}/unicode/measfmt.h
%{_includedir}/unicode/measunit.h
%{_includedir}/unicode/measure.h
%{_includedir}/unicode/msgfmt.h
%{_includedir}/unicode/normlzr.h
%{_includedir}/unicode/numfmt.h
%{_includedir}/unicode/parseerr.h
%{_includedir}/unicode/parsepos.h
%{_includedir}/unicode/platform.h
%{_includedir}/unicode/ppalmos.h
%{_includedir}/unicode/putil.h
%{_includedir}/unicode/pwin32.h
%{_includedir}/unicode/rbbi.h
%{_includedir}/unicode/rbnf.h
%{_includedir}/unicode/regex.h
%{_includedir}/unicode/rep.h
%{_includedir}/unicode/resbund.h
%{_includedir}/unicode/schriter.h
%{_includedir}/unicode/search.h
%{_includedir}/unicode/simpletz.h
%{_includedir}/unicode/smpdtfmt.h
%{_includedir}/unicode/sortkey.h
%{_includedir}/unicode/strenum.h
%{_includedir}/unicode/stsearch.h
%{_includedir}/unicode/symtable.h
%{_includedir}/unicode/tblcoll.h
%{_includedir}/unicode/timezone.h
%{_includedir}/unicode/translit.h
%{_includedir}/unicode/ubidi.h
%{_includedir}/unicode/ubrk.h
%{_includedir}/unicode/ucal.h
%{_includedir}/unicode/ucasemap.h
%{_includedir}/unicode/ucat.h
%{_includedir}/unicode/uchar.h
%{_includedir}/unicode/uchriter.h
%{_includedir}/unicode/uclean.h
%{_includedir}/unicode/ucnv.h
%{_includedir}/unicode/ucnv_cb.h
%{_includedir}/unicode/ucnv_err.h
%{_includedir}/unicode/ucol.h
%{_includedir}/unicode/ucoleitr.h
%{_includedir}/unicode/uconfig.h
%{_includedir}/unicode/ucsdet.h
%{_includedir}/unicode/ucurr.h
%{_includedir}/unicode/udat.h
%{_includedir}/unicode/udata.h
%{_includedir}/unicode/udeprctd.h
%{_includedir}/unicode/udraft.h
%{_includedir}/unicode/uenum.h
%{_includedir}/unicode/uidna.h
%{_includedir}/unicode/uintrnal.h
%{_includedir}/unicode/uiter.h
%{_includedir}/unicode/uloc.h
%{_includedir}/unicode/ulocdata.h
%{_includedir}/unicode/umachine.h
%{_includedir}/unicode/umisc.h
%{_includedir}/unicode/umsg.h
%{_includedir}/unicode/unifilt.h
%{_includedir}/unicode/unifunct.h
%{_includedir}/unicode/unimatch.h
%{_includedir}/unicode/unirepl.h
%{_includedir}/unicode/uniset.h
%{_includedir}/unicode/unistr.h
%{_includedir}/unicode/unorm.h
%{_includedir}/unicode/unum.h
%{_includedir}/unicode/uobject.h
%{_includedir}/unicode/uobslete.h
%{_includedir}/unicode/uregex.h
%{_includedir}/unicode/urename.h
%{_includedir}/unicode/urep.h
%{_includedir}/unicode/ures.h
%{_includedir}/unicode/uscript.h
%{_includedir}/unicode/usearch.h
%{_includedir}/unicode/uset.h
%{_includedir}/unicode/usetiter.h
%{_includedir}/unicode/ushape.h
%{_includedir}/unicode/usprep.h
%{_includedir}/unicode/ustdio.h
%{_includedir}/unicode/ustream.h
%{_includedir}/unicode/ustring.h
%{_includedir}/unicode/usystem.h
%{_includedir}/unicode/utext.h
%{_includedir}/unicode/utf.h
%{_includedir}/unicode/utf16.h
%{_includedir}/unicode/utf32.h
%{_includedir}/unicode/utf8.h
%{_includedir}/unicode/utf_old.h
%{_includedir}/unicode/utmscale.h
%{_includedir}/unicode/utrace.h
%{_includedir}/unicode/utrans.h
%{_includedir}/unicode/utypes.h
%{_includedir}/unicode/uversion.h
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/icu/3.6/Makefile.inc
%{_libdir}/icu/Makefile.inc
%{_libdir}/icu/current
%{_libdir}/libicudata.so
%{_libdir}/libicudata.so.36
%{_libdir}/libicudata.so.36.0
%{_libdir}/libicui18n.so
%{_libdir}/libicui18n.so.36
%{_libdir}/libicui18n.so.36.0
%{_libdir}/libicuio.so
%{_libdir}/libicuio.so.36
%{_libdir}/libicuio.so.36.0
%{_libdir}/libicule.so
%{_libdir}/libicule.so.36
%{_libdir}/libicule.so.36.0
%{_libdir}/libiculx.so
%{_libdir}/libiculx.so.36
%{_libdir}/libiculx.so.36.0
%{_libdir}/libicutu.so
%{_libdir}/libicutu.so.36
%{_libdir}/libicutu.so.36.0
%{_libdir}/libicuuc.so
%{_libdir}/libicuuc.so.36
%{_libdir}/libicuuc.so.36.0
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man1/derb.1
%{_mandir}/man1/genbrk.1
%{_mandir}/man1/gencnval.1
%{_mandir}/man1/genctd.1
%{_mandir}/man1/genrb.1
%{_mandir}/man1/icu-config.1
%{_mandir}/man1/makeconv.1
%{_mandir}/man1/pkgdata.1
%{_mandir}/man1/uconv.1
%{_mandir}/man8/genccode.8
%{_mandir}/man8/gencmn.8
%{_mandir}/man8/gensprep.8
%{_mandir}/man8/genuca.8
%{_mandir}/man8/icupkg.8
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/genccode
%{_sbindir}/gencmn
%{_sbindir}/gensprep
%{_sbindir}/genuca
%{_sbindir}/icupkg
%{_sbindir}/icuswap
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%_arch64
%{_bindir}/%_arch64/derb
%{_bindir}/%_arch64/genbrk
%{_bindir}/%_arch64/gencnval
%{_bindir}/%_arch64/genctd
%{_bindir}/%_arch64/genrb
%{_bindir}/%_arch64/icu-config
%{_bindir}/%_arch64/makeconv
%{_bindir}/%_arch64/pkgdata
%{_bindir}/%_arch64/uconv
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/icu/3.6/Makefile.inc
%{_libdir}/%_arch64/icu/Makefile.inc
%{_libdir}/%_arch64/icu/current
%{_libdir}/%_arch64/libicudata.so
%{_libdir}/%_arch64/libicudata.so.36
%{_libdir}/%_arch64/libicudata.so.36.0
%{_libdir}/%_arch64/libicui18n.so
%{_libdir}/%_arch64/libicui18n.so.36
%{_libdir}/%_arch64/libicui18n.so.36.0
%{_libdir}/%_arch64/libicuio.so
%{_libdir}/%_arch64/libicuio.so.36
%{_libdir}/%_arch64/libicuio.so.36.0
%{_libdir}/%_arch64/libicule.so
%{_libdir}/%_arch64/libicule.so.36
%{_libdir}/%_arch64/libicule.so.36.0
%{_libdir}/%_arch64/libiculx.so
%{_libdir}/%_arch64/libiculx.so.36
%{_libdir}/%_arch64/libiculx.so.36.0
%{_libdir}/%_arch64/libicutu.so
%{_libdir}/%_arch64/libicutu.so.36
%{_libdir}/%_arch64/libicutu.so.36.0
%{_libdir}/%_arch64/libicuuc.so
%{_libdir}/%_arch64/libicuuc.so.36
%{_libdir}/%_arch64/libicuuc.so.36.0
%dir %attr (0755, root, bin) %{_sbindir}/%_arch64
%{_sbindir}/%_arch64/genccode
%{_sbindir}/%_arch64/gencmn
%{_sbindir}/%_arch64/gensprep
%{_sbindir}/%_arch64/genuca
%{_sbindir}/%_arch64/icupkg
%{_sbindir}/%_arch64/icuswap
%endif
%changelog
* Thu Dec 13 2007 - groot@kde.org
- Initial version
