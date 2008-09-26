#
#    Advanced SVR4 package and repository management layer
#    Copyright (C) 2008  The BeleniX team
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#    Author: Moinak Ghosh
#

import sys
import os
import shutil
import getopt
import re
import traceback
import gettext
import string
import tsort
import time
import sha
#from stat import *
from subprocess import Popen, PIPE, STDOUT
from urlparse import urlparse
from decimal import Decimal

class Cl_pkgentry(object):
	"""Class that holds all fields of a package entry in the catalog including site related entries."""

	def __init__(self, entry, sitevars):
		self.cname = entry[0]
		self.version = entry[1]
		self.pkgname = entry[2]
		self.pkgfile = entry[3]
		self.sha1sum = entry[4]
		self.origvers = entry[5]
		self.type = entry[6]
		self.sitevars = sitevars
		self.refername = ""
		self.deplist = []
		self.action = 0
		self.dwn_pkgfile = ""

	def update(self, entry, sitevars):
		self.cname = entry[0]
		self.version = entry[1]
		self.pkgname = entry[2]
		self.pkgfile = entry[3]
		self.sha1sum = entry[4]
		self.sitevars = sitevars
		

class Cl_sitevars(object):
	"""Class that holds site - specific variables."""

	def __init__(self, site, RELEASE, RTYPE, SPKG_VAR_DIR):
		so = urlparse(site)
		self.site = site
		self.psite = so
		self.fullurl = "%s/%s/%s" % (site, RELEASE, RTYPE)
		self.trunkurl = "%s/trunk/%s" % (site, RTYPE)
		self.catalog = "%s/catalog-%s-%s" % (SPKG_VAR_DIR, RELEASE, so[1])
		self.mirrors = "%s/mirrors-%s" % (SPKG_VAR_DIR, so[1])
		self.metadir = "%s/metainfo-%s" % (SPKG_VAR_DIR, so[1])
		self.base_cluster = {}
		self.tcat = "%s/catalog" % SPKG_VAR_DIR
		self.tmeta = "%s/metainfo.tar.7z" % SPKG_VAR_DIR
		self.tmetadir = "%s/metainfo" % SPKG_VAR_DIR
		self.catfh = None

		
class Cl_img(object):
	"""Class that holds some globally used values."""
	def __init__(self):
		# Hardcoded for now
		self.cnffile = "/etc/spkg.conf"

		self.ALTROOT = ""
		self.RTYPE = "unstable"
		self.PKGSITES = ["http://pkg.belenix.org"]
		self.PKGADDFLAGS = ""
		self.SPKG_PRESERVE_DOWNLOADS = False
		self.USE_GPG = True
		self.USE_MD5 = True
		self.WGET = "/usr/sfw/bin/wget"
		self.SZIP = "/usr/bin/7za"
		self.OSREL = "5.11"
		self.CPU = "i386"
		self.SPKG_VAR_DIR = "/var/spkg"
		self.SPKG_DWN_DIR = "/var/spkg/downloads"
		self.SPKG_GRP_DIR = "/var/spkg/groups"
		self.RELEASE = "trunk"
		self.PKGSITEVARS = []
		self.INSTPKGDIR = "/var/sadm/pkg"
		self.ADMINFILE = self.SPKG_VAR_DIR + "/admin"
		self.RELEASES_LIST = "%s/releases" % self.SPKG_VAR_DIR
		self.bename = ""

		# Fields numbers in a catalog entry for a package
		self.CNAMEF = 0; self.VERSIONF = 1
		self.PKGNAMEF = 2; self.PKGFILEF = 3
		self.MD5SUMF = 4; self.ORIGVERSF = 5
		self.TYPEF = 6

		# Action codes for packages
		self.NONE = 0
		self.INSTALL = 1; self.UPGRADE = 2
		self.UPGRADE_BASE = 3; self.UPGRADE_ALL = 4
		self.REMOVE = 5; self.LIST_ONLY = 6

	def set_altroot(self, apath):
		if self.ALTROOT == "":
			if apath[-1] == "/":
				apath = apath.rstrip('/')
			self.ALTROOT = apath
			self.SPKG_VAR_DIR = apath + self.SPKG_VAR_DIR
        		self.SPKG_DWN_DIR = apath + self.SPKG_DWN_DIR
        		self.SPKG_GRP_DIR = apath + self.SPKG_GRP_DIR
        		self.INSTPKGDIR = apath + self.INSTPKGDIR
        		self.ADMINFILE = apath + self.ADMINFILE
			self.RELEASES_LIST = apath + self.RELEASES_LIST
		else:
			self.SPKG_VAR_DIR = self.SPKG_VAR_DIR.replace(self.ALTROOT, apath)
			self.SPKG_DWN_DIR = self.SPKG_DWN_DIR.replace(self.ALTROOT, apath)
			self.SPKG_GRP_DIR = self.SPKG_GRP_DIR.replace(self.ALTROOT, apath)
			self.INSTPKGDIR = self.INSTPKGDIR.replace(self.ALTROOT, apath)
			self.ADMINFILE = self.ADMINFILE.replace(self.ALTROOT, apath)
			self.RELEASES_LIST = self.RELEASES_LIST.replace(self.ALTROOT, apath)
			self.ALTROOT = apath

	def init(self, altroot):
		dwn_dir = altroot + self.SPKG_DWN_DIR
		try:
			os.makedirs(dwn_dir)
		except:
			pass

		conf = self.ALTROOT + self.cnffile
		if not os.path.exists(conf):
			shutil.copyfile(self.cnffile, conf)

		admin = altroot + self.ADMINFILE
		if not os.path.exists(admin):
			shutil.copyfile(self.ADMINFILE, admin)

		#
		# Altroot initialized now reset ourselves to point to this new image
		#
		self.set_altroot(altroot)

class TransformPlan:
	"""Holds a set of packages and actions to perform on those packages
	for a given filesystem image"""

	def __init__(self, img, pdict, sorted_list, action):
		self.img = img
		self.pdict = pdict
		self.sorted_list = sorted_list
		self.action = action

class PKGError(Exception):
	"""General packaging error"""

	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

class PKGVersError(PKGError):
	"""Invalid version exception"""

	def __init__(self, message):
		self.message = message

class PKGCksumError(PKGError):
	"""Package checksum verification error"""

	def __init__(self, message):
		self.message = message

class PKGMetaError(PKGError):
	"""Metainfo processing error"""

	def __init__(self, message):
		self.message = message

img = Cl_img()

def usage():
	print >> sys.stderr, _("""\
Usage:
	spkg [options] subcommand [cmd_options] [operands]

Subcommands:
	updatecatalog   Updates download site metadata
	install         <package names>
	                Install one or more packages/package clusters

	upgrade [<Upgrade Type> <release tag>]|[<package list>]
	                Upgrades already installed packages if possible
	                Upgrade type can be one of:
	                core - Upgrade the core distro (Kernel, core libs etc.)
	                all - Upgrade the entire distribution.

	                release tag - The distro release to upgrade to for core or all.

	available [-r]  Lists the available packages in all sites
                        With '-r' flag lists all the current distro releases available.
	compare         Shows installed package versions vs available
	info [-s] [<pkg list>]
	                List information about packages whether installed or not
	                With '-s' display a short listing of only package descriptions.

	contents [-l]   List all pathnames delivered by the package. With '-l' show a long
	                listing that shows pathname type, ownership and permission.
	search [-F] <pattern>
	                Search for the given pattern in the catalogs. With '-F' perform a
	                full-text search in all the package contents.
	                <pattern> can be simple string/pathname or a regular expression.

	init <dir>      Initialize an Alternate Root image in the given dir. The dir is
	                created if it does not exist
	download        Just download the package, do not install

Options:
	-R <dir>             Perform all operations onto an Alternate Root image in the dir
	-s http://site/dir   Temporarily override site to get from
	-r <release tag>     Use packages from the given release tag overriding configuration
	                     and environment settings. Specify 'trunk' to see latest packages.

Environment Valriables:
	ALTROOT		     Directory that contains an Alternate root image
			     This variable can be used in lieu of -R
	USE_RELEASE_TAG      Use the specified release tag for checking for packages.
	                     This can be "trunk" to indicate use latest head packages.
	                     The behavior is same as that of using 'spkg -l'
	                     Alternatively this can mention a specific release like
	                     belenix_0.7.1. Use spkg available -r to see list of possible
	                     release tags.

	http_proxy	     Http proxy server
	ftp_proxy	     Ftp proxy server""")
	sys.exit(2)

#
# Useful utility functions
#
def removef(path):
	"""Emulate rm -f <filename>"""
	try:
		os.unlink(path)
	except:
		pass

def exec_prog(cmd, outp):
	"""Execute an external program and return stdout if needed."""

	err_file = os.tmpfile()

	output = ""
	if outp == 1:
		pipe = Popen(cmd, shell=True, stdout=PIPE, stderr=err_file, close_fds=True)
		output = pipe.stdout.read()
	else:
		pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
	rt = pipe.wait()

	if rt != 0:
		err_file.seek(0)
		err = PKGError("WARNING: " + cmd + " had errors\n" + err_file.read())
		err_file.close()
		raise err
	err_file.close()

	return string.strip(output)


def load_config(use_site):
	"""Load configuration file and also detect environment settings."""

	com = re.compile("^#")

	if os.environ.has_key("USE_RELEASE_TAG"):
		use_release = os.environ["USE_RELEASE_TAG"]
	else:
		use_release = ""

	fl = open(img.cnffile, "r")
	for line in fl:
		if com.match(line):
			continue

		line = string.strip(line)
		fields = line.split("=")
		if len(fields) < 2:
			continue

		if fields[0] == "RTYPE":
			img.RTYPE = fields[1]
		elif fields[0] == "USE_RELEASE_TAG":
			if not os.environ.has_key("USE_RELEASE_TAG"):
				use_release = fields[1]
		elif fields[0] == "PKGSITES":
			img.PKGSITES = fields[1].split(" ")
		elif fields[0] == "FTP_PROXY":
			if not os.environ.has_key("ftp_proxy"):
				os.environ["ftp_proxy"] = fields[1]
		elif fields[0] == "HTTP_PROXY":
			if not os.environ.has_key("http_proxy"):
				os.environ["http_proxy"] = fields[1]
		elif fields[0] == "PKGADDFLAGS":
			img.PKGADDFLAGS = fields[1]
		elif fields[0] == "SPKG_DOWNLOAD_DIR":
			img.SPKG_DOWNLOAD_DIR = fields[1]
		elif fields[0] == "SPKG_PRESERVE_DOWNLOADS":
			if fields[1] == "true":
				img.SPKG_PRESERVE_DOWNLOADS = True
		elif fields[0] == "USE_GPG":
			if fields[1] == "true":
				img.USE_GPG = True
		elif fields[0] == "USE_MD5":
			if fields[1] == "true":
				img.USE_MD5 = True

	img.OSREL = exec_prog("uname -r", 1)
	img.ARCH = exec_prog("uname -p", 1)

	#
	# Use only package updates from release-specific repository if latest
	# bleeding edge packages are not desired.
	#
	if len(use_release) == 0:
		relfile = "%s/etc/release_tag" % img.ALTROOT
		if os.path.isfile(relfile):
			rf = open(relfile, "r")
			img.RELEASE = string.strip(rf.readline())
			rf.close()
	else:
		img.RELEASE = use_release

	# Initialize site-specific variables
	#
	if len(use_site) > 0:
		img.PKGSITES=[use_site]

	for site in img.PKGSITES:
		sitevars = Cl_sitevars(site, \
	    	img.RELEASE, img.RTYPE, img.SPKG_VAR_DIR)
		img.PKGSITEVARS.append(sitevars)
		

def verify_sha1sum(ent, dfile):
	"""Verify the SHA1 checksum for the downloaded package file"""

	shash = sha.new()
	fh = open(dfile, "rb")
	while 1:
		buf = fh.read(16 * 1024)
		if not buf:
			break
		shash.update(buf)
	fh.close()
	dig = shash.hexdigest()

	if not dig == ent.sha1sum:
		raise PKGCksumError("Failed to verify Checksum for package %s" % ent.refername)

#
# Download from a given URL to a given file. It can also take
# a file:// url in which case it copies the given file.
#
def downloadurl(url, targ):
	"""Use a downloader to fetch the given URL. Return the size or -1 for error."""

	# TODO: Move to prozilla later
	wgetopts = "-c -O %s" % targ
	if url[:7] == "file://":
		fl = url[8:]
		if not os.path.isfile(fl):
			raise PKGError("ERROR: file %s does not exist" % fl)
		shutil.copyfile(fl, targ)
	elif url[:6] == "ftp://":
		wgetopts = "-O %s --passive-ftp" %targ

	out = exec_prog("%s %s %s" % (img.WGET, wgetopts, url), 0)
	sz = 0
	sz = os.path.getsize(targ)
	if sz == 0:
		raise PKGError("Downloaded file is of zero length")

#
# Given a package revision string of the form:
# VERSION=11.11,REV=2008.07.10.02.06
# it can compute a an uniform numeric version sting of the form:
# 1111.0000.1075.9724.46
#
def compute_version(verstr):
	"""Compute an uniform version string given a package revision string"""

	verlst = verstr.split(",")
	if len(verlst) > 1:
		_version, _revision = verlst
	else:
		_version = verstr
		_revision = "REV=1"

	_revision.replace(".0", ".")
	_revision.replace("..", ".0.")

	version = _version.split("=")[1]
	if len(version) == 0:
		version = "1"

	revision = _revision.split("=")[1]
	rv = revision.split(".")
	ln = len(rv)

	cnv1 = Decimal(535680);  cnv2 = Decimal(44640)
	cnv3 = Decimal(1440);    cnv4 = Decimal(60)

	#
	# Process revision strings of various known formats
	#
	if ln == 8:
		pkgrev = Decimal(rv[3]) * cnv1 + Decimal(rv[4]) * cnv2 + \
		    Decimal(rv[5]) * cnv3 + Decimal(rv[6]) * cnv4 + Decimal(rv[7])
	elif ln == 5:
		pkgrev = Decimal(rv[0])  * cnv1 + Decimal(rv[1]) * cnv2 + \
		    Decimal(rv[2]) * cnv3 + Decimal(rv[3]) * cnv4 + Decimal(rv[4])
	elif ln == 4:
		pkgrev = Decimal(rv[0]) + Decimal(rv[1]) * cnv1 + Decimal(rv[2]) * cnv2 + \
		    Decimal(rv[3]) * cnv3
	elif ln == 3:
		pkgrev = Decimal(rv[0]) * cnv1 + Decimal(rv[1]) * cnv2 + Decimal(rv[2]) * cnv3
	else:
		#rv = time.strftime("%Y.%m.%d.%H.%M")
		#pkgrev = Decimal(rv[0])  * cnv1 + Decimal(rv[1]) * cnv2 + \
		#    Decimal(rv[2]) * cnv3 + Decimal(rv[3]) * cnv4 + Decimal(rv[4])
		pkgrev= Decimal(1)


	version = version.replace(".", "")
	#
	# Handle alphanumeric chars in version string. The alpha chars are stripped
	# and their ASCII values added up. The sum is then added to the 8-digit
	# version number.
	#
	tot = len(version)
	cnt = 0
	alphasum = 0
	vstr = []
	append = vstr.append
	while cnt < tot:
		dig = version[cnt]
		try:
			n = int(dig)
			append(dig)
		except ValueError:
			alphasum = alphasum + ord(dig)
		cnt = cnt + 1

	if alphasum > 0:
		if len(vstr) > 0:
			ver = Decimal(''.join(vstr))
		else:
			ver = Decimal(0)
		ver = Decimal(str(ver).ljust(8, "0")) + Decimal(cnt)
		version = str(ver)
	else:
		version = version.ljust(8, "0")

	#
	# Now prepare a version string with a dot after every 4 digits
	#
	revline = version + str(pkgrev)
	tot = len(revline)
	cnt = 0
	num = 1
	vstr = []
	append = vstr.append
	while cnt < tot:
		dig = revline[cnt]
		append(dig)
		cnt = cnt + 1
		if num % 4 == 0 and cnt < tot:
			append('.')
        	num = num + 1

	return ''.join(vstr)

#
# Compare the version part or first 2 components of the version string
# ver1 > ver2:  return 1
# ver1 == ver2:  return 0
# ver1 < ver2;  return -1
#
def compare_version(vstr1, vstr2):
	"""Compare only the version parts of the given version strings.
	First 2 segments of the version string give the upstream package
	version."""

	vers1 = Decimal(''.join(vstr1.split(".")[0:2]))
	vers2 = Decimal(''.join(vstr2.split(".")[0:2]))

	return str(vers1.compare(vers2))


#
# Compare the revision portion of the version string.
# ver1 > ver2:  return 1
# ver1 == ver2:  return 0
# ver1 < ver2;  return -1
#
def compare_revision(vstr1, vstr2):
	"""Compare onyl the revision portion of the given version strings.
	All segments after first 2 in the version string constitute package revision."""

	rev1 = Decimal(''.join(vstr1.split(".")[2:]))
	rev2 = Decimal(''.join(vstr2.split(".")[2:]))

	return str(rev1.compare(rev2))

#
# Compare the full version string
# ver1 > ver2:  return 1
# ver1 == ver2:  return 0
# ver1 < ver2;  return -1
#
def compare_vers(vstr1, vstr2):
	"""Compare the complete version string"""

	ver1 = Decimal(vstr1.replace(".", ""))
	ver2 = Decimal(vstr2.replace(".", ""))

	return cmp(ver1, ver2)

def fetch_local_version(img, pkg):
	"""Return the installed package version in uniform version format"""

	if pkg.type == "P":
		try:
			vf = open("%s/%s/pkginfo" % (img.INSTPKGDIR, pkg.pkgname), "r")
		except:
			pkgnamei = pkgname + ".i"
			vf = open("%s/%s/pkginfo" % (img.INSTPKGDIR, pkgnamei), "r")
	else:
		vf = open("%s/%s/pkginfo" % (img.SPKG_GRP_DIR, pkg.pkgname), "r")

	for line in vf:
		if line[0:4] == "VERS":
			vf.close()
			ver = line.strip()
			cver = compute_version(ver)
			return (cver, ver)
	vf.close()

	raise PKGVersError("FATAL: VERSION field not found for package %s" % pkgname)

def fetch_metainfo_fields(site, pkgname, version, type, fnames):
	"""Fetch one or more pkginfo fields(given by fnames list) from the site's metainfo dir"""

	if type == "P":
		pkginf = "%s/%s/%s/pkginfo" % (site.metadir, pkgname, version)
	else:
		pkginf = "%s/groups/%s/%s/pkginfo" % (site.metadir, pkgname, version)

	pf = open(pkginf, "r")
	nmdict = {}
	for fname in fnames:
		nmdict[fname] = ""

	for line in pf:
		fentry = line.split("=")
		fname = fentry[0].strip()
		if nmdict.has_key(fname):
			if len(fentry) > 2:
				fvalue = '='.join(fentry[1:])
			else:
				fvalue = fentry[1]
			nmdict[fname] = fvalue.strip()
	pf.close()

	fvalues = []
	for fname in fnames:
		if not nmdict.has_key(fname):
			raise PKGMetaError("FATAL: %s field not found for package %s" % \
			    (fname, pkgname))
		fvalues.append(nmdict[fname])

	return fvalues

#
# Generic catalog search routine to support spkg search
#
def searchcatalog(sitevars, srchre, fieldnum):
	"""Search the site's catalog for the given regexp in the given field."""

	catf = open(sitevars.catalog, "r")
	matches = []

	if fieldnum == -1:
		matches = [Cl_pkgentry(line.split(" "), sitevars) for line in catf \
		    if srchre.search(line)]
	else:
		matches = [Cl_pkgentry(entry, sitevars) for entry in \
		    [line.split(" ") for line in catf] \
		    if srchre.search(entry[fieldnum])]
		#for line in catf:
		#	entry = line.split(" ")
		#	if srchre.match(entry[fieldnum]):
		#		matches.append(Cl_pkgentry(entry, sitevars))

	return matches

#
# Download catalogs and package metadata for all configured sites
#
def updatecatalog(img, pargs):
	"""Refresh catalogs and other metadata for all sites."""

	failed_sites = []
	errored = 0
	releases_found = False

	for sv in img.PKGSITEVARS:

		#
		# Try to fetch the catalog first
		#
		removef(sv.tcat)
		try:
			downloadurl("%s/%s/%s/catalog" % (sv.fullurl, img.ARCH, img.OSREL), 
	 		    sv.tcat)
		except PKGError, pe:
			failed_sites.append((sv.site, \
			    _("ERROR fetching catalogs file %s\n" % pe.message)))
			errored = 1
			removef(sv.tcat)
			continue

		## TODO GPG signature checking
		print "Updating Catalog for site %s\n" % sv.site
		shutil.copyfile(sv.tcat, sv.catalog)
		removef(sv.tcat)

		#
		# Try to fetch the metainfo. This is required
		#
		removef(sv.tmeta)
		try:
			downloadurl("%s/trunk/%s/%s/%s/metainfo.tar.7z" % \
			    (sv.site, img.RTYPE, img.ARCH, img.OSREL), sv.tmeta)
		except PKGError, pe:
			failed_sites.append((sv.site, \
			    _("ERROR fetching metainfo %s\n" % pe.message)))
			errored = 1
			removef(sv.tmeta)
			continue
		
		## TODO GPG signature checking
		print "\nUpdating metainfo for site %s\n" % sv.site
		try:
			out = exec_prog("%s e -so %s | (cd %s; tar xf -)" % \
			    (img.SZIP, sv.tmeta, img.SPKG_VAR_DIR), 0)
		except PKGError, pe:
			failed_sites.append((sv.site, \
			    _("ERROR: Could not extract metainfo %s\n" % pe.message)))
			errored = 1
			removef(sv.tmeta)
			shutil.rmtree(sv.tmetadir, True)
			continue

		shutil.rmtree(sv.metadir, True)
		os.rename(sv.tmetadir, sv.metadir)
		removef(sv.tmeta)

		#
		# Try to fetch mirrors list for site, if any
		#
		try:
			downloadurl("%s/mirrors" % sv.site, sv.mirrors)
		except PKGError:
			removef(sv.mirrors)

		#
		# The releases file provides a list of distro releases. A valid releases
		# file found in the first site is used.
		#
		if not releases_found:
			# Now try to fetch the releases file
			removef(img.RELEASES_LIST)
			sz = 0
			try:
				downloadurl("%s/trunk/releases" % sv.site, img.RELEASES_LIST)
				releases_found = True
			except PKGError, pe:
				removef(img.RELEASES_LIST)

	if errored == 1:
		print "\n\n"
		print "ERROR: Failed to update metadata for some sites. Log follows: \n"
		for stuple in failed_sites:
			print "%s :: \n" % stuple[0]
			print "              %s\n" % stuple[1]
		return 1

	if releases_found == 0:
		print "\n\n"
		print "ERROR: The mandatory releases list not found in any site!\n"
		return 1

	return 0

#
# Core package scanning and dependency list scanning logic. However does not
# build a dependency sorted list. Rather it returns the fully resolved package
# hash with all dependencies.
# type == 1   Install packages
# type == 2   Upgrade specified packages
# type == 3   Upgrade base OS packages
# type == 4   Upgrade all packages
# type == 5   Remove packages
# type == 6   Just prepare catalog entries for the given packages
#
# A level argument is used to identify recursive calls for dependency handling.
# This is needed since during dependency handling for either Install or Upgrade
# dependencies my need to be upgraded or installed.
#
def do_build_pkglist(img, pkgs, pdict, type, level):
	"""Build a complete list of packages to be installed/upgraded
	including resolved dependencies"""

	if len(pkgs) == 0:
		if level == 0:
			raise PKGError(_("No packages specified"))
		else:
			return type

	#
	# Locals for performance
	#
	CNAMEF = img.CNAMEF;  PKGNAMEF = img.PKGNAMEF
	VERSIONF = img.VERSIONF
	UPGRADE = img.UPGRADE;  UPGRADE_ALL = img.UPGRADE_ALL
	UPGRADE_BASE = img.UPGRADE_BASE;  INSTALL = img.INSTALL

	#
	# Identify site containing packages. First site in list having the
	# package is used.
	#
	for sv in img.PKGSITEVARS:
		catf = sv.catfh
		catf.seek(0)

		# All packages already found in an earlier site, so bail
		if len(pkgs) == 0: break

		# Scan catalog for the site
		# After scanning pdict will have the latest version entry from the catalog
		rmlist = []
		for line in catf:
			entry = line.strip().split(" ")

			# Ignore invalid entry format
			if len(entry) != 7: continue
			for name in pkgs:
				if name == entry[CNAMEF] or name == entry[PKGNAMEF]:
					nm = entry[PKGNAMEF]

					# If we are requesting upgrade and package is in
					# base cluster then reset upgrade type to all since
					# we need to create a new boot environment.
					#
					if type == UPGRADE and level == 0 and \
					    sv.base_cluster.has_key(nm):
						type = UPGRADE_ALL
					if pdict.has_key(nm):
						if compare_vers(entry[VERSIONF], \
						    pdict[nm].version) > 0:
							pdict[nm].update(entry, sv)
							continue
					else:
						pdict[nm] = Cl_pkgentry(entry, sv)
						pdict[nm].refername = name
						rmlist.append(name)
		#
		# Remove packages that have already been found
		#
		for name in rmlist:
			pkgs.remove(name)

	if type == UPGRADE_BASE:
		# Check for installed base packages
		for nm in pdict.keys():
			if not os.path.isfile("%s/%s/pkginfo" % (img.INSTPKGDIR, nm)):
				del pdict[nm]

	elif len(pkgs) > 0 and type != UPGRADE_ALL:
		if type == img.LIST_ONLY:
			for pkgn in pkgs:
				pdict[pkgn] = None
		else:
			# Check for packages not found. We ignore this check in upgrade
			# all/base mode since there might be packages in the system that
			# are not from our repo. Those are just retained as-is.
			#
			raise PKGError("ERROR: The following packages not found in any catalog: " + \
		    	' '.join(pkgs))

	# Return if we are only asked to prepare a catalog entry list
	if type == img.LIST_ONLY:
		return type

	deplist = []
	for pkgname in pdict.keys():
		#
		# pdict now has latest versions of all specified packages
		# Now based on what we are doing check for installed packages
		# and versions.
		#
		pkg = pdict[pkgname]

		if os.path.exists("%s/%s" % (img.INSTPKGDIR, pkgname)) or \
		    os.path.exists("%s/%s" % (img.SPKG_GRP_DIR, pkgname)):
			# Package exists
			if type == INSTALL:
				if level == 0:
					# Package specified by user is installed. Crib!
					raise PKGError(_("Package %s already installed" % name))
				else:
					# We are in dependency handling. Ignore installed
					# uptodate packages otherwise upgrade.
					localver = fetch_local_version(img, pkg)
					if compare_vers(localver[0], pkg.version) > 0:
						pdict[pkgname].action = UPGRADE
					else:
						pdict[pkgname].action = img.NONE

			elif type == UPGRADE or type == UPGRADE_BASE or \
			    type == UPGRADE_ALL:
				localver = fetch_local_version(img, pkg)
				if compare_vers(localver[0], pkg.version) > 0:
					pdict[pkgname].action = UPGRADE
				else:
					#print >> sys.stderr, \
					#    "Package %s is up to date\n" % pkgname
					pdict[pkgname].action = img.NONE
					continue
		else:
			if type == INSTALL:
				pdict[pkgname].action = INSTALL

			elif type == UPGRADE or type == UPGRADE_BASE or \
			    type == UPGRADE_ALL:
				if level == 0:
					raise PKGError(_("Package %s is not installed" % name))
				else:
					pdict[pkgname].action = INSTALL

		# TODO: Handle incompatibles
		if pkg.type == "P":
			depends = "%s/%s/%s/depend" % (pkg.sitevars.metadir, pkgname, \
			    pkg.version)
		else:
			depends = "%s/groups/%s/%s/depend" % (pkg.sitevars.metadir, pkgname, \
			    pkg.version)

		# Skip is there is no dependency info
		if not os.path.isfile(depends):
			continue

		depf = open(depends, "r")
		for line in depf:
			if line[0] == "P":
				# Get rid of TABs
				line = line.replace("	", " ")
				de = line.split(" ")

				#
				# Ignore already installed dependencies in base_cluster when
				# installing or when upgrading non-base packages.
				#
				if type == INSTALL or type == UPGRADE:
					if os.path.exists("%s/%s" % (img.INSTPKGDIR, de[1])):
						isbase = 0
						for sv in img.PKGSITEVARS:
							if sv.base_cluster.has_key(\
							    pkg.cname):
								isbase = 1
								break
						if isbase == 1:
							continue

				pdict[pkgname].deplist.append(de[1])
				try:
					i = deplist.index(de[1])
				except ValueError:
					if not pdict.has_key(de[1]):
						deplist.append(de[1])
		depf.close()

	#
	# Recursion to scan the dependency list. Circular dependencies
	# are taken care of by the pdict check above.
	#
	do_build_pkglist(img, deplist, pdict, type, level + 1)

	return type

def build_pkglist(img, pkgs, pdict, type, level):
	"""Wrapper for main do_build_pkglist routine"""

	for sv in img.PKGSITEVARS:
		if not os.path.isfile(sv.catalog):
			updatecatalog(img, [])
		sv.catfh = open(sv.catalog, "r")

	type = do_build_pkglist(img, pkgs, pdict, type, level)

	for sv in img.PKGSITEVARS:
		sv.catfh.close()
		sv.catfh = None

	# Return if we are only asked to prepare a catalog entry list
	if type == img.LIST_ONLY:
		return type

	for pkgname in pdict.keys():
		if not pdict[pkgname]: continue
		if pdict[pkgname].action == img.NONE:
			del pdict[pkgname]

	return type

def install_pkg(img, ent, pkgfile):
	"""Install the given package. pkgfile is a compressed 7Zip datastream package"""

	pkgfileds = pkgfile + ".tmp"
	if ent.type == "P":
		#
		# Standard package
		#
		if img.ALTROOT != "":
			PKGADDFLAGS = "-R %s -n -a %s" % (img.ALTROOT, img.ADMINFILE)
		else:
			PKGADDFLAGS = "-n -a %s" % img.ADMINFILE

		try:
			exec_prog("%s e -so %s > %s" % (img.SZIP, pkgfile, pkgfileds), 0)
		except PKGError, pe:
			os.unlink(pkgfile);  os.unlink(pkgfileds)
			raise PKGError("Failed to decompress package %s\n%s" % \
			    (ent.refername, pe.message))

		try:
			exec_prog("/usr/sbin/pkgadd %s -d %s %s" % \
			    (PKGADDFLAGS, pkgfileds, ent.pkgname), 0)
		except PKGError, pe:
			os.unlink(pkgfile);  os.unlink(pkgfileds)
			raise PKGError("Failed to install package %s" % \
			    (ent.refername, pe.message))

	elif ent.type == "G":
		#
		# A package group
		#
		try:
			exec_prog("%s e -so %s > %s" % (img.SZIP, pkgfile, pkgfileds), 0)
		except PKGError, pe:
			os.unlink(pkgfile);  os.unlink(pkgfileds)
			raise PKGError("Failed to decompress group package %s\n%s" % \
			    (ent.refername, pe.message))

		
		if not os.path.exists(img.SPKG_GRP_DIR):
			os.makedirs(img.SPKG_GRP_DIR)

		try:
			exec_prog("cd %s; /usr/bin/tar xf %s" % \
			    (img.SPKG_GRP_DIR, pkgfileds), 0)
		except PKGError, pe:
			os.unlink(pkgfile);  os.unlink(pkgfileds)
			raise PKGError("Failed to install Group package %s" % \
			    (ent.refername, pe.message))

	os.unlink(pkgfileds)


def create_bootenv(img):
	"""Create a new boot environment using SNAP BE management. img is modified to point to it."""

	num = 0
	out = exec_prog("/usr/sbin/beadm list -H", 1)
	for line in out.split("\n"):
		nm = line.split(":")[0]
		nmlst = nm.split("-")
		if len(nmlst) > 1:
			try:
				num = int(nmlst[1])
			except:
				pass

	num = num + 1
	newbe = "opensolaris-%s" % num
	altroot = "/var/tmp/spkg/%s" % newbe
	if not os.path.exists(altroot):
		os.makedirs(altroot)
	try:
		exec_prog("/usr/sbin/beadm create %s" % newbe, 0)
		exec_prog("/usr/sbin/beadm mount %s %s" % (newbe, altroot), 0)
	except PKGError, pe:
		raise PKGError("Failed to create a new boot environment. Cannot upgrade!\n" + pe.message)

	img.bename = newbe
	img.set_altroot(altroot)

def activate_bootenv(img):
	"""Unmount and activate a bootenv."""

	if img.bename == "":
		raise PKGError("No bootenv exists!")

	try:
		exec_prog("/usr/sbin/beadm unmount %s" % img.bename, 0)
		exec_prog("/usr/sbin/beadm activate %s" % img.bename, 0)
	except PKGerror, pe:
		raise PKGerror("Failed to activate new boot environment " + bars.bename + \
		    ". Use /usr/sbin/beadm to fix.\n " + pe.message)

def uninstall_pkg(img, ent):
	"""Remove the given package."""

	if ent.type == "P":
		if img.ALTROOT != "":
			PKGRMFLAGS = "-R %s -n -a %s" % (img.ALTROOT, img.ADMINFILE)
		else:
			PKGRMFLAGS = "-n -a %s" % img.ADMINFILE

		try:
			exec_prog("/usr/sbin/pkgrm %s %s" % (PKGRMFLAGS, ent.pkgname), 0)
		except PKGError, pe:
			raise PKGError("Failed to uninstall package %s" % \
			    (ent.refername, pe.message))
	else:
		try:
			exec_prog("rm -rf %s/%s" % (img.SPKG_GRP_DIR, ent.pkgname), 0)
		except PKGError, pe:
			raise PKGError("Failed to uninstall Group package %s" % \
			    (ent.refername, pe.message))

def create_plan(img, pargs, action):
	"""Create a TransformPlan that contains a set of package transforms for the given action"""

	pdict = {}
	pkgs = []

	for sv in img.PKGSITEVARS:
		base_cluster = "%s/clusters/base_cluster" % sv.metadir
		if os.path.isfile(base_cluster):
			bfh = open(base_cluster, "r")
			for line in bfh:
				sv.base_cluster[line.strip()] = ""
			bfh.close()

	if action == img.UPGRADE_ALL:
		# Get list of packages installed in system.
		pkgs = map(lambda pkg: pkg.replace(".i", ""), os.listdir(img.INSTPKGDIR))

	elif action == img.UPGRADE_BASE:
		# Build full list of base packages. Stripping out uninstalled base pkgs
		# is handled in build_pkglist.
		#
		bset = set([])
		for sv in img.PKGSITEVARS:
			bset = bset.union(sv.base_cluster.keys())
		pkgs = list(bset)
	else:
		pkgs = pargs

	action = build_pkglist(img, pkgs, pdict, action, 0)

	#
	# We now have a dictionary of the full list of package objects to be installed
	# We now need to build a partial dependency dict and do a topological sort on
	# that to get the proper order of installation.
	#
	graphdict = {}
	for name, entry in pdict.iteritems():
		for dep in entry.deplist:
			if not pdict.has_key(dep):
				continue
			if graphdict.has_key(dep):
				graphdict[dep].append(name)
			else:
				graphdict[dep] = [name]

	#
	# Add circular self depdencies for packages with no deps listed otherwise the
	# topo sort complains. These circular deps are properly handled.
	#
	for name in pdict.keys():
		if not graphdict.has_key(name):
			graphdict[name] = [name]

	sorted_list = tsort.robust_topological_sort(graphdict)
	tplan = TransformPlan(img, pdict, sorted_list, action)

	return tplan

def execute_plan(tplan, downloadonly):
	"""Perform package actions as per the given Transform Plan"""

	num = len(tplan.pdict.keys())
	img = tplan.img

	if downloadonly != 1:
		if tplan.action == img.INSTALL:
			print "------------------------------------------------"
			print "Will be installing %d packages" % num
			print "------------------------------------------------"
			print ""
		elif tplan.action == img.UPGRADE or tplan.action == img.UPGRADE_BASE or \
		    tplan.action == img.UPGRADE_ALL:
			print "------------------------------------------------"
			print "Will be upgrading %d packages" % num
			print "------------------------------------------------"
			print ""

	print "** Downloading packages\n"
	#
	# First download all the files and verify checksums. verify_sha1sum raises
	# and exception if checksum verification fails.
	#
	download_packages(tplan)

	if downloadonly == 1:
		print "** Download complete\n"
		return ret

	print "** Installing/Upgrading packages\n"
	print tplan.sorted_list

	# Now perform all the install actions
	for titem in tplan.sorted_list:
		for pkgname in titem:
			ent = tplan.pdict[pkgname]
			if ent.action == img.INSTALL:
				install_pkg(img, ent, ent.dwn_pkgfile)
				os.unlink(ent.dwn_pkgfile)
			elif ent.action == img.UPGRADE:
				uninstall_pkg(img, ent)
				install_pkg(img, ent, ent.dwn_pkgfile)

	print "\n** Installation/Upgrade Complete\n"

def download_packages(tplan):
	"""Download all packages in mentioned in the transform plan"""

	img = tplan.img
	for titem in tplan.sorted_list:
		for pkgname in titem:
			ent = tplan.pdict[pkgname]
			if ent.action != img.INSTALL and ent.action != img.UPGRADE:
				continue
			pkgurl = "%s/%s/%s/%s" % \
			    (ent.sitevars.fullurl, img.ARCH, img.OSREL, ent.pkgfile)
			tfile = "%s/%s" % (img.SPKG_DWN_DIR, ent.pkgfile)
			ent.dwn_pkgfile = tfile

			#
			# If the file is already downloaded then check the sha1sum
			#
			verify = 1
			if os.path.isfile(tfile):
				try:
					print "*** Package %s already downloaded\n" % ent.cname
					print "*** Verifying SHA1 Checksum\n"
					verify_sha1sum(ent, tfile)
					verify = 0
				except:
					print "*** Checksum does not match re-downloading"
					removef(tfile)
					downloadurl(pkgurl, tfile)
			else:
				downloadurl(pkgurl, tfile)

			if verify == 1:
				print "*** Verifying SHA1 Checksum for package %s\n" % ent.cname
				try:
					verify_sha1sum(ent, tfile)
				except:
					print "*** Checksum verification failed. Retrying download"
					removef(tfile)
					downloadurl(pkgurl, tfile)
					verify_sha1sum(ent, tfile)

#
# Main package installation routine
#
def install(img, pargs, downloadonly):
	"""Install one or more packages listed on the command line"""

	if len(pargs) == 0:
		print >> sys.stderr, \
		    "No packages specified to install."
		return

	print "** Computing dependencies and building package list\n"
	#########################################
	# Installation plan creation phase
	#########################################
	tplan = create_plan(img, pargs, img.INSTALL)
	if not tplan:
		return 1
	#########################################
	# End of Installation plan creation phase
	#########################################

	execute_plan(tplan, downloadonly)

	return 0

def upgrade(img, pargs):
	"""Upgrade specified packages or upgrade entire system"""

	if len(pargs) == 0:
		print >> sys.stderr, \
		    "No packages specified to upgrade."
		return

	if pargs[0] == "base":
		tplan = create_plan(img, pargs, img.UPGRADE_BASE)

	elif pargs[0] == "all":
		tplan = create_plan(img, pargs, img.UPGRADE_ALL)
	else:
		tplan = create_plan(img, pargs, img.UPGRADE)

	if tplan.action == img.UPGRADE_BASE or tplan.action == img.UPGRADE_ALL:
		create_bootenv(img)

	execute_plan(tplan, 0)

	if tplan.action == img.UPGRADE_BASE or tplan.action == img.UPGRADE_ALL:
		# Update release tag on boot environment
		rel = os.environ["USE_RELEASE_TAG"]
		try:
			tf = open("%s/etc/release_tag", "w")
			tf.write(rel)
			tf.close()
		except:
			traceback.print_exc()
			print ""
			print "WARNING: Unable to update /etc/release_tag in new boot env."
			print "         Please put '%s' into that file after reboot" % rel
			print "         or set this value for USE_RELEASE_TAG in /etc/spkg.conf"
			print ""
		activate_bootenv(img)
		print "Upgrade SUCCESSFUL. Upgraded system will be available on next reboot"
		print ""
	else:
		print "Upgrade SUCCESSFUL."
		print ""

	return 0

def available(img, pargs):
	"""List latest versions and descriptions of available packages in all catalogs."""

	if len(pargs) > 0 and pargs[0] == "-r":
		# List all releases
		relf = open(img.RELEASES_LIST, "r")

		print ""
		print "######################################################"
		print "# Listing current distro releases in descending order"
		print "######################################################"
		print "%20s   %20s" % ("Release Name", "Tag")
		print "------------------------------------------------------"
		print "%20s   %20s" % ("Latest Head", "trunk")
		for line in relf:
			name, tag = line.strip().split(":")
			print "%20s   %20s" % (name, tag)
		print "######################################################\n"
		relf.close()
		return 0

	pdict = {}
	pipe = Popen("/usr/bin/less", stdin=PIPE, close_fds=False)
	out = pipe.stdin
	for sv in img.PKGSITEVARS:
		catf = open(sv.catalog, "r")

		# depends = "%s/%s/%s/depend" % (pdict[pkgname].sitevars.metadir, \
		#    pkgname, pdict[pkgname].version)

		ioerr = 0
		try:
			print >> out, "############################################################################"
			print >> out, "# Showing packages from site %s" % sv.site
			print >> out, "############################################################################"

			nm1 = ""
			version = ""
			pkgname = ""
			type = "P"
			origversion = ""

			for line in catf:
				line = line.strip()
				entry = line.split(" ")
				if len(entry) != 7: continue

				nm = entry[img.CNAMEF]
				if len(nm1) == 0:
					nm1 = nm
					version = entry[img.VERSIONF]
					origvers = entry[img.ORIGVERSF]
					pkgname = entry[img.PKGNAMEF]
					type = entry[img.TYPEF]

				elif nm != nm1:
					# Extract description from pkginfo
					desc = fetch_metainfo_fields(sv, pkgname, \
					    version, type, ["DESC"])

					print >> out, "%33s: %s\n%33s  %s\n" % \
					    (nm1, desc[0], " ", origver)
					nm1 = nm
					version = entry[img.VERSIONF]
					origvers = entry[img.ORIGVERSF]
					pkgname = entry[img.PKGNAMEF]

				elif compare_vers(entry[img.VERSIONF], version) > 0:
					version = entry[img.VERSIONF]
					origvers = entry[img.ORIGVERSF]
		except IOError, ie:
			ioerr = 1
			if ie.errno == 32:
				pass
			else:
				raise ie
		catf.close()

		if ioerr == 0:
			print >> out, "############################################################################"
			print >> out, "# End of packages from site %s" % sv.site
			print >> out, "############################################################################"

	pipe.stdin.close()
	pipe.wait()

	return 0

def compare(img, pargs):
	"""Compare installed packages with ones in the preferred catalogs"""

	bold = "\033[1m"
	reset = "\033[0;0m"

	pipe = Popen("/usr/bin/less", stdin=PIPE, close_fds=False)
	out = pipe.stdin
	for sv in img.PKGSITEVARS:
		catf = open(sv.catalog, "r")

		ioerr = 0
		pdict = {}
		try:
			print >> out, "############################################################################"
			print >> out, "# Processing packages from site %s" % sv.site
			print >> out, "############################################################################"
			print >> out, "%33s %35s %s\n" % ("Package Name", "Local Vers", "Avail Vers")
			for line in catf:
				line = line.strip()
				entry = line.split(" ")
				if len(entry) != 7: continue

				#
				# Skip if this entry was already compared earlier
				#
				nm = entry[img.CNAMEF]
				if pdict.has_key(nm):
					continue

				pdict[nm] = ""
				pkgname = entry[img.PKGNAMEF]
				type = entry[img.TYPEF]

				#
				# We want the latest pkg revision here.
				# Current symlink in the pkg's metainfo dir always points to the
				# latest version, so we cheat via readlink.
				#
				curr = "%s/%s/current" % (sv.metadir, pkgname)
				version = os.readlink(curr).strip()
				fields = fetch_metainfo_fields(sv, pkgname, version, \
				    type, ["VERSION", "DESC"])
				verstr = fields[0].replace(",REV=", "(") + ")"
				desc = fields[1]

				if os.path.exists("%s/%s" % (img.INSTPKGDIR, pkgname)) or \
				    os.path.exists("%s/%s" % (img.SPKG_GRP_DIR, pkgname)):
					localver = fetch_local_version(img, 
					    Cl_pkgentry(entry, sv))
					lv = localver[1].replace("VERSION=", "").replace(",REV=", "(") + ")"

					try:
						cmp = compare_vers(version, localver[0])
					except InvalidOperation, inv:
						print >> out, traceback.format_exc()
						print >> out, "%s, %s" % (version, localver[0])
						ioerr = 1

					if cmp <= 0:
						print >> out, "%34s: %s\n%34s: %s\n" % \
						    (nm, desc, lv, verstr)

					elif cmp > 0:
						print >> out, "%34s: %s\n%34s: %s\n" % \
						    ("*" + nm, desc, lv, verstr)
				else:
					print >> out, "%34s: %s\n%34s: %s\n" % \
					    (nm, desc, "(Not Installed)", verstr)

		except IOError, ie:
			ioerr = 1
			if ie.errno == 32:
				pass
			else:
				print >> out, traceback.format_exc()
		except:
			print >> out, traceback.format_exc()
			ioerr = 1

		if ioerr == 0:
			print >> out, "############################################################################"
			print >> out, "# End of packages from site %s" % sv.site
			print >> out, "############################################################################"

	pipe.stdin.close()
	pipe.wait()
	return 0

def download(img, pargs):
	"""Only download packages do not install."""

	#
	# Call install with the download flag set. It will cause the package tree
	# to be resolved and downloaded but not installed.
	#
	ret = install(img, pargs, 1)
	return ret

def dump_pkginfo(pkg, pkginfile, out, installed, short):
	"""Dump package info for the given package."""

	vf = open(pkginfile, "r")
	cont = {}
	for line in vf:
		ent = line.strip().split("=")
		if ent[0] == "VERSION":
			ent[1] = "=".join(ent[1:])
		cont[ent[0]] = ent[1]
	vf.close()

	if pkg:
		cname = pkg.cname
		pkgname = pkg.pkgname
	else:
		cname = cont["PKG"]
		pkgname = cname

	if short:
		print >> out, " %20s : %s" % ("Common Name", cname)
		print >> out, " %20s : %s" % ("Description", cont["DESC"])
	else:
		print >> out, " %20s : %s" % ("Common Name", cname)
		print >> out, " %20s : %s" % ("Package Name", pkgname)
		print >> out, " %20s : %s" % ("Description", cont["DESC"])
		print >> out, " %20s : %s" % ("Version", cont["VERSION"])
		if installed:
			print >> out, " %20s : %s" % ("Installed", "Yes")
			print >> out, " %20s : %s" % ("Install Date", cont["INSTDATE"])
		else:
			print >> out, " %20s : %s" % ("Installed", "No")
		print >> out, " %20s : %s" % ("Category", cont["CATEGORY"])
		print >> out, " %20s : %s" % ("Vendor", cont["VENDOR"])
	print >> out, ""

def info(img, pargs):
	"""Display package information. Works for both installed and not-installed packages."""

	allinst = 0
	short = False

	if len(pargs) > 0:
		if pargs[0] == '-s':
			short = True
			del pargs[0]

	if len(pargs) == 0:
		# Get list of packages installed in system.
		pkgs = map(lambda pkg: pkg.replace(".i", ""), os.listdir(img.INSTPKGDIR))
		allinst = 1
	else:
		pkgs = pargs

	pdict = {}
	build_pkglist(img, pkgs, pdict, img.LIST_ONLY, 0)

	if sys.stdout.isatty():
		pipe = Popen("/usr/bin/less", stdin=PIPE, close_fds=False)
		out = pipe.stdin
	else:
		pipe = None
		out = sys.stdout

	print >> out, "############################################################################"
	if allinst == 1:
		print >> out, "# Listing all installed packages"
		print >> out, "############################################################################"

	try:
		for pn in pdict.keys():
			pkg = pdict[pn]
			if pkg:
				if pkg.type == "P":
					pkginfile = "%s/%s/pkginfo" % (img.INSTPKGDIR, pkg.pkgname)
				else:
					pkginfile = "%s/%s/pkginfo" % (img.SPKG_GRP_DIR, pkg.pkgname)
			else:
				pkginfile = "%s/%s/pkginfo" % (img.INSTPKGDIR, pn)
				if not os.path.exists(pkginfile):
					print >> out, "!"
					print >> out, "! Package %s not found" % pn
					print >> out, "!"
					print >> out, ""
					continue
	
			if allinst == 1:
				dump_pkginfo(pkg, pkginfile, out, True, short)
			else:
				if os.path.exists(pkginfile):
					dump_pkginfo(pkg, pkginfile, out, True, short)
				else:
					if pkg.type == "P":
						pkginfile = "%s/%s/%s/pkginfo" % \
				    		    (pkg.sitevars.metadir, pkg.pkgname, pkg.version)
					else:
						pkginfile = "%s/groups/%s/%s/pkginfo" % \
				    		    (pkg.sitevars.metadir, pkg.pkgname, pkg.version)
					dump_pkginfo(pkg, pkginfile, out, False, short)
	except IOError, ie:
		if ie.errno == 32:
			pass
		else:
			raise ie

	if pipe:
		pipe.stdin.close()
		pipe.wait()

	return 0

def init(img, pargs):
	"""Initialize a directory to be an alternate root image."""

	if len(pargs) < 1:
		raise PKGError(_("No directory provided to initialize."))

	altroot = pargs[0]
	img.init(altroot)
	updatecatalog(img, [])

def dump_pkgcontents(out, name, pkgmapfile, long_listing):
	"""Dump the package pathnames for the given package."""

	#
	# Contents of the pkgmap file are dumped
	#
	try:
		pmf = open(pkgmapfile, "r")
	except:
		print >> out, "!"
		print >> out, "! Error fetching package contents for %s " % name
		print >> out, "!"
		print >> out, traceback.format_exc()
		return

	types = {"d":"dir", "s":"symlink", "l":"hardlink", "f":"file", "e":"file", "v":"file"}
	print >> out, "---------------------------------------------------------------"
	print >> out, "- Package contents for %s " % name
	print >> out, "---------------------------------------------------------------"
	for line in pmf:
		entry = line.strip().split(" ")
		if entry[0] == ":" or entry[1] == "i": continue

		if entry[1] == "s":
			fl = entry[3].replace("=", " -> ")
			if long_listing:
				print >> out, "type = %s" % types[entry[1]]
			print >> out, fl
		else:
			if long_listing:
				print >> out, \
				    "type = %s, perms = %s, owner = %s, group = %s" % \
				    (types[entry[1]], entry[4], entry[5], entry[6])
			print >> out, entry[3]
		if long_listing:
			print >> out, ""
	pmf.close()


def contents(img, pargs):
	"""List all pathnames from the given package[s]."""

	long_listing = False
	pl = len(pargs)

	if pl > 0:
		if pargs[0] == "-l":
			long_listing = True
			del pargs[0]

	if len(pargs) < 1:
		raise PKGError(_("No packages provided to show contents"))

	pkgs = pargs
	pdict = {}
	build_pkglist(img, pkgs, pdict, img.LIST_ONLY, 0)

	if sys.stdout.isatty():
		pipe = Popen("/usr/bin/less", stdin=PIPE, close_fds=False)
		out = pipe.stdin
	else:
		pipe = None
		out = sys.stdout

	try:
		for pn in pdict.keys():
			pkg = pdict[pn]
			name = ""

			#
			# First see if this is a Group package
			#
			if pkg and pkg.type == "G":
				print >> out, ">"
				print >> out, "> This is a group package."
				print >> out, ">"
				print >> out, ""
				continue

			#
			# Now check for the pkgmap file in pspool area. This area
			# is set up to support Zones in SVR4 packaging. This allows
			# showing contents for third-party packages not in our catalogs.
			# If the package is not installed then the pkgmap is fetched
			# from /var/spkg/metadir...
			# However if the package is not in our catalogs and not installed
			# then of course we have to dump a not found message for that
			# package.
			#
			if pkg:
				pkgmapfile = "%s/%s/save/pspool/%s/pkgmap" % \
				    (img.INSTPKGDIR, pkg.pkgname, pkg.pkgname)
				if not os.path.exists(pkgmapfile):
					pkgmapfile = "%s/%s/%s/pkgmap" % \
				    (pkg.sitevars.metadir, pkg.pkgname, pkg.version)
				name = pkg.cname
			else:
				pkgmapfile = "%s/%s/save/pspool/%s/pkgmap" % \
				    (img.INSTPKGDIR, pn, pn)
				if not os.path.exists(pkgmapfile):
					print >> out, "!"
					print >> out, "! Package %s not found" % pn
					print >> out, "!"
					print >> out, ""
					continue
				name = pn

			dump_pkgcontents(out, name, pkgmapfile, long_listing)

	except IOError, ie:
		if ie.errno == 32:
			pass
		else:
			raise ie

	if pipe:
		pipe.stdin.close()
		pipe.wait()

def search(img, pargs):
	"""Perform content or catalog searches"""

	if len(pargs) < 1:
		raise PKGError(_("No arguments to search!"))

	ignorecase = False
	for arg in pargs:
		if arg == "-i":
			ignorecase = True
			pargs.remove(arg)

	if ignorecase:
		mtch = re.compile(pargs[0], re.IGNORECASE)
	else:
		mtch = re.compile(pargs[0])
	out = sys.stdout
	for sv in img.PKGSITEVARS:
		if not os.path.isfile(sv.catalog):
			updatecatalog(img, [])
		for pkg in searchcatalog(sv, mtch, -1):
			pkginfile = "%s/%s/%s/pkginfo" % \
			    (pkg.sitevars.metadir, pkg.pkgname, pkg.version)
			dump_pkginfo(pkg, pkginfile, out, False, False)

def do_main():
	"""Main entry point."""
	gettext.install("spkg", "/usr/lib/locale");

	ret = 0
	use_site = ""

	try:
		opts, pargs = getopt.getopt(sys.argv[1:], "s:R:r:")
	except getopt.GetoptError, e:
		print >> sys.stderr, \
		    _("spkg: illegal global option -- %s") % e.opt
		usage()

	if pargs == None or len(pargs) == 0:
		usage()
		sys.exit(2)

	subcommand = pargs[0]
	del pargs[0]

	if subcommand == "init":
		ret = init(img, pargs)
		return ret

	ALTROOT = ""
	for opt, arg in opts:
		if opt == "-R":
			ALTROOT = arg
		elif opt == "-r":
			os.environ["USE_RELEASE_TAG"] = arg
		elif opt == "-s":
			use_site = arg

	if os.environ.has_key("ALTROOT"):
		ALTROOT = os.environ["ALTROOT"]

	if ALTROOT != "":
		if not os.path.isfile(ALTROOT + '/etc/spkg.conf') or \
		    not os.path.isfile(ALTROOT + '/var/spkg/admin'):
			print >> sys.stderr, \
			    _("'%s' is not a valid Alternate Root image") % img.ALTROOT
			return 1
		img.set_altroot(ALTROOT)

	#
	# For certain upgrade options we need to set the release_tag to the one
	# we are upgrading to prior to load_config
	#
	if subcommand == "upgrade":
		if len(pargs) != 2:
			usage()
			sys.exit(1)

		if pargs[0] == "core" or pargs[0] == "all":
			os.environ["USE_RELEASE_TAG"] = pargs[1]

	load_config(use_site)

	if subcommand == "updatecatalog":
		ret = updatecatalog(img, pargs)
	elif subcommand == "install":
		ret = install(img, pargs, 0)
	elif subcommand == "upgrade":
		ret = upgrade(img, pargs)
	elif subcommand == "available":
		ret = available(img, pargs)
	elif subcommand == "compare":
		ret = compare(img, pargs)
	elif subcommand == "download":
		ret = download(img, pargs)
	elif subcommand == "describe":
		ret = describe(img, pargs)
	elif subcommand == "info":
		ret = info(img, pargs)
	elif subcommand == "contents":
		ret = contents(img, pargs)
	elif subcommand == "search":
		ret = search(img, pargs)
	else:
		print >> sys.stderr, \
		    "spkg: unknown subcommand '%s'" % subcommand

	return ret

