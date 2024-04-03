2018 New York precinct and election results shapefile.

## RDH Date retrieval
10/25/2021

## Sources
Election results primarily from individual county canvass reports as processed by OpenElections (https://github.com/openelections/openelections-data-ny/). Results for the following counties in part or in whole directly from county canvass reports: Allegany, Cattaraugus, Chautauqua, Erie, Genesee, Jefferson, Kings, Lewis, Madison, Monroe, Nassau, New York, Orange, Richmond, Schenectady, Warren.
Ontario, Schuyler, Warren, and Wyoming reported some votes at the countywide level. These were distributed by candidate to precincts based on the precinct-level reported vote. Some New York counties only report official write-ins by precinct while placing invalid write-in votes with blank or other void ballots so that write-in figures are not directly comparable at the statewide level.
Precinct shapefiles were obtained from the respective county governments for most counties. The following counties instead use shapefiles from the U.S. Census Bureau's Redistricting Data Program: Chenango, Columbia, Franklin, Genesee, Hamilton, Lewis, Montgomery, Oswego, Otsego, Schenectady, Schuyler, Seneca, St. Lawrence, Wayne, Wyoming. Nearly all of the Census shapefiles were edited to match PDF maps from the respective county boards of elections or the voter file from the New York State Board of Elections.
The Nassau County shapefile includes several dozen unassigned precinct divisions where a distinct ballot style would be required if they had registered voters. The following include registered voters and were merged into adjoining active precincts based on the voter registration file: HE 19049/19065, HE 20012/20093, HE 21087/22108, HE 22066/22702, NH 13016/13701, OB 15093/15703.
The Chemung County shapefile is significantly outdated. Multiple precincts were split, merged, and adjusted in Elmira, Horseheads, and Southport to match PDF maps provided by the county board of elections. The county boundary between Nassau and Suffolk is misaligned in both shapefiles and was edited to match the voter file. Tioga County has a more accurate parcel-based precinct shapefile that was used instead of the shapefile based on BOE descriptions of the precincts.

## Fields metadata

Vote Column Label Format
------------------------
Columns reporting votes follow a standard label pattern. One example is:
G16PREDCli
The first character is G for a general election, P for a primary, C for a caucus, R for a runoff, S for a special.
Characters 2 and 3 are the year of the election.
Characters 4-6 represent the office type (see list below).
Character 7 represents the party of the candidate.
Characters 8-10 are the first three letters of the candidate's last name.

Office Codes
A## - Ballot amendment, where ## is an identifier
AGR - Commissioner of Agriculture
ATG - Attorney General
AUD - Auditor
CFO - Chief Financial Officer
CHA - Council Chairman
COC - Corporation Commissioner
COM - Comptroller
CON - State Controller
COU - City Council Member
CSC - Clerk of the Supreme Court
DEL - Delegate to the U.S. House
GOV - Governor
H## - U.S. House, where ## is the district number. AL: at large.
HOD - House of Delegates, accompanied by a HOD_DIST column indicating district number
HOR - U.S. House, accompanied by a HOR_DIST column indicating district number
INS - Insurance Commissioner
LAB - Labor Commissioner
LAN - Commissioner of General Land Office
LND - Commissioner of Public/State Lands
LTG - Lieutenant Governor
MAY - Mayor
MNI - State Mine Inspector
PSC - Public Service Commissioner
PUC - Public Utilities Commissioner
RGT - State University Regent
RRC - Railroad Commissioner
SAC - State Appeals Court (in AL: Civil Appeals)
SBE - State Board of Education
SCC - State Court of Criminal Appeals
SOC - Secretary of Commonwealth
SOS - Secretary of State
SPI - Superintendent of Public Instruction
SPL - Commissioner of School and Public Lands
SSC - State Supreme Court
TAX - Tax Commissioner
TRE - Treasurer
UBR - University Board of Regents/Trustees/Governors
USS - U.S. Senate

Party Codes
D and R will always represent Democrat and Republican, respectively.
See the state-specific notes for the remaining codes used in a particular file; note that third-party candidates may appear on the ballot under different party labels in different states.

## Fields
G18USSDGIL - Kirsten E. Gillibrand (Democratic, Working Families, Independence, and Women's Equality fusion)
G18USSRFAR - Chele Chiavacci Farley (Republican, Conservative, and Reform fusion)
G18USSOWRI - Write-in Votes

G18GOVDCUO - Andrew M. Cuomo (Democratic, Working Families, Independence, and Women's Equality fusion)
G18GOVRMOL - Marc Molinaro (Republican, Conservative, and Reform fusion)
G18GOVLSHA - Larry Sharpe (Libertarian Party)
G18GOVGHAW - Howie Hawkins (Green Party)
G18GOVSMIN - Stephanie A. Miner (Serve America Movement Party)
G18GOVOWRI - Write-in Votes

G18COMDDIN - Thomas P. DiNapoli (Democratic, Working Families, Independence, Women's Equality, and Reform fusion)
G18COMRTRI - Jonathan Trichter (Republican and Conservative fusion)
G18COMLGAL - Cruger E. Gallaudet (Libertarian Party)
G18COMGDUN - Mark Dunlea (Green Party)
G18COMOWRI - Write-in Votes

G18ATGDJAM - Letitia A. James (Democratic, Working Families and Independence fusion)
G18ATGRWOF - Keith Wofford (Republican and Conservative fusion)
G18ATGLGAR - Christopher B. Garvey (Libertarian Party)
G18ATGGSUS - Michael Sussman (Green Party)
G18ATGOSLI - Nancy B. Sliwa (Reform Party)
G18ATGOWRI - Write-in Votes

## Processing Steps
Precincts reported on combined line items for the 2020 general election were consolidated in the following counties: Bronx, Cattaraugus, Kings, Monroe, Nassau, New York, Onondaga, Queens, Richmond, Tompkins.

These additional modifications were made to reflect precinct boundaries as of the 2018 general election:

Chautauqua: Add Ellery 2V; Adjust Jamestown 5-3/6-1
Chenango: Split Oxford 1/2
Delaware: Merge Tompkins 1/2
Erie: Adjust Tonawanda 63/67
Lewis: Split Croghan 2/4, Leyden 1/2
Otsego: Add Oneonta wards; Split Worcester 1/2; Adjust Laurens 1/2
Schuyler: Split Hector 2/5; Adjust Hector 3/6
Seneca: Split Seneca Falls 5/6
Tompkins: Merge Ithaca City 3-1/3-2, Lansing 2/8
Washington: Consolidate Whitehall from 5 to 3 EDs
Wayne: Align Palmyra districts with county maps