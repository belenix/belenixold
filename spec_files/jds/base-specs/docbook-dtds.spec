#
# spec file for package docbook-dtds
#
# copied from fedora core 6
#
# Owner: laca
#
Name: docbook-dtds
Version: 1.0
Release: 30.1
Group: Applications/Text

Summary: SGML and XML document type definitions for DocBook.

License: Distributable
URL: http://www.oasis-open.org/docbook/

Obsoletes: docbook-dtd30-sgml docbook-dtd31-sgml
Obsoletes: docbook-dtd40-sgml docbook-dtd41-sgml
Obsoletes: docbook-dtd412-xml

Provides: docbook-dtd-xml docbook-dtd-sgml
Provides: docbook-dtd30-sgml docbook-dtd31-sgml
Provides: docbook-dtd40-sgml docbook-dtd41-sgml
Provides: docbook-dtd412-xml
Provides: docbook-dtd42-sgml docbook-dtd42-xml
Provides: docbook-dtd43-sgml docbook-dtd43-xml
Provides: docbook-dtd44-sgml docbook-dtd44-xml

PreReq: xml-common fileutils
PreReq: textutils grep perl
PreReq: libxml2 >= 2.4.8
# If upgrading, the old package's postun scriptlet may use install-catalog
# to remove its entries.  xmlcatalog (which this package uses) adds quotes
# to the catalog files, and install-catalog only handles this in 0.6.3-4 or
# later.
PreReq: sgml-common >= 0.6.3-4
# We provide the directory layout expected by 0.6.3-5 or later of
# xml-common.  Earlier versions won't understand.
PreReq: xml-common >= 0.6.3-8

BuildRoot: %{_tmppath}/%{name}-%{version}

BuildArch: noarch
Source0: http://www.oasis-open.org/docbook/sgml/3.0/docbk30.zip
Source1: http://www.oasis-open.org/docbook/sgml/3.1/docbk31.zip
Source2: http://www.oasis-open.org/docbook/sgml/4.0/docbk40.zip
Source3: http://www.oasis-open.org/docbook/sgml/4.1/docbk41.zip
Source4: http://www.oasis-open.org/docbook/xml/4.1.2/docbkx412.zip
Source5: http://www.oasis-open.org/docbook/sgml/4.2/docbook-4.2.zip
Source6: http://www.oasis-open.org/docbook/xml/4.2/docbook-xml-4.2.zip
Source7: http://www.docbook.org/sgml/4.3/docbook-4.3.zip
Source8: http://www.docbook.org/xml/4.3/docbook-xml-4.3.zip
Source9: http://www.docbook.org/sgml/4.4/docbook-4.4.zip
Source10: http://www.docbook.org/xml/4.4/docbook-xml-4.4.zip
# owner:laca date:2007-02-15 type:bug state:upstream from fedora core
Patch0: docbook-dtds-01-30-sgml-1.0.catalog.diff
# owner:laca date:2007-02-15 type:bug state:upstream from fedora core
Patch1: docbook-dtds-02-31-sgml-1.0.catalog.diff
# owner:laca date:2007-02-15 type:bug state:upstream from fedora core
Patch2: docbook-dtds-03-40-sgml-1.0.catalog.diff
# owner:laca date:2007-02-15 type:bug state:upstream from fedora core
Patch3: docbook-dtds-04-41-sgml-1.0.catalog.diff
# owner:laca date:2007-02-15 type:bug state:upstream from fedora core
Patch4: docbook-dtds-05-42-sgml-1.0.catalog.diff
# owner:laca date:2007-02-15 type:bug state:upstream from fedora core
Patch5: docbook-dtds-06-4.2-euro.diff
# owner:laca date:2007-02-15 type:bug state:upstream from fedora core
Patch6: docbook-dtds-07-ents.diff
BuildRequires: unzip

%define openjadever 1.3.2
Requires: openjade = %{openjadever}

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is XML-compliant and is developed by the OASIS consortium.
This package contains SGML and XML versions of the DocBook DTD.


%prep
%setup -c -T
# DocBook V3.0
mkdir 3.0-sgml
cd 3.0-sgml
unzip %{SOURCE0}
gpatch -b docbook.cat %{PATCH0}
cd ..

# DocBook V3.1
mkdir 3.1-sgml
cd 3.1-sgml
unzip %{SOURCE1}
gpatch -b docbook.cat %{PATCH1}
cd ..

# DocBook V4.0
mkdir 4.0-sgml
cd 4.0-sgml
unzip %{SOURCE2}
gpatch -b docbook.cat %{PATCH2}
cd ..

# DocBook V4.1
mkdir 4.1-sgml
cd 4.1-sgml
unzip %{SOURCE3}
gpatch -b docbook.cat %{PATCH3}
cd ..

# DocBook XML V4.1.2
mkdir 4.1.2-xml
cd 4.1.2-xml
unzip %{SOURCE4}
cd ..

# DocBook V4.2
mkdir 4.2-sgml
cd 4.2-sgml
unzip %{SOURCE5}
gpatch -b docbook.cat %{PATCH4}
cd ..

# DocBook XML V4.2
mkdir 4.2-xml
cd 4.2-xml
unzip %{SOURCE6}
cd ..

# DocBook V4.3
mkdir 4.3-sgml
cd 4.3-sgml
unzip %{SOURCE7}
cd ..

# DocBook XML V4.3
mkdir 4.3-xml
cd 4.3-xml
unzip %{SOURCE8}
cd ..

# DocBook V4.4
mkdir 4.4-sgml
cd 4.4-sgml
unzip %{SOURCE9}
cd ..

# DocBook XML V4.4
mkdir 4.4-xml
cd 4.4-xml
unzip %{SOURCE10}
cd ..

# Fix &euro; in SGML.
%patch5 -p1

# Fix ISO entities in 4.3/4.4 SGML
%patch6 -p1

# Increase NAMELEN (bug #36058, bug #159382).
for f in */docbook.dcl
do
  mv $f $f.namelen
  sed -e's,\(NAMELEN\ \ *\)44,\1256,' $f.namelen >$f
done

if [ `id -u` -eq 0 ]; then
  chown -R root:root .
  chmod -R a+rX,g-w,o-w .
fi


%build


%install
# DocBook V3.0
cd 3.0-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-3.0-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook V3.1
cd 3.1-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-3.1-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook V4.0
cd 4.0-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.0-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook V4.1
cd 4.1-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.1-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook XML V4.1.2
cd 4.1.2-xml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/xml-dtd-4.1.2-%{version}-%{release}
mkdir -p $DESTDIR/ent
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
install ent/* $DESTDIR/ent
cd ..

# DocBook V4.2
cd 4.2-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.2-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook XML V4.2
cd 4.2-xml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/xml-dtd-4.2-%{version}-%{release}
mkdir -p $DESTDIR/ent
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
install ent/* $DESTDIR/ent
cd ..

# DocBook V4.3
cd 4.3-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.3-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook XML V4.3
cd 4.3-xml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/xml-dtd-4.3-%{version}-%{release}
mkdir -p $DESTDIR/ent
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
install ent/* $DESTDIR/ent
cd ..

# DocBook V4.4
cd 4.4-sgml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/sgml-dtd-4.4-%{version}-%{release}
mkdir -p $DESTDIR
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
cd ..

# DocBook XML V4.4
cd 4.4-xml
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/docbook/xml-dtd-4.4-%{version}-%{release}
mkdir -p $DESTDIR/ent
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
install ent/* $DESTDIR/ent
cd ..

# Symlinks
mkdir -p $RPM_BUILD_ROOT/etc/sgml
ln -s sgml-docbook-4.4-%{version}-%{release}.cat \
	$RPM_BUILD_ROOT/etc/sgml/sgml-docbook.cat
ln -s xml-docbook-4.4-%{version}-%{release}.cat \
	$RPM_BUILD_ROOT/etc/sgml/xml-docbook.cat


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-,root,root)
%doc --parents 3.1-sgml/ChangeLog
%doc --parents 4.1-sgml/ChangeLog
%doc --parents */*.txt
/usr/share/sgml/docbook/sgml-dtd-3.0-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-3.1-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.0-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.1-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.2-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.3-%{version}-%{release}
/usr/share/sgml/docbook/sgml-dtd-4.4-%{version}-%{release}
/usr/share/sgml/docbook/xml-dtd-4.1.2-%{version}-%{release}
/usr/share/sgml/docbook/xml-dtd-4.2-%{version}-%{release}
/usr/share/sgml/docbook/xml-dtd-4.3-%{version}-%{release}
/usr/share/sgml/docbook/xml-dtd-4.4-%{version}-%{release}
/etc/sgml/sgml-docbook.cat
/etc/sgml/xml-docbook.cat


%post
## Clean up pre-docbook-dtds mess caused by broken trigger.
for v in 3.0 3.1 4.0 4.1 4.2
do
	if [ -f /etc/sgml/sgml-docbook-$v.cat ]
	then
		/usr/bin/xmlcatalog --sgml --noout --del \
			/etc/sgml/sgml-docbook-$v.cat \
			/usr/share/sgml/openjade-1.3.1/catalog 2>/dev/null
	fi
done

##
## SGML catalog
##

# Update the centralized catalog corresponding to this version of the DTD
# DocBook V3.0
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/sgml-dtd-3.0-%{version}-%{release}/catalog

# DocBook V3.1
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/sgml-dtd-3.1-%{version}-%{release}/catalog

# DocBook V4.0
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/sgml-dtd-4.0-%{version}-%{release}/catalog

# DocBook V4.1
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/sgml-dtd-4.1-%{version}-%{release}/catalog

# DocBook XML V4.1.2
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/xml-dtd-4.1.2-%{version}-%{release}/catalog

# DocBook V4.2
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/sgml-dtd-4.2-%{version}-%{release}/catalog

# DocBook XML V4.2
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/xml-dtd-4.2-%{version}-%{release}/catalog

# DocBook V4.3
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/sgml-dtd-4.3-%{version}-%{release}/catalog

# DocBook XML V4.3
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/xml-dtd-4.3-%{version}-%{release}/catalog

# DocBook V4.4
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/sgml-dtd-4.4-%{version}-%{release}/catalog

# DocBook XML V4.4
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat \
	/usr/share/sgml/sgml-iso-entities-8879.1986/catalog
/usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/xml-dtd-4.4-%{version}-%{release}/catalog

# The following lines are for the case in which the style sheets
# were installed after another DTD but before this DTD
STYLESHEETS=$(echo /usr/share/sgml/docbook/dsssl-stylesheets-*)
STYLESHEETS=${STYLESHEETS##*/dsssl-stylesheets-}
if [ "$STYLESHEETS" != "*" ]; then
    # DocBook V3.0
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V3.1
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.0
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.1
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook XML V4.1.2
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.2
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook XML V4.2
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.3
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook XML V4.3
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook V4.4
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog

    # DocBook XML V4.4
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat \
	/usr/share/sgml/openjade-%{openjadever}/catalog
    /usr/bin/xmlcatalog --sgml --noout --add \
	/etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat \
	/usr/share/sgml/docbook/dsssl-stylesheets-$STYLESHEETS/catalog
fi

# Fix up SGML super catalog so that there isn't an XML DTD before an
# SGML one.  We need to do this (*sigh*) because xmlcatalog messes up
# the order of the lines, and SGML tools don't like to see XML things
# they aren't expecting.
CATALOG=/etc/sgml/catalog
SGML=$(cat -n ${CATALOG} | grep sgml-docbook | head -1 | (read n line;echo $n))
XML=$(cat -n ${CATALOG} | grep xml-docbook | head -1 | (read n line; echo $n))
# Do they need switching around?
if [ -n "${XML}" ] && [ -n "${SGML}" ] && [ "${XML}" -lt "${SGML}" ]
then
  # Switch those two lines around.
  XML=$((XML - 1))
  SGML=$((SGML - 1))
  perl -e "@_=<>;@_[$XML, $SGML]=@_[$SGML, $XML];print @_" \
    ${CATALOG} > ${CATALOG}.rpmtmp
  mv -f ${CATALOG}.rpmtmp ${CATALOG}
fi

##
## XML catalog
##

CATALOG=/usr/share/sgml/docbook/xmlcatalog

if [ -w $CATALOG ]
then
	# DocBook XML V4.1.2
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Publishing//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Greek Letters//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ELEMENTS DocBook XML Information Pool V4.1.2//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/dbpoolx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Box and Line Drawing//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-box.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD DocBook XML V4.1.2//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/docbookx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Greek Symbols//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-num.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Character Entities V4.1.2//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/dbcentx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Notations V4.1.2//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/dbnotnx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Diacritical Marks//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Monotoniko Greek//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Additional General Entities V4.1.2//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/dbgenent.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.1.2//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/dbhierx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Russian Cyrillic//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-cyrl.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES General Technical//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/soextblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD DocBook XML CALS Table Model V4.1.2//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/calstblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Latin 1//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Latin 2//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN" \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
		"http://www.oasis-open.org/docbook/xml/4.1.2" \
		"xml-dtd-4.1.2-%{version}-%{release}" $CATALOG
	/usr/bin/xmlcatalog --noout --add "rewriteURI" \
		"http://www.oasis-open.org/docbook/xml/4.1.2" \
		"xml-dtd-4.1.2-%{version}-%{release}" $CATALOG

	# DocBook XML V4.2
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Publishing//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Greek Letters//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ELEMENTS DocBook XML Information Pool V4.2//EN" \
		"xml-dtd-4.2-%{version}-%{release}/dbpoolx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Box and Line Drawing//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-box.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD DocBook XML V4.2//EN" \
		"xml-dtd-4.2-%{version}-%{release}/docbookx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Greek Symbols//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-num.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Character Entities V4.2//EN" \
		"xml-dtd-4.2-%{version}-%{release}/dbcentx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Notations V4.2//EN" \
		"xml-dtd-4.2-%{version}-%{release}/dbnotnx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Diacritical Marks//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Monotoniko Greek//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Additional General Entities V4.2//EN" \
		"xml-dtd-4.2-%{version}-%{release}/dbgenent.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.2//EN" \
		"xml-dtd-4.2-%{version}-%{release}/dbhierx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Russian Cyrillic//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-cyrl.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES General Technical//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
		"xml-dtd-4.2-%{version}-%{release}/soextblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD DocBook XML CALS Table Model V4.2//EN" \
		"xml-dtd-4.2-%{version}-%{release}/calstblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Latin 1//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Latin 2//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN" \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
		"http://www.oasis-open.org/docbook/xml/4.2" \
		"xml-dtd-4.2-%{version}-%{release}" $CATALOG
	/usr/bin/xmlcatalog --noout --add "rewriteURI" \
		"http://www.oasis-open.org/docbook/xml/4.2" \
		"xml-dtd-4.2-%{version}-%{release}" $CATALOG

	# DocBook XML V4.3
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Publishing//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Greek Letters//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ELEMENTS DocBook XML Information Pool V4.3//EN" \
		"xml-dtd-4.3-%{version}-%{release}/dbpoolx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Box and Line Drawing//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-box.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD DocBook XML V4.3//EN" \
		"xml-dtd-4.3-%{version}-%{release}/docbookx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Greek Symbols//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-num.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Character Entities V4.3//EN" \
		"xml-dtd-4.3-%{version}-%{release}/dbcentx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Notations V4.3//EN" \
		"xml-dtd-4.3-%{version}-%{release}/dbnotnx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Diacritical Marks//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Monotoniko Greek//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Additional General Entities V4.3//EN" \
		"xml-dtd-4.3-%{version}-%{release}/dbgenent.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.3//EN" \
		"xml-dtd-4.3-%{version}-%{release}/dbhierx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Russian Cyrillic//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-cyrl.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES General Technical//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
		"xml-dtd-4.3-%{version}-%{release}/soextblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD DocBook XML CALS Table Model V4.3//EN" \
		"xml-dtd-4.3-%{version}-%{release}/calstblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Latin 1//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Latin 2//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN" \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
		"http://www.oasis-open.org/docbook/xml/4.3" \
		"xml-dtd-4.3-%{version}-%{release}" $CATALOG
	/usr/bin/xmlcatalog --noout --add "rewriteURI" \
		"http://www.oasis-open.org/docbook/xml/4.3" \
		"xml-dtd-4.3-%{version}-%{release}" $CATALOG

	# DocBook XML V4.4
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Publishing//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Greek Letters//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ELEMENTS DocBook XML Information Pool V4.4//EN" \
		"xml-dtd-4.4-%{version}-%{release}/dbpoolx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Box and Line Drawing//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-box.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD DocBook XML V4.4//EN" \
		"xml-dtd-4.4-%{version}-%{release}/docbookx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Greek Symbols//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-num.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Character Entities V4.4//EN" \
		"xml-dtd-4.4-%{version}-%{release}/dbcentx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Notations V4.4//EN" \
		"xml-dtd-4.4-%{version}-%{release}/dbnotnx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Diacritical Marks//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Monotoniko Greek//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ENTITIES DocBook XML Additional General Entities V4.4//EN" \
		"xml-dtd-4.4-%{version}-%{release}/dbgenent.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.4//EN" \
		"xml-dtd-4.4-%{version}-%{release}/dbhierx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Russian Cyrillic//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-cyrl.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES General Technical//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
		"xml-dtd-4.4-%{version}-%{release}/soextblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"-//OASIS//DTD DocBook XML CALS Table Model V4.4//EN" \
		"xml-dtd-4.4-%{version}-%{release}/calstblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Latin 1//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Latin 2//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "public" \
		"ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN" \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
		"http://www.oasis-open.org/docbook/xml/4.4" \
		"xml-dtd-4.4-%{version}-%{release}" $CATALOG
	/usr/bin/xmlcatalog --noout --add "rewriteURI" \
		"http://www.oasis-open.org/docbook/xml/4.4" \
		"xml-dtd-4.4-%{version}-%{release}" $CATALOG
fi

# Finally, make sure everything in /etc/sgml is readable!
/bin/chmod a+r /etc/sgml/*

%postun
##
## SGML catalog
##

# Update the centralized catalog corresponding to this version of the DTD
# DocBook V3.0
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-3.0-%{version}-%{release}.cat

# DocBook V3.1
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-3.1-%{version}-%{release}.cat

# DocBook V4.0
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.0-%{version}-%{release}.cat

# DocBook V4.1
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.1-%{version}-%{release}.cat

# DocBook XML V4.1.2
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat
rm -f /etc/sgml/xml-docbook-4.1.2-%{version}-%{release}.cat

# DocBook V4.2
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.2-%{version}-%{release}.cat

# DocBook XML V4.2
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat
rm -f /etc/sgml/xml-docbook-4.2-%{version}-%{release}.cat

# DocBook V4.3
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.3-%{version}-%{release}.cat

# DocBook XML V4.3
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat
rm -f /etc/sgml/xml-docbook-4.3-%{version}-%{release}.cat

# DocBook V4.4
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat
rm -f /etc/sgml/sgml-docbook-4.4-%{version}-%{release}.cat

# DocBook XML V4.4
/usr/bin/xmlcatalog --sgml --noout --del /etc/sgml/catalog \
	/etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat
rm -f /etc/sgml/xml-docbook-4.4-%{version}-%{release}.cat

# Fix up SGML super catalog so that there isn't an XML DTD before an
# SGML one.  We need to do this (*sigh*) because xmlcatalog messes up
# the order of the lines, and SGML tools don't like to see XML things
# they aren't expecting.
CATALOG=/etc/sgml/catalog
SGML=$(cat -n ${CATALOG} | grep sgml-docbook | head -1 | (read n line;echo $n))
XML=$(cat -n ${CATALOG} | grep xml-docbook | head -1 | (read n line; echo $n))
# Do they need switching around?
if [ -n "${XML}" ] && [ -n "${SGML}" ] && [ "${XML}" -lt "${SGML}" ]
then
  # Switch those two lines around.
  XML=$((XML - 1))
  SGML=$((SGML - 1))
  perl -e "@_=<>;@_[$XML, $SGML]=@_[$SGML, $XML];print @_" \
    ${CATALOG} > ${CATALOG}.rpmtmp
  mv -f ${CATALOG}.rpmtmp ${CATALOG}
fi

##
## XML catalog
##

CATALOG=/usr/share/sgml/docbook/xmlcatalog

if [ -w $CATALOG ]
then
	# DocBook XML V4.1.2
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/dbpoolx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-box.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/docbookx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-num.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/dbcentx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/dbnotnx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/dbgenent.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/dbhierx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-cyrl.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/soextblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/calstblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.1.2-%{version}-%{release}" $CATALOG

	# DocBook XML V4.2
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/dbpoolx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-box.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/docbookx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-num.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/dbcentx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/dbnotnx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/dbgenent.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/dbhierx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-cyrl.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/soextblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/calstblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.2-%{version}-%{release}" $CATALOG

	# DocBook XML V4.3
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/dbpoolx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-box.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/docbookx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-num.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/dbcentx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/dbnotnx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/dbgenent.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/dbhierx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-cyrl.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/soextblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/calstblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.3-%{version}-%{release}" $CATALOG

	# DocBook XML V4.4
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-pub.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-grk1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/dbpoolx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-box.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/docbookx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-grk3.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsn.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-num.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/dbcentx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-grk4.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/dbnotnx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-dia.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-grk2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/dbgenent.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/dbhierx.mod" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsa.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amso.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-cyrl.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-tech.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsc.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/soextblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/calstblx.dtd" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-lat1.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsb.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-lat2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-amsr.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}/ent/iso-cyr2.ent" $CATALOG
	/usr/bin/xmlcatalog --noout --del \
		"xml-dtd-4.4-%{version}-%{release}" $CATALOG
fi

%changelog
* Wed Feb 28 2007 - halton.huo@sun.com
- Fix Increase NAMELEN sed script error.
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0-30.1
- rebuild
* Tue Dec 13 2005 Tim Waugh <twaugh@redhat.com> 1.0-30
- Fix ISO entities in 4.3/4.4 SGML.
* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt
* Fri Oct 21 2005 Tim Waugh <twaugh@redhat.com> 1.0-29
- Scriptlet fix (bug #171229).
* Thu Oct 13 2005 Tim Waugh <twaugh@redhat.com> 1.0-28
- Fixed last fix (bug #159382).
* Thu Jun  2 2005 Tim Waugh <twaugh@redhat.com> 1.0-27
- Increase NAMELEN (bug #36058, bug #159382).
* Tue Feb  1 2005 Tim Waugh <twaugh@redhat.com> 1.0-26
- DocBook 4.4 SGML and XML.
* Mon Sep 13 2004 Tim Waugh <twaugh@redhat.com> 1.0-25
- DocBook 4.3 SGML and XML (bug #131861).
* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 1.0-24
- Use ':' instead of '.' as separator for chown.
* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt
* Wed Aug  6 2003 Tim Waugh <twaugh@redhat.com> 1.0-22.1
- Rebuilt.
* Wed Aug  6 2003 Tim Waugh <twaugh@redhat.com> 1.0-22
- More work-arounds for buggy xmlcatalog.
* Tue Jul 15 2003 Tim Waugh <twaugh@redhat.com> 1.0-21.1
- Rebuilt.
* Tue Jul 15 2003 Tim Waugh <twaugh@redhat.com> 1.0-21
- Fix &euro; in SGML tools.
* Wed May 28 2003 Tim Waugh <twaugh@redhat.com> 1.0-20
- Fix summary and description (bug #73005).
* Fri Mar 28 2003 Tim Waugh <twaugh@redhat.com> 1.0-19
- Use --parents in %%doc.
- Fix %%postun scriptlet.
* Fri Mar 14 2003 Tim Waugh <twaugh@redhat.com> 1.0-18
- Use Requires:, not Conflicts:, for openjade.
- Require openjade 1.3.2.
* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.0-17
- rebuilt
* Fri Dec 20 2002 Tim Waugh <twaugh@redhat.com> 1.0-16
- Fix typos in scriplets (bug #80109).
* Wed Nov 20 2002 Tim Powers <timp@redhat.com> 1.0-15
- rebuild in current collinst
* Mon Jul 30 2002 Tim Waugh <twaugh@redhat.com> 1.0-14
- Fix typo in XML catalog (Eric Raymond).
* Tue Jul 23 2002 Tim Waugh <twaugh@redhat.com> 1.0-13
- Provide docbook-dtd42-sgml and docbook-dtd42-xml.
* Thu Jul 18 2002 Tim Waugh <twaugh@redhat.com> 1.0-12
- Fix up SGML super catalog if necessary.
* Wed Jul 17 2002 Tim Waugh <twaugh@redhat.com> 1.0-11
- Add DocBook V4.2.
* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.0-10
- automated rebuild
* Thu May 23 2002 Tim Powers <timp@redhat.com> 1.0-9
- automated rebuild
* Thu Mar 14 2002 Tim Waugh <twaugh@redhat.com> 1.0-8
- Allow for shared /usr/share (bug #61147).
* Tue Mar 12 2002 Tim Waugh <twaugh@redhat.com> 1.0-7
- Make sure that the config files are readable.
* Fri Mar  8 2002 Tim Waugh <twaugh@redhat.com> 1.0-6
- Make %%post scriptlet quiet (bug #60820).
* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.0-5
- Make sure to clean up old catalog files.
* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.0-3
- Rebuild in new environment.
* Mon Jan 28 2002 Tim Waugh <twaugh@redhat.com> 1.0-2
- Prepare for openjade 1.3.1.
* Thu Jan 17 2002 Tim Waugh <twaugh@redhat.com> 1.0-1
- Merged all the DTD packages into one (bug #58448).
- Use /usr/share/sgml exclusively.
- Prevent catalog files from disappearing on upgrade (bug #58463).
* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild
* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 1.0-8
- Hmm, still need to depend on sgml-common for /etc/sgml.
* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 1.0-7
- Use xmlcatalog (libxml2) instead of install-catalog (sgml-common) in
  scriptlets.
- Conflict with install-catalog if it can't handle quotes in catalogs.
- Use release number in centralized catalog name, so that the scriptlets
  work properly.
* Wed Oct 10 2001 Tim Waugh <twaugh@redhat.com> 1.0-6
- Change some Requires: to PreReq:s (bug #54507).
* Mon Oct  8 2001 Tim Waugh <twaugh@redhat.com> 1.0-5
- Use release number in the installed directory name, so that the
  package scripts work.
* Sat Oct  6 2001 Tim Waugh <twaugh@redhat.com> 1.0-4
- Restore the /etc/sgml/catalog manipulation again.
- Oops, fix DTD path.
* Sat Oct  6 2001 Tim Waugh <twaugh@redhat.com> 1.0-2
- Require xml-common.  Use xmlcatalog.
- Move files to /usr/share/xml.
* Tue Jun 12 2001 Tim Waugh <twaugh@redhat.com> 1.0-1
- Build for Red Hat Linux.
* Sat Jun 09 2001 Chris Runge <crunge@pobox.com>
- Provides: docbook-dtd-xml (not docbook-dtd-sgml)
- undo catalog patch and dbcentx patch (this resulted in an effectively
  broken DTD when the document was processed with XSL stylesheets); added a
  symbolic link to retain docbook.cat -> catalog; added ent
- added ChangeLog to doc
* Fri Jun 08 2001 Chris Runge <crunge@pobox.com>
- created a 4.1.2 version
- update required a change to OTHERCAT in postun
- update required a change to the Makefile patch (no dbgenent.ent any more,
  apparently)
* Wed Jan 24 2001 Tim Waugh <twaugh@redhat.com>
- Scripts require fileutils.
- Make scripts quieter.
* Mon Jan 15 2001 Tim Waugh <twaugh@redhat.com>
- Don't play so many macro games.
- Don't use 'rpm' in post scripts.
- Be sure to own xml-dtd-4.1 directory.
* Sun Jan 14 2001 Tim Waugh <twaugh@redhat.com>
- Change requirement on /usr/bin/install-catalog to sgml-common.
* Tue Jan 09 2001 Tim Waugh <twaugh@redhat.com>
- Change group.
- Use %%{_tmppath}.
- Correct typo.
- rm before install
- openjade not jade.
- Build requires unzip.
- Require install-catalog for post and postun.
- Change Copyright: to License:.
- Remove Packager: line.
* Tue Jan 09 2001 Tim Waugh <twaugh@redhat.com>
- Based on Eric Bischoff's new-trials packages.
