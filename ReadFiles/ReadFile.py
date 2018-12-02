

class ReadFile:

    def __init__(self, config):
        self.config = config
        self.path = self.config.get__corpusPath()

    @staticmethod
    def _readTextFromFile( filePath):

        file = open(filePath,'r')
        fileText = file.read()
        file.close()
        return fileText


    def readTextFile(self, fileName):
        folderPath = self.path + '\\' + fileName
        filePath = folderPath + '\\' + fileName
        fileAsText = self._readTextFromFile(filePath)
        documents = fileAsText.split('</DOC>')[:-1]
        return documents




    def readAllDocs(self):
        import os
        import re

        counterTotal = 0
        counterWithDocNo = 0
        counterOnlyText = 0
        counterMeter = 0
        counterKM = 0


        listOfFolders = os.listdir(self.config.get__corpusPath())
        listOfFolders.remove(self.config.get__stopWordFile())

        for file in listOfFolders:
            documentList = self.readTextFile(file)



            for documentAsString in documentList:

                topOfText1 = documentAsString[0:int(len(documentAsString) / 6)]
                docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', topOfText1)
                if len(docNo) > 0:
                    docNo = docNo[0].strip(' ')
                    counterWithDocNo += 1
                    onlyText = documentAsString[documentAsString.find('<TEXT>') + len('<TEXT>'):documentAsString.rfind('</TEXT>')]
                    # onlyText = re.findall(r'<TEXT>(.*?)</TEXT>', documentAsString)
                    if len(onlyText) > 20:
                        counterOnlyText += 1
                        if "meter" in onlyText:
                            counterMeter += 1
                        if "km" in onlyText:
                            counterKM += 1


                counterTotal += 1



        print('Total docs:      ',counterTotal)
        print('With docNo:  ', counterWithDocNo)
        print('OnlyText docs:   ', counterOnlyText)
        print('meter count:  ', counterMeter)
        print('km count:  ', counterKM)




#
#
# text = '''
#
#
# Table     of Contents
#
#    JAPAN:  Auto Industry - FEATURE:  Auto Industry Firms Receiving
# Employment Subsidies
#
#    Economic Trends - FEATURE:  Keidanren Role Likely To Change Under
# New Chairman; FEATURE:  Welfare Payment Increases Will Offset Tax
# Cuts for Households; FEATURE:  Economic Organizations Critical of
# MITI 'Interference'
#
#    Environmental Issues - Thirty Small Industrial Waste Companies
# Form Cooperative
#
#    Financial Issues - Nippon Credit Bank Expanding, Introducing U.S.
# Techniques; Banks Considering Establishment of Offices in Hanoi;
# Former MOF Officials May Become Next BOJ Governor, Stock Exchange
# Head; MOF To Require Disclosure of 'Off-Balance Sheet' Transactions
#
#    Foreign Trade and Investment - CHINA -- Japanese Firms Forming
# Broad Range of Joint-Venture Companies
#
#    PHILIPPINES -- Shipping Firm Establishes Subsidiary in Manila
#
#    THAILAND -- Canon To Expand Office Automation Equipment
# Production
#
#    UNITED STATES -- Kobe Steel, TI To Market Cladding Material in
# Japan; Sumitomo Metal To Extend Technical Cooperation to Steel Rod
# Firm
#
#    VIETNAM -- Japanese Firm To Assist Marine Products Processing
# Company
#
#    Machine Tools/Robotics - MT Sales Fell 25 Percent in 1993,
# December Sales Dropped 16 Percent
#
#    Semiconductors/Computers/Electronics - NEC Wins Supercomputer
# Order From Private University; Seiko Epson To Build IC Design-In
# Center in China
#
#    Telecommunications/Satellites - NEC, Mitsui To Build Ground
# Station For Sri Lanka Telecom; NHK Will Lease Circuit on Panamsat
# Satellite; Tokyo Experimental CATV Project To Be Operational by
# 1996; Matsushita Electric Industrial Co., EO Revamp Production
# Agreement
#
#    CHINA:  Domestic Developments - Shanghai Enterprise Ownership
# Composition Changes Through Reform; Textile Shortages, Price
# Increases Forecast in 1994; Bank of China To Introduce Computerized
# Service Network; Shenzhen Calls Halt to Listing of New 'A' Share
# Issues; Shandong Remains Country's Leading Gold Producer; Xiamen To
# Invest in Transport Facilities; Jialing To List Subsidiaries in Hong
# Kong
#
#    Foreign Trade and Investment - Fujian Sets Up Intellectual
# Property Rights Court; Shanghai Exports Exceed Target in 1993;
# Guangzhou To Set Up Individual Foreign Exchange Markets; Foreign
# Investment Estimated at $30 Billion for 1993; Guangdong Foreign-
# Funded Enterprises Expand Export Share; Beijing Views Use of Foreign
# Loans, Donations; Hebei Use of 1993 Foreign Loans; Airbus Signs
# Spare Parts Production Deal; Aerospace Industry Corporation Seeks
# International Cooperation; Stanley Ho Threatens To Halt Mainland
# Investments; China Overseas To Invest in Guangdong Power Plant; Hong
# Kong Firm Holds Two Thirds Shares of Guangdong Power Plant; Xiamen
# People's Income, Foreign Capital Increase; Zhuhai, Singapore Company
# Sign Shipyard Construction Pact; Sino-Thai Project To Produce Suzuki
# Motorbikes in Nanning; Wuhan Iron and Steel Imports Spanish
# Machinery; Tianjin Establishes Joint-Venture Building Materials
# Institute
#
#    Taiwan:  Additional Incentives To Promote Southern Policy; Draft
# Trade Regulations on Hong Kong, Macao; Textile Companies To Invest
# or Expand in Vietnam; Government To Hold Current Tariffs on
# Automobiles, Parts for Now; Imposition of Anti-Dumping Tax on
# Japanese, Korean Polypropylene; MOEA Assesses Impact on
# Manufacturers of Joining GATT; Statistics on Exports to PRC May Be
# Underestimated
#
#    NORTH KOREA:  FEATURE:  DPRK-Chosen Soren Joint Ventures Face
# Continuing Problems
#
#    SOUTH KOREA:  FEATURE:  Patent Office Looks for Countermeasures
# to Patent Disputes; FEATURE:  ROK Efforts in Obtaining Foreign
# Commercial Technology Chronicled; FEATURE:  Electronics Companies
# Focusing on Large Screen TV's; Government Committee Devising NAFTA
# Countermeasures; Study Compares ROK and Japanese Overseas Investment
# Strategies; KDI Approves of Samsung's Entry Into Auto Production;
# Samsung Develops One-Chip Integrated Circuit; Hyundai Motors Opens
# Car Institute; Seoul, Beijing Seeking Industrial Alliance; Companies
# Withdraw From Indonesia Because of Rising Labor Costs; Plant Exports
# to China on Increase; Companies To Participate in Telephone Business
# in Russia; Goldstar Signs Communications Agreement With Romania;
# China Emerges as Major Export Market for ROK Textiles
#
#    SOUTHEAST ASIA:  INDONESIA - FEATURE:  Government Urged To Reduce
# Cost of Economy; FEATURE:  Workers Strike as Government Enforces
# Minimum Wage Decree; Central Bank Needs $400-Million 'Standby Loan';
# Government Discontinues 'Protection' of Steel Industry; P.T. PAL To
# Shift Production Focus; Increase in French Investments Reported;
# Agriculture's Contribution to GDP Drops to 19 Percent
#
#    MALAYSIA:  Contract for Asia Pacific Cable Network Signed
#
#    PHILIPPINES:  Proposals for Satellite Project Reported
#
#    SINGAPORE:  'Largest' Petrochemical Investment Announced
#
#    THAILAND:  Rice Sale to North Korea Reported; Cabinet Approves
# Soybean Import
#
#    VIETNAM:  FEATURE:  Losses in Rice Export Earnings Reported;
# Government To Approve Foreign Construction of Infrastructure
# Projects; Government To Develop 'Core' Groups of State Enterprises;
# Banking Association To Include Domestic, Foreign Banks; Finance
# Ministry Personnel To Study Japan's Securities Industry; Joint
# Venture With French, Chinese Firms To Produce Nylon Cords; Jewelry
# Joint Venture Formed With Japanese Company; Joint Venture With
# Philippine Firm To Build Commercial Complex; Joint Venture With
# Singaporean Company To Provide Hotel Services; Joint Venture With
# Malaysian Firm To Produce Glass Containers; Decrease in Coal Export
# Noted; Singapore's Liang Court Holdings To Invest in Apartment
# Complex; Hanoi Launches First Paging Service; Hong Kong Firm To
# Invest in Da Lat Infrastructure; PetroVietnam To Increase
# Production; Government To Increase Cement Production; Peanut Exports
# Put Vietnam Third Among Exporting Countries; First Phase of Hoa Binh
# Hydroelectric Plant Completed; Rice Joint Venture Accord With Hong
# Kong Company Signed; Construction of Sulfuric Acid Factory Reported;
# Vietnam Airlines Leases Two Airbus Jets From Air France
#
#    (Pacific Rim Economic Review FBPSP 94-05)
#
#    JAPAN:  Auto Industry - FEATURE:  Auto Industry Firms Receiving
# Employment Subsidies -- SUMMARY:  Battered by Japan's prolonged
# economic slump, numerous firms in three auto industry sectors-
# -finished car makers, auto-body manufacturers, and auto parts
# makers--are temporarily shutting down operations and initiating
# "one-time layoffs," according to media reports.  An increasing
# number of large industry firms are joining smaller companies in
# receiving government "employment adjustment subsidies?? to offset
# labor costs associated with the layoffs.
#
#    According to the 6 January NIHON KEIZAI SHIMBUN (NIKKEI), Japan's
# auto industry is ??reeling?? from the fall in domestic demand for
# new cars because of the prolonged recession.  On 5 January, the
# Japan Automobile Dealers Association announced that domestic auto
# sales in 1993 fell for the third straight year to a six-year low.
# Sales of cars (excluding minicars), trucks, and buses totaled
# 4,887,179 vehicles, down 8.4 percent from 1992, and the lowest level
# since 1987.  The paper adds that sales have fallen nearly 18 percent
# from their peak in 1990.
#
#    Auto exports also have fallen sharply.  According to the Japan
# Automobile Manufacturers Association, in January 1994 auto exports
# fell by 26.5 percent compared to January 1993 to 390,418 vehicles,
# the tenth consecutive monthly decline, the 25 February NIKKEI
# reports.  This is the largest drop "since statistics have been
# collected" and the lowest number of vehicles exported in the month
# of January since 1979.  Further, the monthly value of both auto and
# auto parts exports fell 12.6 percent to just over $6.5 billion, the
# fifth consecutive monthly decline, the paper notes.
#
#    Companies Forced To Initiate Temporary Layoffs - According to the
# 20 November 1993 ASAHI SHIMBUN, because of the prolonged slump, the
# auto industry is faced with "excess personnel and production
# capacity."  However, given Japan's lifetime employment system,
# companies are unable to simply fire workers and are looking for
# other means to lower labor costs.  One means companies have resorted
# to, according to ASAHI, is "one-time," or temporary layoffs.  Under
# this arrangement, to reduce production without actually firing
# excess personnel, firms require that designated workers take
# temporary layoffs, during which plant operations are halted.  Firms
# must pay an "operations shutdown allowance" equal to or more than 60
# percent of the employee's average salary, as required by the Labor
# Standards Law.
#
#    To help firms in selected industries during recessionary
# downturns, in 1975 the Japanese Government initiated an "employment
# adjustment subsidy system" through which the Ministry of Labor (MOL)
# pays companies a subsidy to offset labor costs "during temporary
# layoffs, retraining, and employee transfers," ASAHI notes.  To
# receive these subsidies, firms must first be "designated" as being
# in an industry sector experiencing difficulties by the MOL, after
# which the firm must specify the conditions of its temporary layoffs
# and petition the MOL for the subsidies.  This designation is
# effective for 1 year, after which the industry may be redesignated
# by the MOL for another year.
#
#    Large Number of Industry Firms Receiving Employment Subsidies -
# In the auto industry, the auto-body manufacturing sector received
# MOL certification for employment adjustment subsidies in late
# January 1993, according to the 6 February 1993 NIKKEI, following an
# appeal by the Japan Auto-Body Industries Association, which
# represents 218 firms.  The MOL eligibility designation was set to
# expire on 31 January 1994, but, according to the 15 February 1994
# NIKKEI SANGYO SHIMBUN, the MOL "redesignated" the auto-body sector
# for another year.  On 1 May 1993 the finished auto assembly sector
# and the auto parts manufacturing sector were also added to MOL's
# list of industries eligible for employment adjustment subsidies,
# according to the 3 May 1993 NIKKEI WEEKLY.
#
#    Since the designations were made, the number of companies
# utilizing one-time layoffs has been increasing, reports the 15
# February 1994 NIKKEI SANGYO.  According to MOL statistics, the
# number of finished car makers (including some auto-body assembly
# firms) who petitioned for labor adjustment subsidies to pay for
# temporary shutdowns and layoffs mushroomed in late 1993, from five
# firms in November to 21 in December covering 26,785 employees.  As
# these firms halted production, in a ripple effect, an increasing
# number of auto-body and auto parts firms have had to initiate work
# stoppages, NIKKEI SANGYO reports.  The number of auto-body firms
# undertaking work stoppages in November expanded to 12 and then to 20
# firms, while the number of targeted personnel increased from 990 to
# 1,515.
#
#    Auto Parts Firms Particularly Hard Hit - Auto parts manufacturing
# firms have been particularly hard hit by the downturn, according to
# the 27 January NIKKEI SANGYO.  The number of parts companies
# planning work stoppages more than doubled, from 136 firms in October
# to 280 in November, while the number of employees involved jumped
# from 30,382 in October to 79,201 in November.  Further, according to
# the 15 February NIKKEI SANGYO, the numbers increased again from
# November to December, from 280 to 361 firms.  NIKi?I SANGY0 adds
#                                                  ?
# that the finished car and auto parts industries do not expect the
# number of firms requesting subsidies to fall "any time soon."
# Press Reports on Companies Initiating Layoffs, Requesting
# Subsidies - Although a number of small auto industry firms applied
# for subsides soon after the MOL made its designations, until October
# 1993 no major company had applied.  Subsequently, a number of larger
# auto-related firms plans to initiate temporary layoffs and apply for
# employment adjustment subsidies.  According to press reports, the
# following companies have initiated temporary layoffs and have
# received employment adjustment subsidies:
#
#    Nissan Motor Co.--According the 26 October MAINICHI SHIMBUN,
# Nissan announced plans to apply for subsidies after revealing that
# it would stop production for two days in November on one line at its
# Tochigi assembly plant, which employs 6,500 people, and institute
# temporary layoffs on those days to 2,100 production workers.  In
# November, Nissan announced it would expand the scope of temporary
# layoffs to include "virtually all" domestic production lines.  The
# 18 November MAINICHI SHIMBUN reports that Nissan decided to target
# nearly 15,000 employees and five plants for two-day shutdowns in
# December, which would cut production by nearly 4,000 vehicles.
#
#    In December, Nissan announced it would continue to conduct
# temporary layoffs and production shutdowns in January and February,
# according to the 18 December YOMIURI SHIMBUN.  In January, Nissan
# had shutdowns for three days at its Murayama and Yokohama plants,
# two days at its Tochigi plant, and one day at its Kyushu plant.  In
# February the company planned layoffs for two days at its Tochigi and
# Kyushu plants and one day at the Murayama plant.  According to
# YOMIURI, the Murayama plant will have been closed six days during
# four consecutive months of temporary shutdowns.
#
#    Mazda Motor Corp.--According to the 26 October MAINICHI, Mazda
# decided to initiate temporary layoffs of two days in November for
# 25,000 of its nearly 30,000 employees throughout the country.
# MAINICHI reports that Mazda also applied for employment adjustment
# subsidies.  The 25 December Y0MIURI SHIMBUN reports that Mazda,
# following its November layoffs, planned to have four days of layoffs
# in January at its Hofu plant.  Mazda, which is heavily dependent on
# exports, has seen its sales fall for fourteen consecutive months.
#
#    Nissan Diesel Motor--According to the 23 November 1993 NIKKEI,
# Nissan Diesel, a heavy-duty truck and bus manufacturer, announced it
# would initiate two days of temporary layoffs involving nearly 3,700
# employees at three different plants.  The company also stated it
# would apply for government employment adjustment subsidies, and also
# announced it had reached agreement with its labor unions to cut
# yearend bonuses.
#
#    Sumitomo Wiring Systems--The 26 January 1994 CHUBU SHIMBUN
# reports that Sumitomo Wiring Systems, the third largest manufacturer
# of auto wire harnesses, will initiate one-day shutdowns in February
# and March, affecting more than 4,700 employees.  The firm plans to
# apply for employment adjustment subsidies from the MOL.  The
# shutdowns will cover all of the company's offices and eight plants
# in Japan.  It has seen orders for wire harnesses, which account for
# over 90 percent of total sales, plummet nearly 20 percent since
# 1990.  If orders do not recover soon, the firm may extend its
# planned shutdowns beyond March.
#
#    Tsuchiya Manufacturing Co.--According to the 24 January 1994
# NIKKEI SANGYO, Tsuchiya, an auto parts maker affiliated with Nissan,
# plans to stop production for two days a month at its main plant in
# Kawasaki City.  During this time, the salary of full-time employees
# will be covered by employment adjustment subsidies, but the salaries
# of temporary and part-time employees will be reduced on a prorated
# basis.  The Kawasaki plant, which among other things produces fuel,
# oil, and air filters, accounts for nearly one-third the firm's total
# sales.  The work stoppages will continue "until demand for auto
# parts has recovered," according to company officials.  Further, the
# company is considering work stoppages at other plants where
# productivity is low.
#
#    Other Suppliers Receiving Subsidies Under Different Designations
# - Other major suppliers to the auto industry have resorted to
# temporary layoffs and have accepted employment adjustment subsidies
# under other industry designations.  Two major examples, from the
# rubber and steel industry, are as follows:
#
#    Bridgestone Corp.--The 3 December 1993 NIKKEI reports that
# Bridgestone, the world's second largest tire manufacturer, announced
# that it would initiate three and four days of temporary layoffs at
# the end of December at nine of the its ten tire plants in Japan.
# The firm will also apply for subsidies.  Layoffs could cover 9,500
# employees, or nearly 60 percent of the firm's total payroll.
#
#    According to NIKKEI, the tire industry received its MOL
# designation at the end of November, and "this is the first time
# temporary layoffs have taken place in the tire industry."  Earlier,
# Bridges tone decreased the number of operating days from seven to
# five per week, but even this measure failed to compensate for the
# "severe" drop in demand for tires.
#
#    Daido Steel Co.--The world's largest maker of specialty steel and
# a major supplier to the auto industry, particularly to Nissan, Daido
# announced it would receive subsidies for temporary layoffs of nearly
# 4,000 personnel at four plants at the end of December and in early
# January, according to the 11 December 1993 YOMIURI SHIMBUN (Chubu
# edition).  While the firm had undertaken temporary layoffs at its
# Kawasaki plant, this is its first "large-scale" employment
# adjustment.  Daido's sales have fallen for three consecutive years.
#
#    Economic Trends - FEATURE:  Keidanren Role Likely To Change Under
# New Chairman -- SUMMARY:  On 7 February the Federation of Economic
# Organizations (Keidanren) selected Shoichiro Toyoda, chairman of
# Toyota Motor Corp., to succeed Gaishi Hiraiwa as Keidanren chairman,
# according to press reports.  While Toyoda chairs Japan's largest
# manufacturing firm, some industrial leaders express concern whether
# he can successfully lead Japanese industry because of his
# personality and Toyota's unusual corporate culture.  The press
# anticipates that under Toyoda's leadership, Keidanren will become an
# ordinary economic organization" representing the interests of
# private business, rather than acting as a coordinator between
# politicians, bureaucrats, and the business community.
#
#    On 7 February Keidanren chose Shoichiro Toyoda (68 years old),
# chairman of Toyota Motor Corp. and a Keidanren vice president, to
# succeed Gaishi Hiraiwa when he steps down as Keidanren chairman in
# May, according to the 8 February NIKKEI SANGYO SHIMBUN.  (The
# company name is rendered "Toyota"; the legal family name is
# "Toyoda.")  While industrial leaders generally welcomed Toyoda's
# selection, they also expressed concern, based on his background as
# the owner and chairman of Toyota Motor, according to the 8 February
# MAINICHI SHIMBUN.  The 8 February NIKKEI SANGYO quotes an
# unidentified industrial leader as questioning Toyoda's ability to
# break free from "Toyota egoism" and lead Japanese industry from a
# "broader viewpoint."  Writing in the 10 February NIKKEI SANGYO,
# editorial staff writer Atsushi Suemura asks whether the head of
# Toyota, which is often said to have a "Mikawa (the old name for
# Aichi Prefecture) Monroe doctrine--we don't interfere with you, so
# don't you interfere with us"--is qualified to lead the entirety of
# Japanese industries.
#
#    The 8 February NIHON KEIZAI SHIMBUN (NIKKEI) reports on the
# expectations--"which also reflect the concerns "--industrial leaders
# have concerning Toyoda.  Masaru Hayami, chairman of Japan's
# Association of Corporate Executives (Keizai Doyukai), states that he
# wants Toyoda to exhibit strong leadership "apart from the interests
# of the auto industry."  Kosaku Inaba, chairman of the Japan Chamber
# of Commerce and Industry, says that the key lies in "how well Toyoda
# can balance" the interests of various industries and the interests
# of consumers and corporate shareholders, not as the manager of
# Toyota Motor, which has "always defended the interests of Toyota and
# the auto industry," but as a leader of all industries.
#
#    Concerning Japan-U.S. trade issues, Yoshinari Yamashiro, chairman
# of steel firm NKK Corp., notes that Japan-U.S. friction "is the
# Japan-U.S. automobile problem," according to the 8 February NIKKEI,
# implying that Toyota Motor should change its corporate philosophy
# and behavior to ease Japan-U.S. trade friction.  The article adds
# that Toyota Motor "symbolizes" Japan's large trade surplus.
#
#    Where Will Keidanren Go Under Toyoda's Leadership? - Writing in
# the 15 January ASAHI, economic reporter Yomei Tsuji speculates that
# Keidanren may become an "ordinary economic organization" under
# Toyoda's leadership.  Tsuji assumes that Keidanren will abandon its
# function of channelling corporate political contributions to the
# political parties.  Since Toyota Motor has devoted itself to
# manufacturing and selling cars from its Aichi Prefecture base and
# has avoided involvement in politics in Tokyo, Tsuji expects Toyoda
# to be effective in "changing Keidanren's relationship with
# politicians."
#
#    In addition, unlike previous Keidanren chairmen who came from the
# steel, heavy machinery, or electric power industries, industry
# sectors which were "sponsored" by the government, Toyoda is a
# representative of "true" private sector firms in Japan.  A change in
# Keidanren's chairmanship from a leader of state-sponsored industry
# to a private industry leader, Tsuji maintains, means that Japan's
# economy has been "taken from the government's hands."  He also notes
# that since Toyoda comes from the auto industry, which must sell to
# consumers directly, Keidanren under Toyoda is expected to pay more
# attention to consumer interests, unlike his predecessors, who spoke
# about "national interests" as leaders of "Japan Inc."
#
#    Writing in the 8 February NIKKEI, editorial staff writer Kazuo
# Mori notes that Toyoda's Keidanren will no longer play the role of
# coordinating interests between industry, the politicians, and
# bureaucrats.  Indeed, now it will be difficult for Keidanren to
# coordinate interests even within private industry.  Mori notes that
# Toyota is an "owner-managed firm, which tends to compete fiercely
# and to pursue only its own interests,'' even though it has become a
# giant."  He observes that the Keidanren's selection of Toyoda
# indicates that "competition based on market principles" will be
# emphasized by corporations more than ever.  Japanese practices that
# hinder competition, Mori notes, such as implementing policies
# through discussions among political, bureaucratic, and industrial
# circles, "will be avoided."
#
#    Press Urges Toyoda's Keidanren To Promote Deregulation - On 7 and
# 8 February, NIKKEI, SANKEI SHIMBUN, ASAHI, MAINICHI, and YOMIURI
# carried editorials on Toyoda's selection.  All the editorials urge
# Keidanren under Toyoda's leadership to promote deregulation.  For
# example, ASAHI points out that Japan's auto industry has grown to
# the level of the U.S. auto industry because of "self-initiated
# technical innovations and rationalization efforts," not by support
# from the government, and urges Toyoda to "boldly promote
# deregulation."  MAINICHI, noting that Toyoda himself was a member of
# the Hiraiwa Study Group, urges him to take the initiative in
# pressing the government to implement the Hiraiwa Report and "further
# promote deregulation."  YOMIURI also asks Toyoda to promote
# deregulation to change Japan's economic structure, under which
# corporations compete for market share or conduct business in a
# collusive manner."
#
#    SANKEI's editorial notes that Keidanren also must change its role
# of being a coordinator between government and industry to being "a
# representative of private companies."  Through channelling corporate
# contributions to the Liberal Democratic Party (LDP) the past 40
# years, Keidanren has "directly and indirectly influenced government
# policy formulation," but it now has to "deal directly with
# government regulators."    The editorial urges the Keidanren under
# Toyoda "not be passive" toward the government concerning regulations
# and administrative guidance, but rather "assert its opinions and act
# as the leader of private firms in protecting private sector
# vitality."
#
#    Profiles Note Similarities Between Toyoda, Hosokawa - The 17
# January CHUNICHI SHIMBUN points out the many similarities between
# Toyoda and Prime Minister Morihiro Hosokawa, such as being from a
# well-known family, from a regional city, and "somewhat amateurs in
# their respective new fields," but also observing that "the era
# requires such leaders."  Toyoda is from a rich family--the eldest
# grandson of Toyota founder Sakichi Toyoda--and has reached his
# current position "without any political or financial support from
# the outside."  He is viewed as an honest and sincere person, the
# paper notes, "but not a tactician or a charismatic leader."  Since
# he has been far removed from Tokyo, Toyoda reputedly has not been
# involved in politics and "is not close to a political party or
# politicians."  He is also viewed as an "amateur" industrial leader,
# because he had not been involved in the activities of any economic
# organization before becoming a Keidanren vice chairman in 1990.
# Toyoda has a doctorate in mechanical engineering and is an
# accomplished engineer.
#
#    According to the 8 February CHUNICHI, Toyoda's stances on various
# issues are as follows:
#
# --Political contributions:  Toyoda thinks politicians should receive
# government support and individual contributions rather than
# contributions from business.  He realizes this will "disconnect"
# collusion within in the so-called "iron triangle" of politicians,
# bureaucrats and corporations.
#
# --Japan-U.S. trade:  Toyoda believes that Japan and the United
# States should build a trade relationship based on "harmony and
# competition."  He has opposed setting numerical targets for Japan's
# imports of automobiles and auto parts.
#
# --Economic structural reform:  He believes that corporations should
# promote self-help efforts to restructure themselves as their own
# responsibility, while the government should make the Japanese market
# more open and fair by deregulation.
#
#    FEATURE:  Welfare Payment Increases Will Offset Tax Cuts for
# Households -- SUMMARY:  Japan's proposed increases in welfare and
# national annuity premium rates will lessen the stimulative effects
# of the government's proposed income tax cuts on the consumption of
# working households, according to press reports.  The total increase
# in premium payments is estimated to be equivalent to one-fourth the
# total estimated gain in disposable income from the income tax cuts,
# thus largely offsetting tax cuts for average-income working
# households.  The Ministry of Health and Welfare (MHW) claims, on the
# other hand, that retirees will receive annuity increases that
# slightly exceed the total amount of premium increases.
#
#    The MHW has drafted a bill to reform the welfare annuity program
# (for private sector wage earners) and the national annuity program
# (for the self-employed, students, and people without jobs) which
# includes premium rate increases in FY94, according to the 18
# February NIHON KEIZAI SHIMBUN (NIKKEI). The draft bill will be
# submitted to the Diet in mid-March for deliberation.  According to
# the MHW draft, the welfare annuity premium rate will increase from
# the current 14.5 percent (split equally between employer and
# employee) to 16.5 percent of monthly salaries effective in October
# 1994, increasing to 17.35 percent effective October 1995, and a new
# payment of 1.0 percent (split between employer and employee) of each
# bonus payment effective in April 1995.  Regarding the national
# annuity premium, the current premium amount, which is a fixed 10,500
# yen ($100), will be raised to 11,100 yen ($106) per month effective
# April 1994.
#
#    The 26 February NIKKEI reports that total welfare and national
# annuity premium payments by working households will increase by 1.4
# trillion yen ($13.3 billion) a year, which is nearly equivalent to
# one-fourth the estimated 5.5 trillion yen ($52.4 billion) in income
# tax cuts specified in the 8 February economic stimulus package.
# According to MHW's calculations cited by NIKKEI, the total amount of
# welfare annuity premiums will increase by approximately 2.6 trillion
# yen ($24.8 billion) a year, assuming an average worker's monthly
# salary of 340,000 yen ($3,200) and 33 million wage earners.  Of this
# 2.6 trillion yen ($24.8 billion), 1.3 trillion yen ($12.4 billion)
# will be paid by wage earners, since employers and employees equally
# split premium payments.  The MHW also anticipates that total
# national annuity premiums will increase by 100 billion yen ($952
# million) a year.
#
#    Premium Hikes Will Wipe Out Tax Cut Gains for Average-Income
# Families - According to the 15 February NIKKEI, working households
# with annual incomes below 6 million yen ($57,000) will realize
# little benefit from the income tax cuts due to increases in annuity
# premium payments and other public levies.  Moreover, while the
# income tax cuts are only for FY94, the premium increases "will be
# permanent."  In the case of a household with an annual income of 6
# million yen ($57,000) or below, an income tax cut of around 71,400
# yen ($680) or less "will be largely offset by the increased welfare
# annuity premium payments."  Although the MHW claims that welfare
# annuity recipients over 60 years of age will receive 5 percent more
# in benefits from FY94, and therefore the total household disposable
# income will increase by 3 trillion yen ($28.6 billion), NIKKEI
# argues that incomes will increase "at the cost of increased burdens
# for all working households."
#
#    More broadly, the NIKKEI article notes that FY94 may be a "losing
# year" for working class households with children in school, since
# postal rates have recently increased; a 9-percent increase in
# national university tuition has been proposed for 1995; and an
# increase in Tokyo expressway tolls has been proposed.  The paper
# concludes that even when workers want to have a bottle of beer after
# a hard day's work, a 8.9 yen ($.08) tax increase per bottle will
# "hurt their thin wallets."
#
#    FEATURE:  Economic Organizations Critical of MITI 'Interference'
# -- SUMMARY:  The Ministry of International Trade and Industry (MITI)
# reportedly faxed a memorandum to four major private economic
# organizations summarizing the "important points" of the latest
# government economic stimulus package as well as "model comments" to
# be made by the heads of the four organizations before the Hosokawa
# Cabinet approved the package on 8 February, according to press
# reports.  A NIH0N KEIZAI SHIMBUN article on 15 February reported
# that the economic organizations were very critical of MITI's
# "interference" concerning comments by their leaders.  An editorial
# in that newspaper the same day sharply criticizes MITI for
# "excessive guidance" of the private sector, observing that it is
# "quite ironic" that under the Hosokawa administration, which
# advocates deregulation, the bureaucrats' control of the private
# sector "appears to have been strengthened."
#
#    Major economic organizations are very critical of MITI's
# "interference" concerning comments by their leaders on government
# economic policies, according to the 15 February NIHON KEIZAI SHIMBUN
# (NIKKEI).  MITI reportedly faxed a memorandum summarizing the
# "important points" of the latest government economic stimulus
# package and "model comments" to the offices of four leading private
# sector economic organizations--the Federation of Economic
# Organizations (Keidanren); the Japanese Association of Corporate
# Executives (Keizai Doyukai); the Japan Federation of Employers'
# Association (Nikkeiren); and the Japan Chamber of Commerce and
# Industry--on the afternoon of 8 February, a few hours before the
# Hosokawa Cabinet approved the stimulus package.  The fax reportedly
# emphasized the "importance" of "praising measures like the income
# tax cut" and "supporting the government's policy" of cutting direct
# taxes and increasing indirect taxes.  According to the NIKKEI
# article, the "model comments" for use by the heads of the four
# economic organizations included:  "We highly praise the courageous
# decisions of the government and coalition to include an income tax
# cut in the stimulus package."
#
#    Although MITI defended its action with the assertion that it
# never intended to force" the organizations to use MITI's comments,
# NIKKEI reports that the economic organizations are "annoyed" by the
# fax, which "sounded like an order" for them to use MITI's comments.
# The article notes that "this is the first instance" of MITI actually
# sending a document instructing the economic organizations what to
# say, although in the past MITI telephoned them to request that they
# make comments "favorable" to MITI.
#
#    According to a "source connected with an economic organization"
# cited by NIKKEI, "bureaucratic interference" concerning comments by
# leaders of the economic organizations "assumed prominence" in
# December 1993, when Jiro Saito, Ministry of Finance vice minister,
# and Hideaki Kumano, MITI vice minister, visited the four
# organizations to "explain" the government's policy of income tax
# cuts to be paid for by increases in the consumption tax.
#
#    Editorial Blasts Fax as Example of MITI's 'Excessive Guidance' -
# NIKKEI's 15 February editorial, which is headlined "Appalled by
# MITI's Excessive Guidance," is very critical of MITI, noting that
# its fax "reminds us of an 'education mama' teaching a two-year-old
# with simple words."  However, it observes, "the postwar period, in
# which Japanese industries were rebuilt under strong MITI guidance,
# has already ended."  "MITI's excessive guidance," the editorial
# continues, is an "extreme anachronism."  "MITI may think that it can
# freely control private economic organizations with its guidance, but
# such presumptuousness is no longer acceptable."  The editorial urges
# MITI to "realize that excessive guidance is now one of the causes
# hindering the vitality of Japanese industries."
#
#    The editorial also points out that MITI's fax "may be cited by
# the U.S. Government" to prove its assertion that "bureaucrats
# control the Japanese economy."  It notes that during the recent
# Japan-U.S. framework talks, the U.S. Government criticized Japanese
# bureaucrats for "controlling the Japanese economy and hindering
# deregulation."
#
#    The editorial concludes that it is "quite ironic" that under the
# Hosokawa administration, which advocates deregulation, bureaucrats
# "are gaining more power" and their control of the private sector
# "appears to have been strengthened."  The editorial demands that
# MITI "reflect gravely on its conduct."
#
#    Environmental Issues - Thirty Small Industrial Waste Companies
# Form Cooperative -- About 30 small-scale manufacturers of industrial
# waste treatment equipment and industrial waste disposal companies
# from the Tokyo Metropolitan Area and Nagano, Kanagawa, and Shizuoka
# Prefectures have joined together to form a cooperative association
# which will pursue contracts for building final industrial waste
# disposal facilities and conducting R and D activities.  The
# "Cooperative Association for Promoting Environment-Related
# Enterprises" will be established with an investment of 10 million
# yen ($96,000) and will be chaired by Yoshinori Ito, president of
# Kankyo Seibi Shinko, an environmental equipment firm.
#
#    The companies decided to form this "unique" cooperative because
# as independent firms, each has limited financial resources and thus
# can not qualify for special programs sponsored by public
# corporations, such as the Japan Environment Corporation, to finance
# work for improving disposal facilities to conform with stricter
# environmental regulations.  The cooperative plans to expand its
# membership to about 1,000 companies and establish a network of
# branch chapters throughout the country.  (Tokyo NIKKAN KOGYO SHIMBUN
# 17 Feb 94 p 12)
#
#    Financial Issues - Nippon Credit Bank Expanding, Introducing U.S.
# Techniques -- Nippon Credit Bank (NCB), the newest and smallest of
# Japan's three long-term credit banks, has established a wholly-owned
# trust banking subsidiary that will begin operations in April 1994,
# according to the 1 March NIKKEI KINYU SHIMBUN.  It will be the
# seventh financial institution, after the "big four" securities
# companies and two banks, to enter the trust banking business through
# a financial subsidiary.  Capitalized at 5 billion yen ($48 million)
# and with 15 employees, the new subsidiary will begin buying real-
# estate trusts and bank loans for resale.
#
#    NCB also established a "financial development division" within
# its Planning Department in February to engage in real-estate project
# finance and asset securitization, according to the 18 February
# NIKKEI KINYU.  The new division will offer advice to customers on
# how to securitize their assets through trust banking or by setting
# up special-purpose companies, and will introduce the securitized
# products to its large bank bond purchasing customers.  For now the
# division will focus on assisting in the securitization of a
# customer's better assets, but in the future it will expand to
# nonperforming loans, as is done by U.S. investment banks.
#
#    Establishing the new division is NCB's first step in expanding
# commission-earning operations that fully exploit the financial
# engineering techniques used by U.S. investment banks.  The new
# division will work in concert with NCB's new trust bank subsidiary
# in promoting business.  By bringing its customers financial
# engineering techniques from the United States, "smooth fund-raising
# will become possible" for real estate  financing.
#
#    In addition, NCB is also building up its system of developing new
# derivative products, such as options, futures and swaps, by
# establishing a product-development team, according to the 25
# February NIKKEI KINYU.  The team's objective is to facilitate
# product development by addressing the need of institutional
# investors and average companies to hedge against interest rate and
# currency risks.  The team will be located at NCB's interest-rate
# swap trading desk, the first time a long-term credit bank has set up
# a product-development team at a trading desk.  Product development
# and marketing will be streamlined, with a single person in charge of
# both. This official will concentrate on developing products for the
# portfolio management of manufacturers, not Just securities and
# insurance companies.
#
#    Although many banks separate their dealing sites and development
# divisions, product development is easier at a trading desk because
# there dealers can collect the hedging know-how of major commercial
# and foreign banks.  NCB expects to be able to reduce the time it
# takes to develop a product, such as swap-related products, from
# design to completion in half the time this took previously.  NCB
# plans to sell these products not only to institutional investors but
# also to average companies.
#
#    Banks Considering Establishment of Offices in Hanoi - Several
# Japanese commercial banks are considering opening offices in Hanoi.
# The Bank of Tokyo, Sakura Bank, Fuji Bank, Tokai Bank, and Daiwa
# Bank, which have already opened representative offices in Ho Chi
# Minh City, have also begun looking into opening offices in Hanoi,
# Vietnam's financial administration center.  These banks are expected
# to set up operations in Hanoi "in the next two or three years" in
# response to the growing number of foreign banks opening offices in
# both cities.  Sanwa and Sumitomo banks, which are planning to open
# representative offices in Ho Chi Minh City in the spring of 1994,
# are expected to join the others in establishing Hanoi offices in the
# future.
#
#    The banks are considering several ways of establishing bases in
# Hanoi, including establishing representative offices, local offices,
# or liaison offices of their Ho Chi Minh City representative offices.
# Of the 30 or more non-Japanese foreign banks that have begun
# operations in Vietnam, roughly one-third have bases in both cities
# in the form of a branch offices, representative offices, or local
# offices.  (Tokyo NIKKEI KINYU SHIMBUN 16 Feb 94 p 2)
#
#    Former MOF Officials May Become Next BOJ Governor, Stock Exchange
# Head - Mitsuhide Yamaguchi, president of the Export-Import Bank of
# Japan (Ex-Im Bank), who entered the Ministry of Finance (MOF) in
# 1951 and rose to  become vice minister in 1984, is rumored to be the
# probable candidate to succeed Bank of Japan (BOJ) Governor Yasushi
# Mieno in December 1994 when Mieno's term ends.  In recent years the
# BOJ governorship has alternated between former MOF vice ministers
# and BOJ "careerists."  Since Mieno is a BOJ careerist, the next
# governor is likely to be a former MOF vice minister.  Although
# appointing the BOJ governor is the prerogative of the prime
# minister, the incumbent MOF vice minister customarily recommends a
# candidate to the prime minister, who "almost automatically
# approves."
#
#    Although Yamaguchi is rumored to be the probable candidate, the
# MOF, BOJ and banking industry officials "are not completely sure
# yet."  They question whether the Hosokawa administration will last
# until December, when Mieno steps down, and if Prime Minister
# Morihiro Hosokawa's "advocacy of reforms" might lead to changes in
# the selection process.  There have been several instances in the
# past where the personal desires of prime ministers altered the
# selection process.  One example was Prime Minister Masayoshi Ohira's
# selection of Haruo Maekawa, then vice president of the Ex-Im Bank,
# over MOF candidate Satoshi Sumita, president of the Ex-Im Bank at
# that time.  As a result, Sumita had to wait for five years before
# getting his chance.
#
#    BOJ officials have been resistant to the custom whereby every
# second BOJ governor is a former MOF vice minister.  A senior BOJ
# official is quoted as saying that the BOJ governor needs to have a
# "sustainable and medium-term viewpoint" of the economy and be strong
# enough to implement monetary policies from such a viewpoint,
# "regardless of what the public at large may say," implying that
# being a former MOF vice minister in itself is not a sufficient
# qualification to be BOJ governor.  Some banking industry officials
# are also concerned that former MOF bureaucrats tend to compromise
# too easily with politicians.  They are also concerned that former
# MOF officials tend to adhere to MOF--not BOJ--"priorities" and
# subject monetary policy to the MOF's fiscal objectives.
# Yoshino Rumored To Be Next TSE Board Chairman - Yoshihiko
# Yoshino, president of the Japan Development Bank, who entered the
# MOF in 1953 and became vice minister in 1986, most likely will
# succeed Minoru Nagaoka, chairman of the Tokyo Stock Exchange (TSE)
# Board of Directors, when Nagaoka steps down in May.  The
# chairmanship has been filled by former MOP vice ministers since
# 1965, when the TSE invited former MOF vice minister Teiichiro
# Morinaga to restore financial health to the securities industry
# following the so-called "securities recession" of the mid-1960's.
# Since likely candidates from within the securities industry have
# been tainted by the stock-loss compensation scandals of 1991, it is
# highly likely that a former MOF vice minister will become the next
# TSE chairman.  Nagaoka has been quoted as saying that since current
# MOF Vice Minister Jiro Saito "plans and decides personnel moves of
# all former MOF bureaucrats," Saito will select a candidate from
# among the available former MOF vice ministers.  Then, the candidate
# will be nominated by the TSE Board of Directors and officially
# elected by two-thirds of all TSE members.
#
#    Within the securities industry, however, there is strong
# resistance to the chairmanship becoming a "reserved seat" for former
# MOF vice ministers.  The president of a major securities house
# states that "the securities industry is now capable of voluntarily
# promoting fairness and transparency in the stock market," so that
# the industry "no longer needs influential MOF retirees."  Another
# reason for the strong resistance is that the securities industry was
# not happy with Nagaoka, who, in the industry's view, "adopted the
# MOF's position," rather than representing the securities industry,
# during the series of securities scandals that began in 1991.  This
# viewpoint was particularly evident concerning the issue of
# establishing a securities industry watchdog organization.  Nagaoka
# supported the MOF's idea of establishing the Securities Exchange
# Surveillance Commission within the MOF, instead of an independent
# organization similar to the U.S. Securities and Exchange Commission,
# which the industry sought.  (Tokyo ASAHI SHIMBUN 17 Feb 94 p 11)
#
#    MOF To Require Disclosure of 'Off-Balance Sheet' Transactions -
# The Ministry of Finance (MOF) has decided to require financial
# institutions to disclose information on the status of their so-
# called "off-balance sheet" transactions.  The MOF has determined
# that the nontransparency of financial transactions not currently
# included in a financial institution's balance sheet--so-called "off-
# balance sheet" transactions," such as unlisted futures, swaps, and
# options--and the concomitant risk of such transactions can cause
# enormous instability to the Japanese financial system as a whole.
# Consequently the MOF will reconvene its special advisory panel in
# March to study the issue in detail.
#
#    "Off-balance sheet" transactions use cutting-edge financial
# engineering techniques to allow financial institutions to hedge
# against risk.  Compared to more traditional financial instruments
# such as loans, off-balance-sheet transactions are conducive to
# large-volume trading across national borders and have a
# destabilizing effect internationally when a contract default occurs.
# Overseas off-balance-sheet transactions of Japanese financial
# institutions are said to be ballooning, which is one reason why the
# Bank for International Settlements (BIS) is calling for their
# thorough disclosure and methods of managing the concomitant risks.
#
#    Some of the issues the MOF advisory committee, "The Working
# Subcommittee on Financial Institution Disclosure," will consider
# are:  whether it can establish a means for market-value assessment
# of unlisted "off-balance-sheet" financial products; whether risk
# assessment of all counterparts to off-balance-sheet transactions and
# comprehensive risk assessment are possible; whether overseas
# transactions are to be disclosed as well; and whether there is a
# method to demonstrate risk management methods that financial
# institutions are already using.  (Tokyo NIKKEI KINYU SHIMBUN 24 Feb
# 94 p 1)
#
#    Foreign Trade and Investment - CHINA:  Japanese Firms Forming
# Broad Range of Joint-Venture Companies -- Japanese economic
# newspapers in recent weeks have reported the formation of joint
# venture (JV) companies and other corporate tie-ups in China that
# involve a wide range of industrial sectors.
#
#    Manufacturing Sector - Nippon Alkyl Phenol, a Japan-based JV
# company organized by Mitsui Petrochemical Industries, the Swiss
# chemical company Ciba-Geigy, and Musashino-Geigy, will sign an
# agreement in the near future with Gaoqiao Petrochemical Company, a
# major Chinese petrochemical manufacturer, establishing a JV company
# in Shanghai to build a plant to manufacture a resin additive which
# uses alkyl phenol as a feedstock.  The investment ratio in the JV
# will be Nippon Alkyl Phenol 75 percent and Gaoqiao Petrochemical 25
# percent.
#
#    The new company will invest 10 billion yen ($95.2 million) to
# build a resin additive plant in South China with an annual capacity
# of 2,500 tons.  The alkyl phenol used in the production of the
# additive, which is an antioxidant and ultraviolet radiation
# absorbing agent used in resins such as acrylonitrile butadiene
# styrene, will be shipped from Nippon Alkyl Phenol's plant located in
# Mitsui Petrochemical's Chiba plant complex.  (Tokyo NIKKAN KOGYO
# SHIMBUN 7 Feb 94 p 1)
#
#    Shiko Technical Research--The world's largest manufacturer of
# cooling fans used in notebook computers, Shiko has begun full-scale
# operations at two JV plants in China.  The factories, located in
# Shanghai and Wenzhou, Zhejiang Province, were completed in December
# 1993 and employ about 100 workers each.  Shiko projects that sales
# in FY94 from the two plants will be 1-2 billion yen ($9.5-$19
# million), which would about double their FY93 sales of 1.4 billion
# yen ($13.3 million).
#
#    The Shanghai plant will produce cooling fans for personal
# computers and sell them to major electronics manufacturers in
# Taiwan.  Production will be contracted out to the Shanghai Video
# Recorder Equipment Factory until Shiko officially decides on a
# partner in May.  The Wenzhou JV plant, the "Wenzhou Golden Dragon
# Shiko Company," will make vibration motors for pagers which will be
# sold to Motorola and to Casio Computer's plant in Tianjin.  The JV
# partner will be an individual.  With the establishment of these
# foreign production bases, Shiko will implement a policy of "domestic
# production for domestic sales and foreign production for foreign
# sales."  (Tokyo NIKKAN KOGYO SHIMBUN 16 Feb 94 p 26)
#
#    Juken Sangyo, a second-tier manufacturer of processed wood
# products, together with the general trading company Nissho Iwai,
# will establish a wood products manufacturing and sales JV company in
# Shanghai in April.  The company, Juken Nissho China, will be
# capitalized at $5 million, with Juken investing 85 percent and
# Nissho Iwai 15 percent.  The JV has obtained a 50-year lease from
# the Chinese Government on a 5-hectare site in Shanghai's Baoshan
# District.  Total investment, including plant and equipment, will be
# about $10 million.  The JV plant, scheduled to begin operation in
# February 1995, will use imported wood from Southeast Asian countries
# such as Myanmar, will cut lumber, and will manufacture plywood for
# export to Japan and for sale in China.  (Tokyo NIKKAN KOGYO SHIMBUN
# 16 Feb 94 p 19)
#
#    Engineering Design, Transport, and Printing Services - Mitsubishi
# Heavy Industries (MHI) and Mitsubishi Corp. will establish a JV
# company on 1 April with the Baoshan Iron and Steel Co. to carry out
# the design work for Baoshan's No. 2 rolling mill.  The JV
# company, "Shanghai Bao-Mitsu Metallurgical Facilities Engineering
# Technology Co. Ltd.," will be capitalized at about 200 million yen
# ($1.9 million), with the Japanese firms investing 50 percent and
# Baoshan 50 percent.  The rolling mill, scheduled to be completed by
# 1996, is part of Baoshan's third-phase construction.  A consortium
# of seven Japanese companies, including MHI, Mitsubishi Corp., and
# Nippon Steel, won the third-phase contract in November 1993.  MHI is
# also establishing a JV company with Sumitomo Metal Industries in
# Chongqing, Szechuan, to design an electric continuous casting steel
# mill.  (Tokyo NIKKEI SANGYO SHIMBUN 10 Feb 94 p 10)
#
#    Nippon Konpo Unyu Soko, a Japanese transportation company,
# together with the China Foreign Transport Nanjing Company, in late
# February established a JV transport company, Nanjing Nikkon Storage
# and Transport Co. Ltd.  The JV will be will be capitalized at $3
# million, with Nippon Konpo investing 51 percent and the Chinese firm
# 49 percent.  The JV agreement will be for 20 years.  Nippon Konpo
# hopes to capitalize on trade between Japan and the developing
# industrial belt along the Yangzi River.  In addition, Nippon Konpo
# plans to establish a transportation network in China by setting up
# representative offices in Shanghai, Chongqing, and Guangzhou.
# (Tokyo NIHON KEIZAI SHIMBUN 14 Feb 94 p 11)
#
#    Nippo Ltd., an Osaka-based trading company with strong ties to
# printing companies, will open a wholly owned subsidiary offset
# printing plant in Beijing.  The subsidiary, Beijing Nippo Printing
# Co. Ltd., will be capitalized at $2.3 million.  The plant, which
# will begin operations in late March, will import all materials from
# Japan and will print high-quality four-color artwork for Japanese
# companies operating in China.  (Tokyo ASAHI SHIMBUN 22 Feb 94 p 10)
#
#    Consulting Services - Cosmo Public Relation, a marketing
# consulting company, has established a JV marketing consulting
# company, Cosmo China Enterprise Ltd., to provide support to Japanese
# companies planning to enter the Hong Kong and PRC markets.  The JV
# will be capitalized at HK$200,000 ($26,000).  The Chinese partner
# will be a company owned by Yang Zhenhan, a former high-level Chinese
# Government official with experience in the machine and auto-
# manufacturing industries, and Tan Nushi, a former Shanghai official
# responsible for textiles.  The JV firm will use the "personal
# contacts" and market knowledge of Yang and Tan to provide
# introductions to government organizations and business partners, and
# to provide business-site selection and real estate contract
# mediation services.  The JV will have its head office in Hong Kong
# and a a branch office in Shanghai.  (Tokyo NIKKAN KOGYO SHIMBUN 8
# Feb 94 p 6)
#
#    Ikeda Hiroyoshi Accountants, an accounting firm, and Inform, an
# Osaka-based consulting company specializing in investment in China,
# together with the Shanghai Yangzi International Economic Cooperation
# Center, will establish a consulting company in Shanghai to target
# small Japanese companies that are interested in setting up
# operations in China.  The new company, Shanghai Foreign Business
# Commercial Research Club, will advise small companies on the legal,
# accounting, and tax systems in China and sponsor regular seminars on
# business and personnel management, taxes, and legal issues in China.
# The club will not be based on capital investment but will "operate
# cooperatively," supported entirely by membership fees of 50,000 yen
# ($476) and monthly dues of 20,000 yen ($190).  The club hopes to
# recruit 50 companies.  (Tokyo NIHON KEIZAI SHIMBUN 21 Feb 94 p 15)
# PHILIPPINES:  Shipping Firm Establishes Subsidiary in Manila --
# Keihin Co., a medium-sized warehousing and transport firm, has
# established a Philippine subsidiary, Keihin Everett Forwarding Co.,
# headquartered in Manila.  As Japanese companies have expanded
# operations in the Philippines, the need for shipping services has
# grown.  Although Keihin has been handling product distribution and
# delivery services for Japanese companies there, establishing a
# subsidiary will allow it to initiate full-scale shipping services in
# the Philippines and expand its international transportation network.
# Initial annual sales for the subsidiary are expected to be 112
# million yen ($1.06 million).  Keihin already has subsidiaries in the
# United States, Singapore, Europe, and Hong Kong and resident offices
# in Taiwan and Australia.  (Tokyo NIKKEI RYUTSU SHIMBUN 24 Feb 94 p
# 17)
#
#    THAILAND:  Canon To Expand Office Automation Equipment Production
# -- Canon Hi-Tech (Thailand) Ltd., a Canon subsidiary that produces
# office automation equipment such as copiers for the Japanese,
# European, and U.S. markets, will expand operations this year and
# increase production capacity by 30 percent.  In the past, when a new
# Canon product was manufactured in Thailand, the product was made
# entirely from parts imported from Japan.  As production increased,
# the local parts content gradually increased as well.  In the future,
# however, Canon Hi-Tech's planned expansion will permit the shift of
# parts production.  Thus, Canon Hi-Tech will be able to develop and
# produce new products from scratch, with the majority of parts
# manufactured in Thailand.  To ensure the continued high-quality of
# parts used in its products, in 1994 Canon Hi-Tech will bring in a
# technology team from Japan to handle product development.
#
#    Canon Hi-Tech was established in 1990 in Bangkok to help Canon
# offset the effects of yen appreciation.  In 1993 the company shipped
# 260,000 copiers and 430,000 printers, with sales totaling 20 billion
# yen ($190.5 million).  The expansion work will begin in March and
# should be completed by October 1994.  (Tokyo NIKKEI SANGYO SHIMBUN
# 15 Feb 94 p 13)
#
#    UNITED STATES:  Kobe Steel, TI To Market Cladding Material in
# Japan -- Kobe Steel and Texas Instruments (TI) have agreed to
# jointly market cold-rolled cladding material in Japan manufactured
# in the United States by TI.  This will be the first introduction of
# cold-rolled cladding material on the Japanese market.  TI, which
# developed its own technology to produce cold-rolled cladding
# material that is two to three times stronger than existing
# materials, decided to link up with Kobe Steel in entering the Japan
# market because Kobe has the aluminum and steel resources and also
# has "deep connections" with its consumers.  The companies have
# already decided on one use of the cladding material--to make the
# stainless aluminum composite used in the canisters of induction-
# heating (IH) thermoses and in the pots for IH rice cookers.
# Kobe Steel and TI have set a FY94 sales target of 300 tons of
# cladding material and a turnover of 500 million yen ($4.8 million).
# Matsushita Electric Industrial Co. also unofficially plans to use
# this cladding material in its new IH thermos.  (Tokyo NIKKEI SANGYO
# SHIMBUN 16 Feb 94 p 17)
#
#    Sumitomo Metal To Extend Technical Cooperation to Steel Rod Firm
# - Sumitomo Metal Industries will cooperate technically with American
# Steel and Wire (AS and W), a steel rod manufacturer based in Ohio.
# Sumitomo Metal will provide software-related support to AS and W in
# equipping its new high-grade steel bar mill, will help conduct
# various technical inspections, and also will provide operational
# support when the mill opens.  U.S. steelmakers are considering
# whether to file dumping charges against Japanese firms as a measure
# to shut out imports of high-grade steel.  AS and W decided to seek
# technical support from Sumitomo Metal, with which it has previous
# business ties in purchasing steel rods.  Sumitomo Metal, on the
# other hand, is seeking to establish a foothold in the U.S. market.
#
#    The new AS and W mill, which will cost an estimated $70 million
# and will have a production capacity of 550,000 tons annually, will
# produce high-grade steel bars 30-40 millimeters in size mainly for
# use in automobiles.  Plant construction is scheduled to begin this
# summer, with completion targeted for December 1995.  Sumitomo
# Metal's two-year cooperation agreement, which began in February
# 1994, includes a financial commitment of- 100 million yen
# ($962,000).
#
#    Sumitomo Metal may consider expanding its cooperation with AS and
# W to include technical support for remodeling AS and W's existing
# wire rod mill and building facilities to manufacture billets.  It
# will then follow up with consultations with AS and W on producing
# high-grade auto parts.  (Tokyo NIKKEI SANGYO SHIMBUN 22 Feb 94 p 15)
#
#    VIETNAM:  Japanese Firm To Assist Marine Products Processing
# Company -- Shinto Bussan, the importing subsidiary of Toyo Suisan, a
# major Japanese food products company, will expand the technical
# guidance it provides to the Vietnamese company that processes the
# marine products Shin to Bussan imports into Japan.  By raising the
# processing level of products like shrimp and squid, Shinto Bussan
# can sell them directly to Japanese sushi and specialty restaurants
# and other retailers and make far higher profits.  In this way,
# Shin to Bussan hopes to increase sales of products imported from
# Vietnam to 1.5 billion yen ($14.3 million) annually from the current
# 1 billion yen ($9.5 million) level.
#
#    Shinto Bussan will expand the technical guidance it provides to
# its production consignee, SeaProdex, a Vietnamese state-operated
# enterprise that processes more than 30 marine products for Shin to
# Bussan at eight processing plants.  Shinto Bussan's imports from
# Vietnam constitute 20 percent of the company's total sales.  (Tokyo
# NIKKEI SANGYO SHIMBUN 24 Feb 94 p 17)
#
#    Machine Tools/Robotics - MT Sales Fell 25 Percent in 1993,
# December Sales Dropped 16 Percent -- According to statistics
# compiled by the Japan Machine Tool Builders' Association, machine
# tool (MT) sales for 1993 totaled 531.783 billion yen ($5.06
# billion), down 25.1 percent compared to 1992.  Sales of lathes and
# machining centers dropped by 45 percent.  Total domestic sales for
# the year came to 322.57 billion yen ($3.07 billion), down 32.0
# percent, while exports totaled 209.213 billion yen ($1.99 billion),
# down 11.2 percent.  The large decline in domestic sales raised the
# ratio of exports to total sales to 39.3 percent, topping the
# previous high of 36 percent recorded in 1986.  Outstanding orders
# fell to 267 billion yen ($2.54 billion) at the end of 1993 compared
# to 354.9 billion yen ($3.38 billion) in 1992.
#
#    For December, MT sales totaled 40.054 billion yen ($381.467
# million), down 16.7 percent compared to December 1992.  However,
# this is the first time in three months that monthly sales have risen
# above the 40 billion yen ($381 million) level.  December domestic
# sales came to 23.068 billion yen ($220 million), down 24.0 percent
# year-on-year but up 10.3 percent from November.  December exports
# were 16.986 billion yen ($161.8 million), down 4.3 percent from
# December 1992.  However, exports to the United States increased.
# (Tokyo NIHON KEIZAI SHIMBUN 10 Feb 94 p 11)
#
#    Semiconductors/Computers/Electronics - NEC Wins Supercomputer
# Order From Private University -- NEC Corp. has won an contract from
# Fukuoka University, a private institution in Fukuoka City, to build
# a  research and education system" that includes a supercomputer at a
# total cost of just over 1 billion yen ($9.3 million).  The company
# will provide its "SX-3/IIR" vector supercomputer.  Further, NEC will
# construct a local-area network (LAN) that will combine image
# processing workstations, education-use personal computers, and a
# library information system.  One "special feature" of the system is
# that the supercomputer and workstations will use UNIX operating
# software.  The system will be delivered in August and is expected to
# be in operation by October.
#
#    This is NEC's first supercomputer order in the Kyushu region.
# Also, NEC's supercomputer will replace a Fujitsu-made "VP2100/10"
# the university has been using.
#
#    NEC has not won any of the bids for ten of the eleven
# supercomputers funded under the the government's first FY93
# supplemental budget, while Fujitsu has won four.  In several of the
# bids, including those sponsored by the Communications Research
# Laboratory and Tsukuba University, the two firms competed head on,
# but Fujitsu won out over NEC and the other bidders with lower prices
# and higher technical evaluations "beyond the scope of expectations."
# With the Fukuoka University contract, however, NEC "has had its
# revenge."  (Tokyo NIHON KEIZAI SHIMBUN 4 Feb 94 p 7)
#
#    Seiko Epson To Build IC Design-In Center in China - Seiko Epson
# Corp. will establish an integrated circuit (IC) design-in center in
# Shenzhen, China in the spring of 1995.  The center's goal will be to
# strengthen local customer support for Seiko Epson's IC design-in
# operations in China, which were developed through Hong Kong.
# Currently most of Seiko Epson's design-in customers are in Japan,
# but the company has decided "it is essential to increase foreign
# sales."  Therefore it is expanding directly into China, where the
# company anticipates a huge demand in the future for design-in ICs.
# Seiko Epson first will focus on developing a market in southern
# China for semiconductors designed for use in light industry, such as
# electronic notebooks and game machines.
#
#    Seiko Epson derives about 50 percent of its sales from customized
# and semi-customized ICs.  In this field the ability to develop
# products which are specialized to a user's needs is the deciding
# factor in a company's success.  For this reason, after starting its
# semiconductor operations in 1980, Seiko Epson moved to aggressively
# strengthen its design-in system.
#
#    Domestically, Seiko Epson has semiconductor design-in centers in
# Tokyo, Osaka, Nagoya, Fujimi, and Sapporo.  The Shenzhen center will
# be Seiko Epson's fourth overseas design-in center; the other three
# are in Canada, California, and Taiwan.  (Tokyo NIKKAN KOGYO SHIMBUN
# 10 Feb 94 p 7)
#
#    Telecommunications/Satellites - NEC, Mitsui To Build Ground
# Station For Sri Lanka Telecom -- NEC and Mitsui and Co. have won a
# contract worth 1.5 billion yen ($14.4 million) from Sri Lanka
# Telecom, the country's state-run telecommunications enterprise, to
# build an INTELSAT (International Telecommunication Satellite
# Organization) Standard-A ground station and supply NEAX61 switching
# equipment.  The ground station, the second in Sri Lanka, will be
# built in the eastern outskirts of Colombo, Sri Lanka's capital, by
# early 1995.  It will increase the country's international
# communications capacity from the existing 500 lines to 2,500.
# Sri Lanka Telecom will set up support facilities in the Padukka
# region, east of Bombay, India, and plans to begin operations at the
# ground station in early 1995.  All financing for the project will be
# handled through the Asia Development Bank.  AT and T and Sweden's
# Ericsson also bid for the project, but Sri Lanka Telecom selected
# NEC and Mitsui based on its "high appraisal" of the first ground
# station the two companies built in 1975.
#
#    Demand for international communications in Sri Lanka is growing
# not only because the country is a popular tourist spot, but more
# importantly because several Asian countries, especially South Korea,
# have begun textile production operations there.  NEC is seeking to
# sell its equipment for both international and domestic
# communications in conjunction with Sri Lanka's active program to
# upgrade its communications infrastructure.  (Tokyo NIKKEI SANGYO
# SHIMBUN 22 Feb 94 p 7)
#
#    NHK Will Lease Circuit on Panamsat Satellite - The Japan
# Broadcasting Corp. (NHK) has confirmed that it will lease a circuit
# on the Panamsat (Pan American) satellite, scheduled to be placed in
# orbit this May, for video transmission of its newscasts between
# Japan and the United States.  NHK, which currently leases two
# circuits from INTELSAT (International Telecommunications Satellite
# Organization), reached its decision after "a comprehensive review of
# factors."  Reportedly the deciding factor was Panamsat's low costs,
# although NHK has not made a "definite statement" regarding this
# matter.  NKH and Panamsat are currently working out final details of
# the contract through Kokusai Denshin Denwa (KDD), which is acting as
# the negotiating agent between the two firms because Panamsat does
# not have an office in Japan--a requirement for foreign enterprises
# seeking satellite communications business activities with Japan, as
# stipulated in the Japanese Government's deregulation measures for
# this sector of the communications industry.
#
#    NHK's decision to contract with Panamsat will likely encourage
# other Japanese customers to follow.  This trend will affect
# INTELSAT, which currently dominates the Japan-U.S. video
# transmission market, but will also affect Japanese companies like
# Japan Satellite Systems, which is seeking to establish a presence in
# the international satellite communications market.  (Tokyo NIKKEI
# SANGYO SHIMBUN 18 Feb 94 p 6)
#
#    Tokyo Experimental CATV Project To Be Operational by 1996 - The
# Tokyo Metropolitan Government soon will begin planning for a large
# experimental digital-based cable television (CATV) project in the
# new city center currently under development in the Tokyo Bay area.
# The CATV project is slated to be operational in 1996.  This May the
# metropolitan government will call on representatives from the public
# and private sector, including the Ministry of Posts and
# Telecommunications, the Japan Broadcasting Corp. (NHK), Nippon
# Telegraph and Telephone (NTT), NEC, Hitachi, Matsushita Electric
# Industrial Co., and communications software companies to form a
# committee and define a project plan.  The government estimates it
# will cost about 3 billion yen ($28.8 million) to build the CATV
# project center and to develop the necessary software.
#
#    Once the committee defines an overall plan, the metropolitan
# government will proceed with building the project center and
# establishing a 100-channel CATV network for offices and residences
# in the city center area that also will provide services such as
# video-on-demand, home television shopping, interactive health and
# medical consulting, and business communications services.  The
# metropolitan government plans to officially inaugurate the CATV
# project in March 1996 during the "Tokyo Frontier" world trade fair.
# (Tokyo NIHON KEIZAI SHIMBUN 26 Feb 94 p 1)
#
#    Matsushita Electric Industrial Co., EO Revamp Production
# Agreement - Matsushita Electric Industrial Co. has concluded an OEM
# (original equipment manufacturer) agreement with EO, a California-
# based company which develops portable communications terminal units.
# The move follows a request by EO to discontinue its existing
# consignment production relationship with Matsushita because the
# number of units currently produced is considerably lower than
# originally forecast due to a decline in demand in the U.S. market.
#
#    America Matsushita Computer, based in Illinois, has been
# producing EO terminal units on consignment since 1992, when EO was
# established with investment from Matsushita Electric Industrial, AT
# and T, and Olivetti.  Initially, the two companies set production
# targets of 5,000 units per month, but because of the decline in U.S.
# market demand, they realized only half the target figure.
# Matsushita states "it is not thinking about reexamining the other
# aspects of its EO relationship, such as withdrawing its investment
# from the company."  (Tokyo NIHON KEIZAI SHIMBUN 15 Feb 94 p 12)
#
#    CHINA:  Domestic Developments - Shanghai Enterprise Ownership
# Composition Changes Through Reform -- Economic reform has had a
# tremendous impact on enterprise ownership composition in Shanghai,
# with the number of joint ventures, private enterprises, and other
# types of ownerships growing yearly.  According to the latest
# statistics, from 1980 to early 1993, state-owned enterprises
# declined from 85.9 percent to 62.2 percent of Shanghai's gross
# domestic product while collectives, private, and joint venture
# enterprises grew from 12.4 percent, 0.3 percent, and 1.7 percent to
# 19.2 percent, 2 percent, and 18.2 percent of the gross domestic
# product respectively.
#
#    Shanghai has vigorously encouraged the development of collective
# enterprises in townships since 1985.  The ensuing policy of opening
# up has also helped to attract a lot of foreign investment.  With the
# liberalization of enterprise ownership, Shanghai's private
# enterprises have grown to over 5,000 at present.  After the
# socialist market economy was instituted in 1992, the shareholding
# system proliferated.  There are now over 90 Shanghai enterprises
# selling shares to the public, with capital exceeding 23 billion
# yuan.  The growing economic prosperity during the past 15 years
# proves that ownership reform is suited to China's general economic
# development.  This reform is not only beneficial to raising people's
# living standard, increasing state revenue, and maintaining social
# stability, it is also beneficial to establishing a socialist market
# economy.  (Shanghai WEN HUI BAO 8 Jan 94 p 1)
#
#    Textile Shortages, Price Increases Forecast in 1994 - According
# to estimates of the State Administration of Commodity Prices, this
# year textile supplies will not meet demand and prices will rise.
# Based on an annual output of 1,150,000 tons of cotton yarn, the
# textile industry needs 3.5 million tons of cotton, but cotton
# shortages will reach 1 million tons.  Because cotton prices have
# increased, the price of cotton yarn has also increased.  In
# December, 21-count yarn was 14,000 yuan per ton, and 32-count yarn
# was 15,000 yuan per ton, increases of 28 percent and 17 percent
# respectively over the first quarter of 1993.  This year the price of
# cotton yarn will continue to rise.
#
#    China produces about 2 million tons of chemical fiber annually,
# and imports 650,000 tons.  In 1994, the price of chemical fiber will
# increase.  Annual domestic output of polyester is 1.1 million tons
# while the processing industry needs 1.3 million tons.  Annual
# imports are 200,000 tons.  In December, the price was 10,3000 yuan
# per ton and in 1994 the price will remain at the current level.
# Annual output of dacron is 700,000 tons, and the processing industry
# needs 800,000 tons.  Annual imports are 150,000 tons.  However, in
# 1993 the international market price increased and imports decreased.
# In December, the price was 12,5000 yuan per ton.  Production
# enterprises that use this material changed or stopped production.
# In 1994 dacron prices will rise.  Meanwhile, annual domestic output
# of acrylic fibers is 150,000 to 200,000 tons and the processing
# industry needs 400,000 tons.  Thus, imports supply over SO percent.
# In 1994 the price will follow the international market.  (Shanghai
# SHANGHAI JINGJI BAO 28 Jan 94 p 3)
#
#    Bank of China To Introduce Computerized Service Network - By
# January this year, renminbi deposits in the Bank of China had
# increased by almost 4 billion yuan over the end of last year, to
# stand at 112 billion yuan.  By the end of last year, foreign
# currency deposits in the bank amounted to $9.19 billion, an increase
# of more than 50 percent over the end of the previous year.  In this
# year's work, the bank will focus on improving efficiency, providing
# better service, increasing flexibility, strengthening the formation
# of the deposit network, perfecting the disposition of the network,
# improving the service functions of big cities' deposit networks, and
# expediting the automation of deposit service, the aim being to
# "invigorate itself by means of science and technology."  This year
# it has planned to equip a large number of service networks in all
# branches with computers.  It will try to greatly increase the
# popularity and use rate of its computerized network in the shortest
# possible time.  It will actively and appropriately introduce a
# single-person receipt and payment operational method to its deposit
# service.  This method will be introduced by trial throughout the
# country and popularized in coastal areas.  (Beijing ZHONGGUO XINWEN
# SHE 1318 GMT 16 Feb 94) Hong Kong Bureau
#
#    Shenzhen Calls Halt to Listing of New 'A' Share Issues - The
# Shenzhen stock exchange has imposed a complete halt on new listings
# of "A" shares, issued to locals, in an apparent attempt to ease
# strains put on the system by the rush of companies coming to the
# market.  Although the 22 February official statement said the ban
# applied to all issues, it is unlikely that "B" shares, which are
# traded by foreign investors, will be affected.  Saying that
# investors were unhappy with the flood of new shares being listed,
# the exchange indicated that listings would resume depending on
# market conditions.
#
#    Analysts said the problem lay with the government's overly
# ambitious plan to enlarge stock markets, while ignoring the markets'
# capacity to absorb new shares.  Of the 5 billion shares approved for
# listing in 1993, only about 2.6 billion had been listed by the end
# of the year, leaving 2.4 billion to be listed in 1994, thereby
# straining the listing schedule.  (Hong Kong SOUTH CHINA MOENING POST
# (BUSINESS POST) 23 Feb 94 p 1) Hong Kong Bureau
#
#    Shandong Remains Country's Leading Gold Producer - Shandong
# Province overfulfilled its annual gold production target last year,
# thereby retaining its 18-year lock on the position of China's
# leading gold producer.  Shandong's gold reserves amount to half the
# PRC's total, with annual production accounting for one-third of
# national output.  With the deepening of reform and the strengthening
# of administration over the industry, as well as enterprises'
# implementation of 14 self-decision-making powers, 1993 profits in
# the industry rose by 30 percent over the previous year.  Since last
# year, the gold industry has adjusted its development strategy by
# investing in other industries.  By the end of 1993, RMB2OO million
# had been invested in such industries as construction materials,
# electronics, and metallurgy, with profits tax earned in these
# industries alone amounting to 40 million yuan.  (Beijing ZHONGGUO
# XINWEN SHE 1356 GMT 16 Feb 94) Hong Kong Bureau
#
#    Xiamen To Invest in Transport Facilities - Pan Shijian, general
# manager of the Xiamen Municipal Roads and Bridges Construction
# Investment Corporation, said that 1994 would see the largest amount
# of investment and the greatest number of projects to construct
# transport facilities in the special economic zone.  Pan said Xiamen
# would adopt various measures to raise capital by guaranteeing the
# commencement of all key items.  Construction began last year on the
# Shigushan overpass, at a total cost of 90 million yuan.  The project
# is scheduled for completion by September 1994.  Work has begun on
# reconstruction of the Jimei-Guankou road, also slated for completion
# by September, while the 19-km Jimei-Tongan road will be upgraded at
# a total cost of 400 million yuan.  The work will be completed in
# 1995.  In March, construction will begin on the Xiaoyingling section
# of the Fuzhou-Xiamen expressway.  It should be completed within four
# years.  Construction of the Haicang bridge will start by the end of
# 1994, with planned investment of RMB2 billion, to be raised in
# several ways, including government allocation and the issue of
# stocks both at home and abroad.  (Beijing ZHONGGUO XINWEN SHE 0815
# GMT 25 Feb 94) Hong Kong Bureau)
#
#    Jialing To List Subsidiaries in Hong Kong - Jialing, a Hong Kong-
# based company controlled by Sichuan Province, is restructuring its
# subsidiaries in an effort to list them on the Hong Kong Stock
# Exchange.  Recently, Jialing has operated as a holding company and
# has filed an application with the mainland authorities to gain
# commensurate status there.  Jialing's businesses cover import-
# export, equity investments in industrial and commercial enterprises,
# real estate investments, information services, securities,
# transportation, hotels, and the importation of capital and
# technology.  Last year, 70 percent of its income came from real
# estate investments, mostly in Hong Kong.  According to Jialing's
# chairman, Liu Guangbing, the company will increase investment in the
# mainland this year.  (Hong Kong WEN WEI PO 23 Feb 94 p C3) Hong Kong
# Bureau
#
#    Foreign Trade and Investment - Fujian Sets Up Intellectual
# Property Rights Court -- Fujian provincial's procuratorial court has
# set up an intellectual property rights (IPR) judicial court recently
# and the City of Xiamen's Intermediate People's Court has also
# officially set up an IPR protection court.  The move is to
# demonstrate that the province will fully exercise its judicial
# authority in IPR cases and is determined to punish the infringement
# and violation of IPR.  According to an estimate, the various levels
# of the people's court in Fujian has in recent years handled 47 cases
# and tried 35 involving IPR.  These cases include disputes about
# authorship (copyright) rights, patent rights, and trademark rights.
# Some cases involve foreign enterprise contract disputes.  For
# example, one such case was between a certain company in Hong Kong
# and a certain unit in Fujian in dispute involving non-patent
# technology transfer and in patent application permits.
#
#    The cases being tried in the provincial procuratorial court cover
# seven categories of disputes:  patent disputes; trademark disputes;
# copyright disputes; disputes involving invention infringement,
# exclusive rights to technology and other scientific and
# technological achievements; technology contractual disputes;
# disputes involving illegal competition; and any other disputes
# belonging to the scope of intellectual property protection rights.
# All categories apply to sino-foreign, Hong Kong, Macao, and Taiwan
# cases.  (Beijing GUOJI SHANGBAO 2 Feb 94 p 1)
#
#    Shanghai Exports Exceed Target in 1993 - Shanghai's exports
# exceeded $7.38 billion in 1993 and the export growth rate was higher
# than the national average.  In early 1993, the Shanghai municipal
# government set its export target at $7.34 billion, but by mid-year
# only 45 percent of the target had been fulfilled.  In June, a
# municipal economic and trade conference was held to further reform
# and to create an environment more compatible with a socialist market
# economy.  After administrative protection and preferential policies
# were abolished, foreign trade enterprises were forced into market
# competition.  Last year, foreign trade privileges were also granted
# to an additional 4,000 or so industrial units, research institutes,
# enterprises, and joint venture firms, bringing Shanghai's trading
# entities to approximately 7,000.  Meanwhile, all relevant government
# work units were instructed to support exports and to launch
# coordinated measures.  After concerted efforts, exports began to
# increase and eventually exceeded the 1993 target.
#
#    Future export growth is targeted at 15.4 percent annually.  Since
# the state abandoned the mandatory export plan and foreign exchange
# submitting quota, relevant export promoting measures, including
# transforming the operational mechanism of trade offices, providing
# incentives, and adjusting industrial production, should be
# instituted as soon as possible.  (Shanghai WEN HUI BAO 6 Jan 94 p 1)
#
#    Guangzhou To Set Up Individual Foreign Exchange Markets - Plans
# are in the making for Guangdong's capital city to set up individual
# swap centers to handle foreign exchange transactions. These
# individual centers will then link up with the nationally established
# foreign exchange centers.
#
#    Presently, Guangzhou's foreign exchange regulating markets have
# two kinds of operations.  One involves a specified volume and the
# other a spot exchange.  Having planned to expedite a nationwide
# foreign exchange market network, the Bank of China and the State
# Administration of Exchange Control are setting up the corresponding
# financial organs at the provincial and city levels.  Under the plan,
# the Guangzhou area is the first to form public swap centers, then
# set up a province wide network, and lastly, to link up with the
# national foreign exchange market network.  Additionally, Guangzhou
# will set up the Guangzhou financial center and a city shareholding
# cooperative bank to handle the Renminbi operations involving
# promissary notes and financial capital.  (Beijing ZHONGHUA DISAN
# CHANYE BAO 6 Jan 94 p 3)
#
#    Foreign Investment Estimated at $30 Billion for 1993 - China
# became the world's biggest foreign investment recipient country in
# 1993.  Actual foreign investment introduced for the whole year
# exceeded $30 billion, of which Guangdong Province accounted for one-
# quarter, ranking first among China's provinces and municipalities.
# According to statistics, foreign businessmen invested in nearly
# 100,000 projects in mainland China in 1993.  Agreements signed
# involved $110 billion, of which direct investment exceeded $20
# billion.
#
#    Guangdong Province attracted more foreign investment than any
# other province.  Last year, $8.5 billion was actually received,
# accounting for one-quarter of total foreign investment in the
# mainland.  Shanghai ranked second in 1993 with $7.016 billion.
# Beijing ranked third, attracting $6.28 billion.  These were followed
# by Shenzhen, which attracted more than $5 billion; Fujian, $2.8
# billion; Jiangsu, $2.1 billion; Shandong, $1.6 billion; Guangxi,
# $1.06 billion, and Hainan, $730 million.  The overall amount of
# foreign investment in China increased by a wide margin over the
# previous year.
#
#    Hong Kong businessmen ranked first in investing on the mainland
# last year, with investments exceeding about $13 billion.  Taiwan
# businessmen ranked second, with investments amounting to more than
# $6 billion, exceeding the total of many previous years.  U.S.,
# Japanese, and German businessmen also made enormous amounts of
# investment in the mainland last year.  (Hong Kong ZHONGGUO TONGXUN
# SHE 0928 GMT 18 Feb 94) Hong Kong Bureau
#
#    Guangdong Foreign-Funded Enterprises Expand Export Share -
# According to an office of the Guangdong Provincial Government, by
# late 1993, foreign-funded enterprises in Guangdong and local state-
# owned foreign trade, industrial, and commercial enterprises had
# almost equal shares of the export business for the first time.
# Guangdong's 1993 export volume hit $26.33 billion, of which $10
# billion was contributed by foreign-funded enterprises.  In 1993, the
# average export growth rate throughout the province was 8.6 percent,
# while the corresponding growth rate of foreign-funded enterprises
# was as high as 23.2 percent.  (Hong Kong ZHONGGUO TONGXUN SHE 0947
# GMT 17 Feb 94) Hong Kong Bureau
#
#    Beijing Views Use of Foreign Loans, Donations - Since 1979,
# Beijing has applied multilateral aid totaling $29.903 million from
# the UN Planning Program for carrying out 33 projects; and aid
# totalling $86.63 million yuan from Japan, Australia, Canada,
# Germany, and other countries for carrying out 15 projects.  Nineteen
# aid projects, involving $62 million, were being carried out in 1993.
# As of the end of 1993, Beijing had used government loans and
# donations from 14 countries for carrying out 85 projects, involving
# $820 million.  With these loans, Beijing has completed 54 projects
# involving $137.52 million and carried out 19 projects involving
# $611.38 million.  Agreements were also reached on the use of loans
# for building six projects, involving $28.72 million.  Beijing has
# also used foreign donations to complete four projects, involving
# $11.75 million.  These foreign loans and donations were mainly used
# for building infrastructure and industries related to the people's
# lives in the capital, covering industry, agriculture, foodstuffs,
# aquaculture, environmental protection, education, scientific
# research, fire prevention, and communications management.  For
# example, Japan has provided 2.7 billion yen of free aid for building
# the China meat products research center to take charge of Beijing's
# meat quality inspection, and the Japanese Government has provided
# aid of 3 billion yen for China to build Beijing Television Station
# and granted 19.2 billion yen in loans to help Beijing build a
# subway.  (Beijing BEIJING RIBAO 13 Feb 94 p 1) Hong Kong Bureau
#
#    Hebei Use of 1993 Foreign Loans - Hebei Province has achieved a
# breakthrough in the use of foreign loans.   As of the end of 1993,
# the Hebei Province had carried out 161 projects with foreign loans,
# involving foreign capital of $670 million, and with $580 million of
# funds actually utilized.  These loans were mainly used for improving
# saline-alkaline farmlands, developing farming on Huang-Huai-Hai
# Plain, and building fast-growing forestry; improving teaching
# conditions, training teachers and developing adult education;
# preventing and curing tuberculosis; building the Hebei section of
# Beijing-Tianjin-Tanggu expressway, the No.7 and No.8 berths of
# Tangshan Port, Shijiazhuang-Tangshan microwave telecommunications
# line, and 240,000 program-controlled telephone lines in seven
# central cities and 22 counties and cities; carrying out polluted
# water disposal and gas supply projects in Handan, Shijiazhuang, and
# Baoding cities; and building a cement kiln with a daily production
# capacity of 2,000 tons at the Tangshan Qixin Cement Plant.
# (Shijiazhuang HEBEI RIBAO 8 Feb 94 p 1) Hong Kong Bureau
#
#    Airbus Signs Spare Parts Production Deal - On 1 March, Airbus
# Industrie announced that it had signed a major cooperation agreement
# in Beijing last month with the China Aviation Supplies Corporation
# which will allow Chinese manufacturers to become further involved in
# the production of the company's spare parts.  The deal is valued in
# the hundreds of millions of dollars.  Airbus will deliver nine
# aircraft to Chinese companies this year and has announced plans to
# set up a training center and a service support center in Beijing.
# About 40 percent of pilots and other workers who receive training at
# the Airbus headquarters in France are expected to come from China.
# Airbus also has set up Airbus Industrie China, which handles
# commercial, industrial, and product support activity in the PRC.
# (Beijing CHINA DAILY 2 Mar 94 p 2) Hong Kong Bureau
#
#    Aerospace Industry Corporation Seeks International Cooperation -
# An official from the China Aerospace Industry Corporation has said
# that the corporation seeks more extensive international cooperation
# in the areas of satellite information systems, mobile communication
# devices, global television relay systems, and satellite data
# communication VSAT stations.  He also said that the corporation
# plans to expand the scale of cooperation in other areas, such as the
# manufacture of communications, resource-survey, meteorological, and
# navigational satellites, as well as various kinds of satellites for
# scientific experiments, and that satellite launching services also
# will be provided.  At a news conference last June, the corporation
# announced 93 cooperation projects involving $1.28 billion.  A
# majority of the state laboratories and applied technology research
# centers under the corporation have been opened up to the outside
# world.  (Hong Kong CHING CHI TAO PAO, No 8, 28 Feb 94) Hong Kong
# Bureau
#
#    Stanley Ho Threatens To Halt Mainland Investments - Property
# developer and Macao casino operator Stanley Ho has threatened to
# stop investing in the Chinese real estate market if the capital
# gains tax on property is implemented.  Ho issued the warning at a
# foundation-laying ceremony in Shanghai on 26 February for his
# Shanghai Plaza development, an office, residential, and hotel
# complex.  Shun Tak Holdings, which is controlled by Ho, has a 15-
# percent stake, and one of his private companies has 20 percent of
# the 8-billion-yuan project.  "If the tax is implemented, I will not
# be interested in further investment," Ho said, referring to
# Beijing's new value-added land tax, but he added that his existing
# projects on the mainland would proceed as scheduled.  (Hong Kong
# EASTERN EXPRESS 28 Feb 94 p 31) Hong Kong Bureau
#
#    China Overseas To Invest in Guangdong Power Plant - The Hong
# Kong-listed China Overseas Development Company Limited, a wholly
# owned subsidiary of China State Construction Engineering
# Corporation, is planning to invest $117 million in a thermal power
# plant project in Shaoguan City, Guangdong Province.  The plant,
# Shaoguan City Pingshi Power Plant (B Factory), is a joint venture
# with the Shaoguan City government and the Shui Heng Development
# Company Limited, who hold 25 percent and 22.5 percent respectively.
# The joint venture has a 20-year operating franchise for the plant.
# (Hong Kong HSIN PAO 1 Mar 94 p 5) Hong Kong Bureau
#
#    Hong Kong Firm Holds Two Thirds Shares of Guangdong Power Plant -
# Hong Kong-based Chia Ho Ltd. has invested in a power plant in
# Guangdong under Maoming City's Electric Development Corporation and
# now holds two thirds of the shares at a cost of HK$23 million.  The
# term of the partnership is 35 years.  This four-year-old power plant
# has eight generating units imported from Germany, with an installed
# capacity of over 50,000 kw.  (Hong Kong TA KUNG PAO 24 Feb 94 p 5)
# Hong Kong Bureau
#
#    Xiamen People's Income, Foreign Capital Increase - Last year,
# Xiamen's per-capita gross domestic product amounted to 9,288 yuan,
# about 10 times the amount before the establishment of the Xiamen
# special economic zone.  Citizens' per-capita annual income was 2,034
# yuan, an increase of 24.8 percent over the previous year, while
# peasants' per-capita annual net income was 1,690 yuan, an increase
# of 20.2 percent over the previous year.  Meanwhile, Xiamen has
# improved its approval procedures and management in introducing
# foreign capital.  The city approved 655 foreign-invested projects
# last year.  Contracted foreign capital was $2.404 billion, while
# foreign capital that actually arrived in Xiamen amounted to $1.034
# billion, an increase of 84.8 percent over the previous year.  There
# were 391 newly started foreign-invested enterprises last year, an
# increase of 167.81 percent over the previous year.  (Fuzhou Fujian
# People's Radio Network 2300 GMT 16, 17 Feb 94) Hong Kong Bureau)
#
#    Zhuhai, Singapore Company Sign Shipyard Construction Pact -
# Zhuhai Port Investment, a subsidiary of the Port Authority of
# Zhuhai, signed a joint-venture contract on 1 March with Singapore's
# Marinteknik company to build a 5-hectare shipyard for the production
# and maintenance of catamarans and monohull ferries, China's first
# such shipyard.  Marinteknik's investment will amount to $12 million.
# The two partners have a long history of cooperation, having linked
# up in 1982 to provide the first passenger ferry service between Hong
# Kong and Zhuhai.  Phase one of the shipyard will be completed in
# mid-1995, enabling the yard to produce 12-16 high-speed ferries per
# year, which will generate revenues of some $50 million.  In
# addition, the yard will provide ferry maintenance services, which
# initially should earn around $5 million.  Phase two is slated for
# completion in early 1997.  Marinteknik will hold a 60-percent stake
# in the 50-year joint venture, which initially will be aimed at the
# export market, though the longer-term outlook envisions selling up
# to 50 percent of output in China.  (Hong Kong EASTERN EXPRESS 2 Mar
# 94 p 23) Hong Kong Bureau
#
#    Sino-Thai Project To Produce Suzuki Motorbikes in Nanning - The
# Nanning machinery factory and the Thailand S.P. International
# Company have pooled funds to establish the Nanning Yibin Motorcycle
# Company Limited, which will produce "Suzuki King" motorcycles in
# Nanning.  The new company has an investment of $29.55 million, of
# which the Chinese side contributed 40 percent.  A contract has been
# signed with Japan's Suzuki Company to import advanced technology,
# facilities, and management methods to produce Suzuki GS125ESK
# motorcycles and other new models.  By 1996, the company will have an
# annual output of 400,000 motorcycles.  (Beijing ZHONGGUO XINWEN SHE
# 26 Feb 94) Hong Kong Bureau
#
#    Wuhan Iron and Steel Imports Spanish Machinery - On 1 March,
# China's fourth largest steel producer, the Wuhan Iron and Steel
# Corporation (WISC), signed a contract with two Spanish companies-
# -Tecnicas Reunidas Internacional SA and Eurocontrol SA--to import an
# $82.1 million continuous casting machine intended for the second
# stage of WISC's No. 3 steel smelting plant.  The two Spanish
# companies earlier had supplied equipment worth $320 million for the
# plant's first stage.  WISC used both Spanish Government and
# commercial loans to seal the deals.  The No. 3 plant, with an annual
# steel production capacity of 2.5 million tons, will go into
# operation in 26 months, laying the foundation for WISC to increase
# its annual steel output to 10 million tons by the end of the
# century.  In 1993, WISC produced 5.06 million tons of steel and 5.44
# million tons of iron, increases of 6.12 and 6.69 percent,
# respectively, over the previous year.  Sales revenues for 1993
# amounted to 11.37 billion yuan ($1.3 billion), up 26 percent; taxes
# and profits hit 3.1 billion yuan ($356 million), up 38 percent;
# while exports hit $110 million, up 25 percent.  (Beijing CHINA DAILY
# 2 Mar 94 p 2) Hong Kong Bureau
#
#    Tianjin Establishes Joint-Venture Building Materials Institute -
# The Tianjin building materials supply general company and the
# Australian CSR company will jointly build a precast concrete
# project, and the Tianjin Municipal Building Materials Research
# Institute will cooperate with the Housing Construction Research
# Center of an Australian university to establish the Tianjin-
# Australian building materials research institute--the first of its
# kind in China.  The agreement signing ceremony was held at the
# conference room of the Tianjin Municipal government on 19 February.
# The investment of the concrete company totals $30 million and the
# designed annual production capacity is 1 million cubic meters of
# concrete.  Four production lines and 90 sets of concrete equipment
# will be set up in Dongli, Nankai, Hexi, and Hongqiao building
# materials supply companies under the Tianjin building materials
# supply general company.  This project is expected to be completed
# within this year.  Based on the agreement, the Tianjin Commission of
# Science and Technology will cooperate with a university in Australia
# in research, exchange of scholars, training of personnel, and
# exchange of academic data, and the Tianjin-Australia building
# research institute will serve as their cooperation demonstration
# unit in research regarding new building materials, quality control,
# and construction cost.  (Tianjin TIANJIN RIBAO 19 Feb 94 p 1) Hong
# Kong Bureau
#
#    Taiwan:  Additional Incentives To Promote Southern Policy -- On
# 14 February Minister of Economic Affairs Chiang Ping-kun said the
# ministry will offer additional incentives for Taiwanese businessmen
# to invest in Southeast Asia.  Chiang Ping-kun said such incentives
# would include extending workers' training period, urging banks to
# increase loans for companies which invest in Southeast Asia, and
# signing agreements with Southeast Asian countries to avoid double-
# taxation.  The ministry will also help secure loans to businessmen
# who are interested in establishing industrial development zones in
# the region.  (Taipei CHING-CHI JIH-PAO 16 Feb 94 p 2) Okinawa Bureau
#
#    Draft Trade Regulations on Hong Kong, Macao - The Executive
# Yuan's Mainland Affairs Council has drafted regulations concerning
# Taiwan-Hong Kong-Macao relations in investment, technological
# cooperation, shipping, finance, and insurance after Hong Kong and
# Macao are returned to the Chinese Communists in 1997 and 1999
# respectively.  The first internal examination of the 54-article
# draft regulations will be held on 24 February.  Parts of the draft
# regulations that concern the economy and trade include: Taiwanese
# businessmen must report their investment or technological
# cooperation in Hong Kong and Macao to the ministry; financial and
# insurance institutions must obtain prior approval before
# establishing branches in Hong Kong and Macao; the Ministry of
# Economic Affairs shall draw up procedures to regulate Hong Kong and
# Macao investments in Taiwan; and the Ministry of Transportation and
# Communications shall draw up procedures governing air and shipping
# services with Hong Kong and Macao.  (Taipei CHING-CHI JIH-PAO 16 Feb
# 94 p 3) Okinawa Bureau
#
#    Textile Companies To Invest or Expand in Vietnam - After the
# United States lifted its trade embargo against Vietnam, several
# Taiwanese textile companies decided to invest or expand their
# investments in Vietnam.  The Far East Textile Company plans to
# establish garment and dyeing mills in Vietnam soon.  At the end of
# 1993, the Hualon Group applied to the Vietnamese Government to
# establish a comprehensive textile mill involving investment funds of
# $240 million.  The Huang Ti Lung Textile Company has decided to
# invest more than $20 million to establish knitting and spinning
# mills in Vietnam.  The Chung Hsing Textile Company, which has long
# been established in Vietnam, decided to invest another $50 million
# to expand its knitting and spinning production facilities in
# Vietnam.  (Taipei CHING-CHI JIH-PAO 17 Feb 94 p 10) Okinawa Bureau
#
#    Government To Hold Current Tariffs on Automobiles, Parts for Now
# - In view of the fact that automobiles and the relevant industries
# account for 8.5 percent of Taiwan's total industrial output value,
# Vice Economic Minister Yang Shih-chien said on 17 February:  "The
# government will take this into account, and at this moment will not
# consider lowering tariffs on imported automobiles and parts and
# accessories before the issues of Taiwanese restrictions on car-
# exporting regions and of local car-parts content rates are settled
# during negotiations for GATT membership."  Although the United
# States calls for Taiwan to lower its auto tariff from 30 percent to
# 15 percent, the government will still uphold the principle of
# lowering it slightly, with 25 percent as the bottom line.  (Taipei
# CHING-CHI JIH-PAO 18 Feb 94 p 2) Okinawa Bureau
#
#    Imposition of Anti-Dumping Tax on Japanese, Korean Polypropylene
# - The Ministry of Finance has ruled that Japan and South Korea are
# dumping polypropylene (PP) in Taiwan, and decided to impose a 6.57-
# 110.68 percent temporary anti-dumping tax on 18 South Korean and
# Japanese petroleum-chemical factories.  According to customs
# statistics, Taiwan imported 178,000 tonnes of PP in the first 11
# months of 1993, and nearly 60 percent of that was exported by Japan
# and South Korea.  (Taipei CHING-CHI JIH-PAO 19 Feb 94 p 13) Okinawa
# Bureau
#
#    MOEA Assesses Impact on Manufacturers of Joining GATT - According
# to an assessment by the Ministry of Economic Affairs, after Taiwan
# joins GATT and lowers tariffs, the automobile and motorcycle,
# textile, and machine tool industries will experience the greatest
# impact.  It is estimated that the output value of the auto industry
# will drop by 60 percent, auto and motorcycle parts by 50 percent,
# and machine tools by 12.4 percent.  However, Taiwan's net exports
# and imports of manufactured goods may increase by $1.8 billion and
# $546 million respectively. The net output value of the manufacturing
# industry is likely to increase by $1.3 billion.  In addition to a
# decline in the output values of the aforementioned industries,
# thousands of workers in the auto and machinery industries may also
# lose their jobs after Taiwan joins GATT.  (Taipei CHING-CHI JIH-PAO
# 21 Feb 94 p 2) Okinawa Bureau
#
#    Statistics on Exports to PRC May Be Underestimated - According to
# an official of the Board of Foreign Trade, Taiwan's real export
# value to the PRC is about 10-20 percent higher than statistics
# indicate.  The cause of this discrepancy is because Hong Kong did
# not add the price of PRC-bound transshipped or transit goods into
# their statistics.  It is also because some goods were not exported
# to the PRC via Hong Kong; therefore Hong Kong's statistics cannot
# represent Taiwan's total exports to the PRC.  According to PRC
# customs, Taiwan exported $12.9 billion of goods to the PRC and
# imported $1.4 billion of goods from the PRC in 1993.  PRC statistics
# on Taiwanese exports should be more reliable because they were based
# on certificates of origin.  (Taipei CHING-CHI JIH-PAO 21 Feb 94 p 9)
# Okinawa Bureau
#
#    NORTH KOREA:  FEATURE:  DPRK-Chosen Soren Joint Ventures Face
# Continuing Problems -- SUMMARY:  According to South Korean press
# reports, since 1990, most of the DPRK's joint venture companies with
# Chosen Soren (the General Association of Korean Residents in Japan)
# have failed because of contract violations, "excessive" government
# control, a shortage of electricity, and difficulties in obtaining
# technology from Japan.  The surviving companies are at "high risk"
# of closing down as well, if current conditions prevail, the reports
# say.
#
#    Since 1984, when joint venture laws were enacted in North Korea,
# Chosen Soren and the DPRK have established about 120 joint-venture
# companies which account for over 60 percent of the total number of
# DPRK joint ventures, according to the 13 January Seoul NAEWOE
# TONGSIN.  The 25 January Seoul HANGYORE SINMUN, citing the ROK
# National Unification Board's recent report to the National Assembly,
# states that since 1990, most of the North Korean joint ventures with
# Chosen Soren have closed down and only 20 some companies--out of
# more than 120--are currently in business.  Moreover, if the DPRK
# maintains its "excessive regulations" and "closed-door policy," the
# remaining joint ventures run the risk of going bankrupt as well, the
# paper asserts.
#
#    NAEWOE notes that, according to Chon Chin-sik, president of
# Moranbong Joint Venture Co. (one of the major DPRK-Chosen Soren
# joint-venture companies), as relations between Japan and the DPRK
# improved following former Deputy Prime Minister Shin Kanemaru's
# visit to Pyongyang in September 1990, North Korea moved from mainly
# dealing with Chosen Soren to attempting to "recruit" Japanese
# companies for joint venture projects.  Chon said that during this
# period, North Korea "ignored" Chosen Soren joint-venture companies.
#
#    Moreover, after the DPRK announced its withdrawal from the
# Nuclear Non-Proliferation Treaty in March 1993, it put "tight"
# restrictions on foreign visitors, including Koreans associated with
# Chosen Soren, and Japanese experts who were to advise the joint-
# venture factories on technical matters, NAEWOE reports.  In
# addition, the energy shortage in North Korea has had an impact on
# Chosen Soren joint ventures as well.  HANGYORE points out that North
# Korea has been giving preferential treatment to domestic companies
# which received their supply of electricity before Chosen Soren
# joint-venture companies.  Furthermore, North Korea has often
# exported substandard goods, causing a loss of credibility for the
# joint ventures and eliciting claims against them, according to
# HANGYORE.  For example, a large quantity of poorly made suits
# manufactured by Moranbong Joint Venture Co. was found at customs
# clearance in Japan last October, NAEWOE says.
#
#    NAEWOE cites additional reasons behind the difficulties
# experienced by the joint-venture companies, such as North Korea's
# violations of contract provisions,  excessive regulations," multiple
# inspections, and bribery.  North Korea has reportedly marketed goods
# in places that were not stipulated under existing agreements, such
# as Macao and Hong Kong, in order to obtain a better profit margin.
# NAEWOE reports that Chosen Soren "strongly protested" against such
# conduct in 1989 at the 4th annual meeting of Korea International
# Joint Venture Union Co.'s board of directors, which is responsible
# for coordinating and giving guidance to DPEK-Chosen Soren joint-
# venture projects.  The board's yearly meeting, whose purpose is to
# set guidelines for upcoming joint-venture activities, has not been
# held since November 1992, NAEWOE notes.
#
#    SOUTH KOREA:  FEATURE:  Patent Office Looks for Countermeasures
# to Patent Disputes -- SUMMARY:  According to recent Seoul press
# reports, the number of ROK patent applications is growing, as is the
# number of patent disputes that ROK firms face.  Yet most firms pay
# scant attention to issues of patents and technology protection.
# Recently, the Office of Patent Administration has started setting up
# patent technology councils to foster cooperation among ROK firms and
# help counterbalance patent disputes.  In addition, it has held an
# open forum to discuss reforming the patent judgment system.
#
#    According to an article in the 9 February CHUGAN MAEGYONG, there
# are four ways to protect ideas using the ROK legal system:  by
# registering patents, utility models, designs, or trademarks.  It
# takes an average of 32 to 34 months to screen a patent or utility
# model application.  While South Korea ranks sixth in the world in
# the number of applications filed for patents or utility models, it
# lacks the systematic backing to help commercialize these ideas,
# according to CHUGAN.  While there are funds available to help cover
# production costs for commercializing new ideas, they only amount to
# about 200 million won ($250,000) annually.
#
#    The 24 January HANGUK KYONGJE SINMUN (HKS) publishes data from
# the Office of Patent Administration showing that South Koreans
# applied for 21,459 patents in 1993, an increase of 34.5 percent over
# 1992.  At the same time patent applications by foreigners dropped
# 0.6 percent.  ROK citizens' applications for low-tech utility models
# totaled 31,505, a l2.8-percent increase over 1992, while foreign
# applications fell 3.9 percent.  Design and trademark applications by
# Koreans rose by 20.4 percent and 40.4 percent, respectively.
# Industrial property rights applications rose 22 percent, to 155,870,
# with corporations accounting for 57.9 percent of the total.
# According to HKS, these increases are not caused by an increased
# awareness of the concept of technology as property, but rather they
# are spurred by the growing number of industrial property disputes
# between both domestic and foreign firms.
#
#    The 29 January HANGUK KYONGJE SINMUN notes that intellectual
# property rights (IPR) disputes are growing in number, and that ROK
# firms do not have sufficient ability to respond to the problem.  The
# Hanbit IPR Center recently surveyed member firms about this issue.
# Of the 153 firms responding, 69.2 percent had been involved in such
# disputes.  For electronics firms, the percentage was even higher-
# -81.3 percent.  Disputes between ROK firms accounted for 50.5
# percent of the cases, while disputes with foreign firms accounted
# for 13.1 percent.  HKS adds that 35.4 percent of the firms had had
# disputes with both domestic and foreign firms.  With regard to
# dispute resolution, HKS reports that 31.3 percent of disputes were
# resolved in court, with the judge finding for one side or the other,
# while 30.3 percent were resolved through compromise.  According to
# HKS, when a dispute involved a foreign firm, ROK firms faced such
# difficulties as a lack of data or technical information (22
# percent), insufficient knowledge of foreign laws (14 percent), and
# high costs (12 percent).
#
#    Most firms have paid little attention to the issue of patents or
# technology protection, reports the 15 January HANGUK KYONGJE SINMUN.
# According to statistics from the Office of Patent Administration,
# 749 manufacturers, or slightly more than 1 percent of all
# manufacturing firms, have set up offices to deal with patent issues.
# Of these, more than 96 percent employ fewer than five workers in
# their patent office.  However, some of the larger firms are devoting
# resources to this area, HKS notes.  Samsung Electronics has a 130-
# member IPR team, Goldstar has a 43-member intellectual property
# management office, and Daewoo Electronics, Goldstar Electron, and
# Hyundai Electronics are all expanding their patent-related offices.
# HKS comments that the most "anxious" organizations within
# electronics firms are those responsible for industrial property
# rights.  Firms must control their technology through patents, the
# paper suggests, and patent experts, who are scarce, should be
# quickly trained.  HKS also notes by cooperating on technology
# development, firms might reduce the burden of industrial property
# rights disputes.
#
#    There are already moves towards cooperation on a larger scale.
# According to the 4 February MAEIL KYONGJE SINMUN (MKS), "patent
# technology councils" are becoming active in high-tech areas.  These
# councils enable firms to share reciprocal licenses or patent rights.
# MKS reports that the Office of Patent Administration is considering
# cooperative "countermeasures" to international patent disputes and
# the rise in foreign countries "patent aggression," and this year
# will set up three new patent technology councils--for computers,
# electric ranges, and construction.  At the end of 1993 it set up
# nine councils, covering washing machines, electronic circuits,
# antibiotics, synthetic textiles, PVC processing technologies,
# organic and inorganic chemistry, waste disposal technology for steel
# producers, and CFC substitutes.  The patent administration believes
# that these councils could indirectly aid firms in technology
# development by supplying information on leading edge technologies.
# MKS predicts that as these councils become more active, cross-
# licensing agreements will flourish.  Another measure which would
# promote technological cooperation--a proposal to grant tax benefits
# to firms that have concluded cross-licensing agreements--is under
# consideration, according to MKS.
#
#    On the legal front, there are voices calling for establishing a
# "patent court," reports the 25 January HANGUK KYONGJE SINMUN.  On 24
# January, the Korea Chamber of Commerce and Industry held a public
# forum on the issue of revising the patent judgment system.  At the
# meeting, representatives from business and technology circles
# demanded the establishment of a patent court that includes judges
# who are technical experts.  (According to the 25 January MAEIL
# KYONGJE SINMUN, currently the Office of Patent Administration
# handles an initial patent dispute trial and the first appeal, if
# any.  If those involved in the case still disagree with the ruling,
# they may appeal to the Supreme Court for a third trial.)  Industrial
# circles question the cost, timeliness, and courts' ability to make
# technical judgments under the current system; they recommend setting
# up a patent court.  One industry representative emphasized that in
# patent judgments a factual trial is more important than a legal
# analysis.  HKS reports that patent attorneys oppose letting the
# patent office handle the first and second trials, and suggest
# establishing a patent court composed of both technical and legal
# judges.  Legal circles also oppose the patent office's role,
# maintaining that it is unconstitutional.  According to HKS, this
# group would like to see a patent department set up in the Seoul High
# Court, with the existing court handling matters and bringing in
# technical aides and advisory groups.  Finally, the Office of Patent
# Administration asserts that the current system is legal.  It does,
# however, recognize a drop in the quality of judges.  It recommends
# setting up a patent judgment court within the current framework, and
# raising the number of technical judges to improve the quality of
# judgments.
#
#    FEATURE:  ROK Efforts in Obtaining Foreign Commercial Technology
# Chronicled -- SUMMARY:  South Korea is using a variety of methods to
# acquire advanced foreign commercial technology, according to ROK
# press reports.  Recognizing a "gap" between the level of technology
# employed by foreign competitors and what is available domestically
# to ROK manufacturers, industry and government are jointly engaged in
# efforts to compensate by appropriating foreign know-how as the basis
# for the country's commercial S and T programs.
#
#    Seoul business newspapers recently published several articles
# describing efforts by the ROK Government and commercial firms to
# promote economic competitiveness through the use of foreign
# technology.  These methods reportedly include using public funds to
# indigenize foreign high-tech, hiring foreigners with technical
# expertise, collecting technical intelligence through overseas ROK
# subsidiaries, identifying and recruiting expatriate scientists,
# technical "cooperation" with foreign companies, and exploiting cash-
# strapped Russian firms for patented technology (see related article
# in PACIFIC RIM ECONOMIC REVIEW Vol 2 No 20, 6 Oct 93 pp 24-26).
#
#    The number of cases listed would increase significantly if
# reports of technical agreements, licensed production of foreign
# products, buyouts of foreign firms, "indigenized" products, new
# overseas "research" facilities, and other types of scientific
# "exchanges" (where the transfer or appropriation of foreign
# technology is implied) were also included.  The picture that emerges
# through ROK press reporting in recent months on South Korea's
# intensified quest for technology is that of a country striving to
# close the "gap" with "advanced countries" more through imitation
# than innovation.  This is reflected in the ROK press' habitual use
# of verbs such as "acquire," "accumulate," and "indigenize," while
# the term "develop" is usually restricted to broad technologies with
# little specific content or to ROK efforts to reinvent existing
# products, and the word "create" simply does not appear.
#
#    South Korea To 'Develop' Laser Disk Drive - The ROK Government
# and domestic computer manufacturers will jointly develop a laser
# disk drive for use with peripheral equipment in next-generation
# computers.  Work began in December 1993 with a 370-million won
# ($462,500) grant from the Ministry of Trade, Industry and Energy
# (MOTIE) to the Korea Computer Research Association, which is
# managing the project with Goldstar's and Hyundai Electronics'
# participation.  The drive will be ready for domestic use and export
# by 1997.
#
#    Goldstar has on hand laser disk drive technology which it
# imported from Japan in 1990.  Hyundai, for its part, obtained "world
# standard" technology from its buyout of the U.S. electronics firm
# Maxter, and claims  we won't have much trouble developing it."  The
# project is also expected to give a big boost to domestic
# manufacturers of recording equipment that uses laser disk
# technology, and could lead to "indigenizing" all parts connected
# with computer memory devices.  (Seoul MAEIL KYONGJE SINMUN 20 Jan 94
# p 15)
#
#    ROK Companies Hiring More Foreigners - The number of ROK firms
# that hire foreign specialists "to overcome the technological gap
# with competitors in advanced countries" is rising.  Even mid-size
# firms are discovering they can defeat "barricades to technology"
# erected by another country by hiring that country's nationals,
# directly or through overseas subsidiaries.  The latter are sent to
# South Korea periodically "to solve problems that occur on production
# lines and for technical consultations."  The strategy of hiring
# foreigners with technical skills to improve the competitiveness of
# ROK products is likened to "using barbarians to control barbarians."
# (Seoul MAEIL KYONGJE SINMUN 8 Feb 94 p 14)
#
#    U.S.-Based Subsidiaries Collecting Technical Information - ROK
# factory automation (FA) companies are busily setting up subsidiaries
# abroad to open up new markets for their products, and to "beef up
# their collection of technical information."  Poscon's new subsidiary
# in Delaware, Poscon International Corporation (PIC), will attempt to
# market its own FA products in the United States while it "engages in
# technical information collection activities."  Samsung Aerospace
# will form two "teams" this year for FA equipment exports and control
# equipment exports, while stepping up activities at its U.S.
# subsidiary Samsung Optical America (SOA).  (Seoul MAEIL KYONGJE
# SINMUN 7 Feb 94 p 18)
#
#    'Brain Pool' To Identify, Recruit Expatriate Scientists - The
# Ministry of Science and Technology (MOST) will begin operating a
# "brain pool" this year aimed at inducing high-level scientists
# abroad to come to South Korea and help the country "acquire at an
# early date the newest science, technology, and know-how in the R and
# D stages in advanced countries, and breathe life into the domestic R
# and D scene."  The ministry will recruit 100 "overseas Korean" and
# other foreign scientists in 1994, and if the program is effective
# expand its scope in subsequent years.
#
#    Recruits will be leading scientists and technicians with more
# than five years postdoctoral experience in their countries of
# residence.  Exceptions will be made for personnel with world class
# achievements who lack these credentials.  South Korea will pay
# round-trip transportation, all moving expenses, and a salary higher
# than that currently received.  A review will be made every six
# months of each individual's performance as a basis for deciding
# whether to continue the contract.
#
#    The system will allow MOST "to make systematic use of more than
# 40,000 expatriate Korean scientific personnel, including the 14,000-
# plus members of the Association of Overseas Korean Scientific and
# Technical Personnel" and "top notch" Western and former-Soviet
# scientists.  MOST is instituting the system "to deal effectively
# with the increasing reluctance of advanced countries lately to
# transfer core technology" and to help "overcome South Korea's
# inferior domestic research and educational environments."  (Seoul
# MAEIL KYONGJE SINMUN 25 Jan 94 p 13)
#
#    MOTIE Subsidizes Technical 'Cooperation' With Japan - MOTIE will
# spend 100 billion won ($125 million) between now and 1997 to support
# companies specializing in Japanese exports.  The ministry will also
# solicit greater "technical cooperation" with Japan through the "ROK-
# Japan Technical Cooperation Foundation."  Firms which shipped $1
# million in goods to Japan, and more than 50 percent of their total
# exports, will have up to two-thirds of their R and D costs
# subsidized from a "Basic Industrial Technology Development Fund."
# In addition, some 20 billion won ($25 million dollars) of the $125
# million export subsidy fund will be used to help ROK companies
# market their products in Japan.
#
#    Technical cooperation with Japan will be facilitated by 3.26
# billion won ($4.075 million) spent on personnel exchanges, 600
# million won ($750,000) to support joint research, 160 million won
# ($200,000) on "structural activities for basic industrial
# technological cooperation," and other related subsidies totaling 4.4
# billion won ($5.5 million).  MOTIE will increase the number of
# technicians it sends to Japan for training from 197 in 1993 to more
# than 300.  Another 30 retired Japanese technicians will be invited
# to South Korea to provide "technical guidance" to ROK small and
# medium businesses (SMB's).  (Seoul MAEIL KYONGJE SINMUN 31 Jan 94 p
# 4)
#
#    ROK Firms Importing Patented Russian Technologies - According to
# the ROK Patents Administration, 41 South Korean companies have
# applied to transfer 365 different patented Russian technologies
# since October 1993.  The ROK firms include 22 conglomerates, 14
# SMB's, and five research institutes, including the Korea Atomic
# Energy Research Institute (KAERI).  Applications by field number 157
# in electricity and electronics, 143 in chemistry, 31 in machinery
# and metals, and 34 others.  (Seoul HANGUK KYONGJE SINMUN 31 Jan 94 p
# 15)
#
#    FEATURE:  Electronics Companies Focusing on Large Screen TV's -
# SUMMARY:  South Korean electronics firms are marketing a variety of
# large screen color televisions, including conventional designs with
# screens up to 46 inches, and newer "widescreen" models which make
# use of redesigned picture tubes for a flatter chassis, according to
# Seoul press reports.  At least one ROK firm is seeking to apply
# plasma display technology to "multivision" TV's with screens more
# than eight feet wide.  The industry regards these products as
# "transitional" steps on the way to high-definition equipment now
# being developed.
#
#    South Korean electronics manufacturers are turning their
# attention to large screen color televisions in response to
# increasing demand for upscale commercial appliances both
# domestically and abroad.  According to the 9-16 February CHUGAN
# MAEGYONG, large color TV's held 5 percent of the ROK market in 1990,
# 11 percent in 1991, 21 percent in 1992, and 27 percent last year (35
# percent by value).  At present, the most popular models are 25-inch
# sets which have 70 percent of the large screen market, 29-inch with
# 25 percent of the market, and 33-inch with 4 percent.  A small
# number of homes have 42-inch and 46-inch projection TV's, the
# magazine reports.
#
#    These units, whose verticle-to-horizontal dimensions have a fixed
# ratio of 3:4, differ from the widescreen color TV's just now being
# marketed which are proportionately wider and based on different
# technology.  According to the 9 January MAEIL KYONGJE SINMUN (MKS),
# South Korea's first domestic widescreen television--a 36-inch model-
# -was introduced in February 1993 by Goldstar.  A follow-up model
# with a 32-inch screen that can project as many as four pictures on
# the same screen (picture-in-picture or PIP) came out at the end of
# last year.  Goldstar expects 1994 sales of the two models to reach
# 2,000 and 6,000 sets, respectively.  Samsung Electronics recently
# introduced its own 32-inch widescreen model with PIP and
# stereophonic sound, and is bringing out a 28-inch model later in
# 1994.  Total sales are expected to pass 10,000.  Daewoo and Anam
# reportedly will market competitive products shortly.
#
#    Meanwhile, the 11 January MKS reports that Samsung Electron
# Devices has made South Korea the "second country after Japan" to
# develop a flat cathode ray tube for widescreen TV.  The company
# spent one year and 5 billion won ($6.25 million) "indigenizing" the
# part which will be used in 32-inch screens.  The tube reportedly is
# "twice as flat" as existing models.  It uses a 32.5 mm electron gun
# (down from 37.5 mm) and Samsung's "double dynamic focus" system to
# produce clear pictures.  The newspaper reports the tube will be used
# in widescreen televisions just now being produced in South Korea,
# and in the high-definition television (HDTV) sets of the future.
# The 9 January MKS states that the ROK electronics industry views
# widescreen TV as a "transitional by-product" of HDTV, which is
# expected to "dominate" the market by the year 2000.
#
#    In a related development, the 10 February Tokyo NIKKEI SANGYO
# reports that Orion Electronics, a subsidiary of the Daewoo Group,
# has established a joint venture with Russia's Gas Discharge
# Equipment Research Lab (under the jurisdiction of Russia's Munitions
# Industrial Committee) to produce plasma display panels (PDP's).  The
# equipment, originally produced for Russia's aerospace program,
# reportedly is being designed for use with extra large
# ("multivision") televisions with 100-inch plus displays.  According
# to the newspaper, PDP's are much narrower than conventional cathode
# ray tubes, and offer a brighter screen than liquid crystal displays
# (LCD's).  The new company, Orion Plasma Research and Production,
# will be located southeast of Moscow.  Each partner will supply half
# of the $4-million capital.
#
#    Government Committee Devising NAFTA Countermeasures - On 24
# January, the ROK Government's "NAFTA Countermeasures Committee"
# consisting of 17 members from trade-related agencies and industry
# met to discuss a "new strategy" that entails increasing local
# investment, moving "full-scale" into the U.S. distribution market,
# relying on trade diplomacy, and strengthening industrial
# technological "cooperation."  The committee agreed that plans to
# secure a share of the North American market will be frustrated
# unless accompanied by direct local investment.  In those sectors
# where South Korean exports lose their competitiveness to Mexican
# goods which enter the United States duty free, South Korea will
# react by reducing distribution expenses through more aggressive
# export marketing.  A fact-finding team will be sent to the United
# States in the first half of 1994 to survey the distribution market,
# while ROK companies are encouraged to participate in U.S. trade
# exhibitions and make other efforts to find local vendors.
# Competitiveness of South Korean products will also be enhanced by
# strengthening technological "cooperation" through the ROK-U.S.
# Industrial Cooperation Foundation.  In terms of diplomacy, South
# Korea will use the Uruguay Round and bilateral trade negotiating
# forums to check NAFTA's "excessive discrimination" against non-
# member countries as evidenced, for example, in its stringent
# country-of-origin criteria.  The committee plans to have a "full-
# blown NAFTA strategy" ready by March this year.  (Seoul MAEIL
# KYONGJE SINMUN 25 Jan 94 p 6)
#
#    Study Compares ROK and Japanese Overseas Investment Strategies -
# The Korea Chamber of Commerce and Industry has published a
# "Comparative Study of Direct Overseas Investment Strategies by South
# Korean and Japanese Companies."  The study points out that Japan
# follows a two-part strategy of manufacturing high value-added, high-
# tech products at home while farming out medium and low value-added
# work to overseas production sites.  Also, Japan continuously shifts
# its overseas sites depending on the manufacturing cost and the
# "technological level of the product targeted for investment" so that
# no country obtains more technology than what it already has.
#
#    Conversely, the study notes that ROK firms appreciate less the
# need to keep technology out of other countries' hands, and are
# concerned only with raising productivity at the overseas site.  It
# adds that South Korean companies take high risks, by Japanese
# standards, in moving production to countries such as China, Vietnam,
# and Burma without making a full analysis of the situation and with
# no means to deal with unfavorable changes that may develop.  Japan's
# ability to keep high technology at home and diversify its overseas
# labor sites effectively "squeezes" ROK firms which are adept at
# doing neither.  (Seoul MAEIL KYONGJE SINMUN 26 Jan 94 p 12)
#
#    KDI Approves of Samsung's Entry Into Auto Production - The Korea
# Development Institute (KDI), a national policy group with close ties
# to the ROK Government, recently reported it "agrees in principle"
# with Samsung's bid to enter the passenger car market.  KDI
# acknowledged that "overlapping investment" would be inefficient in
# terms of the domestic market, but that exports could expand with the
# enhanced competitiveness that Samsung's entry would help bring
# about.  KDI observed that instead of putting "unreasonable
# restrictions" on the auto industry, government should support it by
# investing in related R and D and training of personnel.  KDI's
# approval follows a similar recommendation made last November at a
# seminar of international experts.  The findings are expected to have
# a major impact on the Korea Institute for Industrial Economics and
# Trade's recommendation to the Ministry of Trade, Industry, and
# Energy this April.  (Seoul MAEIL KYONGJE SINMUN 17 Jan 94 p 3)
#
#    Samsung Develops One-Chip Integrated Circuit - Samsung
# Electronics Co. has developed a high-fidelity one-chip integrated
# circuit (IC) for wireless phones, that combines the functions of
# four standard IC's.  Using the circuit could reduce the number of
# IC's used in wireless phones from 12-13 to two or three, and reduce
# the phone's components by 25-30 percent.  This could pave the way
# for miniaturization of wireless phones.  (Seoul YONHAP 0133 GMT 17
# Feb 94) Seoul Bureau
#
#    Hyundai Motors Opens Car Institute - Hyundai Motors recently
# opened a research institute at the Korea Advanced Institute of
# Science and Technology (KAIST) to develop high-tech auto
# technologies and groom skilled workers.  The institute, named
# "Smarveh" (Smart Vehicle Laboratory), is manned by five KAIST
# professors specializing in machinery and 15 KAIST researchers.  The
# institute will concentrate on developing cleaner-running, quieter,
# and safer cars. It will also focus on producing more than 1O auto
# experts with masters-degree level diplomas each year.  Hyundai
# supplied research equipment worth 200 million won ($250,000) and 300
# million won ($375,000) in cash to the institute.  (Seoul THE KOREA
# TIMES 20 Feb 94 p 8) Seoul Bureau
#
#    Seoul, Beijing Seeking Industrial Alliance - The ROK Government
# will seek an industrial cooperation agreement with China.  For South
# Korea, the main areas of cooperation would include aircraft,
# automobiles, digital telephone exchanges, and nuclear power plants,
# while China is interested in high-definition television (HDTV),
# facsimile, and large-screen televisions.  South Korea has already
# announced an aircraft development plan, and China is expected to be
# invited to participate in it.  In the automotive sector, South Korea
# has asked China to allow ROK car imports, and will encourage ROK
# parts producers to invest in China.  The ROK Government is also
# eager to become involved in the modernization of China's telephone
# networks.  Nuclear power is another promising area of cooperation as
# China constructs new nuclear power plants.  The Korea Electric Power
# Corporation (KEPCO) has signed an agreement to provide operational
# and management services to a nuclear power plant in Guangdong
# Province.  (Seoul TONGA ILBO 18 Feb 94 p 11) Seoul Bureau
#
#    Companies Withdraw From Indonesia Because of Rising Labor Costs -
# ROK companies are closing their plants in Indonesia due to wage
# hikes.  The average daily wage in Indonesia increased from $1.05-
# $1.33 last year to $1.67 recently, an increase of 25 to 60 percent.
# ROK companies plan to move their plants to Vietnam or China, where
# labor costs are lower.  Samsung closed its sewing plant in west
# Jakarta at the end of last year and is moving to close five other
# plants.  Sokwang closed one of two plants in Indonesia, and Lucky-
# Goldstar International is considering selling its plant.  (Seoul
# HANGUK ILBO 21 Feb 94 p 5) Seoul Bureau
#
#    Plant Exports to China on Increase - ROK companies are increasing
# plant exports to China as economic cooperation between the two
# countries is expected to "improve drastically" following President
# Kim Yong-sam's visit to China.  According to the Korea Export and
# Import Bank, major ROK companies are expanding from small-volume
# trade to large-scale plant projects in China.  The bank has received
# applications for deferred payment for nine projects with a total
# value of $167 million.  Plant exports range from port facilities to
# telecommunications cable equipment and railroads.  (Seoul MAEIL
# KYONGJE SINMUN 21 Feb 94 p 4) Seoul Bureau
#
#    Companies To Participate in Telephone Business in Russia - Dacom
# and Goldstar Data Communications will sign a contract with Russia on
# 25 February to establish a joint communication corporation that will
# provide local phone service to Russia's Maritime Province.  Dacom
# will invest 1,440 million won ($1.8 million) in the project and hold
# a 45-percent share in the venture, while Goldstar Data
# Communications will hold 5 percent and six Russian companies will
# have a 50-percent share.  (Seoul MAEIL KYONGJE SINNUN 25 Feb p 11)
# Seoul Bureau
#
#    Goldstar Signs Communications Agreement With Romania - Goldstar
# Information and Communications has signed a turnkey agreement to
# supply $50 million worth of telecommunications equipment to Rom
# Telecom of Romania.  The equipment will be used to modernize the
# telephone network in Prahova Province, a project that will cost $75
# million.  The ROK's Economic Development and Cooperation Fund (EDCF)
# will provide $50 million in loans to help the Romanian Government
# purchase the equipment.  Goldstar will supply two types of digital
# telephone exchanges (TDX), STAREX-TD1 for small cities and STAREX-
# IMS for rural villages.  The firm will also provide optical
# transmission equipment, microwave equipment, and cables.  Goldstar's
# $50-million contract is the largest TDX contract ever for a ROK
# firm.  (Seoul THE KOREA HERALD 24 Feb 94 p 8) Seoul Bureau
#
#    China Emerges as Major Export Market for ROK Textiles - China has
# emerged as a major textile market for ROK companies.  According to
# the Korea Federation of Textile Industries, textile exports to China
# between January and November 1993 totaled $756 million, a 71.4-
# percent increase compared to the same period in 1992.  This makes
# China the fifth largest export market for ROK textiles, or the
# second largest if exports through Hong Kong are included.  (Seoul
# MAEIL KYONGJE SINMUN 23 Feb 94 p 11) Seoul Bureau
#
#    SOUTHEAST ASIA:  INDONESIA - FEATURE:  Government Urged To Reduce
# Cost of Economy -- SUMMARY:  Jakarta press sources recently reported
# the views of several economists on Indonesia's "high cost economy."
# These economists stress the need to stimulate overall economic
# activity, reduce production costs, and attain better productivity
# and efficiency, so that Indonesia can achieve economic growth as
# well as become more competitive in overseas markets.
#
#    Sumitro Djojohadikusumo, President Suharto's senior economic
# advisor, recently expressed his concern over Indonesia's high cost
# economy and his remarks were cited in several major Jakarta dailies
# on 22 January.  Sumitro's analysis of the economic situation, as
# reported in BISNIS INDONESIA, KOMPAS, SUARA PEMBARUAN, and MERDEKA,
# is based on a "capital-output ratio," using quantitative and
# empirical data, as well as statistical figures from the Central
# Bureau of Statistics.  Sumitro's conclusion is that Indonesia's
# economic development has been "less efficient and less effective"
# compared with other ASEAN countries whose economies are
# "structurally similar."  The papers also note that Sumitro
# attributes this "undesirable situation" to the "large amounts of
# waste and losses," caused by mismanagement; investments in
# infrastructure that have slow or little yield; "incompetence" in
# planning, operating, and maintaining investment projects; and
# "irregularities" such as graft.
#
#    BISNIS INDONESIA reports that during Indonesia's fifth Five-Year
# Development Plan (1989-1994), public and private investments
# amounted to 33.4 percent of the national income, with annual
# economic growth at 6.8 percent.  Based on these figures, the
# incremental capital-output ratio (ICOR) is 33.4 : 6.8 = 4.9 or 5.
# This ICOR, Sumitro points out, is "somewhat high" compared to the
# ratios for other ASEAN countries, which generally range from 3 to
# 3.5.  Sumitro suggests that a reduction in the cost of the economy
# will ultimately result in Indonesia's becoming more competitive
# abroad and in a higher economic growth for the country; he adds that
# if the ICOR during the second stage of Indonesia's long-term
# development cycle could be reduced to 3.5, and if investments remain
# at 33.4 percent of national income, Indonesia could achieve an
# annual growth of 9.5 percent (33.4 : 3.5).
#
#    Sumitro's assessment of the country's economic situation
# coincides with that of Rizal Ramly, executive director of the
# economic, industrial, and trade consulting firm Ekonit.  According
# to a 23 January KOMPAS editorial, Rizal believes that new measures
# to directly address Indonesia's high cost economy should be worked
# out and implemented in order to improve the country's
# competitiveness in overseas markets.
#
#    Economists Priasmoro Prawiroardjo and Hadi Soesastro of the
# Center for Strategic and International Studies share Rizal's view
# that a new set of deregulation policies is deeded.  According to the
# 22 January KOMPAS, Hadi believes that improving the business climate
# would play an important role in stimulating overall economic
# activity and in improving efficiency in the industrial sector, while
# Priasmoro views production efficiency as the key problem that
# Indonesian exporters must overcome to penetrate the world market.
# Priasmoro stresses that cutting back on production cost alone will
# not be enough and that improved macroeconomic conditions are also
# necessary.  Moreover, he asserts that implementation of the
# agreements reached at the Uruguay Round will pose more challenges
# than opportunities to the Indonesian industrial sector.  He also
# points out that Indonesia's electronic industrialists are already
# concerned about the competition that will come from AFTA (Asean Free
# Trade Area).  They fear that under the Common Effective Preferential
# Tariff (CEPT) plan of AFTA, the market will be saturated with
# electronic products from Singapore, Malaysia, and Thailand.  And
# because of the time-consuming procedures and "unpredictable costs"
# associated with investing in Indonesia (such as "illegal levies"
# that have to be paid to obtain business licenses), these
# industrialists predict that other Indonesian products have little
# chance of getting a share of the international market, KOMPAS
# reports.
#
#    FEATURE:  Workers Strike as Government Enforces Minimum Wage
# Decree -- SUMMARY:  Several Jakarta newspapers report that thousands
# of employees went on strike recently to demand better treatment by
# their employers and an increase to the $2 daily minimum wage
# recently set by the government for Jakarta and its surrounding
# areas.
#
#    The 4 February ANGKATAN BERSENJATA and SUARA PEMBARUAN report
# that thousands of employees of several companies in the Tangerang
# area went on strike three weeks after a ministerial decree on an
# increase in daily minimum wage went into effect on 1 January.  The
# strikes occurred after employers turned down the employees' demand
# for a 26-percent increase in the daily minimum wage--which is
# approximately $2--set by the government.  In Bekasi, 30 km east of
# Jakarta, 1,200 workers from five companies went on strike early last
# week, according to the 7 February ANGKATAN BERSENJATA.  In addition
# to a salary increase, workers demanded that companies grant them
# better benefits and special allowances.  The paper also states that
# reports from Bandung indicate that hundreds of employees went on
# strike for the same reasons as their counterparts in Bekasi, while
# hundreds of workers from Bogor demonstrated in front of the Ministry
# of Manpower.  The demonstration prompted a government investigation
# into allegations that employers are violating the minimum wage
# regulations, ANGKATAN BERSENJATA says.
#
#    SUARA PEMBARUAN notes that most employers have proposed that the
# decree enforcement be postponed until April, citing the need for
# more time to adjust their payrolls, not only in connection with the
# wage hike but also for the annual "Lebaran" (festivities at the end
# of the fasting month) bonus in March.  The paper also quotes
# Tangerang Regent Saifullah Abdulrahman who said that out of 870
# companies in the region, at least 80 small and medium firms cannot
# afford to pay their workers a daily minimum wage of $2.  Saifullah
# stated that some of the firms have even filed a protest to the
# Ministry of Manpower and have enclosed their financial statements.
# However, the paper continues, Manpower Minister Abdul Latief has
# stated that based on the outcome of a recent survey on cost
# structure, companies are in fact capable of and should be paying
# their workers more.  Latief said that labor cost averages only 9.8
# percent of total production cost, which is "too small."  He also
# asserted that, according to the All-Indonesia Labor Union (SPSI),
# some companies in the shoe industry have spent only 2 percent of
# their total operational budget on labor.  SPSI General Secretary
# Bomer Pasaribu attributes this "deplorable situation" to the fact
# that employers have always regarded wages as part of production
# cost, subject to reduction, and hence wages have always been
# suppressed.
#
#    Minister Latief warns businesses that more strikes will occur
# prior to Lebaran, unless employers become more responsive to
# workers' demand for better pay and better benefits, ANGKATAN
# BERSENJATA reports.  The paper also quotes Aburizal Bakrie, chairman
# of the Indonesian Chamber of Commerce and Industry, who called on
# all employers to willingly comply with the minimum wage regulation.
# Bakrie said that "workers are assets, not production tools," and
# that the minimum wage is set at "a low level so companies won't be
# burdened."
#
#    According to the 8 February KOMPAS, the government is determined
# to make companies comply with the minimum wage regulation.  The
# paper says that President Suharto has ordered his cabinet ministers
# to make a list of the companies that violate the regulation and/or
# operate without a labor union, and to take the necessary steps
# against them.  The president has stated that employers should not be
# concerned with profits only, but that they must also pay attention
# to the rights and welfare of workers, the paper reports.
#
#    Central Bank Needs $400-Million 'Standby Loan' - The Bank of
# Indonesia (Central Bank) recently announced that Indonesia has
# tasked six international banks to come up with a $400-million
# "standby loan."  The six banks include Banque Nationale de Paris,
# Bank of Tokyo in Hong Kong, Chase Manhattan Asia, Dresdner,
# Industrial Bank of Japan, and Long Term Credit Bank, Asia.
#
#    The seven-year loan will be signed in March, with a utility
# period of five years after the loan is signed.  It will be repaid in
# five installments every six months, starting at the end of the first
# five years.  The interest for the first two years is set at 0.75
# percent above LIBOR (London Interbank Offered Rate), and in the
# third year, the interest will increase to 0.875 percent above LIBOR.
#
#    Former Finance Minister Frans Seda said the loan will only be
# used in the event the government is unable to pay for non-oil/gas
# imports, or as a safeguard for the balance of payments.  (Jakarta
# KOMPAS 28 Jan 94 pp 1, 5)
#
#    Government Discontinues 'Protection' of Steel Industry - Minister
# of Industry Tunky Ariwibowo recently announced that the government
# will no longer "protect" the national steel industry, even in the
# event of declining world steel prices.  Ariwibowo said the decision
# is meant to force the national company P.T. Krakatau Steel to become
# more efficient and more competitive.  This decision is also
# necessary to counteract a claim by the United States that Indonesia
# is dumping its steel in the international market, the minister said.
# (Jakarta KOMPAS 28 Jan 94 p 3)
#
#    P.T. PAL To Shift Production Focus - A recent report issued by
# P.T. PAL, a state-owned shipyard in Surabaya, states that within two
# years, the company intends to stop producing small ships in the 900-
# 4,200 dead weight ton (dwt) range, and will start building war ships
# and larger ships up to 40,000 dwt.  The report does not specify what
# type of war ships P.T. PAL expects to produce, but the larger ships
# will include coal carriers, passenger ships, container carriers up
# to 2,700 twenty feet equivalent unit (teu), and oil tankers up to
# 30,000 dwt.  (Jakarta KOMPAS 4 Feb 94 p 7)
#
#    Increase in French Investments Reported - The Capital Investment
# Board recently reported that French investments in Indonesia in 1993
# registered a total of $431 million, a 68.3-percent increase over the
# previous year.  Most of the investments were in the chemical,
# electronic, and gas industries, and in the hotel, banking, and
# financial sectors.  (Jakarta ANGKATAN BERSENJATA 21 Jan 94 p 3)
#
#    Agriculture's Contribution to GDP Drops to 19 Percent -
# Agriculture Minister Syarifudin Baharsyah recently said that the
# agriculture sector's contribution to GDP has dropped to 19 percent,
# causing a loss of jobs in the sector and particularly in farming.
# Syarifudin expects the figure to continue to drop, down to as low as
# 15 percent eventually.  (Jakarta ANTARA 1032 GMT 28 Feb 94) Bangkok
# Bureau
#
#    MALAYSIA:  Contract for Asia Pacific Cable Network Signed - Nine
# Asian telecommunication companies have recently signed a $7.16-
# million contract with Fugro Survey Private Ltd. to study the
# region's optic fiber submarine cable system for the Asia Pacific
# Cable Network (APCN).  The nine companies include Singapore Telecom,
# Telekom Malaysia Berhad, Communications Authority of Thailand, Hong
# Kong Telecom International Ltd., Indonesia's Indosat, Taiwan's
# International Telecommunication Development Corp., Japan's Kokusai
# Denshin Denwa Company Ltd., the Philippines' Long Distance Telephone
# Company, and Korea Telecom.  The study is designed to find a safe
# and economically viable route for the APCN.  Expected to be put into
# service in 1996, the APCN will comprise two submarine cable systems:
# the first system will connect Japan, Korea, Taiwan, Hong Kong, the
# Philippines, Malaysia, and Singapore, and the second will link
# Thailand, Malaysia, Singapore, and Indonesia.  (Kuala Lumpur BERNAMA
# 0437 GMT 24 Feb 94) Bangkok Bureau
#
#    PHILIPPINES:  Proposals for Satellite Project Reported -
# Transportation and Communication Undersecretary Josefina Lichauco
# recently stated that the Philippines has begun to receive proposals
# from various private consortiums for a project to launch its own
# satellite or to lease a satellite from another country.  Lichauco
# stressed that the government will facilitate the project which will
# be under a government build-operate-transfer arrangement, with the
# consortiums financing and overseeing construction of the entire
# project.  The consortiums will then be given the right to operate
# the project for a specified period in order to recoup their
# investments.  The prospective satellite firm will be a 60-percent
# Filipino-owned public utility and the rest of the equity will be
# open to foreign partners.
#
#    To date, Manila has received proposals from Russia-based Global
# Information Systems, Malaysia's Measat, Thailand's Shinawatra group,
# and U.S.-based Rimsat.  Other companies that have expressed an
# interest include Europe's Arianespace and Matra Marconi, Hong Kong's
# Asiasat, and U.S. companies such as Hughes Space and Communications,
# Martin Marietta, and Panamsat.  (Manila BALITA 10 Feb 94 p 2, 11 Feb
# 94 p 3)
#
#    SINGAPORE:  'Largest' Petrochemical Investment Announced - A
# partnership of leading chemical firms from Europe, Japan, and the
# United States will invest over $1.875 billion in the second
# petrochemical complex on Ayer Merbau and Seraya islands.  It will be
# the single largest foreign investment in Singapore.  The project is
# expected to be completed in the second quarter of 1997 and will
# include Singapore companies such as the Petrochemical Corporation of
# Singapore, the Polyolefin Company, Denka Singapore, and Seraya
# Chemicals Singapore.  (Singapore Singapore Broadcasting Corporation
# 1100 GMT 1 Mar 94) Bangkok Bureau
#
#    THAILAND:  Rice Sale to North Korea Reported - Deputy Prime
# Minister Amnuai Wirawan said recently that Thailand will sell North
# Korea 50,000 tons of rice under a two-year credit plan.  Thailand
# had previously agreed to sell 200,000 tons of rice, but North Korea
# has delayed issuing a letter of credit.  To maintain the
# relationship, Thailand has decided to proceed with a lesser sale at
# this time.  (Bangkok BANGKOK POST 23 Feb 94 p 20) Bangkok Bureau
#
#    Cabinet Approves Soybean Import - The cabinet has approved the
# import of 98,000 tons of soybean, following the recommendation of
# the Soybean and Other Oil Crops Policy Committee.  Some 5,000 tons
# will be imported from Laos and 10,000 tons from Cambodia.  The
# imports must be completed by July and no imports are allowed during
# March or April.  Current annual domestic demand for soybean is 1.2
# million tons, while production is only about 400,000 tons.  Thailand
# spends about $160 million annually on soybean imports.  (Bangkok
# Radio Thailand Network 0000 GMT 2 Mar 94) Bangkok Bureau
#
#    VIETNAM:  FEATURE:  Losses in Rice Export Earnings Reported --
# SUMMARY:  A Hanoi press report notes that Vietnamese rice dealers
# suffered losses of about $2 million in rice export earnings in
# October 1993, mainly because of a shortage of funds and stiff
# competition among the dealers.  The same report shows that Vietnam
# currently ranks third among world rice exporters and points out the
# need for changes in the State's management of rice export.
#
#    According to a 22 August 1993 Hanoi VNA report, between 1989 and
# 1992, Vietnam exported 5.76 million metric tons of rice worth over
# $1 billion.  The 5 January THOI BAO KINH TE VIET NAM notes that in
# the last three years, the country has exported a yearly average of
# about 1.7 million metric tons of rice, which brought in revenues
# that are second only to earnings from  crude oil export.  The 6-12
# January TUAN BAO QUOC TE points out that although Vietnam currently
# ranks third among world rice exporters, rice dealers have registered
# losses of about $2 million in October 1993, in exporting more than
# 100,000 metric tons of rice.
#
#    TUAN BAO QUOC TE (TBQT) suggests that one of the main reasons for
# the losses in rice export earnings is the stiff competition between
# rice dealers, resulting in rising domestic purchase prices and
# falling export prices.  Another reason cited by the newspaper is
# poor management" by the State.  Despite a government directive to
# reduce the number of principal rice exporters to 17, there were
# still over 40 exporters in November 1993, since any firm with a
# contract listing prices commensurate with government prices could
# obtain an export permit, including those who did not have storage
# space or processing mills.
#    TBQT also cites the shortage of funds used to buy rice as a
# problem.  Some $200 million were actually required to purchase rice
# in the Mekong River delta, but the largest amount received was only
# $740,000 and the smallest $45,000, while small enterprises received
# only 10 percent of the funds needed.  According to TBQT, few firms
# want to sign big contracts and take out loans to buy rice for export
# ahead of time, but they will rush out to make rice purchases only
# when customers offer letters of credit and ships start to come in.
#
#    TBQT reports that Vietnamese rice export increased from 1.42
# million metric tons in 1989 to 1.95 million metric tons in 1992, and
# totaled 1.7 million metric tons in 1993.  The number of countries
# who have signed purchase contracts with Vietnam has also increased
# from 24 in 1992 to 50 in 1993.  The quality of the exported rice is
# reportedly improving each year, with an increasingly smaller
# percentage of broken rice.  Currently, prices for Vietnamese rice
# are $50-$60 less per metric ton than Thai rice of the same quality.
#
#    TBQT concludes that to achieve success in rice export, the State
# needs to improve its management system, strengthen the Union of
# Grain Exporters, and give rice exporters regular guidance on
# domestic and international trade regulations in order to avoid the
# kind of losses experienced in the last quarter of 1993.
#
#    Government To Approve Foreign Construction of Infrastructure
# Projects - The Vietnamese Government will reportedly prepare
# legislation to implement a system whereby foreign companies will
# undertake the construction of infrastructural projects on a turnkey,
# or "build, operate, and transfer" (BOT) basis.  This "BOT-style"
# system involves entrusting all matters concerning infrastructural
# projects to foreign companies, from financing to construction and
# actual operation.  The government has "great expectations" for this
# system, since it will not have to provide financing and because
# foreign firms will contribute management and other knowhow to
# Vietnam.  China and Southeast Asian countries have successfully used
# the BOT system to build power-generating facilities and highways.
#
#    In the first half of March, the Vietnam State Committee for
# Cooperation and Investment (SCCI) plans to hold a "forum on BOT-
# style investment" in Hanoi for foreign financial organs and
# development companies.  At that time the SCCI will announce
# regulations concerning BOT bidding and contracting.
#
#    However, there have been "many problems" with the BOT system
# involving contracts let by government agencies and the companies
# signing them, as exemplified by the recent withdrawal of Japanese
# companies from an expressway construction project in Thailand.  In
# Vietnam's case, there probably will be difficulties over the long
# term in collecting fees from completed generating plants, highways,
# and bridges.  And even if some financing consortiums are formed,
# they will adopt a "cautious stance" regarding involvement in
# Vietnam.  It appears that initially, banks controlled by overseas
# Chinese and French banks will be the main participants in financing
# consortiums.  (Tokyo NIKKEI KINYU SHIMBUN 24 Feb 94 p 2)
#
#    Government To Develop 'Core' Groups of State Enterprises -
# According to an article in the 19 February NIHON KEIZAI SHIMBUN by
# Makoto Suzuki, the paper's Hanoi correspondent, the Vietnamese
# Government has decided to make the development of "core enterprise
# groups" from among major state enterprises a "pillar" of its
# economic restructuring program.  Although the government has been
# making efforts to nurture private companies as part of its economic
# reform measures, private companies still remain "weak."  Thus, the
# government's plan is to use selected "core" state enterprises as
# "locomotives" of economic growth.
#
#    As soon as possible, a list of candidate firms from among
# enterprises currently under the control of government agencies will
# be presented to Prime Minister Vo Van Khiet.  Then a "limited
# number" of core groups will be established--more will be designated
# later--and they will be removed from the control of ministries and
# agencies, "placed directly under the government," run
# "experimentally," and gradually will be expanded.
#
#    Suzuki writes that as explained by Le Xuan Trinh, minister and
# director of the Government Office, these core enterprises will be
# developed into "powerful" groups with capital levels of "several
# trillion" dong (several hundred million dollars).  Also, each group
# will have "several dozen umbrella companies" under it.  According to
# Trinh, companies under the Energy Ministry and the postal and
# communications authorities "will be the first" to be transferred.
#
#    Reorganizing state enterprises is one of the government's basic
# policy goals, Suzuki notes, along with privatization and
# reorganizing loss-making enterprises.  In this process, developing
# core enterprise groups appears to be a "precise" policy of
# selectively developing "superior" state enterprises.
#
#    Banking Association To Include Domestic, Foreign Banks - Vietnam
# will establish a Banking Association by mid-1994 that is expected to
# bring together various domestic financial institutions as well as
# foreign banks operating in Vietnam.  The government intends to use
# their views in modernizing Vietnam's financial system.
#
#    There are four types of financial institutions in Vietnam, in
# addition to Vietnam's State Bank--state-owned commercial banks,
# private joint-venture banks, credit cooperatives, and finance
# companies (nonbanks). There are "more than 20 large and medium-size"
# state-owned commercial banks and private joint-venture banks.  About
# 40 domestic financial organizations intend to join the association.
# As for foreign banks, there are more than 30 operating in Vietnam
# through branches, joint ventures, or resident offices.
#
#    Among Japanese banks, Tokyo and Sakura Banks, which already have
# resident offices in Ho Chi Minh City, are expected to join the new
# association.  Also, it is anticipated that American banks will
# quickly enter Vietnam now that the economic embargo has been lifted.
# However, since foreign banks are "uneasy" about doing business in
# Vietnam because of the country's undeveloped financial markets,
# Japanese and other foreign banks hope to use the Banking Association
# to propose ways the Vietnamese Government might regulate the
# industry.  (Tokyo NIKKEI KINYU SHIMBUN 22 Feb 94 p 2)
#
#    Finance Ministry Personnel To Study Japan's Securities Industry -
# In June, Nikko Securities, one of Japan's "big four" securities
# companies, will invite 15 employees of Vietnam's Finance Ministry to
# study Japan's stock exchange regulatory system.  Ten members of the
# group will be regular ministry employees and five are students that
# will be joining the ministry.  During their month-long stay, the
# group will visit the Tokyo Stock Exchange, the Ministry of Finance,
# securities firms, and listed companies to study market regulations,
# regulation of securities sales, and market settlement issues.
#
#    Vietnam is planning to establish a stock exchange in Ho Chi Minh
# City, but whether the exchange will actually be opened this year,
# given delays in preparing its regulatory systems and slowness in
# issuing stock of government-owned companies, has become a "delicate"
# issue.
#
#    Anticipating that American investment banks will begin operations
# in Vietnam with the lifting of economic sanctions, Japanese
# securities firms and banks "are quickly establishing close personal
# ties (jimmyaku) with the Vietnamese Government so as not to lag
# behind."  (Tokyo NIHON KEIZAI SHIMBUN 21 Feb 94 p 8)
#
#    Joint Venture With French, Chinese Firms To Produce Nylon Cords -
# The Hanoi Industrial Textile Factory, France's Rhone-Poulenc Chimie,
# and China's Heavenly Horse Tire Fabric Company have formed the Thang
# Long Nylon Company, a 20-year joint venture in Hanoi to manufacture
# nylon cords for bicycle and motor vehicle tires.  The new venture
# was licensed in mid-December 1993, with an investment capital of
# $4.76 million.  Prescribed capital is $3.33 million, of which the
# Vietnamese company is contributing 34 percent while the other two
# partners are contributing 33 percent each.  (Hanoi NHAN DAN 1 Jan 94
# p 6)
#
#    Jewelry Joint Venture Formed With Japanese Company - The
# Vietnamese Gemstone Company (Vinagemco) and Japan's Kotobuki
# Holdings Company Ltd. have formed Vijagem, a 30-year joint venture
# in Hanoi to process gems tones and to make and sell jewelry.  The
# new venture was licensed in October 1993 and is capitalized at $2
# million.  Prescribed capital is also $2 million, of which the
# Japanese company is contributing 70 percent.  (Hanoi QUAN DOI NHAN
# DAN 3 Jan 94 p 4)
#
#    Joint Venture With Philippine Firm To Build Commercial Complex -
# The Merchant Marine Center (under the Vietnam Maritime Department)
# and the Philippines' Imex Pan-Pacific have formed the Hanoi Marine
# Commercial Center, a 30-year joint venture in Hanoi to build a
# commercial complex--containing a hotel and offices--and to provide
# merchant marine services.  The new venture was licensed in late
# October 1993, with an investment capital of $12 million.  Prescribed
# capital is $6.02 million, of which the Philippine company is
# contributing 51 percent.  (Hanoi NHAN DAN 4 Jan 94 p 4)
#
#    Joint Venture With Singaporean Company To Provide Hotel Services
# - The Vietnam Tourism Company in Ho Chi Minh City and Singapore's
# Koh Brothers Building and Civil Engineering Contractor Pte., Ltd.
# have formed Vina Viet-Sinh Ltd., a 15-year joint venture in Ho Chi
# Minh City to provide hotel services.  The new venture was licensed
# in October 1993, with a listed investment capital of $3.2 million.
# Prescribed capital is $2.4 million, of which the Singaporean firm is
# contributing 70 percent.  (Hanoi NHAN DAN 3 Jan 94 p 2)
#
#    Joint Venture With Malaysian Firm To Produce Glass Containers -
# The Khanh Hoi Glass Factory in Ho Chi Minh City and Malaysia's
# Malaya Glass Berhad have formed Malaya-Vietnam Glass Ltd., a 30-year
# joint venture in Ho Chi Minh City to produce glass containers for
# domestic consumption and export.  The new venture was licensed in
# late October 1993, with an investment capital of $22 million.
# Prescribed capital is $15.47 million, of which the Malaysian firm is
# contributing 70 percent.  (Hanoi NHAN DAN 8 Jan 94 p 6)
#
#    Decrease in Coal Export Noted - Coal export in 1993 totaled
# nearly 1.25 million metric tons, about 350,000 metric tons less than
# in 1992.  Competition among various units brought down prices by 5
# to 7 percent compared with 1992.  Coal's export value has also
# decreased by nearly $20 million.  (Hanoi THOI BAO KINH TE VIETNAM
# 23-29 Dec 93 p 5)
#
#    Singapore's Liang Court Holdings To Invest in Apartment Complex -
# Peregrine Capital Vietnam Ltd. and Singapore's Liang Court Holdings
# plan to build a $30-million, 150-unit apartment complex in Ho Chi
# Minh City.  Liang Court owns 60 percent of the project and the
# Vietnamese firm the remainder.  (Singapore BUSINESS TIMES 21 Feb 94
# p 18) Bangkok Bureau
#
#    Hanoi Launches First Paging Service - Hanoi Post and
# Telecommunications recently launched its first paging service, with
# technical assistance from Hong Kong's ABC Communication (Holding)
# Ltd.  The service has numeric or alpha-numeric pagers capable of
# storing up to 98 messages and 280 characters and receiving messages
# in Chinese characters as well as in the Roman alphabet.  The Hanoi
# paging center has 170 subscribers and charges a monthly fee of $8.
# The subscription fee for Ho Chi Minh City is $10 a month.  (Hanoi
# VNA 0555 GMT 19 Feb 94) Bangkok Bureau
#
#    Hong Kong Firm To Invest in Da Lat Infrastructure - Hong Kong's
# Strategic Development International Corporation will invest in a
# $150-million project to improve Da Lat's infrastructure, including
# roads and power and water supplies.  (Hanoi VNA 0648 GMT 21 Feb 94)
# Bangkok Bureau
#
#    PetroVietnam To Increase Production - The Vietnam Oil and Gas
# Corporation, PetroVietnam, expects to produce 7.1 million tons of
# crude oil this year, up by 300,000 tons from the previous year.  The
# increase is attributed to an estimated 6.7 million-ton yield from
# the Bach Ho oil field and a 0.3 million-ton output from the Rong and
# Dai Hung fields.  (Hanoi Voice of Vietnam 1000 GMT 22 Feb 94)
# Bangkok Bureau
#
#    Government To Increase Cement Production - Six ministries and 21
# provinces are committed to increase cement production using vertical
# furnaces.  Nearly 35 feasibility studies to upgrade or build new
# furnaces at a total investment of $670,000 have been done.  Experts
# estimate that these vertical furnaces will produce 650,000 tons of
# cement this year and 2.5 million tons in 1996.  (Hanoi VNA 1444 GMT
# 19 Feb 94) Bangkok Bureau
#
#    Peanut Exports Put Vietnam Third Among Exporting Countries -
# Vietnam exported about 150,000 tons of peanuts last year, ranking
# third among peanut exporting countries.  This year Vietnam expects
# to produce 275,000 tons of peanuts, including 200,000 tons for
# export.  (Hanoi VNA 0611 GMT 1 Mar 94) Bangkok Bureau
#
#    First Phase of Hoa Binh Hydroelectric Plant Completed - A 670-ton
# rotor was recently installed at the Hoa Binh Hydroelectric Power
# Plant, marking the end of the first phase of the plant's
# construction, which has taken over 10 years.  The rotor will
# increase the plant's output to 1,920 mw, as planned.  (Hanoi Voice
# of Vietnam Network 1100 GMT 25 Feb 94) Bangkok Bureau
#
#    Rice Joint Venture Accord With Hong Kong Company Signed - Long
# An, Tien Giang, Dong Thap, and An Giang Provinces have recently
# signed a 50-year joint-venture agreement with a Hong Kong company to
# produce and process rice.  The $10-million project includes the
# planting of special rice varieties on 30,000 hectares in southern
# Vietnam, and the construction of a processing mill with an annual
# capacity of 90,000 tons.  (Hanoi Voice of Vietnam 1000 GMT 2 Mar 94)
# Bangkok Bureau
#
#    Construction of Sulfuric Acid Factory Reported - Construction of
# a sulfuric acid factory--a joint venture between  Indonesia's Unggul
# Indah Corporation (UIC) and Vietnam Company Ltd.--in Dong Nai
# Province has begun.  The $7.5-million, UIC-funded factory will have
# an annual capacity to produce 30,000 tons of dodecyl benzene
# sulfuric acid, the primary ingredient in soap powders and laundry
# detergents.  The factory will begin operating in September and will
# provide jobs for 100 workers.  (Hanoi VNA 1404 GMT 26 Feb 94)
# Bangkok Bureau
#
#    Vietnam Airlines Leases Two Airbus Jets From Air France - Vietnam
# Airlines will lease two Airbus A320 passenger jets from Air France
# to meet an expected 40-percent rise in passengers over the next few
# years.  The two jets will bring the total of Airbus and Boeing
# aircraft leased by the airline to seven.  Vietnam Airlines has been
# replacing its aging fleet of 20 Soviet-built planes with more modern
# jets.  (Hanoi Voice of Vietnam 1000 GMT 26 Feb 94) Bangkok Bureau
# EAG/9MAR94/ECONF/TECHTF/EAST ASIA GROUP JEG 10/0134Z MAR
#
#
#
# '''
#
#
import re
# filteredText2 = re.sub(r"[A-Z]?[a-z]+ [A-Z]?[a-z]+ \([A-Z][A-Z]\)", "ZAX",text)
# filteredText3 = re.sub(r"[A-Z]?[a-z]+[ -][A-Z]?[a-z]+ [A-Z][a-z]+ \([A-Z][A-Z][A-Z]\)", "ZAX",text)
# filteredText4 = re.sub(r"[A-Z]?[a-z]+ [A-Z]?[a-z]+ [A-Z][a-z]+ [A-Z][a-z]+ \([A-Z][A-Z][A-Z][A-Z]\)", "ZAX",text)
# filteredText3AND = re.sub(r"[A-Z]?[a-z]+\n? [A-Z]?[a-z]+\n? and\n? [A-Z]?[a-z]+\n? \([A-Z][A-Z][A-Z]\)", "ZAX",text)
# # print(filteredText2)
# # print(filteredText3)
# # print(filteredText4)
# # print(filteredText3AND)
#
# t = "Nippon Credit Bank (NCB)"
# filteredText3 = re.sub(r"[A-Z]?[a-z]+ [A-Z]?[a-z]+ [A-Z][a-z]+ \([A-Z][A-Z][A-Z]\)", "ZAX",t)
# print(filteredText3)
#
# t2 = "construct a local-area network (LAN) that will combine image "
# filteredText3 = re.sub(r"[A-Z]?[a-z]+[ -][A-Z]?[a-z]+ [A-Z]?[a-z]+ \([A-Z][A-Z][A-Z]\)", "ZAX",t2)
# print(filteredText3)
#
#
# test = "the Japan Broadcasting Corp. (NHK), Nippon Telegraph and Telephone (NTT),"
# filteredText3AND = re.sub(r"[A-Z]?[a-z]+\n? [A-Z]?[a-z]+\n? and\n? [A-Z]?[a-z]+\n? \([A-Z][A-Z][A-Z]\)", "ZAX",test)
# # print(filteredText3AND)
#
#
#
