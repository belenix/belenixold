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
import cPickle
#from stat import *
from subprocess import Popen, PIPE, STDOUT
from urlparse import urlparse
from decimal import Decimal

class Cl_pkgentry(object):
	"""Class that holds all fields of a package entry in the catalog including site related entries.
	   This is essentially a package object representation."""

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
		self.version_given = False
		self.actionrecord = ""
		self.dependfile = ""
		self.pkginfile = ""

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
		self.catalog_tm = "%s/.catalog-%s-%s" % (SPKG_VAR_DIR, RELEASE, so[1])
		self.mirrors = "%s/mirrors-%s" % (SPKG_VAR_DIR, so[1])
		self.metadir = "%s/metainfo-%s" % (SPKG_VAR_DIR, so[1])
		self.base_cluster = None
		self.axel_mirror_prefix = ""
		self.tcat = "%s/catalog" % SPKG_VAR_DIR
		self.tmeta = "%s/metainfo.tar.7z" % SPKG_VAR_DIR
		self.tmetadir = "%s/metainfo" % SPKG_VAR_DIR
		self.catfh = None

class Cl_img(object):
	"""Class that holds some globally used values."""
	def __init__(self):
		# Hardcoded for now
		self.cnffile = "/etc/spkg.conf"
		self.cnffile_master = "/var/spkg/spkg.conf"

		self.ALTROOT = ""
		self.RTYPE = "unstable"
		self.PKGSITES = ["http://pkg.belenix.org"]
		self.PKGADDFLAGS = ""
		self.SPKG_PRESERVE_DOWNLOADS = False
		self.USE_GPG = True
		self.USE_MD5 = True
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
		self.uninst_type = 0  # 0 - simple, 1 - recursive
		self.cnames = {}

		# Fields numbers in a catalog entry for a package
		self.CNAMEF = 0; self.VERSIONF = 1
		self.PKGNAMEF = 2; self.PKGFILEF = 3
		self.MD5SUMF = 4; self.ORIGVERSF = 5
		self.TYPEF = 6

		# Action codes for packages
		self.NONE = 0
		self.INSTALL = 1; self.UPGRADE = 2
		self.UPGRADE_BASE = 3; self.UPGRADE_ALL = 4
		self.UNINSTALL = 5; self.LIST_ONLY = 6

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

	def __init__(self, img, pdict, sorted_list, action, num):
		self.img = img
		self.pdict = pdict
		self.sorted_list = sorted_list
		self.action = action
		self.num = num

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
	                Install one or more packages or group packages
	uninstall [-d]  <package names>
	                Uninstall one or more packages or group packages.
	                With '-d' this action also removes dependencies of these
	                packages if no other packages depend on them and they were
	                not explicitly installed by user.

	upgrade [<Upgrade Type> <release tag>]|[<package list>]
	                Upgrades already installed packages if possible
	                Upgrade type can be one of:
	                core - Upgrade the core distro (Kernel, core libs etc.)
	                all - Upgrade the entire distribution.

	                release tag - The distro release to upgrade to for core or all.

	available [-r|-g]  Lists the available packages in all sites
                        With '-r' flag lists all the current distro releases available.
                        With '-g' flag lists all group packages available.

	compare         Shows installed package versions vs available
	info [-s|-d|-D] [<pkg list>]
	                List information about packages whether installed or not
	                With '-s' display a short listing of only package descriptions.
	                With '-d' list the packages on which the specified packages
	                depend.
	                With '-D' list the packages which depend on the specified packages.

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
	-v                   Verbose output
	-n                   Prepare action plan and print it. Do not actually perform the
	                     the action.

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

	logv(_("Executing " + cmd))
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

def depend_entries(depfile, types):
	"""A generator that allows iterating over lines in a depend file.
	   Takes care of empty and commented lines and translating TABs to
	   spaces."""
	for line in depfile:
		line = line.strip()
		if line == "" or line[0] not in types:
			continue

		# Get rid of TABs
		line = line.replace("	", " ")
		yield line.split(" ")

def load_config(use_site):
	"""Load configuration file and also detect environment settings."""

	com = re.compile("^#")

	logv(_("Loading configuration"))
	if os.environ.has_key("USE_RELEASE_TAG"):
		use_release = os.environ["USE_RELEASE_TAG"]
	else:
		use_release = ""

	#
	# /etc/spkg.conf is not delivered by the package to avoid overwriting modifications
	# when the package is upgraded/reinstalled. It is created from a default config
	# for the first time.
	#
	if not os.path.exists(img.cnffile):
		shutil.copyfile(img.cnffile_master, img.cnffile)

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

	logv(_("Loading common names"))
	# Load the package name to common name mappings
	cf = open("%s/cnames.pickle" % img.SPKG_VAR_DIR)
	img.cnames = cPickle.load(cf)
	cf.close()

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
# Axel is used to do concurrent chunked download of a file from multiple
# mirrors. Wget is used as a fallback in case Axel was not found.
#
def downloadurl(sv, url, targ, use_mirror=True):
	"""Use a downloader to fetch the given URL. Return the size or -1 for error."""

	if not AXEL_FOUND:
		wgetopts = "-c -O %s" % targ
	if url[:7] == "file://":
		fl = url[8:]
		if not os.path.isfile(fl):
			raise PKGError("ERROR: file %s does not exist" % fl)
		shutil.copyfile(fl, targ)
	elif url[:6] == "ftp://" and not AXEL_FOUND:
		wgetopts = "-O %s --passive-ftp" %targ

	if not AXEL_FOUND:
		if not S__NOEXEC:
			out = exec_prog("%s %s %s" % (WGET, wgetopts, url), 0)
		else:
			print "*** Will execute %s %s %s" % (WGET, wgetopts, url)
	else:
		axel_opts = ""
		# If the site defines mirrors then prepare 
		if sv.axel_mirror_prefix == "" and os.path.exists(sv.mirrors):
			mh = open(sv.mirrors)
			sv.axel_mirror_prefix = '{' + sv.site
			for line in mh:
				sv.axel_mirror_prefix += ',' + line.strip()
			mh.close()
			sv.axel_mirror_prefix += '}'

		#
		# Use only 2 concurrent streams per mirror. We want to be nice!
		# Axel automatically ignores mirrors not having the file.
		#
		if use_mirror and sv.axel_mirror_prefix != "":
			murl = url.replace(sv.site, "").strip("/")
			axel_opts = "-a -n 2 -o %s %s/%s" % \
			    (targ, sv.axel_mirror_prefix, murl)
		else:
			axel_opts = "-a -n 2 -o %s %s" % (targ, url)
		if not S__NOEXEC:
			out = exec_prog("%s %s" % (AXEL, axel_opts), 0)
		else:
			print "*** Will execute %s %s" % (AXEL, axel_opts)
	if not S__NOEXEC:
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
# Check for package names having versions of the form <package name>@<version string>
# <version string> must be of the folowing form: <version number>(<revision string>)
# Ths version string is converted into the normalized form using compute_version
# The regular expression below allows empty revision strings.
#
vre = re.compile("([^\( ]+)\({0,1}([^\( ]*)\){0,1}")

def normalize_versions(pkgs):
	"""Normalize user-speficied package version strings"""

	logv(_("Normalizing package versions"))
	npkgs = []
	for pn in pkgs:
		if pn.find('@') > -1:
			pkgn, vers = pn.split("@", 1)
			vl = vre.findall(vers)
			if len(vl) < 1 or len(vl[0]) < 1:
				raise PKGError(_("Invalid package version string " + pn))
			vers = compute_version("VERSION=" + vl[0][0] + ",REV=" + vl[0][1])
			npkgs.append([pkgn, vers, pn])
		else:
			npkgs.append(pn)
	return npkgs

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
			vf.close()
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

def pkgname_is_installed(pkgname, img):
	"""Return True if the given package name is installed in the given image.
	   The pkgname parameter is the package name, Not common name."""

	return os.path.exists("%s/%s" % (img.INSTPKGDIR, pkgname)) or \
	    os.path.exists("%s/%s" % (img.SPKG_GRP_DIR, pkgname))

def pkg_is_installed(pkg, img):
	"""Return True if the given package object is installed in the given image.
	   This checks both name and version, if version is non-empty."""

	installed = pkgname_is_installed(pkg.pkgname, img)
	if not installed:
		return False

	elif pkg.version != "":
		# Check if the specific version is installed
		cmp = 0
		localver = fetch_local_version(img, pkg)
		try:
			cmp = compare_vers(pkg.version, localver[0])
		except InvalidOperation, inv:
			cmp = -1
			pass;
		if cmp != 0:
			installed = False

	return installed

def logv(msg):
	"""Print messages if verbose output was selected"""
	if S__VERBOSE:
		print msg

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
	return matches

def update_cname_mappings(catfile, cnames):
	"""Update mappings dictionary that maps package name to common name."""
	
	catf = open(catfile, "r")
	CNAMEF = img.CNAMEF;  PKGNAMEF = img.PKGNAMEF

	for line in catf:
		entry = line.strip().split(" ")

		# Ignore invalid entry format
		if len(entry) != 7: continue
		cnames[entry[PKGNAMEF]] = entry[CNAMEF]
	catf.close()

def put_timestamp(fl):
	"""Dump the current timestamp into the given file."""
	fh = open(fl, "w")
	fh.write(str(time.time()))
	fh.close()

#
# Download catalogs and package metadata for all configured sites
#
def updatecatalog(img, pargs, ignore_errors=False):
	"""Refresh catalogs and other metadata for all sites."""

	failed_sites = []
	errored = 0
	releases_found = False
	cnames = {}

	#
	# We do not use mirrored downloads for catalog updates so we pass the False
	# parameter to downloadurl.
	#
	for sv in img.PKGSITEVARS:

		#
		# The releases file provides a list of distro releases. A valid releases
		# file found in the first site is used.
		#
		if not releases_found:
			# Now try to fetch the releases file
			removef(img.RELEASES_LIST)
			sz = 0
			try:
				downloadurl(sv, "%s/trunk/releases" % sv.site, \
				    img.RELEASES_LIST, False)
				releases_found = True
			except PKGError, pe:
				removef(img.RELEASES_LIST)

		#
		# Now try to fetch the catalog only if it has changed
		#
		removef(sv.tcat)
		try:
			downloadurl(sv, "%s/%s/%s/catalog-sha1sum" % \
			    (sv.fullurl, img.ARCH, img.OSREL), sv.tcat, False)
			sf = open(sv.tcat, "r")
			rsum = sf.read().strip();  sf.close()
			removef(sv.tcat)
			lsumfile = "%s-sha1sum" % sv.catalog
			if os.path.exists(lsumfile):
				sf = open("%s-sha1sum" % sv.catalog, "r")
				lsum = sf.read().strip();  sf.close()
			else:
				lsum = ""
			if lsum != rsum:
				downloadurl(sv, "%s/%s/%s/catalog" % \
				    (sv.fullurl, img.ARCH, img.OSREL), sv.tcat, False)
			else:
				put_timestamp(sv.catalog_tm)
				print ""
				print "*** Catalog for site %s is up to date" % sv.site
				print ""
				continue
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
		sf = open("%s-sha1sum" % sv.catalog, "w")
		sf.write(rsum)
		sf.close()
		update_cname_mappings(sv.catalog, cnames)

		#
		# Try to fetch the metainfo. This is required
		#
		removef(sv.tmeta)
		try:
			downloadurl(sv, "%s/trunk/%s/%s/%s/metainfo.tar.7z" % \
			    (sv.site, img.RTYPE, img.ARCH, img.OSREL), \
			    sv.tmeta, False)
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
			    (SZIP, sv.tmeta, img.SPKG_VAR_DIR), 0)
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
		put_timestamp(sv.catalog_tm)

		#
		# Try to fetch mirrors list for site, if any
		#
		removef(sv.mirrors)
		try:
			downloadurl(sv, "%s/mirrors" % sv.site, sv.mirrors, False)
		except PKGError:
			removef(sv.mirrors)

	#
	# Write cname mappings in binary pickled representation
	#
	mapfile = open("%s/cnames.pickle" % img.SPKG_VAR_DIR, "w")
	cPickle.dump(cnames, mapfile, 2)
	mapfile.close()

	if errored == 1:
		if not ignore_errors:
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

def check_catalog(img):
	"""Check the catalog's age and if it is older than 15 days then
	   check for an update."""

	update_needed = False
	for sv in img.PKGSITEVARS:
		curtime = time.time()
		fh = open(sv.catalog_tm, "r")
		mtime = float(fh.read().strip())
		fh.close()

		# Older than 15 days ?
		if curtime - mtime > 1296000:
			update_needed = True
			break
	if update_needed:
		ret = 1
		try:
			ret = updatecatalog(img, None, True)
		except:
			pass
		# Failed to update ? Issue warning if older than 30 days
		if ret == 1 and curtime - mtime > 2592000:
			print ""
			print "WARNING: Catalogs older than 30 days. Failed to" \
			    " auto-update.\nPlease run spkg updatecatalog while" \
			    " connected to the net."
			print ""

def load_inverse_deps(img):
	"""Scan dependencies of installed packages and build an inverse
	   dependency table. A pickled representation is used for speed
	   unless some package operations have happened. In that case the
	   table is re-generated."""

	# Fast path, load a pre-generated pickled invdeps table.
	invdep_pkl_file = os.path.join(img.SPKG_VAR_DIR, "invdeps.pickle")
	if os.path.exists(invdep_pkl_file):
		pkl_mtime = os.path.getmtime(invdep_pkl_file)
		pkgdir_mtime = os.path.getmtime(img.INSTPKGDIR)
		if pkl_mtime >= pkgdir_mtime:
			print "*** Loading installed package dependencies"
			idepf = open(invdep_pkl_file, "r")
			invdeps = cPickle.load(idepf)
			idepf.close()
			return invdeps

	print "*** Analyzing installed package dependencies"
	# Packages have changed on system so we need to re-generate
	pkgs = os.listdir(img.INSTPKGDIR)
	if os.path.exists(img.SPKG_GRP_DIR):
		pkgs.extend(os.listdir(img.SPKG_GRP_DIR))

	invdeps = {}
	for pkgname in pkgs:
		depends = "%s/%s/install/depend" % (img.INSTPKGDIR, pkgname)
		if not os.path.exists(depends):
			depends = "%s/%s/depend" % (img.SPKG_GRP_DIR, pkgname)
			if not os.path.exists(depends):
				continue
		depf = open(depends, "r")
		for de in depend_entries(depf, ["P"]):
			if not invdeps.has_key(de[1]):
				invdeps[de[1]] = [pkgname]
			else:
				invdeps[de[1]].append(pkgname)
		depf.close()
	idepf = open(invdep_pkl_file, "w")
	cPickle.dump(invdeps, idepf, 2)
	idepf.close()
	return invdeps
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
def do_build_pkglist(img, pkgs, pdict, incompats, type, level):
	"""Build a complete list of packages to be installed/upgraded
	including resolved dependencies"""

	if len(pkgs) == 0:
		if level == 0:
			raise PKGError(_("No packages specified"))
		else:
			return type

	logv(_("Building package list for packages: " + str(pkgs)))
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
	newlist = []
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
			for pkgn in pkgs:
				vers = ""
				if isinstance(pkgn , list):
					name, vers, givenname = pkgn
				else:
					name = pkgn

				if name == entry[CNAMEF] or name == entry[PKGNAMEF]:
					nm = entry[PKGNAMEF]

					# If we are requesting upgrade and package is in
					# base cluster then reset upgrade type to all since
					# we need to create a new boot environment.
					#
					if type == UPGRADE and level == 0 and \
					    sv.base_cluster.has_key(nm):
						print "NOTE: Core package being upgraded. Will" \
						    " create new boot environment."
						type = UPGRADE_ALL

					#
					# If the user provided a specific version string we
					# do an exact match with that version string.
					#
					if vers != "":
						if compare_vers(entry[VERSIONF], vers) == 0:
							pdict[nm] = Cl_pkgentry(entry, sv)
							pdict[nm].refername = givenname
							pdict[nm].version_given = True
							rmlist.append(pkgn)
							newlist.append(nm)
						continue

					if pdict.has_key(nm):
						if compare_vers(entry[VERSIONF], \
						    pdict[nm].version) > 0:
							pdict[nm].update(entry, sv)
							continue
					else:
						pdict[nm] = Cl_pkgentry(entry, sv)
						pdict[nm].refername = name
						rmlist.append(name)
						newlist.append(nm)

						#
						# Record how the package is being brought
						# into the system. At level 0 we are processing
						# user-specified packages. Any other level is
						# dependency processing. This info is needed
						# for recursive uninstall.
						#
						if level == 0:
							pdict[nm].actionrecord = "user"
						else:
							pdict[nm].actionrecord = "dependency"
		#
		# Remove packages that have already been found
		#
		for name in rmlist:
			pkgs.remove(name)

	# Check for packages not found. We ignore this check in upgrade
	# all/base mode since there might be packages in the system that
	# are not from our repo. Those are just retained as-is.
	#
	if len(pkgs) > 0 and type != UPGRADE_ALL and type != UPGRADE_BASE:
		if type == img.LIST_ONLY:
			for pkgn in pkgs:
				pdict[pkgn] = None
		else:
			pkgl1 = [ent[2] for ent in pkgs if isinstance(ent, list)]
			pkgl2 = [ent for ent in pkgs if not isinstance(ent, list)]
			raise PKGError("ERROR: The following packages not found in any catalog: " + \
		    	' '.join(pkgl1) + ' ' + ' '.join(pkgl2))

	# Return if we are only asked to prepare a catalog entry list
	if type == img.LIST_ONLY:
		return type

	deplist = []
	for pkgname in newlist:
		#
		# pdict now has latest versions of all specified packages
		# Now based on what we are doing check for installed packages
		# and versions.
		#
		pkg = pdict[pkgname]

		if pkgname_is_installed(pkgname, img):
			# Package exists
			if type == INSTALL:
				if level == 0 and not pkg.version_given:
					# Package specified by user is installed. Crib!
					raise PKGError(_("Package %s already installed" % name))
				else:
					#
					# We are either in dependency handling or user provided
					# a version string. Ignore installed uptodate packages
					# otherwise upgrade.
					#
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
		for de in depend_entries(depf, ["P", "I"]):
			if de[0] == "P":
				#
				# Ignore already installed dependencies in base_cluster
				# when installing or when upgrading non-base packages.
				# That is if pkg is not in base_cluster and dep is in
				# base_cluster then ignore dep.
				# pkg itself being in base_cluster is not checked here
				# since that is already being checked earlier and type
				# gets changed to UPGRADE_ALL, in that case.
				#
				if (type == INSTALL or type == UPGRADE) and \
				    pkgname_is_installed(de[1], img):
					isbase = 0
					for sv in img.PKGSITEVARS:
						if sv.base_cluster.has_key(de[1]):
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

			elif de[0] == "I":
				# Incompatibles
				if pkgname_is_installed(de[1], img):
					if incompats.has_key(de[1]):
						incompats[de[1]].append(pkg.pkgname)
					else:
						incompats[de[1]] = [pkg.pkgname]
		depf.close()

	#
	# Recursion to scan the dependency list. Circular dependencies
	# are taken care of by the pdict check above.
	#
	do_build_pkglist(img, deplist, pdict, incompats, type, level + 1)

	return type

def build_pkglist(img, pkgs, pdict, incompats, type):
	"""Wrapper for main do_build_pkglist routine"""

	for sv in img.PKGSITEVARS:
		if not os.path.isfile(sv.catalog):
			updatecatalog(img, [])
		sv.catfh = open(sv.catalog, "r")

	pkgs = normalize_versions(pkgs)
	type = do_build_pkglist(img, pkgs, pdict, incompats, type, 0)

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

def build_uninstall_pkglist(img, pkgs, pdict):
	"""Wrapper routine to do preprocessing and call do_build_uninstall_pkglist."""

	for sv in img.PKGSITEVARS:
		if not os.path.isfile(sv.catalog):
			updatecatalog(img, [])
		sv.catfh = open(sv.catalog, "r")

	#
	# Build an inverse dependency dictionary for all installed packages and
	# group packages.
	#
	#invdeps = {}
	#ipkgs = os.listdir(img.INSTPKGDIR)
	#if os.path.exists(img.SPKG_GRP_DIR):
		#ipkgs.extend(os.listdir(img.SPKG_GRP_DIR))

	invdeps = load_inverse_deps(img)

	print "*** Scanning specified packages"
	#
	# Version specified during uninstall has no useful meaning. However if the
	# user does specify a version then it is checked whether that specific
	# version is actually installed.
	#
	pkgs = normalize_versions(pkgs)
	# Check if user has mentioned core packages.
	for pn in pkgs:
		if isinstance(pn, list):
			name, vers, givenname = pn
		else:
			name = pn
			givenname = pn

		# Force simple uninstall if core packages are being removed.
		if sv.base_cluster.has_key(name):
			if img.uninst_type == 1:
				print >> sys.stderr, "WARNING: Core package %s specified." \
				    " Ignoring Recursive uninstall option" % givenname
			img.uninst_type = 0

	do_build_uninstall_pkglist(img, pkgs, pdict, 0)

	#
	# Now figure if any installed packages not in this list depend on any of
	# these packages. When trimming a package that has dependents, it's entire
	# dependency subtree has to be trimmed. We use an iterative approach. We
	# keep deleting "can't be removed elements" from pdict and re-scanning pdict
	# until there are no more elements to be removed.
	#
	recheck = True
	while recheck:
		recheck = False
		trimlist = []
		for pn in pdict.keys():
			# Check if package has dependents
			if invdeps.has_key(pn):
				for dependent in invdeps[pn]:
					#
					# If dependent is not among packages to be removed,
					# this package must be trimmed
					#
					if not pdict.has_key(dependent):
						trimlist.append((pn, dependent))
						recheck = True
						break
		for pn, dependent in trimlist:
			if dependent in img.cnames:
				dependent = img.cnames[dependent]
			print "Can't uninstall %s, package %s depends on it" % \
			    (pdict[pn].refername, dependent)
			del pdict[pn]

	for sv in img.PKGSITEVARS:
		sv.catfh.close()
		sv.catfh = None

def do_build_uninstall_pkglist(img, pkgs, pdict, level):
	"""Build a list of packages to be uninstalled. Packages are uninstalled
	   if no other package depends on them. In addition dependencies are also
	   removed if not other packages depend on them."""

	UNINSTALL = img.UNINSTALL
	CNAMEF = img.CNAMEF;  PKGNAMEF = img.PKGNAMEF

	if len(pkgs) == 0:
		return

	#
	# We need to scan catalogs to find out a variety of package properties
	# and also to resolve common names to actual package names.
	#
	newlist = []
	for sv in img.PKGSITEVARS:
		catf = sv.catfh
		catf.seek(0)

		for line in catf:
			entry = line.strip().split(" ")
			name = ""; ri = -1; i = -1 
			for pn in pkgs:
				i += 1
				vers = ""
				if isinstance(pn , list):
					name, vers, givenname = pn
				else:
					name = pn
					givenname = pn

				if name != entry[CNAMEF] and name != entry[PKGNAMEF]:
					continue

				name = entry[PKGNAMEF]
				pkg = Cl_pkgentry(entry, sv)
				pkg.refername = givenname
				pkg.action = UNINSTALL
				pkg.version = vers

				if not pkg_is_installed(pkg, img):
					print >> sys.stderr, \
					    _("Package %s not installed. " \
					    "Ignoring." % pkg.refername)
				else:
					#
					# Read the package's action record if
					# level > 1.
					#
					if level == 0:
						pkg.actionrecord = "force"
						pdict[name] = pkg
						newlist.append(name)
					else:
						try:
							fh = open("%s/%s/actionrecord" \
							    % (img.INSTPKGDIR,
							    pkg.pkgname), "r")
							rec = fh.read().strip()
							fh.close()
							# Only remove auto-dep pkgs
							if rec == "dependency":
								pkg.actionrecord = rec
								pdict[name] = pkg
								newlist.append(name)
						except IOError:
							#
							# We can't reliably determine
							# how the package came in so we
							# ignore this package.
							#
							pass

						if not pdict.has_key(name):
							print >> sys.stderr, \
							    _("Package %s was not a dependency "\
							    "action. Ignoring." % pkg.refername)
				#
				# We come out at the first sucessful catalog match since
				# we do not need the latest version entry.
				#
				ri = i
				break

			#
			# Delete the entry just found from the given pkg list
			#
			if ri > -1:
				del pkgs[ri]
				if len(pkgs) == 0: break

	#
	# Scan for possible packages not in our catalog. We support
	# uninstalling third-party packages so fake up pkg entries.
	#
	for pn in pkgs:
		vers = ""
		if isinstance(pn , list):
			name, vers, givenname = pn
		else:
			name = pn
			givenname = pn
		entry = [name, vers, name, "", "", vers, "P"]
		pkg = Cl_pkgentry(entry, sv)
		pkg.refername = givenname
		pkg.action = UNINSTALL

		if not pkg_is_installed(pkg, img):
			print >> sys.stderr, _("Package %s not installed. " \
			    "Ignoring." % pkg.refername)
		else:
			pdict[name] = pkg
			newlist.append(name)

	#
	# Now trawl through dependencies 
	#
	deplist = []
	gdeplist = []
	for pkgname in newlist:
		pkg = pdict[pkgname]
		if pkg.type == "P":
			#
			# Do not trawl normal package deps if we are not in
			# recursive mode. Deps of group packages are always
			# trawled since removing a group package by itself
			# without removing actual packages it references makes
			# no sense.
			#
			if img.uninst_type == 0:
				continue
			depends = "%s/%s/install/depend" % (img.INSTPKGDIR, pkgname)
		else:
			depends = "%s/%s/depend" % (img.SPKG_GRP_DIR, pkgname)

		# Skip is there is no dependency info
		if not os.path.isfile(depends):
			continue

		depf = open(depends, "r")
		for de in depend_entries(depf):
			if de[0] == "P":
				#
				# Ignore dependencies in base_cluster even when
				# uninstalling base packages. We want to be safe
				# than sorry!
				#
				if pkgname_is_installed(de[1], img):
					isbase = 0
					for sv in img.PKGSITEVARS:
						if sv.base_cluster.has_key(de[1]):
							isbase = 1
							break
					if isbase == 1:
						continue

				pdict[pkgname].deplist.append(de[1])
				try:
					if pkg.type == "P":
						i = deplist.index(de[1])
					else:
						i = gdeplist.index(de[1])
				except ValueError:
					if not pdict.has_key(de[1]):
						if pkg.type == "P":
							if de[1] not in gdeplist:
								deplist.append(de[1])
						else:
							gdeplist.append(de[1])
							try:
								i = deplist.index(de[1])
								del deplist[i]
							except ValueError:
								pass
		depf.close()

	#
	# Recursion to scan the dependency list. Circular dependencies
	# are taken care of by the pdict check above.
	# We handle Group package and normal package dependencies separately since group
	# package dependencies are special.
	#
	do_build_uninstall_pkglist(img, gdeplist, pdict, 0)
	do_build_uninstall_pkglist(img, deplist, pdict, level + 1)

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
			exec_prog("%s e -so %s > %s" % (SZIP, pkgfile, pkgfileds), 0)
		except PKGError, pe:
			os.unlink(pkgfile);  os.unlink(pkgfileds)
			raise PKGError("Failed to decompress package %s\n%s" % \
			    (ent.refername, pe.message))

		try:
			exec_prog("/usr/sbin/pkgadd %s -d %s %s" % \
			    (PKGADDFLAGS, pkgfileds, ent.pkgname), 0)
			arec = open("%s/%s/actionrecord" % (img.INSTPKGDIR, ent.pkgname), "w")
			arec.write(ent.actionrecord)
			arec.close()
		except PKGError, pe:
			os.unlink(pkgfile);  os.unlink(pkgfileds)
			raise PKGError("Failed to install package %s" % \
			    (ent.refername, pe.message))

	elif ent.type == "G":
		#
		# A package group
		#
		try:
			exec_prog("%s e -so %s > %s" % (SZIP, pkgfile, pkgfileds), 0)
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

def create_plan(img, pargs, incompats, action):
	"""Create a TransformPlan that contains a set of package transforms for the given action"""

	pdict = {}
	pkgs = []

	for sv in img.PKGSITEVARS:
		if not sv.base_cluster:
			sv.base_cluster = {}
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
		#
		# Build full list of base packages stripping out uninstalled base pkgs.
		# Some additional base packages might be brought in as part of upgrade
		# via new dependencies.
		#
		bset = set([])
		for sv in img.PKGSITEVARS:
			bset = bset.union(sv.base_cluster.keys())

		#
		# Check for base packages not installed. We do not want to bring in
		# not installed base packages as part of the upgrade process unless
		# they are new deps found in build_pkglist.
		#
		pkgs = [nm for nm in bset if pkgname_is_installed(nm, img)]
	else:
		pkgs = pargs

	if action == img.UNINSTALL:
		build_uninstall_pkglist(img, pkgs, pdict)
	else:
		action = build_pkglist(img, pkgs, pdict, incompats, action)

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
	pkgs = pdict.keys()
	num = len(pkgs)
	for name in pkgs:
		if not graphdict.has_key(name):
			graphdict[name] = [name]

	sorted_list = tsort.robust_topological_sort(graphdict)

	# Reverse order for uninstall since packages must be uninstalled that way.
	if action == img.UNINSTALL:
		sorted_list.reverse()
	tplan = TransformPlan(img, pdict, sorted_list, action, num)

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

	#
	# First download all the files and verify checksums. verify_sha1sum raises
	# and exception if checksum verification fails.
	#
	if not tplan.action == img.UNINSTALL:
		print "*** Downloading packages\n"
		download_packages(tplan)

		if downloadonly == 1:
			print "** Download complete\n"
			return ret

	if tplan.action == img.UNINSTALL:
		print "*** Uninstalling packages\n"
	else:
		print "*** Installing/Upgrading packages\n"

	# Now perform all the install actions
	for titem in tplan.sorted_list:
		for pkgname in titem:
			ent = tplan.pdict[pkgname]
			if ent.action == img.INSTALL:
				if not S__NOEXEC:
					install_pkg(img, ent, ent.dwn_pkgfile)
					os.unlink(ent.dwn_pkgfile)
				else:
					print "*** Will install %s" % ent.cname
			elif ent.action == img.UPGRADE:
				if not S__NOEXEC:
					uninstall_pkg(img, ent)
					install_pkg(img, ent, ent.dwn_pkgfile)
				else:
					print "*** Will upgrade %s" % ent.cname
			elif ent.action == img.UNINSTALL:
				if not S__NOEXEC:
					uninstall_pkg(img, ent)
				else:
					print "*** Will uninstall %s" % ent.cname

	if tplan.action == img.UNINSTALL:
		print "\n*** Uninstallation Complete\n"
	else:
		print "\n*** Installation/Upgrade Complete\n"

def download_packages(tplan):
	"""Download all packages in mentioned in the transform plan"""

	#
	# We download one package at a time to avoid swamping all bandwidth.
	#
	img = tplan.img
	for titem in tplan.sorted_list:
		for pkgname in titem:
			ent = tplan.pdict[pkgname]
			if ent.action != img.INSTALL and ent.action != img.UPGRADE:
				continue
			if ent.type == "P":
				fc = ent.pkgfile[0:1]
				pkgurl = "%s/%s/%s/%s/%s" % \
				    (ent.sitevars.fullurl, img.ARCH, img.OSREL, fc, \
				    ent.pkgfile)
			else:
				pkgurl = "%s/%s/%s/groups/%s" % \
				    (ent.sitevars.fullurl, img.ARCH, img.OSREL, \
				    ent.pkgfile)

			tfile = "%s/%s" % (img.SPKG_DWN_DIR, ent.pkgfile)
			ent.dwn_pkgfile = tfile

			#
			# If the file is already downloaded then check the sha1sum
			#
			verify = 1
			if os.path.isfile(tfile):
				try:
					print "*** Package %s already downloaded\n" % \
					    ent.cname
					print "*** Verifying SHA1 Checksum\n"
					if not S__NOEXEC:
						verify_sha1sum(ent, tfile)
					verify = 0
				except:
					print "*** Checksum does not match re-downloading"
					removef(tfile)
					downloadurl(ent.sitevars, pkgurl, tfile)
			else:
				downloadurl(ent.sitevars, pkgurl, tfile)

			if verify == 1:
				print "*** Verifying SHA1 Checksum for package %s\n" % \
				    ent.cname
				try:
					if not S__NOEXEC:
						verify_sha1sum(ent, tfile)
				except:
					print "*** Checksum verification failed." \
					    " Retrying download"
					removef(tfile)
					downloadurl(ent.sitevars, pkgurl, tfile)
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

	incompats = {}
	print "*** Computing dependencies and building package list\n"
	#########################################
	# Installation plan creation phase
	#########################################
	tplan = create_plan(img, pargs, incompats, img.INSTALL)
	if not tplan:
		return 1
	#########################################
	# End of Installation plan creation phase
	#########################################

	if tplan.num == 0:
		print "------------------------------------------------"
		print "All packages are up to date. Nothing to do"
		print "------------------------------------------------"
		print ""
		return

	if len(incompats) > 0 and downloadonly == 0:
		#
		# We have incompatible packages and have to try to
		# uninstall them.
		#
		inpkgs = incompats.keys()
		for pn in inpkgs:
			print "Package %s to be removed since following packages " \
			    " to be installed are incompatible with it:" % pn
			print incompats[pn]
		img.uninst_type = 0
		uplan = create_plan(img, inpkgs, None, img.UNINSTALL)
		if uplan:
			# Find out whether all incompat pkgs can be uninstalled
			abort = False
			for pn in incompats.keys():
				if pn not in uplan.pdict:
					if pn in img.cnames:
						pn = img.cnames[pn]
					print "Package %s can't be uninstalled" % \
					    pn
					abort = True
			if abort:
				raise PKGError(_("Unable to remove incompatible packages."
				    " Can't proceed!"))
			execute_plan(uplan, 0)

	execute_plan(tplan, downloadonly)

	return 0

#
# Main package installation routine
#
def uninstall(img, pargs):
	"""Uninstall one or more packages listed on the command line along with
	   their dependencies"""

	if len(pargs) > 0 and pargs[0] == "-d":
		img.uninst_type = 1
		del pargs[0]

	if len(pargs) == 0:
		print >> sys.stderr, \
		    "No packages specified to uninstall."
		return

	print "** Computing dependencies and building package list\n"
	#########################################
	# Uninstallation plan creation phase
	#########################################
	tplan = create_plan(img, pargs, None, img.UNINSTALL)
	if not tplan:
		return 1
	#########################################
	# End of Uninstallation plan creation phase
	#########################################

	if tplan.num == 0:
		print "------------------------------------------------"
		print "No packages to uninstall."
		print "------------------------------------------------"
		print ""
		return

	execute_plan(tplan, 0)

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

	if tplan.num == 0:
		print "------------------------------------------------"
		print "All packages are up to date. Nothing to do"
		print "------------------------------------------------"
		print ""
		return

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
			print "     Please put '%s' into that file after reboot" % rel
			print "     or set this value for USE_RELEASE_TAG in /etc/spkg.conf"
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

	group = False
	if len(pargs) > 0:
		if pargs[0] == "-r":
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
		elif pargs[0] == "-g":
			group = True

	pdict = {}
	for sv in img.PKGSITEVARS:
		catf = open(sv.catalog, "r")

		print "#################################################" \
		    "###########################"
		if group:
			print "# Showing Group packages from site %s" % sv.site
		else:
			print "# Showing packages from site %s" % sv.site
		print "#################################################" \
		    "###########################"
		for line in catf:
			line = line.strip()
			entry = line.split(" ")
			if len(entry) != 7: continue

			#
			# Skip if this entry was already compared earlier
			#
			nm = entry[img.CNAMEF]
			pkgname = entry[img.PKGNAMEF]
			type = entry[img.TYPEF]
			if group and type != "G":
				continue

			#
			# We want the latest pkg revision here.
			# Current symlink in the pkg's metainfo dir always points to
			# the latest version, so we cheat via readlink.
			#
			if type == "P":
				curr = "%s/%s/current" % (sv.metadir, pkgname)
			else:
				curr = "%s/groups/%s/current" % (sv.metadir, pkgname)
			version = os.readlink(curr).strip()
			fields = fetch_metainfo_fields(sv, pkgname, version, \
			    type, ["VERSION", "DESC"])
			verstr = fields[0].replace(",REV=", "(") + ")"
			desc = fields[1]

			print "%33s: %s\n%33s  %s\n" % \
			    (nm, desc, " ", verstr)
		catf.close()

		print "#################################################" \
		    "###########################"
		print "# End of packages from site %s" % sv.site
		print "#################################################" \
		    "###########################"
	return 0

def compare(img, pargs):
	"""Compare installed packages with ones in the preferred catalogs"""

	bold = "\033[1m"
	reset = "\033[0;0m"

	for sv in img.PKGSITEVARS:
		catf = open(sv.catalog, "r")

		ioerr = 0
		pdict = {}
		print "############################################################################"
		print "# Processing packages from site %s" % sv.site
		print "############################################################################"
		print "%33s %35s %s\n" % ("Package Name", "Local Vers", "Avail Vers")
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
			if type == "P":
				curr = "%s/%s/current" % (sv.metadir, pkgname)
			else:
				curr = "%s/groups/%s/current" % (sv.metadir, pkgname)
			version = os.readlink(curr).strip()
			fields = fetch_metainfo_fields(sv, pkgname, version, \
			    type, ["VERSION", "DESC"])
			verstr = fields[0].replace(",REV=", "(") + ")"
			desc = fields[1]

			if os.path.exists("%s/%s" % (img.INSTPKGDIR, pkgname)) or \
			    os.path.exists("%s/%s" % (img.SPKG_GRP_DIR, pkgname)):
				localver = fetch_local_version(img, 
				    Cl_pkgentry(entry, sv))
				lv = localver[1].replace("VERSION=", "")
				lv = lv.replace(",REV=", "(") + ")"

				try:
					cmp = compare_vers(version, localver[0])
				except InvalidOperation, inv:
					print traceback.format_exc()
					print "%s, %s" % (version, localver[0])
					ioerr = 1

				if cmp <= 0:
					print "%34s: %s\n%34s: %s\n" % \
					    (nm, desc, lv, verstr)

				elif cmp > 0:
					print "%34s: %s\n%34s: %s\n" % \
					    ("*" + nm, desc, lv, verstr)
			else:
				print "%34s: %s\n%34s: %s\n" % \
				    (nm, desc, "(Not Installed)", verstr)
	return 0

def download(img, pargs):
	"""Only download packages do not install."""

	#
	# Call install with the download flag set. It will cause the package tree
	# to be resolved and downloaded but not installed.
	#
	ret = install(img, pargs, 1)
	return ret

def dump_pkginfo(pkg, installed, short, depmode, invdeps):
	"""Dump package info for the given package."""

	vf = open(pkg.pkginfile, "r")
	cont = {}
	for line in vf:
		line = line.strip()
		if line == "" or line[0] == "#":
			continue
		ent = line.split("=")
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

	print ""
	if short:
		print " %20s : %s" % ("Common Name", cname)
		print " %20s : %s" % ("Description", cont["DESC"])
	else:
		print " %20s : %s" % ("Common Name", cname)
		print " %20s : %s" % ("Package Name", pkgname)
		print " %20s : %s" % ("Description", cont["DESC"])
		if cont["VERSION"].find(",REV=") > -1:
			print " %20s : %s" % ("Version", \
			    cont["VERSION"].replace(",REV=", "(") + ")")
		else:
			print " %20s : %s" % ("Version", cont["VERSION"] + "()")
		if installed:
			print " %20s : %s" % ("Installed", "Yes")
			print " %20s : %s" % ("Install Date", cont["INSTDATE"])
		else:
			print " %20s : %s" % ("Installed", "No")

		if pkg.type == "P":
			print " %20s : %s" % ("Type", "Standard Package")
		else:
			print " %20s : %s" % ("Type", "Group Package")
		print " %20s : %s" % ("Category", cont["CATEGORY"])
		print " %20s : %s" % ("Vendor", cont["VENDOR"])

	# List package dependencies
	if depmode == 1:
		print " -- Package Dependencies --"
		if not os.path.exists(pkg.dependfile):
			print "  - None -"
			return

		depf = open(pkg.dependfile, "r")
		for de in depend_entries(depf, ["P"]):
			if de[1] in img.cnames:
				print "  " + img.cnames[de[1]]
			else:
				print "  " + de[1]
		depf.close()
	elif depmode == 2:
		print " -- Packages that depend on this package --"
		if pkg.pkgname not in invdeps:
			print "  - None -"
			return

		for pn in invdeps[pkg.pkgname]:
			if pn in img.cnames:
				print "  " + img.cnames[pn]
			else:
				print "  " + pn

def info(img, pargs):
	"""Display package information. Works for both installed and not-installed packages."""

	allinst = 0
	short = False
	#invdeps = {}
	depmode = 0 # 0 - none, 1 - dependencies, 2 - dependents

	if len(pargs) > 0:
		if pargs[0] == '-s':
			short = True
			del pargs[0]
		elif pargs[0] == '-d':
			depmode = 1
			del pargs[0]
		elif pargs[0] == '-D':
			depmode = 2
			del pargs[0]

	if len(pargs) == 0:
		# Get list of packages installed in system.
		logv(_("Scanning installed packages"))
		pkgs = map(lambda pkg: pkg.replace(".i", ""), os.listdir(img.INSTPKGDIR))
		allinst = 1
	else:
		pkgs = pargs

	pdict = {}
	build_pkglist(img, pkgs, pdict, None, img.LIST_ONLY)

	pkgs = pdict.keys()
	invdeps = {}
	if depmode == 2:
		invdeps = load_inverse_deps(img)

	print "############################################################################"
	if allinst == 1:
		print "# Listing all installed packages"
		print "############################################################################"

	for pn in pkgs:
		pkg = pdict[pn]
		if pkg:
			if pkg.type == "P":
				pkginfile = "%s/%s/pkginfo" % (img.INSTPKGDIR, pkg.pkgname)
				dependfile = "%s/%s/install/depend" % (img.INSTPKGDIR, pkg.pkgname)

			else:
				pkginfile = "%s/%s/pkginfo" % (img.SPKG_GRP_DIR, pkg.pkgname)
				dependfile = "%s/%s/depend" % (img.SPKG_GRP_DIR, pkg.pkgname)
		else:
			pkginfile = "%s/%s/pkginfo" % (img.INSTPKGDIR, pn)
			dependfile = "%s/%s/install/depend" % (img.INSTPKGDIR, pn)
			if not os.path.exists(pkginfile):
				print "!"
				print "! Package %s not found" % pn
				print "!"
				print ""
				continue
			# Fake up a pkg object
			entry = [pn, "", pn, "", "", "", "P"]
			pkg = Cl_pkgentry(entry, None)

		pkg.pkginfile = pkginfile
		pkg.dependfile = dependfile

		if allinst == 1:
			dump_pkginfo(pkg, True, short, depmode, invdeps)
		else:
			if os.path.exists(pkginfile):
				dump_pkginfo(pkg, True, short, depmode, invdeps)
			else:
				if pkg.type == "P":
					pkginfile = "%s/%s/%s/pkginfo" % \
			    		    (pkg.sitevars.metadir, pkg.pkgname, pkg.version)
					dependfile = "%s/%s/%s/depend" % \
			    		    (pkg.sitevars.metadir, pkg.pkgname, pkg.version)
				else:
					pkginfile = "%s/groups/%s/%s/pkginfo" % \
			    		    (pkg.sitevars.metadir, pkg.pkgname, pkg.version)
					dependfile = "%s/groups/%s/%s/depend" % \
			    		    (pkg.sitevars.metadir, pkg.pkgname, pkg.version)
				pkg.pkginfile = pkginfile
				pkg.dependfile = dependfile
				dump_pkginfo(pkg, False, short, depmode, invdeps)
	return 0

def init(img, pargs):
	"""Initialize a directory to be an alternate root image."""

	if len(pargs) < 1:
		raise PKGError(_("No directory provided to initialize."))

	altroot = pargs[0]
	img.init(altroot)
	updatecatalog(img, [])

def dump_pkgcontents(name, pkgmapfile, long_listing):
	"""Dump the package pathnames for the given package."""

	#
	# Contents of the pkgmap file are dumped
	#
	try:
		pmf = open(pkgmapfile, "r")
	except:
		print "!"
		print "! Error fetching package contents for %s " % name
		print "!"
		print traceback.format_exc()
		return

	types = {"d":"dir", "s":"symlink", "l":"hardlink", "f":"file", "e":"file", "v":"file"}
	print "---------------------------------------------------------------"
	print "- Package contents for %s " % name
	print "---------------------------------------------------------------"
	for line in pmf:
		entry = line.strip().split(" ")
		if entry[0] == ":" or entry[1] == "i": continue

		if entry[1] == "s":
			fl = entry[3].replace("=", " -> ")
			if long_listing:
				print "type = %s" % types[entry[1]]
			print fl
		else:
			if long_listing:
				print "type = %s, perms = %s, owner = %s, group = %s" % \
				    (types[entry[1]], entry[4], entry[5], entry[6])
			print entry[3]
		if long_listing:
			print ""
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
	build_pkglist(img, pkgs, pdict, None, img.LIST_ONLY)

	for pn in pdict.keys():
		pkg = pdict[pn]
		name = ""

		#
		# First see if this is a Group package
		#
		if pkg and pkg.type == "G":
			print ">"
			print "> This is a group package."
			print ">"
			print ""
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
				print "!"
				print "! Package %s not found" % pn
				print "!"
				print ""
				continue
			name = pn

		dump_pkgcontents(name, pkgmapfile, long_listing)

#
# TODO: This is a simple search of catalog. Implement advanced indexing and
# searching based on Nucular.
#
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
	for sv in img.PKGSITEVARS:
		if not os.path.isfile(sv.catalog):
			updatecatalog(img, [])
		for pkg in searchcatalog(sv, mtch, -1):
			pkginfile = "%s/%s/%s/pkginfo" % \
			    (pkg.sitevars.metadir, pkg.pkgname, pkg.version)
			pkg.pkginfile = pkginfile
			dump_pkginfo(pkg, False, False, 0, None)

#
# Identify a usable downloader utility.
# Axel is a dependency of spkg but we perform this check anyway
# to at least fall back to wget if axel is not available for
# any reason.
#
AXEL_FOUND = True
AXEL = "/usr/bin/axel"
WGET = ""
if not os.path.exists(AXEL):
	AXEL_FOUND = False
	WGET = "/usr/sfw/bin/wget"
	if not os.path.exists(WGET):
		WGET = "/usr/bin/wget"
		if not os.path.exists(WGET):
			raise PKGError(_("No downloader utility found! Need either axel or wget."))
	logv(_("Axel not found using wget"))

SZIP = "/usr/bin/7za"
if not os.path.exists(SZIP):
	raise PKGError(_("7Zip utility not found"))

S__VERBOSE = False
S__NOEXEC = False

def do_main():
	"""Main entry point."""
	global S__VERBOSE, S__NOEXEC

	gettext.install("spkg", "/usr/lib/locale");

	ret = 0
	use_site = ""

	try:
		opts, pargs = getopt.getopt(sys.argv[1:], "s:R:r:vn")
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
		elif opt == "-v":
			S__VERBOSE = True
		elif opt == "-n":
			S__NOEXEC = True

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
	else:
		check_catalog(img)

	if subcommand == "install":
		ret = install(img, pargs, 0)
	elif subcommand == "uninstall":
		ret = uninstall(img, pargs)
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
	elif subcommand != "updatecatalog":
		print >> sys.stderr, \
		    "spkg: unknown subcommand '%s'" % subcommand

	return ret
