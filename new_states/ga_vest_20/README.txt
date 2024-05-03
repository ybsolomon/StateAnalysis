2020 Georgia precinct and election results shapefile.

## RDH Date retrieval
06/29/2021

## Sources
Election results from the Georgia Secretary of State Elections Division (https://sos.ga.gov/index.php/Elections/current_and_past_elections_results). 
Presidential recount results from the Georgia Secretary of State Elections Division via Reuters.
Precinct shapefile primarily from the Georgia General Assembly Reapportionment Office (http://www.legis.ga.gov/Joint/reapportionment/en-US/default.aspx). 
Cobb, DeKalb, and Gwinnett counties instead use shapefiles from the U.S. Census Bureau's 2020 Redistricting Data Program. 
Forsyth and Fulton use shapefiles sourced from the respective counties.

## Fields metadata

Vote Column Label Format
------------------------
Columns reporting votes follow a standard label pattern. One example is:
G20PRERTRU
The first character is G for a general election, C for recount results, P for a primary, S for a special, and R for a runoff.
Characters 2 and 3 are the year of the election.
Characters 4-6 represent the office type (see list below).
Character 7 represents the party of the candidate.
Characters 8-10 are the first three letters of the candidate's last name.

Office Codes

Office Codes

AGR - Agriculture Commissioner
ATG - Attorney General
AUD - Auditor
COC - Corporation Commissioner
COU - City Council Member
DEL - Delegate to the U.S. House
GOV - Governor
H## - U.S. House, where ## is the district number. AL: at large.
INS - Insurance Commissioner
LAB - Labor Commissioner
LTG - Lieutenant Governor
PRE - President
PSC - Public Service Commissioner
SAC - State Appeals Court (in AL: Civil Appeals)
SCC - State Court of Criminal Appeals
SOS - Secretary of State
SSC - State Supreme Court
SPI - Superintendent of Public Instruction
TRE - Treasurer
USS - U.S. Senate

Party Codes
D and R will always represent Democrat and Republican, respectively.
See the state-specific notes for the remaining codes used in a particular file; note that third-party candidates may appear on the ballot under different party labels in different states.

## Fields
G20PRERTRU - Donald J. Trump (Republican Party)
G20PREDBID - Joseph R. Biden (Democratic Party)
G20PRELJOR - Jo Jorgensen (Libertarian Party)

C20PRERTRU - Donald J. Trump (Republican Party)
C20PREDBID - Joseph R. Biden (Democratic Party)
C20PRELJOR - Jo Jorgensen (Libertarian Party)

G20USSRPER - David A. Perdue (Republican Party)
G20USSDOSS - Jon Ossoff (Democratic Party)
G20USSLHAZ - Shane Hazel (Libertarian Party)

S20USSRLOE - Kelly Loeffler (Republican Party)
S20USSRCOL - Doug Collins (Republican Party)
S20USSRGRA - Derrick E. Grayson (Republican Party)
S20USSRJAC - Annette Davis Jackson (Republican Party)
S20USSRTAY - Kandiss Taylor (Republican Party)
S20USSRJOH - A. Wayne Johnson (Republican Party)
S20USSDWAR - Raphael Warnock (Democratic Party)
S20USSDJAC - Deborah Jackson (Democratic Party)
S20USSDLIE - Matt Lieberman (Democratic Party)
S20USSDJOH - Tamara Johnson-Shealey (Democratic Party)
S20USSDJAM - Jamesia James (Democratic Party)
S20USSDSLA - Joy Felicia Slade (Democratic Party)
S20USSDWIN - Richard Dien Winfield (Democratic Party)
S20USSDTAR - Ed Tarver (Democratic Party)
S20USSLSLO - Brian Slowinski (Libertarian Party)
S20USSGFOR - John Fortuin (Green Party)
S20USSIBUC - Allen Buckley (Independent)
S20USSIBAR - Al Bartell (Independent)
S20USSISTO - Valencia Stovall (Independent)
S20USSIGRE - Michael Todd Greene (Independent)

G20PSCRSHA - Jason Shaw (Republican Party)
G20PSCDBRY - Robert G. Bryant (Democratic Party)
G20PSCLMEL - Elizabeth Melton (Libertarian Party)

G20PSCRMCD - Lauren Bubba McDonald, Jr. (Republican Party)
G20PSCDBLA - Daniel Blackman (Democratic Party)
G20PSCLWIL - Nathan Wilson (Libertarian Party)

R21USSRPER - David A. Perdue (Republican Party)
R21USSDOSS - Jon Ossoff (Democratic Party)

R21USSRLOE - Kelly Loeffler (Republican Party)
R21USSDWAR - Raphael Warnock (Democratic Party)

R21PSCRMCD - Lauren Bubba McDonald, Jr. (Republican Party)
P21PSCDBLA - Daniel Blackman (Democratic Party)

## Processing Steps
Three of the four VTDs in Chattahoochee County are comprised of Fort Benning. However, the county only reports one polling location for all voters, including residents of Fort Benning that vote within the county. The four Chattahoochee County VTDs have therefore been merged in the shapefile.

The following additional modifications reflect changes made prior to the 2020 general election.

Barrow: Merge 2/15, 3/12, 4/14, 5/7, 6/10/13, 8/9, 11/16; Adjust new 2/13 boundary
Bartow: Split Cassville/Hamilton Crossing
Candler: Merge Candler/Metter as Jack Strickland Comm Center
Chatham: Split 7-7/8-16, 7-12/7-16; Realign 7-06C/7-07C
Chatooga: Split Cloudland/Teloga along ridgeline that marks boundary between them with the USGS Topographic Contour shapefile
Clayton: Split Ellenswood 1/2, Jonesboro 1/17/19, Lovejoy 3/6/7, Morrow 3/11, 5/10, Oak 3/5 
Cobb: Split Bells Ferry 3/4, Dobbins 1/2, Marietta 3A/3B, Smyrna 3A/3B
Columbia: Split Bessie Thomas/2nd Mt Moriah, Harlem Branch/Harlem Senior Ctr; Merge Blanchard Park/MTZ Col FD;  Align multiple precincts with county maps
Coweta: Merge Arts Centre/Jefferson Parkway as Newnan Centre
Fulton: Merge CP07A/CP07D, CH01/CH04B, SS29A/SS29B, UC031/UC035
DeKalb: Split Clarkston/Clarkston Comm Ctr; Realign Decatur/Oakhurst; Align precincts with Atlanta, Brookhaven, Decatur, Tucker city limits 
Gwinnett: Adjust Baycreek F/G, Berkshire J/M, Cates D/F, Garners C/B, Lawrenceville G/N, Pinckneyville S/T, Rockbridge A/G
Lowndes: Split Northgate Assembly/Trinity, Jaycee/Mt Calvary/Northside/VSU
Oconee: Merge Annex/City Hall; Align City Hall with Watkinsville city limits
Paulding: Reorganize 12 precincts into 19 precincts as redrawn in 2019
Randolph: Merge Carnegie/Cuthbert-Courthouse, 4th District/Fountain Bridge/Shellman
Troup: Split Mountville between Gardner Newman/Hogansville/Rosemont; Align multiple precincts with county maps
Towns: Merge Macedonia/Tate City
Wilkes: Align 1/2A boundary with the voter file
Note that the leading zeros in the Paulding County precinct IDs are included in some election reports and omitted in others. The shapefile includes the leading zeros consistent with the voter file.