2020 Washington precinct and election shapefile.

## RDH Date retrieval
08/31/2021

## Sources
Election results and precinct shapefile from the Washington Secretary of State (https://www.sos.wa.gov/elections/research/election-results-and-voters-pamphlets.aspx)

## Fields metadata

Vote Column Label Format
------------------------
Columns reporting votes follow a standard label pattern. One example is:
G16PREDCli
The first character is G for a general election, P for a primary, S for a special, and R for a runoff.
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
G20PRESLAR - Gloria La Riva (Socialism and Liberation Party)
G20PRESKEN - Alyson Kennedy (Socialist Workers Party)
G20PREOWRI - Write-in Votes

G20GOVDINS - Jay Inslee (Democratic Party)
G20GOVRCUL - Loren Culp (Republican Party)
G20GOVOWRI - Write-in Votes

G20LTGDHEC - Denny Heck (Democratic Party)
G20LTGDLII - Marko Liias (Democratic Party)
G20LTGOWRI - Write-in Votes

G20SOSDTAR - Gael Tarleton (Democratic Party)
G20SOSRWYM - Kim Wyman (Republican Party)
G20SOSOWRI - Write-in Votes

G20TREDPEL - Mike Pellicciotti (Democratic Party)
G20TRERDAV - Duane A. Davidson (Republican Party)
G20TREOWRI - Write-in Votes

G20AUDDMCC - Pat (Patrice) McCarthy (Democratic Party)
G20AUDRLEY - Chris Leyba (Republican Party)
G20AUDOWRI - Write-in Votes

G20ATGDFER - Bob Ferguson (Democratic Party)
G20ATGRLAR - Matt Larkin (Republican Party)
G20ATGOWRI - Write-in Votes

G20LANDFRA - Hilary Franz (Democratic Party)
G20LANRPED - Sue Kuehl Pederson (Republican Party)
G20LANOWRI - Write-in Votes

G20INSDKRE - Mike Freidler (Democratic Party)
G20INSRPAT - Chirayu Avinash Patel (Republican Party)
G20INSOWRI - Write-in Votes

## Processing Steps
In Kittitas County the votes reported as Ellensburg 28 in the Secretary of State results are actually those of Cle Elum 2. Ellensburg 28 was not a distinct voting precinct for the 2020 general election.