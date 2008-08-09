#
# Default settings for GNOME packages on Solaris
#
# Portions Copyright 2007 Sun Microsystems, Inc.
#
SUNW_ProdName:             SpecFilesExtra
SUNW_ProdVers:             1.0

%define default_pkg_version 2.18.0
%define jds_version         JDSosol
%define default_category   SFE,application
%define support_level      unsupported

# use --with-tjds to build the JDS Trusted Extensions
# default: no tjds
%define build_tjds %{?_with_tjds:1}%{?!_with_tjds:0}

Vendor:			   http://pkgbuild.sf.net/spec-files-extra
%define                    pkg_prefix SFE
%{?sf_mirror:#}%define sf_mirror easynews.dl.sourceforge.net
%{?sf_download:#}%define sf_download http://downloads.sourceforge.net

%define xfce_pkg_version 4.4.2
%define xfce_src_url http://www.us.xfce.org/archive/xfce-%{xfce_pkg_version}/src
%define xfce_banding OSOL


# ChangeLog:
# 2008-03-01  moinakg@gmail.com
# - Add Xfce definitions.
# 2008-02-21  moinakg@gmail.com
# - Add Sourceforge download URL for auto-selecting best mirror.
# 2007-03-16  Laszlo (Laca) Peter  <laca@sun.com>
# - copied from the JDS spec-files and updated for SFE
# 2007-03-15  Laszlo (Laca) Peter  <laca@sun.com>
# - create by moving product specific stuff out of Solaris.inc