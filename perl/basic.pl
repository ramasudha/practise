#
# Hello World Program in Perl
#
use warnings;
use strict;


print "Hello World!\n";
_find_cfg
my $var = "one";
if (system("ping -c1 a3r3-pdu-sups-00.dc.pa.sophos > /dev/null 2>&1") != 0) {
#if (7 >> 8 == 0) {
        print "in if"
    } else {
        print "in else"
    }
#print system("ls -lz > /dev/null 2>&1");
# print "a= $a"
my @a = split(',', 'a3r3-pdu-sups-00.dc.pa.sophos:13');
my ( $pdu, undef ) = split(':', 'a3r3-pdu-sups-00.dc.pa.sophos:13');
#print "\n@a,$pdu, $outlet"
print "\n $pdu ";
my $type1 = 'VMware';
if ( $type1 !~ ('VMware'|'BreakingPoint'|'KVM'|'Hyper-V'|'Xen') ){
    print "\n hwtype condition in if pass";
}
my @virtual_hwtypes = ("VMware", "BreakingPoint", "KVM", "Hyper-V", "Xen");

my $current_hw = "VMware";

if ( ! grep( /^$current_hw$/ , @virtual_hwtypes ) ) {
    print "PDU code is executed";
}

if ( 'VMware' eq 'VMware' or 'asd123' =~ /:/ ) {
    print "\n in the if";
}

my @a = (1..3);
my $value = 1

if ( $value >= 0 & $value <= 3 ) {
    @a = (1..3, $value);
}