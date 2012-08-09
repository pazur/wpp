#!/usr/bin/perl

use strict;
use warnings;
use feature 'say';

use CGI qw/-utf8/;
use File::Temp qw/tempfile/;
use File::Basename;

my $DIRECTORY = 'songbook';
my $OUT_FILENAME = 'spiewnik.pdf';
my $TMP_PREFIX = 'mysongbook';

my $q = CGI->new;

my ($tex_fh, $tex_filename) = tempfile("${TMP_PREFIX}-XXXXXX", SUFFIX => '.tex', DIR => $DIRECTORY, UNLINK => 0);
my $tex_basename = basename($tex_filename, '.tex');
print $tex_fh $q->param('tex');

my $outlog = "$DIRECTORY/log/$tex_basename.outlog";
my $errlog = "$DIRECTORY/log/$tex_basename.errlog";

my $result = system("make -C $DIRECTORY DOC=$tex_basename.tex > $outlog 2>$errlog");
if ($result != 0) {
    say "Content-type: text/html\n";
    say "Error! Make songbook exited with code $result.";
    return;
}

my $out_file = "$DIRECTORY/$tex_basename.pdf";

print $q->header(-type            => 'application/x-download',
		 -attachment      => $OUT_FILENAME,
		 -Content_length  => -s "$out_file");

open OUT_FILE, "<$out_file";
binmode OUT_FILE;
print while <OUT_FILE>;
close OUT_FILE;

return 0;

		 
