#!/usr/bin/perl

use URI::Escape;

while(<>) {
    print uri_escape($_);
}
