use Data::Dumper;
my @a = (1..3);
my $var = 1;
#if ( ($var >= 0) && ($var <= 3))
#  { # $var is a number
#     print "in if";
#  }

my $time = time();
#print $time;

my $n = ('exitstatus'=>1);
#print Dumper(defined $n->{exitstatus});
#print $n->{exitstatus};
$n->{exitstatus} = 2 unless defined $n->{exitstatus} and $n->{exitstatus} > 2;
print Dumper($n);