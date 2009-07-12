#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long qw(:config gnu_getopt no_auto_abbrev);
use rpm_spec;
use config;

my $rpm_target = "i586";
our $opt_specdir;
my $spec_id = 0;
my @specs_to_build = ();
my $build_command;

sub usage (;$) {
    my $retval = shift;
    print << "EOF";
build-gnome2 [options] [command] specs...

Options:

    --dumprc
                  Print the current configuration in a format suitable
                  for an rc file.

    --get-name
                  Print the self package or rpm name. Use with 'parse' 
                  commad.

    --get-child-names
                  Print the child package or rpm names. Use with 'parse' 
                  command.

    --get-sources
                  Print all source filenames in the spec file. Use with 
                  the 'parse' command.

    --get-sources-from-child=name
                  Print the source filenames beloging to the specified 
                  rpm name. Use with the 'parse' command.

    --get-patches
                  Print all patch filenames in the spec file. Use with 
                  the 'parse' command.

    --get-patches-from-child=name
                  Print the patch filenames beloging to the specified 
                  rpm name. Use with the 'parse' command.

    --get-builddir
                  Print the build dirname under %{_buildir}. Use with the 
                  'parse' command.

    --get-child-builddirs
                  Print all child build dirnames under %{_buildir}/parent. 
                  Use with the 'parse' command.

    --get-builddir-from-child=name
                  Print the all child build dirnames under %{_buildir}/parent. 
                  belonging to the specified rpm name, Use with the 'parse' 
                  command.

Commands:

    uninstall-pkgs Remove all rpms defined in the spec files listed
                   on the command line. (runs rpm --erase --nodeps)

    parse          Parse the spec file. Currently effect spec file names 
                   and source filenames only.

EOF
    exit 0;
}


# --------- utility functions ----------------------------------------------
my $os;
my $os_rel;

sub init () {
    $os = `uname -s`;
    chomp ($os);
    $os = lc($os);
    $os_rel = `uname -r`;
    chomp ($os_rel);
    if ($os eq 'sunos') {
        if ($os_rel >= 5) {
            $os = 'solaris';
        }
    }

    if ($os eq "linux") {
      $opt_specdir = "/jds/packages/spec-files/base-specs";
    } else {
      $opt_specdir = "/jds/packages/spec-files";
    }
}

my $defaults;

sub process_defaults () {
  $defaults = config->new();
  $defaults->add ('get_name', 'n',
                  'get the self package or rpm name',
                  0);
  $defaults->add ('get_child_names', 'n',
                  'get the child package or rpm names',
                  0);
  $defaults->add ('get_source_names', 'n',
                  'get all source filenames',
                  0);
  $defaults->add ('get_source_names_from_child', 's',
                  'get all source filenames beloging to the specified rpm name',
                  '');
  $defaults->add ('get_patch_names', 'n',
                  'get all patch filenames',
                  0);
  $defaults->add ('get_patch_names_from_child', 's',
                  'get all patch filenames beloging to the specified rpm name',
                  '');
  $defaults->add ('get_builddir_name', 'n',
                  'get the build dirname under %{_buildir}',
                  0);
  $defaults->add ('get_child_builddir_names', 'n',
                  'get all child build dirnames under %{_buildir}/parent',
                  0);
  $defaults->add ('get_builddir_name_from_child', 's',
                  'get the build dirname under %{_buildir}/parent belonging to the specified rpm name,',
                  '');
}

sub add_spec ($) {
  my $spec_name = shift;
  my $spec;

  if (-f $spec_name) {
    $spec = rpm_spec->new ($spec_name, $rpm_target);
  } else {
    if (not $spec_name =~ /\.spec$/) {
      $spec_name = "${opt_specdir}/${spec_name}.spec";
    }
    $spec = rpm_spec->new ("$spec_name", $rpm_target);
  }

  if (not defined ($spec)) {
    printf ("error");
  } else {
    my $this_spec_id = $spec_id ++;
    $specs_to_build[$this_spec_id] = $spec;
  }
}

sub process_args {
  my $arg = shift;

  if (not defined ($build_command)) {
    if (($arg ne "parse")) {
      printf ("unknown command: $arg\n");
      usage (1);
    }
    $build_command = $arg;
  } else {
    add_spec ($arg);
  }
}

sub process_options {
  GetOptions (
              'get-name' => sub { $defaults->set ('get_name', 1); },
              'get-child-names' => sub { $defaults->set ('get_child_names', 1); },
              'get-sources' => sub { $defaults->set ('get_source_names', 1); },
              'get-sources-from-child=s' => sub { shift; $defaults->set ('get_source_names_from_child', shift); },
              'get-patches' => sub { $defaults->set ('get_patch_names', 1); },
              'get-patches-from-child=s' => sub { shift; $defaults->set ('get_patch_names_from_child', shift); },
              'get-builddir' => sub { $defaults->set ('get_builddir_name', 1); },
              'get-child-builddirs' => sub { $defaults->set ('get_child_builddir_names', 1); },
              'get-builddir-from-child=s' => sub { shift; $defaults->set ('get_builddir_name_from_child', shift); },
              'help' => \&usage,
              '<>' => \&process_args);
}

# --------- parse command --------------------------------------------------
sub print_self_name ($) {
  my $spec = shift;
  my @sources;

  if ($os eq "linux") {
    @sources = $spec->get_param_array ('sources');
    printf ("%s\n", $spec->{name});
  } elsif ($os eq "solaris") {
#    printf ("%s\n", $spec);
    printf ("%s\n", $spec->get_name($spec));
  }
}

sub print_child_names ($) {
  my $spec = shift;
  my @sources;

  if ($os eq "linux") {
    return;
  } elsif ($os eq "solaris") {
    @sources = $spec->get_sources('sources');
    my @spec_names_used = keys %{$spec->{_specs_used}};

    foreach my $spec_name_used (@spec_names_used) {
      my $spec_used = $spec->{_specs_used}->{$spec_name_used};
      printf ("%s\n", $$spec_used->get_name($$spec_used));
#      printf ("%s\n", $$spec_used->get_base_file_name());
    }
  }
}

sub print_sources ($) {
  my $spec = shift;
  my @sources;

  if ($os eq "linux") {
    @sources = $spec->get_param_array ('sources');
    foreach my $src (@sources) {
      if (not defined ($src)) {
        next;
      }
      printf ("%s\n", $src);
    }
  } elsif ($os eq "solaris") {
    @sources = $spec->get_sources('sources');
    foreach my $src (@sources) {
      if (not defined ($src)) {
        next;
      }
      printf ("%s\n", $src);
    }
  }
}

sub print_sources_from_child ($$) {
  my $spec = shift;
  my $user_rpm = shift;
  my @sources;

  if ($os eq "linux") {
    return;
  } elsif ($os eq "solaris") {
    @sources = $spec->get_sources('sources');
    my @spec_names_used = keys %{$spec->{_specs_used}};
    foreach my $spec_name_used (@spec_names_used) {
      my $spec_used = $spec->{_specs_used}->{$spec_name_used};

      if($user_rpm eq $$spec_used->get_name ($$spec_used)) {
        my @sources_used = $$spec_used->get_sources ();

        foreach my $src (@sources_used) {
          printf ("%s\n", $src);
        }
        exit 0;
      }
    }

    printf ("#### Not Found the rpm: %s\n", $user_rpm);
    exit 1;
  }
}

sub print_patches ($) {
  my $spec = shift;
  my @patches;

  if ($os eq "linux") {
    @patches = $spec->get_param_array ('patches');
    foreach my $patch (@patches) {
      if (not defined ($patch)) {
        next;
      }
      printf ("%s\n", $patch);
    }
  } elsif ($os eq "solaris") {
    @patches = $spec->get_patches('patches');
    foreach my $patch (@patches) {
      if (not defined ($patch )) {
        next;
      }
      printf ("%s\n", $patch);
    }
  }
}

sub print_patches_from_child ($$) {
  my $spec = shift;
  my $user_rpm = shift;
  my @sources;

  if ($os eq "linux") {
    return;
  } elsif ($os eq "solaris") {
    @sources = $spec->get_sources('sources');
    my @spec_names_used = keys %{$spec->{_specs_used}};
    foreach my $spec_name_used (@spec_names_used) {
      my $spec_used = $spec->{_specs_used}->{$spec_name_used};

      if($user_rpm eq $$spec_used->get_name ($$spec_used)) {
        my @patches_used = $$spec_used->get_patches ();

        foreach my $patch (@patches_used) {
          printf ("%s\n", $patch);
        }
        exit 0;
      }
    }

    printf ("#### Not Found the rpm: %s\n", $user_rpm);
    exit 1;
  }
}

sub print_builddir ($) {
  my $spec = shift;
  my @sources;

  if ($os eq "linux") {
    @sources = $spec->get_param_array ('sources');
    my $bsdirname = $spec->get_def('_build_src_dir_name');

    if (not defined $bsdirname) {
      $bsdirname = $spec->_deref ('%name-%version');
    }
    printf ("%s\n", $bsdirname);

  } elsif ($os eq "solaris") {
    @sources = $spec->get_sources('sources');
    my $bsdirname = $spec->eval ('%{_build_src_dir_name}');

    if ($bsdirname eq '%{_build_src_dir_name}') {
      $bsdirname = $spec->eval ('%name-%version');
    }
    printf ("%s\n", $bsdirname);

  }
}

sub print_child_builddirs ($) {
  my $spec = shift;
  my @sources;

  if ($os eq "linux") {
    return;
  } elsif ($os eq "solaris") {
    @sources = $spec->get_sources('sources');
    my @spec_names_used = keys %{$spec->{_specs_used}};

    foreach my $spec_name_used (@spec_names_used) {
      my $spec_used = $spec->{_specs_used}->{$spec_name_used};
      my $bsdirname = $$spec_used->eval ('%{_build_src_dir_name}');

      if ($bsdirname ne '%{_build_src_dir_name}') {
        printf ("%s\n", $bsdirname);
      }
    }

  }
}

sub print_builddir_from_child ($$) {
  my $spec = shift;
  my $user_rpm = shift;
  my @sources;

  if ($os eq "linux") {
    return;
  } elsif ($os eq "solaris") {
    @sources = $spec->get_sources('sources');
    my @spec_names_used = keys %{$spec->{_specs_used}};

    foreach my $spec_name_used (@spec_names_used) {
      my $spec_used = $spec->{_specs_used}->{$spec_name_used};

      if($user_rpm eq $$spec_used->get_name ($$spec_used)) {
        my $bsdirname = $$spec_used->eval ('%{_build_src_dir_name}');

        if ($bsdirname ne '%{_build_src_dir_name}') {
          printf ("%s\n", $bsdirname);
        }
        exit 0;
      }
    }

    printf ("#### Not Found the rpm: %s\n", $user_rpm);
    exit 1;
  }
}

sub get_misc () {
  my $spec = shift;
  my @sources;

  if ($os eq "linux") {
    @sources = $spec->get_param_array ('sources');
    foreach my $src (@sources) {
      if (not defined ($src)) {
        next;
      }
# $1 Name:, 
# $2 build dir name
# $3 source filename
      printf ("Srcs: %s %s %s\n", $spec->{name}, $spec, $src);
    }
  } else {
    @sources = $spec->get_sources('sources');
    foreach my $src (@sources) {
      if (not defined ($src)) {
        next;
      }
# $1 Solaris Name:, 
# $2 Solaris spec filename, 
# $3 source filename
      printf ("Srcs: %s %s %s\n", $spec, $spec->{_base_file_name}, $src);
    }

    my @spec_names_used = keys %{$spec->{_specs_used}};
    foreach my $spec_name_used (@spec_names_used) {
        my $spec_used = $spec->{_specs_used}->{$spec_name_used};

        my @sources_used = $$spec_used->get_sources ();
        foreach my $src (@sources_used) {
# $1 Solaris Name:, 
# $2 Solaris spec filename, 
# $3 Linux Name:, 
# $4 Linux source filename

# I don't know but when used 'printf (' instead of 'printf(', got exec errors.

          printf("Spec sources: %s %s %s %s\n", $spec,
                                                $spec->{_base_file_name},
                                                $spec_name_used,
                                                $src);
        }

        my @patches_used = $$spec_used->get_patches ();
        foreach my $patch (@patches_used) {
# $1 Solaris Name:, 
# $2 Solaris spec filename, 
# $3 Linux Name:, 
# $4 Linux patch filename
          printf("Spec pths: %s %s %s %s\n", $spec, 
                                              $spec->{_base_file_name}, 
                                              $spec_name_used, 
                                              $patch);
        }
    }
  }
}

sub get_parse_options ($) {
  my $spec_id = shift;
  my $spec = $specs_to_build[$spec_id];
  my @sources;
  my $user_rpm_name;

  if ($defaults->get ('get_name')) {
    print_self_name ($spec);
    exit (0);
  }

  if ($defaults->get ('get_child_names')) {
    print_child_names ($spec);
    exit (0);
  }

  if ($defaults->get ('get_source_names')) {
    print_sources ($spec);
    exit (0);
  }

  $user_rpm_name = $defaults->get ('get_source_names_from_child');
  if ($user_rpm_name ne "") {
    print_sources_from_child ($spec, $user_rpm_name);
    exit (0);
  }

  if ($defaults->get ('get_patch_names')) {
    print_patches ($spec);
    exit (0);
  }

  $user_rpm_name = $defaults->get ('get_patch_names_from_child');
  if ($user_rpm_name ne "") {
    print_patches_from_child ($spec, $user_rpm_name);
    exit (0);
  }

  if ($defaults->get ('get_builddir_name')) {
    print_builddir ($spec);
    exit (0);
  }

  if ($defaults->get ('get_child_builddir_names')) {
    print_child_builddirs ($spec);
    exit (0);
  }

  $user_rpm_name = $defaults->get ('get_builddir_name_from_child');
  if ($user_rpm_name ne "") {
    print_builddir_from_child ($spec, $user_rpm_name);
    exit (0);
  }

  else {
    sub get_misc ();
    exit (0);
  }

}

sub do_build {
  while(0){}; #dummy
}

sub do_parse {
  for (my $i = 0; $i <=$#specs_to_build; $i++) {
    get_parse_options ($i);
  }
}

sub main {
  process_defaults ();
  process_options ();

  if ($build_command eq "build") {
    do_build;
  } elsif ($build_command eq "parse") {
    do_parse;
  }
}

init;
main;
