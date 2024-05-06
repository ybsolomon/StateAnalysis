2020 Vermont precinct and election results shapefile.

## RDH Date retrieval
01/12/2022

## Sources
Election results from the Vermont Secretary of State (https://vtelectionarchive.sec.state.vt.us/)
Precinct shapefile from the U.S. Census Bureau's 2020 Redistricting Data Program.

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
LAN - Commissioner of Public Lands
LTG - Lieutenant Governor
PRE - President
PSC - Public Service Commissioner
RRC - Railroad Commissioner
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
G20PREDBID - Joseph R. Biden (Democratic Party)
G20PRERTRU - Donald J. Trump (Republican Party)
G20PRELJOR - Jo Jorgensen (Libertarian Party)
G20PREGHAW - Howie Hawkins (Green Party)
G20PREIWES - Kanye West (Independent)
G20PREOOTH - Other Candidates on Ballot
G20PREOSAN - Bernie Sanders (Write-in)
G20PREOWRI - Other Write-in Candidates

G20HALDWEL - Peter Welch (Democratic Party)
G20HALDRBE - Miriam Berry (Republican Party)
G20HALCHEL - Christopher Helali (Communisty Party)
G20HALIBEC - Peter R. Becker (Independent)
G20HALIHOR - Marcia Horne (Independent)
G20HALIORR - Shawn Orr (Independent)
G20HALITRU - Jerry Trudell (Independent)
G20HALOWRI - Write-in Votes

G20GOVDZUC - David Zuckerman (Progressive Party and Democratic Party (fusion candidate))
G20GOVRSCO - Phil Scott (Republican Party)
G20GOVIHOY - Kevin Hoyt (Independent)
G20GOVTPEY - Emily Peyton (Truth Matters Pary)
G20GOVIWHI - Erynn Hazlett Whitney (Independent)
G20GOVIBIL - Wayne Billado III (Independent)
G20GOVIDEV - Michael Devost (Independent)
G20GOVUDIC - Charly Dickerson (Unaffiliated)
G20GOVOWRI - Write-in Votes

G20LTGDGRA - Molly Gray (Democratic Party)
G20LTGRMIL - Scott Milne (Republican Party)
G20LTGPERI - Cris Ericson (Progressive Party)
G20LTGIBIL - Wayne Billado III (Independent)
G20LTGBCOR - Ralph Corbo (Banigh the F-35s Party)
G20LTGOWRI - Write-in Votes

G20ATGDDON - T.J. Donovan (Democratic Party)
G20ATGRPAI - H. Brooke Paige (Republican Party)
G20ATGPERI - Cris Ericson (Progressive Party)
G20ATGOWRI - Write-in Votes

G20SOSDCON - Jim Condos (Democratic Party)
G20SOSRPAI - H. Brooke Paige (Republican Party)
G20SOSPERI - Cris Ericson (Progressive Party)
G20SOSISMI - Pamala Smith (Independent)
G20SOSOWRI - Write-in Votes

G20TREDPEA - Beth Pearce (Democratic Party)
G20TRERBRA - Carolyn Whitney Branagan (Republican Party)
G20TREPERI - Cris Ericson (Progressive Party)
G20TREIWRI - Alex Wright (Independent)
G20TREOWRI - Write-in Votes

G20AUDOHOF - Doug Hoffer (Democratic Party and Republican Party (fusion candidate))
G20AUDPERI - Cris Ericson (Progressive Party)
G20AUDOWRI - Write-in Votes

## Processing Steps
The Census VTD shapefile features city wards. However, precinct boundaries for state and federal elections are not based on city wards. They are instead defined by legislative districts wherever they cross municipal boundaries. Therefore, city wards were merged in the shapefile and cities or townships were instead split into precincts wherever necessary using the state legislative district shapefile.

Essex 2 and Essex 3 are incorrectly labeled in the Census VTD shapefile. The labels and results are switched consistent with the township voting district map.

Vermont has four unorganized towns whose residents cast votes in neighboring towns. These were distributed back based on voting age population in the 2020 U.S. Census. (Averill-Canaan, Buel's Gore-Huntington, Ferdinand-Brighton, Glastenbury-Shaftsbury.)