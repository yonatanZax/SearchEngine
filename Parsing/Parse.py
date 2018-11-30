import re
from Parsing.IterativeParsing import IterativeTokenizer

class Parse:

    def __init__(self,config):
        self.tokenizer = IterativeTokenizer(config=config)


    def parseDoc(self, documentAsString):
        from Indexing.Document import Document

        docNo = 'doc null'
        cityAsArray = [""]
        try:
            topOfText1 = documentAsString[0:int(len(documentAsString)/10)]
            topOfText2 = documentAsString[0:int(len(documentAsString)/6)]
            docNo = re.findall(r'<DOCNO>(.*?)</DOCNO>', topOfText1)
            if len(docNo) > 0:
                docNo = docNo[0].strip(' ')
                # print("#"+docNo+"#")
            else: return None
            countryLine = re.findall(r"<F P=101>(.+?)</F>", topOfText2)
            cityLine = re.findall(r"<F P=104>(.+?)</F>", topOfText2)
            if len(cityLine) > 0:
                cityAsArray = re.findall(r"[a-zA-Z]+", cityLine[0].strip(' '))
                if cityAsArray[0].lower() in ['new','san','sao','la','tel','santa']:
                    cityAsArray = [str(cityAsArray[0]) + ' ' + str(cityAsArray[1])]
            if len(countryLine) > 0:
                country = countryLine[0].strip(' ')


            onlyText = documentAsString.split("<TEXT>")
            if len(onlyText) > 0:
                documentAsString = onlyText[1]
            else: return None
        except IndexError as e:
            print('DocNo: ',docNo)
            print('Error spliting docs in parse, e: ',e)
            # print("Error - Parse - parseText")
            return None

        termDictionary, docLength = self.tokenizer.getTermDicFromText(documentAsString)
        document =  Document(docNo, termDictionary, docLength, city = cityAsArray[0])
        return document




text = '''

<DOC>
<DOCNO>FT924-1183</DOCNO>
<PROFILE>_AN-CLTALABGFT</PROFILE>
<DATE>921219
</DATE>
<HEADLINE>
FT  19 DEC 92 / Jelly ball toys are banned
</HEADLINE>
<TEXT>
STOCKING-FILLER Christmas toys known as jelly balls were banned yesterday.
The brightly coloured golfball-sized toys are designed to be thrown at
walls, where they stick before slowly trickling downwards.
The government has served prohibition notices on 14 companies. Baroness
Denton, consumer affairs minister, said toddlers might mistake the jelly
balls for sweets.
Brand names covered are: Jelly Balls, Kung Fu Balls, Splat Balls, Splat
Eggs, Splat Tomatoes, Slime Balls, Sticky Balls, Tacky Wacky Wall Rollers,
Spike Balls, Sticky Flying Hammers, Hand Hammer Sticky Catchers, Sticky
Hand, Sticky Flicker and Sticky Troll.
</TEXT>
<PUB>The Financial Times
</PUB>
<PAGE>
London Page 5
</PAGE>


'''


text2 = '''

<DOC>
<DOCNO> LA111990-0063 </DOCNO>
<DOCID> 310433 </DOCID>
<DATE>
<P>
November 19, 1990, Monday, Home Edition 
</P>
</DATE>
<SECTION>
<P>
Sports; Part C; Page 3; Column 1; Sports Desk 
</P>
</SECTION>
<LENGTH>
<P>
722 words 
</P>
</LENGTH>
<HEADLINE>
<P>
ALLAN MALAMUD: NOTES ON A SCORECARD 
</P>
</HEADLINE>
<BYLINE>
<P>
By ALLAN MALAMUD 
</P>
</BYLINE>
<TEXT>
<P>
Maybe this was one game that should have ended in a tie. Neither UCLA nor USC 
deserved to lose. . . . 
</P>
<P>
I've seen the last 40 renewals of the cross-town rivalry and Saturday's was the 
best, minute-for-minute. . . . 
</P>
<P>
Overheard on the USC sidelines after Johnnie Morton caught the touchdown pass 
that put the Trojans ahead with 16 seconds remaining: "We scored too early." . 
. . 
</P>
<P>
Thumbs up to Jim Sprenger, Dave McCullough, Jay Stricherz, Chuck McFerrin, 
Nardy Samuels, David Becker and Rich Freitas. They're the officials who let the 
players do their thing. Not one big play was called back. No holding penalties 
were called. No penalties of any kind were called in the second or third 
quarters. . . . 
</P>
<P>
Postgame snapshots: Two wide receivers who caught 15 passes between them, USC's 
Gary Wellman and UCLA's Scott Miller, shaking hands, exchanging compliments, 
and wishing each other good luck at midfield. . . . Larry Smith interrupting 
his news conference to hug and kiss wife Cheryl. . . . USC players wearing 
ear-to-ear smiles nearly as big as their tiny Rose Bowl dressing room. . . . 
Terry Donahue patiently answering questions in the interview room and then 
granting every request for a one-on-one interview. . . . Tommy Maddox doing the 
same. . . . 
</P>
<P>
All Maddox needs to become a high first-round draft pick is three more years -- 
well, maybe two. . . . 
</P>
<P>
Todd Marinovich conducts the coolest, most proficient game-winning touchdown 
drives this side of Joe Montana. 
</P>
<P>
The biggest play that won't be remembered was USC fullback Raoul Spears 
apparently being stopped and then spinning off a tackler for three yards and a 
first down on fourth and one on the UCLA 24 in the fourth quarter. On the next 
play, Marinovich threw the first of his two touchdown passes to Morton to put 
the Trojans ahead, 38-35. . . . 
</P>
<P>
It was also Spears, a second-stringer, who made Smith's gamble look good when 
he dived for two yards and a first down on fourth and one on the USC 39 early 
in the third quarter. . . . 
</P>
<P>
Longest time between touchdowns in the fourth quarter was 6 minutes 39 seconds. 
. . . 
</P>
<P>
Only one field goal was attempted all day and Quin Rodriguez's three-pointer 
was the difference. . . . 
</P>
<P>
Another thing that made this game unusual -- neither coach was criticized. . . 
. 
</P>
<P>
Theme of Troy Week was "Another Trojan conquest. Ho hum." . . . 
</P>
<P>
The rematch next Nov. 23 in the Coliseum should be something. Of the 44 
starters Saturday, only 14 were seniors. . . . 
</P>
<P>
Won't those intellects in the California rooting section and Stanford band ever 
learn to stay off the field until the end of the game? . . . 
</P>
<P>
Most USC fans were disappointed that Notre Dame lost to Penn State. They wanted 
the Trojans to have an opportunity to knock off the top-rated team Saturday in 
the Coliseum. . . . 
</P>
<P>
I doubt that there will be a quarterback controversy at USC this week. 
</P>
<P>
If the Orange Bowl had shown some patience, it could have had hometown Miami 
vs. Colorado with the national championship most likely at stake. Actually, 
Notre Dame still should be rated ahead of Miami. Notre Dame is 8-2, Miami 7-2, 
and the Irish beat the Hurricanes. . . . 
</P>
<P>
The Sugar Bowl looks real smart, too, for inviting Virginia, which lost to 
Maryland and probably won't have injured quarterback Shawn Moore in the lineup 
New Year's Day. . . . 
</P>
<P>
Washington has UCLA to blame for not ending the regular season as No. 1. . . . 
</P>
<P>
An asterisk should be put beside the 11 touchdown passes thrown by David 
Klingler Saturday in the Astrodome. After all, Houston was playing Eastern 
Washington. . . . 
</P>
<P>
In coaching Cal State Long Beach to a 6-5 season, George Allen proved that he 
hasn't lost his winning touch. . . . 
</P>
<P>
This time, Boston College would have needed five Hail Mary passes to beat 
Miami. . . . 
</P>
<P>
Howard Schnellenberger, who is bringing Louisville to the Fiesta Bowl, may stay 
in Tempe, Ariz., to replace Larry Marmie as coach of Arizona State. . . . 
Nothing like the Rams' defense to bring out the best in Troy Aikman. . . . 
</P>
<P>
Pity Orange County, home of the Rams and Cal State Fullerton. . . . 
</P>
<P>
The well-balanced Buffalo Bills won't lose by 45 points if they play in the 
Super Bowl. . . . 
</P>
<P>
How about those streaking Indianapolis Colts. . . . 
</P>
<P>
Circle Sept. 7 on your 1991 calendar. Tommy Maddox and UCLA vs. Ty Detmer and 
BYU at the Rose Bowl. 
</P>
</TEXT>
<GRAPHIC>
<P>
Photo, Todd Marinovich ; Photo, Tommy Maddox ; Photo, Troy Aikman 
</P>
</GRAPHIC>
<TYPE>
<P>
Column 
</P>
</TYPE>
</DOC>


'''
from Configuration import ConfigClass
p = Parse(ConfigClass())
p.parseDoc(text2)



