import re           # Python standard library     
import math         # Python standard library
import tables       # HDF/Saphire
import datetime
import utilities
import solveSky

from solveSky import celestialCoords3Station,coincCoords

from sapphire import esd, download_data, CoincidencesESD, time_util, transformations
from sapphire.api import API, Network, Station
from sapphire.transformations import clock
from utilities import degToRad, radToDeg, mtonlgt

debug    = 1
testMode = True

def stationNumToIDdict(coincidences):
    """Given a coincidences data structure, buld two dictionaries:
         - station numbers ===> station ids\
         - station numbers ===> station_cluster.
    """
    
    s_index = coincidences.s_index        # An array, each element of which is a station-id, in the form of a character string containing the 
                                          # station number as its last part, for example: /hisparc/cluster_birmingham/station_14003.
                                          # This will need to be transformed to a mapping from station number --> station name.
                                          # (E.g   station_to_num["/hisparc/cluster_birmingham/station_14003"] == 14003.)
                                          # The station number is used as an index.

    # Create empty dictionaries.
    station_to_num     = {}
    station_to_cluster = {}

    for s in s_index:
        values            = re.split('_',s)                                     #   Split the string on underscores.
        station_num       = int(values[-1])                                     #   The last element of this array will be the station number.
        station_to_num[s] = station_num                                         #   So copy this to the station number dictionary.
        cluster_string    = values[-2]                                          #   This currently has the form "<cluster>/station"
        station_to_cluster[station_num] = re.sub('/station','',cluster_string)  #   This maps station number to cluster name.

        if(debug >=3):
            print "Station: %-45s"%s,"==>  index= %5d"%station_to_num[s],"; cluster=",station_to_cluster[station_num]
            
    return ( station_to_num, station_to_cluster )


def processCoincidences(cluster,year,month,csv3a):
    """Process a coincidence HDF file for a particular year and month (which identifies 
       the HDF file on disk by means of a standard name encoding: coincidences_<yyyy>_<m>.h5).
       Produce a CSV output file containing altitude/azimuth and ra/declination coordinates."""

    global testMode
    testMode = False

    fileNameH5  = 'coincidence%s_%d_%d.h5'%(cluster,year,month)
    fileName3CSV = 'coincidence3%s_%d_%d.csv'%(cluster,year,month)


    if(debug >= 1):
        print "Process coincidences for cluster %s for year %d month=%2d"%(cluster,year,month),
        print "   Input from file: ",fileNameH5,
        print "   Output for 3-station coincidences to file:  ",fileName3CSV


    csv3 = open(fileName3CSV,'w')
    
    csv3.write('year,month,cluster,id, multiplicity,gps_timestamp,uts_timstamp, GMST(Hours),GMST(deg), ra,ha,dec,alt,azm, s1,s2,s3, delta_ab,delta_ac,ecef_dx_b,ecef_dy_b,ecef_dz_b,ecef_dx_c,ecef_dy_c,ecef_dz_c,enu_dx_b,enu_dy_b,enu_dz_b,enu_dx_c,enu_dy_c,enu_dz_c,bac\n')      # Write the heading on the CSV table.

   
    data  = tables.open_file(fileNameH5,'r')        # The table containing the coincidence data.

    s_index = data.root.coincidences.s_index        # An array, each element of which is a station-id, in the form of a character string containing the 
                                                    # station number as its last part, for example: /hisparc/cluster_birmingham/station_14003.
                                                    # This will need to be transformed to a mapping from station number --> station name.
                                                    # (E.g   station_to_num["/hisparc/cluster_birmingham/station_14003"] == 14003.)
                                                    # The station number is used as an index.

    c_index = data.root.coincidences.c_index        # An array, each element of which corresponds one-to-one in sequence to elements in ctable[].
                                                    # Each array element of c_index is itself an array which each element relates to a station in the coincidence:
                                                    #   - each station element is a tuple: (seq_id, event_no)
                                                    #     where the seq_id indexes into s_index, to identify a station-id (a character string).
                                                    #     and event_no is the unique event identifier for the shower trace at that station.

    ctable  = data.root.coincidences.coincidences   # An array of coincidences.
                                                    # Each coincidence (ctable[i]) is a dictionary with the following entries:
                                                    #   ctable[i]['id']             Unique Id of the coincidence.
                                                    #   ctable[i]['N']              number of stations in the coincidence.
                                                    #   ctable[i]['timestamp']      unix format timestamp.
                                                    #   ctable[i]['nanosecs']       nanoseconds after the unix timestamp.
                                                    #   ctable[i]['ext_timestamp']  extended timestamp.


    # Create a dictionary relating station IDs (as used in the Coincidences data structure)
    # to station numbers (as used to access station information via the Station object).

    ( station_to_num, station_to_cluster ) = stationNumToIDdict(data.root.coincidences)       
    
    if(debug >= 1):    
        print "Number of coincidences to process for month: ",month,"=",ctable.nrows

    for i in range(ctable.nrows):                   # Iterate over coincidences in the table.

        if( i > 40000):
            break

        coincidence = ctable[i]
        
        coinc_multiplicity   = ctable[i]['N']   # The number of stations registering the coincidence 
        
        # Extract data and construct arrays to hold data describing a coincidence
        (coinc_stat_num,coinc_stat_id,coinc_stat_delta,coinc_stat_gps,coinc_stat_event,
                     coinc_stat_ecef_x, coinc_stat_ecef_y, coinc_stat_ecef_z,
                     coinc_stat_ecef_dx,coinc_stat_ecef_dy,coinc_stat_ecef_dz,
                     coinc_stat_enu_dx, coinc_stat_enu_dy, coinc_stat_enu_dz,
                     ecef_bac
                     ) = coincCoords(data, coincidence, station_to_num, c_index[i], s_index)

        if(debug>=4):
            print "Coincidence %d"%i
            print coinc_stat_num
            print coinc_stat_id
            print coinc_stat_delta
            print coinc_stat_gps
            print coinc_stat_event[0]
            print coinc_stat_event[1]
            print coinc_stat_event[2]

        cluster = station_to_cluster[coinc_stat_num[0]]
        uts_timestamp = clock.gps_to_utc( coincidence['timestamp'] )

        if coinc_multiplicity == 3:                     # Need at least 3 stations for direction finding

            # Solve for the shower direction.
            (gmst,ra,ha,dec,alt,azm,bac,F) = celestialCoords3Station(coincidence, coinc_stat_num, coinc_stat_id, coinc_stat_delta, coinc_stat_gps, coinc_stat_event)


                
            if( not re.search("error",F) and bac*radToDeg > 20.0 and bac < 160.0):               # Distrust the results if the included angle between detector arms is too small or too big.

                csv3.write('%d,%d,%s,%d,%d,%d,%d,' %(year,month,cluster,coincidence['id'], coinc_multiplicity, coincidence['timestamp'],uts_timestamp))
                csv3.write('%f,%f,'             %(gmst, radToDeg*gmst*math.pi/12.0))
                csv3.write('%f,%f,%f,%f,%f,'    %(radToDeg*ra,radToDeg*ha,radToDeg*dec,radToDeg*alt,radToDeg*azm)),                
                csv3.write('%d,%d,%d,'          %(coinc_stat_num[0],coinc_stat_num[1],coinc_stat_num[2]))
                csv3.write('%f,%f,'             %(coinc_stat_delta[1],coinc_stat_delta[2]))
                csv3.write('%f,%f,%f,'          %(coinc_stat_ecef_dx[1],coinc_stat_ecef_dy[1],coinc_stat_ecef_dz[1]))
                csv3.write('%f,%f,%f,'          %(coinc_stat_ecef_dx[2],coinc_stat_ecef_dy[2],coinc_stat_ecef_dz[2]))
                csv3.write('%f,%f,%f,'          %(coinc_stat_enu_dx[1], coinc_stat_enu_dy[1], coinc_stat_enu_dz[1]))
                csv3.write('%f,%f,%f,'          %(coinc_stat_enu_dx[2], coinc_stat_enu_dy[2], coinc_stat_enu_dz[2]))
                csv3.write('%f,%s'              %(ecef_bac,F))
                csv3.write('\n')

                csv3a.write('%d,%d,%s,%d,%d,%d,%d,' %(year,month,cluster,coincidence['id'], coinc_multiplicity, coincidence['timestamp'],uts_timestamp))
                csv3a.write('%f,%f,'             %(gmst, radToDeg*gmst*math.pi/12.0))
                csv3a.write('%f,%f,%f,%f,%f,'    %(radToDeg*ra,radToDeg*ha,radToDeg*dec,radToDeg*alt,radToDeg*azm)),                
                csv3a.write('%d,%d,%d,'          %(coinc_stat_num[0],coinc_stat_num[1],coinc_stat_num[2]))
                csv3a.write('%f,%f,'             %(coinc_stat_delta[1],coinc_stat_delta[2]))
                csv3a.write('%f,%f,%f,'          %(coinc_stat_ecef_dx[1],coinc_stat_ecef_dy[1],coinc_stat_ecef_dz[1]))
                csv3a.write('%f,%f,%f,'          %(coinc_stat_ecef_dx[2],coinc_stat_ecef_dy[2],coinc_stat_ecef_dz[2]))
                csv3a.write('%f,%f,%f,'          %(coinc_stat_enu_dx[1], coinc_stat_enu_dy[1], coinc_stat_enu_dz[1]))
                csv3a.write('%f,%f,%f,'          %(coinc_stat_enu_dx[2], coinc_stat_enu_dy[2], coinc_stat_enu_dz[2]))
                csv3a.write('%f,%s'              %(ecef_bac,F))
                csv3a.write('\n')
        else:
            print "Coincidence Multiplicity: ",coinc_multiplicity
            csv3.write('%d,%d,%s,%d,%d,%d,%d,' %(year,month,cluster,coincidence['id'], coinc_multiplicity, coincidence['timestamp'],uts_timestamp))
            csv3.write('\n')
            csv3a.write('%d,%d,%s,%d,%d,%d,%d,' %(year,month,cluster,coincidence['id'], coinc_multiplicity, coincidence['timestamp'],uts_timestamp))
            csv3a.write('\n')
            
#============================================================================================================

def printStationCoordinates(stationNumbers):
    """Given a list of station numbers (integers), print station GPS coordinates."""
    
    for stationNum in stationNumbers:
        station = Station(stationNum)
        location = station.gps_location()
        print stationNum, station.country(), station.cluster(), station.n_detectors(),location['latitude'],location['longitude'], location['altitude']



#===================================================================================================================

                           
if __name__ == "__main__":
    import sys,re,math
    
    cluster="Amsterdam"
   
    fileNameCSV_A='coincidence3%s.csv'%cluster
    csv3a=open(fileNameCSV_A,'w')
#    csv3a.write('year,month,cluster,id, gps_timestamp,uts_timstamp, GMST(Hours),GMST(deg), ra,ha,dec,alt,azm, s1,s2,s3, delta_ab,delta_ac\n')      # Write the heading on the CSV table.

    for year in [2017]:
    
        for m in range(0,12):             # for 2016 only 10 months of data as yet
            month  = m+1
            processCoincidences(cluster,year,month,csv3a)




