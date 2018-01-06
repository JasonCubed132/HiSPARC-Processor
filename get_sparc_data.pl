
#
# Automated download of sparc data
#

#
# Required arguments are:
# folder to download data to: use -download <my folder>
# station id: use -station <id>
#
# Optional arguments are:
# start/end year/month/date: use something like -start_y 2013 -start_m 1 -start_d 1 -end_y 2013 -end_m 12 -end_d 31
# 
# example command line:
# perl get_sparc_data.pl -download c:\users\maria\documents\hisparc\data -station 501 -start_y 2012 -start_m 6 -start_d 1 -end_y 2012 -end_m 9 -end_d 30
#

use WWW::Mechanize;
use DateTime;
use File::Path qw(make_path);
use Getopt::Long;

my ($root_download_dir,$station_id);
my ($start_y,$start_m,$start_d);
my ($end_y,$end_m,$end_d);


# all data into one file
# date - time - data

GetOptions ("download_dir=s" => \$root_download_dir,
	    "station_id=i" => \$station_id, 
	    "start_year:i" => \$start_y,
	    "start_month:i" => \$start_m,
	    "start_day:i" => \$start_d,
	    "end_year:i" => \$end_y,
	    "end_month:i" => \$end_m,
	    "end_day:i" => \$end_d,

    ) or die("Error in command line arguments\n");

# check arguments
my $arg_errors = 0;
unless (defined $root_download_dir)
{
    warn "Error: download directory must be specified, use -download <folder name>";
    $arg_errors++;
}
unless (defined $station_id)
{
    warn "Error: station id must be specified, use -station <station id>";
    $arg_errors++;
}

# define default dates if args not specified
unless (defined $start_y)
{
    $start_y = 2013;
    warn "Info: using default start year $start_y, use -start_year <yyyy> to specify a different date\n";
}
unless (defined $start_m)
{
    $start_m = 1;
    warn "Info: using default start month $start_m, use -start_month <m> to specify a different date\n";
}
unless (defined $start_d)
{
    $start_d = 1;
    warn "Info: using default start date $start_d, use -start_date <d> to specify a different date\n";
}

unless (defined $end_y)
{
    $end_y = 2013;
    warn "Info: using default end year $end_y, use -end_year <yyyy> to specify a different date\n";
}
unless (defined $end_m)
{
    $end_m = 1;
    warn "Info: using default end month $end_m, use -end_month <m> to specify a different date\n";
}
unless (defined $end_d)
{
    $end_d = 31;
    warn "Info: using default end date $end_d, use -end_date <d> to specify a different date\n";
}

die "There were command argument errors" if $arg_errors;

# Bristol:
# $station_id = 13001;

# create root download directory if it 
# doesn't exist
unless (-d $root_download_dir)
{
    print "Creating directory \"$root_download_dir\"\n";
    make_path($root_download_dir);
}


# get sparc data for each day within a range
my $time_zone = 'Europe/London';
my $start_dt  = DateTime->new(
    year       => $start_y,
    month      => $start_m,
    day        => $start_d,
    hour       => 0,
    minute     => 0,
    second     => 0,
    nanosecond => 0,
    time_zone  => $time_zone);

my $end_dt  = DateTime->new(
    year       => $end_y,
    month      => $end_m,
    day        => $end_d,
    hour       => 23,
    minute     => 0,
    second     => 0,
    nanosecond => 0,
    time_zone  => $time_zone);


# check start/end dates don't span an interval
# bigger than the max allowed
my $max_days = 366;
my $max_interval = DateTime::Duration->new(days => $max_days);
unless ($end_dt > $start_dt)
{
    print "Start: $start_dt\n";
    print "End: $end_dt\n";
    die "Error: end date must be after start date\n";
}
if ($start_dt + $max_interval < $end_dt)
{
    die "Error: time interval between start and end dates must be less than $max_days days\n";
}

my $mech = WWW::Mechanize->new;
$st_download_dir = $root_download_dir . "\\station_${station_id}";

#
# loop over the date range
#
my $n = 1000;
my $dt = $start_dt;
my $one_day = DateTime::Duration->new(days => 1);
my @failure = ();
my @success = ();
my @data_files = ();
my %has_data = ();
for ($i=1; $i<=$n; $i++)
{
    print "$dt\n";
    # have we gone beyond the end date/time?
    my $result = DateTime->compare_ignore_floating($dt, $end_dt);
    if ($result >= 0)
    {
	print "Stopping, reached end date/time\n";
	last;
    }

    # get the month/date info
    my $year;
    my $month;
    my $date;
    if ($dt =~ /(\d{4})\-(\d{2})\-(\d{2})T/)
    {
	$year = $1;
	$month = $2;
	$date = $3;
    }
    else
    {
	die "Error: $dt";
    }

    my $url = "http://data.hisparc.nl/show/source/eventtime/${station_id}/${year}/${month}/${date}/";
    my $download_dir_y = "$st_download_dir\\$year";
    my $download_dir_m = "$download_dir_y\\$month";
    make_path($download_dir_m) unless (-d $download_dir_m);

    my $local_file_name = $download_dir_m . "\\eventtime-$station_id-$year-$month-$date.csv";
    push (@data_files,$local_file_name);
    print "$local_file_name\n";
    
    print "Getting data...\n";
    eval {$mech->get($url, ":content_file" => $local_file_name); };
    if ($@) 
    {
	unless ($mech->success)
	{	    
	    print "URL get request failed\n";
	    print "Status: " . $mech->status() . "\n";
	    push(@failure,$url);
	    $has_data{$local_file_name} = 0;
	}
    }
    else
    {
	push(@success,$url);
	$has_data{$local_file_name} = 1;
    }

    # increment by one day
    $dt->add_duration($one_day);
}

my $num_success = scalar(@success); 
my $num_fail = scalar(@failure);

print "\nNumber of successful downloads: $num_success \n";
print "Number of failed downloads: $num_fail \n";

#
# now process the data files to generate a single
# file containing all data
#
my $all_data_file = $st_download_dir . "\\all_data.csv";
my $fh,$out;
open ($out,">$all_data_file") or die "Error: cannot open output file $all_data_file";
foreach $file (@data_files)
{
    # eventtime-$station_id-$year-$month-$date.csv
    if ($file =~ /eventtime\-(\d+)\-(\d{4})\-(\d{2})\-(\d{2})\.csv/)
    {
	$year = $2;
	$month = $3;
	$date = $4;
    }
    else
    {
	die "Error: file name format not recognised \"$file\"\n";
    }
    my $date_info = "$date\-$month\-$year";
    
    if ($has_data{$file})
    {
	open($fh,$file) or die "Error: could not open file $file";
	undef my $bin_id;
	while (<$fh>)
	{
	    next if (/^\#/);
	    next unless (/\S/);
	    chomp;
	    my @data = split(/\t/,$_);
	    die "Error: file $file, did not find 2 data values: $_" unless (scalar @data == 2);
	    if (defined $bin_id)
	    {
		die "Error: $data[0]" unless $data[0] == $bin_id+1;
		$bin_id = $data[0];
	    }
	    else
	    {
		die "Error: $data[0]" unless $data[0] == 0;
		$bin_id = $data[0];
	    }
	    die "Error: $data[1]" unless ($data[1] =~ /^\d+$/);
         undef my $count;
         if ($data[1] > 0)
         {
             $count = $data[1];
         }

	    print $out "$date_info,$bin_id,";
	    print $out "$count" if (defined $count);
	    print $out "\n";
	}
	close ($fh);
    }
    else
    {
	# no data - use blank entries
     for ($i=0; $i<24; $i++)
	{
	   print $out "$date_info,$i,\n";
	}
    }
}

close $out;
print "All data written to file \"$all_data_file\"\n";
