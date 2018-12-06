import re
from Parsing.IterativeParsing import IterativeTokenizer

class Parse:

    def __init__(self,config):
        self.tokenizer = IterativeTokenizer(config=config)

        self.keepGoingCityDic = {'new','san','sao','la','tel','santa','hong','xian','cape','rio','buenos','panama','mexico','guatemala','abu'}

        self.avoidCities = {'bartaman','dokumentation','nezavisimaya','calcutta','the','air'}


    def parseDoc(self, documentAsString):
        from Indexing.Document import Document

        docNo = 'doc null'
        city = ''
        cityLine = ''
        language = ''
        languageLine = ''
        try:
            docNo = documentAsString[documentAsString.find('<DOCNO>') + len('<DOCNO>'):documentAsString.rfind('</DOCNO>')]
            if len(docNo) > 2:
                docNo = docNo.strip(' ')
                # print("#"+docNo+"#")
            else: return None
            textLabelIndex = documentAsString.find('<TEXT>')
            onlyText = documentAsString[textLabelIndex + len('<TEXT>'):documentAsString.rfind('</TEXT>')]
            findTextSquared = onlyText.find('[Text]')
            if findTextSquared > 0:
                onlyText = onlyText[findTextSquared + len('[Text]'):]
                textLabelIndex = findTextSquared
            if len(onlyText) < 15:
                return None

            # countryLine = documentAsString[documentAsString.find('<F P=101>') + len('<F P=101>'):documentAsString.find('</F>')]
            # countryLine = re.findall(r"<F [Pp]=101>(.+?)</F>", documentAsString)
            cityStart = documentAsString.find('<F P=104>')
            if cityStart > 0:
                cityEnd = documentAsString[cityStart:].find('</F>')
                cityLine = documentAsString[cityStart + len('<F P=104>'): cityStart + cityEnd]
            # cityLine = documentAsString[documentAsString.find('<F P=104>') + len('<F P=104>'):documentAsString.find('</F>')]
            # cityLine = re.findall(r"<F [Pp]=104>(^((?!</F>).)*)", documentAsString)
            # languageLine = documentAsString[documentAsString.find('<F P=105>') + len('<F P=105>'):documentAsString.find('</F>')]
            languageStart = documentAsString.find('<F P=105>')
            if languageStart > 0:
                languageEnd = documentAsString[languageStart:].find('</F>')
                languageLine = documentAsString[languageStart + len('<F P=105>'): languageStart + languageEnd]


            if len(cityLine) > 1 :
                splittedCity =  cityLine.replace('\n',' ').strip(' ').split(' ')
                city = splittedCity[0]
                if city.lower() in self.keepGoingCityDic and len(splittedCity) > 1:
                    city = city + ' ' + splittedCity[1].strip(' ')
                    if len(splittedCity) > 2 and splittedCity[1].lower() in ['de']:
                        city = city + ' ' + splittedCity[2].strip(' ')

                if city.isalpha() and city.lower() not in self.avoidCities:
                    onlyText = onlyText.replace(city, 'ZAXROY')
                else:
                    city = ''
            # if len(countryLine) > 0:
            #     country = countryLine[0].strip(' ')

            if len(languageLine) > 0 :
                languageLine = languageLine.replace('\n',' ').strip(' ').split(' ')[0]
                if len(languageLine) > 1 and languageLine[0].isupper():
                    tempLanguage = languageLine[0]
                    for l in languageLine[1:]:
                        if l.isalpha():
                            tempLanguage += l
                        else: break

                    if len(tempLanguage) > 2:
                        language = languageLine



        except Exception as e:
            print('DocNo: ',docNo)
            print('Error spliting docs in parse, e: ',e)
            # print("Error - Parse - parseText")
            return None


        termDictionary, docLength = self.tokenizer.getTermDicFromText(onlyText)
        document =  Document(docNo, termDictionary, docLength, city = city,language=language)
        return document


#
# from Configuration import ConfigClass
# configClass = ConfigClass()
# p = Parse(configClass)

text = '''

[Text] 
<H3>  RAU Corporation RAU Press Information Agency Institute of 
Mass Political Movements </H3>
  Ecological Organizations on the Territory of the Former 
USSR. 
Directory 
  RAU Press Publishing House Moscow 1992 BBK N-53 
  Compiling authors: Ye. N. Kofanova and N. I. Krotov. 
  Author of the article and scientific editor: A. B. Shubin. 
  Scientific editor of "Kazakhstan" chapter: A. M. Dzhunusov. 
  Editor and compiler of the index: N. N. Silin. 
  Taking part in the work were: A. V. Zudin, A. Ye. 
Kvatkovskiy, A. V. Koroleva, S. Yu. Kutukov, I. A. Nevskaya, G. 
V. Prokofyeva, and V. Yu. Khabidulin. 
  Ecological Organizations on the Territory of the Former 
USSR. 
Directory Moscow: RAU Press Publishing House, 1992. ISBN 
5-86014-052-5 
  This directory contains the most complete information on 818 
ecological organizations on the territory of the former USSR. 
  The publication is intended primarily for scientific 
workers, 
graduate students, teachers, students, and organizers of nature 
protection work, as well as all those who are interested in the 
contemporary ecology movement. 
  P 0803010200/594(03) - 92 Without declaration BBK N-53 
  The computer original was prepared by N. N. Silin using the 
"Russkoye slovo" (c) SP Para Graf package, which includes the 
word processing program MicroSoft Word 5.0 (c). 
  The format is 84 x 108 1/8. Book and journal paper. Offset 
print. 
  3,000 copies printed. Book price is by contract. Printed at 
the VAAP [All-Union Agency for Authors' Rights] Printing Plant. 
  ISBN 5-86014-052-5 
  Y. N. Kofanova, N. I. Krotov. Compilation, 
commentaries, reference articles, 1992. 
  A. M. Dzhunusov, Ye. N. Kofanova, N. I. Krotov. 
Compilation, commentaries, reference articles, the chapter 
"Kazakhstan," 1992. 
  A. V. Shubin. Introductory article, 1992. 
<H5>  FOREWORD </H5>
  To the reader! 
  This directory includes information on 818 ecological 
organizations operating on the territory of the former USSR 
(there are explanatory articles on 551 of them and another 267 
are mentioned). The states which were part of the Union still 
have a great deal in common, among other things, a grave 
ecological situation. And there are common patterns which can be 
traced in the history of the "Green" organizations here. 
  The stages of the development of the ecology movement and 
the 
classification of Green organizations by several criteria are 
presented in an article by Aleksandr Shubin, historian and 
cochairman of the Russian Greens Party. This article is placed 
at the beginning of the directory. 
  Data on organizations are combined into two chapters: 
  1. Interrepublic organizations (operating on the territory 
of 
all or several former Union republics); 
  2. Republic and local organizations. 
  Within the chapters devoted to a particular republic they 
are 
placed in the following order: 

  -  republic organizations, 
  -  the capital's organizations 
  -  organizations in oblasts, krays, and republics which are part 
of the Federation (oblast organizations, organizations of the 
oblast center, and organizations of populated points). 

    The directory has alphabetical indexes of names, 
nongovernmental organizations mentioned (the pages where the 
explanatory article is found are set off in italics 
[not given in English translation]), mass information media, and 
populated points. 
  The data on organizations are presented in items of 
information which usually tell the organization's size, age, and 
social make-up, the history of its creation and activity, the 
sources of financing, mass information media (set off in 
italics [given in all capital letters in English 
translation]), and other things. Then the addresses and contact 
telephone numbers and a short bibliography (set off in 
italics [merely listed in English translation]) are 
indicated. 
  The following were the primary materials used in working on 
the directory: 
  USSR Goskomprirody [USSR State Committee for Protection of 
Nature and Natural Resources]; 
  archives of the RAU Press Agency Institute of Mass 
Political Movements; 
  Galkina, L., "Zelenyye v SSSR. Spravochnik" ["Greens in 
the USSR. Directory"], Moscow, 1991; 
  "Zelenyye v SSSR. Krupneyshiye organizatsii i dvizheniya: 
kratkiy spavochnik" ["Greens in the USSR. Large Organizations 
and Movements: Short Directory"], Lika Information Research 
Center, Moscow, 1990; 
  catalog prepared by USSR Goskomprirody; 
  personal archives of A. V. Shubin; 
  personal archives of A. M. Dzhunusov; 
  "Rossiya: partii, assotsiatsii, soyuzy, kluby. 
Spravochnik" [Russia: Parties, Associations, Alliances, and 
Clubs. Directory"], Moscow, RAU PRESS, 1991, volume 1, parts 1-2; 
  "Spravochnik politicheskikh i obshchestvenyykh 
organizatsiy Latvii s kommentariyami" ["Directory of Political 
and Public Organizations of Latvia with Commentaries"], compiled 
by I. Kudryavtsev, Moscow, Moscow Public Bureau of Information 
Exchange, 1990; 
  "Spravochnik `Ekologicheskiye organizatsii.' 90 gorodov" 
["`Ecology Organizations' Directory. 90 Cities"], 
INFORMATSIONNYY BYULLETEN SMOT, No 75, January 1992; 
  "Samodeyatelnyye obshchestvennyye organizatsii (SOO) 
Kazakhskoy SSR (spravochnik)" ["Non-Professional Public 
Organizations (NPO) of the Kazakh SSR (Directory)"], Almaty, 
1990. 
  Newspapers of various political orientations and various 
regions (starting in 1987) were also studied. 
  The authors thank everyone who submitted information on the 
Greens organizations to us. 
  We will be grateful for all suggestions, comments, 
programs and by-laws of ecological organizations, information on 
their activities, excerpts from newspapers, "samizdat" material, 
and so on sent to the following address: 103104, Moscow, 
Tverskoy bulvar, 7/2, Institut massovykh politicheskikh 
dvizheniy (RAU-Korporatsiya) [Institute of Mass Political 
Movements (RAU Corporation)], telephone 202-05-85, Nikolay 
Ivanovich Krotov and Yelena Nikolayevna Kofanova. 
  At the present time work is being completed in our institute 
on a computer version of the directory which will also include 
materials accumulated in the institute's archives which were not 
part of this publication. A second edition (revised and 
enlarged) of this directory is being prepared. 
<H5>  BASIC ABBREVIATIONS USED </H5>
  AN--Academy of Sciences AO--autonomous oblast 
APK--agroindustrial complex APN--Novosti Press Agency 
AST--atomic heat plant ATS--telephone exchange AES--atomic power 
plant BVK--protein-vitamin concentrates VASKhNIL--All-Union 
Academy of Agricultural Sciences imeni V. I. Lenin VS--Supreme 
Soviet g.--year g.--city GK--city committee GU--state university 
GES--hydroelectric power plant d.--building DK--House of Culture 
DOSAAF--Voluntary Society for Assistance to the Army, Air Force, 
and Navy DS--Democratic Union IGP--Institute of the State and 
Law IMPD--Institute of Mass Political Movements 
ITR--engineering-technical worker kv.--apartment KGB--State 
Security Committee kom.--room korp.--block KPK--party control 
committee KPSS--Communist Party of the Soviet Union M.--Moscow 
MID--Ministry of Foreign Affairs mkrn.--microrayon MO--Ministry 
of Defense MP--small enterprise NII--scientific research 
institute NITs--scientific research center 
<H3>  A. SHUBIN: THE ECOLOGY MOVEMENT IN THE USSR AND THE 
COUNTRIES WHICH EMERGED FROM IT </H3>
  The ecology movement is a diverse and in many respects 
unique 
phenomenon which appeared in our countries in the second half of 
the 20th century. The lack of such a movement in the 
prerevolutionary history of Russia caused some serious 
differences between the domestic ecology movement and other 
social trends. Ecologists did not have a domestic tradition to 
which they could turn. The result of that was the initially slow 
rate of evolution of the ecology movement, the importance of 
Western experience for it, the lack of an independent positive 
ideal for a long time, and other things. 
  Just as in other industrial countries, the appearance of the 
ecology movement was caused by the crisis of the industrial 
system in a particular stage of its development. The attempt to 
implement the scientific-technical revolution by preserving the 
industrial structures of vertical management of production 
aggravated the ecological crisis, while the parallel development 
of social self-awareness and ordinary literacy in the natural 
sciences sphere made people willing to oppose the process of the 
destruction of the environment and man. 
  Industrial man, alienated from decision making, from 
information, and from nature itself, crowded in cities, and 
oppressed at the factory and at home, began to understand his 
position. He had become so complex that he could no longer 
fulfill his role of a specialized cog in the industrial machine 
on which industrial civilization is based. 
  Despite the universality of the causes of the appearance of 
the ecology movement in various countries of the world, its 
genesis in the USSR had its own particular features. Above all 
it occurred under conditions of a supermonopolized 
state-industrial system. The high degree of monopolization in 
all spheres of life determined the system's destructiveness in 
relation to nature and man. Police and political control over 
any kind of manifestation of public activism made it more 
difficult for the reaction to this destruction to develop. 
  At the same time, however, society's lack of influential 
social subjects independent of the party and state made its 
paternalistic function develop. The state attempted to protect 
its subjects from its own parts. As soon as the ecological 
problem began to be recognized by the official community (and 
that happened during the "thaw" of 1953-1964), "the party and 
the state" took some steps to increase control over certain 
violations of ecological standards (above all by private 
citizens). 
  Social activism which was directed against these violations 
but did not affect political aspects was also legalized. 
  Thus began the first INDUSTRIALIZED period of the 
ecology movement (approximately 1958-1982). During this period 
the movement was typically built into the structures of official 
public organizations like the All-Union Nature Protection 
Society (VOOP). But within the framework of these structures 
informal associations arose--Nature Protection Squads (DOP's). 
The first DOP's were formed in the early 1960s and in 1968-1972 
became a system which encompassed the entire country. This 
system was focused above all on the struggle against poaching 
and cautious, only within the framework of the law, restraint of 
the most flagrant manifestations of industrial expansion. 
  After the "thaw" was curtailed, the system of the nature 
protection movement became a refuge for the liberal-minded 
intelligentsia, above all youth, who in the DOP's and inspection 
offices of VOOP could find an opportunity to serve society 
outside state structures in relatively autonomous and not very 
bureaucratized groups, an opportunity which was very scarce at 
that time. Participation in DOP's and VOOP inspection offices by 
people with "unorthodox" views threatened the existence of these 
very organizations. This promoted the formulation of a unique 
ethical principle which excluded the political orientation of a 
nature protection group. "Our business is ecology." 
  The romance of the DOP's contrasted with the "orderliness" 
of 
"developed socialism" and provided an opportunity to temporarily 
escape the all-encompassing industrial system. At the same time, 
however, the state was able to channel this social activism in 
the direction it needed. Nevertheless, accumulated experience 
with the institutionalized nature protection movement allowed 
people to gradually come to the conclusion that large-scale 
ecological problems could not be solved within the framework of 
the official structures. 
  The rapid buildup of ecological problems in the second half 
of the 1970s and early 1980s also promoted this awareness. The 
attempt to deal with this wave of violations, which were the 
result of objective economic and social causes and the "sins of 
the system," led to an increasing number of confrontations 
between the nature protection movement and the system's 
influential links--beginning with bureaucratic poachers and 
ending with the ministries which joined the initiative to 
"reverse the flow of the northern rivers." Ecologists were made 
to understand that they were interfering in what was not their 
business. The crisis of the movement brought a new stage of the 
movement into being--the PETITION stage 
(approximately 1982-1989). 
  This stage was characterized by the greater independence and 
larger scale of the ecology movement. It still remained a nature 
protection movement and appealed primarily to the authorities, 
intending to change their particular decisions and at the same 
time not change the system. But the ecology movements and groups 
independently selected the object of the attack without taking 
into account the elite's position and resorted to mass 
mobilization means--they called on the population and proposed 
that they support the appeal to the authorities. 
  During this period the movement acquired a primarily 
negativistic orientation. Ecologists spoke out against the most 
destructive installations and projects, hoping to restrain 
industrial expansion and localize its harmful consequences. Such 
a strategy in the ecological organizations united people of the 
most diverse views, from conservative-ethnocratic to anarchist. 
  The first mass campaign of this stage ended in success. In 
1986 the "river reversal" project, which had originally been 
supported by the country's highest leadership (including the 
"architects of perestroyka"), was canceled, although the former 
system of water management was preserved and the problems of 
water supply which "reversing the rivers" was supposed to 
resolve continued to worsen. 
  The position of the country's leaders in relation to the 
growing ecology movement in this stage was relatively favorable. 
The protest of the citizens driven to desperation was directed 
against the local bureaucratic leadership and fit the strategy 
of "pressure from below" which was supposed to make the local 
clans more conciliatory toward the "perestroyka leadership." The 
"fathers of perestroyka" appealed to the public; they needed a 
powerful public movement, but one which would not encroach upon 
the foundations of the system, that is on the highest 
leadership's authority. 
  The original "apolitical nature" of the movement and the 
"patriotic" conservatism (which later took on an anticommunist 
slant) of many of its leaders from the writers' milieu, the 
concentration on particular objects, and the lack of a 
constructive program seemed to guarantee that the process was 
under control. 
  However, it became explosive. The years 1987-1989 were the 
most productive from the standpoint of the number of movements 
which arose and the scale of demonstrations. The need to 
coordinate efforts in the petition and rally campaigns brought 
broad associations of ecological organizations and movements to 
life. In 1987-1988 the Social-Ecological Alliance (SoES) 
emerged. In 1989 the even broader Greens Movement emerged. About 
a million people participated in the campaign against the 
construction of the Volga-Chogray Canal. 
  The successes of the ecological protest directed toward the 
elite were marked. Dozens of harmful enterprises were shut down 
and projects for reversing water resources and power engineering 
giants (the Katun GES, for example) were buried. But given the 
preservation of the former economic system, this promoted 
greater paralysis of the economy, which in itself was caused by 
other things. 
  These processes promoted greater opposition by the regime to 
the ecology movement. This could not fail to cause the 
politicization of the ecological masses, and that was extremely 
dangerous to the CPSU, which was losing equilibrium. The 
continued concessions threatened the superindustrial economic 
system with permanent paralysis. At the same time, however, the 
ecological crisis continued to expand despite the localized 
successes of the Greens, since it was caused by deeper reasons 
than ill will or the stupidity of particular functionaries. 
  This stalemate meant a crisis not only of government policy 
in the field of ecology, but also a crisis of the ecology 
movement itself. The negativism of its demands during this 
period was unpromising--the problems built up faster than 
enterprises could be closed. But even the closing of enterprises 
did not yet resolve the problems. The ecology movement needed a 
constructive alternative and a positive ideal which could 
suggest a solution to the problem in principle. The need for 
this alternative program was also dictated by criticism of the 
ecology movement for its negativism. 
  Naturally, from the very start the ecology movements had 
formulated alternative programs capable of offering solutions to 
local ecological crises. But these alternatives were primarily 
technical. Their great complexity as compared to simple but 
ecologically harmful projects and decisions of state organs and 
the requirement of additional expenditures prevented the 
implementation of the ecological projects. 
  The joint struggle against these phenomena and the 
accumulated experience and information already in this period 
promoted specialization of the movements and formulation of 
comprehensive alternative technical projects (projects of the 
six sections of VOOP, and the power engineering project of 
Novosibirsk "Pamyat"). But all these projects also remained 
unrealized when they ran up against the sociopolitical 
structures of industrial-bureaucratic society. 
  The de-ideologization of the ecology movement more and more 
became an anachronism. In 1989 it provoked more and more serious 
conflicts. The acceptance of Novosibirsk "Pamyat" into SoES 
caused a multitude of protests by its members despite the lack 
of "ecological" claims against this organization. The attempt to 
reconcile the entire political spectrum from "patriots" to 
anarchists within the framework of the ecology movement proved 
increasingly hopeless. A new stage of the ecology movement began. 
  This stage can be called POPULIST (1989-1991). Its 
first symptoms were revealed during the 1989 election campaign 
when the ecology movement supported candidates who advanced 
ecological slogans. 
  The politicization of the ecology movement and the move by 
most ecological organizations to open opposition to the CPSU by 
1990 required the promotion of a political idea which would not 
split the unity of the activists who were assembled in them. 
This idea was found most quickly in the "Union republics." Here 
the idea of protecting the environment and the cultural legacy 
was quickly combined with the idea of national resurrection and 
then, independence. The accelerated onset of the populist stage 
in republics striving for independence (the Baltic republics, 
Georgia, and in part, Armenia) starting in 1988 accounted for 
this. A coincidence of factors of the petition and populist 
periods as well as the geographic compactness of the territory 
resulted in a sharp increase in the size of the ecology 
movements in these republics and their rapid integration into 
unified systems, and later the recognition of their independent 
social interests. 
  Such processes also occurred in the Ukraine, where they 
initially were not so clearly expressed. But even here the 
Chernobyl Catastrophe stimulated an upsurge and rapid 
politicization of the ecology movement. 
  But in Russia the national factor, which promoted the 
upsurge 
of the ecology movement in 1982-1986, did not play a significant 
role in most organizations after this. For various reasons the 
mass consciousness of the politically active strata of the 
population rejected chauvinist and near-chauvinist ideas. The 
"guilt complex" of a large people reinforced by most of the 
intelligentsia made the abstract-democratic idea foremost. 
  A large part of the ecology movement accepted this idea 
after 
the general democratic political movement moved to open 
opposition to the regime. The relatively slow formation of the 
ecology movement's sociopolitical posture allowed general 
democratic groups to take over as leaders of the ecologists and 
integrate the ecologist activists into their own make-up. 
  The idea that Western forms of civilization would provide 
full salvation, which dominated in the consciousness of the 
socially active population, infatuated the ecology movement too 
during this period. The example of the Western countries which 
had "dealt with" ecological problems "in their own homes" seemed 
convincing proof of the ecological effectiveness of private 
property and parliamentary democracy. 
  The concern of the leaders of "Democratic Russia" about 
expanding the electoral base promoted the inclusion of 
abstractly formulated ecological demands and promises to help 
shut down the most dangerous installations in election programs 
of the "democratic" candidates. As a result most ecology 
movements supported the "Democratic Russia" candidates in 
elections and identified hopes for solving ecological problems 
with their victory and the defeat of the CPSU. 
  Only a minority of ecology groups abstained in 1990 from 
supporting the election campaign of the "democrats," but for 
various reasons. A certain number of the groups were inclined to 
support the "patriots." Also preserved was the fundamentally 
apolitical tendency, which during this period largely coincided 
with the "democratic" orientation: politics for politicians and 
ecology for ecologists. 
  But deep within the populist ecological movement with its 
orientation to support "prestigious political leaders" new 
trends were maturing, trends which were an alternative to 
populism and inclined to formulate an independent sociopolitical 
posture, an alternative both to the Western and to the 
communist-"patriotic" orientation. This relatively new 
phenomenon in the ecology movement was related to the movement 
to create a Greens party. 
  The appearance of groups which warned that hopes placed on 
liberals who had come out of the CPSU were false and which 
proposed a philosophy of seeking an alternative to the 
contemporary industrial society presaged a new crisis in the 
ecology movement. This crisis did not delay in bursting out 
after the "democrats" came to power in several cities and on the 
parliamentary level in Russia. The mass move of the nomenklatura 
to democratic banners and the "decommunization" of the CPSU put 
the question of changing to freer forms of the market and 
Western political forms on the agenda. The "democrats" came to 
power and had to begin paying debts, including ecological debts. 
  But the ecologists suddenly encountered processes which were 
directly opposite their expectations. In 1990-1991 the 
"democratic" administrations fundamentally revised their 
attitude toward ecological problems. One of the clearest 
examples was the refusal of the Moscow leadership to freeze 
construction of the Northern TETs [Central Heat and Power 
Plant]. The economic troubles which had broken out during this 
period made it possible to set a new theoretical base under this 
policy. The mass information media tried to convince the 
population that ecological problems should be solved after 
economic ones. 
  This same idea was the basis of the "500 days" program 
supported by the majority of the democratic camp. A large number 
of the newly elected deputies set former ecological demands 
aside. The Western orientation of foreign policy and economic 
ties more and more clearly marked the prospects for turning the 
country into an importer of industrial and radioactive wastes. 
The new economic relations did not lessen but on the contrary 
intensified the plundering of natural resources and violation of 
ecological standards. 
  The rapid change in the position of the "democratic" leaders 
on the question of ecology had a demoralizing effect on the 
ecology movement. Some of the movement's activists convinced 
themselves that the arguments of the opponents of ecological 
priorities were right. Without an independent constructive 
program, they continued to follow former political leaders. Some 
ecologists were profoundly disappointed in the results of their 
social activity and drew the conclusion that it was hopeless to 
oppose industrial expansion. Some were poorly informed of the 
changes which had occurred and continued to trust in "victorious 
democracy." 
  All these factors caused a marked decline in the ecology 
movement, the collapse of many organizations, and a decrease in 
the numbers of members remaining. 
  At the same time, however, the unfolding of ecological 
disaster together with the "democratic" camp's more and more 
obvious responsibility for it helped gradually increase the 
influence in the ecology movement of organizations oriented 
toward an alternative social program. Theories of anarchism 
began to acquire a great deal of influence in the ecological 
milieu (the active participation of anarchists in ecological 
work promoted this). 
  But the emergence of an alternative movement in the populist 
period was painful, running up against both the old traditions 
formed in the ecology movement and "growing pains." 
  The movement in support of creating a Greens Party emerged 
in 
December 1988 (it had existed under this name since 1989), but 
the party itself was proclaimed only in March 1990. The 
development of the party in 1990-1991 was accompanied by splits, 
the collapse and emergence of organizations, and the lack of 
workable interregional structures. Most ecology activists 
shunned the party Greens and their ideology, suspecting the 
"alternative advocates" of a desire to subordinate the movement 
to themselves on the one hand and to split the "democratic camp" 
on the other. 
  At the same time, however, the search for an alternative 
ideology was fraught with internal clashes related to the 
ideological differences of the authors of the different theories 
of ecological policy. 
  The situation changed in 1992, which signaled a new period 
in 
the development of the ecology movement. This period may be 
called the ALTERNATIVE. The reforms of 1992 and the 
absence of the "eternal culprit" in the form of the CPSU finally 
helped overcome the "political inferiority complex." The 
conference of ecological organizations in St. Petersburg 
dedicated to the intergovernment conference on the environment 
and development showed the ability of the most diverse ecology 
movements, both party and nonparty movements, to form an 
independent public posture. 
  Those groups which survived the crisis of 1991 acquired 
experience in public activity and formulation of constructive 
programs. Despite all the disagreements, an understanding became 
established that local problems are subordinate to global ones 
and comprehensive reforms whose principles are based on 
ecological priorities must be carried out. 
  Most of the groups which survived until 1992 also found 
their 
own "ecological niche" in society and a commercial and political 
base. All this created the prerequisites for a new upsurge in 
the ecology movement in 1992. Although this upsurge does not 
promise such quantitative growth in ecology movements as in 
1988-1989, the influence of the Greens on social processes in 
1992-1993 may prove to be more substantial than before. 
  Despite these new phenomena in the milieu of the ecology 
movement, the scope of change must not be exaggerated. 
Development is occurring unevenly. 
  The history of the development of the ecology movement 
determined the extreme diversity of its forms. In order to 
simplify the orientation in its structure we will propose 
certain principles of classification of ecological organizations. 
  Ecological organizations may be classified based on 
different 
features. Above all these are: geography of activity, number of 
members, link with governmental organizations, work areas, 
organizational structure and self-identification, work areas 
[sic], methods of work, and ideology. 
  The geographic distribution of ecological organizations is 
uneven. Concentration of ecology groups in zones with bad 
ecological situations is natural. But for ecological 
organizations to appear, an alarming ecological situation is not 
yet sufficient (strictly speaking, even the controversial Soviet 
ecological standards are violated practically everywhere). A 
certain level of political sophistication and an absence of 
authorities who destroy the organization of opposition are 
needed. 
  As a result the largest number of ecology movements and most 
widely-branching systems took shape in the Baltic republics, 
Ukraine, Armenia, Georgia, a number of oblasts of Russia 
(Chelyabinsk, Tomsk, and Nezhegorodskiy, for example), and some 
metropolitan areas (St. Petersburg, Moscow, Nizhniy Novgorod, 
Novosibirsk, and others). Small ecology groups exist in each 
oblast, but the degree of their influence and activism is 
different. The "ecology map" looked different in different 
periods. 
  By geographic range of activity, organizations may be 
divided 
into localized ones (tied to a particular naturally occurring or 
industrial object whose significance does not require the 
cooperation of ecology movements on the scale of the populated 
point), territorial ones (rural, rayon, city, oblast, regional, 
interregional, republic, all-Union, and international), and 
specialized ones. Specialization is linked to the struggle 
against a common enemy, a common ideology, or party affiliation. 
  The number of organizations which exist in a region may 
reflect not only the strength but also the weakness of a 
movement and its fragmentation. The formal size of a movement is 
also a disputable factor for evaluating the scale of the 
movement (it depends on the structure of the organization and 
frequently does not promote effective activity). By size 
organizations may be divided into microgroups (a few people), 
small (up to 30 people), medium-sized (up to 100 people), large 
(up to 1,000 people), and mass organizations. Despite the 
arbitrary nature of this gradation, the formal nature of size in 
the ecology movement and the large gap in the total numbers and 
the real aktiv must also be taken into account. 
  An organization's impact cannot always be determined by 
participation in organs of power either (many organizations have 
deliberately declined to nominate their candidates in 
elections). It is also risky to judge an organization's might by 
its financial resources--a great deal of capital may attest to 
the organization's dependence on industrial "sponsors." 
  Various approaches to the problem of financing an 
organization sometimes cause friction among different 
organizations. Usually ecology organizations treat the very idea 
of commercial support of ecological activity positively, but 
they are very scrupulous on the question of links between this 
financing and production facilities which harm the environment 
and man. The popularity in the ecological milieu of the idea of 
creating their own ecologically harmless production facilities 
and even whole settlements is also tied to this. Organizations 
dependent on state-economic organs usually arouse suspicion in 
the ecological milieu too. 
  An organization's effectiveness is determined above all by 
performance of those tasks which it sets for itself. In the 
ecology movement "small causes" and the formulation of global 
social projects are equally valuable from the standpoint of 
internal division of labor in the milieu of ecology activists. 
While in the first stages the greatest respect in the ecology 
movement went to organizations with large numbers of members 
which were able to shut down enterprises, later the "weight" of 
politically influential organizations grew. After the size of 
the ecology movement declined, the activism of members and their 
organizational and propagandist talents became especially 
important. 
  An organization's work areas depend on the region's problems 
and the ideology of the group's leaders, and the presence in 
that group of specialists on the particular problem. Among the 
work areas typical of the ecology movement we should single out 
the struggle to shut down harmful production facilities and to 
participate in cleaning up the consequences of environmental 
pollution, expert research work and monitoring of the state of 
the environment, protection of the cultural legacy and the 
restoration or support of the existence of ecological and 
cultural monuments, theoretical work, political work, and 
participation in the work of organs of power. 
  The various work areas also presuppose various methods: 
voluntary ecology work days, expert studies, street parades, 
agitation in the mass information media, petition campaigns, 
production of publications and leaflets, debates, seminars, and 
conferences, picketing of installations, and even "ecological 
terrorism," that is to say, violent actions against destroyers 
of the environment. Naturally the last method does not enjoy 
great popularity, although it has certain admirers, in the 
Rainbow Keepers organization for example. 
  Some organizations specialize in a small set of methods, but 
most prefer to vary them broadly. Typical of the ecology 
movement are two directly opposite trends of development--from 
the lack of specialization and work in all areas to 
concentration of efforts on a narrow group of problems, and the 
opposite--from specialization to global approaches to ecological 
problems. 
  Naturally the specialization and globalism of the later 
period for the most part differs qualitatively from similar 
phenomena of earlier origin. And specialized and "universal" 
groups which have gone through a long evolution are usually 
distinguished by much greater constructiveness than groups which 
have appeared recently. 
  The transfer of the experience of old groups to new ones is 
also possible, of course. This is accompanied by the passage of 
activists who have experience in public (not necessarily 
ecological) activity to the new group. 
  The problem of the transfer and accumulation of experience 
in 
the ecology movement is closely related to the processes of 
development of various ideological trends in it. A certain 
number of ecological organizations are oriented to comprehensive 
philosophical systems (Christianity, Rerikh's teachings, and 
original theories), but in most of them the sharing of views is 
not so comprehensive. 
  As was already said, predominating until 1991 were 
deliberate 
de-ideologization (initially, before the 1989 elections even 
external apoliticality), populism (abstractness of unifying 
slogans), and general democratic views whose sense consisted in 
a Western orientation of consciousness and selection of 
"democratic" symbols like "multiparty system," "parliament," and 
"market." 
  Despite the prevalence of these directions, already in 
1988-1989 virtually the entire ideological palette of the 
ecology movement had been formed. 
  "Patriotically" oriented groups evolved toward the idea of 
ethnocracy--the need to establish political privileges for the 
"native" nationality. Ethnocratic groups are operating in the 
ecology movement of St. Petersburg, Krasnoyarsk, and 
Novosibirsk. In 1992 the advocates of ethnocratic views made an 
unsuccessful attempt to extend their influence to the Russian 
Greens Party. The sharply negative reaction of the party to the 
attempt to organize a "patriotic" faction in its make-up showed 
that even in a moderate version "patriotic" ideas are vigorously 
rejected in the ecological milieu. 
  Conservative ideology which sometimes characterizes itself 
as 
patriotic (in the original meaning of this word) is more 
widespread. Despite the fact that the holders of these views are 
not organized within the framework of the ecology movement, they 
are fairly large in number. A conservative orientation of 
thinking corresponds to the ecology movement's orientation to 
protect the natural and cultural environment. 
  Liberal-democratic and social-democratic views remain the 
most widespread political ideology in the ecology movement. A 
legacy to the movement from previous development, democratic 
ideology is supplemented in the ecological milieu with greater 
attention to ecology and social protection. 
  Liberal-democratic ideology predominates in the Democratic 
Party of Greens of Chelyabinsk Oblast--the largest of the Greens 
parties. Democratic views of various hues predominate in the 
mass of members of other Greens parties too. 
  Respectable ecology movements and Greens parties of the West 
which fight to protect the environment without questioning the 
foundations of Western society are the usual model for the 
democratic ecologists to imitate. At the same time, however, the 
costs of Westernization in countries which were part of the USSR 
promote an evolution of the bearers of democratic ideology 
toward socialist, anarchist, and conservative views. But this 
process has just begun. 
  The weaknesses of the "democrats'" policies promote the 
support of state-socialist (communist) views in the ecological 
milieu too. But the CPSU's responsibility for the destruction of 
the environment in the recent past makes the state socialism of 
certain ecologists more of a dying phenomenon. 
  Different directions of nonstate socialism and anarchism are 
becoming much more popular among ecologists. The rejection of 
the state as a mechanism for solving social problems by these 
trends is in keeping with ecological criticism of the 
destruction of the environment by the departments. This initial 
area for cooperation becomes, upon further examination, 
supplemented by deeper correspondences. Both the Greens and the 
anarchists favor the priority of local interests over statewide 
ones. Preservation of the environment from outside expansion is 
the task of ecologists which incites them against the state's 
centralized bureaucracy. 
  A consistent ecological approach also presupposes rejection 
of the industrial organization of production--the main source of 
industrial expansion against the natural environment. As a 
constructive antithesis to the industrial system based on total 
control, anarchism suggests self-government and decentralization 
of the economy, including technological decentralization. This 
in turn is in keeping with the preference which ecologists give 
to small-scale production rather than industrial giants. 
  The participation of anarchists in the ecology movement, 
from 
the moment anarchist organizations were restored in the USSR, 
from the beginning promoted alliance relations between them and 
ecologists and then the interpenetration of anarchist and 
ecological organizations as the latter were politicized. 
  The diversity of anarchist organizations from left-socialist 
to anarchist-communist and the complicated relations with them 
were also reflected in the development of the politicized 
ecology movement. The conflicts of the syndicalists and 
communists in anarchism were especially noticeable during the 
formation of the Greens Party, which as a result split into the 
Russian Greens Party [RPG] in which the supporters of market 
relations--the syndicalist anarchists (communal 
socialists)--have great influence, and the Greens Parties League 
[LZP], whose initiators belonged to the ecosocialist 
(communist-anarchist) trend, which opposes market mechanisms. 
  Of course, the conflicts between the anarchists were not the 
only but merely one of the reasons for the split in the Greens 
Party, which had appeared "before its time," in the populist 
period. But the participation of politicized groups which had 
already undergone lengthy political evolution and gained the 
corresponding experience in events related to the split helped 
accelerate the political "evolution into manhood" of the ecology 
movement, which relatively quickly passed through the inevitable 
period of internal ideological conflict. Splits occurred in the 
milieu of the Greens parties earlier and less painfully than 
could have been expected in the event of autarkic development of 
the politicized ecology movement. As a result the politicized 
ecology movement was able to overcome the most acute internal 
conflict before the alternativist stage involving the mass 
politicization of ecologists began. It is significant that it 
was precisely the anarchists, who clashed among themselves in 
1991, who helped normalize relations between the RPZ and the LZP. 
  The very fact of a demarcation into different organizations 
helped reduce the internal tension which existed in the general 
but amorphous organization. The distribution of ecological 
organizations across the political spectrum and the quantitative 
predominance of general democratic cadres help consolidate 
efforts of politicized ecologists into the struggle against 
common enemies. Only in relation to ethnocratic organizations do 
most ecology organizations continue to be split. 
  An organization's ideology and the time when it emerged 
determine the structural composition. Initially, as a rule, 
amorphous groups and traditionally democratic organizations with 
an elected leadership and broad rights for rank and file members 
emerged. 
  The coordinating council, whose members made up the real 
aktiv who were involved in constant work, was the usual form of 
the management organs in democratic organizations. The rest of 
the members were enlisted for actions and assisted in certain 
work areas. Expenditures of personal time of rank and file 
members were less than that of leaders, but also caused an 
impact on the adoption of decisions. Internal specialization or 
notions of the need for this arouse a desire to support a 
sectional structure of organizations which from time to time 
dissolves into the common mass of members and then is 
periodically revived. 
  Despite the fact that this democratic form remains 
predominant, others also exist. Some organizations were able to 
preserve an amorphous structure--no management organs and only 
general coordination of work, support of regular exchange of 
information, and joint actions of those who want to join with 
it. The largest ecological organization of the former USSR, the 
Social-Ecological Alliance, has close to an amorphous structure. 
  There are centralized organizations which are grouped around 
one leader and maintain a higher level of discipline than other 
organizations. These organizations are not numerous. 
  Associations of ecological organizations keep to democratic 
(usually understood as federative), confederative, and amorphous 
structures. A confederation (a free association of subjects with 
minimal powers in the coordinating organs) is the most typical, 
but there is no strict line between these structural forms. 
Thus, for example, the Moscow Ecological Federation in reality 
is a typical confederation. As a rule interregional 
organizations with a freer structure are more viable. 
  The organizational self-identification of organizations is 
weakly related to their real structure. As a rule it depends on 
the organization's ideology, the conditions of its emergence and 
registration, and the traditions and conditions of the 
movement's development in a particular stage. Ecological 
organizations call themselves groups, parties, committees, 
sections, patrols, associations ["obyedineniye" and 
"assotsiatisiya"], alliances, federations, confederations, and 
so forth. The "ecologists' trade union" and "ecological 
international" also exist. But it is very risky to judge an 
organization by its name. 
  During the period of its existence, the ecology movement has 
undergone a noticeable evolution both from the standpoint of 
internal structure and from the standpoint of its position in 
society. Starting from the role of public assistant of state 
organs and at the same time of the lower classes in which 
opposition sentiments had matured, the ecology movement later 
became one of the levers used to overthrow the existing form of 
autocracy. 
  In trying to limit the destructive aspects of the industrial 
system, ecologists helped paralyze this system, because it 
cannot but be destructive. For this reason the "victory of 
democratic forces" was accompanied by paralysis of the ecology 
movement--industrial society, after replacing the red flags with 
the tricolored ones, did not change its quantitative 
characteristics and therefore did not have a response to the 
ecological "challenge." 
  For this reason the prospects of development of the ecology 
movement seem large in scale. It will apparently grow right up 
to the stabilization of the sociopolitical system and, if the 
new regime does not violently smash the structure of the 
ecological organizations, the movement will occupy its niche in 
the new social system. This may be both parliamentary opposition 
(in a number of cases--the regime's ally in conducting certain 
aspects of its policy) and a nonparliamentary movement oriented 
to pressure the establishment in order to check the development 
of ecological catastrophe. 
  In the event of the rout of the existing ecological 
organizations with the stabilization of the regime, the latter 
will all the same try to isolate or create loyal ecological 
structures which can fulfill functions close to those which the 
ecology movement performed in the 1970s. But in that case the 
accumulated experience of constructive work will be lost and 
radical-extremist trends will intensify in the illegal ecology 
movement. 
  In any case the peak of the ecology movement is still ahead. 
Processes of destruction of man's environment continue to 
develop at a rapid rate. The crest of the ecology movement which 
will evidently come at the end of the millennium may take on the 
most diverse forms, from a movement of civic initiatives to 
ecofascism and spontaneous destructive riots. Which of these 
forms is chosen depends not only on today's theoretical and 
practical searching by ecology movement activists but also on 
the form of society which sooner or later will replace the 
industrial society. 
  The crisis of industrial society which is manifested above 
all in the ecology crisis may be resolved through global 
catastrophe able to thrust civilization way back or even put an 
end to humankind, or through the qualitative transformation of 
society while preserving those achievements of civilization 
which do not result in the destruction of man's habitat. 
  This choice in turn depends on the ecology movement. At the 
same time, however, social strata interested in overcoming man's 
alienation from the adoption of decisions affecting him and his 
habitat are already being formed. The gradual surmounting of 
strict class division into those who govern and those who are 
governed, the development in society of principles of 
self-government and autonomy of economic and social subjects, 
the growth in the cultural level of broad strata of the 
population, the development of means of communication and 
flexible and energy-saving technologies, affirmation in social 
consciousness of the principles of civil rights and social 
stability, and recognition of the importance of global 
problems--all these at-first-glance heterogeneous circumstances 
help form a social stratum able to become the foundation of a 
new, already post-industrial society based on the predominance 
of a civil society over the state. Consequently the stratum 
itself may be called civil. 
  Representatives of this stratum combine in one body the 
functions of the intellectual, the direct producer of output, 
and their own manager, recalling the "small bourgeoisie" in 
traditional Marxist terminology. The adherence of this stratum 
to small production forms, the production of information, and 
frugality, including in relation to resources, is in contrast to 
the civilian class of industrial civilization and makes this 
stratum the potential base of the ecology movement. Recognition 
of this idea is a most important factor which determines the 
extent of the costs to overcome industrial civilization and the 
destructive ecological crisis. 
<H5>  INTERREPUBLIC ORGANIZATIONS </H5>
<H3>  Association of Anarchist Movements ["Assotsiaysiya dvizheniy 
anarkhistov" (ADA)] </H3>
  The association operates on the territory of the former 
USSR. 
Appeared in May-November 1990 during the withdrawal of some 
nonsyndicalist anarchists from the Confederation of 
Anarcho-Syndicalists. Has no coordinating organs and interaction 
is carried out through an information network and joint actions. 
  Participated in the blockade of the Balakovo AES in 
June-July 
1990 and in picketing the Gorkiy AEST [atomic heat and power 
plant] in May 1991. Certain activists of the Greens Parties 
League are members of the ADA. 
  In July 1991 in the industrial zone of the city of 
Zaporozhye 
organized an ecology protest tent camp. The action was conducted 
jointly with representatives of the Rainbow Keepers (Saratov), 
the Greens Parties League (participants in the League from 
Nizhniy Novgorod [including S. Fomichev], Kiev, and other 
places), the Association of Saratov Anarchists, the 
Revolutionary Anarchists Initiative (Moscow), anarchists and 
pacifists from Zaporozhye; a representative of the Confederation 
of Anarcho-Syndicalists and the Confederation of Independent 
Trade Unions, Dmitriy Dundich, participated. In all 19-20 
people. Seven of them were students from Nizhniy Novgorod, 
Kharkov, Kazan, and Kiev. 
  The camp's participants appealed to managers of enterprises, 
to the city soviet, and to the press. City residents' attitude 
toward the camp was at first indifferent. 
  On 19 July, the day before Metallurgists Day, eight 
representatives of the ecology protest camp, having notified the 
press in advance, climbed up the 200-meter smokestack of the 
coke shop of the Zaporozhye Coke and Chemical Plant and 
announced that they would not come down until their demands were 
met: 

  -  to stop the processing of imported coal tar; 
  -  to ensure 
that existing decontamination structures operated perfectly and 
to stop the work of production facilities without 
decontamination structures, providing workers with compensation 
for the forced inactivity; 
  -  to offer representatives of the 
public the opportunity to monitor the plant's operations 
unobstructed and to obtain reliable information at the 
enterprise. 

    On 22 July the chairman of the city soviet, Yu. Bochkarev, 
held a meeting with camp representatives and Deputy M. 
Chernysheva, who supported the pickets' demands. During the 
meeting a support rally was held in front of the city soviet 
building. A reconciliation commission made up of representatives 
of industry, deputies, and representatives of the protest camp 
was created. (Even before the camp the city soviet deputies had 
decided to shut down the processing of coal tar in the 
tar-distilling shop.) 
  On 30 July the pickets left the stack. 
  On 5 August two rallies were held in Zaporozhye: a 
sanctioned 
rally (1,000 people) and an unsanctioned one (2,000 people). 
There it become known that the plant was continuing production 
while the pickets had left the stack earlier, believing the 
promise that their demands would be met. 
  On 6 August the pickets blocked the plant administration 
with 
a demand to fulfill the oblast nature committee's decision. The 
plant administration expelled them by calling OMON. The pickets 
were taken to the police station. The rayon procurator announced 
that criminal proceedings were being instituted against them. 
Eight members of the ecology camp (of those who remained free) 
declared a hunger strike demanding that those arrested be freed 
and that the demands be carried out. The city's population 
stopped the militsia's attempts to expel the hunger strikers 
from the square. In the evening of that same day all those 
detained were freed. 
  On 7 and 8 August the hunger strike on the square continued. 
  On 9 August the decree of the oblast nature committee was 
fulfilled--the tar-distilling shop stopped processing imported 
tar. 
  On 10 August a notice from the procurator's office arrived: 
for lack of elements of a crime criminal proceedings would not 
be instituted against the pickets. The camp's hunger strike was 
terminated. 
  On 12 August a rally of city residents proposed to make the 
pickets Honorary Citizens of Zaporozhye. 
  On 17 August an ecological mourning march was conducted 
within the framework of the Red Rue festival. A Central 
Television program filmed the march and the film was later 
stolen from the reporter on the train. 
  Under the influence of the action in Zaporozhye, an informal 
ecology organization called the "Clean Air Committee" emerged. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2; 
  -  "A New 
Generation Chooses the Stacks," SPASENIYE, No 9, August 1991, p 
6; 
  -  Turin, A., "Ultimatum... From the Stack," SPASENIYE, No 8, 
August 1991, p 3; 
  -  "Just Climb the Stack," ZELENYY MIR, Nos 
27-28, 1991, p 2. 

<H3>    Association of Ecology Centers ["Assotsiyatsiya 
ekologicheskikh tsentrov"] (AETs, original name: Association of 
Ecology Centers of the USSR) </H3>
  The association formulates alternative plans, designs, and 
technologies; organizes ecological education; studies public 
opinion; gathers and disseminates ecological information; and 
participates in solving problems related to agricultural and 
industrial pollution. 
  Director--Aleksandr Nikolayevich Ivanov. 
  Address: 107078, city of Moscow, ul. ["ulitsa"--street] 
Novo-Basmannaya, d. 10, tel. 265-90-14. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "To the Informals, About the 
Informals," SPASENIYE, March 1991, p 2. 

<H5>    Bambi ["Bembi"] </H5>
  This is the association of a children's esthetics and 
ecology 
club. Initiator of its creation--Nataliya Sergeyevna Bondarchuk. 
The club was formed in 1985 and was officially registered at the 
All-Union Nature Protection Society (see article) in the same 
year. 
  The by-laws were adopted in 1985. A program is drawn up 
every 
year. 
  The goals of the club are: defense of animals and spiritual 
education of the children. 
  In operation are a press center (15-20 people); an ecology 
group (works on questions of the ecology of the spirit); circles 
devoted to the French and English languages, stage studies, 
vocals, the "living ethics" of Yelena Ivanovna Rerikh, and the 
study of a children's Bible. The instructors are actors of the 
Film Actors Theater (the Film Actors Studio Theater). 
  The organizational structure includes a president, director, 
deputy director, accountant, teachers, children's council, 
parents aktiv, and board of trustees. 
  The collective members of the Bambi Association are: 
children 
of the associates of the two Novodaryino Sovkhozes (Moscow 
Oblast and Altay Kray); children of associates of the Far East 
Aeroflot Corporation (city of Khabarovsk), the Mine imeni Third 
International (city of Nizhniy Tagil), and INTURSERVISA, the 
children's aktiv of the city of Suzdal museum, and students of 
the philological department of MGU [Moscow State University]. 
Members of the association include 25 actors of the Bambi 
Children's Theater aged 3 to 20. About 120 children participate 
in all. 
  As yet there are no membership dues. There are no official 
premises. The society is a collective member of the USSR-USA and 
USSR-France friendship societies. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    All-Union Society for the Defense of Animals ["Vsesoyuznoye </H5>

obshchestvo zashchity zhivotnykh"] 
  Goals are to monitor compliance with nature protection 
legislation, provide ecological education, disseminate 
information, shape public opinion, and participate in resolving 
problems of protecting the plant and animal worlds. 
  Chairman is Oleg Stepanovich Kolbasov. 
  Address: 11941, city of Moscow, ul. Frunze, d. 10, USSR 
Academy of Sciences IGP [Institute of the State and Law], tel. 
291-88-16 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 
  -  "To the Informals...," op. cit., p 
2. 

<H3>    All-Union Council of Hunters and Fishermen's Societies 
["Vsyesoyuznyy sovet obshchestv okhotnikov i rybolovov"] (VSOOR) </H3>
  The council unites the efforts of republic societies in 
order 
to improve the results of labor in the new conditions of 
economic activity and develop direct economic, trade, 
scientific, technical, educational, and production ties as well 
as cooperation in the foreign economic area. The council 
performs advisory-recommendation and coordinating functions. 
  Interrelations among republic societies are built on the 
basis of their complete self-sufficiency and independence. 
  The council was formed on 30 November 1989. Taking part in 
the work of the first session of the council were 69 delegates 
from republic hunters and fishermen's societies, except the 
societies of Lithuania, Estonia, and Armenia. Representatives of 
Georgia abstained on the question of forming the VSOOR. 
  The council's chairman is A. A. Ulitin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Little Dove ["Golubka"] </H5>

  This is a Soviet-American humanitarian initiative. Jointly 
with activists of American social movements it carries on 
educational work in the USSR (Russia). Conducts seminars on 
ecological and humanitarian problems. Adheres to a pacifist 
orientation. The Golubka documents say: "As Mahatma Ghandi said, 
'What you do may seem insignificant, but it is very important 
that you do it.'" 
  Address: 121601, city of Moscow, Filevskiy bulvar, d. 1, kv. 
[apartment] 48, tel. 42-92-83, Fax 292-65-11, a/ya 3775; USA, 
GOLUBKA, c/o Tides Foundation, 1388 Sutter Street, San 
Francisco, CA 94109. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greenpeace ["Grinpis"] </H5>

  The Soviet division was founded in June 1989 under the 
international foundation "For the Survival and Development of 
Humankind." It has a structure and carries on activity 
characteristic of Greenpeace, that is to say, in fact it is the 
Greenpeace regional organization. 
  The chairman of the Soviet division in 1989-1991 was 
Academician A. Yablokov and members of the board of directors 
included S. Zalygin, R. Sagdeyev, A. Chilingarov, and Ye. 
Velikhov. 
  In 1991 the Greenpeace leadership was completely replaced 
and 
the role of foreign Greenpeace organizations in the management 
of the Russian organization was increased. At this time there 
exists a board of directors consisting of five people, among 
whom are the chairman of the Greenpeace International [GI] board 
of directors, Matti Vuori, and the director of the Russian 
Greenpeace office, Aleksandr Knorre. 
  In 1990 the Soviet division was working on two programs: 
"Ladoga" and "Western Siberia." The latter proposed to intervene 
in construction of gigantic joint-venture oil and gas chemical 
complexes in Tyumen Oblast. The coordinator of the "Western 
Siberia" ecoprogram is Vladimir Zamoyskiy. 
  At the present time Greenpeace of Russia projects 
(reconciled 
with GI) oppose paper and pulp industry wastes and support 
nuclear-free seas, energy conservation and alternative sources 
of energy, and other things. 
  The execution of ecological programs requires cooperation 
with local Greens associations, representatives of the press, 
and state functionaries. Within the framework of the programs, 
information is gathered on enterprises and public opinion and on 
who is involved in the construction of a joint venture. 
Greenpeace publishes the information gathered. The making of 
videofilms is planned. 
  Address: 121002, city of Moscow, a/ya 60; city of Moscow, 
Kolpachnyy per. [lane-"pereulok"], d. 6, korp. [block] 4, kv. 
26, tel: 928-76-51, Dmitriy Anatolyevich Shaposhnikov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Nature Protection Squads Movement ["Dvizheniye druzhin po </H5>

okhrane prirody"] (DOP Movement) 
  An "alliance of public non-professional volunteer 
organizations and associations of youth" (by-laws of the DOP 
Movement). It operates on the territory of the USSR. 
  In mid-1991 there were 156 squads operating in the USSR, 
which included roughly 5,000 people; for the most part they are 
students and in addition a small group of VUZ graduates and 
secondary school students. 
  The movement's goal, according to the by-laws, is "the 
resolution of pressing problems of protection of nature and the 
environment and education based on practical nature protection 
activity by field specialists able to solve these problems." No 
political goals are pursued. 
  "Concrete practical nature protection activity is the most 
important thing for the movement's participants. For the 
movement the conversion of this work into a fashionable hobby or 
political bait is intolerable." (From the "DOP Movement 
Manifesto.") 
  The basic areas of activity of the DOP Movement include the 
following: identification, planning, and organization of 
protectable natural areas, protection of preserves and spawning 
grounds of cartiloginous fish, the fight against poaching, land 
planning, protection of small rivers, the fight against 
industrial and agricultural pollution, and ecological propaganda. 
  The DOP Movement's activity is noncommercial in nature and 
the basic source of funding is voluntary donations. 
  Membership in the DOP Movement is collective. The following 
demands are made on the particular squads in addition to local 
nature protection work; complete self-government, voluntary 
selection of work areas and independent planning of the work, 
constant contact with other DOP's, and participation in 
intersquad programs and actions. 
  Members are accepted in the DOP Movement at movement 
conferences (including regional ones, but with the participation 
of at least 12 members of the movement) by an absolute majority 
vote. Given compliance with the same conditions an organization 
may be expelled from the movement. Organizations which wish to 
be members of the movement are registered as candidates for 
membership in the movement the moment the application is 
submitted to the secretariat of the DOP council. 
  The highest body of the DOP Movement is the all-Union 
(interrepublic) conference convened by the movement council in 
accordance with the decisions of the previous conference or on 
demand of at least one-third the movement's members, but at 
least once every 2 years. The conference ratifies the movement's 
by-laws and other documents and the criteria and procedure for 
membership in the movement, admits and expels members of the 
movement, and elects the DOP Movement council and other elected 
organs. Members of the DOP Movement participate in conferences 
with full voting rights, while candidates for membership have 
the right to a consultative vote. Decisions of the conference 
and the organs of the DOP Movement are only recommendations. 
Conferences have the right to reorganize the movement (with at 
least a two-thirds vote in favor) or to terminate its activity 
(by unanimous decision). 
  The DOP Movement council is the movement's 
executive-representative and coordination-information organ 
between all-Union (republic) conferences. The movement council 
is a legal person that represents the movement. The coordinator 
of the movement council is Askhat Abdurakhmanovich Kayumov 
(Nizhniy Novgorod). 
  The movement has the longest history among the independent 
public movements. It began with a nature protection circle 
organized in the spring of 1958 by students of three Tartu 
VUZes--Tartu State University, the Estonian Agricultural 
Academy, and the Tartu Medical Institute. The first nature 
protection squad appeared on 13 December 1960 in the school of 
biology at MGU. At first the DOP's appeared in natural science 
departments but soon other departments joined the movement. 
  By 1972 there were about 40 student squads. Operations work 
in the fight against poaching was the basic area of their 
activity in the early 1970s. But in 1970-1972 four squad members 
were killed by poachers. 
  And in order to avoid dilettantism and fragmentism, on 21-27 
September 1972 the first all-Union DOP seminar with the 
participation of delegations from 28 squads from 22 cities of 
the USSR was held using the facilities of the DOP in the MGU 
school of biology. Then DOP seminars and conferences began to be 
conducted every year or two. The squads' activity began to be 
comprehensive in nature: operations work was supplemented with 
scientific research work. 
  In 1976 in Kirov squad members conducted a seminar in which 
the first comprehensive program for the fight against poaching 
as a social phenomenon--the "Shot" program--was discussed. Since 
that time occupational training of squad members has begun: they 
have studied the foundations of social psychology, legislation, 
criminal science, and operations work. 
  In 1976-1977 work began on other multifaceted international 
programs as well: "Spruce," "Recreation," "Fauna," and others. 
Their goal was to reduce the level of poaching. 
  On 13-19 September 1977, in Perm, at the "Methodology of VUZ 
Youth Work on Nature Protection" seminar, the coordinating 
council of the student nature protection movement was created in 
order to improve contacts between squads; Svyatoslav Zabelin, 
the commander of the MGU DOP, became the chairman of the council. 
  The years 1972-1979 were the peak years of the DOP's. Among 
the activists of the movement of that time were Nikolay Krayev 
(the Kazan Squad), D. Kavtoradze, who worked together with 
Svyatoslav Zabelin on uniting the squads, and the first 
commander of the DOP of the Kazan Chemical Technical Institute, 
Sergey Mukhachev; his statement that "Nature should have its own 
people everywhere" became the slogan of the DOP. 
  Since the early 1980s, in the opinion of some of the 
movement's leaders, a crisis situation has taken shape in the 
DOP's. The number of squads has begun to decline gradually. 
  Beginning in 1985, different ecological and 
ecological-political groups and organizations began to appear on 
the basis of the DOP's. Among other things, in August 1987 the 
Social-Ecological Alliance (SES) was formed at the initiative of 
DOP graduates. 
  The First All-Union DOP Movement Conference was held in 
Dolgoprudnyy in Moscow Oblast on the base of the MFTI [Moscow 
Physicotechnical Institute] DOP on 8-11 December 1987. The 
Ecology and Peace Association, the USSR Academy of Sciences 
All-Union Ornithological Society, the MFTI DOP, and the MGU 
school of biology conducted it. Taking part in the conference 
were 110 DOP's (96 with a full vote and 14 with a consultative 
vote) from 74 cities of the USSR. The conference was dedicated 
to defining strategic tasks and resolving organizational 
questions. The "Model Statute of the Student DOP" and the 
"Statute on the Coordinating-Methodological Council of the DOP 
Movement" were adopted and the members of the council and its 
chairman, Aleksey Volkov (MFTI DOP), were elected. 
  The Second All-Union DOP Movement Conference was held in the 
settlement of Staryy Saltov in Kharkov Oblast on 23-27 October 
1989. Participating in it were 78 squads (63 with a full vote 
and 15 with a consultative vote) from 58 cities of 3 Union 
republics. The "DOP Movement By-Laws," the "Statute on 
Membership in the DOP Movement," the "Statute on the Movement 
Council," and the "Statute on the Editing of Information 
Materials ("Herald") (Sergey Taglin, KhGU [Kharkov State 
University], Kharkov, became the editor). The need for regular 
publication of a press organ was recognized. 
  The basic provisions of the resolution adopted at the 
conference were later included in the USSR Supreme Soviet Decree 
"On Urgent Measures To Normalize the Ecological Situation in the 
Country." 
  Many of the conference participants linked the crisis in the 
movement with the lack of a political program and of new leaders. 
  A group for formulating the "DOP Movement Platform" and the 
"DOP Movement Manifesto" was created at the conference. 
  A representative function was declared the priority function 
of the movement council at this stage. Dmitriy Boriskin (VGU 
[Voronezh State University] DOP, Voronezh), Askhat Kayumov (GGU 
[Gorkiy State University] DOP, Gorkiy), and Oleg Cherp (MFTI 
DOP, Moscow) were elected cochairmen of the council. The 
chairman of the council before then, Aleksey Volkov (MFTI DOP), 
was elected one of the four deputy chairmen of the council along 
with Aleksandr Gavrilov (RRTI [Ryazan Radiotechnical Institute], 
Ryazan) and Dmitriy Goncharov (MGU school of biology DOP, 
Moscow); one place was reserved for the Belarus representative 
until the republic conference. 
  Another 10 organizations (including the Tula Oblast Youth 
Ecological Alliance [TOMES] and the Kharkov Oblast Ozone Ecology 
Center) were admitted into the movement. 
  The movement's Third All-Union Conference was in all 
probability conducted in later 1990 in the city of Moscow on the 
base of MGU, MFTI, and MOPI [Moscow Oblast Polytechnic 
Institute]. 
  In 1990-1991 the movement had to perform various nature 
protection tasks. The Voronezh State University DOP fought 
against the construction in Voronezh of an atomic heat plant; 
the Nizhniy Novgorod State University DOP fought for an 
immediate drawdown of the Cheboksary Reservoir; and the Ryazan 
people's volunteer nature protection squad--for preserving the 
Oka floodplains. Squads also worked on the "Fauna," "Flora," 
"Recreation," "Refuge," "Spruce," "Primrose," "New Year's 
Bouquet," and "Spawning" programs. 
  The DOP Movement cooperates regularly with the 
Social-Ecological Alliance (see article), conducts joint 
actions, exchanges information, and helps in work. Some of the 
DOP's are collective members of the SES. 
  The emblem of the movement was adopted by decision of the 
Perm Conference (1977). The author was Sergey Krinitsyn (Ural 
State University DOP, Sverdlovsk). "The emblem of the movement 
is a circle whose top half is dark blue and whose bottom is 
green. Located on the right side of the emblem is a red circle 
whose center lies on the border dividing the blue and green 
parts while the circumference passes through the center of the 
sign. The diameter of the small circle is one-third the diameter 
of the large circle." (From the materials of the All-Union DOP 
Movement Conference of 8-11 December 1987.) 
  Addresses: 119899, city of Moscow, GSP-3, Leninskiye gory, 
MGU, School of Biology, DOP Movement Coordinating-Methodological 
Council; 603019, city of Nizhniy Novgorod, Kremlin, korpus 2, k. 
20, "Dront" ecology center, DOP Movement Council, tel. 39-75-58, 
Council coordinator Askhat Abdurakhmanovich Kayumov; city of 
Perm, tel. 48-89-66 (home), Aleksandr Nikolayevich Balyberdin, 
deputy coordinator; city of Moscow, tel. 339-07-19 (home), Zoya 
Vyacheslavovna Talitskaya, deputy coordinator. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. Krupneyshiye 
organizatsii i dvizheniya: kratkiy spravochnik" ["Greens in the 
USSR. The Largest Organizations and Movements: A Short 
Reference"], "Lika" Information Research Center, Moscow, 1990, 
pp 5-6; 
  -  "To the Informals...," op. cit., p 6. 

<H3>    Movement To Create the Greens Party ["Dvizheniye za 
sozdaniye partii `Zelenykh'"] </H3>
  This is an informal ecological-political organization 
operating on the territory of Russia, Belarus, Kazakhstan, and 
Ukraine. Appeared in December 1988 as the organizing committee 
of the Greens Party as a result of the meeting in Moscow of 
representatives of various ecology clubs from Kuybyshev 
(Samara), Leningrad (St. Petersburg), Bryansk, Khmelnitskiy, and 
other cities. In the spring of 1989 the Moscow group joined it 
and a new name was ratified. 
  In August-September 1989 the Kuybyshev (Samara), Chapayevsk, 
and certain other sections of the movement took part in 
organizing a protest action against the construction of a plant 
to destroy chemical weapons in the city of Chapayevsk in 
Kuybyshev (Samara) Oblast. The protest was supported by the 
public and labor collectives. As a result, by decision of the 
government construction of the plant was terminated. 
  In late March 1990 the Founding Conference of the Greens 
Party (see article) took place in Moscow. Taking part in its 
work were about 80 representatives of various ecology 
organizations from 4 republics (the RSFSR, Belarus, Kazakhstan, 
and Ukraine). 
  The resolution adopted at the congress was based on the 
movement's program formulations: "We support the radical 
transformation of society on the basis of the preeminence of 
ecology, civil self-government, and direct democracy. We intend 
to utilize existing legislative institutions as a rostrum to 
publicize our views and ideas and to oppose totalitarianism, 
authoritarianism, chauvinism, industrial expansion, and 
ecofascism..." 
  Address: 443084, ul. Voronezhskaya, d. 190, kv. 15, Sergey 
Krivov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Lukanovskiy, N., "The Greens 
Party: A Test of Strength," ZELENYY MIR, No 1, 1990, p 5. 

<H5>    Dniester ["Dnestr"], Interrepublic Public Committee </H5>
  It was formed in 1986. Conducts ecological and scientific 
expeditions and monitors the ecological balance of the Dniester 
River basin. 
  Member of the Social-Ecological Alliance (see article). 
Participates in the Greens Movement (see article) and cooperates 
with the "Chernoye morye" [Black Sea] organization. 
  Address: 278210, Moldova, pgt [urban-type settlement] Novyye 
Aneny, ul. Kishinevskaya, d. 12, kv. 6, tel. 2-30-84, Aleksandr 
Fedorovich Sefer. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Movement </H5>

  This is an all-Union public organization. The goals are: 
monitoring the state of the environment, the population's 
health, and the quality of food products and consumer goods; 
gathering and disseminating ecological information; providing 
ecological education, and shaping public opinion. 
  The founding conference of the Greens Movement was held in 
February 1989, 2 months after the founding conference of the 
Social-Ecological Alliance (see article); the two organizations 
overlap each other in many respects, and at first this made it 
questionable whether their coexistence was useful. The common 
goals and proximity in time of appearance are results of the 
fact that "the idea was hovering in the air" and different 
people undertook to carry it out. At the same time there are 
certain differences between the organizations. 
  The chairman is the writer and journalist Oleg M. Poptsov 
(since 1990 a people's deputy of the RSFSR and member of the 
RSFSR Supreme Soviet). Responsible secretary in 1989-1991 was 
Lyubov Borisovna Rubinchik. 
  In 1989 concluded an agreement with the German Robin Hood 
Greens Movement (headed by Gerd Renker) and the Ecological 
Institute in Freiburg (FRG) on prospects for creating an 
International Information Center on the Ecology of Nature and 
Ecology of Culture, a Data Bank. The West German side offered 
computers and organizational equipment and the editorial office 
of the journal SELSKAYA MOLODEZH [Rural Youth] allocated space. 
Information is gathered in three fields--ecology, culture, and 
the ecology movement. According to the contract, the Greens 
Movement data bank is a noncommercial enterprise for public 
movements. In the future it is planned to create a network of 
computer data banks throughout the country and join it up with 
an international data bank network. 
  Together with some state and public organizations, the 
action 
"Caravan of Life" (a special train on the Murmansk-Tashkent 
route) was held from 17 October to 4 December 1991 in order to 
gather information on the ecological situation in the country 
for the government and the Brazil-92 conference. During the 
action meetings were held with local Greens, harmful production 
facilities were visited, and press conferences were held. Taking 
part in the "Caravan of Life" were activists of the Ecological 
Developments Bureau (Yu. Shevchuk--leader of the action), 
anarchist organizations, and the Russian Greens Party (see 
article). 
  The Greens Movement runs a regular column,"Weather for 
Tomorrow," in the journal SELSKAYA MOLODEZH (for the most part 
information materials are published in it) and has its own page 
in the weekly ZEMLYA. 
  After some leaders of the Greens Movement came to power, its 
organizational structure became markedly weaker and a whole 
number of leading activists focused on work in the 
Social-Ecological Alliance (see article). 
  Address: 125015, city of Moscow, ul. Novodmitrovskaya, d. 
5a, 
kom. [room] 1103, editorial office of the journal SELSKAYA 
MOLODEZH, Valeriy Yuryevich Khabidulin, journalist, head of the 
journal's science department, Moscow, tel. 285-80-27 (work). 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. Krupneyshiye...," op. cit., p 10; 
  -  "The 
Caravan of Life," EKOLOGICHESKAYA GAZETA, No 10, 1991, p 2; 
  -  "To 
the Informals...," op. cit., p 2; 
  -  Khmara, I., "Make Decisions 
Yourself," ZELENYY MIR, No 11-12, 1991, p 11. 

<H5>    ZELENYY MIR [Green World]. Ecology: Problems and Programs </H5>
  This is an ecological newspaper. The founders are the 
Soyuzekopress Information-Publishing Association, USSR 
Goskomprirody, the Inzhenernaya Ekologiya Publishing Foundation, 
the Soviet Association of UNESCO Clubs, and the All-Russian 
Nature Protection Society. 
  It has been published since April 1990. 
  It consists of 16 pages. The print run is not indicated. The 
language is Russian. 
  The editor in chief is M. L. Borozin. It is black and white. 
It has the format of the newspaper NEDELYA. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  ZELENYY MIR, Nos 1-22, 1991. 

<H3>    The Information-Research Center of the Movement for Communes 
["Informatsionno-isledovatelskiy tsentr dvizheniya za kommuny"] </H3>
  It was created in July 1988 at a seminar convened at the 
initiative of sociologist S. Bondazhevskiy (participants 
included supporters of creating communal settlements from seven 
cities--Leningrad [St. Petersburg], Dnepropetrovsk, Kirov, 
Ryazan, and others). It has dissociated itself from the 
pedagogical communal movement. They consider their goal to be 
communism, with a plurality of paths to it. About 20 
participants. Small seminars are conducted. The problem of 
ecological settlements is studied. 
  Address: city of Kaluga, tel. 6-42-59 (work), Sergey 
Gavrilovich Ikryannikov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galkina, L., "Zelenyye v SSSR. 
Spravochnik" [Greens in the USSR. Directory], Moscow, 1991, p 
15. 

<H3>    Travel Club in Defense of Peace and Nature ["Klub 
puteshestviy v zashchitu mira i prirody"] </H3>
  This is attached to the Soviet Peace Defense Committee. 
Created in 1987. 
  The club's goal is "organization of meaningful recreation 
for 
citizens, development of their political and social activism, 
affirmation of a healthy way of life, indoctrination of 
champions of peace and nature protection who have highly 
developed ecological sophistication, and formation of harmonious 
relations between nature and man." 
  Activities in 1990 included the following: 

  -  from 23 through 28 May the International Scientific 
Seminar "Ecology, Culture, and Education" took place in Odessa; 
  -  starting on 1 June an expedition in the footsteps of 
Radishchev 
from St. Petersburg to Moscow; 
  -  starting on 1 August--an ecology 
cruise on the Volga (Moscow to Perm). 

    Address: 129010, city of Moscow, pr. [prospect] Mira, d. 36, 
tel. 280-35-82, 280-33-82. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Georgiyeva, L., "Forward to 
Nature," ZELENYY MIR, No 2, 1990, p 3. 

<H3>    Committee To Save the Black Sea ["Komitet spaseniya Chernogo 
morya"] </H3>
  The decision to create it was made at the All-Union 
Conference on Social-Ecological Problems of the Black Sea held 
in Kerch no later than April 1991. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Michurin, Yu., "Scientists Warn: 
In the South Breathing Will Soon Be Dangerous to Your Health," 
SPASENIYE, No 3, March 1991, p 3. 

<H3>    Ecological Planning Laboratory of the Soviet-American 
Cultural Initiative Foundation ["Laboratoriya ekologicheskogo 
proyektirovaniya sovetsko-amerikanskogo fonda 'Kulturnaya 
initsiativa'"] </H3>
  It was founded in 1988 under the Altair Agency. The by-laws 
were adopted at that time. The initiators of the creation of the 
laboratory were a group of people who worked on similar topics. 
It operated under the foundation for less than a year. 
  The basic areas of work were: 

  -  conduct of independent ecological expert studies; 
  -  work on 
examining different ecosystems as a consequence of social 
transformations in the past (this topic was declared the best at 
the foundation's competition); 
  -  development of various 
ecological plans; 
  -  work to create preserves and substantiating 
the usefulness of creating preserves along the Cossack defense 
line of the Moscow state; 
  -  reconstruction of the history of land 
use of particular territories based on the current state of the 
top soil; 
  -  expert studies of the causes of fluctuations in the 
ground water level in certain regions, primarily in the European 
part. 

    Ten people are permanent members; specialists are recruited 
for particular jobs and students--for on-the-job training. 
Age--25-33 years. 
  The laboratory was the founder of the Social-Ecological 
Alliance (see article) and belongs to the Academy of the Urban 
Environment as a cofounder. 
  The director of the laboratory is S. V. Ponomarenko. 
  Address: city of Moscow, per. Mariny Raskovoy, d. 19/23, 
laboratory: tel. 214-52-58, 190-23-68, S. V. Ponomarenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Parties League ["Liga zelenykh partiy"] </H5>

  This is a party-confederation of non-professional groups. 
  It was formed on 10-11 May 1991 at the meeting of several 
Greens Party organizations (see article) in Nizhniy Novgorod. 
The Nizhiy Novgorod Greens Party, the Lipetsk Greens Party 
Organization, and several organizing committees of Greens Party 
organizations announced the name change of the Greens Parties to 
the Greens Parties League. This decision was not recognized by 
most Greens Party organizations. The Greens Parties League 
adopted a left-radical declaration which rejected the principles 
of industrial society. 
  In May-October 1991 it sharply opposed the Russian Greens 
Party (see article), considering it "to blame for the split" of 
the Greens Party. 
  The basic forms of work are: conducting rallies, picket 
lines, and the like. 
  The initial size of the league [LZP] was a few dozen people. 
In October 1991 several liberal Greens organizations which did 
not recognize the left-radical principles of the LZP founders 
joined it; they included the Democratic Greens Party of 
Chelyabinsk Oblast (see article) with a formal membership of 
more than 1,000 people. 
  The social-occupational make-up includes pupils, students, 
workers, white-collar workers, and unemployed people. 
  There are about 25 local organizations in all in the league. 
In addition to Russia, league organizations exist in Kiev, 
Odessa, Ilyichevsk, Bashkiria, Tataria, Chuvashia, and other 
places. 
  The cochairmen of the league are S. Fomichev (Nizhniy 
Novgorod), Fedorov (Lipetsk), and T. Bulat (Odessa). The 
coordinating council of the league consists of 15 people. 
  League activists participated in the blockade organized by 
the Nizhniy Novgorod Greens and anarchists of the AST being 
built there. In July-August 1991 the members of the LZP from 
Nizhniy Novgorod, Kiev, and other cities along with Ukrainian, 
Kaliningrad, and Saratov anarchists participated in the blockade 
of an ecologically dangerous industrial enterprise--the coke 
chemical combine in Zaporozhye. In addition, each local 
organization of the league conducts its own local actions. 
  On 26-27 October 1991 the Third LZP Congress (the numbering 
of the congresses comes from the first PZ [Greens Party] 
congress) was held in Lipetsk. Corrections were made to the 
by-laws and the coordinating council and three cochairmen of the 
league were elected. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Funds 1, 2; 
  -  "The New Generation Chooses the Stacks," SPASENIYE, No 9, 
September 1991, p 6; 
  -  Tyurin, A. "An Ultimatum... From the 
Stack," SPASENIYE, No 8, August 1991, p 3; 
  -  "Just Climb Up the 
Stack," ZELENYY MIR, No 27-28, 1991, p 2. 

<H3>    Moscow Ecology Center ["Moskovskiy ekologicheskiy tsentr"] 
(METs) </H3>
  The center has the status of an international and all-Union 
club and at the same time a comprehensive educational 
institution. 
  Created in the spring of 1991. The founders were the USSR 
Ecological Alliance (see article), the Moscow Institute of 
Precision Chemical Technology imeni M. V. Lomonosov (MITKhT) and 
Russia's Open University (ROU). 
  The chairman is V. S. Timofeyev, professor and rector of 
MITKhT. Manager of the educational center is N. F. Reymers, 
doctor of biological sciences and president of the Ecological 
Alliance. 
  Jointly with Russia's Open University the center created a 
new specialization, ecology. One can obtain a bachelor's degree 
and a master's in this field. Anyone who wants, from an upper 
classman to an academician, can study. Courses are by 
correspondence but since September 1991 short regular courses 
have begun to operate. It is planned that the best students will 
spend a year studying ecology at one of the U.S. universities. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Moscow Ecology Center Created," 
ZELENYY MIR, No 19-20, 1991, p 5; 
  -  SPASENIYE, No 6, July 1991, p 
4. 

<H5>    Next Stop USSR ["Nekst-Stop-SSSR"] </H5>
  The movement originated in Denmark in 1987 when 65 young 
Danes went to the United States and near the nuclear test range 
in Nevada began to propagandize ideas of peace and speak out 
against nuclear weapons testing. 
  Next Stop's first contacts with Soviet independent 
organizations (Commune, "Socialist Initiative," and others) date 
to February 1988. It was proposed to set up extensive 
communication between activists of the public movement and 
people with common interests within the framework of a people's 
diplomacy program. 
  An organizational meeting of representatives of Denmark's 
movement and the Soviet initiative group was held on 9-10 July 
1988. The initiative group reached 250 people in 1988. 
  In April 1989 a Next Stop group was formed in Kazakhstan and 
set its goal to stop experiments at the Semipalatinsk and 
Aktyubinsk test ranges. 
  The next meeting of participants in the movement from the 
USSR and the Scandinavian countries (about 150 people) took 
place on 4-5 February 1989. Participating from the Soviet side 
were representatives of youth, political, ecological, and 
creative organizations and rock groups from more than 20 cities 
of the USSR from the Baltics to Almaty. 
  In September 1989 the international campaign "Next Stop" was 
held throughout the USSR, and during it a debate was held in 
Murmansk on the topic "Society and Ecology" (representatives of 
the movement from Denmark, Finland, the FRG, and Sweden 
participated). 
  The Kazakhstan group became an independent public 
organization waging a struggle against nuclear testing. From 500 
to 1,000 people participate in the events. The coordinating 
council consists of 17 people. The coordinator is D. Mamadzhanov. 
  Address: Kazakhstan, city of Almaty, tel. 62-94-08, 
69-64-48. 
Garun Tasybayev. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  OBSHCHINA (Moscow), No 6-7, 1988; 
  -  "Rossiya: partii...," op. cit., pp 46, 68. 

<H3>    Noosphere ["Noosfera"], All-Union Ecology Association 
["Vsesoyuznoye ekologicheskoye obyedineniye"] (VEO) </H3>
  Operates on the territory of the former USSR and other 
countries. The founding meeting of the VEO occurred on 13 June 
1989. The founders were the International Foundation for the 
Survival and Development of Humankind, Zhilsotsbank SSSR, USSR 
Academy of Medical Sciences Institute of Labor Hygiene and 
Disease Prevention, the USSR Ecological Alliance (see article), 
the council of primary organizations of the USSR Goskomprirody 
All-Union Economic Society, and the Soviet Committee on the 
UNESCO "Man and the Biosphere" Program. 
  The by-laws were registered in the Moscow Soviet in 
September 
1990. The program is adopted for the year. 
  The goal of its creation was to concentrate scientific and 
production potential of various types of organizations on the 
effective practical resolution of problems of protection of 
nature and human health in different regions of the USSR and 
abroad. 
  The tasks are: to create alternative, ecologically clean, 
renewable energy, ecologically clean and safe means of 
transportation, equipment to protect humans from the impact of 
dangerous artificial factors of the environment, and means of 
improving human health. 
  The forms of activity are: 

  -  joint utilization of the latest technologies and systems 
for decontaminating air, water, and soil; 
  -  organization of 
production and sale of output in demand on the world market; 
  -  joint patenting of technical innovations and technologies; 
  -  development and introduction of low-waste technologies, 
ecologically clean technologies for handling agricultural 
production, equipment for biological stimulation and defense of 
plants and animals, and ecologically clean technologies for 
processing agricultural products; 
  -  development and creation of a 
bank of technologies for processing waste that exists in the 
USSR and abroad; 
  -  practical assistance to enterprises in 
compiling ecological factory labels and conducting ecological 
expert studies of production facilities, soil, and water; 
  -  propaganda of ecological knowledge--seminars on general and 
special ecological topics; 
  -  encouragement of work in the area of 
protection of nature and human health together with state 
institutions, cooperatives, and domestic and international 
public organizations; 
  -  publication of collections of the most 
interesting reports. 

    The collective members (partners) of the VEO are introducing 
the following developments: a compact power plant, technologies 
for managing atmospheric precipitation, an automated hothouse, 
an electronic separator, intellectual development games by the 
pedagogue B. P. Nikitin, a writing instrument for the blind, 
disposable syringes, dishes, and so forth. 
  The membership is mixed: collective--based on collective 
management of labor and self-government in order to carry on 
economic and other activity not prohibited by law, and 
individual persons (about 40 people) able to take part in 
implementing the VEO's goals. In order to withdraw from the VEO 
the governing board must be notified in writing 2 months in 
advance. 
  The organizational structure: 
  When necessary the VEO creates cost accounting subdivisions 
and opens regional branches, offices, and centers operating 
within the limits of authority granted by Noosphere. VEO 
independently approves its staff and the staffs of regional 
centers, branches, offices, and other subdivisions without 
consideration of the norms and ratio of number of management 
employees and specialists. VEO members retain their legal and 
economic independence and operate on the basis of their own 
by-laws. 
  The highest body is the general assembly (conference). The 
supreme assembly (conference) issues decisions if three-quarters 
of its members are present. Its competence includes electing the 
governing board and the auditing commission as well as reviewing 
complaints against the actions of the chairman of the governing 
board and the chairman of the auditing commission of the VEO. 
  The governing board (eight people: the chairman of the 
governing board, the secretary and members of the governing 
board) provides overall leadership and monitoring of the work of 
its presidium and the board of directors of the VEO. The 
governing board is convened by its chairman when necessary, but 
at least three times a year. The chairman of the governing board 
and the general director of the VEO is S. A. Domashnev. 
  The presidium of the governing board coordinates the VEO's 
activity between sessions of the governing board. 
  The board of directors (the director and four deputies) is 
the VEO's executive and administrative organ. All operations 
involving terminating the VEO's activity are carried out by a 
liquidation commission. For the purpose of propaganda and 
dissemination of ecological and commercial information related 
to it, the Noosphere VEO press center carries on independent 
publishing activity. The director of the press center is the 
editor of the journal ZELENYY KREST, N. A. Kharitonenko. 
  Capital in rubles and foreign currency is compiled from the 
stock fees of VEO members--representatives of different ecology 
organizations, enterprises, and departments. 
  On 23-27 April 1990 a scientific seminar on problems of 
ecology was held in the city of Vladimir. Its organizers and 
sponsors were the VEO, the International Foundation for the 
Survival and Development of Humankind, the USSR Academy of 
Sciences VINITI [All-Union Institute of Scientific and Technical 
Information], and APN [Novosti Press Agency], among others. 
  Regional ecology centers have been created in Kursk, 
Cherepovets, Voronezh, Bashkiria, and the Far East. They are 
joined in cost accounting and work is done on contract. 
  The emblem (see drawing). The inscription: "Remember! Now it 
is not the inventor who is seeking a sponsor, but the Noosphere 
VEO which is seeking the inventor!" 
  Address: 103012, city of Moscow, ul. Varvarka, d. 3, room 
73, 
tel. 298-31-47, Sergey Arkadyevich Domashnev; contact tel. 
298-36-92, Nikolay Aleksandrovich Kharitonenko, A. F. Shashkova, 
reviewer and secretary of the governing board. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "To the Informals...," op. cit., p 
6; 
  -  VEO press release; 
  -  "What can 'Noosphere' Do?" VEO 
Information Leaflet; 
  -  VEO By-Laws. 

<H3>    United Trade Union of Ecologists ["Obyedennyy profsoyuz 
ekologov"] (OPE) </H3>
  This is an all-Union organization which besides purely trade 
union tasks "takes upon itself the resolution of ecological 
problems which are urgent but expensive for the state." 
  The OPE was created no later than March 1991 by 
representatives of 36 ecology organizations from different 
regions of the country; it joins together scientists and 
specialists of ecology organizations and representatives of the 
public who are doing nature protection activity. According to 
the organizers' assertion, on 18 April 1991 there were about 
10,000 members in the OPE. 
  Significant tax benefits are extended to enterprises which 
join the union. 
  The OPE's goal is "to consolidate efforts of everyone who 
considers defending nature and man from the negative 
consequences of production activity their task"; "to direct the 
force of laws on trade union activity toward resolving 
ecological tasks, since the right to clean air and clean water 
and hence to life itself is an inalienable social human right, 
while increasing the effectiveness of its activity is the 
ecologist's inalienable occupational right." 
  One of the OPE's tasks is to resolve issues of pension 
support, payment for sick time, and payment for drug expenses in 
a new way. 
  The chairman is V. I. Borzov. Rodina Commercial Bank r/s 
[current account] N 161366 Main Administration of RSFSR Gosbank 
[State Bank], Moscow, code 201791; United Coordinating Council 
of the Ecologists Trade Union, current account No 7005. 
  Address: 119034, city of Moscow, a/ya 486; tel. 280-05-20, 
478-46-73. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Gvozdev, L., "Another 'School'?" 
SPASENIYE No 3, March 1991, p 6; 
  -  Nikolayev, A., "The Ecologists 
Trade Union," ZELENYY MIR, No 15-16, 1991, p 10. 
<H5>  Greens Party ["Partiya zelenykh"] (PZ) </H5>
  This is a political party. Founded in March 1990 at the 
founding conference in Moscow. In 1990 the PZ was organized on 
the principles of complete autonomy of local organizations and 
basic democracy: adoption of decisions "from the bottom up," 
maximum prerogatives for the lower structures (general 
assemblies and local referendums); imperative mandate 
(delegation of powers by lower structures to their delegates in 
higher party organs); rotation. The PZ proposed to fight against 
totalitarianism, industrial expansion, and fascist tendencies 
and for expansion of the sphere of self-government. 
  Several factions existed in the PZ: ecosocialist 
(communitarian-anarchist), communal-socialist 
(syndicalist-anarchist), liberal-ecological, and patriotic. 
  The party has about 1,000 members and supporters. The 
social-occupational make-up includes: primarily youth (older 
secondary school students, college students, and others) and in 
some cities the scientific intelligentsia, creative workers, 
teachers, and the like. 
  The leaders of the PZ are V. Damye, A. Shubin, and A. 
Zheludkov (Moscow), S. Krivov (Samara), S. Fomichev (Nizhniy 
Novgorod), A. Kokryatskiy (Khmelnitskiy, Ukraine), and M. Shubin 
(Bryansk). 
  The press organ is the independent journal TRETIY PUT. 
  The first congress of the PZ was held on 9-10 June 1990 in 
Kuybyshev (Samara) at the premises of the branch of the Central 
Museum of V. I. Lenin. Participating in its work were 56 
delegates and more than 50 observers from 25 of the country's 
cities representing about 600 members. At the suggestion of the 
organizing committee the following questions were to be 
discussed: 
  1) adoption of PZ by-laws; 
  2) adoption of a PZ program; 
  3) election of PZ management organs. 
  Because of disagreements which arose no decisions were made 
on any of the points of the agenda. The PZ provisional governing 
board was elected as a compromise. The basic causes of the 
disagreements were contradictory views on the party's structure 
and political orientation. The Samara, part of the Moscow, the 
Western Ukrainian, and the Tatar organizations were at the stage 
of breaking relations with the structure being created. The 
management organ is the coordinators' council (19 people) headed 
by the provisional chairman A. Atnashev (Orenburg). 
  The second PZ congress which was supposed to perform those 
tasks which had not been resolved at the first congress was 
planned in Orenburg in late October 1990. But delegates from 
only five regional organizations came to work at the congress. 
In view of the lack of representation and previous 
disagreements, the congress was in fact broken off and defined 
as a work meeting of a number of regional PZ party 
organizations. As a result working resolutions which were in 
fact not distributed to the regional and primary PZ 
organizations were adopted. 
  In late 1990-early 1991 work was underway to organize new 
and 
register existing primary structures of the party, to finish 
work on program and charter documents, and to create an 
information agency, "Zelenaya Nit" [Green Thread]. Practical 
measures with ecology protection characteristics were organized 
primarily by local structures. 
  Some PZ organizations appeared as critics of the "500 Days" 
program and worked to create alternative groups of left-radical 
and left-socialist orientation, and certain PZ subdivisions 
participated in mass demonstrations of the Democratic Russia 
movement. 
  In May 1991 the PZ split into the Russian Greens Party (see 
article) and the Greens Parties League (see article). The split 
was caused by both ideological (attitude toward the market) and 
personal differences. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Funds 1, 2. 

<H5>    Rainbow ["Raduga"] </H5>
  This is an interregional youth organization. It appeared on 
28-30 October 1991 during a meeting of young activists of 
ecology organizations who were discussing the agenda of the 
intergovernmental conference in Brazil. 
  Favors increasing international cooperation in the cause of 
environmental protection and ecological education. Proposes to 
reject the use of atomic energy by developing alternative 
energy. Makes other traditional ecological demands as well. 
  Has a confederative structure. 
  Address: city of Moscow, MGU, Krotov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Council on Ecology Under the USSR Artists Union Governing </H5>

Board Commission on Ties With Creative Unions and Other Public 
Organizations ["Covet po ekologii pri Komissii po svyazi c 
tvoricheskimi soyuzami i drugimi obshchestvennymi 
organizatsiyami Pravleniya Soyuza khudozhnikov SSSR"] 
  It was founded on 30 October 1989 by decision of the 
secretariat of the USSR Artists Union presidium. The presidium 
secretary, Ivan Leonidovich Lubennikov, was approved as chairman. 
  In 1990 the exhibit "Artists for the Aral" was held. An 
International Ecological Exhibit in the Central Artists House is 
planned in the first quarter of 1992. The year 1991 was 
dedicated to preparing for the exhibit. 
  The size is 25 people, including Deputy of the USSR Supreme 
Soviet Viktor Dmitriyevich Sidorenko, the chairman of the 
Artists Union of the city of Kharkov, while the rest are 
Muscovites. 
  Address: 12109, city of Moscow, Gogolevskiy b-r., 10, USSR 
Artists Union Governing Board, tel. 291-29-65, Lyudmila 
Anatolyevna Konik, senior consultant. 
<H3>  Social-Ecological Council of Informals 
["Sotsialno-ekologicheskiy sovet neformalov"] </H3>
  It was founded in August 1987. It brings together ecological 
groups of Ryazan, Kuybyshev, Kharkov, Zaporozhye, and Krasnodar 
and other collective and several dozen individual members. The 
Krasnodar branch of the SESN is one of the initiators of the 
creation of the Kuban People's Front. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., p 134. 

<H3>    Social-Ecological Alliance ["Sotsialno-ekologicheskiy 
soyuz"] (SES or SoES) </H3>
  This is the largest informal association of ecology groups 
on 
the territory of the former USSR. Gathers and disseminates 
ecological information and develops ecological and political 
programs. Conducted several all-Union actions with the 
participation of up to a million people at one time, beginning 
in 1989. 
  The initiative group was formed on 6 August 1987 at the 
Third 
Conference of Student Nature Protection Squads in the Caucasus 
State Biosphere Preserve. 
  On 14 December 1988 the conference of the aktiv of ecology 
groups of Moscow and the Moscow Region made the decision to 
prepare to form the USSR Ecological Society and an organizing 
committee for conducting the founding conference was formed. 
  On 24-26 December 1988 the founding conference of the SoES 
took place in the Moscow Hunter and Fisherman's House and about 
150 groups from 90 of the country's cities participated. There 
the by-laws were adopted and the operational actions council, 
the editorial staff, and auditing commission were elected. 
  The SES by-laws were accepted for review by the presidium of 
the USSR Supreme Soviet on 10 February 1989. The Supreme Soviet, 
which referred to the 1930 USSR VTsIK [All-Russian Central 
Executive Committee] Decree on Public Organizations did not 
register the alliance (at least by the start of 1990). The SES 
does not have legal status or a bank account. The question of 
registration was postponed by the USSR Supreme Soviet until a 
Law on Public Organizations is adopted. 
  On 26-28 December the Second SoES Conference was held and 
representatives of 106 cities participated. 
  Members of the SES hold different views and convictions, but 
admission to membership in the alliance of the ecology division 
of Novosibirsk Pamyat at the Second Congress caused a protest 
among many members of the CES. 
  The organizational center is in Moscow. Primary, regional, 
and associated organizations are located in 111 cities of 8 
former Union republics. By 1 November 1989 it joined together 
112 organizations with a total aktiv of more than 3,000 people, 
as well as more than 200 individual members from 145 cities and 
populated points of 11 Union republics. In 1990 about 150 groups 
were in the alliance; they included 120 from the RSFSR. In 1991 
there were about 600 informal nature protection organizations. 
The largest of them were Delta (St. Petersburg), Green World 
(Astrakhan), the Kalmyk Steppe Association (Elista), Green Wave 
(Volgodonsk), the Surgut People's Ecological Society, the Altay 
Ecological Alliance, the Novosibirsk Initiative, the Ecology 
Committee (Tyumen), the Bashkir Branch of the SES, and others 
(see article). The SES coordinating and information center was 
already linked with more than 300 non-professional ecology 
associations in 260 cities and populated points of all the 
former Union republics even in 1989. Ties and cooperation are 
expanding. 
  Organizations and citizens are joined together in the CES on 
the principles of "self-organization, public self-government, 
and self-financing" with the "most complete, reliable, and 
effective information provided to all of its members" (from the 
CES by-laws). 
  The SES is an "association of organizations, associations, 
and citizens who, based on their own convictions, regularly 
participate in the work on nature protection, decontamination of 
the environment, or other activity focused on harmonizing the 
condition of the biosphere" (from the Decisions on the Formation 
of the SES). 
  The goal is to "unite intellectual potential, material and 
financial means, and the organizational possibilities of the 
alliance's members to preserve and restore the natural and 
cultural environment and to prevent destruction of natural and 
cultural treasures and human health" (SES by-laws). 
  The tasks are: 

  -  participation in resolving problems of protecting the 
plant and animal worlds, of agricultural, industrial, radiation, 
and other pollution, and of the construction and use of major 
sources of energy; 
  -  assistance to citizens and associations in 
nature protection activity; 
  -  propaganda of ecological 
knowledge. 

    The basic forms of activity are: 

  -  participation by SES specialists in conducting ecological 
expert studies of economic projects and administrative 
decisions; 
  -  development of alternative projects and 
technologies; 
  -  gathering and dissemination of ecological 
information; 
  -  organization of public monitoring of the condition 
of the environment, the population's health, and the quality of 
goods and of compliance with nature protection legislation; 
  -  organization of all-Union actions in defense of the 
environment; 
  -  advancement of initiatives, including legislative 
initiatives, in state and other organs; 
  -  participation in 
elections of different levels of people's deputies; 
  -  conduct of 
economic (including foreign economic) activity not prohibited by 
Soviet laws. 

    The first SES action was the submission of the unpublished 
draft CPSU Central Committee and USSR Council of Ministers 
decree "On Measures To Accelerate the Development of Hydropower 
Engineering in the USSR in 1990-2000" for national discussion. 
(The decree proposed building more than 90 large GES's on the 
rivers of Siberia, the Far East, and other regions with a 
sharply lessened role for expert studies). A large number of 
protest letters came to the CPSU Central Committee and as a 
result this decree was in fact not adopted. 
  The basic measures: 

  -  an all-Union protest action against construction of the 
Volga-Chogray Canal; activists of more than 100 cities 
participated in the action and more than a million signatures 
were gathered; 
  -  the "Katun" campaign: the fight against 
construction of the Katun GES, including organization of a 
summer protest camp on the Katun and development of alternative 
versions of development of Gornyy Altay; a special SES committee 
gathered information for state experts: comprehensive expert 
study of the project drew the conclusion that it was 
economically and ecologically unsound; 
  -  the Chernobyl Bell 
campaign; 
  -  conduct by SES member organizations from Kirishi, 
Tomsk, Volgograd, Kremenchug, and other cities of two 
scientific-practical conferences, mass collection of signatures, 
and other actions focused on stopping production of feed protein 
from petroleum paraffins (BVK); as a result the USSR Supreme 
Soviet adopted a decree to terminate production of BVK starting 
in 1991; 
  -  a campaign against construction in Tyumen Oblast of 
petrochemical complexes, including organization of mandates to 
people's deputies of the USSR, publication of appeals in the 
central press, and participation in the work of the USSR 
Goskompriroda expert commission; 
  -  participation of an SES 
working group in research involving the consequences of and 
prospects for USSR atomic power; 
  -  expeditionary work in sites of 
the habitat of the cheetah, which was considered extinct in the 
USSR; 
  -  participation of an SES working group together with USSR 
Supreme Soviet Ecology Committee in a study of the complex of 
problems of developing the preserve system in the USSR and doing 
questionnaire surveys of preserve collectives; processing of 
information collected; 
  -  information and organizational support 
of the production of individual and collective equipment for 
monitoring the quality of the environment and food products, 
including nitrate content in agricultural output; 
  -  with SES 
support 39 people were elected people's deputies of the USSR 
(including Aleksey Yablokov, Aleksey Kazannik, and Gennadiy 
Filshin) and 18 people were elected people's deputies of the 
RSFSR (including Viktor Revyakin and Valeriy Menshikov; today 
they are, respectively, chairman and deputy chairman of the 
RSFSR Supreme Soviet Committee on Questions of Ecology); there 
are also people supported by the SES among the people's deputies 
of Ukraine and Moldova; almost everywhere there is an SES 
branch, their representatives have become deputies of local 
soviets and members of ecology commissions; 
  -  implementation of 
the "Democratic Consolidation" program focused on combining the 
efforts of people's deputies of the USSR with Greens programs; 
  -  protest actions against including certain candidates guilty 
of 
following an anti-ecology policy in the make-up of the USSR 
Council of Ministers during discussion by the USSR Supreme 
Soviet of its new membership in 1989; 

    before 1990: 

  -  preparation and conduct of an all-Union campaign to 
declare a 5-year moratorium on construction of AES's and ATS's, 
as well as the proposal to develop provisions on the procedure 
for classifying rayons and populated points as ecological 
disaster regions (these SES proposals were rejected by the USSR 
Council of Ministers); 
  -  constant organizational and information 
support by the coordinating and information center (the former 
information center) of the work of USSR and RSFSR supreme 
soviets' committees on questions of ecology; 
  -  members of the SES 
council participated in preparing the text of the USSR Supreme 
Soviet Decree "On Emergency Measures To Normalize the Ecological 
Situation in the Country"; at the initiative of the SES the 
following points were included in the Draft Decree and 
adopted: 

    * termination of financing of building projects without a 
positive finding from an ecological expert study; 
  * termination of the production of BVK; 
  * termination of the practice of withdrawing group 1 forest 
land by decision of the executive power; 
  * formulation of provisions on economic incentive for 
enterprises doing ecologically useful activity; 

  -  conduct of the first historical-ecological expedition camp 
for secondary school students in the region of the city of 
Sviyazhsk on the Volga (before 1990) by the Green World Club 
(see article) and the KKhTI [Kazan Institute of Chemical 
Technology imeni S. M. Kirov] Nature Protection Squad (city of 
Kazan); 
  -  conclusion of a contract on the yearly publication of 
an anthology with the provisional name "Ekofakt" on the 
ecological situation in various regions of the country by 
Progress Publishing House; 
  -  April 1990: together with the U.S. 
Natural Resource Defense Council, conduct of an independent 
international expert study of the plan for creating in the city 
of Kaluga in Ivanovo-Frankovsk Oblast a Soviet-American 
enterprise for producing polyvinyl chloride and items made from 
it; as a result the American side recalled its documents and 
postponed conclusion of a contract; 
  -  an agreement in principle 
was reached with the Natural Resource Defense Council on a joint 
expert study of the ecological situation in Bashkiria; 
  -  in 
mid-1990 together with the DOP Movement (see article) and the 
Audubon Society (United States), a program of Soviet-American 
nongovernmental monitoring of acid rainfall was signed; 
  -  no 
later than November 1990 members of the "Ekomonitoring" 
department of the Social-Ecological Alliance completed two 
projects on ecological monitoring of the first phase of the 
Karakum Canal (10 films over the course of a year and one-half 
using data for the period from 1956 through 1989) and the Neva 
Inlet (1983-1989) and did some remote ecological research (the 
watershed of the Rybinsk Reservoir in 1987 and the forest fire 
zones in Tyumen Oblast in 1988); 
  -  in July-August 1991 an SES 
medical-biological expedition worked in Arkhangelsk Oblast in 
the White Sea basin where the year before a catastrophic 
destruction of marine animals had been observed; 
  -  in March 1991 
in Khimki (Moscow Region) a Soviet-American conference of 
nongovernmental ecology organizations was conducted with the 
participation of about 100 Soviet and 50 American 
representatives of Greens organizations; the problems discussed 
at the conference became the SES's areas of activity; they 
include the preserve system and ecologization of agriculture, 
nature protection laws and law and global problems of ecology, 
radiation safety and alternative energy, clean technologies, 
independent monitoring, ecological education and the creation of 
a unified computer network, relations between official and 
nongovernmental nature protection associations, and joint 
ecology projects; a joint statement was adopted. 

    Membership in the SES is individual or collective. 
Organizations and citizens register as candidates for membership 
after submitting group and individual applications to the 
coordinating and information center and become actual members at 
SES conferences by a two-thirds vote of the delegates present. 
Organizations and citizens may expel members and candidates for 
membership in the SES by the same two-thirds vote. SES members 
(individual and collective) have the right to participate in 
conferences with full voting rights. Dual membership is allowed 
in the SES: some DOP's which are members of the DOP Movement as 
well as organizations of Greens parties are simultaneously 
collective members of the SES. 
  In early 1991 there were more than 150 collective members 
and 
organizations numbering about 15,000 people in the SES. 
  The highest SES body is the conference convened by the SES 
operational actions council in accordance with the decision of 
the previous conference or on the demand of at least one-third 
of the collective members of the SES, but at least once a year. 
The conference elects and recalls members of the membership 
organs (including members of the operational actions council, 
the director of the coordinating and information center, and the 
editor in chief of the press organ), ratifies the work plan for 
the year for the elected organs, handles admission to membership 
in the SES and expels members from it, and ratifies proposals on 
legislative initiatives. The conference's decisions are adopted 
by a simple majority vote. 
  The operational actions council works on behalf of the SES 
in 
the period between conferences, advances legislative initiatives 
on the SES's behalf, "elects people's deputies of the USSR," 
provides monitoring of the activity of the coordinating and 
information center in registering SES branches, opens accounts 
in USSR banking institutions, organizes international contacts 
on the SES's behalf, and so forth. The council's decisions are 
made on a collective basis and are valid if more than half of 
all the SES members voted for them. 
  The coordinating and information center is an enterprise 
created by the operational actions council and works on an 
independent balance. The center "collects essential information, 
offers it to interested persons and organizations, and forms 
working groups to resolve particular issues and problems." 
  SES branches may be created by at least three SES members 
and 
are registered by the operational actions council. SES branches 
are independent in resolving their own internal issues, 
including determining their structure and highest bodies and 
areas and forms of work, and are also on independent balances. 
  The following are sources of financing: 

  -  cash receipts from state enterprises, institutions, 
organizations, cooperatives, and other legal persons and from 
foreign and international organizations and individual citizens; 
  -  income from measures conducted on the SES's behalf; 
  -  income 
from SES economic activity. 

    The SES established contact with the European Greens Parties 
Headquarters and cooperates with the U.S. Natural Resource 
Defense Council and the Audubon Society (United States), the 
Greens and Antinuclear Movement in the FRG (a contract on 
interaction until 1990 was concluded with the last two), and 
other Western European and American ecology organizations. 
Jointly with the Soviet branch of Greenpeace (see article), the 
SES works on the "Western Siberia" program, which includes an 
expert study of the activity of joint ventures of the region's 
petroleum and gas chemical complex. At the all-Europe meeting of 
the international Friends of the Earth organization (before 
1990), the SES delegation proposed a program of cooperation of 
national and international nongovernmental ecology organizations 
in the areas of monitoring the condition of the environment, 
developing and introducing various ecological technologies and 
producing the corresponding equipment, and training specialists. 
  The SES did not immediately include a point on a moratorium 
on construction of atomic power plants in its program and thus 
alienated the domestic antinuclear movement. 
  In 1990 through the efforts of the SES the directory 
"Sotsialno-ekologicheskiy soyuz. Informatsionno-metodicheskoye 
pismo" [Social-Ecological Alliance. An Information-Methodology 
Letter] was published. In 1991 the directory "Vsya nasha zhizn. 
Vestnik socialno-ekologicheskogo soyuza" [All Our Life. Bulletin 
of the Social-Ecological Alliance] came out. The editor in chief 
was Ye. Golovina (Moscow, "Master," 6 printers sheets, print 
run--3,000 copies each in Russian and in English). Since 
November 1988 information letters of the ecology movement have 
been periodically published (more than 10 issues). 
  The SES has its own emblem approved at the conference. 
  SES leader S. Zabelin is an assistant to the president of 
Russia's advisor on ecology, Academician A. Yablokov. 
  In 1992 the SES plans joint actions to institute court 
proceedings against enterprises which violate ecological laws. 
<H5>  The Social-Ecological Alliance in April 1992 </H5>
<H5>  Russia </H5>
  1. Aleksin--Greens Association ["Assotsiatsiya zelenykh"] 
  2. Apatity--public ecology committee 
  3. Apatity--"Ekonord" Ecology Center 
  4. Arkhangelsk--Ecology of the North ["Ekologiya severa"] 
Association 
  5. Astrakhan--Green World ["Zelenyy mir"] Association 
  6. Barnaul--Altay Ecological Alliance 
  7. Berezhniki--Ecology and Health ["Ekologiya i zdorovye"] 
  8. Bryansk--Apogee ["Apogey"] Concern 
  9. Bryansk Oblast--Bryansk Woods ["Bryanskiy les"] Preserve 
  10. Vladivostok--the maritime society of technical ecology 
  11. Volgograd--Ecology ["Ekologiya"] Club 
  12. Volgograd--Noosphere ["Noosfera"] 
  13. Volokolamsk--Dignity ["Dostoinstvo"] 
  14. Voronezh--Ecological Initiative ["Ekologicheskaya 
initsiativa"] 
  15. Glazov--Ecological Alliance 
  16. Groznyy--Ecological Alliance 
  17. Dzerzhinsk--TRETIY PUT journal 
  18. Dimitrovgrad--the city committee on ecological problems 
  19. Dubna--SoES branch 
  20. Yekaterinburg--Ecology Information ["EkoInfo"] 
  21. Zvenigorod--Forest Defense Committee 
  22. Ivanovo--oblast ecological society 
  23. Izhevsk--ecological alliance 
  24. Yoshkar-Ola--SoES branch 
  25. Kazan--Green World ["Zelenyy mir"] Ecology Club 
  26. Kazan--KKhTI Nature Protection Squad 
  27. Kaluga--Ecology Center 
  28. Kamensk-Uralskiy--ecology committee of the society of 
specialists in regional studies 
  29. Kemerovo--Committee To Save the Tom River ["Komitet 
spaseniya Tomi"] 
  30. Kirishi--6th VOOP Section 
  31. Kondopoga--Sandalwood Tree ["Sandal"] Greens Alliance 
  32. Krasnodar--Kuban People's Academy 
  33. Krasnodar--Ecological Cordon ["Ekokordon"] 
  34. Krasnodar--Magnitude ["Magnituda"] Cooperative 
Geophysical Expedition 
  35. Krasnoyarsk--Green World ["Zelenyy mir"] 
  36. Lipetsk--Ecologist ["Ekolog"] Club 
  37. Maykop--ecosection of the Citizen ["Grazhdanin"] Club 
  38. Moscow--editorial office of the journal EKOS 
  39. Moscow--EKOGANG 
  40. Moscow--Center for Independent Ecology Programs 
  41. Moscow--MOSKh [Moscow Branch of the RSFSR Artists Union] 
Ecology Section 
  42. Moscow--ecosection of the Association of Soviet 
Esperanto-ists 
  43. Moscow--Nature Protection Group of the MGU School of 
Geography 
  44. Moscow--Energy 2050 ["Energiya 2050"] Club 
  45. Moscow--Agroresources ["Agroresursy"] 
  46. Moscow--Moscow River ["Moskva reka"] Society 
  47. Moscow--Noosphere ["Noosfera"] Children's Ecology 
Station 
  48. Moscow--SoES division 
  49. Moscow--Biotest 
  50. Murmansk--ecosection of the Citizens Initiative 
["Grazhdanskaya initsiativa"] Club 
  51. village of Nepetsino in Moscow Oblast--Nature Defense 
League 
  52. Nizhniy Novgorod--NGU [Nizhniy Novgorod State 
University] 
Nature Protection Squad 
  53. Nizhniy Novgorod--Green Shore ["Zelenyy bereg"] 
  54. Nizhniy Novgorod--Dodobird ["Dront"] Ecocenter 
  55. Nizhniy Novgorod-ecosection of the Nizhniy Novgorod 
Branch of the Journalists Union 
  56. Nizhniy Novgorod--Green World ["Zelenyy mir"] 
Association 
  57. Nizhniy Novgorod--Kitavras [translation unknown] 
Cultural-Ecological Association 
  58. Nizhniy Novgorod--Landscape-Ecology Section of the 
Nizhniy Novgorod Branch of the Architects Union 
  59. Nizhniy Tagil--Purification ["Ochishcheniye"] Club 
  60. Novgorod--Ecology ["Ekologiya"] Club 
  61. Novokuybyshevsk--Resonance ["Rezonans"] EPK [Expert 
Verification Commission] 
  62. Novosibirsk--ecosection of the Pamyat [Memory] IPO 
[Historical-Patriotic Association] 
  63. Novosibirsk--Novosibirsk Initiative ["Initsiativa"] 
Ecology Council 
  64. Norilsk--Ecology and Man ["Ekologiya i chelovek"] 
  65. Obninsk--Noosphere "Protva" [translation unknown] 
Committee 
  66. Omsk--Green City ["Zelenyy gorod"] Association 
  67. village of Orshanka, Mariy-El--SoES branch 
  68. Ostashkov--SoES branch 
  69. Penza--Ecology Club 
  70. Pervouralsk--Chance ["Shans"] Ecology Club 
  71. Perm--SoES branch 
  72. Petrozavodsk--Our Common Future ["Nashe obshcheye 
budushcheye"] Center 
  73. Petropavlovsk--Kamchatka "Ekomor" Scientific Production 
Association 
  74. Petropavlovsk--Kamchatka Alternative ["Alternativa"] 
Group 
  75. Protvino--SoES branch 
  76. Pskov--Greens Movement ["Zelenoye dvizheniye"] 
  77. Pudozh in the Karelian Republic--Forest ["Les"] 
  78. Rostov-na-Donu--public ecology center 
  79. settlement of Roshchino in the Maritime Kray--ecology 
group 
  80. Ryazan--Nature Protection Squad 
  81. Samara--oblast regional lore laboratory school 
  82. Samara--oblast SoES branch 
  83. St. Petersburg--Ecological Developments Bureau 
  84. St. Petersburg--Karelia ["Kareliya"] Travelers' Club 
  85. St. Petersburg--"Delta" Ecology Association 
  86. St. Petersburg--In Defense of the Natural World ["V 
zashchitu mira prirody"] Ecology Club 
  87. Sayanogorsk--Green World ["Zelenyy mir"] 
  88. Sergiyev Posad--ecology society 
  89. settlement of Smirnykh in Sakhalin Oblast--initiative 
ecogroup 
  90. Smolensk--EKO/Orbis children's ecology club 
  91. Sosnovyy Bor--Green World ["Zelenyy mir"] Association 
  92. Sterlitamak 2--Ecology and Health ["Ekologiya i 
zdorovye"] 
  93. Surgut--Surgut Public Ecology Society 
  94. Syktyvkar--Syktyvkar Social-Ecological Alliance 
  95. [misnumbered here on in text] Tomsk--Ecological 
Initiative ["Ekologicheskaya initsiativa"] 
  96. Troitsk in Moscow Oblast--SoES branch 
  97. Tuapse--Public Committee for Ecological Control and 
Assistance 
  98. Tula--For Survival ["Za vyzhivaniye"] City Ecology 
Organization 
  99. Tula--oblast youth ecology alliance 
  100. Tyumen--Ecology Association 
  101. village of Uvat in Tyumen Oblast--Ecology ["Ekologiya"] 
Public Association 
  102. Ulyanovsk--SoES branch 
  103. Ufa--Ecology, Health, and Life ["Ekologiya, zdorovye i 
zhizn"] Society 
  104. Ufa--SoES branch 
  105. Ufa--Bashkiria Nature Protection Squad 
  106. Cheboksary (Novocheboksarsk)--Exotica ["Ekzotika"] MP 
[possibly medical station] 
  107. Cheboksary--SoES branch 
  108. Chelyabinsk--Nuclear Safety ["Yadernaya bezopasnost"] 
Movement 
  109. Chelyabinsk--oblast Greens association 
  110. Chernogolovka in Moscow Oblast--Ecologist ["Ekolog"] 
Society 
  111. Yuzhno-Sakhalinsk--"Fauna" MNIP [possibly medical 
scientific survey station] 
  112. Yaroslavl--Green Branch ["Zelenaya vetv"] Ecology Club 
  113. Yartsevo--"EKOS" Ecology Group 
<H5>  Belarus </H5>
  114. Minsk--Belarusian "Chernobyl" Social-Ecological Club 
<H5>  Moldova </H5>
  115. Chisinau--KGPI [Chisinau State Pedagogical Institute] 
Greens Squad 
  116. Chisinau--"Altair" Agency 
  117. village of Novyye Aneny--Dniester ["Dnestr"] 
Interrepublic Committee 
<H5>  Ukraine </H5>
  118. Voznesensk--Green World ["Zelenyy mir"] 
  119. Yenakiyevo--ecology foundation 
  120. Zaporozhye--children and adolescents ecology club 
  121. Kiev--Salvation ["Spaseniye"] 
  122. Kramatorsk--Apogee ["Apogey"] Cooperative 
  123. Lenino, Crimea--Hot August ["Zharkiy avgust"] 
  124. Mariupol--Committee To Save the Azov Sea 
  125. Nikolayev--Green World ["Zeleniy svit"] branch 
  126. Odessa--SoES branch 
  127. Rakhov--"Karpaty" [Carpathians] Ecology Group 
  128. Sumy--Green World branch 
  129. Ternopol--Green Planet ["Zelena planeta"] 
  130. Feodosiya--Ecology and the World ["Ekologiya i mir"] 
  131. Kharkov--SoES branch 
  132. Kharkov--Ecocenter Ecoorganization of School Students 
and Youth 
<H5>  Azerbaijan </H5>
  133. Baku--Greens Movement of Azerbaijan 
<H5>  Armenia </H5>
  134. Yerevan--SoES branch at the State Engineering 
University 
of Armenia 
<H5>  Georgia </H5>
  135. Tbilisi--SoES branch in Georgia 
<H5>  Kazakhstan </H5>
  136. Almaty--Initiative ["Initsiativa"] Social-Ecological 
Association 
  137. Dzhambul--Greens Movement ["Zelenoye dvizheniye"] 
  138. Leninogorsk--Noosphere ["Noosfera"] Ecoclub 
  139. Pavlodar--Ecology and Public Opinion ["Ekologiya i 
obshchestvenoye mneniye"] 
  140. Uralsk--Eureka Scientific Apprentice Society of 
Regional 
Studies 
<H5>  Turkmenistan </H5>
  141. Tashauz--Resource ["Resurs"] Scientific-Production 
Center 
  142. Tashauz--Ecology Association 
<H5>  Uzbekistan </H5>

  143. Nukus--Alliance for Defense of the Aral and the Amu 
Darya 
  144. Tashkent--Ecologist ["Ekolog"] Club 
  145. Fergana--For a Clean Fergana ["Za chistuyu Ferganu"] 
<H5>  Tajikistan </H5>
  146. Dushanbe--SoES branch 
  Address: 125319, city of Moscow, ul. Krasnoarmeyskaya, d. 
25, 
kv. 85, tel. 151-62-70, Svyatoslav Igoryevich Zabelin--director 
of the coordinating and information center; 121019, city of 
Moscow, a/ya 211; (home) tel. 298-51-85; 290-08-09 (home), 
Mariya Cherkasova, director of the independent ecological 
programs center 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "One More Bridge," ZELENYY 
MIR, No 11-12, 1991, p 1; 
  -  Zabelin, S. I., "People 'Who Are Not 
Indifferent' Are Strong Not Because of the Organization But 
Because of Spiritual Unity," SPASENIYE, No 3, 1991, p 3; 
  -  "Zelenyyy v SSSR. Krupneyshiye...," op. cit., pp 7-9; 
  -  Galkina, 
L., op. cit., p 34; 
  -  "To the Informals...," op. cit., SPASENIYE, 
March 1991, p 2; 
  -  "A 'Russian Aerospace Center'?" ZELENYY MIR, 
No 15, 1990, p 6; 
  -  "Rossiya: partii...," op. cit., p 83. 

<H3>    Let Us Save the World and Nature ["Spasem mir i prirodu"] 
Association </H3>
  The association's plans includes programs: "Model City" (for 
small cities of Russia which are suffering from aggressive 
industry) and "Interconversion" (social retraining of Soviet 
military personnel discharged into the reserve and others). At 
the association's plenum held in late 1990 expeditions were 
planned, social and ecological programs were adopted, and the 
concept of creating an international assistance network for 
countries which by the forces of the elements are in an 
emergency situation was reviewed. One of the main tasks of this 
network is monitoring. (According to UNESCO data, 43 percent of 
the aid given to Armenia did not reach its destination). 
  In 1990 the association conducted a Soviet-American 
expedition sailing from New York to Leningrad. Yachtsmen's 
expeditions preceded the week-long peace march around the United 
States. One of the participants in the expedition made a film 
which was shown formally in the Oktyabr Hall of the House of 
Unions in Moscow. 
  The association is a member of the preparations committee of 
the 1992 UN conference in Brazil CED-92 [Conference on the 
Environment and Development--92]. Within the framework of 
preparations for the conference, national public hearings on 
problems of the environment and development of the ECO-92 Forum 
were held in Moscow on 6-8 July 1992. Participating in them were 
representatives of the Soviet and world community interested in 
resolving ecological problems. Among the organizations of the 
Forum were the Soviet Nongovernmental CED-92 Preparations 
Committee, the Geneva "For Our Common Future" Center, and the 
International CED-92 Assistance Committee. 
  The association is the main organizer of the youth part of 
the Forum-92 program. On the first day of the hearings devoted 
to young ecologists, the question of the lack of teaching aids 
for ecological disciplines was raised, although the RSFSR 
Ministry of Education announced a competition of authors' 
programs to compile such a textbook. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Klimovskaya, Yu., And Let Our 
Great-Grandchildren Live," ZELENYY MIR, No 23-24, 1991, p 1; 
  -  ibid., "Toward a Direct, Open Dialogue," ZELENYY MIR, No 
31-32, 
1991, p 3; 
  -  ibid., "We Are All in the Same Boat," ZELENYY MIR, 
No 1-2, 1991, p 7. 

<H5>    SPASENIYE [Salvation] </H5>
  This is a weekly ecology newspaper. Published since February 
1991. 
  The cofounders were USSR Minprirody [Ministry of Nature], 
the 
Business World consortium, and the newspaper's journalist 
collective. 
  The editor in chief is Vitaliy Chelyshev. 
  Printed in offset at the printing house of the Pressa 
Publishing House. Eight pages in newspaper format. 
  Address: 103473, city of Moscow, 2-oy Volkonskiy per., d. 8, 
tel. 281-71-84, 971-18-98. 
<H5>  Rainbow Keepers ("Khraniteli radugi") </H5>
  The goal is to protect the environment. The forms of work 
are 
organization and conduct of rallies, attacks, picketing, and 
appeals to managers of industrial enterprises and 
representatives of organs of power. 
  Size unknown. Participated in the picketing of the plant to 
destroy chemical weapons in Chapayevsk (August-September 1989), 
the Balakovo AES, and the Gorki AEST. 
  In June 1991 they attacked the vivarium of the Sechenova 
Hospital and released the animals imprisoned there. Eighteen 
months of scientific research were ruined and damages totaled 
R2,500. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galkina, L., op. cit., p 25. 

<H3>    Ecological Perspective ["Ekologicheskaya perspektiva"], 
Committee of the USSR Alliance of Scientific and Engineering 
Societies ["Komitet Soyuza nauchnykh i inzhenernykh obshchestv 
SSSR"] </H3>
  The goal is to coordinate work on inventing ecologically 
clean technologies and putting them into production. 
  The chairman of the committee is Nikita Nikolayevich 
Moiseyev, academician and advisor at the USSR Academy of 
Sciences presidium. The committee's learned secretary is 
Nadezhda Vladimirovna Ilyinskaya. 
  Address: 119034, city of Moscow, Kursovoy per., d. 17, tel. 
291-68-21. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "To the Informals...," op. cit., p 
6. 

<H5>    Ecology Competition ["Ekologicheskiy konkurs"] </H5>
  This is an all-Union organization. 
  Formed in 1990. The goal was to make the USSR ecologically 
healthy. 
  Activities: collection of information on new developments in 
the field of ecology, conduct of expert studies, ecological 
projects, technologies, and other things and their submission 
for competition, and assistance in introducing them. 
  The first competition took place in Kemerovo on 17-24 
November 1991. The founders were the SKZM [Soviet Peace Defense 
Committee], the Molodaya gvardiya Publishing House, the USSR 
Supreme Soviet human ecology subcommittee, and the editorial 
offices of the journals PUT K USPEKHU and TEKHNIKA MOLODEZHI. 
The leader is Vledislav Khristoforovich Ksionzhek, the editor of 
the science department of the journal TEKHNIKA MOLODEZHI and 
editor in chief of the journal PUT K USPEKHU. 
  EK is creating a joint venture, "Inter-EKO." 
  Address: 121019, city of Moscow, Arbatskiy per., d. 6/2, kv. 
31, editorial official of the journal PUT K USPEKHU, tel. 
291-50-00; 125012, city of Moscow, ul. Novodmitrovskaya, d. 5a, 
tel. 285-89-80. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    USSR Ecology Foundation ["Ekologicheskiy Fond SSSR"] </H5>

(EKOFOND) 
  This has been in existence since April 1989. Registered in 
April 1991. 
  Has the following programs: 

  -  "rendering of material assistance to victims of ecological 
disasters and to volunteers for restoring native nature, 
development of universal ecological education, and revival of 
the public movement to save the environment; 
  -  conduct of 
independent ecological expert studies; 
  -  creation of no-waste and 
low-waste technologies, new instruments, assemblies, equipment, 
and other technical devices, including electric cars; 
  -  cultivation of ecologically clean agricultural products; 
  -  defense of particular sections of nature from encroachments 
of 
industry through the creation of nature-history parks, and other 
things; 
  -  international programs of defense of nature; programs 
of the Soviet branch of the World Information Center and the 
Ecological Inventions Foundation; 
  -  creation of films, 
newspapers, and journals, organization of conferences, seminars, 
and symposiums on the most acute problems of ecology, and 
cultural-ecological programs." 

    Provides financial assistance to victims of accidents and 
natural disasters. Participates without charge in financing 
ecology programs (including research in the field of promising 
ecological technologies) offered to the foundation by citizens, 
organizations, and enterprises. The capital attracted to the 
Ekofond for special purposes is used only for the development of 
the particular program. 
  In March 1990 jointly with the newspaper ZA RUBEZHOM, the 
Ekofond conducted a competition for the best ecological act. Of 
the 650 works proposed, 5 were declared best. Taking the 
opinions of the newspaper's readers into consideration, the 
prize of R10,000 was awarded to a doctor of medical sciences and 
director of the Rodniki Tuberculosis Prevention Clinic in 
Ivanovo Oblast, A. A. Saleyev. 
  On 4-5 June jointly with the Oktyabrskiy Rayon Committee of 
the CPSU and the board of directors of youth programs under the 
All-Union Komsomol Central Committee, the Ekofond organized a 
number of charitable concerts in Moscow which were dedicated to 
World Environment Day. The USSR Ekofond decided to transfer the 
full amount collected to Oktyabrskiy Rayon in the city of Moscow 
as one of the most ecologically polluted. 
  In 1992 schools, kindergartens, and palaces of pioneers and 
school children in the rayons of Belarus who suffered as a 
result of the Chernobyl catastrophe, as well as those in rayons 
of Karakalpakia and Kazakhstan which make up the Aral Ecological 
Disaster Zone, will receive the newspaper ZELENYY MIR at the 
foundation's expense. 
  The foundation has branches in almost all Union republics 
and 
four branches in the Russian Federation (the Oks Regional 
Branch, the Ural Branch, the Chelybinsk Branch, and the Northern 
Caucasus Branch). 
  Together with the Russian Ecological Academy in Leningrad 
became the initiator of the creation of the Russian Ecology 
Foundation (see article), whose founding assembly occurred on 31 
May 1991. 
  The Ekofond is the cofounder of the Veterinary Society in 
the 
USSR and the Anti-Nicotine Foundation. 
  Cooperates with the International "Vita Longa" Association, 
the World Information Center, and the Ecological Inventions 
Foundation. 
  The management organ is the expert council. About 100 
enterprises and cost accounting organizations have become 
collective members of the foundation. 
  Current account No 706801 in the Transactions Office at USSR 
Zhilsotsbank, Moscow, MFO [possibly Interbranch Turnover] 
299093; hard currency account No 70600002 in USSR 
Vneshekonombank [Foreign Economic Bank], Moscow. 
  Address: 117313, city of Moscow, Leninskiy pr., d. 87, kom. 
272, tel. 134-63-62, Fedor Fedorovich Metlitskiy, deputy 
chairman of the governing board; tel. 203-90-67, Eduard 
Vladimirovich Girusov, cochairman of the foundation's governing 
board, head of the philosophy division of the USSR Academy of 
Sciences, and professor. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "At the Expense of the USSR 
Ecology Foundation," ZELENYY MIR, No 31-32, 1991, p 2; 
  -  "The 
USSR Ecology Foundation," ZELENYY MIR, No 17-18, 1991, p 10; 
  -  "To the Informals...," op. cit., p 6; 
  -  "Jazz Helps the 
Capital," ZELENYY MIR, No 4, 1990, p 3; 
  -  "Man With a Shovel," 
ZELENYY MIR, No 6, 1991, pp 14-15. 

<H3>    USSR Ecological Alliance ["Ekologicheskiy soyuz SSSR"] 
(EKOSOYUZ, ES) </H3>
  "A self-governed independent nongovernmental public 
organization which carries on its activity in accordance with 
the USSR Constitution and laws of the country and its Union 
republics, as well as... the by-laws" (Ekosoyuz By-Laws, 1.1). 
  Created at the founding conference in Moscow on 24 December 
1988. Founders: USSR Geographic Society, the USSR Ecology 
Foundation, and the "Algoritm" [Algorithm] Youth 
Scientific-Technical Creativity Center. 
  Ekosoyuz operates on the territory of the USSR. Its 
organizational center is in Moscow. 
  The goal is to "achieve ecological security and the 
prosperity of the USSR and the world and harmony between man and 
nature" (By-Laws, 21). 
  The tasks are to monitor the condition of the environment 
and 
compliance with nature protection legislation, to conduct 
ecological-social-economic expert studies of existing and newly 
created installations; to form an "ecology market"--a knowledge 
market, to develop alternative, "clean" technologies and 
technical devices, to help enterprises create low-waste 
technologies, to produce various types of monitoring devices; to 
create "ecological enterprises, consortiums, and joint stock 
companies which will make the problems of our planet's difficult 
issues the basis of their activity; to create a network of 
scientific centers; and to shape public opinion. 
  The basic forms of activity are: 

  -  organization of scientific developments related to the 
study of the ecological situation in the USSR and the solution 
of particular ecological problems; 
  -  advisory-coordinating 
assistance in conducting practical measures in the field of 
ecology; 
  -  participation along with other public organizations in 
conducting expert studies of economic installations; 
  -  organization and conduct of regional, all-Union, and 
international conferences, symposiums, and the like on ecology 
issues; 
  -  ecological education and propaganda of ecological 
knowledge. 

    In 1989 the USSR Ekofond along with the newspaper ZA 
RUBEZHOM 
organized an ecological competition and along with the 
AUCCTU--an ecological exhibit at USSR VDNKh [Exhibit of the 
Achievements of the National Economy]; the Central Television 
broadcast "Ecological Expedition in the Moscow Region" began. 
Representatives of the ES participated in conducting a number of 
ecological expert studies and conferences. Together with SSOD 
[Union of Soviet Friendship Societies and Cultural Ties With 
Foreign Countries] they organized and conducted a meeting of the 
Soviet public and deputies of the FRG Bundestag on the topic 
"FRG Policy in the Area of Environmental Protection." In late 
1990 the Ekosoyuz created a scientific-production and commercial 
association of ecologically oriented enterprises and 
organizations, the Nature Use Federation ["Federatsiya 
Prirodopolzovaniya"]. 
  Before April 1991 Ekosoyuz had received a state license for 
a 
trademark of ecological quality, the "White Lotus" (the symbol 
of the ES). The mark will be awarded after a public expert study 
(independent occupational collectives will conduct it) to goods, 
devices, and technologies, which will provide enterprises and 
associations with an advantage in commerce, including abroad. 
  No later than April 1991 the ES published a brochure 
"Methodology of Scientific (Ecological-Social-Economic) Expert 
Study of Projects and Economic Undertakings." 
  Within the framework of Russia's Open University (ROU), a 
department of theoretical ecology headed by the president of 
Ekosoyuz was created in the college of natural sciences and 
mathematics. 
  USSR ES was one of the founders of the Russian Ecological 
Alliance no later than April 1991. 
  In the spring of 1991 the ES, together with MITKhT [Moscow 
Institute of Fine Chemical Technology] and ROU, founded the 
Moscow Ecology Center. 
  There are another seven republic and a multitude of regional 
branches in the USSR ES in addition to the Russian ES. 
  Membership in the ES is collective. The exception is people 
with the title "Honorary Member of the USSR Ecological 
Alliance." It is nominal and does not afford any legal rights as 
an ES member. Soviet and foreign societies and associations and 
labor collectives with organizational and financial independence 
may be members of the ES. To join the ES an organization (or 
labor collective) must send a written application, select its 
representative to the ES Council, and establish the amount of 
the organization's annual membership dues which it can afford, 
and if desired pay an initiation fee. The ES is a confederation 
of its collective members and branches operating independently. 
  The highest management organ is the conference, which makes 
amendments and additions to the by-laws, determines the 
directions of work of the ES, and elects the Ekosoyuz council 
bureau. All decisions are made by a majority vote. Regular 
conferences are convened by the ES council at least once every 5 
years. 
  The Ekosoyuz council, as a rule convened once a year, 
coordinates the ES work in the intervals between conferences. It 
includes representatives of all members of the ES. The number of 
members in the council is not restricted. 
  The ES secretariat (5 people on staff), who are hired to 
work 
and paid under existing norms, perform ongoing work. 
  The main source of financing is voluntary and mandatory 
deductions of members and support of interested international 
and Soviet foundations. 
  Because of the USSR ES's close connection with state 
departments, the largest nongovernmental ecology organizations 
refrain from active cooperation with it. At the same time, 
however, some ES activists are members of the coordinating 
council of the Moscow Ecological Federation (see article). 
  Current account No 608459 Transactions Office under the 
governing board of USSR Zhilsotsbank MFO 299093. 
  Address: 117418, city of Moscow, ul. Krasikova, 32, USSR 
Academy of Sciences TsEMI [Central Economic-Mathematical 
Institute], Ekosoyuz SSSR; tel. 129-11-22; 117049, city of 
Moscow, ul. Dmitrova, d. 38a; tel. 238-34-78 (secretariat). 
Chairman of the ES council bureau--Nikolay Fedorovich Reymers: 
336-38-39 (home); 129-11-22, 238-34-78 (work). Deputy 
chairman--Aleksandr Leonidovich Nikonov: 457-43-68 (home); 
238-34-55 (work). ES members: Anatoliy Ivanovich Kadukin, USSR 
Academy of Sciences Institute of Water Problems, deputy of the 
Moscow Soviet, and member of the coordinating council of the 
Moscow Ecological Federation (see article), city of Moscow, tel. 
208-31-65 (work); Yuriy Yakovlevich Korotkikh, deputy of the 
Moscow Soviet and member of the coordinating council of the 
Moscow Ecological Federation, city of Moscow, tel. 449-92-15 
(work); Leonid Vasilyevich Korablev, pensioner, docent, 
candidate of philosophical sciences, and member of the 
coordinating council of the Moscow Ecological Federation, city 
of Moscow, tel. 132-20-90 (home); Leonid Alekseyevich Pets, head 
engineer, nuclear physics, and member of the coordinating 
council of the Moscow Ecological Federation, city of Moscow, 
tel. 462-06-76 (work). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "To the Informals...," op. cit., p 
2; 
  -  Reymers, N. "The USSR Ecological Alliance," ZELENYY MIR, No 
15-16, 1991, p 10; 
  -  "Cooperate! Appeal of the Governing Board of 
the USSR Ecological Alliance," ZELENYY MIR, No 15-16, 1991, p 
10; 
  -  Khmara, I. "The 'White Lotus," the Mark of Quality," 
ZELENYY MIR, No 5-6, 1991, p 4. 

<H5>    Ecology and Peace ["Ekologiya i mir"], Soviet Association </H5>
  According to the by-laws, it is an all-Union public 
organization which operates in accordance with the constitutions 
of the USSR and the Union republics; and provides independent 
public expert study of the most dangerous nature-transforming 
projects and formulation of new ecological concepts of the 
development of the country and its individual regions. 
  The founders were the Soviet Peace Foundation and the Soviet 
Peace Defense Committee [SKZM]. The Ecology and Peace 
Association was created in June 1987 under the SKZM. Its core 
was made up of public affairs commentators and scientists who in 
1983-1986 had done a comprehensive independent expert study of 
plans for reversing part of the flow of northern and Siberian 
rivers, the results of which served as scientific grounds for 
the adoption in August 1986 of the CPSU Central Committee and 
USSR Council of Ministers Decree "On Terminating Work To Reverse 
Northern and Siberian Rivers." With the association's 
participation other similar projects were rejected 
("Volga-Chogray," "Volga-Don-2," "Danube-Dnepr," and others). 
  On 23 January 1989 the founding assembly transformed the 
"EiM" Association under the SKZM into an independent public 
organization the SA "EiM." The by-laws were ratified and the 
governing board and its chairman, Sergey Pavlovich Zalygin 
(writer, editor in chief of the journal NOVYY MIR, and a 
people's deputy of the USSR), were elected. 
  Members of the governing board include academicians of the 
USSR Academy of Sciences and VASKhNIL [All-Union Academy of 
Agricultural Sciences imeni V. I. Lenin] A. L. Yanshin, G. S. 
Golitsyn, A. A. Dorodnitsyn, B. S. Sokolov, N. A. Shilo, V. A. 
Tikhonov, A. S. Monin, and A. V. Yablokov. Five of the members 
of the governing board are people's deputies of the USSR. 
  The goals are: 

  -  to shape ecological public consciousness focused on 
preserving peace and natural treasures and the ecological 
balance on the Earth; 
  -  to help unite the public ecology movement 
on the basis of new ecological thinking; 
  -  to increase the level 
of ecological substantiation of national economic 
decisions. 

    Forms of activity are: scientific-research, expert study, 
methodological and advisory, and lecture and propaganda 
activity. The EiM participates in electing deputies to all 
levels of soviets. 
  The basic results of the nature protection activity are: 

  -  together with other ecology organizations, expert studies 
were done of the most ecologically dangerous water management 
projects: the Volga-Chogray, Volga-Don, Danube-Dnepr canals, the 
Bashkir (Ishtuganovskiy) Reservoir, the Leningrad Dike, and 
others and the public was notified of the results; 
  -  with the 
assistance of "EiM" the journals NOVYY MIR and PAMIR conducted 
an expedition to the ecological catastrophe region in the Aral 
basin in the fall of 1988 (see NOVYY MIR, No 5, 1989); 
  -  on 22-23 
November 1989 "EiM" and the Soviet Peace Foundation conducted 
the First All-Union EiM Conference on the topic "Ecology and 
Agriculture" with the participation of delegations from the 
United States and the FRG; 
  -  in 1990 the program "Agroecology" 
was developed; it was an expert ecological-economic evaluation 
of the condition of the agroindustrial complex and its economic 
mechanism and the ecological consequences of contemporary land 
use and animal husbandry. The results were published in the 
anthology "Ecology and Agriculture"; 
  -  no later than 7 February 
1991 the association held a press conference for Soviet and 
foreign journalists, "Ecological catastrophes in the USSR: 
Facts, Causes, and Consequences," devoted to three major 
ecological catastrophes which had occurred in the last 2-3 
decades and were getting worse at that time (the Aral Basin, the 
Lower Volga and Caspian Region, and the Neva Inlet and the Gulf 
of Finland); a professional evaluation of the ecological 
situation given by scientists and members of the association and 
the identification of the socioeconomic causes of ecological 
catastrophes were a contribution to the preparatory process for 
the UN conference on the "Environment and Development" (Brazil, 
1992). 

    On 26 March 1992 they participated in discussing the 
possibility of producing ecologically clean food products on 
Russia's territory in Moscow at the House of Scientists 
(ministers and scientists took part in the discussion). 
  Membership is individual and collective. Collective members 
operate on the basis of their by-laws and the EiM by-laws. The 
criterion for membership is compliance of activity with the EiM 
by-laws. 
  The highest management organ is the conference, which is 
convened at least once every 2 years (the conference is valid if 
at least half the members of the EiM participate). Decisions are 
made by a simple majority vote. The conference elects the 
governing board and the auditing commission; adopts decisions on 
the areas and forms of work of the EiM; and adopts and amends 
the by-laws. 
  The governing board manages the work of the EiM in the 
periods between conferences, elects the chairman and his 
deputies, the secretaries, and the members of the governing 
board bureau from its members, and makes decisions on admission 
into membership and expulsion from the EiM. The governing 
board's decisions are made by a majority of the governing 
board's members. 
  The governing board bureau represents the EiM in all state, 
cooperative, public, and other organizations in the USSR and 
abroad, provides operational management of the association's 
activity, and formulates special-purpose programs of activity of 
the EiM. Decisions are adopted by a majority vote. 
  The chairman of the governing board and his deputies and the 
secretaries open and close accounts in banks on behalf of the 
EiM and sign official documents which support the activity of 
the EiM. 
  Sources of financing are: voluntary contributions, revenue 
from the State Budget (there is the USSR Decree on Extension of 
the Force of the 19 February 1988 USSR Council of Ministers 
Decree No 240 'On Improving the Conditions of Activity of the 
SSOD, Soviet Committees, the SO KK and the Communist Party of 
the USSR, and the SFM' to the SA EiM) and founding 
organizations, and membership dues. 
  Address: USSR, 103031, city of Moscow, ul. Kuznetskiy most, 
19, tel. 926-04-64; 209-57-02, chairman S. P. Zalygin; 231-51-79 
(home), 234-16-02 (work), deputy chairman N.A. Shilo. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Bitter Truths," ZELENYY MIR, No 
5-6, 1991, p 4; 
  -  "To the Informals...," op. cit., p 2; 
  -  Novikov, 
A., "So Just Where Are We Going?" KRESTYANSKIYE VEDOMOSTI, No 15 
(62), 7-13 April 1992, p 11. 

<H3>    ENIO, All-Union Association of Applied Eniology ["ENIO," 
Vsesoyuznaya assotsiatsiya prikladnoy eniologii"] (VA "ENIO") </H3>
  The founding congress was held on 17 November 1988. 
  The tasks were to unite the most highly qualified 
specialists 
in the field of eniology, to create favorable conditions for 
them to work creatively, and to defend their creative, social, 
and other interests. "The association must become an attractive 
milieu for professional interaction and the inception and 
competition of new ideas" and "must teach its specialists great 
responsibility for progressiveness and the ecological security 
of the scientific-technical decisions being made" (Resolution of 
the founding congress). 
  The forms of work are: creation of temporary labor 
collectives and NTTs [scientific-technical centers] (on a 
competitive basis); and administrative and technological 
planning. 
  The management organ is the congress; at the congress the 
collegium and the central auditing commission are elected for a 
term of 5 years. The commission meets at least twice a year. 
  The president of the ENIO Association is F. R. Khantseverov. 
  Address: city of Moscow, tel. 927-33-14, Firom Rakhimovich 
Khantseverov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    REPUBLIC AND LOCAL ORGANIZATIONS </H5>

<H5>  Azerbaijan </H5>
<H5>  Azeri Nature Protection Society </H5>
  It organizes ecological education and studies public 
opinion. 
Cooperates with nature protection societies of other republics 
(see article). 
  Address: 370116, city of Baku, 7-y mkrn., ul. Akhundova, d. 
5, tel. 61-71-40. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "To the Informals...," op. cit., 
No 4, April 1991, p 4. 

<H5>    Greens Movement of Azerbaijan </H5>
  It appeared in September 1989 on the base of the Independent 
Ecology Club. The founding conference occurred on 6 May 1990. 
Registered. Coordinating council--40 people, governing board--9, 
and council of elders--10 people. Twenty-five topical 
commissions. 
  The goal is to combine efforts to resolve the republic's 
ecological problems. 
  Together with the Greens of Georgia organized an ecological 
expedition to the Kura River; conducts ecological research and 
produces films and printed material. Participant in the First 
International Conference on Problems of the Caspian Sea (Baku, 
13-17 June 1991), which brought together scientists and 
specialists in the field of ecology and managers of state nature 
protection organizations and public ecology formations. 
  Is a member of the National Congress and the "Democratic 
Azerbaijan" Bloc and supports the initiative "The Caucasus Is 
Our Common Home" (an attempt to unite the ecology movements of 
the Caucasus). 
  Address: 370000, city of Baku, ul. Gadzhibekova, d. 16, kv. 
2, tel. 93-05-36, Ismail Rustamov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  MOLODEZH AZERBAYDZHANA, 23 May 
1991, p 1. 

<H5>    City of Baku </H5>
<H5>  Ecology Club </H5>
  This is a city organization. The club was founded in 1989. 
Conducts debates and organizes planting activities in the city. 
Speaks out against industrial pollution. 
  Address: 370005, city of Baku, u. Zevina, d. 4. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Sumgait </H5>

<H5>  Sumgait City Ecological Society </H5>
  The society produces films and printed material. 
Participates 
in resolving problems of protecting the plant and animal worlds, 
preserving biological diversity, and preserving and developing 
the network of nature territories and objects under special 
protection; and problems related to industrial pollution and the 
construction and operation of hydraulic engineering structures. 
  Address: 373200, city of Sumgait, 3-y kvartal, d. 23a, korp. 
5, kv. 49, tels 3-69-19, Taryan Ya. Sheydayev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Armenia </H5>

<H5>  Armenian Nature Protection Society </H5>
  The society organizes ecological education and the study of 
public opinion. Cooperates with nature protection societies of 
other republics (see article). 
  Address: 375010, city of Yerevan, ul. K. Marksa, d. 16, tel. 
58-11-61. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "To the Informals...," op. cit., 
No 4, April 1991, p 4. 

  - 
<H5>  "Goyabaykar" (Fight To Survive) </H5>
  This is an ecology group. Appeared in 1987. Supports 
shutting 
down the Oktemberyan AES. On 17 February 1988 the group held a 
demonstration against chemical plants in the city of Abovyan. On 
20 December 1989 began picketing the Nairit Chemical Combine in 
the city of Yerevan. The picketing ended in June 1990 with the 
closing of the combine. The leader of Goyabaykar, Kh. 
Stamboltsyan, went on a hunger strike in support of the people 
of Narodnyy Karabakh. 
  Is a member of the Armenian Liberation Movement. Social 
make-up: teachers, pensioners, high-school students, 
journalists, workers, and others. 
  Address: 375033, Yerevan, ul. Gaydara, d. 18, kv. 51, tel. 
22-57-40, Khachik Stamboltsyan; 375033, Yerevan, ul. Komitasa, 
d.3, kv. 45, V. R. Kalashyan. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2. 
  -  Galkina, L., op. cit., p 27. 

<H5>    "Goyatevum" (Rebirth), Alliance </H5>
  This is an ecological-cultural organization. Tasks: to 
protect monuments of culture and nature. 
  Address: 375018, Yerevan-18, p. Ostemberyana, d. 31, kv. 
152, 
S. A. Karakhanyan. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2. 
  -  "To the Informals...," op. cit., 
No 4, April 1991, p 4. 

<H5>    Greens Movement of Armenia </H5>
  The Greens Movement coordinating council organizes work. 
Among the members of the council are A. V. Grigoryan, candidate 
of physical and mathematical sciences, docent of the Yerevan 
State University school of geography, and laboratory chief. 
  Address: city of Yerevan, YeRGU school of geography, Ashot 
Vageyevich Grigoryan. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Alliance of Armenia </H5>

  It emerged in October 1989. Collects and disseminates 
ecological information. Managed to stop work on expanding the 
GRES in Rozdan. 
  Address: city of Yerevan, tel. 28-16-22. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Yerevan </H5>

<H5>  Ecology Search, Club, City of Yerevan </H5>
  Engages in ecological education and development of new 
"clean" technologies. Cooperates with the Aboyan Ecology Search 
Club (see article). 
  Address: 375018, city of Yerevan, pr. Oktembryana, d. 31, 
kv. 
152, tel. 57-74-76, Smbat Aleksanovich Karakhanyan. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Movement (Ecomovement} </H5>

  Part of the Greens Movement. Chairman of Ecomovement is A. 
V. 
Grigoryan and secretary is A. G. Gabrielyan. 
  Address: 375101, city of Yerevan, Avan-Duryan-3, d. 45, kv. 
1, Ashot Vageyevich Grigoryan, Asmik Grachayevna Gabrielyan; 
375114, city of Yerevan, Yugo-zapadnyy massiv, B-2, d. 21, kv. 
23, Grant Kyarimovich Sarkisyan. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Abovyan </H5>

<H5>  Ecology Search, Ecoclub </H5>
  Formed under the Komsomol of Abovyanskiy Rayon. Cooperates 
with the Yerevan Ecology Search Club (see article). 
  Address: 378510, city of Abovyan, pl. Barekamutyan, Komsomol 
raykom, tel. 204-34, Anush Avetovna Gevoryan. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Belarus </H5>

<H5>  "Belaya Rus" [White Russia], Youth Ecology Movement </H5>
  Sponsor of the movement is the Matena Minsk City 
Scientific-Technical Youth Creativity Center. In 1990 the Matena 
Center financed a trip by a group of Belarusian school children 
to an ecology camp in the FRG. 
  Address: 220016, city of Minsk, ul. K. Marksa, d. 40, tel. 
29-39-70; 211412, city of Polotsk, ul. imeni 6-oy Armii, d. 9, 
kv. 83, tel. 329-87, Andrey Vladimirovich Ignatovich. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Matena--Sponsor of 'Belaya Rus,'" 
ZELENYY MIR, No 7-8, 1991, p 4; 
  -  "To the Informals...," op. 
cit., No 8, August 1991, p 6. 

<H5>    Belarusian Republic Chernobyl Committee </H5>
  In early 1991 together with representatives of the Russian 
and Ukrainian republic Chernobyl committees (the territory of 
republics which suffered most after the explosion of the 
reactor) took part in a conference at the USSR Commission on 
UNESCO Matters. At the conference the draft program of 
assistance in cleaning up the consequences of the Chernobyl 
accident was discussed. The program presupposes the 
participation of scientists and employees of state departments 
and the community. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Klimovskaya, Yu., "With UNESCO's 
Help," ZELENYY MIR, No 3-4, 1991, p 5. 

<H3>    Belarusian Council of the Ecology International of the Green 
Cross and the Green Crescent </H3>
  This is a nongovernmental, noncommercial organization 
striving to prevent global ecological crisis. 
  On 7 February 1991 the conference of public initiative 
groups 
was held to create the "Belarusian Council of the Ecology 
International." At this conference an organizing committee was 
formed and in early May it appeared on the pages of the 
newspaper ZELENYY MIR with an appeal to convene the founding 
conference of the Belarusian Council. The conference took place 
on 25 May 1991 in Minsk. Participating in it were 
representatives of various organizations and creative unions. 
  Organizing Committee address: city of Minsk, "Dom Druzhby," 
tel. 45-31-53. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Appeal of the Organizing 
Committee To Create the `Belarusian Council of the Ecology 
International of the Green Cross and the Green Crescent' to 
State, Scientific, Educational, and Public Organizations and 
Creative Unions and to All Citizens of the Republic," ZELENYY 
MIR, No 17-18, 1991, p 5. 

<H5>    Belarusian Ecological Alliance (BES) </H5>
  This is a nonpolitical organization. Its task is make the 
population active in order to resolve the crisis ecological 
situation and "put an end to the destruction of natural, 
spiritual, and moral values and people's health as the basis of 
the nation's well-being." 
  The alliance was formed on 1 June and approved by the BSSR 
Supreme Soviet presidium on 24 August 1989. Among the founders 
of the BES were the Belarusian Peace Defense Committee, the BSSR 
Writers, Architects, and Artists unions, the BSSR Ministry of 
Health Institute of Radiation Medicine, and others. 
  Forms of work are: organization in the republic of a mass 
ecology movement able to perform practical tasks; formation 
among citizens of a contemporary ecological worldview; support 
and creation of cooperative cost accounting enterprises in the 
field of ecology; creation of special purpose funds of the BS 
and its own bank of ecological information; advertising and 
publishing activity; submission of proposals to resolve 
particular ecological problems to the Supreme Soviet and the 
Government; and approval of awards and prizes for active work in 
nature protection activity. 
  In 1989 the BES participated in creating a governmental 
program to clean up the consequences in Belarus of the accident 
at the Chernobyl AES. At its insistence a number of points 
focused on the general cleanup of the ecological situation of 
regions which had suffered were included in the program. 
  In April 1991 together with the musical ecology movement 
"Clean Water Rock" (see article) the BES conducted a charitable 
event dedicated to the fifth anniversary of the catastrophe at 
the Chernobyl AES. Artists of Belarus and other USSR republics 
and from abroad held several concert rallies in some of the 
republic's cities. The slogan was "Today life on earth depends 
on you!" 
  The social base of the BES is primarily scientific workers 
and VUZ instructors. 
  Membership is individual and collective. Persons at least 16 
years of age who participate in the BES's work, recognize the 
by-laws, and pay membership dues may become members of the 
alliance; dues include an initiation fee of 1 ruble and an 
annual fee of 1 ruble. Children under 16 years of age 
participate in BES work as corresponding members without paying 
membership dues. 
  BES members have the right to participate in all spheres of 
the alliance's activity and elect and be elected to BES 
management organs; to receive the necessary assistance in the 
alliance's management organs in order to perform the goals and 
tasks envisioned by the by-laws; and to obtain a BES 
identification card and chest badge of the established model. 
  A BES member is obligated to: comply with the by-laws; 
participate in BES activity; "by personal example affirm a 
stewardly attitude toward nature" and nurture great ecological 
sophistication aand morality in himself"; and pay dues. 
  With substantial scientific and practical experience in 
nature protection activity, one can become a BES expert, and 
this is certified by an appropriate document. Experts are 
approved by the governing board; expert groups are formed and 
they give lectures and reports on the BES's behalf. 
  The president of the BES is B. P. Savitskiy and the vice 
presidents are L. G. Tarasenko, Ye. P. Petryayev, and R. G. 
Garetskiy. 
  The alliance's structure: Individual members of the BES may 
create a primary organization (at least 5 people), the 
structural basis of the BES. Primary organizations are combined 
into regional divisions which have the rights of a legal person. 
The council elected at the regional conference manages the 
regional division's work. The supreme organ of the BES is the 
republic congress (called at least once every 3 years). An 
extraordinary congress is assembled at the demand of one-third 
the BES members or two-thirds of the members of the BES 
governing board. A BES conference is convened every year. In the 
period between congresses and conferences the governing board 
and its presidium manage the alliance's work. The BES president 
bears responsibility for all types of alliance activity, obeys 
the congress, provides overall leadership of the BES and the 
governing board, and manages BES credits. 
  Sources of income of the BES are individual and collective 
membership dues, cost accounting activity of cooperatives, and 
donations. 
  Addresses: 246699, city of Gomel, ul. Sovetskaya, d. 104, 
Gomel State University, school of biology, tel. 56-75-61 (work), 
56-22-02 (home), Boris Parfenovich Savitskiy; 220030, city of 
Minsk, ul. Lenina, d. 15a; city of Minsk, tel. 39-46-61 (work), 
Leonid Grigoryevich Tarasenko; city of Minsk, tel. 56-14-03 
(work), Yevgeniy Petrovich Petryayev; city of Minsk, tel. 
64-53-15 (work), 34-45-81 (home), Radim Gavrilovich Garetskiy. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "To the Informals...," op. cit., 
No 4, April 1991, p 4; 
  -  EKOLOGICHESKAYA GAZETA, No 4-5, 1991, p 
8; 
  -  BES by-laws. 

<H5>    Belarusian Greens Movement (BZD) </H5>
  The coordinating council organizes the movement's work. Part 
of the Greens Movement operating on the territory of the former 
USSR (see article). 
  Address: 220030, Minsk, Sergey Vladimirovich Dorozhko; 
222823, Pukhovichskiy Rayon, pos. Svisloch, ul. Stroiteley, d. 
1, kv. 89, Nikolay Nikolayevich Chernevich; Dmitriy V. Gunich; 
city of Brest, Aleksey Danilovich Stepulenok, member of the BES 
coordinating council. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Movement To Create the Ecology Party of Belarus (Movement To </H5>

Create the Greens Party of Belarus) 
  It appeared in 1990. The aktiv is 60 people. The 
organization 
has organizing committees in Minsk, Gomel, Brest, Bobruysk, 
Baranovichi, and Kobrin. The founding congress of the ecology 
party (see article) prepared a draft party program in which the 
term "ecology" is treated as encompassing all aspects of human 
life, including economics, politics, and culture. 
  Part of the All-Union Greens Movement (see article). 
  Address: city of Minsk, tel. 71-38-58, Anatoliy Baranovskiy; 
city of Kobrin, Tel. 2-53-08, Vladimir Satsevich. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. 
Krupneyshiye...," op. cit., p 25. 

<H5>    For the Children of Chernobyl </H5>
  This is a Belarusian charitable foundation. Began its 
activity in May 1990. Registered at the BSSR Ministry of Justice 
on 20 November 1990 as a public organization. 
  There are no paid staff employees in the foundation. The 
tasks are: providing material, medical, social, and other aid 
and organizing the treatment, improvement of health, and 
recreation of children living on Belarus's territory and 
suffering as a result of the accident at the Chernobyl AES. 
  From June 1990 through the summer of 1991, the foundation 
sent 11,092 children from regions of the contaminated zone 
abroad to improve their health, and 526 children from Mogilev 
Oblast were sent to sanatoriums and resort bases of Belarus, 
Russia, and the Black Sea Coast. Together with FRG organizations 
a base for year-round improvement of the health of Chernobyl 
children is being created in Vitebsk Oblast. Forty-nine children 
with serious chronic diseases were sent for treatment, 
consultation, and study to clinics of Italy and the FRG along 
with their mothers. 
  The foundation has received more than 300 tonnes of 
charitable humanitarian aid for children who suffered as a 
result of the accident at Chernobyl since the summer of 1991. In 
addition 190 tonnes of charitable aid for the population of 
Brest, Gomel, Mogilev, and Minsk oblasts came through Minsk. 
  The foundation organized on-the-job training for medical 
personnel at foreign clinics. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    "Znich," Belarusian P. M. Masherov Alliance for Aid to </H5>

Victims of the Chernobyl Accident 
  "Znich" is the "holy fire by which ancestors were protected 
from the force of evil." 
  Tasks are: to send donations to people who suffered in the 
Chernobyl accident; and to invest capital in developing science 
and medicine. The alliance proposes to establish an 
international prize named for Masherov (Petr Mironovich 
Masherov) for especially outstanding achievements. 
  Sources of financing: collection of donations. In April 1990 
the alliance distributed an appeal through the mass information 
media to the heads of states and governments, international 
organizations, and citizens to make donations to help those who 
suffered from the accident at Chernobyl. 
  Accounts: No 700947 at the Republic Belzhilsotsbank, MFO 
400019; No 933431142 to the BSSR OPERU, Vneshekonombank SSSR MFO 
805153. 
  Address: 220611, city of Minsk, pr. Masherova, d. 21, tel. 
29-35-30, 23-64-58, 20-80-57. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Appeal of the 'Znich' Belarusian 
P. M. Masherov Alliance for Aid to Victims of the Chernobyl 
Accident," MOLODEZH AZERBAYDZHANA, 16 May 1991, p 3. 

<H5>    "Clean Water Rock," Musical Ecology Movement </H5>
  Gives concerts performing musical works on ecological 
topics. 
In April 1991 together with the Belarusian Ecological Alliance 
(see article) conducted the action "Clean Water Rock--Chernobyl 
91." 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  EKOLOGICHESKAYA GAZETA, No 2-3, 
1991, p 6. 

<H5>    Brest Oblast Ecodefense Foundation </H5>
  Speaks out against industrial pollution. Organizes 
ecological 
education. 
  Address: city of Brest, tel. 1-33-29 (home) Vladislav 
Arkadyevich Surskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Chernobyl, Belarusian Social-Ecological Movement </H5>

  Founded in March 1990 and 6 months later registered by the 
BSSR Ministry of Justice. 
  Programs: 

  -  construction of the Center for Radiation Safety and 
Ecological Defense of Man and the Environment, a unified complex 
to work on study of the environment and its impact on man in the 
past, present, and future as well as on rehabilitation and 
prevention of harmful consequences plus establishment of 
radiation monitoring; 
  -  introduction of a method of biological 
dosimetry and to do this opening of the Ekogen Enterprise with 
share participation of several institutes and collection of 
capital, including foreign currency; 
  -  in the next 2 years 
building of a sanatorium-type hospital for mothers and babies; 
  -  creation of an interrepublic newspaper to cover events in the 
contamination zone (Belarus, Russia, and Ukraine). 

    Activities include: 

  -  in April 1990 the alliance conducted an interrepublic 
scientific-practical conference "Chernobyl--Socioeconomic and 
Moral-Ethical Aspects"; 
  -  in the summer of the same year together 
with scientists from Kiev and Kharkhov the possibilities, ways, 
and means of removing radionuclides from soil, food products, 
and the human organism were examined at the conference. 

    The alliance founded the social-ecological interrepublic 
newspaper NABAT [Toxin]. The editor in chief is Vasil Yakovenko. 
  Has publications. Member of the Social-Ecological Alliance 
(see article). Part of the Chernobyl Alliance All-Union 
Volunteer Association (see article). 
  Address: 220000, city of Minsk, pr. IZVESTIYA, d. 17, kv. 
172, tel. 71-58-19, Vasiliy Timofeyevich Yakovenko, writer and 
leader of the ecology section of the BSSR Writers Union. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "To the Informals...," op. cit., 
No 8, August 1991, p 6. 

<H5>    Ecology Party of Belarus </H5>
  (See article: "Movement To Create the Ecology Party of 
Belarus.") Representatives of the Ecology Party of Belarus 
became members of the Humanist Party founded in St. Petersburg 
in July 1990. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, p 91. 

<H5>    Ecological Alliance of Belarus (Ekosoyuz) </H5>
  Founders were: Writers Union, Architects Union, BSSR Academy 
of Sciences, and Belarus State University. Preparations for 
creating the Ecological Alliance of Belarus began in early March 
1989. 
  The founding conference took place on 3 April. At the 
conference an organizing committee consisting of 40 people and 
the chairman, writer V. T. Yakovenko, were elected. 
  The first congress took place in Minsk on 1-2 July 1989. The 
520 delegates from 55 cities of Belarus adopted the program and 
the by-laws and elected the governing board (from 80 
representatives of 18 regional branches), the president, 
Professor of Gomel University Boris Savitskiy (he soon became a 
people's deputy of Belarus, member of the presidium of the 
Supreme Soviet, and chairman of the Supreme Soviet Ecology 
Commission), and three vice presidents. By early 1990 the 
alliance united more than 10,000 people. 
  Tasks are: creation of economic structures to realize 
ecological projects, ecological education and indoctrination of 
the population, and other things. The alliance participated in 
the election campaign for republic and local organs of power. 
Six participants in the alliance became people's deputies of 
Belarus. 
  Address: 220000, Minsk, tel. 39-46-61 (home), 22-60-01, 
22-87-96 (home), Lyavon Tarasenko, alliance vice president. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. 
Krupneyshiye...," op. cit., p 26. 

<H5>    City of Minsk </H5>
<H5>  "Murlyka" [Purr] KLK [expansion unknown] Club </H5>
  Goal--to defend domestic animals. 
  Address: 220052, city of Minsk, ul. Kuybysheva, d. 101, kv. 
13, tel. 32-58-25 (home), Andrey Katok. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    "Oykos" Travel Club in Defense of Treasures of Culture and </H5>

Nature 
  "Oykos" or "ekos" (Greek) means a habitat, dwelling, a home. 
  Unites the creative and scientific intelligentsia. Goal is 
to 
"form space for productive intellectual interaction." 
  The club's activity is closed in character and only for 
highly intellectual people. New ideas and projects which appear 
in the club are applied in practice. 
  There are 25 individual and 11 collective members. The 
chairman is the candidate of philosophical sciences Aleksandr 
Likhodiyevskiy. 
  Address: city of Minsk, tel. 27-14-32. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Avdeyev, I., "'Oykos'--A Club for 
Creative People" (Interview with A. Likhodiyevskiy), ZNAMYA 
YUNOSTI, Minsk, 3 August 1991, pp 2, 4. 

<H5>    "Ranitsa," Group </H5>
  Ecology organization. Part of the Belarusian Greens Movement 
(see article) and the Ecoclub of the city of Minsk (see article). 
  Address: 220007, city of Minsk, ul. Zhukovskogo, d. 9, korp. 
2, kv. 39, Yevgeniy Georgiyevich Terekhov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    "Talaka" </H5>

  This is a sociopolitical club. Appeared in the spring of 
1988. Worked on sociopolitical, cultural, historical, and 
ecological problems. Leaders, students of Belarus State 
University in 1988 were: S. Vitushka, A. Shusha (later editor of 
the newspaper NOVINY BNF), and V. Ivashkevich. Spoke out in 
defense of the environment and the historical structures of the 
city of Minsk. Participated in rallies. After the formation of 
the BNF [Belarusian People's Front] the political aktiv 
continued to work in this organization, but the club 
concentrated on cultural-educational and ecological issues. 
  Address: 220000, city of Minsk, tel. 66-58-87 (home), Viktor 
Ivashkevich; tel. 22-01-31 (home), 39-48-34 (work), Ales Susha; 
tel. 78-78-98, Sergey Vitushka. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecoclub </H5>

  Formed under the Komsomol Central Committee. Organizes 
events 
to plant greenery in the city. Engages in ecological education 
and conducts debates. 
  Address: 220030, city of Minsk, Vladimir Vladimirovich 
Koltunov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Brest Oblast </H5>

<H5>  City of Kobrin </H5>
<H5>  Health Improvement ["Ozdorovleniye"], Ecoclub </H5>
  Propagandizes a healthy way of life and organizes ecological 
education. 
  Address: Brest Oblast, city of Kobrin, tel. 24308 (home), 
Vladimir Aleksandrovich Satsevich. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Village of Yatvez (Baranovichskiy Rayon) </H5>

<H5>  Spruce, Group </H5>
  Works on protecting forests. 
  Address: 225361, Brest Oblast, Baranovichskiy Rayon, village 
of Yatvez, p/o Podleseyki, d. 67, Yuriy Georgiyevich Tarabesh. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    Vitebsk Oblast </H5>
<H5>  City of Novopolotsk </H5>
<H5>  OSEP </H5>
  Ecology organization. Involved in ecological education. 
  Address: 211440, Vitebsk Oblast, city of Novopolotsk, tel. 
2-35-66 (home), Anatoliy Mikhaylovich Moiseyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    "Sakavik" (March) </H5>

  Ecological national-cultural society. Formed in summer of 
1988 on the base of the "Maladik" group. Goals are to protect 
nature, restore monuments, and revive the Belarusian language. 
Oriented to the Minsk "Talaka" organization (see article). 
Supports the People's Front of Belarus. 
  Ten members and 25-30 sympathizers: youth, primarily 
workers. 
  Participated in organizing the rallies of 18 March (3,000 
people), 5 June (6,000 people), and November 1988 (1,000 people). 
  Address: 211440, Vitebsk Oblast, city of Novopolotsk, ul. 
Kalinina, d. 15, kv. 120, tel. 5-08-45, Serzhuk Anatolyevich 
Sokolov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Gomel Oblast </H5>

<H5>  City of Gomel </H5>
<H5>  Gomel Oblast Ecological Alliance (GOES) </H5>
  Part of the Belarusian Ecological Alliance (see article). 
Opposes industrial pollution of the environment and studies 
questions of nuclear contamination. 
  Address: city of Gomel, tel. 52-56-72, Valentin Viktorovich 
Kharitonov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Star Peace, Center </H5>

  Gomel ecology organization. Holds debates and lectures on 
philosophical and ecological themes. 
  Address: 246045, city of Gomel, ul. Sviridova, d. 1, korp. 
2, 
kv. 161, tel. 51-70-16 (home), Igor Valeryevich Ardashnikov; 
246015, city of Gomel, pos. Budenovskiy, d. 17. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Green Leaf </H5>

  Gomel ecology organization. Holds events to plant greenery 
in 
the city. Participates in resolving problems related to 
industrial pollution. 
  Address: city of Gomel, tel. 55-24-50, Mikhail Yuryevich 
Sorin. 
<H5>  Polesye Ecology Movement, Initiative Group </H5>
  Opposes industrial pollution of the environment and supports 
development of preserve zones. 
  Address: city of Gomel, tel. 52-62-41, Viktor Vasilyevich 
Toropyno. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Grodno Oblast </H5>

<H5>  Settlement of Subochi (Volkovskiy Rayon) </H5>
  Viola Ecological Problem Center 
  Its task is to ensure the population's ecological security. 
Member of the Social-Ecological Alliance (see article). 
  Address: 231907, Grodno Oblast, Volkovskiy Rayon, pos. 
Subochi, d. 15, kv. 6, Valentin N. Matveychuk. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Mogilev Oblast </H5>

<H5>  City of Mogilev </H5>
<H5>  Noosphere Ecology Committee </H5>
  Organizes ecological education: conducts debates and 
lectures. 
  Address: 212029, city of Mogilev, tel. 418660 (home), 
Valentina Vladimirovna Vorobyeva. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Georgia </H5>

<H5>  Georgian Ecological Association </H5>
  Organizes ecological education and the study of public 
opinion. Participates in resolving problems related to 
industrial and agricultural pollution. Deputy chairman of the 
association is G. I. Tarkhan-Mouravi. 
  Address: 380008, Georgia, city of Tbilisi-8, a/ya 25; 
380012, 
city of Tbilisi, Levaya Naberezhnaya, d. 4, kv. 23, tel. 
34-72-63, Georgiy Ivanovich Tarkhan-Mouravi. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2 
  -  "To the Informals..." op. cit., No 
8, August 1991, p 6. 

<H5>    Greens Movement of Georgia </H5>
  Formally organized by April 1988. Joins together about 5,000 
people of various social strata; they are writers, 
cinematographers, workers, peasants, students, and academy 
members. There are 11 regional and more than 80 primary 
organizations in the movement. 
  The GNG was first headed by corresponding member of the 
Georgian Academy of Sciences, Professor Grigol Tumanishvili. 
Formally the movement was called the Ecological Association 
under the All-Georgian Rustaveli Society (the EA is part of the 
People's Front of Georgia and cooperates with the National 
Movement of Georgia). 
  On 10-13 December 1989 the first GMG conference was held. At 
the conference the movement's new structure was approved--the 
council of cochairmen (Rezo Khuntsariya, Marika Darchiya, and 
Nana Nemsadze) and the executive council (Zurab Zhvaniya, 
Kvandzhi Maniya--press secretary, and Levan Mamaladze--learned 
secretary); and a comprehensive program of activity developed 
specially for the conference was examined: it was made up of 
draft ecological legislation and a political, economic, social, 
and ecological program of actions. 
  The movement's philosophy is: "Nature is our master. That is 
what our ancestors believed, and they treated Mother Nature 
correspondingly. To resurrect our ancient culture of human 
society's relationship with the environment, return the ancient 
attitude and moral interpretation of the world to the people, 
and awaken a sense of stewardship and a sense of participation 
and responsibility in each person is the immediate and paramount 
task." 
  Activity includes protest actions against: harmful emissions 
of industrial enterprises into the sea, rivers, and air; mining 
of ore by open-pit mining, poisoning of food products by 
chemical fertilizers, cutting of the forests in the mountains of 
Georgia, in particular Svanetia, and unlimited livestock grazing 
as a threat to alpine meadows. 
  The results of the activity were: in the fall of 1988 the 
construction of the Caucasus Pass Railroad (R80 million had 
already been spent and the total cost of the project was R1.5 
billion) was stopped; the construction of the Khudonskiy Arched 
High Dam was stopped (R200 million was spent and the total cost 
was R0.6 billion; the plan for a series of earthfill dikes on 
the Enguri River was rejected; construction of a reservoir in 
Kakhetia was frozen (about R100 million was spent); and the work 
of the anti-hail service was stopped (the population of Eastern 
Georgia had insisted on this repeatedly during the 30 years of 
its activity). 
  Among the members of the Greens Movement coordinating 
council 
are Mamukha Georgiyevich Shikhashvili (city of Tbilisi). 
  Addresses: 380008, city of Tbilisi, pr. Rustaveli, d. 37, 
Rustaveli Society, Central Coordinating Council of the Greens 
Movement of Georgia; 380012, pr. D. Agmashenebeli, d. 182, park 
Mushtaid, Greens House, tel. 34-80-68, 35-16-76; 380060, city of 
Tbilisi, ul Anagskaya, d. 18, kv. 25, tel. 37-21-35, Zurab 
Zhvaniya; tel. 36-02-23, Marika Darchiya; tel. 22-46-36, Nika 
Oniani; tel. 22-67-92, Nana Nemsadze. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. 
Krupneyshiye...," op. cit., pp 29-31; 
  -  "To the Informals...," op 
cit, No 8, August 1991, p 6. 

<H3>    Youth Nature Protection Society of Georgia (Nature 
Protection Group or the Georgia Youth Association for Nature 
Protection, or the Youth Association for Nature Protection of 
Georgia) </H3>
  Member of the Greens Movement of Georgia. Chairman of the 
group is M. G. Shikhashvili and deputy chairman is D. A. 
Mushkudiani. 
  Address: 380091, city of Tbilisi, 1 kvartal, korp. 7, kv. 
64, 
Mamuka Georgiyevich Shikhashvili; same address, Georgiy 
Artemovich Shikhashvili; 380061, city of Tbilisi, ul. 
Dzhavakhetskaya, d. 7a, kv. 19, tel. 73-29-41 (home), Dariko 
Aleksandrovna Mushkudiani; 380060, city of Tbilisi, pr. Mira, d. 
21, kv. 117, tel. 38-51-07, Yegeniya Nikolayevna Bagogishvili. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Party of Georgia </H5>

  Created in March 1990 at the founding congress on the basis 
of the organizational structure of the Greens Movement of 
Georgia (see article). Provides political support of Greens 
work. In 1990 cooperated with the Round Table and then changed 
to opposition to President Gamsakhurdiya. In 1991 was persecuted 
by the authorities. In late 1991 and even now has protested 
armed methods of struggle. 
  A parliamentary type party. Ideologically and 
organizationally linked with the Greens Movement of Georgia. 
  On 8 September 1991 in Tbilisi conducted a meeting of Greens 
Parties (see article) of Ukraine, Georgia, Armenia, and 
Azerbaijan. The conference spoke in favor of unilateral nuclear 
disarmament and inviolability of the republics' borders. 
  Address: 380060, city of Tbilisi, ul. Anagskaya, d. 18, kv. 
25, tel. 37-21-35, Zurab Zhvaniya 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Alliance of Georgia </H5>

  Association of children's clubs and groups supervised by 
senior advisors and mentors. Works on ecological, cultural, and 
national problems. Unites more than 3,000 children and adults, 
including 1,500 people in Tbilisi. Membership is not recorded. 
  The club's senior advisor, Yuriy Vakhtanovich Lukashvili, 
supervises several clubs in the city of Tbilis: the "Skhivi" 
Photocenter at the Palace of Pioneers (160 people), the "Vasizi" 
Club (80 people), "Didube" (40 people), and "Eko" (26 people). 
  In September 1989 an "ecology exchange" was organized at the 
Artek Children's Camp with the assistance of the Georgian 
Komsomol Central Committee, and 100 teenagers from the alliance 
came to the camp. On 15 September they held a founding congress: 
the by-laws and the program were adopted, the emblem, the 
uniform (a red shirt, a green tie, the emblem, and a camera or 
movie camera), and rituals of greeting and oath-taking were 
approved ("Tbilisans take the oath in silence standing on the 
Holy Mountain of Mtatsminda above the precipice beneath which 
the city is located. In front of them are Kazbek and the 
Caucasian Range. The left hand lies on the gravestone of the 
great poet Vazh Pshavel and the right is raised in the greeting 
which was customary among ancient Georgians even before 
Christianity"). 
  Activities include: 

  -  taking of photographs and filming of movies (the children 
made five films about ecology and three of them were satires; 
the films are shown in schools and pioneer camps and on 
television, and the film "Ecology, Problems, and Us" was shown 
on Georgian television twice); 
  -  dissemination in markets of 
leaflets which say "Do not poison us, your children, with 
chemicals: we are the branch which you are sitting on"; 
  -  marches 
and bicycle races in gas masks with posters and banners; 
  -  "'combat actions' of detachments of road blockers against 
drivers of garbage trucks who unload garbage in the city's green 
zone." 

    The alliance has contacts with more than 150 children's 
organizations with similar goals; cooperates with Greens 
(children and adults) of the FRG, Cyprus, the United States, and 
other countries as well as with compatriots. Information on the 
alliance's activity regularly appears on the pages of the 
Georgian Komsomol Central Committee NORCHI LENINELI (in Georgian 
and in Russian, print run of 500,000 copies). 
  The alliance is a branch of the Georgian Peace Defense 
Committee and supported first the ecology association and after 
its transformation into the Greens Party of Georgia (see 
article) began to support the party. On this account Yu. V. 
Lukashvili said: "The chicken has not been born yet, but its 
chick is standing squarely on its feet and acting." 
  The alliance's difficulties: few adults, especially those 
with ecological training. 
  Address: 380004, city of Tbilisi, pr. Rustaveli, d. 6, 
Pioneer Palace, Greens Alliance of Georgia, tel. 99-00-94, Yuriy 
Vakhtangovich Lukashvili. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. Krupneyshiye..." 
op. cit., pp 31-33. 

<H5>    Ecological Society of Georgia </H5>
  Involved in ecological education. Among the members of the 
ESG presidium is Irakliy Revazovich Zakariadze (city of Tbilisi). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Tbilisi </H5>
<H5>  Caucasian Circle Society </H5>
  Organized an independent university and works on ecological 
education. 
  Address: 380008, city of Tbilisi, Levaya nab. [embankment], 
d. 4, kv. 23, tel. 34-72-63, Georgiy Ivanovich Tarkhan-Mouravi. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Kazakhstan </H5>

<H5>  Aral-Asia-Kazakhstan Committee </H5>
  Founded in November 1987 at the initiative of the poet 
Mukhtar Shakhanov (people's deputy of the USSR in 1989-1991, 
people's deputy of the Republic of Kazakhstan since 1991) under 
the Writers Union of Kazakhstan as the Committee on Problems of 
the Aral. In 1988 transformed into the Public Committee on 
Problems of the Aral, Balkhash, and the Ecology of Kazakhstan. 
Since mid-1989 has borne the name: Public Committee of the Aral, 
Balkhash, and the Ecology of Kazakhstan. Has had its present 
name since mid-1991. Officially registered on 14 April 1989. 
  At the start of the committee's activity there were about 
100 
highly placed people in it: "After the accident at Dzhamalkum 
(1988) and Shakhanov's sharp criticism of a number of leaders of 
Agroprom, the Ministry of Water Management, and the oblast 
soviet, the ministers not only left the committee but demanded 
that it disband." 
  Organized the "April" meeting in Aralsk on 6-7 June 1988. In 
September 1988 at the committee's initiative an international 
Aral movement of poets, "20th Century. Peace and Ecology," was 
formed. Publishes materials in the press. 
  Elected at the committee's founding conference on 15 June 
1989 were the presidium (25 people, and a year later--about 15 
people, the presidium meets at least 4 times a year), the 
chairman (Mukhtar Shakhanov), the scientific coordinator (Salmen 
Tugelbayev), and the responsible secretary (Pamilya 
Bekturganova). By 1990 there were two responsible secretaries 
who had been discharged. 
  The number of members as of 1 January 1990 was 180. 80-90 
percent are aged 40-60 years, 30 percent were figures of culture 
and party and Soviet employees before the summer and fall of 
1991; 10 percent are pensioners and 15 percent are employees of 
the mass information media. 
  The tasks are to provide "propaganda of ecological 
knowledge, 
rational use of natural resources, and social aid to residents 
of ecological disaster regions," and other things. 
  The main areas of work are: indoctrination of ecological 
awareness and study of public opinion on solutions of problems 
of ecology by regions (Aral, Balkhash, and others). 
  Cooperates with Goskomprirody Kazakhstan, the antinuclear 
movement Nevada-Semipalatinsk (see article), and the republic's 
ecological institutes. 
  Publishes an ecological bulletin and allocates money to buy 
medicines for residents of the Aral Region. Plans to build a 
children's sanitorium and clinic. Studies the experience of 
other "green" organizations and movements. 
  The headquarters is on the premises of the editorial office 
of ZHALYN. Conducts meetings in the House of Scientists of 
Kazakhstan and on the premises of the editorial office of the 
journal ZHALYN. More than 200 people, for the most part writers, 
journalists, and scientists, participate in the meetings. 
  There is an independent cost accounting division in 
Kyzyl-Orda Oblast. 
  Has by-laws. Has its own emblem. At the committee's expanded 
meeting in the summer of 1991, it was decided to create the 
International Public Committee "Aral-Asia-Kazakhstan." T. 
Hayashi, the committee's vice president, member of the governing 
board of the Japan-USSR Society, and president of the firm 
Tachibank Trading, spoke at this meeting and reported that the 
Global Infrastructure Foundation of Japan (one of the largest 
charitable organizations in the world) proposed the concept of a 
plan for reviving the Aral Sea. The committee established an 
annual international Aral prize which will be awarded to 
scientists, statesmen, and political figures for special 
services in formulating and realizing plans and programs to 
revive the Aral, with presentation of a badge of honor and a 
cash prize. 
  Address: 480091, city of Almaty, pr. Kommunisticheskiy, d. 
105, Writers Union of Kazakhstan, Mukhtar Shakhanovich 
Shakhanov; city of Almaty, pr. Lenina, d. 77, tel. 33-22-21, 
60-33-63, committee presidium, Mashen Muntiyevich 
Imanbayev--responsible secretary of the committee; 480002, city 
of Almaty, pr. Lenina, d. 77, tel. 33-22-21 (editorial office of 
ZHALYN), 60-33-63; tel. 62-48-24, 69-25-78, presidium of the 
Supreme Soviet of Kazakhstan. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  LENINSKAYA SMENA, 19 June 1991; 
  -  "To the Informals...," op. 
cit., No 8, August 1991, p 6; 
  -  "Zelenyye v SSSR. 
Krupneyshiye...," op. cit., p 24; 
  -  Ponomarev, V., 
"Samodeyatelnyye obshchestvennyye organizatsii Kazakhstana i 
Kirgizii. 1987-1991 (opyt spravochnika)" [Public 
Non-Professional Organizations of Kazakhstan and Kirghizia. 
1987-1991 (Provisional Directory)], Moscow, Institute of the 
Study of Extreme Processes (USSR), 1991, p 44. 

<H5>    Greens Movement of Kazakhstan </H5>
  Part of the Greens Movement operating on the territory of 
the 
former USSR (see article). Among the members of the GMK 
coordinating council is M. Kh. Yeleusizov, hydraulic engineer. 
  Address: city of Almaty, tel. 21-39-93, Mels Khamzayevich 
Yeleusizov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Front of Kazakhstan </H5>

  A non-professional association. Registered on 24 August 1989 
as a republic organization under the Nature Protection Society, 
although at first work was only done in Almaty. Has by-laws and 
a program. 
  The GF founding meeting took place on 8 June 1988. Among the 
founders were the social-ecological association "Initiative," 
the "Otrar" MZhK [expansion unknown], the Noosphere Center, the 
Creation Cooperative Commune, the ecology center of the 
Kazakhstan Komsomol Central Committee, and others. The front 
united participants in clearing a walking trail (1.5 kilometers 
long) along the Malaya Almaatinka River. "This orientation to 
concrete, ongoing work has been preserved up to the present day; 
it includes the organization of volunteer work days to plant 
trees, to clean up territories after mudflows, to water streets, 
and so forth." 
  The goal is to "search for optimal forms of interrelations 
of 
man and the environment." 
  The tasks are to "close" the destructive manmade reservoirs 
in the region of Almaty, resolve the problem of air pollution 
over the capital, and prevent water from leaking from the 
collector Lake Sorbulak. 
  Involved in ecological education, in particular in relation 
to reservoirs. 
  At first the GF was the largest volunteer association of the 
city of Almaty. But in the fall of 1988 a split occurred in it 
between the advocates of political activity (they made up the 
initiative group of the Almaty People's Front) and the advocates 
of purely ecological activity. 
  By early 1990 there were 67 activists in the GF and by early 
1991 there were about 50 people. 
  The GF council consisting of 10 people meets twice a month 
on 
the premises of the Republic Nature Protection Society. 
  The movement's chairman is Marat Akhmetkhanovich 
Chimbulatov, 
candidate of biological sciences, chief of the "Kazgeofizika" 
AGO [possibly Archives of the Geographic Society], city soviet 
deputy, and chairman of the city soviet's ecology commission. 
Among the members of the GF are two city soviet deputies and 
four rayon soviet deputies. 
  Members of the aktiv include V. Gapchak, Ye. Glebov, M. 
Kanevskaya, V. Karachev, S. Kuratov, A. Skopin, Ye. Slavko, and 
Ye. Sheyger. 
  The association is a member of the Greens Movement (see 
article). 
  Addresses: 480000, city of Almaty, ul. Gorkogo, d. 15, 
Greens 
Front Association, tel. 61-65-16; 480004, city of Almaty, ul. 
Panfilova, d. 101, kv. 55, tel. 63-36-76 (home), 63-69-27, Marat 
Chimbulatov; tel. 43-95-50, Vladimir Karachev. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. Krupneyshiye...," op. cit, pp 23-24; 
  -  "To the 
Informals...," op. cit., No 9, September 1991, p 2; 
  -  Ponomarev, 
V., op. cit., pp 37-38; 
  -  "Samodeyatelnyye obshchestvennyye 
organizatsii (SOO) Kazakhskoy SSR (spravochnik)" [Public 
Non-Professional Organizations (VPO) of the Kazakh SSR 
(Directory)], Almaty, 1990, p 1. 

<H5>    Kazakh Nature Protection Society </H5>
  A republic organization. Registered on 19 November 1991, 
Registration No 0017. Cooperates with nature protection 
societies of other republics (see article). Organizes ecological 
education and the study of public opinion and participates in 
resolving problems of industrial and agricultural pollution. 
  Addresses: 480002, city of Almaty, ul. Zhibeknosoly, d. 15, 
tel. 61-77-42; ul. Zh. Zholy, d. 15, tel. 30-16-40, 69-19-56, 
Kamza Zhumambekov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "To 
the Informals...," op. cit., No 9, September 1991, p 2. 

<H5>    Nevada-Semipalatinsk </H5>
  The antinuclear movement of Kazakhstan. The goal is to 
dismantle all the nuclear test ranges on Kazakhstan's territory, 
establish public monitoring of industrial waste, and create an 
ecological map of the region. "Nevada" means that the movement 
simultaneously supports the termination of nuclear tests in the 
United States. It has branches in all oblast centers of 
Kazakhstan. Enjoys the support of the population outside the 
state's borders. 
  Founded in February 1989. The latest discharge of 
radioactive 
substances during tests in February 1989 served as the impetus 
for the movement's creation; on 26 February Olzhas Suleymenov, 
the first secretary of the Writers Union of Kazakhstan before 
the fall of 1991, a people's deputy of the USSR (1989-1991), and 
author of books, including "AZ i Ya" [AS i A] (which suggested 
an Asian-centered view of history), in a speech on republic 
television proposed to organize the movement, and occurring on 
28 February on the premises of the Writers Union in the city of 
Almaty was the organizing meeting (2,000 participants) which 
adopted an appeal; on 13 March the by-laws were adopted; it was 
registered at the rayispolkom on 16 March 1989 and the same day 
a bank account was opened. On 21 October 1991 it was registered 
by the Kazakh SSR Ministry of Justice, Registration No 0001. 
  The management organs are: the working group of the 
coordinating council (15 people) and the ispolkom (7 people), 
which works on economic questions. The chairman is O. Suleymenov 
and the vice chairmen are M. Auezov and S. Sanbayev. There are 
released employees. In all there are about 100 permanent 
participants. Affiliates of the movement were created in 15 
oblasts of Kazakhstan and in Moscow. A scientific center was 
formed. A distinctive feature of the movement is its 
international make-up. 
  The movement's tasks are stated in the article by its 
activists Olzhas Suleymenov and Vladimir Yakimets "Third Race" 
(that means testing of third generation nuclear weapons): 
  "During the period of time remaining until 1995, public, 
parliamentary, international, and governmental organizations 
need concentrated joint work: 

  -  "to revise and toughen the system of international 
treaties prohibiting the development, production, and testing of 
nuclear weapons; 
  -  "to create a system of economic and political 
sanctions against countries which violate the proliferation 
system; 
  -  "to formulate measures of efficient monitoring of all 
stages of production and transport of existing nuclear 
materials; 
  -  "to organize an international ecological 
purification program of enterprises of the nuclear 
military-industrial complex of countries of the nuclear club and 
countries at its threshold." 

    One more task, in O. Suleymenov's opinion, is that "in our 
consciousness we must single out the threat from geniuses and 
from quiet, modest individuals in secret laboratories as an 
independent factor." 
  Starting in March 1989, signatures began to be gathered in 
Almaty for the movement's benefit, and then money--at first 
semilegally, but soon the signature lists began to be put up 
openly in organizations and institutions. 
  On 17-19 July a scientific-practical conference on the 
impact 
of nuclear weapons testing on the health of local residents was 
organized in Semipalatinsk. 
  On 6 August the world antinuclear march from Semipalatinsk 
to 
the rayon center of Abayskiy Rayon, the settlement of Karaul, 
which is located near a test range, was conducted. 
  In the fall a rally near the Moskva Hotel and a procession 
to 
the Kremlin Palace of Congresses were organized and an appeal 
was delivered to the Second Congress of People's Deputies of the 
USSR. 
  On 9 September and 9 December republic conferences of the 
movement's supporters were held. 
  By late 1989 more than 1 million signatures had been 
gathered 
for the appeal to close the nuclear test range. 
  From 28 February until mid-1991 the newspaper IZBIRATEL was 
published in the Kazakh and Russian languages (12 pages, in 
newspaper format. Photo offset. Print run--50,000 copies). The 
editor in chief was Yermek Tursunov. Publication stopped because 
of financial difficulties. 
  On 24-27 May 1990 the international conference "Voters of 
the 
World for Banning Nuclear Weapons Testing" was held in Almaty 
and Semipalatinsk (more than 700 participants, among them guests 
from various countries). 
  In September a Peace March was held together with 
representatives of foreign antiwar organizations. 
  No later than mid-1991 a conference on the occasion of the 
arrival of German medical personnel from a Turkish-German 
medical foundation was held; they came at the invitation of the 
Nevada-Semipalatinsk Movement in order to familiarize themselves 
with the consequences of nuclear tests in Semipalatinsk and the 
state of medicine in the region. 
  No later than 8 August 1991, after the USSR Ministry of 
Defense offered R5 million as compensation to the residents of 
rayons adjacent to the test range for three planned nuclear 
explosions and the Kazakhstan Supreme Soviet decided to place 
the question of continuing nuclear testing on a referendum of 
local residents, the movement's activists called upon the 
population to vote against the new tests. 
  From May through September 1991, together with the public 
committee "Nomadic People's Trek into the 21st Century" and the 
"Next Stop" Movement, this movement conducted a series of events 
whose goal was to close nuclear test ranges, achieve a universal 
moratorium on testing, and destroy all types of weapons of mass 
destruction; the "People's Trek" began near the Semipalatinsk 
test range and from 6 through 9 August made stops in Japan in 
the cities of Hiroshima and Nagasaki, crossed the Pacific Ocean 
to the United States, and ended its itinerary near the test 
range in the state of Nevada. 
  Several rallies were held in Almaty and other cities of 
Kazakhstan. 
  Thanks to the movement's active work to ban nuclear weapons 
tests, the Semipalatinsk Nuclear Test Range was closed by edict 
of the president of the Republic of Kazakhstan, N. Nazarbayev. 
  On 27 March 1992 the movement's forum began work; the goal 
was to demand that the missile testing range in China near the 
Chinese-Kazakh border be shut down. 
  The organization is financed by the Soviet Peace Committee 
and the Soviet Peace Defense Committee, and it includes R25,000 
received from the Soviet Peace Committee. 
  The movement's symbol is the palm of a hand raised in a 
gesture of protest. 
  Addresses: 480091, city of Almaty, Kommunisticheskiy pr., d. 
105, Writers Union of Kazakhstan, tel. 62-62-95, 292-25-33 (in 
Moscow), Olzhas Omarovich Suleymenov; 480021, city of Almaty, 
pr. Lenina, d. 21, 5-y etazh [floor], executive committee of the 
Nevada-Semipalatinsk Movement, tel. 63-36-55, 63-35-85, 
63-55-44; pr. Lenina, d. 85, tel. 63-36-48; 480044, city of 
Almaty, ul. Gorkogo, d. 50, tel. 33-33-71, 67-27-95, Yermek 
Tursunov; tel. 60-12-15 (work), 39-54-64 (home), Svetlana 
Azaryevna Primova. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "The 
Military Has a Pile of Money," ZELENYY MIR, No 29-30, 1991, p 2; 
  -  "Zelenyye v SSSR. Krupneyshiye...," op. cit., pp 22-23; 
  -  Kosenko, Ye, "Kazakhstan," EKSPRESS-KHRONIKA, No 13 (243) 31 
March 1992, p 3; 
  -  "To the Informals...," op. cit., No 9, 
September 1991, p 2; 
  -  Ponomarev, V. op. cit., pp 43, 51; 
  -  Suleymenov, O., Yakimer, V., "The Third Race," SPASENIYE, No 
4, 
1991, p 3. 

<H5>    Society of Regional Studies Specialists of Kazakhstan </H5>
  Involved in questions of culture, history, and ecology. 
Regional organizations of the society are found in all oblasts 
of Kazakhstan and the city of Almaty. The founding congress was 
held in November 1989. The society was registered on 22 January 
1992 at the Ministry of Justice of Kazakhstan, Registration No 
0069. 
  Considers itself the successor to the Society for the Study 
of Kazakhstan which operated in the 1920s and 1930s. 
  Several sections operate in the society: archeology, 
architecture, folklore, ecology, ethnography, and others. 
Scientific conferences are conducted in memory of forgotten 
heroes, figures of culture, and statesmen. In 1991 a graveside 
monument was erected to the writer Taymanov; the 200th 
anniversary of the birthday of the leader of the Kazakh uprising 
of 1836-1838, I. Taymanov, was celebrated. The publishing house 
"Volnke" (Region) operates in the society on public principles. 
In 1991 the publishing house put out a book. 
  The society founded the Foundation To Support Ecological 
Education (see article). 
  Unites people of various ages (from high school students to 
pensioners) and various occupations. The management organs are 
the council and the presidium. The society's chairman is A. S. 
Takenov. 
  Finance by sponsors, for the most part small enterprises, in 
particular small folk medicine enterprises; receives income from 
publishing activity. 
  Address: 480012, city of Almaty, prosp. Seyfullina, d. 551, 
tel. 57-26-08, 21-28-57, Abu Saktaganovich Takenov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Survey. 

<H5>    "Tabigat" (Nature) </H5>
  This is the Greens Party of Kazakhstan. Created in December 
1989 as an ecological alliance of associations and enterprises 
of Kazakhstan; in March 1992 the alliance changed into a party. 
  The alliance's goal was to bring together ecology 
specialists 
and industrialists to introduce ecologically clean technologies. 
The party's goal is the "humanization of society." 
  On 24 March 1992 the party published draft by-laws and a 
program according to which Tabigat will be a parliamentary-type 
party and the primary organizations will be built on the basis 
of regions. 
  The chairman of the alliance and later the leader of the 
party is M. Kh. Yeleusizov (he was deputy director of 
Kazgiprovodkhoz [Kazakh State Planning, Surveying, and 
Scientific Research Institute of Water Management Construction] 
and is among the activists of the Greens Movement of Kazakhstan). 
  Address: 480083, city of Almaty, ul. Dzerzhinskogo, d. 21, 
kv. 37, tel. 32-86-94; tel. 63-84-26 (work), 21-39-93, Mels 
Khaizovich Yeleusizov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Kosenko, Ye., op. cit., p 3; 
  -  "To the Informals...," op. cit., 
No 9, September 1991, p 2; 
  -  Ponomarev, V., op. cit., p 48; 
  -  Ustinova, T., "In the Political Spectrum--the Greens Party," 
KAZAKHSTANSKAYA PRAVDA, 26 March 1992, p 3. 

<H5>    Alliance of Hunters and Fishermen's Societies of Kazakhstan </H5>
  The alliance was created on 23 August 1958. Numbers about 
4,000 members. The goal is to organize and run game farms taking 
into account the protection, reproduction, and rational use of 
game animals. 
  Forms of work are: raising of game, organization of young 
hunters and fishermen's sections and patrols, and 
acclimatization of game animals. 
  Resources: membership dues--R8 per person per year and a R10 
initiation fee. "There is no one boss because of the 
fragmentation of the republic's game system among nine 
departments," so the task is to combine the efforts of various 
organizations to improve Kazakhstan's game system. 
  The alliance cooperates with Goskomprirody, the Ministry of 
Timber Industry of Kazakhstan, republic societies of hunters and 
fishermen, and Kazakhrybvodzhoz [Kazakh Fisheries Water 
Management Office]. 
  The emblem is in the form of a shield with the following 
inscription on the top: on the left against a dark background 
the bright letters KAZ, to the right against a bright background 
the dark letters SSR; an image takes up a large part of the 
emblem: on the left against a bright background is a pheasant 
and on the right against a dark background is a fish; below and 
in the middle in the contrasting letters is: OKhOT RYBOLOV SOYUZ. 
  The highest body is the governing board. Its chairman is Sh. 
Z. Nurgaliyev and the deputy chairmen are V. S. Lobanov and V. 
T. Khudyakov. 
  Address: 480008, city of Almaty, ul. Chapayeva, d. 22-6, 
House of Hunters, tel. 42-17-33, Shaykheden Zulbukhanovich 
Nurgaliyev; tel. 42-06-75, Vasiliy Semenovich Lobanov; tel. 
42-13-61, Vyacheslav Terentyevich Khudyakov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "To 
the Informals...," op. cit., No 9, September 1991, p 2. 

<H5>    Chernobyl Alliance of Kazakhstan </H5>
  Part of the Chernobyl Alliance operating on the territory of 
the former USSR (see article). Has oblast branches (see 
article). Registered by the Ministry of Justice of Kazakhstan on 
25 December 1991, Registration No 0029. Studies the problem of 
the impact of nuclear contamination on the condition of the 
environment and the population's health. Provides assistance to 
participants in cleaning up the consequences of the Chernobyl 
Catastrophe. 
  Address: 480078, city of Almaty, ul. Dzhambula, d. 159, tel. 
32-25-95, Bulat Kisayevich Razdykov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2. 

<H5>    Foundation To Support Ecological Education </H5>
  Operates on the territory of Kazakhstan. Registered on 25 
December 1991, Registration No 0037. The founder was the Society 
of Regional Studies Specialists of Kazakhstan. 
  Cooperates with specialists in ecology from different 
countries. In late 1991 experts came to Almaty from Denmark, 
Germany, and other countries. A seminar with their participation 
was held. In the spring of 1992 the foundation sent seven people 
to Denmark for 2.5 months; the purpose was to study the system 
of ecological education in Denmark. 
  Zh. A. Takenov heads the foundation. 
  Address: 480121, city of Almaty, KazGU [Kazakh State 
University], school of biology, kom. 318, tel. 47-25-96, Zharas 
Abuovich Takenov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2. 

<H5>    Ecological Foundation of Kazakhstan </H5>
  Linked with the Initiative social-ecological association 
(see 
article). The goal is to finance ecology programs. 
  Address: 480042, city of Almaty, ul. Dezhneva, d. 17, tel. 
53-85-80, Lev Ivanovich Kurlapov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "To 
the Informals...," op. cit., No 8, August 1991, p 6. 

<H5>    City of Almaty </H5>
<H5>  Green Salvation </H5>
  A city ecological society. Broke off from the Initiative 
Group (city of Almaty, see article) in May 1990. Differs from it 
in terms of greater discipline. Registered in the rayispolkom. 
Has a bank account. There are about 10 participants in the 
society. 
  The goal, according to the by-laws, is to help improve the 
ecological situation in the city. Gathers information on the 
ecological situation in the city of Almaty and the oblast (among 
other things, on the explosion in the gas main in May 1989). 
Organizes stands and exhibits on ecology topics for sessions of 
the city and rayon soviets and for the House of Scientists. 
Favors the creation of a Greens Party of Kazakhstan. 
  The society's members meet every month in the House of 
Scientists. The chairman is Sergey Georgiyevich Kuratov. 
  Addresses: 480059, city of Almaty, ul. Shagabutdinova, d. 
133, kv. 66, tel. 63-91-06, Sergey Georgiyevich Kuratov; 480042, 
city of Almaty, mkrn. "Taugul," d. 13, kv. 99, tel. 26-67-57, 
Artem Borisovich Salin. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Ponomarev, V., op. cit., p 37. 

<H5>    Initiative Social-Ecological Association (Club) </H5>
  The first independent city organization. Appeared in April 
1987. The club was registered in November 1988. Its founders 
were employees of Kazakh Television, Sergey Duvanov (now 
cochairman of the Social Democratic Party of Kazakhstan) and 
Anna Belousova. 
  At the start of its activity, it brought together about 40 
people with an aktiv of 7-10 people, primarily Russian-speaking 
intelligentsia. 
  The task is to study regional and republic ecological and 
social problems, support social initiatives of citizens, and 
provide ecological education. 
  In the spring of 1988 Initiative participated in 
investigating events related to the Zhamankumskiy Mudslide; and 
on 8 May they conducted a meeting (400 participants) in the 
settlement of Zarechnyy, which had suffered from the mudslide. 
  Voluntary work days were conducted on 5 June 1988 and 1989 
(300 and 500 participants, respectively). 
  In the spring of 1990 they managed to get expenditures for 
ecological goals included in the Frunzenskiy Rayon budget. 
  Every month 6-10 members of the association conduct debates 
in the House of Scientists. 
  Until April 1990 the chairman of the association was Sergey 
Georgiyevich Kuratov. But because of disagreements with 
association member Viktor Viktorovich Zonov he left this post. 
In May 1990 the Green Salvation Group (see article) split from 
Initiative. S. G. Kuratov became its chairman. 
  Initiative is a member of the Social-Ecological Alliance 
(see 
article). 
  Addresses: 480037 (or 480000), city of Almaty, ul. Teslenko, 
d. 31, kv. 2, tel. 33-67-32, Viktor Viktorovich Zonov; 480059, 
city of Almaty, ul. Shagabutdinova, d. 133, kv. 66, tel. 
63-91-06 (home), 64-02-88 (work), Sergey Georgiyevich Kuratov; 
tel. 26-77-57, Artem Falin; tel. 63-78-41 (work), Anna 
Vladimirovna Belousova. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. Krupneyshiye...," op. cit., pp 24-25; 
  -  Ponomarev, V., op. cit., p 38. 

<H5>    Noosphere Center </H5>
  Created in March 1988 under the Oktyabrskiy Rayon Komsomol 
of 
the city of Almaty. Declared itself an affiliate of the 
international organization "For a Nonnuclear World and the 
Survival of Humankind." Up to 30 people attended the monthly 
meetings. The center adopted by-laws and a program of actions. 
Supported avant garde art. 
  The center's chairman was V. Ganzha. The center disbanded in 
the spring of 1989. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., p 44. 

<H5>    Youth Initiative Center, Ecology Section </H5>
  The average age of the participant is 18-20 years. Conducts 
debates on ecological topics and participates in city nature 
protection events. 
  Address: city of Almaty, pr. Lenina, d. 114, Marina 
Vladimirovna Solotova. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2. 

<H5>    Aktyubinsk Oblast </H5>
<H5>  City of Aktyubinsk </H5>
<H5>  Aktyubinsk Ecologist </H5>
  This is a city association. Registered in September 1989. 
Provides methodological and practical aid to the oblast Nature 
Protection Committee. Monitors the execution of nature 
protection laws. 
  Size is 15 people. Meetings are held twice a month in the 
building of the oblast Nature Protection Committee. A report on 
the work was published monthly in the oblast newspaper PUT K 
KOMMUNIZMU. The leader of the association is V. V. Mutaniol, 
department head of the newspaper PUT K KOMMUNIZMU. 
<H6>  Source of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. 
cit., p 
10. 

<H5>    "Zhem" </H5>
  City antinuclear group. It was registered at the Aktyubinsk 
Gorispolkom in September 1989. Goal: a complete ban on testing 
of nuclear weapons and other weapons of mass destruction and a 
prohibition against burying radioactive waste in Kazakhstan. 
  It has 11 members. It is financed through public charitable 
money and by organizing cultural events. The leader is S. Utenov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. 
cit., p 
10. 

<H5>    East Kazakhstan Oblast </H5>
<H5>  City of Leninogorsk </H5>
<H5>  Biosphere Ecoclub </H5>
  Participates in resolving problems related to industrial 
pollution and radiation contamination. Conducts debates on 
philosophical and ecological themes. 
  Address: 493910, East Kazakhstan Oblast, city of 
Leninogorsk, 
ul. Furmanova, d. 21, kv. 12, Lyubov A. Ganzhina. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2. 

<H5>    City of Ust-Kamenogorsk </H5>
<H5>  Provisional Citizens Committee </H5>
  This is a city organization. The committee was formed by the 
Ust-Kamenogorsk City Committee of the CPSU in September 1989 as 
an "alternative formation to the negative and politically 
immature movements and organizations that are trying to `slip' 
their representatives into membership in the soviets." 
  Conducts work to save the ecology of Rudnyy Altay and 
supports stopping nuclear tests at the test range near 
Semipalatinsk. The leader of the committee is V. S. Shparaga, 
the deputy chairman of the city ispolkom and deputy of the city 
soviet. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. cit., 
pp 12-13. 

<H5>    Coordinating Center of the Movement To Defend the Irtysh </H5>
  Founded in 1990. Cooperates with ecology organizations of 
Ust-Kamenogorsk, Semipalatinsk, and other populated points 
located in the floodplain of the Irtysh River. Opposes 
industrial and agricultural contamination of the river. Studies 
the impact of hydraulic engineering structures on flora and 
fauna. 
  Address: 490024, East Kazakhstan Oblast, city of 
Ust-Kamenogorsk, nab. Krasnykh Orlov, d. 109, kv. 16, tel. 
65-27-61, Pavel I. Bortnik. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2. 

<H5>    Nevada-Semipalatinsk </H5>
  The East Kazakhstan Oblast branch of the republic movement 
(see article). Made up of instructors and students of 
pedagogical and road construction institutes and workers and 
engineering technical personnel of the lead and zinc combine. 
Cooperates with the people's fronts of Moscow and Belarus and 
maintains contacts with residents of China who are fighting to 
stop tests at the Xinjian Test Range. The leader is Zh. A. 
Sadykov, an instructor at the pedagogical institute (city of 
Ust-Kamenogorsk). 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. cit. 
p 
12. 

<H5>    Dzhambul Oblast </H5>
<H5>  City of Dzhambul </H5>
<H5>  Greens Movement of the City of Dzhambul </H5>
  This is a public ecology center; it operates on the city's 
territory. The group was created in October 1988 and registered 
in May 1989. 
  The movement unites about 30 people. The social make-up 
includes entrepreneurs, scientists, creative intelligentsia, and 
others; technical intelligentsia 30-45 years old predominate. 
  The chairman is Aleksandr Pavlovich Zagribelnyy, deputy of 
the oblast soviet of people's deputies and chief of the 
pedagogical institute's sociological research laboratory. Among 
the participants in the movement are Askar Berkaliyev, a 
people's deputy of the Dzhambul Soviet; R. Tikebayev; and R. A. 
Tatibayev, chief of the educational center of the Dzhambul 
Pedagogical Institute. 
  The center originated to fight to close down the Khimprom 
[Chemical Industry] Production Association (since the summer of 
1989 the enterprise has begun to gradually change 
specializations). Then the tasks expanded and included 
propaganda of ecological knowledge, planting of green buffer 
zones near chemical plants, organization of ecological expert 
studies, including the gathering of capital to conduct them, and 
similar things. From making preparations for public actions, the 
center gradually changed to working primarily through 
cooperatives and associations. 
  Founds and cofounds different commercial enterprises 
involved 
in nature protection activity. 
  Participants in the movement organized the Flora Cooperative 
under the oblast production association and began work to create 
a wooded sanitary-buffer zone around the superphosphate plant 
and the next year--around the Dzhambul Khimprom Production 
Association, but already through efforts organized under the 
association's cost accounting section. More than 300 hectares of 
wooded area were planted. Planting of a sanitary buffer zone 
around the Novodzhambul Phosphorous Plant are planned in the 
very near future. 
  The creative association Propaganda for the Fundamentals of 
Ecological Knowledge ["Ekologicheskiy vseobuch"] is involved in 
nature protection and naturalist education for children and 
teenagers, set up a puppet theater, prepared a chapter in a book 
on the native region "Rare and Disappearing Animals and Plants 
of Dzhambul Oblast," participated in creating the film by the 
film director and animal painter V. Belyalov, "On the Shores of 
the Bilikul," dedicated to saving it, and together with one of 
the creative associations of Kazakhfilm and the commercial 
center Aziya is involved in shooting a documentary film on the 
Great Silk Road and the plant world of the desert and the Tian 
Shan, while next in line are two books on Dzhambul's historical 
past. 
  The Nature Cooperative began to produce express analyzers of 
agricultural products for nitrates and nitrites. 
  The small enterprise Ecology is building decontamination 
structures. 
  The Flora and Nature cooperatives, the small enterprise 
Ecology, and several other enterprises combined into the 
Association of Ecological Small Enterprises and Cooperatives, 
ELTEKS, in December 1990; the general director is Murat 
Berkaliyev, candidate of technical sciences. The small capital 
of a number of enterprises put together becomes "million-ruble 
contracts for construction of decontamination structures, 
production of consumer goods worth tens of thousands of rubles, 
and construction of new shops in which the volume of output is 
to be... quadrupled." 
  Address: 484006, city of Dzhambul, ul. Lunacharskogo, d. 42, 
kv. 2, tel. 5-24-83 (home), 3-41-20 (work), Aleksandr Pavlovich 
Zagribelnyy, participant in the Initiative Social-Ecological 
Movement (see article) and the initiative group Ecology (see 
article); 484000, city of Dzhambul, ul. Abaya, d. 186, kv. 1, 
tel. 4-73-68, Valeriy Vasilyevich Kuklin. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., pp 53-54; 
  -  Pugovkin, A., people's 
deputy of the Dzhambul Oblast Soviet, "The Noise Has Abated and 
Now They Are Planting," SPASENIYE, No 7, July 1991, p 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. cit., 
pp 5, 15. 

<H5>    Nevada-Semipalatinsk </H5>
  The Dzhambul Oblast branch of the republic movement (see 
article). Created in April 1989 on the base of the pedagogical 
institute. Has subdivisions in the rayon centers of Assa and 
Burnoye. Aktiv consists of seven people. The chairman is Bakhyt 
Toleubayev (worked as an instructor in the city committee of the 
Komsomol in early 1991). 
  In early 1990 the branch conducted a sociological survey of 
the residents of the city of Dzhambul regarding the 
Semipalatinsk Test Range. 
  Address: 484040, city of Dzhambul, Pervyy Severnyy per., d. 
18, tel. 4-45-57, 4-32-22 (work), Bakhyt Toleubayev. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., p 54 
  -  "Samodeyatelnyye 
obshchestvennyye organizatsii...," op. cit., p 15. 

<H5>    Dzhezkazgan Oblast </H5>
<H5>  City of Dzhezkazgan </H5>
<H5>  "Uly Tau" </H5>
  This is a city ecological society. Appeared in March 1989 at 
the initiative of the teachers of the Dzhezkazgan Affiliate of 
the Karaganda Polytechnical Institute, registered under the 
gorispolkom, and has a bank account. In February 1990 a branch 
of the society was created in the settlement of Ulytau. 
  Is a collective member of the Nevada-Semipalatinsk Movement 
(see article). 
  Weekly meetings are held in the city's House of Political 
Education and up to 100 people gather at them; they are 
intelligentsia, including instructors of VUZes, and workers, for 
the most part of the Kazakh nationality. The aktiv comprises 15 
people. The chairman is Deputy of the Dzhezkazgan Oblast Soviet 
A. M. Baymenov. 
  Addresses: city of Dzhezkazgan, tel.-6-29-07 (work), 6-16-14 
(work), 3-44-51, Alikhan Mukhamedyarovich Baymenov; city of 
Dzhezkazgan, tel. 6-01-08, Yerken Dzhabaginov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., pp 54-55; 
  -  "Samodeyatelnyye 
obshchestvennyye organizatsii...," op. cit., p 16. 

<H5>    Karaganda Oblast </H5>
<H5>  Nevada-Semipalatinsk </H5>
  The Karaganda regional branch of the republic movement (see 
article), the first of the regional organizations of the 
antinuclear movement on Kazakhstan's territory. 
  The founding assembly of the Karaganda City Branch occurred 
on 9 April 1989 at the initiative of the second secretary of the 
Komsomol gorkom, Sh. Abdrakhmanova. Participating were 150 
people. Formed an organizing committee of 32 people. Elected a 
chairman--Morgulan Khamiyevich Khamiyev (candidate of technical 
sciences and senior scientific associate of the Karaganda Coal 
Scientific Research Institute). 
  On 21 April 1989 created a city coordinating council of the 
antinuclear movement in the city of Karaganda; 3 cochairmen were 
elected. The aktiv consists of 15 people. "On 1 May 50 'Nevada' 
supporters walked in a separate column during the holiday march. 
On 9 June 1989 the 'Nevada' rally was held on Yunost Square 
(around 350 participants). On 20-22 October 1989 protest rallies 
against a nuclear test that had been conducted were held in 
seven cities of Karaganda Oblast; around 20,000 people 
participated in them. The oblast working committee adopted a 
resolution to start a strike in the event the nuclear tests 
continued. By November 1989 more than 50,000 signatures had been 
gathered for an appeal demanding that the nuclear test range be 
closed. By that time branches of the antinuclear movement had 
been formed in Saran (4 November), Temirtau, and other populated 
points in the oblast." 
  On 21 December the founding conference of the oblast branch 
of the movement was held. The oblast branch was registered and a 
bank account was opened. 
  The oblast branch conducts charitable actions, including 
musical concerts, and participates in the election struggle. 
  On 13 September 1990 an antinuclear rally was held in 
Karaganda (around 15,000 participants). 
  In 1990 the Nevada-Semipalatinsk Movement was supported 
along 
with the economic demands during the strikes of Karaganda miners. 
  On 8 December 1990 the interregional council was formed to 
coordinate the actions of the oblast branches of Nevada. It 
includes representatives of Nevada groups from oblasts located 
near the Semipalatinsk Test Range. 
  Address: 470000, city of Karaganda, ul. Lobody, d. 12, kv. 
17, tel. 57-14-51, Morgulan Khamiyevich Khamiyev; 470000, city 
of Karaganda, ul. Dzhambula, d. 1, kv. 16, tel. 57-17-06, 
Mikhail Semenovich Brodskiy. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., pp 55-56; 
  -  "Samodeyatelnyye 
obshchestvennyye organizatsii..." op. cit., p 17. 

<H5>    City of Temirtau </H5>
<H5>  "Nura" </H5>
  This is a city society. Formed in July and registered at the 
gorispolkom in September 1989. The goal is to defend the city's 
environment. There is a program and by-laws. There are 27 
members and the ethnic make-up is diverse. Cooperates with local 
organs of power. The chairman is D. V. Oskin, in 1990 a member 
of the USSR Writers Union. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. cit., 
pp 17-18. 

<H5>    Kustanay Oblast </H5>
<H5>  City of Dzhetygora </H5>
<H5>  Ecological Society </H5>
  Formed and registered in May 1989. Initiative group (13 
people) composed of employees of the Kustanayasbest [Kustanay 
Asbestos] Combine. In 1990 the society had 37 people. 
  Tasks are to monitor the ecological situation in the city of 
Dzhetygora, to participate in measures to fix up the city, and 
to do lecture work. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. 
cit., p 
20. 

<H5>    Kzyl-Orda Oblast </H5>
<H5>  City of Kyzl-Orda </H5>
<H5>  Greens Front Association </H5>
  Created in February 1990 and registered. Involved in 
ecological propaganda. The 15 participants, for the most part of 
Kazakh nationality, are involved in nature protection activity 
and enjoy the support of students. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. 
cit., p 
19. 

<H5>    City of Aralsk </H5>
<H5>  Aral-Front </H5>
  This is a cooperative-creative association. Formed in March 
1989 and registered. The aktiv consists of six people. The goal 
is to "fight for the region's ecological balance and social 
justice through intervening in the activity of party-soviet 
organs." 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvenyye organizatsii...," op. cit., 
p 
19. 

<H5>    Kokchetav Oblast </H5>
<H5>  Nevada-Semipalatinsk </H5>
  This is the Kokchetav Oblast branch of the republic movement 
(see article). Created on 5 December 1989, registered in 
February 1990, and has a bank account. The coordinating council 
consists of 18 people. The working bureau consists of three 
people. The chairman is S. B. Yeslamov, the director of 
Kokchetavglavsnab [Kokchetav Main Supply Administration]. 
  They are fighting to close the uranium mines in Volodarskiy 
and other rayons of the oblast. 
  Address: 480000, city of Kokchetav, ul. Srednyaya, d. 91, 
kv. 
50, tel. 6-70-41 (work), 6-57-61, Seraly Bolatovich Yeslamov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., p 59; 
  -  "Samodeyatelnyye 
obshchestvenyye organizatsii...," op. cit., p 20. 

<H5>    Myngystauskaya (Guryev) Oblast </H5>
<H5>  City of Altau (Shevchenko) </H5>
<H5>  Save the Caspian Sea </H5>
  Involved in ecological education. Cooperates with other 
organizations of the republic and outside its borders which 
pursue the goal of saving the Caspian. 
  Address: 466200, Myngystauskaya Oblast, city of Altau, 7-y 
mkrn., d. 26, kv. 54, M. I. Maslennikov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2. 

<H5>    Pavlodar Oblast </H5>
<H5>  Nevada-Semipalatinsk </H5>
  The Pavlodar Oblast branch of the republic movement (see 
article). The founding assembly took place in November 1989 and 
the branch was registered. The chairman is Amantay Kaliyev. In 
the summer of 1989, a branch of the movement was formed in the 
city of Ekibastuz. 
  Address: 637000, city of Pavlodar, ul. Dzherzhinskogo, d. 
104, OPTs, kab. [office] 5, tel. 72-40-91; 637000, city of 
Pavlodar, ul. Kutuzova, d. 99, kv. 24, tel. 45-61-31, Amantay 
Kaliyev. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., p 60. 

<H5>    City of Pavlodar </H5>
<H5>  Ecology and Public Opinion (EKOM) </H5>
  This is an initiative group. Founded in July 1987 at the 
initiative of the delegate of the 20th All-Union Komsomol 
Congress, Pavel Kuzmich Likhachev. Registered on 4 July. Has a 
program and by-laws. 
  About 40 participants (workers, engineers, teachers, and 
doctors). There are 11 people in the coordinating council. Pavel 
Kuzmich Likhachev, now the leader of the Ecology Group under the 
oblast Peace Defense Committee, was the head of the group at one 
time. Later its chairman was Valeriy Pavlovich Galenko. The 
responsible secretary is Nikolay Stepanovich Savukhin. 
  Task: to observe the ecological situation in Pavlodar and 
"achieve ecological harmony." 
  Forms of work are: organization of rallies, sociological 
research, and dissemination of appeals and articles on ecology 
and health care and on issues of "discrediting local party 
organs" (that means the CPSU before 1991). 
  The group opposed the construction in the city of a plant 
for 
producing BVK and gathered signatures of local residents in 
support of its demand. The decision to build the enterprise was 
rescinded. In November 1987 and in June 1988 they conducted a 
sociological survey of the residents of Pavlodar on their 
attitude toward perestroyka and in late 1988--on the ecological 
situation in the city. In 1989-1990 they opposed the 
construction of residential buildings in the floodplain of the 
Usolka River, conducted a public opinion poll, and suggested 
creating an ecological commission including experts from Almaty. 
  Gradually the EKOM began to be politicized. In December 
1989, 
V. Galenko was elected deputy of the oblast soviet and two other 
members of the group became deputies of the rayon soviet. The 
group had confrontations with the leadership of the city and the 
oblast (EKOM promoted the retirement of the chairman of the 
oblast soviet, Yu. Meshcheryakov). 
  Every week the group gathers in the assembly hall at the 
following address: city of Pavlodar, ul. Dzerzhinskogo, d. 46. 
It publishes a bulletin. 
  In August-September 1989 the group published two issues of 
the type-written NEZAVISIMAYA GAZETA in a 1*2 meter format and 
distributed the newspaper for exhibit on fixed stands. 
  There are groups of supporters at the aluminum, tractor, and 
chemical plants of Pavlodar and an affiliate in Ekibastuz (about 
10 people). 
  Is a member of the Social-Ecological Alliance (see article). 
  Address: 637021, city of Pavlodar, ul. 1 Maya, d. 284, kv. 
129, tel. 72-67-75, Valeriy Pavlovich Galenko; 637046, city of 
Pavlodar, ul. Suvorova, d. 12, kv. 131, Nikolay Stepanovich 
Savukhin. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., pp 61-62; 
  -  "Samodeyatelnyye 
obshchestvennyye organizatsii...," op. cit., pp 5, 21-22. 

<H5>    Petropavlovsk Oblast </H5>
<H5>  Nevada-Semipalatinsk </H5>
  This is the Petropavlovsk Oblast branch of the republic 
movement (see article). The organizational meeting occurred in 
December 1989. Numbers about 30 participants. The chairman is 
Omir Yeskaliyev. "Organized a number of actions and transferred 
the capital to support the antinuclear movement." 
  Address: 642026, city of Petropavlovsk, ul. Lenina, d. 11, 
editorial office of LENIN TUY, work tel. 36-28-08, 36-50-35, 
Omir Yeskaliyev. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., p 64. 

<H5>    Semipalatinsk Oblast </H5>
<H5>  Physicians Against Nuclear War </H5>
  This is a Semipalatinsk city society. Appeared in May 1989 
and was registered under the gorispolkom. The goal is to stop 
nuclear testing at the Semipalatinsk Test Range and to provide 
medical aid to people who have suffered from nuclear explosions. 
The society's by-laws and program correspond to similar 
documents of Physicians Against Nuclear War societies on the 
territory of Kazakhstan and all the former USSR. 
  The make-up includes for the most part instructors and 
students of the Semipalatinsk Medical Institute. Meetings are 
held four times a year at the medical institute. The chairman of 
the society is M. U. Iskakbayev, the chief doctor of the City 
Hospital No 1. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. 
cit., p 
25. 

<H5>    Nevada-Semipalatinsk </H5>
  This is the Semipalatinsk Oblast branch of the republic 
movement (see article), the most active and largest branch. The 
initiative group of 5-8 people took shape on 17-19 July 1989 
during the scientific-practical conference on the impact of 
nuclear testing on the health of local residents. In August the 
city branch (20 participants) was created. In December the 
founding conference of the oblast branch took place. The oblast 
branch was registered. There are 9 people in the coordinating 
council and about 20 in the aktiv. The chairman is M. M. 
Urazalin, the former party committee secretary and chief of a 
department of the Semipalatinsk Medical Institute. 
  Financed by the republic Nevada-Semipalatinsk Society. 
  The program and by-laws are similar to the Almaty documents. 
  By early 1991 the oblast branch numbered its subdivisions in 
roughly 10 populated points of the oblast. 
  On 6-7 August 1989 the Semipalatinsk Oblast branch together 
with the Almaty center organized the first antinuclear rallies 
in Karaul and Semipalatinsk and 5,000 and 10,000 people, 
respectively, participated. On 21 October, after the latest 
nuclear explosion, rallies were again organized in these cities 
with participation by more than 10,000 people. Antinuclear 
rallies were held later too, and in December a "tribunal" was 
held on the Semipalatinsk Test Range and in September 1990--a 
"Peace March." 
  Meetings are held once a month at the Semipalatinsk Medical 
Institute. 
  Address: city of Semipalatinsk, ul. Zasyadka, d. 88, kv. 21, 
tel. 3-07-15 (work), 6-89-80, Serikbol Rakhmanovich Musinov; 
tel. 2-73-49, 2-73-41 (work), M. M. Urazalin. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., p 66. 

<H5>    Alliance of Victims of Nuclear Testing </H5>
  This was created on 29 August 1990. The founders were the 
regional branches of the Nevada-Semipalatinsk Movement, the 
Peace Defense Committee, the Semipalatinsk oblast and city 
soviets of people's deputies, and others. 
  The goal is to aid people who have suffered from nuclear 
testing and to create a data bank on damage to health, the 
economy, and ecology. 
  The aktiv is more than 20 people. The alliance has a bank 
account. The by-laws were registered on 24 October 1990. The 
program of actions was accepted by late 1990. 
  Address: 490050, city of Semipalatinsk, ul. Sovetskaya, d. 
86, tel. 2-48-46. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., p 67. 

<H5>    Chernobyl Alliance </H5>
  This is the Semipalatinsk Oblast branch of the Chernobyl 
Alliance of Kazakhstan (see article). 
  The founding meeting was held in January 1991. Attending 
were 
150 people. The founders were the oblast council of trade unions 
and the Nevada-Semipalatinsk Movement. Unites participants in 
cleaning up the consequences of the accident at the Chernobyl 
AES. The goal is material and medical aid to residents of 
Semipalatinsk Oblast who suffered from the Chernobyl 
Catastrophe; there are more than 150 of them. Elected at the 
founding meeting was a committee of 15 people and the chairman, 
Veniamin Alekseyevich Slednikov. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  Ponomarev, V., op. cit., pp 67-68. 

<H5>    City of Stepnogorsk </H5>
<H5>  Public Committee To Assist Perestroyka </H5>
  Registered in 1989. There is a program and by-laws. The goal 
is to protect the environment. The aktiv consists of 20 people, 
intelligentsia, for the most part Russian in nationality. The 
leader is V. K. Kunilovskiy, a doctor of a military medical unit. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhusunov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennye organizatsii...," op. cit., 
p 
30. 

<H5>    Taldy-Kurgan Oblast </H5>
<H5>  City of Taldy-Kurgan </H5>
<H5>  Zhetysu" </H5>
  This is an ecology association. Formed in 1989 and 
registered 
under the oblast ispolkom. The goal is to defend the environment 
in Taldy-Kurgan Oblast. The aktiv is 23 people (of various 
nationalities). Meetings are held once or twice a month at the 
premises of the Nature Protection Society. 
  The leader is K. Zh. Abdrakhmanov, correspondent of the 
newspaper OKTYABR DUY. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvenyye organizatsii...," op. cit., 
pp 
26-27. 

<H5>    Uralsk Oblast </H5>
<H5>  City of Uralsk </H5>
<H3>  Eureka Scientific-Apprentice Society of Ecology and Regional 
Studies </H3>
  Conducts ecological research and is involved in ecological 
education. Member of the Social-Ecological Alliance (see 
article). 
  Address: 417003, city of Uralsk, ul. Tyulenina, d. 52, kv. 
45, tel. 3-28-95, A. M. Panchenko. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2. 

<H5>    Tselinograd OblasT </H5>
<H5>  Nevada-Semipalatinsk </H5>
  This is the Tselinograd Oblast branch of the republic 
movement (see article). Created and registered in 1989. Has a 
program and by-laws. About 40 participants, for the most part 
intelligentsia and students. 
<H6>  Sources of Information </H6>

  -  Archives of A. M. Dzhunusov; 
  -  IMPD Archives, Fund 2; 
  -  "Samodeyatelnyye obshchestvennyye organizatsii...," op. 
cit., p 
30. 

<H5>    Kyrgyzstan </H5>
<H5>  City of Bishkek (Frunze) </H5>
<H5>  Ecologist" Club </H5>
  It was formed on 17 August 1987 at a rally and meeting in 
Gorky Park in the city of Frunze (Bishkek). It has 60 members. 
  The club engages in ecological education, studies public 
opinion, and collects and disseminates ecological information. 
It monitors the state of the environment and performance of 
decisions of the authorities on ecological questions. 
  The club does ecological studies of new industrial 
enterprises and organizes protest campaigns. 
  It engages in sociopolitical activity (participation in 
elections and the like). 
  The club is a member of the Social-Ecological Alliance (see 
article). The cochairmen are V. Kopylenko and G. Kozeyev. In 
early 1990 the club was subjected to persecution by the 
authorities and then fell apart. Some participants continue to 
work in the Social-Democratic section. 
  Address: 720027, City of Bishkek, ul. Kuzbasskaya, d. 102, 
Gennadiy A. Kozeyev; tel. 25-74-37, Vladimir Matveyevich 
Kopylenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Latvia </H5>

<H5>  Environmental Defense Club ("Vizes Aizsargs Klub"--VAK) </H5>
  Its tasks are protection of nature and monuments of ancient 
days, as well as political goals. It was formed in 1980. 
Initially it brought together participants in the restoration of 
architectural monuments. Evening meetings and guitar concerts 
were held in restored Catholic churches. In 1984 they joined 
into a group named the Center for the Defense of Monuments. The 
members of the center studied folklore and forgotten and 
forbidden writers and became involved in ecological issues. On 
25 February 1987 the center was officially registered under the 
name Environmental Defense Club. 
  On 10 October 1987 the club conducted its first ecology 
rally, called "For Clean Air," outside the VEF [Valst Electrical 
Engineering Plant]. The authorities tried to stop the club's 
activities, but could not. At one time club meetings were held 
at the University, but club members were driven out there and 
from other premises as well. Then they began organizing weekly 
meetings in parks, usually Arkadiy Park. They once held a rally 
outside the House of Political Education. 
  At that time the club was the largest independent 
organization in the republic. People of different political 
convictions gathered around it. In 1987-1988 more radical people 
than before began to predominate in the club leadership; they 
created an organizational structure that permitted the 
implementation of radical political decisions. 
  In 1987 in Riga the club organized the first demonstration 
(in Latvia during the Soviet years) against construction of a 
subway in Riga. The participants believed that construction was 
not justified from an economic standpoint. Moreover, it could 
have impaired the appearance of the old city. Despite being 
prohibited the demonstration was held. The participants marched 
through the entire old city. As a result the decision to build 
the subway was withdrawn. 
  A week later VAK organized an ecological demonstration 
against pollution of the Jurmala coastline by the Slok Pulp and 
Paper Combine. The next demonstration was directed against 
construction of an atomic power plant. Branches of the club were 
formed in the port cities of Ventspils and Lijepaja (inhabitants 
of these cities took part in VAK demonstrations). In Vidzem in 
northeastern Latvia the club organized actions in support of 
preserving the natural area near the Gauya River. 
  The ecological demands were taking on a political coloring. 
  On 16 July 1988 a rally was held in Mezhapark demanding 
restoration of the national symbols of Latvia. About 50,000 
people took part. On 3 September "hundreds of thousands of 
people all along the Baltic coast" came to the seacoast for a 
public prayer meeting. 
  "By the end of the summer of 1988 VAK reached its political 
apex." VAK activists took part in the organization of the 
Latvian People's Front and the Movement for the National 
Independence of Latvia. A large share of the radical 
participants in the club began acting within these 
organizations. The club began to become less political. The 
formation of the Latvian Greens Party (see article) in early 
1990 was the next step along the path "from a politicized 
organization to the club of dedicated amateurs that it had been 
in the beginning." 
  The club today does not have a rigid structure. Its 
activities are "distinguished not so much by good organization 
as by good fantasy." They are usually conducted outdoors, "far 
from the closed halls in which the politicians gather." VAK 
organizes picketing, sometimes outside military installations, 
and ecological protests to stop actions. In 1990, for example, 
the club organized picketing in Saldus District where a firing 
range was set up in an old cemetery and corpses flew into the 
air during exercises. 
  In the fall of 1991 the club, together with the Latvian 
Republic Committee for Environmental Defense (see article), the 
Latvian Greens Party (see article), and the Vieda Publishing 
House of Ecological Education conducted the second "Green 
Logicians" conference in order to invigorate the Greens movement 
in the republic. 
  The president of the club is A. Ulme. The club puts out the 
journal STRABURAGS. VAK includes the Environmental Defense Club 
of the city of Lijepaja (see article) and the Environmental 
Defense Club of the city of Jurmala (see article). 
  Addresses: 226046, city of Riga, ul. Kalnstiyemas, d. 30, 
Klub Zashchity Sredy, tel. 61-28-50 (work), Arvids Ulme; 226098, 
city of Riga, 6-p Rainisa, 19, Molodezhniy Ekotsentr LatGU, tel. 
61-28-50, Arnis Brunovich Brumelis; 226009, city of Riga, ul. 
Lienas, d. 9, kv. 11, tel. 29-11-67, Dzintar Oskarovich Bush; 
226014, city of Riga, pr. Mezha, d. 1, Rizhskiy zoosad, 
laboratoriya ekologii, V. A. Vilpitis; 229073, city of Jurmala, 
ul. Marupes, d. 11, tel. 65-38-86 (home), Anda Aispoka; 
Information Department, tel. 46-58-75, 61-28-50 (work), Jaanis 
Legzdins, tel. 53-15-86, 61-28-50 (work), Maris Svilans. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2; 
  -  "Digest," SPASENIYE, No 8, August 1991, p 3; 
  -  Kudryavtsev, I., 
"Spravochnik politicheskikh i obshchestvennykh organizatsiy 
Latvii s kommentariyami" [Index of Latvian Political and Social 
Organizations], Moscow, Moskovskoye Obshchestvennoye Byuro 
Informatsionnogo Obmena, 1990, pp 20-21. 

<H5>    The Environmental Defense Committee </H5>
  After the first "Green Logicians" conference, which was held 
in Latvia in 1989, the committee became independent of the 
government. In the fall of 1991 it, along with other Latvian 
ecology organizations (the Latvian Greens Party [see article], 
the Environmental Defense Club [see article], and the Vieda 
Publishing House of Ecological Education) called the second 
"Green Logicians" conference. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Digest," SPASENIYE, No 8, August 
1991, p 3. 

<H5>    The Latvian Greens Party </H5>
  The political representatives of the Greens movement in the 
Supreme Soviet of Latvia. "The leadership of the LGP is 
convinced that an independent Latvia is a prerequisite to 
solving ecological problems." But there were disagreements 
within the LGP on the ways to achieve independence, through 
parliament or through citizens committees. 
  The party was formed after the first "Green Logicians" 
conference, which took place in Latvia in 1989. The first 
meeting of the LGP initiative group was held in the late fall of 
1989. The founding congress was on 14-15 January 1990; it was 
officially registered. The founders were VAK (the Environmental 
Defense Club--see article), the Youth Center at LGU [Latvia 
State University] (see article), and other organizations. 
  The party's goals are set forth in its Manifesto, which 
announces the formation of the Greens Party (the Manifesto was 
adopted at the founding congress of the party): "transition of 
the economy from agroindustry to agroculture and from large 
production facilities to small and medium-sized enterprises. The 
current priority of the economy must give way to the priority of 
life, and the consumption society must become a preservation 
society. The path to this lies in overcoming the indifference of 
the hired worker, making him a proprietor of the land, and 
through making ecological awareness a part of people's 
thinking." By early 1990 the LGP program was in the development 
phase, and it was expected to be adopted at the next party 
congress in July 1990. Party members consider the Manifesto a 
statement of the "principles of the Green philosophy," which set 
"remote goals." But the program should be a "very concrete 
document." 
  The total membership at the start of 1990 was about 100, and 
by the summer of 1991 it was 3,000. The party by-laws envisions 
the status of full members of the LGP and the status of 
nonvoting party supporters. The party has formed a temporary 
coordinating council (one of its members is Karlis 
Overtedzh-Gudermanis). LGP members cannot belong to other 
parties. About 60 percent of party members at its inception were 
activists from the Environmental Defense Club. All three 
cochairmen of the LGP (among them Juris Zvirgzds and Valts 
Vilnitis) are members of the Club Duma and the Club president 
and both vice presidents are LGP members. This illustrates the 
interpenetration of the structures of the two organizations. But 
the Club is involving primarily in organizing protests and 
picketing, while the party engages in work in parliament. 
  In the elections to the Latvian Supreme Soviet in March 
1990, 
seven of the eight deputy candidates from the LGP were elected. 
The goal of the parliamentary "Green" faction is "legislation to 
protect the environment, to protect human beings in this 
environment, and to preserve the peace as a prerequisite to 
achieving all of this." 
  In the fall of 1991 the party, along with other Latvian 
ecology organizations--the Environmental Defense Club (see 
article), the Committee for Environmental Defense (see article), 
and the Vieda Publishing House of Ecological Education, called 
the second "Green Logicians" conference in order to invigorate 
the green movement in the republic. 
  The LGP also collaborates with the Latvian People's Front. 
  Addresses: 226083, city of Riga, ul. Darza, d. 48, kv. 3, 
tel. 45-23-48, Igor Mey; 226046, city of Riga, ul. Kalntsiemas, 
d. 30, tel. 61-28-50. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Digest," SPASENIYE, No 8, August 
1991, p 3; 
  -  "Zelenyye v SSSR. Krupneyshiye...," op. cit., pp 
20-21; 
  -  "Overcoming Indifference," SPASENIYE, No 8, August 1991, 
p 2; 
  -  Kudryavtsev, op. cit., pp 28-29. 

<H5>    City of Riga. </H5>
<H5>  Youth Ecological Center of Latvia State University </H5>
  It was formed in 1988 at the Latvian Youth Center. 12 
members. They engage in teaching and public education, conduct 
expert studies, and carry on agitation work at the university. 
  The activists of the ecocenter are Raimonds Ernshteinis and 
Arnis Brumelis. 
  Addresses: 226011, city of Riga, ul. Dzirnavu, d. 66, kv. 
28, 
tel. 28-53-51, Raimonds Ernshteinis; 226098, city of Riga, 6-p 
Rainisa, d. 19, ibid. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Society for the Protection of Nature and Monuments </H5>

  An ecological-cultural organization. It takes action against 
the destruction of monuments of ancient times, participates in 
their restoration, and takes part in events conducted in the 
city in defense of nature. 
  Address: 226000, city of Riga, ul. Gorkogo, d. 85, tel. 
22-59-54 (home), Vita Georgiyevna Zablovska. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Lijepaja </H5>

<H5>  Environmental Defense Club of the City of Lijepaja </H5>
  Member of the republic Environmental Defense Club (see 
article). 
  Address: 229700, city of Lijepaja, ul. Klaipedas, d. 68, kv. 
7, Inese Eistere. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Jurmala </H5>

<H5>  Environmental Defense Club of the City of Jurmala </H5>
  Member of the republic Environmental Defense Club (see 
article). It takes action against industrial pollution of the 
coast. 
  Address: 229073, city of Jurmala, ul. Marunas, d. 11, tel. 
65-38-86, Anda Anspoka, publisher of the journal STRABURAGS. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Lithuania </H5>

<H5>  "Atgaja" Club (Society) </H5>
  In translation "atgaja" means freshening [of the air] or 
sprout or shoot [of a plant]. 
  The club was founded in 1987. It emerged as the result of 
the 
joining of the Kaunas Ecology Club and the nature protection 
club. It was registered at the Komsomol Committee in 1988. The 
registration papers list about 500 members. The group of 
activists is 50-60 persons. 
  The age range is from secondary school to pensioners. "In 
activities 15-year-old students walk side by side with 
professors, punks with pensioners." 
  The management organ is a council of six persons headed by a 
chairman. The council is elected each year. 
  The society consists of two groups: Greens and the monument 
preservation group. 
  Goals and tasks: "Atgaja tries by all humane means to 
preserve environmental balance and preserve monuments of culture 
and the natural world." 
  Atgaja is involved above all with monuments that are 
perishing, neglected, or being specifically destroyed. It 
participates in the preparation and adoption of drafts and laws 
on protection of cultural monuments and the environment. 
  It organizes lectures, exhibits, and propaganda actions. It 
conducts activities in ecological education and antiwar 
indoctrination. It promotes the "Green" way of life. 
  An official newspaper of the society is published. 
  Activities: 
  1986-1988--numerous actions and a constant "struggle" with 
the city authorities for preservation of St. Gertrude's Catholic 
Church, a monument of 17th century architecture. Restoration and 
establishment of a museum in the 18th century house in which an 
outstanding Lithuanian linguist lived. 
  1988--the ecological protest march through Lithuania. The 
purpose was to show the republic's hotspots to the people, to 
study the Neris, one of the largest rivers, and to determine the 
condition of monuments and the environment. 
  The marches have become traditional. The "Living Ring of the 
Baltic," an action to save the Baltic Sea, has been conducted 
since 1988. 
  Summer of 1989--peace march along the same route and 
further. 
The goals were the same, plus antiwar propaganda. 
  August-September 1989---protracted picketing stopped 
construction of the Nemen military installation. 
  In 1988-1989 construction of 5-8 units of the Kaishiador 
GAES 
[pumped-storage electric power plant] on the Nialunes River was 
stopped; numerous actions were conducted throughout Lithuania to 
accomplish this. They took part in various actions as the result 
of which construction of the third power unit at the Ignalin AES 
was suspended. They conducted many volunteer work days, cleaned 
up illegal dump sites on river embankments, planted trees, and 
worked on saving the oak park in Kaunas. 
  In 1989 four members of Atgaja went on a hunger strike, 
demanding an immediate start to construction of decontamination 
facilities for the city of Kaunas. 
  The symbolic fee to join Atgaja is R3-R5. The sponsors of 
its 
actions are various institutions, organizations, and especially 
plants that produce chemical products. Atgaja also gets funds 
from donations. The sponsors of the peace march were the 
chemical plant in Kedlpiai (R15,000), the chemical fertilizer 
plant in Ionova (R15,000), the Peace Committee (R10,000), and 
others. Atgaja pays for the restoration of monuments, conducts 
"Green" schools, and helps the poor, old people, and large 
families. 
  Atgaja is a member of the Greens Movement of Lithuania (see 
article). It has collaborated with Sajudis since its beginning 
(1988). S. Gricius (long-term chairman of Atgaja) and S. Piksris 
(chairman of Atgaja) are members of the Sajudis council. Atgaja 
participates in the activities of the Lithuanian Cultural 
Foundation. 
  Addresses: Lithuania., 233008, Kaunas, 5, Neries Krantine 
4-13, Saulius Gricius; 234320, Lithuania, Kuanas-Ravoondvaris, 
Kalnu, 2, Gintarac Zeizys, tel. 54-96-22; city of Kaunas, tel. 
208-58-85 (r.), Sajudis Piksris; city of Vilnius, tel. 77-24-46 
(r.), 26-08-01 (or 26-09-01) (d.), Ludis Grakauskas, council 
member. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Letter to GKP dated 18 January 
1990. 

<H5>    The Greens Movement of Lithuania </H5>
  It was founded in late 1987 and registered in the spring of 
1989. The total membership is more than 10,000. Its source of 
financing is dues. The GML is a member of Sajudis and of the 
International Greens Movement and enjoys the support of the 
Lithuanian Academy of Sciences. 
  The GML disseminates its information through the 
Lithuanian-language newspaper GREEN LITHUANIA (published since 
March 1989) and the monthly 1-hour television program "Green 
Wave." 
  Prehistory: In late 1987 the first Ziamina Ecology Club (see 
article) in Lithuania appeared in Vilnius, and by June of 1988 
two more similar clubs were formed in Lithuania, in Kaunas and 
Klaipeda. On 5 August 1988 at a meeting of representatives of 
the Vilnius and Kaunas clubs it was decided to form the republic 
Greens Movement. 
  The movement held debates on the Ignalin AES and the 
condition of the Niamunas River delta; they drew a large 
response. 
  On 4 September 1988 the movement together with the Latvian 
Greens organized a human chain along the coast of the Baltic Sea. 
  The movement's first congress was held on 30 April and 1 May 
of 1989. The congress was attended by 150 delegates. They 
adopted a by-laws and a program and elected an 11-person 
coordinating council and a parliament (17 consultants and one 
representative from each of the 70 ecology clubs of Lithuania). 
The first chairman of the GML was Arturas Abromavicius, followed 
by Aidas Vaisuras. Among the members of the GML coordinating 
council are Professor Zigmas Zigmovich Vaisvila, people's deputy 
of the USSR, and Girginius Vitautovich Jakubauskas, chief 
specialist in ecology for the nature protection department of 
the Institute of Planning for Industrial Construction. 
  Thanks to the activities of the movement: 
  --expansion of the Ignalin AES was prevented; 
  --construction of the Kaunas GES was delayed; 
  --the quality of food products was improved by organizing 
republic-wide boycotts, for example the milk boycott conducted 
in the republic in the winter of 1989. 
  Addresses: 232042, city of Vilnius, ul. Kalvariu, d. 130, 
kv. 
48, Aidas Vaisuras; 232600, city of Vilnius, pr. Gedimino, d. 3, 
tel. 22-55-44 (work), Arturas Abromavicius, Saulus Lapinis; 
2320235, city of Vilnius, ul. Taikos, d. 87, kv. 30, tel. 
42-39-23 (home), Zigmas Zigmovich Vaisvila; city of Vilnius, 
tel. 76-67-37, fax 76-67-37; city of Vilnius, tel. 76-94-69 
(work), 77-86-55 (home), Jonas Tamulis; city of Vilnius, tel. 
73-03-67 (work), 42-39-23 (home), Zigmas Zigmovich Vaisvila; 
town of Girenis, tel. 20-86-12 (work), Girginius Vitautovich 
Jakubauskas. 
<H5>  Sources of Information </H5>

  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. 
Krupneyshiye...," op. cit., p 21. 

<H5>    Lithuanian Nature Protection Society (LNPS) </H5>
  "A voluntary, mass, public organization." Its goal is to 
involve the public in nature protection work, help in 
identifying natural wealth, and multiply it and ensure its 
rational use. 
  The tasks of the society, according to its by-laws, which 
was 
adopted in 1984, are: 
  --"propaganda for party and government decrees on the 
question of nature protection and indoctrination of the 
population with a communist attitude toward nature and its 
protection"; 
  --"implementation of public monitoring of the use of 
natural wealth." 
  To accomplish its tasks the LNPS publishes and distributes 
appropriate literature and organizes lectures, exhibits, special 
months devoted to nature protection, planting, contests, and 
other large-scale activities. It develops plans and outlines for 
fixing up and landscaping areas, consults on these matters, and 
provides assistance in planting the grounds of kolkhozes, 
sovkhozes, industrial enterprises, and so on. 
  It collaborates with the State Committee for Nature and the 
Lithuanian Academy of Sciences and maintains contacts with the 
Nature Protection Societies of other former Union republics. 
  The structure, staff size, and monthly wages fund of the 
Republic Council of the Lithuanian Nature Protection Society are 
ratified by the Lithuanian Council of Ministers. 
  The membership is varied. Persons who have reached the age 
of 
16 and who take part in LNPS activities may become members of 
the society; children under the age of 16 can be young members 
of the society. People are admitted to the LNPS by the primary 
organizations, while collective members are admitted by the 
presidium of the council of the rayon (or city) branch of the 
society. 
  Members of the LNPS have a membership card and pin of a 
design established by the LNPS. 
  LNPS members may be rewarded, under established procedures, 
with certificates of honor, distinguished service pins, and the 
title of honored member of the society; gratitude to them may be 
expressed formally. Employees and activists of the LNPS may also 
receive bonuses in the manner established by the Lithuanian 
Council of Ministers from funds allocated for this purpose. 
Social measures may be employed for violation of the LNPS 
by-laws, all the way to expulsion from the society. 
  Structure: 
  The highest body is the LNPS congress, which meets at least 
once every 5 years. An extraordinary congress may be called on 
the demand of at least one-quarter of the local branches. A 
congress is empowered if more than two-thirds of the delegates 
participate in it. 
  The congress elects the republic council and auditing 
commission of the LNPS. The republic council calls a plenum at 
least once a year. An extraordinary plenum is called on the 
demand of at least one-third of the republic council or the 
central auditing commission. 
  The executive body is the LNPS presidium. 
  Local organizations: rayon and city divisions of the 
society. 
The highest body is the rayon (city) conference, which is held 
every 2-3 years. The conference is empowered if at least 
two-thirds of the delegates attend it. The conference elects the 
council and the auditing commission of the society. The council 
of an LNPS branch elects a presidium of the council, chairman, 
deputy, responsible secretary, and executive body--the 
presidium. The auditing commission reports to the conference. 
  Primary organizations are formed at enterprises, 
institutions, and sovkhozes where there are at least five LNPS 
members. The highest body is the meeting of members, which is 
called at least once a year. The meeting elects the chairman and 
cashier. 
  Resources: initiation and membership dues, income from 
publishing activity, voluntary donations, and other monetary 
means. 
  Initiation fee--10 kopecks; annual dues--50 kopecks, but 20 
kopecks for college and secondary students (trade-vocational 
schools and others) and R50 a year for collective members. 
Honored members of the LNPS do not pay dues. They themselves 
establish the particular amount. 
  The LNPS ceases activity on the decision of its congress or 
by order of the Lithuanian Council of Ministers. 
  Address: 232001, city of Vilnius, ul. Ju. Janonis, d. 4. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Party of Lithuania (GPL) </H5>

  Registered. Tasks are the struggle for civil rights, a free 
society, ecological balance, and international solidarity. 
  The session of the Greens Movement of Lithuania (see 
article) 
on 1-2 July 1989 adopted the decision to form a political party 
and that it should take part in elections for the Lithuanian 
parliament and local councils. 
  The founding congress of the GPL took place in Vilnius on 
16-17 June 1990. 150 delegates attended. They elected management 
organs: a council of 11 persons, and a board of directors of 3 
persons (Zigmas Vaishvila as chairman, plus Irena Ignataviciune 
and Romuldas Juknis). 
  The party publishes information about the ecological 
situation in Lithuania and exposes the actions of the military 
authorities. Its press organ, the newspaper POLUSVIRA (Balance), 
has been published since the fall of 1989 in Panevezis. 
  The party is represented in the Lithuanian Supreme Soviet. 
  Addresses: 232000, city of Vilnius, ul. Radvilaites, d. 1, 
Irena Ignataviciune; 232001, city of Vilnius, ul. Pilimo, d. 4, 
tel. 61-14-15, 26-43-44 (home), Zigmas Vaisvila; city of 
Vilnius, tel. 22-62-68 (work), Vida Kisuniane; City of Vilnius, 
tel. 64-10-72 (work), Rimantas Astrauskas; City of Tautininkai, 
tel. 26-43-44, Rimas Matulis. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. 
Krupneyshiye...," op. cit., pp 21-22. 

<H5>    City of Vilnius </H5>
<H5>  "Ziamina" </H5>
  The first Lithuanian ecology club. Its founding conference 
was held in late 1987 in Vilnius. The conference adopted a 
by-laws according to which the "club has the right to organize 
rallies, picketing, and demonstrations in cases of ecological 
disasters and catastrophes." Members of the club are mainly 
young scientists of the Lithuanian Academy of Sciences. 
  The club organized public debates on the ecological problems 
of the Ignalin AES and the Niamunas River delta, "which brought 
about a real explosion of public opinion in Lithuania." Club 
representatives took part in the 5 August 1988 meeting at which 
the decision was made to form the Greens Movement of Lithuania 
(see article). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Zelenyye v SSSR. 
Krupneyshiye...," op. cit., p 21. 

<H5>    City of Zarasai </H5>
<H5>  "Azuolas" (Oak) Ecology Club </H5>
  The club monitors environmental preservation, the quality of 
food products and consumer goods, and public health. It develops 
alternative plans, designs, and technologies. It organizes 
ecological education, the study of public opinion, and the 
collection and dissemination of ecological information. 
  Address: 234780, city of Zarasai, ul. Siauliu, d. 5, kv. 22, 
tel. 5-34-30, Robiartas Jukniavicius. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Mazeikiai </H5>

<H5>  Greens Club of the City of Mazeikiai </H5>
  The club monitors environmental preservation, the quality of 
food products and consumer goods, and public health. It 
organizes ecological education, the study of public opinion, and 
the collection and dissemination of ecological information. 
  Address: 235500, city of Mazeikiai, ul. Naftininku, d. 14, 
kv. 56, A. Kukuliekis 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Siauliai </H5>

<H5>  Siauliai Club for the Protection of Monuments and Nature </H5>
  Ecological-cultural organization. It takes action against 
the 
destruction of monuments of ancient times, participates in their 
restoration, and also takes part in activities conducted in the 
city in defense of nature. 
  Address: 235406, city of Siauliai, ul. Kosmonautu, d. 77, 
kv. 
66, Rimas Braziulis. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Moldova </H5>

<H5>  "Zimbru" Republic Ecology Club </H5>
  Member of the Social-Ecological Alliance (see article). 
Participates in solving problems of industrial pollution. 
  Address: 277019, city of Chisinau, 5-y Agronomicheskiy pr., 
d. 13, kv. 2, tel. 56-78-89, Mikhail Poyag. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 1. 

<H5>    Inter-Oblast Committee To Defend the Prut River </H5>

  It was founded in 1989. It conducts ecology field trips. It 
is a member of the Social-Ecological Alliance (see article). 
  Address: 277000, city of Chisinau, ul. Demokraticheskaya, d. 
6/2, kv. 23, Vasile Nestase. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Moldavian Greens Movement ("Aktsiunya Verde" [AVE], Greens </H5>

Movement of Moldova) 
  It was founded in November 1988 with the aid of the 
Moldavian 
Nature Protection Society (see article) and was registered in 
1990. 
  It uses ecological causes as the beginning of political, 
social, and ecological reforms. 
  According to the by-laws of the AVE and the materials of the 
founding conference (August 1989): 
  The AVE is a radical, democratic, civil initiative to 
surmount the ecological crisis, eliminate the deadly 
technocratic model of nature use, and mold an ecological, 
evolutionary way of life; 
  the AVE is a self-governing public movement that is 
"realizing the right of the people to a healthy living 
environment." 
  It works together with all people and organizations within 
the framework of its by-laws. 
  It is structured according to the principles of democratic 
centralism. It rejects violent acts, chauvinism, nationalism, 
and other forms of discrimination. 
  Its goals are: 
  --"to awaken the general human conscience and the feeling 
of humanism, cultivate biospheric ('green') ethics, and raise 
new generations of people on these grounds"; 
  --"to combine the interests of defending peace, the 
homeland, and nature. To strive for the elimination of nuclear, 
chemical, and bacteriological arsenals and abolition of the 
chemical strategy in agriculture"; 
  --"to oppose the actions of the departments which are 
aggravating the biospheric and demographic situation in Moldavia 
and throughout the Dniester basin"; 
  --"to defend the interests of the region from the 
standpoint of the ethnocultural rights of the population for 
whom the region is their homeland." 
  To achieve its goals the AVE holds conferences and other 
public-scientific forums on ecology, conducts demonstrations, 
rallies, and other actions in defense of nature as well as 
public discussions, works for implementation of existing laws, 
cooperates closely with people's deputies at all levels, 
organizes free labor actions and charitable measures, and 
participates actively in them. 
  The AVE is setting up an environmental data bank. It brings 
lawsuits against departments and others who violate nature 
protection laws. Where necessary it prepares alternative plans. 
It works toward the recall of deputies who do not carry out 
their duties. 
  It founded the Greens Foundation and other societies. It 
organizes public protests against AES's and is conducting a 
study of the Prut River together with Romania. 
  The structure of the AVE: 
  Its highest body is the republic ecoforum, which comprises 
representatives elected by the primary organizations. It gathers 
once a year and, when necessary, in extraordinary session within 
1 month when demanded by at least three-quarters of the members 
of the initiative group. 
  Between ecoforums the movement is directed by the initiative 
group, headed by the chairman of the presidium or his deputy. 
The group elects, from its own members, the AVE presidium, its 
chairman, two deputies, and a secretary, with 2-year terms. 
  The activities of the AVE are carried on primarily through 
the primary elements, and also by means of the problem 
commissions that are created. In addition to the problem 
commissions the initiative group forms a republic problem-debate 
club and directs its work. 
  In their ongoing activities the rayon (city) subdivisions 
are 
independent on the condition that they regularly coordinate them 
within the framework of the republic AVE. The rayon (or city) 
AVE society is directed by the corresponding initiative group 
(headed by a presidium and auditing commission). 
  Money is received from the activity of cooperative, 
contracting, and other economic subdivisions; from the sale of 
articles and memorabilia, and income from AVE activities. The 
AVE uses revenue received by the Greens Foundation from the 
subsidies and voluntary donations of organizations, 
institutions, and private persons. 
  AVE money is used for development of the movement, to pay 
for 
the work of experts, to organize contests, as prizes and 
bonuses, and to pay associates. 
  The membership: 
  A citizen of the republic who recognizes the by-laws and has 
reached the age of 16 may be a member. Admission to membership 
is done in two stages through the primary elements: persons who 
have been active in defending the environment are enrolled as 
competitive members of AVE (on submission by the primary 
element), and from these competitive members people are selected 
for admission to full AVE membership. 
  A full member "understands the ecological way of thinking, 
always acts in conformity with convictions and principles 
developed on its basis, actively disseminates AVE ideas, has not 
besmirched his own personal moral image in any way, has been 
admitted into AVE membership on the basis of a personal 
application and two recommendations from AVE members of at least 
1 year's standing (at first they were from confirmed 
environmentalists known to the public of the republic)." 
  Collective membership with the rights of AVE supporter is 
encouraged and does not change the individual membership. The 
AVE joins together ecology clubs, cooperatives, and societies. 
  Full AVE members who by their activities and behavior 
compromise society or do not fulfill their obligations are 
expelled from AVE membership by decision of the ecoforum (a 
majority of two-thirds of the votes of the delegates present). 
Competitive members can be expelled in the primary element (by a 
majority of two-thirds of the votes) or on the initiative of the 
ecoforum. 
  The AVE is a member of the Social-Ecological Alliance (see 
article). It is a part of the world Greens Movement and also of 
the Greens Movement that is operating in the territory of the 
former USSR (see article). 
  It publishes a newspaper (officially registered). The AVE 
has 
its own logo and other symbols. 
  Address: 277028, city of Chisinau, ul. Dzerzhinskogo, d. 64, 
korp. 4, kv. 21, Valentin Bobeyko; tel 44-38-84, George 
Malarchuk--president; city of Novyye Aneny, tel. 57-16-85 
(work), Aleksandr Fedorovich Sefer. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Moldavian Nature Protection Society (MNPS) </H5>

  It was formed on 30 November 1950. By 1987 it had 1.2 
million 
members and 4,500 primary organizations. Collective members 
comprise 1,850 enterprises, kolkhozes, sovkhozes, and 
construction and other organizations. There are 30,000 
activists, 1,725 lecturers, 2,000 detachments of "green" and 
"blue" patrols, and 90 school forestry groups that involve 3,500 
students. 
  Its primary tasks are: providing active assistance to state 
organs in implementing measures related to the protection and 
scientifically substantiated, rational use of natural wealth and 
improvement of the environment; multiplying natural wealth, 
planting in populated points, along roads, and so on; organizing 
and implementing public monitoring of the extent of use of 
natural resources and their preservation; propagating knowledge 
of nature. 
  The MNPS carries on its work through a broad network of 
primary organizations. 
  As a rule the rayon and city divisions of the society make 
370-400 surprise inspections a year checking on preservation and 
rational use of land and water resources and protection of 
atmospheric air and monitoring correct use of toxic chemicals. 
  Each year they conduct 7-8 contests, among which the 
following can be singled out: "For the best primary organization 
of the society," "Birds--Our Friends," and "Nature through the 
Eyes of Children." 
  Together with the State Committee for Nature, Agroprom, and 
other organizations MNPS conducted annual competitions "For best 
performance of techniques for controlling soil erosion, raising 
soil fertility, and using land rationally." In 1985-1988 the 
winners of the prize included the Kaushanskiy Economic Planning 
Sovkhoz-Tekhnikum, the Tsvetushchaya Moldaviya Sovkhoz-Tekhnikum 
of Viticulture, and others. 
  In addition, each year they conducted a contest for best 
treatment of the topic of nature protection in the periodical 
press, radio, and television. In 1985 2,548 articles were 
published in this connection; the newspaper VYATSA SATULUY told 
about the contest in greatest detail. 
  People's universities of nature are operating in 49 rayons 
and cities of the republic. They have about 4,000 students. 
  On 27 July 1989 they adopted this decision: "The Seventh 
Congress finds that perestroyka and the wave of renewal have had 
a positive effect on MNPS activities. The conscious 
participation of MNPS members and young friends of nature in 
practical nature protection activities is becoming more 
vigorous." 
  According to the by-laws individual MNPS members have the 
right to elect and be elected to congresses and conferences and 
to the governing and auditing bodies of the society; to receive 
consultation and training in schools and people's universities 
organized by MNPS, and to use the society's library. MNPS 
members are obligated to stay on the roll and participate 
actively in society activities, to propagate the tasks of MNPS, 
to attract new members, and to pay annual dues. If people do not 
pay dues during the year and do not work in the society, they 
are expelled from MNPS. 
  Collective members have the right to allocate 
representatives 
for participation in different organs of the society. They are 
obliged to "carry on explanatory work about the points of the 
CPSU Program and decrees of the Party and Government on 
questions of nature preservation and the goals and tasks of the 
society, to disseminate knowledge about nature," and so on. 
"Collective members may be released from payment of membership 
dues with the knowledge of the appropriate ispolkom of the 
soviet of people's deputies and by decision of the presidium of 
the council of the rayon or city branch." 
  Certificates of honor and valuable gifts are given to MNPS 
members for active participation in nature protection work and 
their names are put on the Honor Board and in the society's Book 
of Honor. 
  Organizational structure: 
  The highest body is the congress of the society, which is 
convened once every 5 years and selects the republic council. 
The republic council elects the presidium, the executive organ. 
The auditing commission is elected from MNPS members who do not 
belong to the republic council. The RC is subordinate to the 
congress. 
  Local organizations. By decision of the presidium of the 
republic council rayon and city branches are formed in the 
rayons and cities of republic subordination. These branches are 
subordinate to the MNPS republic council and its presidium. The 
highest body of the branches of the Moldavian society is the 
rayon or city conference, which is held at least once every 2-3 
years. Other than this the rayon and city branches copy the MNPS 
structure. 
  Primary organizations. They are formed at various 
institutions and organizations where there are at least five 
members. The highest body of the primary organization is the 
general meeting, which is convened at least once a year. All 
questions in MNPS are decided by open ballot. If the primary 
organization has more than 15 members, they elect an auditing 
commission. The auditing commission elects its chairman and 
secretary. 
  Attached to the presidium of the republic council there are 
scientific-technical councils, an editing and publishing 
council, and six volunteer sections: preservation of the earth 
and its interior; atmospheric air; fauna; flora and monuments of 
nature; the use of pesticides; and a youth section. They provide 
methodological guidance for the work of all rayon and city 
branches. 
  They have conducted socialist competition between the rayon 
and city branches of the society under the slogan, "For a 
stewardly attitude toward nature." 
  Resources: initiation and membership dues (initiation fee of 
15 kopecks, annual dues of 30 kopecks; college students pay 5 
and 10 kopecks, respectively; secondary students do not pay; for 
collective members the initiation fee is R20 and membership dues 
are R50; the republic council can lower the amount of dues); 
income from production, trade, and publishing activity, 
lectures, courses, exhibits, and other activities; income from 
property that belongs to the society; voluntary donations, and 
revenue. 
  Address: 277014, city of Chisinau, ul. Sadovaya, d. 31, Code 
8-042-2; tel. 21-35-32, Aleksandr Andreyevich Barkar, deputy 
chairman; tel. 24-14-87, Fedor Telker, responsible secretary. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  MNPS By-Laws. 

<H5>    Ecology Section of the Moldovan Journalists Union </H5>
  It engages in ecological education and uses the mass 
information media to propagate ecological knowledge and 
criticize violations of nature protection law. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 277000, city of Chisinau, ul. Pushkina, d. 22, Dom 
pechati; 277071, city of Chisinau, ul. Engelsa, d. 196, kor. 1, 
kv. 170, Oleg Renitse, editor in chief of ZELENYY MIR [Green 
World]. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Chisinau </H5>

<H5>  "Altair" Agency </H5>
  It was founded in 1989. It produced individual indicators of 
nitrates and nonnitrate fertilizers for house plants. It puts 
out the newspaper HERITAGE in Russian, English, and Romanian. 
  It takes actions to support ecologically clean industry and 
agriculture. It conducts ecological studies and is developing 
technologies for decontaminating water and air and for 
processing waste products. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 270012, city of Chisinau, a/ya 91. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Russia </H5>

<H5>  Republic Organizations </H5>
<H3>  All-Russian Ecology Center of VOOP ["Vserossiyskiy 
ekologicheskiy tsentr pri VOOP" (All-Russian Nature Protection 
Society)] (VETs) </H3>
  It was founded by decision of the central council of the 
All-Union Nature Protection Society (VOOP) (see article) on 9 
March 1989. Its by-laws were ratified on 11 April 1989. It 
operates on the foundation of the normative base of the NTTM 
[scientific-technical creativity of young people] system. 
  Its goal: "ensuring accelerated and efficient use of the 
scientific-technical and production potential of the republic's 
economy and the social initiatives of its population, raising 
the level of ecological safety, and establishing ecological 
sophistication." 
  Its tasks are: organizing training and retraining of 
specialists in the fields of the methods and systems of 
geoecomonitoring; advertising ecoengineering innovations; 
promoting the distribution of progressive ecoengineering 
concepts; providing essential organizational and economic 
assistance in the formation of geoecoinformation complexes and 
automatic expert systems of the USSR State Committee for Nature 
and its local organs, the State Committee for Science and 
Technology, organizations of the agroindustrial complex, and 
others in using the advanced knowhow in economic activities of 
the NTTM Centers; and using other forms of propagating knowledge 
of ecology. 
  To accomplish its tasks VETs can sell its own completed work 
at contract prices, become a collective member of voluntary 
associations, cooperatives, and international organizations; 
jointly with other associations which have similar tasks, 
finance nature protection programs; create international 
collectives of specialists to solve global problems of ecology 
and scientific forecasting; and create joint enterprises and the 
like to carry on export-import operations in the subject of its 
activity. 
  Forms of activity: intermediary activities; formation of 
labor collectives within the limits of economic contract 
relations; exploratory scientific research; monitoring of 
geosystems. 
  "In its activity VETs observes socialist legality and state 
discipline." 
  Organization and management of VETs: 
  The management organ is the VETs central council. 
Methodological and scientific guidance is provided by the 
scientific-technical council of the presidium of the VETs 
central council. VETs is subordinate to the VOOP central 
committee. 
  In its activity VETs combines collective decision-making and 
centralized management during implementation of decisions on the 
basis of economic independence and the initiative of the center 
itself. 
  VETs is headed by a director who operates on a 
one-man-management basis. He is competitively elected for 5 
years. The director and chief accountant of VETs are ratified in 
their positions and released from them by decision of the 
presidium of the central council in agreement with the 
scientific-technical council of VOOP. 
  For the performance of large-scale projects chief designers 
(scientific directors) of the development are appointed and 
councils of chief designers (scientific councils) are ratified. 
  A main expert council (GES) and problem-oriented expert 
councils (PES's) are formed with the rights of consultative 
bodies to ensure overall coordination of projects. The 
membership of the GES is coordinated with the presidium of the 
VOOP council and ratified by a joint decision of the director of 
the center and the scientific-technical council of the VOOP 
central committee. The membership of a PES is coordinated with 
the GES and ratified by the VETs director. 
  Calendar plans of contract work and future plans for longer 
periods of time are developed, as are plans for economic and 
social development. 
  VETs is supplied with special equipment and instruments by 
ministries and departments based on its orders. This is done 
through USSR Gossnab [State Committee for Material and Technical 
Supply] in the established manner. 
  State registration of VETs developments is done at the 
All-Union Scientific-Technical Information Center of the USSR 
State Committee for Science and Technology. 
  In accordance with its by-laws VOOP established the charter 
fund of VETs at R100,000 and its working capital at R150,000. 
  VETs ratifies for a 3-year period the normative percentage 
of 
deductions to the fund of the VOOP central committee (30 percent 
of profit). 
  Local organizations: VETs can organize its own 
branches--regional ecological centers [RETs's]. They are formed 
at oblast, kray, and city councils of VOOP and at the republic 
councils of the nature protection societies of the Union 
republics (with the consent of the latter) as independent 
cost-accounting organizations. The higher-ranking organization 
for an RETs is the VETs. The presidium and the 
scientific-technical territorial council of VOOP provide 
scientific methods guidance for the RETs's. 
  Address: 103012, city of Moscow, K-12, proyezd Kuybysheva, 
d. 
3, str. 3, tel. 921-38-97. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    All-Russian Order of the Labor Red Banner Nature Protection </H5>

Society ["Vserossiyskoye ordena Trudovogo Krasnogo Znameni 
obshchestvo okhrany prirody"] (VOOP) 
  It was founded in 1924. 
  Its main goal is to promote and carry out state nature 
protection policy. 
  The primary charter tasks are: 
  --ecological education of the population and shaping of 
objective public opinion on important ecological problems; 
  --involvement of the population, especially VOOP members, 
in practical nature protection activities; 
  --public monitoring of compliance with nature protection 
laws; 
  --organization and development of the club movement in 
natural science areas. 
  The membership is varied. At the start of 1990 VOOP had more 
than 36 million members and young friends of the society, joined 
into approximately 200,000 primary organizations and clubs, as 
well as 79,000 collective members from among enterprises, 
organizations, and institutions. The total number of nature 
protection society councils is 2,436. 
  VOOP has a far-flung structure of public subdivisions 
(scientific-technical councils, sections, commissions, 
committees, public inspectorates for nature protection, 
detachments of "blue" and "green" patrols, and the like). 
  The management organ is the presidium of the central council 
of VOOP. The chairman of the presidium of the VOOP central 
council is VASKhNIL Academician A. Kashtanov. The first deputy 
chairman is Ivan Barishpol. The other members of the VOOP 
central council are V. Rakhilin, O. Kolbasov, and Yu. Yefremov 
(honorary member of VOOP). 
  Primary activities: 
  Already in the early 1980s VOOP was taking an active part in 
the development and establishment of the system of the first 
Russian national parks. 
  The main event of 1988-1989 was the All-Russian Inspection 
of 
the Use of Reclaimed Lands. A plenum of the VOOP central council 
was held based on its results. 
  In 1989: 
  --more than 600,000 lectures were given, up to 150,000 
students studied in people's universities, and about 38,000 
exhibits were organized; 
  --by order of the society the films "The Scars of War and 
the Wounds of Peace," "Bioshield," and "Rivers of Our Childhood" 
were made. An amateur film festival on the topic of nature 
protection was held jointly with the RSFSR Ministry of Culture; 
  --an all-Union ecology poster contest was held jointly with 
USSR Goskomprirody and other interested organizations; 
  --through public efforts more than 8,000 kilometers of 
banks along small rivers were cleaned up, about 8,000 springs 
were protected by construction, 90,000 hectares of suburban 
forests and wooded parks were cleaned up, 3 million trees were 
planted, and so on; 
  --expert commissions continued work on atomic power plants, 
the Ishtuganov Reservoir in Bashkiria, and the series of BES's 
[possibly bioengineering plants] on the Katun River in Altay 
Kray; 
  --central and local VOOP councils took part in deciding the 
fate of construction of the Cheboksary pumped-storage power 
plant, construction of the bypass road in the city of Sochi, the 
problems of Pleshcheyev Lake in Yaroslavl Oblast, and 
construction of the Caucasian Pass Railroad; 
  --to stimulate the club movement, the all-Russian 
association of cat fanciers clubs was formed in early 1989, and 
at the end of the same year the Alliance of Animal Lovers was 
founded; 
  --the All-Russian Ecology Center and the Soyuzekoservis 
Production Association were formed under the VOOP central 
council; 
  --VOOP became involved in the international action, "Trees 
for Life"; 
  --VOOP enlarged and improved the "Bioshield" march, in 
which significant financial resources are invested; 
  --work was done to create public ecology funds; 
  --specific issues related to Losinyy Ostrov [Moose Island], 
Samarskaya Luka [Samara Arc], and other national parks were 
resolved; 
  --no later than March 1991 a session of the presidium of 
the VOOP central council discussed the situation at Samarskaya 
Luka, one of the first Russian national nature parks, which had 
become a site of industrial development of natural wealth and 
for dumping radioactive waste. A decision was adopted to study 
the situation and place before the highest state organs the 
question of a comprehensive solution to the problems of the 
national park; 
  --VOOP called for all interested public organizations, 
enterprises, and institutions to cooperate to carry out specific 
nature protection programs (EKOLOGICHESKAYA GAZETA No 2-3, 1991, 
p 2); 
  --in early May 1991 VOOP organized and carried out a 
surprise inspection of land reclamation at farms in Zagorskiy 
and Yegoryevskiy rayons of Moscow Oblast, Astrakhan, 
Kaliningrad, and Novosibirsk oblasts, Krasnodar Kray, and 
Mordvinia; violations of nature protection law were identified; 
  --the 11th plenum of the VOOP central council was held in 
the summer of 1991. It discussed draft documents for the next 
VOOP congress: the 1991-1995 Program of Society Actions and 
by-laws. The regular congress was held in October. It adopted a 
policy of enlarging the rights of primary and other local 
subdivisions of VOOP in the organizational and financial areas 
and decided to introduce cost accounting principles in 
conducting certain types of nature protection work and services 
for the population and to carry on continuous ecological 
training; 
  --VOOP is one of the founders of the newspaper ZELENYY MIR 
[Green World], which began coming out in January 1991. The 
presidium of the VOOP central council paid R100,000 from 
membership dues to the fund of the newspaper ZELENYY MIR after 
adopting, in February-March 1991, the decision of the publisher 
of the center's newspaper EKOPRESS to lower the price of a 
single copy from 50 to 20 kopecks; 
  --VOOP together with the Arkhangelsk Pulp and Paper Combine 
founded EKOLOGICHESKAYA GAZETA [Ecology Gazette], which began to 
come out in November 1991. 
  Management structure: 
  VOOP consists of 248 trade subdivisions (stores) in 48 
oblasts, krays, and republics of Russia and 10 production 
enterprises. Its commercial activity has mainly a nature 
protection orientation. 
  Its income in 1989 was more than R15 million; R6 million of 
this is membership dues which go entirely for nature protection 
activity. 
  In 1989 VOOP switched to a new model of economic activity 
and 
the councils were switched to new conditions within the limits 
of the funds received with due regard for expanding the economic 
activity of VOOP enterprises and organizations. 
  VOOP founded the Engineering Ecology Publishing Foundation 
(before the start of 1991). 
  VOOP is a member of the International Nature Protection 
Alliance. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Gorokhov, M., "VOOP on the Path of 
Changes," EKOLOGICHESKAYA GAZETA, No 7, 1991, p 2; 
  -  Borozin, M., 
"They Kept Their Word," ZELENYY MIR, No 19-20, 1991, p 1. 

<H3>    Public Committee To Save the Volga ["Obshchestvennyy komitet 
spaseniya Volgi"] (OKSV) </H3>
  "Russian national-patriotic public organization." 
  The committee was formed at its founding conference on 27 
January 1989 in Moscow on the initiative of the public 
organizing committee made up of representatives of regional 
newspapers and cultural and ecological initiative groups. About 
250 persons attended: representatives of cities and populated 
points in the Volga basin as well as regional newspapers. 
  The goal: ecological salvation of the Volga from 
"unrestrained exploitation by industrial departments and 
cultural rebirth of the lives of the Russian peoples in the 
Volga basin." 
  Forms and methods of work: demonstrations and picketing at 
AES's, organization of scientific expert studies on specific 
ecological problems, and propaganda work in the press. 
Participation in political actions of solidarity with Russian 
national-patriotic forces. 
  Membership in the organization is not fixed (in practice 
collective membership evolved). It was planned to institute 
individual membership in the first quarter of 1992. 
Social-professional composition: primarily representatives of 
the urban creative and scientific-technical intelligentsia. 
  By the start of 1992 it had about 5,000-6,000 supporters. 
The 
constantly active body of activists was about 300. The main 
structural units of the OKSV were groups of 20-30 persons joined 
into regional organizations under overall coordinating 
direction. The regional organizations, whose number reached 22 
by the start of 1992, are the foundation of the organization 
structure. 
  The highest body is the conference. The working body is the 
board of directors, which has 62 members (representatives of 
regional organizations and chairmen of subject commissions). The 
leader of the organization is S. A. Shatokhin. 
  An organizing committee of 20 persons, representatives of 
regional newspapers and initiative groups, first formed in 
Moscow in October 1988. Among the cities represented were 
Kalinin (Tver), Kuybyshev (Samara), Gorkiy (Nizhniy Novgorod), 
Astrakhan, Kostoma, Kazan, Ulyanovsk, Ivanovo, and Volgograd. 
They formed 16 commissions, among them commissions on peasants, 
energy, fishing, archives (for the purpose of creating a public 
archive fund), cultural heritage, cultural relations with 
Russians abroad, law, science, information, theory, and others. 
  At the founding conference the OKSV Program and by-laws were 
adopted. Three cochairmen were elected (S. Shatokhin, V. 
Denisov, and F. Shipunov), plus the board of directors and its 
chairman (the writer V. Belov). 
  On 29 January 1990 a working conference of the OKSV was held 
with participation by 352 delegates representing the regions 
(representation was 1 person out of 20). There was a partial 
change of leadership at the conference: S. Zhukov (later also 
removed on a working basis) was elected cochairman in place of 
V. N. Denisov and the position of chairman of the board of 
directors (held by V. Belov) was eliminated. Positive work by 
the press (the journal VOLGA and the newspapers VOLGA of 
Astrakhan, PRAVDA of Kalinin [Tver], PRAVDA of Volgograd, 
NIZHEGORODSKIYE NOVOSTI, and VECHERNYAYA KAZAN) in illuminating 
the ecological situation in the region was noted. The failure of 
the scientific, cultural, and legal commissions was noted. The 
work of S. A. Shatokhin as official responsible for creation of 
AKSV regional structures was praised. 
  Regional founding conferences had been held in Moscow, 
Saratov, Yaroslavl, Kostroma, Rostov Velikiy, Ufa, Rybinsk, and 
Volgograd by the start of 1990. In the course of 1990-1991 the 
Nizhniy Novgorod, Cheboksary, Samara, and various other regional 
organizations were formed. 
  During 1991 the Volgograd regional organization was 
especially active. In January 1991 they formed the Lower Volga 
Ecological Parliament (chairman L. N. Savelyeva) with about 100 
members. The Parliament held four sessions in 1991. People's 
deputies of all levels were represented in it, and thanks to 
this the "Rebirth of the Volga" program (authored by V. V. 
Naydenko, rector of the Nizhniy Novgorod Construction 
Engineering Institute) was developed and prepared for 
ratification on the state level. 
  During this period the OKSV takes credit for stopping 
construction on the Bashkir, Tatar, Gorky, and Rostov AES's and 
suspension of the AES's being planned for Kalinin and Yaroslavl. 
  At the end of February 1992 a report and election conference 
was to be held in Nizhniy Novgorod (the headquarters of OKSV was 
to be moved there from Moscow). At the conference a change in 
the structure of the organization was planned, after which it 
would presumably be organized on the territorial principle: an 
organization of the lower Volga with its center in Volgograd, 
the middle Volga with its center in Nizhniy Novgorod, and the 
upper Volga with a center in Tver. It was assumed that the 
centralized coordinating leadership would be in Nizhniy 
Novgorod. It was contemplated that nonworking structures would 
be eliminated, nonworking members of the OKSV would be removed 
from governing bodies, and the size of the board of directors 
would be cut from 62 to 40-45. 
  During preparation for the conference the question of 
establishing an Ecological Party on the basis of the OKSV is 
being discussed. 
  The OKSV does not have its own newspaper. The one issue of 
the newspaper SPASENIYE which came out (August 1991, 5,000 
copies, 4 pages, editor was F. Ya. Shipunov) was put out by 
Shipunov without the participation of OKSV and, in the words of 
S. A.Shatokhin, has no relationship to the organization. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Russian Greens Party ["Rossiyskaya Partiya Zelenykh"] (RPZ) </H5>

  A political party. It was formed on 25 May 1991 from a 
number 
of Greens Party (see article) organizations and several 
ecological organizations. It declared itself the successor to 
the Greens Party that existed before. The RPZ initially 
comprised 20 organizations with a total membership of about 
1,000 persons. At the founding conference the by-laws and the 
Declaration of the Russian Greens Party were adopted and the 
party's working and management bodies were elected. 
  Primary forms of work: conducting rallies and picketing to 
defend the environment, conducting independent expert studies 
and investigations, doing agitation and educational work, and 
doing work in representative organs of power. 
  The party declaration is a synthesis of the views of its 
general democratic and anarchist factions. The by-laws envision 
preservation of the full independence of structures that belong 
to the party. 
  The highest governing body is the congress. The coordinating 
organ is the council of cochairmen, consisting of 15 persons who 
represent different regions of Russia. Among the members of the 
council of cochairmen are V. Gushchin, I. Blokov, and V. Panov 
(St. Petersburg), A. Shubin (Moscow), M. Salakhov (Perm), V. 
Kniginichev (Chelyabinsk), V. Pushkarev (Novokuznetsk), S. 
Grosheva (Kemerovo), V. Skorin and A. Tukhvatulin (Sterlitamak), 
V. Rapota (Norilsk), and others. The RPZ has deputies in the 
local governmental bodies in St. Petersburg, Moscow, Norilsk, 
Novokuybyshev, and elsewhere. 
  Because the party by-laws envision full independence of the 
regional structures belonging to the RPZ, from the moment of the 
organization's formation active work has been done primarily in 
the local areas. The most important campaigns have been the 
struggles against the Novokuznetsk Metallurgical Combine, 
logging in the forests of Karelia, the Northern TETs [central 
heat and power plant] in Moscow, and others. Local organizations 
take part in the political struggle against authoritarian groups 
in governmental organs. 
  Radio Russia's program "Green Thread" is run on the basis of 
the RPZ. 
  On 21 June 1991 Vladimir Gushchin was beaten up; shortly 
before this he had published an interview in the city press 
about cases of illegal trade in lumber (sale of lumber to 
Finland for hard currency) and of instances of persecution of 
RPZ activists who were working on this question. Nina Zuyeva, 
one of the party activists who was trying to conduct an 
independent investigation of logging in Leningrad Oblast, 
perished. 
  In February 1992 a meeting of the cochairmen of the RPZ 
spoke 
out against the danger of the spread of chauvinist ideas in the 
ecology movement. 
  On 28-29 February 1992 the RPZ acted as one of the 
organizers 
of the conference of nongovernmental organizations in St. 
Petersburg. 
  In March-April 1992 party activists investigated an accident 
at the AES in Sosnovyy Bor, Leningrad Oblast (according to V. 
Gushchin's statement, the Greens faction of the Finnish 
parliament raised doubts about the official version to the 
effect that only technical equipment at the AES was damaged 
because cesium-137, traces of which were found in Finland on the 
border with Leningrad Oblast, appears when a reactor is damaged). 
  Address: 191186, city of St. Petersburg, ul. Zhelyabova, d. 
8; 198013, city of St. Petersburg, a/ya 146; tel. 312-44-08 and 
186-52-00. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Funds 1, 2; 
  -  Polyanskaya, A., "Greens Party Activist Beaten," 
EKSPRESS-KHRONIKA, 25 June 1991, p 1; 
  -  Polyanskaya, A., "St. 
Petersburg," EKSPRESS-KHRONIKA, No 13 (243) 31 March 1992, p 
2. 

<H3>    Russian Committee for Defense and Resurrection of the Oka 
River ["Rossiyskiy komitet zashchity i vozrozhdeniya Oki"] </H3>
  Its primary task is to join the efforts of local 
governmental 
bodies, the public, and specialists to improve the ecological 
state of the Oka region. 
  On 19 June the expedition called "Oka--Living Water of 
Russia" began, following a route from Orel to Nizhniy Novgorod. 
It was organized by the committee jointly with the "ecology 
newspaper," radio station Smena, the RF State Committee for 
Water Management, the Moscow-Oka Water Management Association, 
and the small Ekor Enterprise in Pushchino. 
<H5>  Sources of Information </H5>

  -  IMPD Archives, Fund 2; 
  -  Kruzhek, V., "How Is Your Health, 
Oka?" EKOLOGICHESKAYA GAZETA, No 7, 1991, p 2. 

<H3>    Russian Social-Ecological Alliance ["Rossiyskiy 
sotsialno-ekologicheskiy soyuz"] </H3>
  An all-Russian association. It was registered on 9 January 
1992. It has by-laws. 
  Goals: "join the intellectual potential, material and 
financial resources, and organizational capabilities of members 
of the alliance to preserve and restore our natural and cultural 
heritage and prevent the destruction of the environment and 
human health." 
  The governing body, the council of operational actions, is 
located in Nizhniy Novgorod. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Affidavit of Registration of the 
By-Laws of a Public Association, 9 January 1992, No 579, RSFSR 
Ministry of Justice. 

<H3>    Russian Ecological Alliance ["Rossiyskiy ekologicheskiy 
soyuz"] (RES) </H3>
  An independent division of the USSR Ecological Alliance (see 
article), which established the RES. Its nature protection 
activities are oriented more to the Far East, Siberia, the 
Urals, and the Far North than to the other regions of Russia. 
<H6>  Sources of Information. </H6>

  -  IMPD Archives, Fund 2; 
  -  "Collaborate! Appeal of the Board 
of Directors of the USSR Ecological Alliance," ZELENYY MIR, No 
15-16, 1991, p 10. 

<H5>    Russian Ecology Foundation ["Rossiyskiy ekologicheskiy fond"] </H5>
  Purpose--active defense of nature which "continues to be 
exploited in the most ruthless manner and is perishing." This is 
stated in the "Appeal to the Citizens of Russia," adopted at the 
founding meeting of the foundation on 31 May 1991 in Moscow. 
  Present at the meeting were representatives of the Ecology 
Committee of the RSFSR Supreme Soviet, the USSR Ministry of Land 
Use and Environmental Protection, other all-Union and Russian 
nature-protection institutions and organizations, plus branches 
of the USSR Ecological Foundation (see article)--the Oka 
regional, Ural, Chelyabinsk, and North Caucasus branches. The 
initiators in forming the foundation were the USSR Ecological 
Foundation and the Russian Ecological Academy in Leningrad. 
  The management organ is the board of directors. Its chairman 
is I. V. Petryanov-Sokolov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Bolshakov, V., "The Russian 
Ecology Foundation Is Formed," SPASENIYE, No 5, 1991, p 7. 

<H3>    RF Alliance of Hunters and Fishermen's Societies ["Soyuz 
obshchestv okhotnikov i rybolovov RF"] (Rosokhotrybolovsoyuz) </H3>
  It was formed on 13 June 1958. As of 1 January 1990 it had 
2,912,604 members. 
  Goal: active participation in the cause of protecting nature 
and using it rationally, and in reproduction of hunting, 
fishing, and forest resources. 
  Primary tasks: to join together hunters and fishermen for 
active participation in managing hunting and fishing, 
development of the sport of hunting and fishing, "preservation 
and enlargement of stocks of wild animals, birds, and fish," 
"assistance to state, cooperative, and public enterprises in 
carrying out the nature protection policy of the Soviet state," 
"teaching society members a stewardly attitude toward nature," 
and others. 
  Forms of work: providing scientifically substantiated 
management of hunting and fishing, increasing the efficiency of 
assigned hunting lands and waters, and participating in 
ecological expert studies at sites. Each year they hold 
exhibitions, field trials for hunting dogs, and rifle hunting 
competitions, representatives of the alliance take part in 
international competition, and international seminars are given, 
such as the "Wildlife, Environmental Protection, and Protection 
of Rare Animal Species" seminar in Moscow in 1989. 
  The alliance's activities may be commercial or 
noncommercial. 
  Resources: dues, income from economic activity, 
special-purpose contributions, and other revenue. Initiation 
fees: with the right to hunt and fish--R10, with the right to 
hunt--R5. Annual membership dues--R10 with the right to hunt, R5 
without it. 
  The chairman of the central governing board is A. A. Ulitin 
and deputy chairmen are V. B. Samokhvalov, V. A. Grigoryev, and 
A. A. Klushin. 
  The emblem is in the form of a seal with moose antlers 
above, 
a fish below, and the name "Rosokhotrybolovsoyuz" across the 
middle. 
  Addresses: 125124, city of Moscow, Golovinskoye shosse, d. 
1a., Central Governing Board; tel 452-13-36, 459-09-15, 
Aleksandr Aleksandrovich Ulitin; tel. 452-13-33, 459-09-75, 
Vyacheslav Borisovich Samokhvalov; tel. 452-13-35, 459-09-35, 
Vladimir Aleksandrovich Grigoryev; same, room 518, the 
"Ekologiya" Cost Accounting Planning-Surveying Service for 
records of hunting resources, ecological evaluations, expert 
studies, and hunting arrangements of Rosokhotrybolovsoyuz, 
director Vladimir Yuryevich Martyanov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Christian Ecological Alliance of Russia </H5>

[Khristiansko-ekologicheskiy soyuz Rossii"] (KhESR) 
  The organizational center is located in St. Petersburg. It 
was formed in October 1989. Among the initiators of its 
formation was the Leningrad "Delta" ecological association (see 
article). It comprises several groups of different political, 
cultural, and ethical directions, including the informal Jewish 
Rebirth organization and the Russian national-patriotic group 
Pamyat [Memory]. 
  The goals of the organization are to achieve a balance 
between nature and man, and between man and man on the basis of 
Christian ethical principles and commandments, and the struggle 
for the formation of a law-governed, democratic state in Russia 
whose spiritual life should be based on Christianity. 
  Tasks: preparation of an alternative plan for the social 
development of St. Petersburg, the granting of free-city status 
to it, resurrection of churches, transfer of all educational 
institutions to them, conversion of the Karelian isthmus into a 
preserve, and so on. 
  Primary forms of work: cultural-educational lectures, 
organization of debates, conduct of charitable events, 
collection of signatures, rallies, mass ecological actions, 
participation in election campaigns, and so on. 
  Membership in the KhESR is not fixed and dues are mainly in 
the form of donations. The work of the alliance is coordinated 
by its chairman (S. Kozhevnikov since it was founded) and two 
cochairmen. The KhESR Declaration was adopted as its program 
document. 
  In mid-1990 there were 20 activists, mainly members of the 
creative intelligentsia. The alliance is organizationally part 
of the Russian Christian Democratic Movement. It is joined with 
the Christian Democratic Union of Russia in a political bloc. 
  On 21 April 1990 (within the framework of celebrating Earth 
Day) the alliance together with the Christian Democratic Union 
of Leningrad, the Delta ecology association, and the Greens 
Alliance organized a rally (about 500 participants). Ecological 
and anticommunist slogans predominated at the rally. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 1, p 121; vol 1, part 2, p 182. 

<H3>    "Ekopolis of the World" ["Ekopolis mira"], Russian 
Association </H3>
  Task: assistance to initiative groups in the local areas in 
creating ecologically clean settlements for the purpose of 
making peace--by information media, coordination, and 
consultation. 
  The movement appeared in December 1988, and the association 
was established in October 1990 by the USSR Ekofond (see 
article), the Culture Foundation, the Moscow Committee of the 
Russian Red Cross, and two architectural 
organizations--"Initsiativa" [Initiative] in Moscow, and 
"Sovremennik" [Contemporary] in Leningrad. The association was 
registered in Moscow in October 1990. 
  There is a staff of four persons. The association comprises 
a 
total of about 200 persons, including deputies of local soviets. 
The average age is 25-40. 
  There are nine regional centers which paid for registration 
and transfer 10 percent of their economic transactions. 
  For admission to the association it is necessary to present 
a 
letter from an initiative group and draft by-laws. 
  Address: City of Moscow, VDNKh, Animal Husbandry Pavilion, 
tel. 461-77-63, Dmitriy Vorobyev, chairman of the association. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Moscow </H5>

<H5>  Airo </H5>
  It was founded in 1989. It fights against discharges into 
bodies of water. It organizes expeditions to survey polluted 
regions of the Moscow River and the northwestern shelf of the 
Black Sea. 
  Total number of members--10. 
  Address: 107150, city of Moscow, ul. Boytsovaya, d. 18, k. 
14, kv. 5, Sergey G. Bashkirov, scientific associate. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    "BIM" Society for the Defense of Animals ["Obshchestvo </H5>

zashchity zhivotnykh"] 
  Moscow city organization. It was formed in 1988. 
  The society built a shelter for homeless dogs and cats, but 
someone set it on fire. Society members took the surviving dogs 
and cats into their homes and appealed to the public for 
contributions to build a new shelter building. 
  Current Account No 170147 Bauman Branch , Zhilsotsbank, City 
of Moscow. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Kharchenko, O., "BIM--Hostel for 
Cats and Dogs," ZELENYY MIR, No 9, 1991, p 4. 
  -  "This Was Done 
by...People?" ZELENYY MIR, No 14, 1991, p 8. 

<H5>    "Bittsa" Society (Association) </H5>
  Ecology organization of Bittsevskiy Rayon in Moscow. The 
number of participants in the society varies, sometimes reaching 
several thousand. 
  In the summer of 1988 they held several rallies that drew 
thousands (including in the center of Moscow) calling for 
preservation of the Bittsa Forest Park. 
  The society is a member of the Moscow Ecological Federation 
[MEF] (see article) and the Moscow People's Front (since 1988). 
  The chairman of the society is Yan Yanovich Iodis, tel. 
229-64-59 (at the Mossoviet). Among the activists of the society 
is Leonid Vasilyevich Korablev, director of the coordinating 
council of the MEF, tel. 132-20-90 (home). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Brateyevo, Committee for Public Self-Government of the </H5>

Brateyevo Microrayon 
  It appeared in September 1988. The impetus to form the 
committee was the grave ecological situation which had developed 
in Brateyevo (the microrayon of 60,000 inhabitants began 
operating in 1985-1986 despite the prohibition of the sanitary 
epidemiological service; it is in the immediate vicinity of the 
Moscow Petroleum Refinery in Kapotnya and other ecologically 
"dirty" enterprises). 
  In the summer of 1988 there were several rallies in the 
microrayon (up to 3,000-4,000 participants) at which demands 
were made to take steps toward a radical improvement of the 
ecological situation in the region. Because the residents and 
the rayon authorities did not reach mutual understanding at that 
time and none of the 26 deputies of the rayon soviet who 
represented the microrayon lived in Brateyevo, the participants 
in the rallies also demanded their recall and the election of 
new deputies from among the inhabitants of the microrayon. 
  The founding meeting of the committee was held on 4 
September 
1988. The statute on the committee was ratified at a session of 
the rayon soviet on 29 September. This marked the beginning of 
working contacts between the committee and the rayon authorities. 
  At the present time the committee has about 100 members. The 
management organ is a coordinating council (10 persons). Each 
member of the coordinating council is responsible for a certain 
area of the committee's work. There is no chairman. The 
committee set up four centers: ecology, work with the 
population, development of the social sphere, and information. 
The centers have formed commissions (about 25 in all). There are 
3-5 members of the committee working in each commission along 
with the activist inhabitants of the microrayon (there are 
several hundred activists). Sessions of the coordinating council 
and committee are held weekly. The commissions are working 
constantly. Personnel changes are made at a conference of 
building representatives. (The conferences must be held at least 
once a year. In 1988 and early 1989 they were held quarterly.) 
Information meetings are held to inform the population of the 
microrayon about the committee's work. The committee is a legal 
person and has premises (committee meetings are held in the 
meeting room of the secondary school) and a current account in 
the bank. 
  At the present time committee members take part in all 
sessions of the rayon soviet and present reports there. 
Relations with the Mossovet have been established. The opinions 
of inhabitants of the microrayon have started to be taken into 
account in the construction of new enterprises. The committee 
conducted a referendum to clarify the opinion of the population 
about intentions to establish an industrial zone near the 
microrayon. About 70 percent of the inhabitants of the 
microrayon took part, and more than 99 percent were against the 
construction plan. A session of the rayon soviet supported this 
decision. S. Druganov, one of the leaders of the Brateyevo 
Committee, was nominated as a candidate for people's deputy of 
the USSR in 1989 and people's deputy of the RSFSR in 1990. He 
was elected people's deputy of the RSFSR. 
  They have no press organ. The committee maintains contacts 
with self-government committees that exist or are forming in 
other rayons of Moscow and in other cities. It has been a member 
of the Moscow People's Front since 1988. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 186. 

<H3>    Information Agency on Nongovernmental Ecology Organizations 
["Informatsionnoye agentstvo po nepravitelstvennym 
ekologicheskim organizatsiyam"] (Ekoinform) </H3>
  It gathers and disseminates information on ecological 
organizations and instances of violation of nature protection 
law. 
  Address: city of Moscow, VDNKh, Computer Technology 
Pavilion, 
tel. 181-99-70. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Cosmos ["Kosmos"] </H5>

  Philosophical and public health club. It appeared in 1981. 
Initially it specialized in public health tasks, and then later 
began to devote more attention to philosophical problems too. 
The views of N. Rerikh are very influential. Director is 
Vladimir Aleksandrovich Artamonov. It has about 150 members. It 
distributes leaflets and conducts debates on philosophical and 
ecological topics. 
  Address: tel. 378-90-58, Inna Petrovna Ozhimkova. 
<H6>  Source of Information </H6>

  -  Archives of A. V. Shubin. 

<H5>    Youth Association To Promote Ecological Initiatives </H5>

["Molodezhnaya assotsiatsiya sodeystviya ekologicheskim 
initsiativam"] 
  It was formed in 1991 and has 75 participants. Its 
management 
organ is the general meeting. President of the association is 
Mikhail Yuryevich Koloborodov. Its goals are: "protection of the 
environment and development of ideas that promote solutions to 
young people's ecological problems." 
  Address: 119435, city of Moscow, ul. Pogodinskaya, d. 14, 
kv. 
21; tel. 290-27-78, Yuriy Nikolayevich Nikitin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Molodezhnyye obshchestvennyye 
organizatsii g. Moskvy" [Youth Public Organizations of the City 
of Moscow], Moscow, Ispolkom Mossoveta, Moscow City Committee 
for Youth Affairs, 1991, p 21. 

<H3>    Youth Nature Protection Council of Moscow State University 
imeni M.V. Lomonosov ["Molodezhnyy sovet po okhrane prirody MGU 
im. M. V. Lomonosova"] </H3>
  Together with the USSR Student Council, it organized and 
conducted the all-Union meeting of youth organizations 
interested in environmental protection in Moscow on 22-24 August 
1991 (within the framework of preparations for the U.N. 
Conference on the Environment and Development in Brazil in 
1992). The tasks of the meeting were development and adoption of 
a program of youth demands on problems of ecology, discussion of 
the possibility of participating in the movement in preparation 
for the Brazilian conference, and discussion of the formation of 
the Association of USSR Youth Ecology Groups to coordinate 
efforts in the field of nature protection because, in the 
opinion of Youth Council activists, a serious move onto the 
international arena is possible only within the framework of a 
national organization. 
  Address: 119899, city of Moscow, Vorobyevy (Leninskiye) 
gory, 
MGU, 2-y gumanitarnyy korpus, ekonomicheskiy fakultet, kom. 513, 
kom. 485, tel. 939-28-39, 219-60-15, fax 939-08-77, tel. 
939-22-54, Marina Vitalyevna Martynova. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2; 
  -  "The 
Youth of the World Are for Ecology!" EKOLOGICHESKAYA GAZETA, No 
10, 1991, p 2; 
  -  Pokizova, O., and Kazarinov, M., "We Will Meet 
in August," ZELENYY MIR, No 25-26, 1991, p 13. 

<H5>    Moscow River ["Moskva-reka"], Organizing Committee </H5>
  Ecology organization consisting of specialists and public 
activists working on the problems of rivers in the Moscow River 
basin. 
  It was formed within the All-Russian Nature Protection 
Society (see article) in 1987. It has been independent since 
1991. Initiators of its formation were A. V. Chernov (geologist) 
and V. M. Khmelinskiy. The by-laws were adopted on 7 September 
1991. The committee is not officially registered. 
  It joins the ecology organizations Brateyevo (see article), 
Yauza (see article), and Rublevo (see article), the Moscow 
Esperanto Club "Scio" (Knowledge), and the ecology committee. 
  The goal of Moscow River is to join together all those who 
are concerned about the ecological problems of the Moscow River 
basin (clean water and air) and involve the organizations that 
are polluting the river to carry out comprehensive studies and 
find joint solutions to the problems. 
  It organizes press conferences on ecological problems of the 
Moscow River. It is proposed to organize an expedition from the 
source to the mouth of the Moscow River to carry out the charter 
task. The governing board has nine members, representatives of 
the member organizations. A chairman is not elected in 
principle. There are no membership dues. The committee 
collaborates with the MEF [Moscow Ecological Federation] (see 
article), SES [Social-Ecological Alliance] (see article), and 
SNIO [Union of Scientific and Engineering Societies]. It is in 
contact with ecology organizations in Kolomna, Mytishchi, and 
elsewhere. 
  It has no official premises. It uses the SNIO quarters in 
building No 18 on ul. Sadovo-Kudrinskaya for meetings. 
  Address: tel. 246-36-24, V. M. Khmelinskiy, member of the 
governing board; tel. 208-15-42, Ye. V. Venetsianov, chairman of 
the ecology commission of SNIO; tel. 414-23-13, M. I. 
Timofeyeva, member of the MEF presidium; tel. 939-11-17, V. S. 
Kusov, cartographer; tel. 271-09-09, V. F. Durnov, member of the 
Rublevo ecology organization; tel. 973-09-78, N. Ye. Kruchinina, 
dean of MKhTI; tel. 577-26-63, B. M. Bystrov, member of the 
governing board of VOOP; tel. 408-48-24, G. A. Ganovskiy, member 
of the MFTI cooperative; tel. 158-64-02, L. V. Samoylova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Moscow Greens Party Organization ["Moskovskaya organizatsiya </H5>

partii zelenykh"] (MOPZ) 
  It was organized in May 1990 on the basis of the Movement To 
Create the Greens Party with the assistance of activists of the 
Confederation of Anarcho-Syndicalists, the Biryulevo-Zagorye 
Self-Government Committee, and the ecology section of the 
Artists Union. It joined the Greens Party. 
  It is organized on the principles of "basic 
democracy"--complete subordination of the coordinating organs to 
the rank-and-file members. 
  In April-December 1991 the organization held a series of 
rallies against construction of the Northern TETs, the cutting 
of wooded areas, construction of a bread plant in a zone of 
heightened radioactivity, and other ecological problems of the 
capital. It sharply criticized the policy of the Moscow mayor's 
office and supported the Mossoviet. It has two deputies in the 
city soviet and two in rayon soviets. 
  The "Green Thread" radio program has been produced since 
March 1991 with help from MOPZ. 
  MOPZ developed its own program in the fields of economics, 
politics, and social and ethnic relations. It supports 
self-government and a market economy based on collective 
ownership of the means of production. This position was 
criticized by V. Damye, one of the cochairmen of the MOPZ. In 
May 1991 he left the MOPZ, which was the start of the ensuing 
schism in the Greens Party. 
  The MOPZ joined the RPZ. In late 1991 it sharply criticized 
government policy in the area of prices, privatization, and 
exploitation of natural resources. An MOPZ rally on Human Rights 
Day, 10 December 1991, was broken up and 11 persons were 
detained, including 5 deputies. Following this, under pressure 
from the MOPZ deputies, the Mossoviet proclaimed Sovetskaya 
Square a "Hyde Park." 
  On 19 April 1992, just before Earth Day, the MOPZ and the 
Cosmos Society (see article) jointly conducted a volunteer 
ecology work day in "Hyde Park," picking up filth and trash. By 
this action the MOPZ was trying to convince Moscow residents 
that they themselves can put an end to disorder in the city, 
without relying on strong executive power. 
  In the spring of 1992 the MOPZ took part in the campaign 
against commercialization of the parks of Moscow. 
  MOPZ deputies belong to the Mossoviet ecology commission and 
the "Strong Council" group. Deputy A. Zheludkov was elected 
chairman of the municipal soviet of Biryulevo-Zagorye. 
  Address: 105318, city of Moscow, a/ya 57, RPZ. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H3>    Moscow Ecological Federation ["Moskovskaya ekologicheskaya 
federatsiya"] (MEF) </H3>
  This is an association of ecology groups of Moscow and 
Moscow 
Oblast. The first organizing session took place in August 1988. 
The founding conference (with about 500 participants) occurred 
15 April 1989 (founders were the Moscow City Council of the 
All-Russian Nature Protection Society [see article] and the 
Moscow Nature Committee). In March 1990 the MEF was registered 
by decision of the VOOP. At the beginning of 1992 the MEF still 
was not registered at the Mossoviet. 
  In August 1989 the Federation comprised 57 informal groups, 
then in the spring of 1990 it was about 50, and by the beginning 
of 1992 there were about 70 groups which differed by nature of 
their activities and by size (the largest ones--Bittsa [see 
article], Brateyevo [see article], and Northern Region--bring 
together up to 1,000 persons). Individual members are mainly 
specialists and experts in fields related to nature protection 
activity. The MEF is organized on the confederative principle. 
  In conformity with the by-laws, the highest body of the 
federation is the conference, which must be held at least once a 
year. In the intervals between conferences the executive organ, 
the coordinating council, operates. The coordinating council 
meets regularly (about twice a month). 
  Initially the MEF's work was coordinated by the council and 
three cochairmen--Lyubov Rubinchik, Sergey Druganov, and Vadim 
Damye. At first the council was elected from representatives of 
organizations, then later by the functional principle. In the 
opinion of L. Rubinchik, this made the council able to do more 
effective work. 
  Shortly after the April conference, cochairmen of the MEF 
(L. 
B. Rubinchik and V. I. Vasiliadi) were elected. 
  The council directs several working groups. The program 
group 
works on polishing the by-laws and the MEF program. The 
scientific information group prepares drafts and proposals for 
the MEF on ecology policy, enlists specialists to work with the 
federation, and gathers the suggestions of MEF groups and 
members on solving local ecological problems. Most of the groups 
that belong to the federation have similar histories of 
origination and development. The groups emerged spontaneously to 
solve some local problem, for example contamination of the 
environment by existing enterprises (Yauze [see article], 
Biryulelvo), construction of new enterprises (Brateyevo, 
Northern Region), and to save natural and cultural sites 
threatened with destruction ("Sloboda" [see article], 
"Studenets" [see article]), in particular cutting forests 
(Tushino, Strogino, Teplyy Stan). The number of people 
participating in the work of the groups is constantly changing. 
It depends, among other things, on the severity of the problem. 
There was also one political group among the organizers of the 
MEF--Commune. Later the Moscow Organization of the Greens Party 
(see article) joined the MEF. 
  The forms of activity of the groups go through three stages: 
  1) collection of signatures, protest letters, telegrams, and 
appeals to official bodies; 
  2) organization of independent expert studies (usually the 
results obtained by the experts do not influence the decision on 
the issue); 
  3) if favorable results are not achieved in the first two 
stages, MEF participants go over to "extremist" methods: 
picketing or blockading sites (Lefortovo, the Northern TETs, 
Sloboda), picketing official bodies, and rallies in front of the 
Mossoviet building (Bittsa, Tushino). 
  All these methods, as a rule, only gained time, without 
leading to accomplishment of the goal. Some groups stopped their 
activity, others split, and still others reorganized. Public 
self-government committees appeared (Brateyevo, Golyanovo, 
Solntsevo, and others). 
  The joining of the groups into a federation was the next 
stage. In June 1989 the MEF took part in the work of the ecology 
session of the Mossoviet. Most of the MEF's package of proposals 
was adopted by the session. Federation participants considered 
cooperation with official nature protection organizations such 
as the Moscow Nature Committee and the Moscow City Council of 
the VOOP to be promising. 
  To make this cooperation more productive, the MEF 
participated in the March 1990 elections for people's deputies. 
MEF cochairman S. Druganov (KOSU [Public Self-Government 
Committee] Brateyevo) was elected an RSFSR people's deputy. More 
than 10 MEF members joined the "Greens" faction that was formed 
in the Mossoviet. Federation participants were also elected 
deputies to the rayon soviets of Moscow and the oblast; they 
were mainly experts. In the elections for RSFSR people's 
deputies, the MEF helped defeat A. Matrosov, who at the time was 
deputy chairman of the Mosgorispolkom and was on the candidate 
list of Democratic Russia. 
  The MEF participates in expert studies of plans for 
residential and industrial construction in Moscow and the oblast 
(including the study of the Northern TETs, the new draft of the 
Master Plan for Development of Moscow, and construction of a 
bread bakery in a zone of heightened radioactivity in 
Khoroshevskiy Rayon of Moscow). It is conducting an 
investigation of the activities of the Moszelenkhozstroy 
Scientific-Production Association which led to cutting trees in 
Moscow and in the wooded park protective zone. It is fighting to 
have the Moscow Nature Committee directly subordinate to the 
Mossoviet, not to executive organs. It is organizing a system of 
ecological education and training, for Mossoviet deputies among 
others. In 1989 the MEF together with the Moscow Nature 
Committee and the Moscow City Council of the VOOP began 
preparation of an ecology program for the Mossoviet. 
  In the summer of 1991, the MEF together with SoES brought 
suit against the Russian Government for authorizing garden plots 
in areas with category No 1 forest. 
  Several members of the MEF belong to the public ecology 
council of the Moscow Nature Committee. 
  Addresses: 121019, Moscow, a/ya 211 or 123363, city of 
Moscow, ul. Aerodromnaya, d. 16, kv. 21, tel. 492-34-52, 
285-80-27, Lyubov Borisovna Rubinchik; legal address: ul. 
Chaykovskogo, 22; Mosgorsovet VOOP. Members of the MEF 
Coordinating Council: Sergey Petrovich Druganov, cochairman of 
MEF, RSFSR people's deputy, member of the Supreme Soviet, 
economist, lawyer, candidate of economic sciences, teacher at 
the Institute of Physical Culture, tel. 341-23-88 (home); 
Anatoliy Ivanovich Kadukin, Institute of Water Problems of the 
Russian Academy of Sciences, people's deputy of the Mossovet, 
member of the Ecological Alliance (see article), Moscow, tel. 
208-31-65 (work); Yuriy Yakovlevich Korotkikh, deputy of the 
Mossovet, member of the MEF Coordinating Council and the 
Ecological Alliance, city of Moscow, tel. 449-92-15 (work); 
Leonid Vasilyevich Korablev, pensioner, docent, candidate of 
philosophical sciences, member of the Ecological Alliance, city 
of Moscow, tel. 132-20-90 (home); Margarita Lvovna Monina, 
pensioner, hydraulic engineer, candidate of technical sciences, 
city of Moscow, tel. 362-44-73 (home); Leonid Alekseyevich Pets, 
head engineer, atomic physicist, member of the Ecological 
Alliance, city of Moscow, tel. 462-06-76 (work); Aleksandr 
Vladlenovich Shubin, historian, cochairman of the Russian Greens 
Party (see article), tel. 905-68-05 (home). 
<H6>  Sources of Information </H6>

  -  Archives of A. Shubin; 
  -  IMPD Archives, Funds 1, 2; 
  -  "Zelenyye v SSSR. Krupneyshiy...," op. cit., pp 14-16; 
  -  "Rossiya: partii...," op. cit., vol 1, part 2, p 173. 

<H3>    Moscow Society for the Defense of Animals ["Moskovskoye 
obshchestvo zashchity zhivotnykh"] </H3>
  It was formed by an initiative group of members of the 
section on protection of living nature of the MGOOP. It was 
ratified by decision of the Mosgorispolkom in January 1989 and 
re-registered in March 1992. 
  It is a non-commercial organization. Its goal is to teach a 
moral attitude toward nature and animals. One of the society's 
tasks was the struggle for a law on protection of animals, and 
on 30 March 1989 the "Edict on Responsibility for Cruel 
Treatment of Animals" was adopted. A struggle is being waged 
against cruel persons, several trials have been held, and 
articles on timely subjects are published in OGONEK, TRUD, and 
elsewhere. 
  The management organ is the presidium (at first with 4 
members, by April 1992 consisting of 10). The society has about 
30 active members. The chairman of the society is USSR People's 
Deputy and academician of the USSR Academy of Sciences A. V. 
Yablokov. 
  It belongs to the Moscow Ecological Federation (see 
article). 
  Address: tel. 190-68-33 (home), Yuliya Ivanovna Shvedova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Moscow Ecology Club of the Peace Defense Committee </H5>

["Moskovskiy ekologicheskiy klub pri komitete zashchity mira"] 
  The mission of the club is to save the Timiryazev Woods. 
This 
was the purpose, in particular, of the letter published in the 
newspaper ZELENYY MIR in April 1991 under the title, "Let's Save 
the Timiryazev Woods!" It was signed by the Moscow City Council 
of VOOP, the USSR Ecological Alliance (see article), the USSR 
Writers Union, and the USSR Journalists Union in addition to the 
Moscow Ecology Club. 
  One of the leaders of the club is N. Lyzlov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2. 
  -  "Let's Save the Timiryazev Woods!" 
ZELENYY MIR, No 13-14, 1991, p 10. 

<H3>    Greens Society of Leningradskiy Rayon of Moscow 
["Obshchestvo `zelenykh' Leningradskogo rayona g. Moskvy"] </H3>
  It appeared in 1988. The initiator was P. A. Kostromicheva. 
The society was registered with the rayon soviet. Its by-laws 
and program were adopted in the summer of 1990. 
  Goal: to have ecological awareness in society and provide 
information to the population. 
  Rallies are conducted and society members attend sessions of 
the soviet, work in the deputy commission or with it, and make 
inquiries. 
  Together with associates of the Institute of Geochemistry 
and 
Crystallography, they prepared a map of contamination of the 
rayon with heavy metals and other harmful substances and found a 
region contaminated with mercury--up to 50 times the permissible 
concentration; in some places radioactive contamination reaches 
160 milliroentgens per hour. The information was brought to the 
attention of deputies of the rayon soviet and the Mossoviet 
ecology commission, but no concrete steps were taken. 
  There are 30 activists, and the other members are not 
recorded. They have three cochairmen and a coordinating council. 
  The society collaborates with the Moscow Ecological 
Federation (see article). It does not have official premises. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Poklonnaya Gora [Poklonnaya Hill], Ecology Group </H5>

  It was formed in 1989 on the initiative of V. I. Pavlov and 
other residents of the microrayon. Its goal is to struggle to 
preserve the environment. It was thanks to the group's 
activities that a harmful printing shop of the Ministry of 
Defense was closed, and they helped in detecting radiation spots 
on Poklonnaya Hill. 
  There are about 15 members. They have no by-laws or program. 
The group is recorded at the Moscow Nature Committee (ul. 
Chaykovskogo). 
  Address: City of Moscow, pl. Pobedy, 1, krasnyy ugolok, 
contact tel. 148-59-28, 558-59-29, V. I. Pavlov, chairman. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Polar [Polyarnaya], Ecogroup </H5>

  It was formed in 1989 by an initiative group of residents of 
buildings in Medvedkovo. 
  Goals: 
  --ecological monitoring of industrial zone No 51 
(suspended the operation of two harmful production 
facilities--the Gidrostekloizol Plant of 
Construction-Installation Administration No 2 of Metrostroy and 
the Polimerplenka [Polymer Film] Cooperative). 
  --creation of a buffer zone (planted a greenbelt of 700 
trees). 
  There are about 30 persons involved, 6 activists. The group 
is headed by a chairman. Ten persons are public inspectors. 
  The social make-up is mainly office workers and medical 
personnel, with one deputy of the local soviet. 
  It has model by-laws and is registered in the nature 
protection sector at the Kirovskiy Ispolkom. It has no official 
premises. 
  Address: tel. 478-38-22, N. D. Kuznetsova, chairman. 
<H5>  Source of Information </H5>

  -  IMPD Archives, Fund 2. 

<H5>    Spring ["Rodnik"], Ecology Group </H5>

  It is an associated member of the Social Initiatives 
Foundation (city of Moscow). It organizes ecological education. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2. 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, p 118. 

<H5>    Sviblovo, Ecology Club </H5>
  It was formed in 1988 at the Institute for Advanced Studies 
of the Ministry of Chemical Industry by associates of the 
department of rational use of resources and environmental 
protection. 
  Tasks: the struggle for a clean environment, ecological 
education of the population, lectures and reports through the 
Znaniye Society, and a seminar at MEF on supplying water to 
Moscow. 
  Size: 30 members, 10 activists. Age: about 30-60 years old, 
office workers. They have no by-laws or program. There are no 
membership dues. There are no official premises. The chairman is 
A. K. Dadivanyan. 
  The club belongs to the Moscow Ecological Federation (see 
article) and the Greens Movement (see article). It takes part in 
the work of the ecology commission of the Babushkinskiy 
Raysoviet. 
  Address: City of Moscow, ul. Kolskaya, d. 2, Institute of 
Advanced Studies of the Ministry of Chemical Industry, tel. 
270-08-37 (home), Dadivanyan. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    North ["Sever"], Ecology Group </H5>

  It was formed in December 1989 at the North Housing 
Construction Cooperative in Moscow and joins together three 
cooperative buildings. In December 1989 notice was sent to the 
Kirovskiy Rayispolkom in Moscow of the formation of the 
ecogroup. The North Housing Construction Cooperative is a legal 
person and has a seal and a bank account. 
  Primary areas of work: rescuing the Losinyy Ostrov National 
Park from the Northern TETs and an industrial zone, cleaning and 
fixing up small rivers such as the Yauza, Chermyanka, 
Likhoborka, and others, and stopping radioactive contamination 
(one of the residents did experiments with cesium). It 
occasionally puts out fliers and appeals to residents. They took 
part in preparation of the collection of materials on the 
Northern TETs and in rallies directed against the policies of 
the Moscow mayor's office. 
  The total membership is about 1,800. They are building 
residents. There are 25-30 activists, with an average age of 
25-30. 
  People's deputies belong to the group: RSFSR deputy V. I. 
Novikov, Mossoviet deputies Gusev, Shekhova, and Nikulin, and 
raysoviet deputies Alekseyeva and Maslyakov. Deputy Gusev 
belongs to the Russian Greens Party. 
  Organizational structure: chairman of the group--N. N. 
Maslyakov, cochairman--A. A. Gusev. The council has two 
representatives from each building. 
  The group is a member of the Social-Ecological Alliance (see 
article) and the Moscow Ecological Federation (see article). 
  Address: city of Moscow, ul. Severodvinskaya, d. 13, k. 1, 
kv. 407; same address, kv. 332, tel. 479-99-63, Nikolay 
Nikolayevich Moslyakov (Maslyakov); tel. 478-43-77, Aleksandr 
Gennadiyevich Gusev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Sloboda </H5>

  A youth ecological-cultural association that has been 
operating in Baumanskiy Rayon of the city of Moscow since August 
1986. Goals: development of local self-government, making the 
historic part of the city a museum, and educational activities. 
Forms of work: seminars, meetings, assemblies, preparation of 
alternative plans, lectures, demonstrations, and the like. 
  In July 1986 there was an "occupation" of the Shcherbakov 
apartments to prevent them from being torn down. In August 1987 
picketing was organized at a building in Furmannyy Lane. By 
gathering signatures they were able to prevent the destruction 
of the Anna Mons apartments in connection with construction of a 
plant. 
  Sloboda took an active part in distributing leaflets during 
election campaigns. The association brings together 20-30 
persons--secondary and college students and creative 
intelligentsia. The average age is 25. There are 10 activists. 
  There is no clearcut organizational structure. There is a 
museum council whose functions are limited to monitoring the 
museum articles. 
  The association has a headquarters. It maintains close 
contacts with the Confederation of Anarcho-Syndicalists. 
Coordinators are G. Strizhenov, V. Turbolikov, and V. Gnezdilov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 194. 

<H3>    Council of Public Self-Government of the Lyublino-2 
Microrayon ["Sovet obshchestvennogo samoupravleniya mkrna 
Lyublino-2"] </H3>
  It was formed in 1989 by a group of residents, and by-laws 
were adopted in that year. The council was registered by 
decision of the ispolkom of the Lyublinskiy Raysoviet on 6 
December 1989. 
  Goal: improve the ecological situation in the microrayon and 
fix up and plant plants in the area. 
  A casting equipment plant is located nearby. Members of the 
council were able to get the USSR Council of Ministers to issue 
a decree stopping production at the Lyublino Casting Equipment 
Plant. 
  Membership is 200 persons. There are 10 activists, and 6 
members are raysoviet deputies. 
  Organizational structure--a presidium of the council, a 
chairman, deputy chairmen, and heads of commissions. There are 
no membership dues. 
  The council is a member of the Moscow Association of 
Self-Government Organs. 
  Addresses: ul. Krasnodonskaya, d. 39, tel. 351-21-79, V. A. 
Movchan, chairman of the council; tel. 351-48-21, M. F. Makarov, 
deputy of the raysoviet; tel. 355-74-97, A. D. Strom, chairman 
of the raysoviet ecology committee; tel. 351-25-36, S. M. 
Balabtseva, deputy chairman of the raysoviet ecology committee. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Studenets, Society </H5>

  It takes actions to preserve the Studenets historical park 
in 
the city of Moscow. It is a member of the Moscow Ecological 
Federation (see article). 
  Among the cochairmen of the society is Sofya Kuzminichna 
Kruglova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Tourism, Sport, and Recreation ["Turizm, sport, otdykh"], </H5>

Association 
  Goal--establishment of a University of Tourism with several 
branches: families, children, therapeutic, sports, and ecology. 
  In February 1991 they began giving lectures and conducting 
practical classes in the ecology tourism branch. The course of 
study is planned for 2 months. After completing it students on 
tourist excursions can make ecological observations of 
vegetation, the earth's surface, and streams of water, take 
samples, and work with instruments that measure radioactivity. 
This will allow organizations engaged in ecological assessment 
to enlist tourists to work in difficult-to-reach regions where a 
scientific party cannot always be sent. 
  President of the association is V. V. Malyakov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Vurleshin, M., "Backpacks--Only 
for the Educated" ZELENYY MIR, No 9-10, 1991, p 12. 

<H5>    Tushino </H5>
  Ecology club, formed in February 1987. 
  Primary goal--struggle to preserve the living environment. 
  Forms of activity: joint work with deputy groups; 
organization of volunteer ecology work days; participation in 
the Moscow ecology movement. 
  This club has about 100 members from 25 to 60 years in age. 
There are about 15 activists. 
  During the 1989 election campaign, the number of members 
almost doubled. 
  Membership is individual, and there are no dues. The program 
was adopted in November 1988. There were no by-laws, and they 
did not have a press organ. 
  In October 1988 the club conducted a rally under the slogan, 
"Popular political activism is a guarantee of perestroyka" (500 
persons). During the election campaign (T. Kh. Gdlyan was 
running in the district), several rallies were organized and 
drew from 300 to 4,000 persons. Signatures were gathered: in 
support of Yeltsin during the 1989 election campaign for USSR 
people's deputies (7,000 signatures) and in defense of an oak 
grove (500 signatures). 
  The club belonged to the Moscow Ecological Federation (see 
article) and the Ecology and Peace Association of SKZM [Soviet 
Peace Defense Committee] (see article). 
  In 1989 the club ceased to exist. In reality it was 
transformed into the Tushino Voters Club. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

  - 
<H5>  Fili, Regional Ecology Organization </H5>
  It was formed in 1989 by residents of the microrayon. 
By-laws 
were adopted and registered at the ispolkom of the raysoviet in 
the same year. 
  Goal--struggle to preserve the environment. 
  In the summer of 1990, an ecology rally was held in 
connection with construction of military plants. They 
participate in city ecology activities and in the broadcast 
program, "Good evening, Moscow!" There are some 15-20 members, 5 
activists, and 1 raysoviet deputy. No dues are collected. They 
have no official premises. 
  The organization is a collective member of the Greens 
Movement organization (see article). 
  Address: tel. 142-75-50, I. N. Zaikanova, chairman of the 
raysoviet ecology commission; tel 142-62-61, S. N. Glazunov, 
chairman of the organization. 
<H6>  Source of Information </H6>

  -  IPMD Archives, Fund 2. 

<H5>    Baikal Foundation ["Fond Baykala"], Moscow Branch </H5>

  In late 1990, the foundation, together with the Alternative 
Education Movement and the Pedagogues for Ecological 
Sophistication Association, organized a round table near 
Zvenigorod (suburban Moscow), with the title: 
"Cultural-Educational Complexes as a Way To Integrate the 
Spiritual-Intellectual Potential of Society." Participants in 
the round table--radical teachers, ecologists, philosophers, 
architects, and managers--adopted a plan of a public system of 
administration in the sphere of education, a draft declaration 
of the foundation entitled "Survival Through Education," and a 
program of cooperation and mutual assistance among round table 
participants, including the idea of a financial mechanism. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Rotin, M., "Parade of 
Alternatives," ZELENYY MIR, No 16, 1990, p 7. 

<H5>    Chermyanka, Ecological Society </H5>
  It was founded in 1989 by N. A. Kirpicheva (now a Mossoviet 
deputy) and an initiative group of residents. It was registered 
at the Mossoviet in October 1991. 
  Goals: improve the ecological situation in the rayon, 
struggle against construction of the Northern TETs, separate out 
the microrayon, and clean up the Chermyanka River. 
  Number of members--about 15, with 2 cochairmen (N. A. 
Kirpicheva and V. G. Rodionova), a 7-person council, an auditing 
commission, and a bookkeeper. 
  By-laws and a program were adopted in September 1991. 
  The society belongs to the Moscow Ecological Federation (see 
article) as a collective member, and several society 
participants are individual members of the MEF. 
  Resources come from voluntary donations by members of the 
society. 
  Address: city of Moscow, ul. Korneychuka, 47, kv. 192; tel. 
406-93-84 (home), N. A. Kirpicheva; tel. 405-60-19 (home), V. G. 
Rodionova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Foundation of Oktyabrskiy Rayon in Moscow </H5>

["Ekologicheskiy fond Oktyabrskogo rayona g. Moskvy"] 
  At the initiative of the foundation, the Oktyabrskiy Rayon 
Soviet, and a number of other organizations, the Moscow branch 
of the European Academy of Urban Environment (which was founded 
in Berlin in 1989) was set up in 1991. With the participation of 
foreign specialists, the Moscow branch developed an ecological 
plan for microrayon A-15 (development of recreation zones and 
planted areas and reconstruction of five-story buildings taking 
account of the opposition of residents to the construction of 
high-rise buildings without consideration of water supply system 
conditions). The construction of a high-rise building in A-15 
has now been suspended. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Kitayev, A., "Urban Ecological 
Initiatives: East-West Comparison," ZELENYY MIR, No 29-30, 1991, 
p 4. 

<H5>    Ecology ["Ekologiya"], Association </H5>
  It prepared for publication the following book: 
  "Obyedineniye 'Ekologiya': Vystavka proizvedeniy moskovskikh 
khudozhnikov. Katalog. Zhivopis, grafika, dekorativnoye 
iskusstvo" [The Ecology Association: Exhibit of the Works of 
Moscow Artists. Catalogue. Painting, Graphic Art, and Decorative 
Art], Moscow, Sovetskiy Khudozhnik, 1992, introductory article 
by Ye. A. Lisenkova. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  KNIZHNOYE OBOZRENIYE, No 12, 1992, 
20 March 1992, p 13. 

<H5>    Ecology--21st Century ["Ekologiya--XXI vek"] </H5>
  The organization engages in ecological education and studies 
problems of the introduction of new, "clean" technologies. 
  Address: 109544, city of Moscow, ul. B. Andronyevskaya, d. 
20, kv. 340, tel. 271-56-77 (home), Ruslan Markovich Nadreyev; 
tel. 268-26-67, Aleksandr Dmitriyevich Katamakhin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology and Journalism ["Ekologiya i zhurnalistika"], </H5>

Association 
  It was formed in 1990 by a group of journalists. It was 
registered at the Mossoviet in 1990. In the same year the 
by-laws and program were adopted. It brings together journalists 
who write on the subject of ecology. 
  Forms of work: organization of joint mass information 
actions 
and meetings between journalists and scientists, exchange of 
know-how, organization of ecology expeditions, propaganda for 
scientific advances in the field of ecology, and publishing 
activity. 
  The "Moskovskiy ekologicheskiy byulleten" [Moscow Ecology 
Bulletin] was prepared. It was planned to set up a press organ 
for the association. 
  There are about 100 members, with 10-15 activists. The 
average age is 30-40. The membership includes one Mossoviet 
deputy and deputies of local soviets. The association's work is 
organized by an executive committee which has a chairman and 
five committee members. There are no membership dues. 
  Address: city of Moscow, ul. Stankevicha, d. 20, k. 4; tel. 
178-36-78, 292-17-50, Vadim Nikolayevich Istomin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ekofam </H5>

  "Women in support of ecology programs." They study the 
effect 
of environmental pollution on human health. 
  Address: city of Moscow, tel. 170-09-30 (home), 269-46-22 
(work), Tatyana Viktorovna Popova; 248-71-12 (home), Tatyana 
Saulovna Gushchina, Sokolova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Energy-2050 [Energiya-2050], MEI (Moscow Power Engineering </H5>

Institute) Club 
  The club was founded in 1979, the same year in which the 
by-laws and program were adopted. 
  Goal: molding an ecological worldview and people's inner 
feelings and searching for ways to establish new ethics. 
  Club participants, among them people who work on problems of 
ecology professionally, give lectures for the Znaniye Society 
and conduct round tables to which scientists are invited. 
  There are 26 activists and up to 190 members in all. 
  The club is a member of the Social-Ecological Alliance (see 
article). 
  Club chairman is Ye. Melkumova. 
  Address: city of Moscow, Energeticheskiy proyezd, 3, DK MEI; 
coordinating tel. 362-75-17 (DK); tel. 444-20-98 (home), Marina 
Leshchikova; tel. 150-67-58 (home), Boris Volchek; tel. 
947-73-59, Yelena Melkumova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Altay Kray </H5>

<H5>  City of Barnaul </H5>
<H3>  Altay Social-Ecological Alliance [Altayskiy 
sotsialno-ekologicheskiy soyuz] </H3>
  It was founded in 1988. Its goal is to promote the 
development of no-waste production facilities, ecological 
education and tourism in the Altay, and solutions to other 
economic problems of the kray. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 656050, Altay Kray, city of Barnaul, ul. Antona 
Petrova, d. 152, kv. 35, tel. 41-81-97, Mikhail Yu. Shishin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Biysk </H5>

<H3>  Biysk Branch of the SES (Social-Ecological Alliance) [see 
article]) </H3>
  The branch promotes ecologically safe development of the 
Altay region. It is protesting construction of the Katun GES. It 
also works on questions of no-waste production. 
  Address: 659309 (or 659700), Altay Kray, city of Biysk, ul. 
Lermontova, d. 9, kv. 140, tel. 208-27, Vladimir A. Vasilyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Amur Oblast </H5>

<H5>  City of Blagoveshchensk </H5>
<H3>  Social-Ecological Alliance (SES) of the City of 
Blagoveshchensk </H3>
  Goal: ecological safety of the region. It is a member of the 
Social-Ecological Alliance (see article). One of the leaders of 
the alliance is Yu. I. Mikhalchenko, who was elected chairman of 
the ecology commission of the city soviet. 
  Address: 675006, Amur Oblast, city of Blagoveshchensk, ul. 
Kuznechnaya, d. 15, kv. 49, tel. 449-75, 250-10, Yuriy I. 
Mikhalchenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Zeya </H5>

<H3>  Zeyskiy Rayon Ecological Initiative Center ["Zeyskiy 
rayonnyy tsentr ekologicheskoy initsiativy"] </H3>
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 676200, Amur Oblast, city of Zeya, ul. 
Stroitelnaya, 
d. 57, kv. 1, Nikolay Nikolayevich Kulesh. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Arkhangelsk Oblast </H5>

<H5>  City of Novodvinsk </H5>
<H5>  Action ["Deystviye"], Ecology Organization (Ecoorganization) </H5>
  It was founded in 1989. Its tasks are to promote improvement 
in the ecological situation in the region while observing 
chemical and radioactive discharges into the White Sea. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 163901, Arkhangelsk Oblast, city of Novodvinsk, ul. 
Mira., d. 7-a, kv. 171, L. S. Gulyayev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Bashkortostan </H5>

<H5>  City of Ufa </H5>
<H5>  For Clean Air and Water [Za chistyy vozdukh i vodu] </H5>
  A social-ecological society, it was founded in November 
1987. 
It was formally organized on 6 May 1988. The society's by-laws 
and program were adopted in 1988. Membership is individual. 
There are about 70 members in all, with 10 activists. Meetings 
of the society are held on Fridays at 1900 hours in the 
gorispolkom building (20-30 participants). 
  The society works on ecological and social problems. It 
analyzes and adds to existing nature protection plans, chiefly 
relating to discharges of the chemical plants and oil 
refineries; it monitors the quality of food products and 
consumer goods, and public health. It watches to see that nature 
protection laws are obeyed, and it works on the problem of 
moving residents out of buffer zones. 
  On 29 November 1987, after the government adopted a decision 
to build a polycarbonate plant, more than 10,000 people came out 
to demonstrate and held a rally at the gorispolkom building. The 
initiative group for the rally (seven persons) made up the 
nucleus of the society. 
  The society tried to hold another rally on 22 June 1988 in 
connection with the 19th CPSU Conference. The city leadership 
moved the rally to the Sports Palace and "filled the hall mostly 
with people who were specially brought in" and "disrupted the 
speeches" of the rally initiators. After this the city 
authorities prohibited rallies. 
  "Society activists are being subjected to many forms of 
persecution and attacks in the republic and central press. D. 
Novitskiy was discharged from his job." 
  They are taking action against construction of the Bashkir 
AES. 
  They took part in the 1989 election campaign. They organized 
picketing and called for votes against Academician Tolstyakov 
and second secretary of the CPSU gorkom Yurin. They supported 
IZVESTIYA correspondent V. I. Prokushev (who became a USSR 
people's deputy) and the local mufti. 
  In February 1990 they joined the newly formed League of 
Democratic Forces of the city of Ufa. Since February the league 
has put out its newspaper UFIMSKOYE VREMYA monthly (editor in 
chief--S. G. Molodtsova). 
  In April 1990 a representative of the society joined the 
Unified Committee of Public Organizations (see article). 
  On 13 May 1990 within the framework of the league, they took 
part in the mass action called the "Living Chain." 20,000 
inhabitants of Ufa and nearby populated points 
(Novoaleksandrovka, Inors, Gastello) held hands and formed a 
living chain from the Council of Ministers of the Bashkir ASSR 
to the Khimprom [Chemical Industry] Production Association. 
  The society is a member of the Social-Ecological Alliance 
(see article). It collaborates with the ethnic cultural centers 
of the city, including the Tatar, Mari, Chuvash, Jewish, and 
German clubs Together with representatives of the Tatar, Mari, 
and German clubs the society joined the OKNF (10-20 persons from 
Ufa, Sterlitamka, and other cities). It worked to form a 
people's front. It took part in the formation of the Radical 
Democratic Bloc (formed in January 1990 during the struggle 
against the CPSU obkom). 
  Addresses: 450025, Republic of Bashkortostan, city of Ufa, 
ul. Lenina, d. 21, kv. 32,; tel. 22-44-89; Dim (Dmitriy) 
Yanovich Novitskiy; 450064, city of Ufa, ul. Komarova, d. 18, 
kv. 39; tel. 42-77-78; Saviya (Sanaya) Gimaletdinovna Molodtsova. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 222.(txt1} 
<H3>  Unified Committee of Public Organizations ["Obyedinennyy 
komitet obshchestvennykh organizatsiy"] </H3>
  Goal: coordination of the efforts of the independent public 
movement to improve the ecological situation in the region. It 
appeared as a reaction by the democratic community to serious 
contamination of drinking water after an accident at one of the 
chemical combines. 
  There are 28 members. Chairman is M. G. Safarov, a professor 
at Bashkir State University. 
  In April 1990 a representative of the For Clean Air and 
Water 
Society of Ufa (see article) joined the committee. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part. 2, p 222. 

<H3>    Bashkiria Branch of the Social-Ecological Alliance (SES) 
["Otdeleniy Sotsialno-ekologicheskogo soyuza (SES) Bashkirii"] </H3>
  In was founded in February 1989. Goal: to join together the 
ecology groups in Bashkiria. It protests against the reservoir 
on the Belaya River and the Bashkir AES, and against discharging 
phenol into the Ufa River. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 450053, Republic of Bashkortostan, city of Ufa, pr. 
Oktyabrya, d. 118, korp. 1, kv. 10, tel. 22-11-24, 34-62-96, 
Boris Nikolayevich Pavlov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Meleuz </H5>

<H5>  Ecology and Health ["Ekologiya i zdorovye"] </H5>
  The organization was founded in 1988 to prevent local and 
regional ecological disasters. It has three branches: Salavat, 
Meleus, and Sterlitamak. 
  The Salavat division is waging protest campaigns against the 
Ushtugan Reservoir on the Belaya River. The Meleuz and 
Sterlitamka branches are involved in ecological education and 
molding and studying public opinion. They gather and disseminate 
ecological information and take part in deciding problems of 
protecting the plant and animal worlds, preserving biological 
diversity, and developing the system of specially protected 
natural areas and sites, and problems linked to the construction 
and operation of hydroengineering structures. 
  The Sterlitamak branch monitors preservation of the 
environment, the quality of food products and consumer goods, 
and public health and participates in solving problems linked to 
industrial pollution, industrial and domestic waste, the use of 
atomic energy, and construction of AES's. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Addresses: 453310, Republic of Bashkortostan, city of 
Meleuz, 
ul. Lenina, d. 152, kv. 311, tel. 2-07-71, Yuriy I. Molchanov; 
453200, city of Salavat, ul. Akhtyamova, d. 12, kv. 239, A. Z. 
Kufterin; 453124, city of Sterlitamak, ul. Khudayberdina, d. 48, 
kv. 139, Vasiliy P. Skorin, people's deputy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Settlement of Nugush (Meleuzovskiy Rayon) </H5>

<H5>  Bashkiria, Initiative Group of GPN </H5>
  It was formed in 1988. It protests against construction of 
the reservoir on the Belaya River and has the goal of organizing 
the Bashkiria National Park. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 453320, Republic of Bashkortostan, Meleuzovskiy 
rayon, pos. Nugush, ul. Molodezhnaya, d. 1, Ivan A. Lavrentyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Salavat </H5>

<H5>  Ecology and Health </H5>
  See "Ecology and Health," city of Meleuz (Republic of 
Bashkortostan). 
<H5>  City of Sterlitamak </H5>
<H5>  Ecology and Health </H5>

  See "Ecology and Health," city of Meleuz (Republic of 
Bashkortostan). 
<H5>  Bryansk Oblast </H5>
<H5>  City of Bryansk </H5>
<H5>  Glasnost </H5>
  City debate club, formed in December 1988. It has 20 
participants. The range of interests covers ecology, politics, 
and human rights. It collaborates with the Public Initiatives 
Council in the city of Bryansk (see article). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...,"op. cit., vol 
1, part 2, p 155. 

<H3>    Noosphere ["Noosfera"] (other name--"Habitat" ["Sreda 
obitaniya"]), Ecoclub </H3>
  The club works on ecological education and holds debates on 
philosophical and ecological subjects. It is a member of the 
Greens Movement (see article). 
  Address: 241001, city of Bryansk, per. Aviatsionnyy, d. 4, 
korp. 1, kv. 38, tel. 1-55-10, Vladimir Ivanovich Sinitsin, 
chairman of the regional Greens Movement. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2 

<H5>    Public Initiatives Council ["Sovet obshchestvennykh </H5>

initsiativ"] (SOI) 
  Independent public organization. It was formed in March 1988 
as an organization to support perestroyka. On 1 December 1988 
the SOI Program was adopted. Goals: defense of the natural 
environment and the social, economic, and political rights of 
citizens and promotion of perestroyka. 
  It has three sections: ecology (the struggle to stop 
construction of the second phase of the Bryansk phosphate plant 
and against plans to build an atomic heat station), "atomic" 
(against construction of ATS's), and "social justice" (1,000 
signatures were gathered in favor of converting the oblast obkom 
hospital into a cardiology clinic). 
  In the 7 November 1988 demonstration, the council organized 
a 
separate column with ecology slogans. On 11 December 1988, a 
rally against construction of the second phase of the Bryansk 
phosphate plant was held in A. K. Tolstoy Park at the door of 
the gorsoviet session. 
  SOI meetings are held in the exhibit hall at the oblast 
branch of the Union of Artists and Journalists (usually 60-1,200 
participants). There are 40 activists, and a 14-member 
coordinating council. 
  The council collaborates with the Bryansk Glasnost Club (see 
article). It participates in the Greens Movement (see article). 
  Address: 241022, city of Bryansk, ul. Dimitrova, d. 81, kv. 
20, tel. 2-20-63, Aleksandr Borisovich Mudrov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galkina, L., "Zelenyye v SSSR...," 
op. cit., p 11; 
  -  "Rossiya: partii...," op. cit., vol 1, part 2, 
pp 154-155. 

<H5>    Habitat ["Sreda obitaniya"], Ecoclub </H5>
  See "Noosphere," City of Bryansk. 
<H5>  Buryatia </H5>
<H5>  City of Ulan-Ude </H5>
<H5>  Buryat Branch of the Baikal Foundation ["Buryatskoye </H5>

otdeleniye fonda Baykala"] 
  It was founded in February 1989 and registered in April 
1989. 
Its task is to consolidate all "green" forces to protect and 
restore Lake Baikal. It cooperates with local soviets, 
disseminates ecological information, and takes part in elections. 
  The management council is located in Irkutsk with branches 
in 
Ulan-Ude and Chita. The Buryat branch has affiliates in 
Kabanskiy and Severo-Baykalskiy rayons. Chairman is sanitary 
doctor A. A. Khakhalov. 
  Sources of financing are dues; the annual budget is 
R600,000. 
  Addresses: 670020, Buryatia, city of Ulan-Ude, Ul. 
Zhukovskogo, d. 23, turklub "Khamar-Daban," tel. 475-11, 
Aleksandr A. Khakhalov; 670020, Buryat SSR, city of Ulan-Ude, 
ul. Pushkina, d. 10, kv. 18, tel. 422-42, Aleksandr 
Tselovalnikov, secretary for Union and international relations. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    People for Baikal ["Narod za Baykal"] </H5>

  This is an ecology organization. It appeared in the fall of 
1989 during A. Limarenko's hunger strike in defense of Lake 
Baikal. The leader is L. Vasilyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Severobaykalsk </H5>

<H3>  Severobaykalsk Headquarters for the Defense of Lake Baikal 
["Severobaykalskiy shtab zashchity Baykala"] </H3>
  Its task is "to defend Lake Baikal through the combined 
efforts of local soviet authorities, cooperative members, and 
ecologists." It collaborates with the Earth Island Institute 
(United States). 
  Address: 671717, Buryatia, city of Severobaykalsk, ul. 
Lenina, d. 7, Fond zashchity Baykala; tel. 5-67 (home), Sergey 
V. Pisarev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Vladimir Oblast </H5>

<H5>  City of Vladimir </H5>
<H5>  Greens Movement ["Zelenoye dvizheniye"], Ecoclub </H5>
  It participated in the election campaign. It has deputies in 
local soviets. In March 1992 it joined the RPZ [Russian Greens 
Party] (see article). The club maintains a democratic 
orientation. 
  The chairman of the ecoclub is L. L. Voyeykov. 
  Addresses: 600005, city of Vladimir, ul. Studencheskaya, d. 
4a, kv. 5, tel. 7-03-02, 2-51-20, Gennadiy Alekseyevich 
Stakhurlov; 600022, city of Vladimir, ul. Zavadskogo, d. 9-a, 
kv. 65, tel. 4-31-01, Leonid Leonidovich Voyeykov. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H5>    City of Kolchugino </H5>
<H3>  Ecoclub of the Nature Protection Society ["Ekoklub pri 
Obshchestve okhrany prirody"] </H3>
  It organizes ecological education and participates in the 
Greens Movement (see article). 
  Address:601750, Vladimir Oblast, city of Kolchugino, ul. 
Druzhby, 18-a, kv. 60, tel. 2-35-30, Arkadiy Issakharovich 
Pinskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Volgograd Oblast </H5>

<H5>  City of Volgograd </H5>
<H3>  Lower Volga (Volgograd) Branch of the Committee To Save the 
Volga ["Nizhnevolzhskoye (Volgogradskoye) otdeleniye komiteta 
spaseniya Volgi"] </H3>
  The branch takes part in solving problems of protecting the 
plant and animal worlds, preserving biological diversity, and 
preserving and developing the system of specially protected 
natural areas and sites. 
  Address: 400003, city of Volgograd, ul. Yeliseyeva, d. 3, 
kv. 
48, Lidiya I. Savelyeva. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology ["Ekologiya"], Club </H5>

  This is a city organization. It was formed on 4 December 
1987 
and is registered. The total membership at the time of 
registration was 50, with an aktiv of 7. By 1989 the club had 
more than 500 members with an aktiv of 50-70. The club council 
has 39 members and the bureau has 9. Membership is individual. 
The club has a program and by-laws. 
  Task: to influence the policies of the authorities in the 
ares of atomic power, BVK's, pesticides, and waste pollution. 
  Forms of work: meetings, rallies, publications in the rayon 
and oblast press, and other things. 
  It holds weekly meetings in the DK [Palace of Culture] 
50-letiya Oktyabrya. The club organized and held rallies on the 
problems of pesticide production in the city on 17 February 1988 
at the Yubileynyy movie theater and on 2 October 1988 at the DK 
50-letiya Oktyabrya. About 2,000 and 5,000 people, respectively, 
participated. On 5 June 1988 the club organized an evening 
meeting on ecology at the DK 50-letiya Oktyabrya. During 1988 
they collected signatures on an appeal to the CPSU Central 
Committee concerning the city's ecological problems. 
  On 4 June 1989 a rally was held in Dvortsovaya Square at the 
club's initiative. It was dedicated to International 
Environmental Protection Day (about 1,000 participants). 
  On 20 June 1989 the club together with the Krasnoarmeyskiy 
Rayon CPSU committee held a meeting at the Khimik Palace of 
Culture at which the managers of all the ecologically "dirty" 
enterprises of Krasnoarmeyskiy Rayon in the city presented 
reports (about 700 participated in the meeting). 
  The club organized the all-Union scientific-practice 
conference under the title, "Movement of Cities To Ban Microbial 
Protein." It was held on 24-25 June 1989. Representatives of 
similar clubs in other cities--Kishari, Pavlodar, Nefteyugansk, 
Orenburg, Angarsk, and Kazan, including the "Six Sections" 
system, as well as scientists from Moscow and Leningrad (St. 
Petersburg) took part in the work of the conference. 
Participants at the conference adopted a resolution addressed to 
the USSR Supreme Soviet which demanded that all BVK plants be 
shut down, the Ministry of Biomedical Industry be eliminated, 
and only feed protein, soya, and other safe products be used. 
The conference was held at the Khimik DK, and about 300 persons 
took part. 
  On 5 August 1989 they took part in a rally at Volgodonsk 
devoted to shutting down the Rostov AES. 
  During the 1989 election campaign for USSR people's deputies 
in the national-territorial district, the club actively 
supported A. A. Kiselev, second secretary of the Volgograd Obkom 
of the Komsomol (his opponent was the writer Yu. Bondarev). 
Kiselev became people's deputy. Club member S. I. Umetskaya ran 
in one of the territorial districts but her candidacy was 
annulled by a district meeting. 
  On 11 February they took part in a rally on the Central 
Embankment (2,000 participants) demanding the retirement of 
Albert Orlov, chairman of the oblispolkom, and the editorial 
board of VOLGOGRADSKAYA PRAVDA. An appeal from the local 
division of the KhDS [Christian Democratic Union] was read. 
  On 25 February 1990 about 15,000 people took part in a rally 
in support of the Democratic Russia bloc of candidates. 
  On 7 March 1990 they took part in picketing organized by the 
Citizens Action Committee at the ispolkom of Tsentralnyy Rayon 
in the city. (The ispolkom had adopted a decision moving 
citywide rallies from Central Embankment to the square in front 
of Lenin Stadium.) 
  The club is a member of the Ecology and the 21st Century 
association (see article) and maintains regular contacts with 
ecology groups in the United States, Austria, and other 
countries. It collaborates actively with the Ecology Club that 
is operating in the town of Svetlyy Yar and is waging a struggle 
against the BVK plant and the use of toxic chemicals in the 
fields. 
  Addresses: 400080, city of Volgograd, ul. 40-letiya VLKSM, 
DK 
"50 let Oktyabrya," club "Ekologiya," tel. 66-04-22 (work), 
Alfred A. Pavlenko; 400055, city of Volgograd, pr. Geroyev 
Stalingrada, d. 18, kv. 40, tel. 67-21-66 (home), 66-02-31 
(work), Irina R. Belay; city of Volgograd, ul. Fadeyeva, d. 13, 
kv. 42, tel. 67-10-75, Svetlana N. Lvova; tel. 44-44-08, 
Svetlana Umetskaya. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 2, pp 156-157. 

<H5>    City of Volzhskiy </H5>
<H5>  Volzhskiy, Socialist Group </H5>
  It was formed in February 1988, initially with 10 members 
and 
then 12 in 1989; the aktiv was 5 persons. The social composition 
is students, workers, and intelligentsia. Average age--25-30 
years. 
  In early June 1988 a rally was held in the city on the 
group's initiative under the slogan, "All Power to the Soviets" 
(30 participants). 
  The group participates in ecology actions: in surveys of 
public opinion and collection of signatures against pollution of 
the atmosphere by chemical enterprises. In June 1988 they 
organized and held a citywide debate entitled, "Ecology and 
Children." In August 1988 they conducted a week devoted to 
defense of the Volga; in December 1988--an ecology photo exhibit 
at the DK Oktyabr; and in March 1989--a rally on ecological 
problems of the city (held on Central Square, about 1,000 
persons). 
  The group participates in the Citizen ["Grazhdanin"] 
"informal" information center which was established in August 
1988 and holds weekly meetings in apartments. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 2, p 158. 

<H3>    Volzhskiy Ecological Alliance ["Volzhskiy ekologicheskiy 
soyuz"] </H3>
  It was founded in 1988. Club members visit enterprises to 
explain ecological dangers and also engage in politics. They had 
some success in shutting down ecologically dangerous 
enterprises. The club's activities receive support from the 
local soviet leadership. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 404100, Volgograd Oblast, city of Volzhskiy, ul. 
Engelsa, d. 2. kv. 22, tel. 7-55-92, 7-92-73, Sergey L. 
Berdnikov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Vologda Oblast </H5>

<H5>  City of Vologda </H5>
<H5>  Vologda Ecology Club ["Vologodskiy ekologicheskiy klub"] </H5>
  The club participates in solving questions of industrial and 
agricultural pollution of the environment. 
  Address: 160000, city of Vologda, pr. Pobedy, d. 37, 
Pedinstitut, kafedra geologii, tel. 2-51-31, Ivan G. Dzhukha. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Voronezh Oblast </H5>

<H5>  City of Voronezh </H5>
<H3>  Ecological Initiative ["Ekologicheskaya initsiativa"], 
Movement </H3>
  It appeared in October 1988. Tasks: collecting and 
publishing 
information on ecological problems and conducting political and 
ecology campaigns. Forms of activity: collection of signatures, 
organization of public opinion surveys, publication of articles 
on ecological issues in the local press, and organization of 
conferences and debates. 
  From November 1988 through August 1989 they gathered about 
100,000 signatures against the Voronezh Atomic Heat Plant (VAST). 
  On 26 April 1990 they held a rally devoted to the 
anniversary 
of the accident at the Chernobyl AES (300 persons). 
  On 15 May 1990 a referendum on the problems of construction 
of the VAST was held. 96 percent voted for construction and 
reconstruction of a heat and power plant without an atomic plant 
(of the 81.1 percent who took part in the voting). Just before 
the referendum, on 13 May, a rally against construction of the 
VAST was held on the initiative of Ecological Initiative, 
Cultural Initiative, and the Voronezh People's Front. 
  The immediate goal was creation of a public council at 
Goskomprirody, with access to ecological information, the 
opportunity to organize independent expert studies, and so on. 
  During the 1989 election campaign they and other independent 
groups supported V. I. Kirillov, senior scientific associate at 
the Voronezh Polytechnic Institute. He was elected USSR people's 
deputy. Six members of Ecological Initiative became deputies of 
the city soviet of people's deputies. 
  Individual membership is envisioned by the statute, but 
there 
are no membership dues. In 1989 there were 15 members. Average 
age is 28-30. Social-vocational composition: associates at 
VUZes, students, and workers. There is no chairman. The movement 
is a collective member of the Social-Ecological Alliance (see 
article). Some representatives of the group (3 persons in 1989) 
are individual members of the SoES. They have cooperated with 
Goskomprirody in disseminating information. 
  Address: 394036, city of Voronezh, ul. Komissarzhevskoy, d. 
10a, kv. 14, tel. 50-21-94, Anatoliy M. German; tel. 52-13-30, 
Olga Iventyeva. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 1, p 159. 
<H5>  City of Bobrov </H5>
<H3>  Initiative Group To Save the Bityug River ["Initsiativnaya 
gruppa po spaseniyu reki Bityug"] </H3>
  The group does ecological studies: ecological expert study 
of 
economic plans and management decisions; development of 
alternative plans, designs, and technologies; monitoring of the 
quality of food products and consumer goods and public health 
and monitoring compliance with nature protection laws. 
  The group is protesting against the local sugar plant. 
  Address: 397710, Voronezh Oblast, city of Bobrov, ul. 
Turbina, d. 42, kv. 1, Aleksandr T. Petrov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Vyatka Oblast </H5>

<H5>  City of Vyatka (Kirov) </H5>
<H5>  Ecology and Peace ["Ekologiya i mir"], Association </H5>
  It monitors preservation of the environment, the quality of 
food products and consumer goods, and public health. It 
organizes ecological education, study of public opinion, and the 
gathering and dissemination of ecological information. 
  It takes part in solving problems of preserving topsoil, 
protecting the plant and animal worlds, and developing a network 
of specially protected natural areas and sites, as well as 
problems related to industrial pollution, industrial and 
domestic waste, the use of atomic energy and construction of 
AES's, and construction and operation of hydroengineering 
structures. 
  Address: 610001, city of Vyatka, ul. Engelsa, d. 41a, OKZM, 
Vladimir Kasatkin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Gornyy Altay </H5>

<H5>  City of Gorno-Altaysk </H5>
<H5>  Gornyy Altay Branch of the SES </H5>
  It originated at the city Political Center in November 1988. 
  It is participating in the struggle against the Katun GES. 
  Address: 659700, Republic of Gornyy Altay, city of 
Gorno-Altaysk, ul. Golovina, d. 7, kv. 25, Sergey Ivanovich 
Kerchilev; tel. 45-38, Nikolay Vitovtsev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Cedar ["Kedr"], Society (Greens Movement) </H5>

  It works on questions of preserving the forests. 
  Address: 659700, Republic of Gornyy Altay, city of 
Gorno-Altaysk, ul. Gorno-Altayskaya, d. 33, kv. 1, tel. 70-77, 
Vasiliy T. Samykov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Committee To Save the Katun and Gornyy Altay ["Komitet </H5>

spaseniya Katuni i Gornogo Altaya"] 
  This is the Gornyy Altay branch of the Social-Ecological 
Union (see article). 
  It was formed with the goal of preventing construction of 
the 
Katun GES; construction of the dike could lead to the poisoning 
of 3 million inhabitants with mercury discharges. The committee 
demands that the Katun River valley be given preserve status and 
be included in the UNESCO world heritage list. 1990 was declared 
the year of Katun. 
  It has a branch in Novosibirsk. 
  Addresses: 659700, city of Gorno-Altaysk, ul. Golovina, d. 
7, 
km. 26, tel. 54-32, Sergey I. Kerilev; 630117, city of 
Novosibirsk-117, ul. Polevaya, d. 16, kv. 5, V. Geydt. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Dagestan </H5>

<H5>  City of Makhachkala </H5>
<H3>  Republic Public Committee To Save the Caspian 
["Respublikanskiy obshchestvennyy komitet spaseniya Kaspiya"] </H3>
  The committee was formed with the goal of "coordinating the 
ecological forces of the republic and enlisting broad strata of 
the community to help state organs save a unique natural object 
of natural and global importance." It was registered by 24 
January 1991 by the Ministry of Justice of the Dagestan ASSR. 
  Its founders were the DASSR Goskomprirody, the Dagestan VOOP 
Council, scientific research institutes, VUZes, editorial boards 
of republic newspapers, the state committee for radio and 
television, and public formations. 
  At the founding conference of the committee, an appeal to 
the 
inhabitants of the Azerbaijan, Kazakh, and Turkmen SSSR's and 
the RSFSR regions bordering the Caspian was adopted calling on 
them to "join the noble cause" and form their own public 
committees to save the Caspian. A special interrepublic council 
was established for this purpose. A decision was also adopted to 
send a corresponding appeal to the public in the Islamic 
Republic of Iran. 
  The committee participated in the 1st International 
Conference on Problems of the Caspian Sea (Baku, 13-17 June 
1991), which brought together scientists and specialists in the 
field of ecology and the heads of state nature protection 
organizations and public ecology formations. 
  Address: Dagestan, city of Makhachkala. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 1; 
  -  MOLODEZH AZERBAYDZHANA, 23 May 
1991, p 1; 
  -  Filmonov, I., "The Committee To Save the Caspian," 
ZELENYY MIR, No 3-4, 1991, p 1. 

<H5>    Ecocenter ["Ekotsentr"] </H5>
  It was formed at the oblast committee of the All-Union 
Komsomol. 
  Address: 367012, Republic of Dagestan, city of Makhachkala, 
ul. Buynakskogo, d. 9, OK VLKSM, Ekotsentr, tel. 7-05-15, 
7-91-58, Sergey Konstantinovich Monakhov, director of the 
Ecocenter. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Yekaterinburg Oblast </H5>

<H5>  City of Yekaterinburg (Sverdlovsk) </H5>
<H5>  Business Ecology Club ["Delovoy ekologicheskiy klub"] </H5>
  It was founded in 1988. Goal--to join together business 
people and associates of state industrial and nature protection 
institutions to discuss common problems. 
  Address: 620098, city of Yekaterinburg, ul. 
Kommunisticheskaya, d. 14, kv. 8, tel. 31-26-59, Valeriy V. 
Shamin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Movement ["Zelenoye dvizheniye"], Ural Regional </H5>

Federation 
  It monitors the state of the environment in the region. It 
has deputies and monitors the gorsoviet ecology commissions. It 
struggles against cutting the forests, contaminating the soil 
with fertilizers, and ecologically harmful enterprises. 
  It participated in forming the Greens Party (see article). 
It 
is a member of the Greens Movement (see article). 
  One of the collective members of the federation is the Ozone 
Club in Yekaterinburg (see article). 
  Address: 620102, city of Yekaterinburg, ul. Yasnaya, d. 30, 
kv. 32, tel. 23-99-15, Nikolay Mikhaylovich Kalinkin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ozone ["Ozon"], Oblast Ecology Club </H5>

  It is a member of the Greens Movement (see article) and also 
of the Greens Movement Ural Regional Federation (see article). 
It belongs to the Yekaterinburg Oblast sociopolitical movement 
"Democratic Choice." 
  Address: 620000, city of Yekaterinburg, pr. Lenina, d. 34, 
kv. 404, tel. 51-31-80, Gennadiy V. Rashchupkin; 620102, city of 
Yekaterinburg, ul. Yasnaya, d. 30, kv. 32, tel. 23-99-15, 
Nikolay Mikhaylovich Kalinkin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Kamensk-Uralskiy </H5>

<H3>  Ecology Committee of the Kamensk-Uralskiy Society of 
Regional Specialists ["Ekologicheskiy komitet Kamensk-Uralskogo 
Obshchestva krayevedov"] </H3>
  It is a member of the Social-Ecological Alliance (see 
article). They study the impact of industrial and agricultural 
pollution on the health of the population and on the 
disappearance of certain plant and animal species. 
  Address: 623413, Yekaterinburg Oblast, city of 
Kamensk-Uralskiy, ul. Isetskaya, d. 14, kv. 6, tel. 2-64-98 
(home), 2-36-20 (work), Vladimir P. Shevalev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Nizhniy Tagil </H5>

<H5>  Purification ["Ochishcheniye"], Ecology Club (EKO) </H5>
  This is an initiative group formed on 29 February 1988 after 
the 13 February ecology rally. The Purification Ecology Club has 
operated since April 1988 when the founding meeting was held. On 
8 September 1988 the club was registered at the gorispolkom. In 
the same month EKO adopted by-laws which envision individual and 
collective membership and dues. A council of nine persons was 
formed. The Purification program was made public at a rally on 
15 October 1989. Open meetings of the club (15-70 participants) 
were held weekly at the Yubileynyy DK. 
  The goal of the club is to improve the ecological situation 
in the city relative to air pollution by the Nizhniy Tagil 
Metallurgical Combine. 
  Forms of work: holding rallies in defense of the 
environment, 
participating in elections, organizing exhibits, and holding 
contests on ecology subjects, and the like. 
  Its size in 1989 (maximum) was: aktiv--20 persons, 
collective 
members--more than 500, individual members--70. In February 1992 
the aktiv was 4 persons, individual members were less than 30, 
and there were really no collective members. 
  Social-occupational composition: engineering-technical 
personnel, workers, students. Ages--from 20 to 55 years. 
  Source of financing--dues. 
  It does not have a press organ. Activities: on 5 July 1988 
an 
ecology rally was held on Teatralnaya Square, dedicated to World 
Environmental Protection Day and organized by independent groups 
(up to 3,000 participants). After the rally there was organized 
gathering of signatures (about 30,000) on an appeal to the 
Presidium of the USSR Supreme Soviet concerning the need for a 
fundamental improvement in the ecological situation in the city. 
Leaders of enterprises, the CPSU gorkom, and the gorispolkom who 
agreed with the assessment of the situation spoke. Members of 
the Rally-87 group (Sverdlovsk-Yekaterinburg, including S. 
Kuznetsov, who is now an RSFSR people's deputy) and independent 
journalists participated in the rally. 
  On 14 July 1988 a session of the gorsoviet devoted to 
discussion of ecological problems was held. Club representatives 
spoke at it, criticizing the measures proposed by the 
authorities to normalize the situation and calling these 
measures intolerable (large expenditures and small impact). 
  On 30 July 1988 Purification conducted a silent protest by 
women (30-40 persons) in front of the entrance to the 
metallurgical combine (against the ecologically harmful 
equipment of the combine). 
  In September 1988 the Resurrection ["Vosrozhdeniye"] public 
committee was formed on the basis of the group for socioeconomic 
problems, the group to save the A. Nevskiy Cathedral, and some 
EKO members (problems areas were ecology, preservation of 
architectural monuments, and the like). 
  During the 1989 election campaign for USSR people's 
deputies, 
the club members together with the Resurrection group actively 
supported the candidacy of Kudrin, who was running in the 
national-territorial district, and organized meetings with the 
voters for him. 
  On 12 February 1989 they held a rally devoted to the city's 
ecological problems (800-900 persons participated). At the rally 
club activists called on voters to vote for candidates who were 
fighting for ecology. 
  V. A. Baklanova, member of the council of the Purification 
Club, was nominated as a candidate for USSR people's deputy from 
the Movement for Democratic Elections coalition (formed in early 
1989 by the Purification and Resurrection groups), but she was 
not elected. 
  On 11 August 1989 a drawing contest on asphalt for children 
was organized, with ecology topics, under the slogan: "Live, 
Land!" 
  In the course of 1988-1989, open meetings of the club were 
held weekly (15-70 persons participated) at the Yubileynyy DK. 
  Later the organization's activities in reality ended. In 
1990 
meetings began to be held once every 2 months, and then they 
stopped entirely. There was just one meeting in 1991. Only in 
January 1992 was an attempt made to revive the club; a new 
chairman (V. A. Baklanova) was elected and goals for further 
action were outlined. 
  The club is a member of the Social-Ecological Alliance (see 
article). 
  Addresses: 622034, Yekaterinburg Oblast, city of Nizhniy 
Tagil, ul. Goroshnikova, d. 64, kv. 75, tel. 5-12-93, Vera A. 
Baklanova; 622035, city of Nizhniy Tagil, ul. Entuziastov, d. 5, 
kv. 22, tel. 3-11-19, Natalya Ovcharenko. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2' 
  -  "Rossiya: partii...," op. cit. 
vol 1, part 2, p 201. 

<H3>    Ecology, Nizhniy Tagil Labor Association ["'Ekologiya,'" 
Nizhnetagilskoye trudovoye obyedineniye"] </H3>
  Its members work for the organization 3 days a week, and the 
money goes for urban public health. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 622034, Yekaterinburg Oblast, city of Nizhniy 
Tagil, 
ul. Parkhomenko, d. 1, kv. 2, B. A. Zhuravlev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Pervouralsk </H5>

<H5>  Chance ["Shans"], Ecoclub </H5>
  The club monitors nature protection. It studies the impact 
of 
environmental pollution on the health of the population. 
  Address: 623105, Yekaterinburg Oblast, city of Pervouralsk, 
ul. Engelsa, d. 13a, Laboratoriya okhrany prirody, tel. 9-52-23, 
Vladimir S. Plyusnin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ivanovo Oblast </H5>

<H5>  City of Ivanovo </H5>
<H5>  Ecologist ["Ekolog"] </H5>
  This is an Ivanovo city club. It was formed in the fall of 
1988 at the city DK. It gathered signatures against construction 
in the refuge zone of an AES designed to supply power to the 
cities of Kineshma and Ivanovo, and signatures in support of the 
Greens movement. Club members met weekly. They organized the 
Ivanovo Montmartre. 
  In 1989 club representatives joined the coordinating council 
of independent sociopolitical associations of the city. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 2, p 161. 

<H5>    Ecology ["Ekologiya"] </H5>
  This is an Ivanovo Oblast society. It was founded in the 
fall 
of 1988 at the city DK. Several thousand signatures were 
gathered in opposition to construction of the AES. 
  Address: 153000, city of Ivanovo, ul. Zvereva, d. 7/2, kv. 
1, 
tel. 4-26-80, S. Volkov, Mikhail Zhavoronkov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Irkutsk OblasT </H5>

<H5>  City of Irkutsk </H5>
<H3>  Movement in Defense of Baikal ["Dvizheniye v zashchitu 
Baykala"] </H3>
  The movement originated in May 1987 among scientific 
associations in Akademgorodok and was registered in 1988. There 
were no more than 60 members at the end of 1988, primarily 
scientists, students, and engineering-technical personnel. They 
had five leaders. There were no by-laws or program. The movement 
had five branches (Angarsk, the Angara Ecology Movement, Baikal, 
Bratsk, and Ust-Ilimsk). 
  Goal--to defend Lake Baikal against harmful discharges and 
uncontrolled industrial construction. "The principal enemy is 
the pulp and paper combine" (the Baikal Pulp and Paper 
Combine--TsBK). 
  Forms of work: doing practical scientific research, 
organizing and holding ecology rallies, and others. 
  Among the movement's activists are Vera Sekerina, Anatoliy 
Sosunov, Viktor Madonov, and T. Amarkhanova. 
  They did not have a press organ. 
  The movement is a member of the Social-Ecological Alliance 
(see article). 
  In 1987-1988 the movement set up "Baikal defense posts" and 
organized several rallies. The first rally was held in the 
summer of 1987 (1,000 participants). On 20 June 1987 the first 
Baikal defense post was organized at the railroad terminal 
square. On 26 November of the same year a rally against the 
pipeline carrying waste from the Baikal TsBK into the Irkutsk 
River was held on Constitution Square (about 8,000 
participants); a demonstration with the same slogans was 
conducted in May 1988 (10,000 participants). From May 1987 
through June of the next year 107,000 signatures were collected 
against construction of the pipeline. After the spring of 1989 
the rallies were stopped. 
  "There were some incidents with the militia during public 
actions." 
  In 1988 they participated in social-ecological conferences 
in 
Moscow and Odessa and in the all-Union social-ecological expert 
study of Baikal in Listvyansk. 
  In October 1988 they nominated their own candidate for the 
job of chairman of the oblast nature protection committee, but 
official organs rejected it. 
  In early 1989 they collected signatures to protest against 
construction of the Volga-Chorgay Canal. Several thousand 
signatures were collected, and the USSR Supreme Soviet was 
notified of this by telegram. 
  The movement joined the Baikal People's Front. It 
participated in the 1989 election campaign for USSR people's 
deputies. Along with other groups belonging to the Baikal 
People's Front, participants of the movement supported the 
candidacy of economist G. N. Filshin, who was elected USSR 
people's deputy. 
  In April 1989 the movement was the initiator in 
establishment 
of the Baikal Foundation (see article), after which activities 
within the framework of the movement ceased. 
  Addresses: 664058, city of Irkutsk, Pervomayskiy mkrn., d. 
9, 
kv. 8, tel. 46-35-51, Vera Nikolayevna Sekerina;; 664033, city 
of Irkutsk, Institut geokhimii RAN, tel. 46-57-52 (home), 
46-19-18 (work), Valeriy Stepanovich Zubkov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, p 129. 

<H3>    Left Bank Citizens Initiatives Club ["Klub grazhdanskikh 
initsiativ levogo berega"] at Akademgorodok </H3>
  Tasks--ecological and political. 
  The club was organized in the summer of 1988 from the voters 
club of Akademgorodok. It has about 100 participants, and an 
aktiv of 30-40. The leader is V. Naumov. Thanks to club support, 
in the summer of 1988 V. Naumov became a deputy to the oblast 
soviet. 
  The club opposed construction of a BVK production facility 
in 
Akademgorodok. 
  At meetings there is discussion of questions of 
environmental 
protection as well as problems of glasnost, lawmaking, and the 
like. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, p 128. 

<H3>    Society for the Defense of Baikal ["Obshchestvo zashchity 
Baykala"] </H3>
  It was founded in November 1987 and registered in 1988 at 
the 
Limnological Institute. There are 40 participants and an aktiv 
of 9. The goal is to have Lake Baikal included in the UNESCO 
Natural Heritage List. 
  Since December 1988 they have put out five issues of VESTNIK 
OBSHCHESTVA ZASHCHITY BAYKALA [Herald of the Society for the 
Defense of Baikal]. The sixth issue came out in March 1990 as 
the independent sociopolitical journal called DEMOKRATICHESKIY 
VESTNIK [Democratic Herald] (photoprint, 44 pp, editor P. Malyy). 
  It conducts rallies together with the Movement for the 
Defense of Baikal (see article). 
  It almost completely ceased its activities in 1989. 
  Address: 664074, city of Irkutsk, ul. Lermontova, d. 77, kv. 
117, tel. 41-63-43, Pavel V. Malykh. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit. vol 
1, part 1, p 128. 

<H5>    Socialist Club ["Sotsialisticheskiy klub"] </H5>
  It originated in May 1988. It was a member of the Federation 
of Socialist Public Clubs. It participated in organizing 
picketing of the Baikal BVK. In January 1989 it joined the 
Confederation of Anarcho-Syndicalists. The leader is I. 
Podshivalov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Baikal Foundation ["Fond Baykala"] </H5>

  This is an independent social-ecological organization. 
  It was formed in early 1989 by a group of Irkutsk volunteer 
organizations. The initiator, and later a collective member, was 
the Movement in Defense of Baikal (see article). It was 
officially registered in 1989. The foundation's by-laws and 
program were adopted in April 1989. 
  Territorially the foundation includes four branches: 
Irkutsk, 
Buryat, Chita, and Moscow. 
  Forms of work: doing scientific-practical research, 
organizing and conducting ecology rallies, and others. 
  Membership--about 160, including about 100 in Irkutsk. Aktiv 
is 10-15 persons. 
  The foundation has both collective and individual 
membership. 
  The foundation's activity is directed by a coordinating 
council (earlier it was called the central council, and G. I. 
Filshin was the chairman) that consists of 11 persons. The 
chairman of the coordinating council is V. V. Montato. 
  The foundation does not have a press organ. 
  By August 1989 the activists had collected more than 
R600,000, designated for activities to protect Baikal. In 
October 1989 they participated in a rally against construction 
of a ceramic materials plant in the city. 
  The foundation holds a general meeting with a report by the 
coordinating council on work done once every 2 years (1989, 
1991). 
  The foundation took an active part in elections for USSR and 
RSFSR people's deputies. With its help G. I. Filshin was elected 
a USSR deputy, I. K. Shirobokov became an RSFSR deputy, and 
several members became deputies on the oblast soviet. 
  At the present time no "mass" work is being done. The 
organization is working on setting up "ecology cooperatives" and 
a tourist center and conducting ecological expert studies. 
  Address: 664043, city of Irkutsk, bul. Ryabikova, d. 39, kv. 
61, tel. 24-26-27, 24-25-27, Marina N. Khamarkhanova. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, pp 128-130. 

<H5>    City of Angarsk </H5>
<H3>  Angarsk Ecology Movement ["Angarskoye ekologicheskoye 
dvizheniye"] </H3>
  It was formed in October 1988 in Angarsk. The cause of its 
formation was discharges of toxic substances by the BVK 
production combine, which led to rallies in October and November 
1988 (1,000 and 3,500 participants, respectively). About 40 
people participated in the election struggle of 1989-1990. 
  It is a member of the Baikal People's Front. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," vol 1, part 
1, p 128. 

<H5>    Ecology Committee ["Ekologicheskiy komitet"] </H5>
  It favors shutting down the enterprise in the city that 
produces protein-vitamin concentrates (BVK) and solving other 
regional ecological problems. 
  Address: 665820, Irkutsk Oblast, city of Angarsk, ul. 
Voloshilova, d. 22, kv. 44, Sergey V. Popov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Bratsk </H5>

<H3>  Ecology Movement of the City of Bratsk ["Ekologicheskoye 
dvizheniye g. Bratska"] </H3>
  The movement is striving to avert an ecological disaster in 
the Bratsk region. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 665725, Irkutsk Oblast, city of Bratsk-25, p/ya 
2621, Mikhail D. Ledetskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Ust-Ilimsk </H5>

<H3>  Initiative Group for the Defense of Perestroyka 
["Initsiativnaya gruppa zashchity perestroyki"] </H3>
  Tasks: "Struggle against bureaucratism and corruption, 
defend 
the rights and interests of citizens, ecology." 
  The group was formed in February 1988. It was registered at 
the gorispolkom. A program and by-laws have been adopted. The 
criterion of membership is active work in the group. There are 
about 40 persons, mainly workers, engineers, and office workers, 
and the average age is 35-50. 
  There are two sections: ecology and social monitoring. In 
1988 they organized a trip to the city by the "Searchlight of 
Perestroyka" group from Central Television. They criticized the 
course of election of delegates to the 19th All-Union Party 
Conference. They passed out leaflets which criticized the 
activities of a number of city executives. 
  They collected signatures against construction of the 
Ust-Ilimsk Pulp and Paper Mill and other projects. They 
conducted ecology rallies in Ust-Ilimsk and the community of 
Nevan. They spoke on ecological matters at a session of the city 
soviet. 
  Meetings are held in apartments; if officials help out they 
may be held in the Druzhba DK or the DK imeni Naymushin. 
  A split occurred in the group at the 1 November 1988 
session. 
Seven persons withdrew from membership, accusing the chairman of 
the group of playing politics. The group works with the 
Committee To Promote Perestroyka of the city of Krasnoyarsk. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 222. 

<H5>    Kabardino-Balkaria </H5>
<H5>  City of Nalchik </H5>
<H5>  Greens Movement ["Zelenoye dvizheniye"] </H5>
  It is a city organization and participates in solving 
problems linked with agricultural pollution. 
  Address: 360004, Kabardino-Balkaria, city of Nalchik, ul. 
Tolstogo, d. 185 (Agromeliorativnyy institut), Dmitriy Dudov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Initiative Ecology Group ["Initsiativnaya ekologicheskaya </H5>

gruppa"] 
  It studies the ecological situation in the region and works 
on ecological education. 
  Address: 360017, Republic of Karbardino-Balkaria, city of 
Nalchik, ul. Baysultanova, d. 13, kv. 44, tel. 5-24-47, T. N. 
Podva. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Kaliningrad Oblast </H5>

<H5>  City of Kaliningrad </H5>
<H5>  Resurrection ["Vozrozhdeniye"] </H5>
  It is a city ecological-cultural society. It appeared in 
early 1988 on the basis of a group at Kaliningrad GU for 
studying the heritage of Immanuel Kant. In addition to the study 
of Kant, the society devotes attention to the protection of 
nature and restoration of monuments. It has by-laws and a 
program. Membership is individual, and at the beginning of 1989 
the society had about 100 persons, with the average age being 
18-20. 
  The society collaborates with the Ecological Monitoring 
Committee of the Leninskiy Rayon Youth Center (see article). 
  Address: city of Kaliningrad, tel. 2-82-74, Viktor 
Batishchev. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii..." op. cit., 
vol 1, part 2, p 163. 

<H3>    Ecological Monitoring Committee ["Komitet ekologicheskogo 
kontrolya"] </H3>
  It was formed in the fall of 1988 at the Leninskiy Rayon 
Youth Center. It collaborates with the Resurrection Society (see 
article) in the city. The aktiv has 15 members. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 163. 

<H5>    Kalmykia </H5>
<H5>  City of Elista </H5>
<H3>  Kalmyk Steppe ["Kalmykskaya step'"], Social-Ecological 
Association </H3>
  It was formed in 1989. Goal: to prevent the steppe from 
being 
turned into a desert. It carries on ecological research and 
protested against construction of the Volga-Chogray Canal. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 358014, city of Elista, 8-y mkrn, d. 21, kv. 18, 
tel. 4-14-15, Nina Stepanovna Kalyuznaya. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 1. 

<H5>    Kaluga ObLast </H5>

<H5>  City of Kaluga </H5>
<H5>  Ecology Center ["Ekologicheskiy tsentr"] </H5>
  It takes action against industrial and agricultural 
contamination of the Oka River. The center conducts ecology 
debates. 
  Address: 248600, city of Kaluga, ul. Lenina, d. 101, Aleksey 
Borisovich Streltsov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Borovsk </H5>

<H5>  Resurrection ["Vozrozhdeniye"], Borovsk Noosphere Center </H5>
  It struggles for a resurrection of the city's ecological and 
cultural milieu. It organizes debates on ecological and 
philosophical topics. 
  Address: 249010, Kaluga Oblast, city of Borovsk-3, pos. 
Institut, d. 3, kv 48, Yuriy B. Minayev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Obninsk </H5>

<H5>  Protva [River], Noosphere Committee </H5>
  The committee monitors environmental protection, the quality 
of food products and consumer goods, and public health. It 
organizes ecological education, studies public opinion, and 
collects and disseminates ecological information. It 
participates in solving problems of protecting the plant and 
animal worlds and preserving biological diversity. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 249020, Kaluga Oblast, city of Obninsk, ul. 
Gurvinova, d. 23, kv. 68, tel. 3-38-34, Nikolay Sergeyevich 
Studenov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Settlement of Sosenki (Kozelskiy Rayon) </H5>

<H5>  UNEKO Detachment ["Otryad UNEKO"] </H5>
  This is a children's organization that engages in ecological 
education. 
  Address: 249711, Kaluga Oblast, Kozelskiy rayon, pos. 
Sosenki, ul. Mashinostroiteley, d. 3., kv. 2, Irina V. 
Gorchakova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Kamchatskaya Oblast </H5>

<H5>  City of Petropavlovsk-Kamchatskiy </H5>
<H5>  Alternative ["Alternativa"], Group </H5>
  It was formed in 1988. Goal: promote decontamination of 
Avachinskiy Gulf. Forms of work: organization of photo exhibits, 
announcements on radio and television. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 683050, Kamchatka Oblast, city of 
Petropavlovsk-Kamchatskiy, ul. Tsentralnaya, d. 20, kv. 30, 
Natalya G. Dyakonova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Association of Kamchatka ["Assotsiatsiya zelenykh </H5>

Kamchatki"] 
  It was founded in March 1990 and registered on 1 July. 
  Its task is to maintain the ecological health of Kamchatka. 
The association organizes tourist hikes, develops waste-free 
technologies, and collaborates with international organizations. 
It opposes destructive methods of mining gold. 
  In September 1990 the association picketed the construction 
of a road in the Paratunka resort zone. The construction was 
canceled. 
  On 7-13 June 1991 they organized the visit of a Greenpeace 
delegation to Kamchatka. The Greenpeace ship Rainbow Warrior 
tried to penetrate into Avachinskiy Bay where the largest naval 
base in the Far East is located in order to monitor 
radioactivity. Radioactive waste burial grounds are located in 
the bay. 
  ASK activists appear regularly in the press. More than 100 
articles have been published on the problem of unfavorable 
consequences of gold mining alone. 
  The association organizes ecological education, including 
the 
use of radio and television. 
  Membership without counting collective members is more than 
100. The coordinating council has nine members. There are two 
deputies to the oblast soviet. 
  Address: 683024, Kamchatka Oblast, city of 
Petropavlovsk-Kamchatskiy, ul. Gorkogo, d. 15, kv. 44, tel. 
3-13-52, Sergey Solovyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Center (Ecocenter, Eco-Center, EC) ["Ekologicheskiy </H5>

tsentr (Ekotsentr, Eko-Tsentr, ETs)"] 
  It was registered at the obkom of the All-Union Komsomol. It 
works on solving the ecological problems of the city and oblast. 
It has taken in several subgroups. 
  The center's work is directed by a bureau. It puts out the 
information bulletin EKOKURYER [Ecocourier] (since the spring of 
1989, with a press run of several thousand). It has published 
articles on topics related to environmental protection. 
  The center is a participant in the Greens Movement (see 
article). 
  Address: 683009, Kamchatka Oblast, city of 
Petropavlovsk-Kamchatskiy, ul. Kurchatova, d.41, kv. 37, 
Stanislav Georgiyevich Safronov, member of the Ecocenter bureau. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 209. 

<H5>    Karelia </H5>
<H5>  City of Petrozavodsk </H5>
<H3>  Association of Ecology Public Organizations of Karelia 
["Assotsiatsiya ekologicheskikh obshchestvennykh organizatsiy 
Karelii"] </H3>

  It was formed on 23 April 1989 at an assembly of ecology 
groups from seven cities and rayons. Its work takes the form of 
conducting assemblies (about once a year). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galkina, L., op. cit., p 10. 

<H5>    "Panayarvi," Creative Noosphere Club </H5>
  It advertises no-waste technologies and takes actions to 
support the creation of a Soviet-Finnish national park. 
  It is a member of the Social-Ecological Alliance (see 
article) 
  Address: 185034, Republic of Karelia, city of Petrozavodsk, 
ul. Gvardeyskaya, d. 15, kv. 8, tel. 6-67-24, Ninel T. 
Khakkaraynen. 

<H6>    Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Nature ["Priroda"], Association </H5>

  It was founded in the summer of 1988. 
  The association monitors compliance with nature protection 
laws, the quality of food products and consumer goods and public 
health, does expert ecological studies of economic plans and 
administrative decisions, develops alternative plans and 
technologies, collects ecological information, engages in 
ecological education,and participates in solving problems of 
preservation of forests and protection of the plant and animal 
worlds, as well as problems linked to the use of nuclear energy 
and the construction and operation of AES's and GES's. 
  It took actions against construction of the Karelian AES, 
the 
GES in Panayarvi, a branch of the Skorokhod Footwear Factory 
(the site was taken out of a nature protection zone), and deep 
dispersion of waste water from the Segezha Pulp and Paper 
Combine (together with the Segezha and Loukhi groups), supported 
establishment of the Vudlozerskiy National Park (Pudozhskiy 
Rayon), and stopped logging in the Kish preserve. They were able 
to get the presidium of the Supreme Soviet of the Karelian ASSR 
to decide to stop construction of the Karelian AEC, but 
construction was continued all the same. Until mid-April 1989, 
meetings of the initiative group of the Karelian People's Front 
were held weekly in their quarters. Together with the initiative 
group, the association organized debates on ecological issues. 
In August-December 1989, the Supreme Soviet of the Karelian ASSR 
planned financing for the group's planning projects, but no 
money was appropriated. The association was not successful in 
the elections. 
  In January 1990 the society participated in the antinuclear 
rally against construction of AES's and nuclear weapons testing 
on Novaya Zemlya (about 1,000 participants). On 26 April 1990 
the association took part in a rally where money was collected 
dedicated to the anniversary of the Chernobyl accident. 
  They had a page, called the "Green Page," in the newspaper 
KOMSOMOLETS. 
  Member of the Greens Movement (see article). 
  Addresses: 185000, Republic of Karelia, city of 
Petrozavodsk, 
ul. G. Titova, d. 3, editorial office of the newspaper 
KOMSOMOLETS, tel. 7-23-76, 7-05-70, Vladimir Vinokurov; 185031, 
Republic of Karelia, city of Petrozavodsk, ul. Moskovskaya, d. 
9, kv. 12, tel. 4-41-21, Aleksey Mikhaylovich Kharlamov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galkina, L., op. cit., p 9; 
  -  "Rossiya: partii...," op. cit., vol 1, part 1, pp 136-137. 

<H3>    Free Student Green League ["Svobodnaya studencheskaya 
zelenaya liga"] </H3>
  It was formed at Petrozavodsk State University in the fall 
of 
1989 by voluntary signature of the SSZL Manifesto. Since October 
1989 they have put out the samizdat journal ZELENYY KVADRAT, 
where the green philosophy is developed and they defend the 
principles of non-violence. In December 1989 they held a march 
against AES's and for a non-nuclear zone. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galkina, L., op. cit., p 10. 

<H5>    City of Kondopoga </H5>
<H5>  Scandal, Greens Alliance ["'Skandal,' Soyuz zelenykh"] </H5>
  This is a group with an alternative orientation. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Kostomushka </H5>
<H3>  Ecology Section of the Democratic Initiative 
["Democraticheskaya initsiativa"] Movement </H3>
  The movement was formed on 30 October 1987. It has an aktiv 
of about 20 persons with an average age of 30-35. By social 
composition they are workers, engineering-technical personnel, 
and office workers. It is a collective member of the Karelian 
People's Front. 
  In the spring of 1988 they organized collection of 
signatures 
against construction of the AES (800 signatures). On 22 April 
1990 they held a city referendum (7,000 of the 7,300 who 
participated in the referendum opposed the construction). They 
formed a public commission to monitor construction. 
  In October 1989 they held a forest ecology seminar together 
with representatives of public organizations from Finnish border 
cities (about 50 participants). 
  On 25 March 1990 they conducted a seminar on the development 
of atomic energy (100 participants, among them a professor from 
Helsinki). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part. 2, p 166. 

<H5>    City of Medvezhyegorsk </H5>
<H5>  Nature ["Priroda"], Initiative Group </H5>
  It is an affiliate of the Petrozavodsk group. The group we 
formed in the summer of 1988. It has an aktiv of 10 persons. In 
1988-1989 they waged a successful campaign against construction 
of a yeast plant. They are fighting against construction of a 
construction combine that is supposed to support the AES. 
  Address: 186300, Republic of Karelia, city of 
Medvezhyegorsk, 
ul. Gorkogo, d. 5-6, kv. 22, tel. 2-10-35, 2-19-80, Yuliya I. 
Shabanova. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galkina, L., op. cit., p 9. 

<H5>    City of Nadvoitsy </H5>
<H3>  Ecology Group of the City of Nadvoitsy ["Ekologicheskaya 
gruppa g. Nadvoitsy"] </H3>
  It was formed in the fall of 1988 on the wave of struggle 
against an aluminum plant. The plant was poisoning the 
population with fluoride compounds, causing the bone disease 
fluorosis. They gathered signatures. In April 1989 they waged a 
campaign of refusal to pay for water. The deputies rejected a 
decision to declare Nadvoitsy an ecological disaster zone. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galkina, L., op. cit., p 9. 

<H5>    City of Pudozh </H5>
<H5>  Forest ["Les"], Social-Ecological Group </H5>
  The group participates in solving problems of protecting the 
plant and animal worlds and preserving biological diversity, 
especially preserving the forests. 
  Address: 186150, Republic of Karelia, city of Pudozh, ul. 
Stroiteley, d. 13, kv. 59, Leonid A. Peregud. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2 

<H5>    Kemerovo Oblast </H5>

<H5>  City of Kemerovo </H5>
<H3>  Committee To Save the Tom River ["Komitet spaseniya reki 
Tomi"] </H3>
  The committee studies the impact of industrial and 
agricultural pollution of the Tom River on human health and the 
disappearance of certain species of fish and plants. 
  Address: 650053, city of Kemerovo, ul. Kuzbasskaya, d. 28a, 
S. P. Grosheva. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Noosphere ["Noosfera"], Ecology Club </H5>

  It was formed in April 1988. The club is registered at the 
gorispolkom. It sets its task as solving the ecological problems 
of the Kuznets Basin. The club conducts rallies, volunteer work 
days, and ecological investigations and carries on ecological 
propaganda. 
  The club has meetings once a week in the premises of the 
city 
All-Union Komsomol committee. In 1989 the aktiv was 15 persons; 
10-25 persons participate in the meetings. Initially students 
came to the club, but since 1989 the meetings are attended 
chiefly by specialists: biologists, medical personnel, 
engineers, and lawyers. The average age is 30-35 years. 
  The club's first action was to hold a May Day meeting in 
Kemerovo on 15 May 1988 (3,000-4,000 persons). They discussed 
questions of building the Krapivinskoye Reservoir, the 
destruction of forests in Kemerovo Oblast, and preserving the 
wooded park in the center of the city. On 14 October 1988, 
together with ecologists from Novokuznetsk and Tomsk they held a 
march to the site where the Krapivinskoye Reservoir is being 
built (700 persons). In February 1989 they took part in a round 
table discussion of the Krapivinskoye Reservoir at the 
oblispolkom. On 21 May 1989 the second May Day meeting was held 
(5,000 participants), and at it there were calls to picket the 
construction of the hydroengineering complex. On 1 June 1989, 
20-25 people visited the construction site and made appeals to 
the construction workers. 
  With club support Yu. Kozmin was elected RSFSR people's 
deputy in 1990. 
  The club is a member of the Social-Ecological Alliance (see 
article). 
  Address: 650065, city of Kemerovo, pr. Komsomolskiy, d. 53, 
kv. 385, tel. 52-13-00, Yuriy A. Kuvshinov; tel. 23-07-46, 
Galina Nikolayevna Alyabyeva. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 164. 

<H5>    City of Leninsk-Kuznetskiy </H5>
<H5>  Ecology Group ["Ekologicheskaya gruppa"] </H5>
  It is a member of the Social-Ecological Alliance (see 
article). 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    City of Novokuznetsk </H5>
<H5>  Ecology (Ecologist) ["Ekologiya" ("Ekolog")], Club </H5>
  The club was formed in late 1987, an offshoot of the Vremya 
["Time"] patriotic antialcohol club. The organizers were T. 
Golubeva and V. Pushkarev. One of the later leaders was Yu. 
Nikitin, docent at the Siberian Metallurgical Institute. In 
April 1988 the Vremya, Laboratory (a Marxist sociopolitical 
club), and Ecology groups held a rally in support of restoring 
monuments of architecture and nature (about 500 participants). 
  In 1988-1992 they organized rallies against expansion of the 
metallurgical plant. For example, about 500-1,000 people 
participated in the ecology rally next to the plant 
administration on 5 June 1988. 
  The club has been involved in political activity since 1988. 
They took part in organizing the "Hyde Park" on Theater Square 
in the summer of 1988. In 1991 they joined the Russian Greens 
Party (see article). 
  Address: 654035, Kemerovo Oblast, city of Novokuznetsk, ul. 
Tsiolkovskogo, d. 9, korp. 8, kv. 4, tel. 44-45-30, Tatyana I. 
Golubeva. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. cit. vol 1, pt 2, p 201. 

<H5>    City of Prokopyevsk </H5>
<H5>  Ecologist ["Ekolog"], Association </H5>
  The association engages in ecological education. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Yurga </H5>
<H5>  Yurga Branch of the Noosphere ["Noosfera"] Club </H5>
  The branch organizes debates on ecology. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 652000, Kemerovo Oblast, city of Yurga, ul. Mira, 
d. 
3a, kv. 10, Nikolay A. Petrovskiy. 

<H5>    Komi </H5>
<H5>  City of Syktyvkar </H5>
<H5>  Syktyvkar Social-Ecological Alliance (SES) </H5>
  The alliance monitors environmental preservation, the 
quality 
of food products and consumer goods, and public health. It 
organizes ecological education, the study of public opinion, and 
the collection and distribution of ecological information. It 
participates in solving problems of preservation of the forests. 
  Address: 167007, Komi, city of Syktyvkar, ul. K. Marksa, d. 
212, kv. 22, tel. 2-50-12, 7-29-64, Valentina M. Shvetsova (or 
Shevtsova). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Vorkuta </H5>

<H5>  Novaya Zemlya-Nevada, Committee </H5>
  The committee struggles against nuclear testing on Novaya 
Zemlya. It emerged from the Memorial organization. 
  Address: 169900, Komi, city of Vorkuta, ul. Dimitrova, d. 
15/5, kv. 59, tel. 3-50-15, 3-51-65, Vitaliy A. Troshin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Pechora </H5>

<H5>  Committee To Save the Pechora ["Komitet spaseniya Pechory"] </H5>
  It puts out the newspaper EKOLOGICHESKIY VESTNIK. The editor 
is V. T. Semyashkina and circulation is 2,000. 
  Address: 169700, Komi, city of Pechora, Glavpochtamt, a/ya 
114. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Ukhta </H5>

<H5>  Committee To Save the Pechora ["Komitet spaseniya Pechory"] </H5>
  This is an association of specialists and activists of the 
ecology movement. It carries out expert studies of the state of 
the rivers of the Pechora basin and fights against their 
pollution. It disseminates information on environmental 
pollution in the region. 
  In March 1991 the committee conducted a scientific-practical 
conference devoted to the condition of the waters of the Pechora 
basin. 
  In May 1991 the committee participated in the founding 
conference of the Russian Greens Party (see article). 
  Address: 169400, Komi, city of Ukhta, ul. Oplesnina, d. 2, 
kv. 61, Aleksey Iosifovich Terentyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Kostroma Oblast </H5>

<H5>  City of Kostroma </H5>
<H3>  Public Council To Save the Volga ["Obshchestvennyy sovet po 
spaseniyu Volgi"] </H3>
  Until May 1990 the council gathered signatures against 
construction of an AES which would cause irreversible harm to 
the Volga River. It is the conviction of members of the council 
that there must be an ecological expert study and a search for 
an alternative to the departmental project. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "I Am Against It!" ZELENYY MIR, No 
2, 1990, p 3. 

<H3>    Ecology Branch of the Sociopolitical Initiatives Club ["Klub 
Obshchestvenno-politicheskiye initiativy"] </H3>
  It is a member of the Greens Movement (see article). 
  Address: 156000, city of Kostroma, ul. Shagova, d. 106, kv. 
17, tel. 7-41-07, Aleksandr Romanovich Verin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Krasnodar Kray </H5>

<H5>  City of Krasnodar </H5>
<H3>  Ecological Power Engineering Section ["Sektsiya 
ekologicheskoy energetiki"] </H3>
  The section works on development of alternative sources of 
energy and "clean" technologies. 
  Address: 350000, city of Krasnodar, ul. Zakharova, d. 41, 
kv. 
24, tel. 52-97-46, Gennadiy I. Molokanov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Grass ["Trava"], Club </H5>

  The club appeared in the mid-1980s as a pedagogical society. 
Its leaders are A. Rodomakha and A. Serebryakov. They worked on 
education, including ecology. 
  In 1987 they organized a public protest campaign against 
plans to build the Krasnodar AES. During the campaign signatures 
were collected. The organizers of the campaign were persecuted 
by the authorities. Nonetheless, the plans to build the AES were 
rejected at this time. 
  The group belonged to the Federation of Socialist Public 
Clubs and many of its members joined the Confederation of 
Anarcho-Syndicalists. 
  In 1989-1991 part of the group made an effort to establish 
an 
ecological settlement in Sakhray. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H5>    Torch of Rerikh ["Fakel Rerikha"] </H5>
  Cultural-creative association. Goal: to promote greater 
humanity in interpersonal relations. Forms of work: organization 
of ecology actions and charitable events and propagating the 
creative work of N. Rerikh. 
  It publishes the journal SVETOCH [Light]. Collective members 
of the association are Light (30 persons), Lotus (20 persons), 
Logos, Dialog, and Harmony in the city of Novorossiysk (see 
article). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, pp 167-168. 

<H5>    Settlement of Guzeripl (Maykopskiy Rayon) </H5>
<H5>  Guzeripl Branch of the SES </H5>
  It participates in solving problems of agricultural 
pollution. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 352797, Krasnodar Kray, Maykopskiy r-n, pos. 
Guzeripl, Zapovednik, Zinaida G. Vakharlovskaya. 

<H6>    Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Maykop </H5>

<H5>  Citizen, Volunteer Club ["Grazhdanin, samodeyatelnyy klub"] </H5>
  Its task is to solve ecological problems of the North 
Caucasus. It appeared in 1988. One of its leaders, A. 
Serebryakov, was the initiator of the campaign against 
construction of the Krasnodar AES (they were successful in 
stopping construction). 
  The club monitors the state of the environment, the quality 
of food products and consumer goods, and public health. It 
organizes ecological education, the study of public opinion, and 
the collection and dissemination of ecological information. It 
engages in sociopolitical activity (participation in elections 
and so on). It participates in solving the problems of 
protecting the plant and animal worlds, preserving biological 
diversity, and developing a system of specially protected 
natural areas and sites, in particular preservation of forests, 
as well as problems linked to the construction and operation of 
hydroengineering structures. 
  It is a member of the Social-Ecological Alliance (see 
Article). 
  Address: 352700, Krasnodar Kray, city of Maykop, ul. 
Pionerskaya, d. 416, kv. 5, tel. 2-11-83, Vladimir I. Karatayev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Novorossiysk </H5>

<H5>  Harmony ["Garmoniya"] </H5>
  This cultural-philosophical society was formed in February 
1987. It organizes seminars on philosophy and ethics as well as 
ecology volunteer work days and peace actions. It has about 100 
members and an aktiv of 20. It is a collective member of the 
Torch of Rerikh Association in the city of Krasnodar (see 
article). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, pp 167-168. 

<H5>    City of Tuapse </H5>
<H3>  Public Committee for Ecological Monitoring and Assistance 
["Obshchestvennyy komitet ekologicheskogo kontrolya i 
sodeystviya"] </H3>
  It was founded on 12 July 1988 and is registered. 
  Goals: formation of a permanently operating ecological 
monitoring system and solution of cultural and ethnic problems 
(in particular, Adygey issues). 
  The committee organizes rallies, engages in publishing, 
participates in planning withdrawal of land for summer homes, 
identifies violations in the application of toxic chemicals and 
in forest uses, is organizing the Safari Park, makes surprise 
inspections to clean up the beach, and so on. 
  "The nucleus of the future committee formed before 
celebration of the official anniversary, the 150th anniversary 
of the city of Tuapse, in May 1988. A letter (19 signatures) was 
sent to the Party Control Commission of the CPSU Central 
Committee in which they expressed their protest against dating 
the founding of the city 'from the beginning of the destruction 
of the Adygey people.' On 4 June 1988 at a round table at the 
CPSU gorkom a promise was made not to hold the anniversary, but 
rather just a 'city celebration,' but the promise was not kept. 
(In Sochi, founded in the same year of 1838, subunits of 
internal troops were posted in Adygey villages to prevent 
possible incidents)." 
  On 12 July 1988 (after changing the time twice) an ecology 
rally was held in Tuapse on the embankment by the monument to 
the destroyer Kerch (500 participants, including members of the 
Pilgrim Communard Club, the Acacia Garden Society, and 
participants in the Neburg school ecology expedition). Although 
representatives of official bodies interfered in the conduct of 
the rally, the participants adopted an independent resolution by 
a majority of votes. This resolution contained a point on lack 
of confidence in the six leaders of the city (including A. 
Grabovets, first secretary of the CPSU gorkom and interrayon 
procurator). The point was included in a draft resolution by a 
majority of votes of the members of the rally organizing 
committee. The resolution also contained a point on setting up a 
public committee for ecological monitoring. A list of committee 
members was submitted by the rally organizing committee. 
  During the election campaign in the spring of 1989, 
committee 
members distributed Academician A. D. Sakharov's "Decree of 
Power" and the co-report of the interregional deputy group. 
There was friction with the local leadership because they 
supported the candidacy of A. O. Karaulov for USSR people's 
deputy (he was victorious in the election). 
  The committee proposed Aleksandrov, director of a plant, as 
candidate for mayor of Tuapse (as of 25 January 1992 he still 
had not been appointed). 
  In April 1989 they conducted a volunteer work day to clean 
up 
the channel of the Pauk River (about 300 people helped, 
including the deputy chairman of the gorispolkom). 
  In June 1989 the ecology plans of the public committee were 
reviewed by the public nature protection council. The ispolkom 
of the city soviet and the CPSU gorkom rejected the plans. 
  They put together exhibitions on the "Window of Ecological 
Information" board. The Pilgrim Club, which belongs to the 
public committee, organized a communard labor camp, called 
Piligrimsk-8, in the summer of 1989. 
  Since early 1990 the committee has focused its activities 
entirely on the plan for Safari Park (the plan involves 
allocating a segment of the city woods for a park where animals 
would live in a semifree setting; the park would be open for the 
public to visit). After 2 years of work the committee was able 
to get land released for a park. The Moscow Institute of 
Structures for Culture, Recreation, and Public Health had 
developed and approved an official plan, the creation of Safari 
Park was announced, a logo was made, the directors of the 
botanical (V. Chernova) and financial (S. Smolyev) parts of the 
plan were appointed, and an account was opened in the bank. 
  In 1989 the committee aktiv (cochairmen) was 23-24 persons, 
and up to 50 took part in activities: members of the Pilgrim 
Club (commissar G. Chernovol), tourists, mountain climbers, and 
hunters. Their average age is 40, and office workers 
predominate. They have by-laws which envisioned an auditing 
structure, individual membership, membership cards and dues, a 
press, an emblem, and so on. 
  The committee is directed by eight cochairmen elected in 
1989: V. I. Yefimenko. V. P. and G. I. Chernovol, Yu. A. 
Garenkov (deputy to the gorsoviet), Ye. A. Gayenkova (sponsors 
ecological education of school children), S. N. Smolyev (an 
associate at the Nika NPKhO [expansion unknown] and commercial 
director of Safari Park), N. A. Tesheva, and B. P. Zaremba. 
  Their source of financing is dues. 
  The committee is a member of the Social-Ecological Alliance 
(see article). It collaborates with other organizations that 
belong to the SoES, with nongovernmental organizations of 
Krasnodar and Sochi, including ecology groups, and also with the 
Committee for Constitutional Supervision of Krasnodar Kray. 
  Address: 352800, Krasnodar Kray, city of Tuapse, ul. 
Mayakovskogo, d. 9, kv. 11, tel. 2-88-07, Vladimir Pavlovich 
Chernoval; tel. 2-88-07, Vladimir Pavlovich and Galina Petrovna 
Chernovol; tel. 5-28-65, Yevgeniya Alekseyevna Gayenkova. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 220. 

<H5>    Ekos, Cooperative </H5>
  This is a youth environmental defense club. It worked under 
the direction of the local Komsomol. 
  Address: Krasnodar Kray, city of Tuapse, tel. 2-32-19, Yuriy 
M. Ustinov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Krasnoyarsk Kray </H5>

<H5>  City of Krasnoyarsk </H5>
<H5>  Green World ["Zelenyy mir"], Ecology Movement </H5>
  The organization monitors environmental preservation, the 
quality of food products and consumer goods, and public health, 
develops alternative plans, designs, and technologies, engages 
in ecological education, studies public opinion, and collects 
and disseminates ecological information. It participates in 
solving problems of protecting the plant and animal worlds, 
preserving biological diversity, and developing a system of 
specially protected natural areas and sites and problems linked 
to the construction and operation of hydroengineering structures. 
  On 26 April 1990 the movement organized a sanctioned rally 
devoted to the anniversary of the Chernobyl accident (about 300 
participants) and discussed the question of the ecological 
well-being of the city. 
  It puts out a newspaper, EKOLOGICHESKIY VESTNIK, and is a 
member of the Social-Ecological Alliance (see article). The 
leaders belong to the Greens Party of Krasnoyarsk Kray. 
  Address: 663001, city of Krasnoyarsk, p. Berezovka, r/ts. 
ul. 
Michurina, d. 8, kv. 10, Vladimir I. Mikheyev. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. cit., vol 1, part 2, p 168. 

<H5>    Green World--Resurrection ["Zelenyy mir--vosrozhdeniye"] </H5>
  This is an ecology group that appeared as the result of 
conflict with the leaders of Green World (see article). The 
leader is S. Panov. They adhere to ethnocratic positions and 
consider it essential that the status of the Russian-speaking 
population be fixed in the Constitution as the "primary ethnic 
factor" of Russia. The group is oriented to alliance with the 
Orthodox Church and participated actively in organizing the mass 
baptism of local inhabitants. They plan, together with the 
Church, to move inhabitants of the Chernobyl zone to Krasnoyarsk 
Kray. 
  In January 1992 S. Panov declared himself cochairman of the 
Russian Greens Party (see article) for Siberia and tried to 
create a "patriotic" faction in the RPZ. But his membership in 
the RPZ was rejected by the party. In February 1992 ZM-V put out 
a newspaper GREEN PEACE in the name of the RPZ, which also 
elicited protest from the international organization of the same 
name (see article). 
  At a conference of ecology groups in St. Petersburg on 28-29 
February 1992, S. Panov acknowledged that he has no relationship 
with either RPZ or Greenpeace and gave a public apology for his 
actions. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H5>    SES Branch in Krasnoyarsk </H5>
  They participate in solving the problem of forest 
preservation. The branch is a member of the Social-Ecological 
Alliance (see article). 
  Address: 660079, city of Krasnoyarsk, ul. 60-let Oktyabrya, 
d. 102, kv. 87, Tatyana Fedorovna Baskanova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Kansk </H5>

<H3>  Ecology Club of the City of Kansk ["Ekologicheskiy klub g. 
Kanska"] </H3>
  It is fighting against industrial pollution of the 
environment. 
  Address: 663606, Krasnoyarsk Kray, city of Kansk, pos. 
Remzavod, d. 4, kv. 17, Viktoriya V. Krylova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Village of Kezhma </H5>

<H5>  Committee To Save the Angara ["Komitet spaseniya Angary"] </H5>
  It is fighting against pollution of the Angara River, in 
particular against GES's. 
  Address: 663470, Krasnoyarsk Kray, c. Kezhma, ul. 60-letiya 
VLKSM, d. 10, kv. 7, Sergey Aleksandrovich Shirobokov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Norilsk </H5>

<H5>  Taymyr Greens Front ["Taymyrskiy zelenyy front"] </H5>
  It originated in 1989 from the Council of the People's 
Front. 
They conducted demonstrations against environmental pollution by 
the Norilsk Mining and Metallurgical Combine. The leader of the 
TZF, V. Rapota, participates in the Confederation of 
Anarcho-Syndicalists and the Humanist Party; he is also 
cochairman of the Russian Greens Party (see article). In 
February-March 1992 he conducted a hunger strike against 
departmental policies in Taymyr. 
  The TZF studies the state of the environment in the region. 
  It belongs to the Humanist Party which was established in 
July 1990 in St. Petersburg. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 663302, Krasnoyarsk Kray, city of Norilsk, a/ya 
1332; Krasnoyarsk Kray, city of Norilsk, ul. Dzerzhinskogo, d. 
3, kv. 165, tel 2-59-63, Viktor V. Rapota. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, p 91. 

<H5>    Ecology and Man ["Ekologiya i chelovek"] </H5>
  The organization was formed in 1990. It conducts ecological 
expert studies of economic projects and administrative 
decisions. It organizes ecological education, studies public 
opinion, and gathers and disseminates ecological information. 
  Address: 663301, Krasnoyarsk Kray, city of Norilsk, pr. 
Lenina, d. 30, kv. 16, Nadezhda Viktorovna Kryukova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Sayanogorsk </H5>

<H5>  Green World ["Zelenyy mir"] </H5>
  It organizes ecological education and takes action against 
industrial pollution of the environment. 
  Address: 662793, Krasnoyarsk Kray, city of Sayanogorsk, 7-y 
mkrn., d. 16, kv. 33, tel. 74-3-79, Viktor V. Lebedev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Village of Sukhobuzima </H5>

<H5>  Ecology ["Ekologiya"], Initiative Group </H5>
  Its task is to observe radioactive discharges in the region. 
  Address: 663040, Krasnoyarsk Kray, s. Sukhobuzima, ul. 
Selezneva, d. 51, kv. 1, Yuriy V. Pirogov. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    Kursk Oblast </H5>
<H5>  City of Kursk </H5>
<H5>  Nature Protection Society ["Obshchestvo okhrany prirody"] </H5>
  In addition to defending the environment, it also engages in 
politics. 
  Address: city of Kursk, ul. Lenina, d. 19, kv. 19, Aleksandr 
Parchikov, deputy chairman. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Spring ["Rodnik"], Sociopolitical Club </H5>

  It works on ecological, cultural, and political problems. It 
was founded in November 1986. 
  In October 1988 the club adopted the Declaration of the 
Moscow Civil Dignity group (which disbanded itself when it 
joined the Constitutional Democrats Party) as their program 
document. Club representatives took part in the Constituent 
Congress of the Kursk People's Front in December 1989. Spring 
collaborates with the Alternative group (city of Gus 
Khrustalnyy, Vladimir Oblast) and participates in the Greens 
Movement (see article). 
  The aktiv is 10 persons. 
  Addresses: 305047, city of Kursk, ul. Zavodskaya, d. 49, kv. 
1, tel. 5-55-70, Ivan Konstantinovich Korshunov; 305000, ul. 
Radishcheva, 35, Dom znaniy, S. N. Shumyakov, Valeriy Fedorovich 
Rozhnov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Kurchatov </H5>

<H3>  Public Committee To Protect the Seym River ["Obshchestvennyy 
komitet okhrany reki Seym"] (OKORS) </H3>
  It studies the effects of environmental pollution, in 
particular pollution of the Seym River, on human health as well 
as on plants and animals. It works on the problems of nuclear 
contamination. 
  Address: 307239, Kursk Oblast, city of Kurchatov, ul. 
Energetikov, d. 35, kv. 54, Valeriy I. Sevryukov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Zheleznogorsk </H5>

<H5>  Nature and Society ["Priroda i obshchestvo"] </H5>
  It conducts debates on philosophical and ecological topics. 
  Address: 307130, Kursk Oblast, city of Zheleznogorsk, ul. 
Lenina, d. 436, kv. 69, tel. 3-30-70, Anatoliy A. Yakimenko. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    City of Khomutovka </H5>
<H5>  Nature and Society ["Priroda i obshchestvo"] </H5>
  This is a social-ecological organization. Its 
representatives 
participated in the Constituent Congress of the Kursk People's 
Front in December 1989. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Leningrad Oblast </H5>

<H5>  City of St. Petersburg </H5>
<H5>  Arctic Movement ["Arkticheskoye dvizheniye"] </H5>
  It studies ecological problems of the Far North in the 
country's territory. It was formed in the late 1980s. 
  Address: 193231, city of St. Petersburg, Tovarishcheskiy 
pr., 
d. 28, kv. 107, Vera A. Yankina, tel. 584-00-13, 352-22-31. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Bureau of Ecological Developments ["Byuro ekologicheskikh </H5>

razrabotok"] (BER) 
  It was organized in mid-1986. It has an aktiv of 4-10 
persons; about 200 persons (mainly specialists) collaborate with 
the BER. It operates on a cost accounting basis. 
  The bureau works in close contact with nature protection 
organizations and official organs. It performs ecological expert 
studies of economic plans and administrative decisions, develops 
alternative designs and technologies, and familiarizes the 
population with ecology law. 
  About 50 local ecological crises have been surmounted with 
the bureau's help. They were able to achieve stoppage of 
construction of the oil tanker terminal near Vyborg, formation 
of a cooperative to process TVTs [expansion unknown], a 
reordering of land use in the oblast, the rescue of parks within 
the city limits, and other things. 
  In 1986 BER participants published about 70 articles on 
ecology in the Leningrad press. In January 1988 the first issue 
of the collection of BER articles entitled "Zazerkalye" [Behind 
the Mirror] was published, 30 pages, and publication was halted. 
  On 8 August 1989 the bureau together with representatives of 
the city Red Cross committee, the city Charity Society, the 
Dezaurus and Femina groups, and USSR People's Deputy D. Granin 
participated in a trip to the city of Sosnovyy Bor, organized by 
the Christian Democratic Union of Leningrad. Their purpose was 
to study the population's living conditions. During the trip it 
was confirmed that there had been two accidents at the Leningrad 
AES and NITI [expansion unknown] in which there were human lives 
lost. From medical personnel they obtained information on a 
sharp increase in the number of congenital anomalies among the 
local population. Participants in the trip demanded the 
formation of a government commission to study living conditions 
in Sosnovyy Bor. The action was covered by Leningrad television 
and the press. 
  In May 1990 the bureau waged a cutting polemic with the 
Leningrad (St. Petersburg) Greens Party (see article); it arose 
mainly from personal factors. 
  In the fall of 1991 the BER was a key structure in 
organizing 
the Green Train, which collected information for the Brazil-92 
conference. 
  The bureau has existed at the Leningrad (St. Petersburg) 
Center for Creative Initiative since 1986; it is a member of the 
Social-Ecological Alliance (see article) and the Greens Movement 
(see article). 
  The director of the BER is Yu. S. Shevchuk, a participant in 
the nature protection movement since 1978 and author of an idea 
of geopathogenic zones according to which a number of cultures 
are moving toward environmental destruction because of their 
corresponding mentalities. 
  Address: 196006, city of St. Petersburg, Moskovskiy pr., 
152, 
Yu. S. Shevchuk; tel. 246-25-83. 
<H6>  Sources of Information </H6>

  -  Archives of A. Shubin; 
  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. cit., vol 1, part 2, pp 173-174, 
181. 

<H5>    Blue Baltic ["Golubaya Baltika"] </H5>
  Its task is to protect the Baltic Sea, the river and lake 
system, and the airspace. It works on ecological education of 
schoolchildren, and conducted an action called "Blue Baltic." It 
was formed in the late 1980s. 
  Total number of members--30. 
  Address: 191025, city of St. Petersburg, ul. Stremyannaya, 
d. 
14, kv. 6, Tamara T. Kudryavtseva; tel. 311-34-97. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Green Hippie ["Grin-Khipp" ("Zelenyy khippi")] </H5>

  The organization was registered as a green patrol and 
conducts surprise ecology inspections. It has more than 30 
activists in St. Petersburg. It is a participant in the System 
["Sistema"] alternative cultural movement (Moscow). It belonged 
to Epicenter ["Epitsentr"] and the USSR Youth Inspection Office 
for Nature Protection. It has been in operation since the late 
1970s. Its goal is to struggle against lack of spirituality. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 1, p 76. 

<H5>    Delta ["Delta"], Ecological Association </H5>
  This is an informal organization. It was formed in 1986, or 
on 12 April 1987. 
  Program goals: prevent ecological disaster, stop further 
destruction of the human habitat, and harmonize relations in the 
society-nature system. 
  Tasks: conduct of independent ecological expert studies, 
participation in social planning for the Leningrad and Baltic 
regions, and conduct of the necessary political activities to 
"incline the leadership of the city and country to immediate 
solutions of ecological problems." 
  Methods of work: organization and conduct of debates and 
round table discussions; organization of and participation in 
rallies and regional and international ecology conferences; and 
promotion of the appearance of operation of ecology-oriented 
political organizations, and the like. 
  The group's first action was conducting debates on the 
topic: 
"Ladoga, Neva, Gulf: Problems of Ecology" (4 June 1987). 
  On 17 May 1987 a citywide rally was organized under the 
title, "The Health of the City Is in the Hands of the 
City-Dwellers" (several thousand participants). 
  On 18 May 1987 a protest rally was held against the first 
version adopted of the "Provisional Rules on Conducting Rallies 
and Marches." 
  Since 1988 Delta has been a participant and one of the 
organizers of the annual international conference called, 
"Baltic-88," "Baltic-89," and so on. 
  Members of the association struggled against the Leningrad 
dike during its construction. They believe that the dike should 
be removed because it is harmful, not necessary. 
  The group took an active part in organizing and conducting 
ecology actions in Leningrad devoted to International Earth 
Day-90 (22 April). P. V. Kozhevnikov (leader of the group from 
1987 who was subjected to attacks from enemies of the group in 
the late 1980s) was ratified as coordinator of the international 
action on the Soviet side. On 21 April 1990 they, together with 
the Leningrad Christian Democratic Union, the Russian Christian 
Ecological Alliance (see article), and the Greens Alliance (see 
article), organized a rally (about 500 participants). Ecological 
and anticommunist slogans predominated at the rally. 
  At the initiative of Delta two new political organizations 
were formed: the Greens Party (October 1989, see article) and 
the Russian Christian Ecological Alliance (October 1989, see 
article). 
  Delta structures its work on the basis of its by-laws and 
program (approved on 12 April 1987). Membership is recorded. 
There is an aktiv of 20 persons. They are chiefly 
intelligentsia. The coordinating organ is called the provisional 
bureau. 
  Group member Pomogayev was elected a deputy to the Leningrad 
Soviet in 1990. 
  Delta is a collective member of the Ecology and Peace (see 
article) and Social-Ecological Alliance (see article) 
organizations; since 1987 it has been a member of the Leningrad 
Center for Creative Initiative. 
  Address: 194295, city of St. Petersburg, pr. Khudozhnikov, 
d. 
9, k. 2, kv. 285, Kozhevnikov, Petr Valeryevich; tel. 511-38-96, 
fax 113-58-06. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "The Leningrad Dike: 
Situation, Positions, Ambitions," ZELENYY MIR, No 14, 1991, p 5; 
  -  "Rossiya: partii...," op. cit., vol 1, part 1, p 130; vol 1, 
part 2, p 173. 

<H3>    Initiative Ecology Group ["Initsiativnaya ekologicheskaya 
gruppa"] </H3>
  It protests against local industrial enterprises. It was 
formed in the late 1980s. 
  Address: 194352, city of St. Petersburg, ul. Pridorozhnaya 
alleya, d. 9. k. 1, kv. 130, A. O. Sukhanov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Green Alliance ["Zelenyy soyuz"] </H5>

  It was formed in late 1988 (the initiative group had existed 
since the early 1980s). It organizes green patrols, mass 
marches, and ecological education. 
  The primary nucleus organized the Greens Party of Leningrad 
(see article) in March 1990. The alliance participates in 
solving problems of protecting the plant and animal worlds, 
developing a system of specially protected natural areas and 
sites, and problems related to the use of nuclear energy. 
  Address: 191186, city of St. Petersbureg, ul. Zhelyabova, d. 
8, gosoblsovet VOOP, Vladimir A. Gushchin (one of the leaders of 
the Greens Party and president of Green Hippie [see article]); 
he directs the Youth Nature Protection Inspection Office, which 
is part of the DOP Movement (see article); tel. 558-28-62, 
312-44-08. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H5>    Karelia ["Kareliya"], Travelers Club </H5>
  This is a city organization. It was formed in the late 
1980s. 
It is a member of the Social-Ecological Alliance (see article). 
  Address: 195268, city of St. Petersburg, ul. Aprelskaya, d. 
5, kv. 384, K. Yu. Gagarin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Neva, Ladoga, Onega, National Alliance (Public Committee To </H5>

Save the Neva, Ladoga, and Onega) ["'Neva, Ladoga, Onega.' 
Natsionalnyy soyuz (Obshchestvennyy komitet spaseniya 
'Neva-Ladoga-Onega')"] 
  It was formed in April 1989 as an ecology committee within 
the Volga Defense Committee (see article). Its first chairman 
was M. Lyubomudrov (member of the editorial board of NASH 
SOVREMENNIK), and since the fall of 1989 it has been Yu. 
Riverov. The committee held to an ethnocratic ("patriotic") 
orientation. In 1990 the Volga Defense Committee separated 
itself from the NLO Committee. In November 1990 the Committee 
renamed itself the Neva-Ladoga-Onega National Alliance. 
  On 20-25 February 1990 the Russian Meetings Festival was 
held 
in Leningrad (St. Petersburg) with the participation of editors 
and authors from the journals MOLODAYA GVARDIYA, MOSKVA, and 
NASH SOVREMENNIK and the newspapers LITERATURNAYA ROSSIYA and 
MOSKOVSKIY LITERATOR. 
  Address: 199034, city of St. Petersburg, 2-ya liniya 
Vasilyevskogo ostrova, d. 3, kv. 49, Yuriy V. Riverov; tel. 
213-37-22. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. cit., vol 1, part 1, p 100. 

<H5>    Monument ["Pamyatnik"] </H5>
  This is a city cultural club. It works on social problems, 
ecology, and protecting and restoring monuments. It was formed 
in March 1987 and is registered. It has by-laws and a program. 
It published the journal YEDINSTVO [Unity] (monthly since 
November 1988, 20 pages). Since mid-1990 it has been a member of 
the Council for the Ecology of Culture (see article). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. cit. 
vol 1, part 2, p 177. 

<H3>    Greens Party of St. Petersburg ["Partiya 'Zelenykh' 
Sankta-Peterburga"] </H3>
  This is a city organization. It was registered in March 1990 
by the ispolkom of the Moskovskiy Rayon Soviet of People's 
Deputies of the city of Leningrad. In January 1991 it was 
registered by the presidium of the Lensoviet. 
  In August 1990 there were about 150 persons in the party, 
and 
in August 1991 about 600. Among them were scientists, writers, 
and deputies of the Lensoviet and raysoviets. 
  The cochairmen of the party are Vladimir Aleksandrovich 
Gushchin and Ivan Blokov. 
  Party by-laws were developed and adopted, and they share the 
Declaration of the Russian Greens Party (see article). 
  Initial tasks--change the orientation of investment in the 
social development of the city, create conditions to attract 
tourists and thereby help the city, combat ecologically harmful 
production facilities, and fix up the city. To do this party 
members join into temporary groups based on interests. Later the 
groups became politicized. 
  Party members took part in conducting the Earth Day 
celebration. 
  The Greens Party strives to avert a possible disaster 
because 
toxic substances whose storage life in sea water is no more than 
50-100 years have been buried in the Baltic Sea. The bulk of the 
toxic substances were buried in 1946-1947 by the Allies in the 
anti-Nazi coalition--Great Britain, the USA, and the USSR. 
Burial of military toxic substances continued until the 1980s. 
The "critical time" is now approaching. The St. Petersburg 
Greens Party gathered this information and submitted it to the 
USSR Ministry of Foreign Affairs, the USSR Ministry of Defense, 
the president of the USSR, and the USSR KGB, suggesting that 
government structures establish precise data and make it 
available to the public. The Greens Party called the attention 
of Russian governmental organs and foreign organizations to this 
problem. 
  The Greens Party wages a struggle against illegal logging in 
the Karelian Isthmus. In April 1991 it began investigating the 
death of Nina Zuyeva, a volunteer nature protection inspector 
who was found hanged in the Priozersk City Division of Internal 
Affairs (see VOOP, Leningrad general staff of the VOOP 
inspection office). Two attempts have been made on the life of 
party cochairman V. Gushchin in connection with this case. 
  At the initiative of the Greens Party, a decision was 
adopted 
to move people out of a building on Kurlyandskaya Street where 
because of ecological factors mortality was significantly higher 
than the average for St. Petersburg. 
  In May 1991 the Leningrad Greens Party was one of the 
principal organizers of the founding conference of the Russian 
Greens Party. 
  In February 1992 the St. Petersburg Greens Party was one of 
the principal organizers of the conference of nongovernmental 
ecology organizations devoted to the conference in Brazil. 
  The party has far-reaching international ties; the closest 
ties are with the Greens Party of Finland. 
  The party includes the Eco-Rock youth groups. The party set 
up the Ekostroitel cooperative. Its program is to build and 
develop recreation centers for establishments and enterprises 
with minimal harm to the environment. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2; 
  -  Blokov, 
I., "How Many Years Until the Disaster?" SPASENIYE, No 9, 1991, 
p 5; 
  -  "City Party...Why Not?" ZELENYY MIR, No 8, 1990, p 3; 
  -  Gushchin, V., "The Greens Are Doing the Investigating," 
EKOLOGICHESKAYA GAZETA, No 4-5, 1991, p 5; "Where Will the Next 
Blow Come From?" EKOLOGICHESKAYA GAZETA, No 4-5, 1991, p 5 
(interview with I. Blokov by Yu. Khayshina). 

<H3>    Council for the Ecology of Culture ["Sovet po ekologii 
kultury"] </H3>
  This is an information and coordinating center. It expresses 
most fully the principles of the so-called ecological-cultural 
movement. 
  It was formed in late 1986. It has been registered at the 
Leningrad Branch of the Culture Foundation since March 1988. 
  Areas of work--information and coordination support for 
people working in the field of the ecology of culture. Forms of 
work--organization of meetings of representatives of groups that 
belong to the council for the purpose of coordinating their 
joint work, publishing, and the like. 
  The chief initiator in forming the SEK was the Salvation 
Group (see article). In addition to it, the Bureau of Ecological 
Developments (see article) has belonged to the council from the 
beginning, as have the Commune ["Mir"] volunteer association 
(association of non-professional historical restoration workers 
which has existed since 1986, restores structures on the islands 
of Kizhi and Valaam, and is registered with the Dzerzhinskiy 
Rayon Ispolkom in Leningrad--aktiv is 30 persons), and Club-81 
(information association of literary figures, named after the 
year of its origin). In January 1987 the SEK was registered at 
Club-81. 
  In the first, relatively peaceful period of its existence, 
the council organized several popular science seminars on 
history at the DK Iyicha. After the Angleterre events (they 
participated in the picketing to defend the Angleterre Hotel 
from demolition on 16-18 March 1987), they found themselves in 
stark opposition to city authorities, which demanded unity and 
the appropriate organizational formalities. 
  On 27 March 1987 the founding meeting was held (the local 
press responded to it); after it a program and by-laws were 
adopted which did not in fact operate. An attempt was made at 
this founding meeting to join with a number of new organizations 
such as TEII [expansion unknown], New World ["Novyy mir"] (a 
group of amateur historical restorationists, in existence since 
1987, it had separated from the Commune group and worked on the 
A. S. Pushkin Apartment Museum on the Moika and restoration of 
the Benua wing of the Russian Museum; aktiv--20 persons), Delta 
(see article), and a number of others. It soon became clear, 
however, that there were significant differences in the goals of 
the particular groups and their leaders, which led to a schism 
in April 1987. Some of the groups withdrew from the council and 
organized the council of the Epicenter Cultural-Democratic 
Movement (which collaborated with the SEK, being more 
politicized in nature). 
  On 21 March 1987 they conducted a rally in St. Isaac's 
Square 
to preserve monuments of culture; about 500-1,000 persons 
participated. 
  In mid-1990 SEK included the following ecology and 
ecological-cultural groups: the Salvation group, the Rural 
Commune volunteer association, Monument (see article), Friends 
of Ropshi, Battle of the Neva (an initiative group of historical 
restorationists formed in May 1987 which is engaged in 
restoration of the Aleksandr Nevskiy church, is registered at 
the Kolpinskiy Rayon ispolkom, and has an aktiv of 30 persons), 
Era, St. Petersburg (historical-cultural society, registered in 
1989 at the Leningrad city administration, interests include 
revitalizing sociocultural life among college students; aktiv 
2-5 persons), and the Artists Aid Society. 
  Because the program documents adopted at the founding 
meeting 
are not in effect, organizational work is structured on the 
basis of the "Statute on the SEK," which was adopted later. This 
statute was registered in the spring of 1988 by the presidium of 
the Culture Foundation. The Culture Foundation offered its 
premises for the weekly meetings of the SEK and sometimes gives 
financial help as well. 
  The council has set up: a scientific sector which conducts 
seminars; an artistic sector which organizes exhibitions and 
auctions; and a public sector which organizes people who are not 
included in stable groups. 
  Their print organ is VESTNIK SOVETA PO EK [Herald of the 
Council on the Ecology of Culture]. It has been coming out 
monthly since July 1987. The editor in chief is Mikhail Talalay, 
and members of the editorial board are S. Vasilyev, A. Kovalev, 
and V. Lurye. 
  One a month an oral presentation of VESTNIK would be held at 
the DK Ilyicha with an average of 100-150 persons participating. 
  Address: 191011, city of St. Petersburg, Nevskiy prosp., d. 
31, Fond Kultury; tel. 311-80-34; Mikhail Talalay. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Zelenyye v SSSR. 
Krupneyshiye...," op. cit., pp 18-19; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, pp 177, 179. 

<H3>    Salvation ["Spaseniye"], Group (GS, other name, Group To 
Save the Historical and Cultural Monuments of St. Petersburg 
[Leningrad] ["Gruppa spaseniya istoriko-kulturnykh pamyatnikov 
Sankt-Peterburga"]) </H3>
  It is involved in the ecology of culture. The group 
originated in 1986 during work to save the poet A. Delvig's home 
on Vladimirskaya Square from demolition. 
  There are 18 persons in the group, with higher education. 
Ages are 20-37 years. They hold various political views (some of 
them are supporters of syndicalist anarchism). Many do not 
engage in political activity at all. The group has supporters of 
active Christian enlightenment and non-believers. 
  There is no clearcut organizational structure. Goals: "To 
save historical and cultural monuments and promote change in the 
economic and political system in the direction of eliminating 
the factors that have a negative impact on the ecology of 
culture." In particular, the group "strives to change the nature 
of the ownership of buildings and the means of production in 
construction and historical restoration work." 
  Forms of work: rallies, picketing, volunteer work days, 
exhibits, expert counter-studies, and counter-plans. 
  The GS took an active part in the Angleterre events. They 
organized picketing on 16-18 March 1987 to defend the Angleterre 
Hotel from demolition. A public information post was operated 
until 1 June 1987. 
  The largest rallies (up to 1,000 persons) were devoted to 
city planning problems and preservation of old structures in 
various parts of Leningrad: Vladimirskaya Square, the Petrograd 
Side, Vasilyevskiy Island, and Rybatskoye. About 2,000 persons 
participated in the rally on Vladimirskaya Square on 19 March 
1988. On 14 June 1988 the GS together with other groups held a 
rally in Yusopov Garden in memory of the victims of Stalinism 
(about 3,000 participants). On 13 March 1988 the GS organized a 
rally against the "temporary rules for conduct of marches and 
rallies" (500 participants). 
  Results of the group's activities in 1987-1988: achieved 
cancellation of about 20 ispolkom decisions to demolish various 
buildings; promoted a several-fold reduction in the list of 
buildings to be demolished; and promoted a change in public 
opinion toward defending historical and cultural monuments and a 
change in the attitude of the city authorities toward the 
problem. Dozens of articles in the Leningrad and all-Union press 
were devoted to the group. 
  GS leader A. Kovalev was elected a deputy of the Lensoviet. 
The GS is collaborating with an analogous group, St. Petersburg. 
It is a member of the Leningrad Center for Creative Initiative 
(since August 1986) and is registered at the LTsTI [possibly 
Leningrad Center of Technical Information]. It was one of the 
founders and a constituent part of the St. Petersburg Council 
for the Ecology of Culture (see article). It is a member of the 
Greens Movement (see article). The group participated in the 
public committee to aid Armenia and collaborates with the 
Yerevan organization "Survival." 
  It is participating in publishing the Leningrad version of 
the journal OBSHCHINA [Commune]. 
  The group operates on a cost accounting basis. In 1990 the 
group's activity declined. 
  Address: 191011, city of St. Petersburg, ul. Tolmacheva, d. 
18, (k. 37), kv. 15; tel. 351-65-28, 311-25-54 (home), Aleksey 
Anatolyevich Kovalev, group leader. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Zelenyye v SSSR. 
Krupneyshiye...," op. cit., pp 18-19; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, pp 173, 179. 

<H5>    Lipetsk Oblast </H5>
<H5>  City of Lipetsk </H5>
<H3>  Greens Movement of the City of Lipetsk ["Zelenoye dvizheniye 
g. Lipetska"] </H3>
  Its activists organized the collection of signatures on a 
demand to stop construction of the giant new 2500 rolling mill; 
they held a rally and picketed the new shop. Commissions from 
the Ministry of Metallurgy, Goskomprirody, Gosplan, Gosstroy, 
and USSR Promstroybank [Industry and Construction Bank] visited 
the city. The project temporarily lost its financing; money was 
only appropriated to preserve the structures that were already 
up. But a final decision had not yet been made in February 1991. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Gorkayev, M., "Does Lipetsk Need 
the 2500 Mill?" ZELENYY MIR, No 5-6, 1991, p 7. 

<H5>    Ecology ["Ekolog"], Club (Ecological Club) </H5>
  It conducts ecological expert studies and protests against 
the new metallurgical plant, which is polluting the environment, 
in particular against construction of the 2500 complex. 
  The management organ is the club council. One of its members 
is S. Ivanov. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Addresses: 398006, city of Lipetsk, ul. Kommunisticheskaya, 
d. 21, kv. 26, tel. 74-10-74, P. V. Pushkov, 398046, ul. 
Vodopyanova, d. 11, kv. 80, Aleksandr Mikhaylovich Fedorov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Ivanov, S., "Go for Gross!" 
ZELENYY MIR, No 19-20, 1991, p 3. 

<H5>    Magadan Oblast </H5>
<H5>  City of Magadan </H5>
<H5>  Magadan ["Magadanskiy"], Ecology Club </H5>
  It organizes ecological education, the study of public 
opinion, and the collection and dissemination of ecological 
information. It participates in solving problems of protecting 
the plant and animal worlds, preserving biological diversity, 
and developing the system of specially protected natural areas 
and sites and problems related to the construction and operation 
of hydroengineering structures. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 685027, city of Magadan, ul. Luka, d. 12, kv. 21, 
tel 5-43-61, 2-61-63, Mikhail A. Kregmer. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Promotion of Perestroyka ["Sodeystviye perestroyke"], </H5>

Ecology Section 
  The SP is a public political organization which was formed 
on 
19 September 1988. It was registered on 19 October 1988. It has 
a bank account. There were 200 members in 1989. A council was 
elected (15 persons) and a program and by-laws have been 
adopted. Sections were formed, including an ecology section. 
  In 1989 they spoke out on radio and television against the 
plan to build a GES and against new mining at the coal deposits. 
They collected signatures against the visit of the 
nuclear-powered lighter carrier Sevmorput in port. They sent the 
signatures gathered (more than 6,000) to the USSR Ministry of 
the Maritime Fleet. 
  V. D. Yudin, member of the organization and engineer of a 
geological party, was elected USSR people's deputy in 1989. The 
SP actively participates in information meetings on Fridays at 
the oblast DPP [House of Party Education] (up to 450 persons, 
including representatives of the city and oblast authorities; 
they discuss city problems and hold debates). 
  They organize volunteer work days and help cooperatives. 
They 
collaborate with other groups in Magadan Oblast. 
  Since January 1989 they have put out an information bulletin 
(editor is V. Saldusov, 25 pages, circulation of 2,000; 
rotoprint). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 2, pp 182-183. 

<H5>    Settlement of Provideniya </H5>
<H5>  Greens ["Zelenyye"] </H5>
  The total number of members is 20. Task: protection of the 
environment, chiefly the air and water. They collaborate with 
the American Pacific Tradition Society (PTS) and carry on joint 
humanitarian and cultural programs, including exchange of 
delegations. The PTS considers the collaboration "very fruitful." 
  Address: 686910, Magadan Oblast, pos. Provideniya, ul. 
Dezhneva, d. 51, kv. 47; Klavdiya Ivanovna Burakova (doctor), 
Lyudmila Alekseyevskaya (geophysicist, worked with a state 
nature protection organization). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Mariy-El </H5>

<H5>  City of Yoshkar-Ola </H5>
<H5>  Social-Ecological Group ["Sotsialno-ekologicheskaya gruppa"] </H5>
  It was founded in 1987. It conducts ecological research, 
engages in ecological education, and protests against the local 
biochemical enterprise. 
  In May 1989 they participated in a protest rally against 
construction of a vitamin plant in the community of Mochalishche 
next to the Mari-Chudra National Park and 80 kilometers from the 
city. In the summer of 1989 it was decided to suspend 
construction. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 424002, city of Yoshkar-Ola, ul. Pervomayskaya, d. 
104, kv. 8, tel. 4-37-72, Pavel V. Kopylov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Moscow Oblast </H5>

<H5>  City of Balashikha </H5>
<H3>  Greens Movement ["Zelenoye dvizheniye"], Regional 
Organization </H3>
  It monitors the state of ecology and the cultural heritage 
in 
the region. It opposes pollution of the rivers, industrial 
expansion, and turning architectural monuments over to 
commercial organizations. A number of the activists are members 
of the RPZ (see article). 
  It is a member of the Greens Movement (see article). 
  Address: 143900, Moscow Oblast, city of Balashikha, ul. 
Nekrasova, d. 11, kv. 6, tel. 521-00-75, (city of Moscow). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Bolshevo-1 </H5>

<H5>  Cosmos ["Kosmos"] </H5>
  The people's university of KSP is an ecological 
organization. 
  Address: 141090, Moscow Oblast, city of Bolshevo-1, ul. 
Moskovskaya, d. 4, korp. 4, kv. 33, tel. 284-00-25-k (home), 
fax: d. 9497, Yan Ivanovich Koltunov, chairman of the KSP. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Vidnoye (Leninskiy Rayon) </H5>

<H3>  Initiative Ecology Group of the City of Vidnoye 
["Initsiativnaya ekologicheskaya gruppa g. Vidnoye"] </H3>
  It is struggling against construction of a road through the 
city. 
  Address: 142718, Moscow Oblast, Leninskiy Rayon, city of 
Vidnoye, pos. Izmaylovo, d. 4, kv. 14, tel. 329-34-88, Vasiliy A 
Latushkin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Voskresensk </H5>

<H5>  Spring ["Rodnik"], Voskresensk Ecological Society </H5>
  This is a rayon organization that operates in suburban 
Moscow. 
  Beginning in March 1990 it has fought to have cutting 
prohibited in the forest included in the Kolomna Forestry 
Combine and to prohibit phosphorite mining (the mine was started 
up by the 14 October 1987 Directive of the RSFSR Council of 
Ministers on the Fosfaty Production Association). It 
collaborates with V. Knyazev, deputy to the Kolomenskiy 
Raysoviet, and G. Galochkina and E. Kharitonov, deputies of the 
Kolomna city soviet. 
  The leaders are V. Shmitko and R. Sokolova. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galochkina, G., and Kharitonov, 
E., "Undeclared Aggression," ZELENYY MIR, No 21-22, 1991, p 12; 
  -  "Gornostayev, Ye., Chairman of the Rayispolkom," 
KOMSOMOLSKAYA 
PRAVDA, 13 March 1990. 

<H5>    City of Dubna </H5>
<H3>  Council of the Nature Protection Society in Oiyai ["Sovet 
Obshchestva okhrany prirody v Oiyai"] </H3>
  Task--to solve the ecological problems of the city and the 
oblast. It participates in solving the problems of protecting 
the plant and animal worlds, preserving biological diversity, 
and developing the system of specially protected natural areas 
and sites. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 141980, Moscow Oblast, city of Dubna, ul. 
Kaliningradskaya, d. 22, kv. 186, tel. 3-23-74, 6-41-73 (home), 
6-30-55 (work), Anatoliy P. Sumbayev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Community of Zarya (Balashikhinskiy Rayon) </H5>

<H3>  Association To Promote Ecological Initiatives 
["Assotsiatsiya sodeystviya ekologicheskim initsiativam"] </H3>
  It works on questions of introducing "clean" technologies 
and 
alternative energy sources. Its management organ is a governing 
board, whose chairman is Aleksandr Gennadiyevich Chenarukhin. 
  Address: 143992, Moscow Oblast, Balashikhinskiy Rayon, pos. 
Zarya, ul. Gagarina, d. 11, kv. 60, tel 525-95-39. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "To the Informals...," op. cit., 
SPASENIYE, No 3, March 1991, p 6. 

<H5>    City of Zvenigorod </H5>
<H5>  Forest Defense Committee ["Komitet zashchity lesa"] </H5>
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 143090, Moscow Oblast, city of Zvenigorod, 
Nakhabinskiy tupik, d. 5, tel. 2-59-72, Lev A. Averin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Kaliningrad </H5>

<H5>  Ecowitch ["Ekolokon"], Society </H5>
  It considers its task to be solving ecological problems in 
the city and the oblast. 
  Address: 141070, Moscow Oblast, city of Kaliningrad, ul. 
Korsakova, d. 3, kv. 18, tel 518-58-44, Lyudmila I. Sokolchik. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Kolomna </H5>

<H5>  Greens Movement of Kolomna ["Dvizheniye zelenykh Kolomny"] </H5>
  It is a member of the Greens Movement (see article). It 
develops alternative plans, designs, and technologies. It works 
on ecological education and collection and distribution of 
ecological information. It participates in solving the problems 
of protecting the plant and animal worlds. 
  In early summer 1990, it joined with several ecology clubs 
into a citywide association. On 5 June, Nature Protection Day, 
they organized a rally (not more than 100 persons). 
  Address: 140410, Moscow Oblast, city of Kolomna, ul. 
Zelenaya, d. 30, Pedinstitut, tel. 3-31-35, Aleksandr P. 
Ryzhenkov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 166. 

<H5>    Settlement of Kosino </H5>
<H5>  Ekopolis Kosino ["Ekopolis-Kosino"], Club </H5>
  It appeared in 1985 at the initiative of D. B. 
Serebrovskaya, 
senior scientific associate at the USSR Academy of Sciences 
Institute of the History of Natural Science and Engineering, and 
V. V. Bortnikova, club director at a factory of the Kosino 
Knitted Goods Production Association. 
  The club program: doing scientific research, ensuring 
ecological development, and enlisting the population during free 
time. 
  Tasks: preservation of the community of Kosino and 
development of alternative long-range programs of 
social-ecological development of the area, creation of 
scientific, medical, and children's centers, preservation of 
City Preserve No 3, and implementation of the Land--Children 
farmer program (author--V. V. Ivanov). 
  Club members, having studied the condition of the land, 
substantiated the impossibility of high-rise construction. They 
worked out a program of alternative ways to raise children. 
  According to the cardfile of club participants, there are 
150 
members, with an aktiv of 20 persons, including a deputy of the 
local soviet. 
  The club collaborates with the Social-Ecological Alliance 
(see article), the All-Russian Nature Protection Society (see 
article), and the All-Union Society for the Protection of 
Monuments of History and Culture (see article). 
  Address: Moscow oblast, Kosino-1, ul. Bolshaya Kosinskaya, 
d. 
23, tel. 550-01-49, Kira Borisovna Serebrovskaya. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Funds 1, 2. 

<H5>    City of Mytishchi </H5>

<H5>  Yauza ["Yauza"], Public Council </H5>
  It has operated in Mytishchinskiy Rayon of Moscow Oblast 
since 1988. It is not registered. 
  The council is fighting to stop construction of the Northern 
TETs and for cleaning up the Yauza and its small tributaries 
(Borisovki, Sukromki). It participates in volunteer work days. 
  The council collaborates with the Moscow Ecological 
Federation (see article). In September 1989 MOSKOVSKIY LITERATOR 
published an open letter from members of the Yauza society to 
Academician V. Ye. Sokolov, chairman of the Soviet Committee on 
Cultural and Natural Heritage under the UNESCO "Humanity and the 
Biosphere" Program, and to V. Astafyev, V. Belov, and V. 
Rasputin, writers and USSR people's deputies. The letter 
proposes concrete ways to save "national dignity in this corner 
of the ancient Russian historical and cultural landscape," among 
them declaring a new protective zone around the villages of 
Tayninskoye, Chelobityevo, and Sgonniki and beginning 
archeological study of them, supporting the idea of building a 
wooded park there. 
  The letter to the newspaper was written by I. I. 
Banshchikova, Z. V. Sitnik, and L. V. Khokhlova. 
  Address: Moscow Oblast, city of Mytishchi, tel. 581-78-04, 
L. 
I. Khokhlova, chairman of the society. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Village of Nepetsyno (Kolomenskiy Rayon) </H5>

<H3>  Nature Defense League of Nepetsino Secondary School ["Liga 
zashchity prirody Nepetsinskoy sredney shkoly"] </H3>
  This is chiefly a children's organization and works on 
ecological education. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 140473, Moscow Oblast, Kolomenskiy Rayon, c. 
Nepetsino, d. 46, Aleksandr S. Oleynikov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Protvino </H5>

<H3>  Protvino Nature Protection Society ["Protvinskoye 
obshchestvo okhrany prirody"] </H3>
  It engages in ecological education, studies public opinion, 
and collects and disseminates ecological information. It works 
on questions of protecting the plant and animal worlds and 
developing the system of specially protected natural areas and 
sites. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 142284, Moscow Oblast, city of Protvino, ul. 
Lenina, 
d. 30, kv. 34, tel 92-84 (work), 93-41 (home), Vladimir G. 
Zinchenko 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Pushchino </H5>

<H3>  Oka Ecological Society ["Okskoye ekologicheskoye 
obshchestvo"] (EKOR) </H3>
  It works on problems of harmful discharges in the Oka River 
basin and organizes ecology expeditions. 
  Address: 142292, Moscow Oblast, city of Pushchino, a/ya 132, 
Vladislav Aleksandrovich Gurkin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Troitsk </H5>

<H3>  Troitsk Branch of the Social-Ecological Alliance 
["Troitskoye otdeleniye Sotsialno-ekologicheskogo soyuza"] </H3>
  It is a member of the Social-Ecological Alliance (see 
article). 
  It monitors the quality of food products, consumer goods, 
and 
public health. It works on ecological education, studies public 
opinion, and collects and disseminates ecological information. 
It participates in solving the problems of protecting the plant 
and animal worlds, preserving biological diversity, and 
preserving and developing natural areas and cultural monuments 
and problems linked with the use of nuclear energy and 
construction of AES's. 
  Address: 142092, Moscow Oblast, city of Troitsk, ul. 
Solnechnaya, d. 8, kv. 101, tel 334-04-24, Andrey A. Yegorov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Khotkovo (Zagorskiy Rayon) </H5>

<H3>  Zagorsk Ecological Society ["Zagorskoye ekologicheskoye 
obshchestvo"] </H3>
  It conducts ecological examinations of industrial 
enterprises 
and ecological expert studies of economic plans and 
administrative decisions. It monitors environmental preservation 
and the quality of food products, consumer goods, and public 
health. It organizes ecological education, studies public 
opinion, and collects ecological information. It participates in 
solving problems of protecting the plant and animal worlds, 
preserving biological diversity, and preserving and developing 
the system of specially protected natural areas, including 
preservation of forests and historical-architectural objects, 
and problems linked to industrial and domestic waste and the use 
of nuclear energy and construction of AES's. 
  It engages in sociopolitical activities (participation in 
elections and the like). 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 141350, Moscow Oblast, Zagorskiy Rayon, city of 
Khotkovo, 1-ya Lesnaya ul., d. 8, tel. 3-27-27, Yuriy Maslov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Settlement of Chernogolovka </H5>

<H3>  Ecologist ["Ekolog"], Society of the USSR Academy of 
Sciences Noginsk Science Center </H3>
  It was founded in October 1988. Its task is to solve the 
region's ecological problems. The society conducts ecological 
expert studies of industrial enterprises. 
  It is a member of the Social-Ecological Alliance (see 
article). Ecologist supported the candidacy of Yuriy Afanasyev 
for USSR people's deputy and Gleb Yakunin for RSFSR people's 
deputy. 
  Addresses: 142438, Moscow Oblast, settlement of 
Chernogolovka, ul. Tsentralnaya, d. 18, kv. 118, tel. 76-06, Ye. 
Lisetskiy; pr. Institutskiy, d. 3, kv. 280, Yu. Gorelov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Murmansk Oblast </H5>

<H5>  City of Murmansk </H5>
<H5>  Green Branch ["Zelenaya vetv"] </H5>
  Ecology club. It was formed in September 1989 at Murmansk 
Gymnasium-School No 51. The immediate reason for the club's 
formation was an abrupt worsening of the ecological situation in 
the microrayon. 
  Goal: "Instill ecological awareness in the inhabitants of 
the 
city of Murmansk and Murmansk Oblast and prevent an ecological 
disaster in the region." 
  Tasks: draw public attention to the ecological problems of 
the region; establish and strengthen contacts with international 
ecology organizations; influence local organs of authority to 
develop concrete policies to clean up the ecological situation 
in the region; organize ecological actions to clean up the city 
of Murmansk; and set up an "ecological nursery" in the city. 
  Forms of work: lectures, conferences and marches, collection 
of signatures, trips abroad by schoolchildren, and the like. 
  In September 1989 they prepared a survey (a photo album with 
attached materials) of the ecological state of their microrayon 
and gave it to the local organs of authority. They are proposing 
to do similar surveys each year. 
  In 1989-1990 they participated in development of the program 
of the international ecological action in Murmansk called "Next 
Stop." Together with members of a Danish ecology organization 
they took part in cleaning up after an accidental discharge of 
fecal waters from the Murmansk poultry factory. 
  In early 1990 some of the former members of the Christian 
Greens Movement (see article), which had fallen apart, joined ZV. 
  The club participated in the 1990 election campaign and 
joined the voter bloc formed by the city volunteer 
historical-educational society called Memorial. The Citizens 
Initiative Club, the city Democratic Platform Party club, the 
Union of Social Defense and Rehabilitation, the 
social-democratic society, and the oblast union of cooperative 
members also joined the bloc. 
  There was a coordinating center for the bloc's election 
campaign, and they organized duty watches at the voting 
precincts. As a result of the elections, about 30 of the bloc's 
candidates became deputies of the oblast soviet and about 20 at 
the city soviet. 
  In mid-May 1990 the club took part in an international 
ecology conference in Bergen, Norway. 
  They conducted protests during the debates in 1990 about 
construction of the Yokaganskaya AES and building new ships for 
the nuclear-powered fleet. 
  The organization is developing a model program of ecological 
education for secondary school and the pedagogical institute. 
They are conducting a regular class in School No 51, lecture 
work (for example, Professor Davydov, an associate at one of the 
Moscow institutes of the USSR Academy of Sciences, was invited 
by Green Branch and delivered lectures), seminars for oblast 
teachers (by January 1991 four seminars had been held), 
role-playing games, and the like. Ecology marches are 
increasingly infrequent and small (for example, 27 April 1991); 
they have collected signatures against construction of the 
nuclear-powered fleet and against deliberate contamination of 
the Barents Sea. 
  ZV collaborates with foreign ecology organizations (which is 
promoted by students at the gymnasium who study the English 
language). Contacts are maintained with 10 countries, including 
the following: 

  -  Norway: on 5-6 October 1991, a Soviet-Norwegian conference 
of ecology organizations was held in Murmansk. Ecologists from 
Murmansk and the oblast participated on the Soviet side; the 
Norwegians were represented by the Nature and Youth Association 
(the "sister" organization to Green Branch) and Stop the Death 
Clouds. ZV collaborates with the school of ecology at the Higher 
School in Alta (in December 1991 a group of 40 ZV members 
visited Alta); 
  -  Sweden: exchange of school classes (this cannot 
be considered a direct form of activity by Green Branch proper, 
but there are always ecologists in every group); 
  -  Great Britain: 
contacts with the Green organization Stop Hinckley A.F. (the 
fight against the AES in Hinckley), with a school in Nottingham, 
and with the Greens in Scotland; 
  -  USA: exchange with a school in 
Jacksonville; in August 1991 one of the secondary-school members 
of ZV participated in the annual conference held by Care Taken 
of Environment, an organization of ecology teachers (city of 
Cuzco, Peru); 
  -  Spain and Portugal: correspondence with schools 
that practice ecological education. 
  ZV has both individual members (mainly teachers and 
secondary 
school graduates, of whom there are 40) and collective members 
(the two oldest classes). At the October 1991 meeting, the 
council of six members was elected (G. A. Khoreva--geography 
teacher, Furman, Fanyushkina, Rogachev, Kreminskaya, and 
Pronkina) and a decision was adopted to submit documents for 
registration. (The R2,000 needed for registration is a problem.) 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, pp 196, 197. 

<H3>    Greens Movement of the City of Murmansk ["Zelenoye 
dvizheniye g. Murmansk"] </H3>
  Task: defense of the marine environment against pollution. 
  Address: 183072, city of Murmansk, ul. Starostina, d. 19, 
kv. 
40, tel. 362-01-75 (city of Moscow), Yuliy Mironovich Polonskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Christian Greens Movement ["Khristianskoye dvizheniye </H5>

zelenykh"] 
  It originated in mid-1989 under the influence of Next Stop, 
which visited the city. Six persons joined the KhDZ. Despite the 
name the group was not noteworthy for a Christian orientation. 
It collaborated with the Murmansk ecology association Green 
Branch (see article). 
  In early 1990 the group came apart: one participant of KhDZ 
was jailed for theft, two left the city (in part this was 
connected with the narcotics used by several KhDZ members), and 
three of them joined Green Branch (Olga Pronkina became a member 
of the ZV council). 
  Address: city of Murmansk, tel. 4-15-21, Pronkina, Olga. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H5>    City of Apatity </H5>
<H3>  Public Ecology Committee ["Obshchestvennyy ekologicheskiy 
komitet"] </H3>
  It was formed in March 1988 in Kirovsk and Apatity. 50 
participants. They consider it their goal to improve the 
ecological situation on the Kola Peninsula. 
  The committee monitors preservation of the environment, the 
quality of food products and consumer goods, and public health. 
It conducts expert ecological studies of economic plans. It 
works on ecological education and takes part in sociopolitical 
activities. 
  It is a member of the Social-Ecological Alliance (see 
article) and the Ecology and Peace organization (see article). 
It cooperates with the Volunteer Society To Promote Perestroyka 
(city of Apatity). 
  Address: 184200, Murmansk Oblast, city of Apatity, ul. 
Lenina, d. 18, kv. 35, Valentina Timofeyevna Filatova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Kola </H5>

<H5>  Ecology Group ["Ekologicheskaya gruppa"] </H5>
  It organizes ecological education. 
  Address: 184360, Murmansk Oblast, city of Kola, ul. 
Andrusenko, d. 8, Shkola No 1, tel. 2-21-87, V. Karelin, N. 
Koksharova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of MonchegorsK </H5>

<H5>  Ecogroup of the Severonikel [Northern Nickel] Combine </H5>
  It opposes the combine's harmful discharges and fights for 
the installation of new decontamination structures. 
  Address: 184280, Murmansk Oblast, city of Monchegorsk, ul. 
Lenina, d. 14, kv. 296, tel. 3-50-95, Mikhail V. Dmitriyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Pechenga </H5>

<H5>  Ecology Group ["Ekologicheskaya gruppa"] </H5>
  It works on questions of the impact of environmental 
pollution on human health. 
  Address: 184411, Murmansk Oblast, city of Pechenga, 
Pechengskoye shosse, d. 3, kv. 17, A. Stepanov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Nizhniy Novgorod Oblast </H5>

<H5>  City of Nizhniy Novgorod (Gorky) </H5>
<H5>  Avant Garde ["Avangard"] </H5>
  The association was founded in May 1988. It organizes 
rallies 
against AES's. In early 1989 the aktiv was 24 persons. It is 
oriented to the People's Front. The Women Against the AST 
Committee operates under it. 
  Address: 603011, city of Nizhniy Novgorod, ul. Oktyabrskoy 
Revolyutsii, d. 72, kv. 32, tel. 42-99-63, Aleksey V. Chernyshev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Dodo Bird ["Dront"], Oblast Youth Ecology Center ["Oblastnoy </H5>

molodezhnyy ekologicheskiy tsentr"] 
  It holds conferences on problems of the Volga River, 
conducts 
ecology expeditions on the river, publishes books, and 
distributes radiometers. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 603163, city of Nizhniy Novgorod, mkrn. Verkhniye 
Pechory, ul. Lopatina, d. 11, kv. 143, tel. 39-74-79 (work), 
39-73-40 (home), Askhat A. Kayumov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2.}txt1} 
<H3>  Nature Protection Squad ["Druzhina okhrany prirody"] of 
Niznhiy Novgorod (Gorky) University </H3>

  It was established on 18 March 1972. It engages in nature 
protection activities and the fight against poaching. 
  There is also a DOP at the Arzamas Pedagogical Institute. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    For Nuclear Safety ["Za atomnuyu besopasnost"], Oblast </H5>

Volunteer Society 
  It opposes the Gorky AES. It was founded on 25 December 
1988. 
It includes activists from Nizhniy Novgorod (Gorky), Dzerzhinsk, 
Bor, Kstov, and Bogorodsk (several hundred persons). It 
collaborates with many ecology groups of the oblast and region, 
has contacts with deputies of various levels, and conducts 
large-scale protest actions. 
  Address: 603081, city of Nizhniy Novgorod, ul. Tereshkovoy, 
tel. 65-36-39, Yuriy Mikhaylovich Likhachev; tel. 33-03-13 
(home), Mikhail Leonidovich Levin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Green Shore ["Zelenyy bereg"] </H5>

  It monitors construction on the shores of Meshcherskoye Lake 
and planting. It favors creation of a wooded park zone along the 
Nizhniy Novgorod-Vyatka highway. 
  Address: 603159, city of Nizhniy Novgorod, ul. Akimova, d. 
49, kv. 32, tel. 35-84-23, 43-13-93, Nina P. Kiryushkina. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Green World ["Zelenyy mir"], Ecological Association. </H5>

  It was founded in 1988. It participates in solving the 
problems of protecting the plant and animal worlds and 
preserving biological diversity and problems related to the use 
of nuclear energy and construction of AES's. 
  It conducts conferences on problems of the Volga. It is a 
member of the Social-Ecological Alliance (see article). 
  Address: 603026, city of Nizhniy Novgorod, ul. Krasnykh zor, 
d. 15, kv. 409, tel. 24-39-41, Valentina V. Malakhova; tel. 
46-73-56. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Kitavras, Cultural-Ecological Association </H5>

  It was formed in 1988. It engages in ecological education, 
study of public opinion, collection and dissemination of 
ecological information, and study of cultural traditions. 
  The association performs ecological expert studies of 
economic plans and administrative decisions and monitors the 
quality of food products, consumer goods, and public health. It 
participates in solving the problems of protecting the plant and 
animal worlds, preserving biological diversity, and preserving 
and developing natural areas and cultural monuments and problems 
related to agricultural pollution, the use of nuclear energy, 
and construction and operation of AES's and hydroengineering 
structures. 
  It is a member of the Social-Ecological Alliance (see 
article) 
  Address:603000, city of Nizhniy Novgorod, pl. Gorkogo, d. 4, 
kv. 28, tel. 33-44-10, Nikolay V. Morokhin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Molitovka Public Council ["Molitovskiy obshchestvenyy sovet"] </H5>

  It was formed in November 1988 in the microrayon of 
Molitovka. It is a federation of building councils. 
  Address: 603132, city of Nizhniy Novgorod, ul. Admirala 
Makarova, d. 3, Opornyy punkt okhrany prirody, tel. 48-09-17, 
48-07-67, Vadim V. Belov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Nizhniy Novgorod Council for the Ecology of Culture (NSEK) </H5>

  It appeared in May-June 1988 and was registered in November 
1988 at the Gorky branch of the USSR Culture Foundation. It 
takes actions to preserve the historical structures of the city. 
Forms of work: picketing, lectures, seminars. They have by-laws 
and a program. There are 50 members and an aktiv of 15. The 
activists pay dues. The coordinating council has three members. 
The by-laws envision a chairman. The leader is Stas 
Dmitriyevskiy. 
  In May-June 1988 activists of the group set up pickets 
(tents) at a small park which is a monument of park and garden 
architecture (it was to be razed to build the first metro 
station in the Nagornaya part of the city). About 20 persons 
participated directly in the picketing. Up to several hundred 
persons gathered around the pickets. Construction of the metro 
in the Nagornaya (historical) part of the city was suspended. 
  In January-April 1989 members of the council fought to 
preserve the mansion of the respected Nizhniy Novgorod citizen 
Yankin, a monument of 19th century architecture (Studenaya 
Street, Building 33a). As a result a commission from the RSFSR 
Ministry of Culture prohibited demolition of the monument and 
ordered a comprehensive study of the issue, but the mansion was 
demolished by the decision of the local authorities. Council 
activists prepared documents for a court hearing with the local 
authorities. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, pp 199-200. 

<H3>    Greens Party of the Nizhniy Novgorod Region ["Partiya 
zelenykh Nizhegorodskogo kraya"] </H3>
  It was formed in 1990 within the all-Union Greens Party (see 
article). It was constituted as an autonomous party in the 
spring of 1991. It was the initiator in formation of the Greens 
Parties League (see article). It has several members. The leader 
is S. Fomichev. PZNK activists participated in picketing the 
Gorky AEST and in the anarchists' action to blockade the 
Zaporozhye Coke-Chemical Combine. The party collaborates with 
the Rainbow Keepers organization (see article). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Bioautomation ["Bioavtomatika"] NITs [Scientific Research </H5>

Center] Ecology Group 
  It engages in ecological education. 
  Address: 603107, city of Nizhniy Novgorod, ul. Shcherbinki, 
d. 1, kv. 15, kv. 173, tel. 38-88-41, Konstantin N. Tkachev,. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Group of the Socialist Youth Association of the </H5>

Leninskiy Raykom of the All-Union Komsomol ["Ekologicheskaya 
gruppa pri Sotsialisticheskom obyedinenii molodezhi Leninskogo 
RK VLKSM"] 
  It engages in teaching, planning projects, and work with 
deputies. 
  Address: 603041, city of Nizhniy Novgorod, per. Bakinskiy, 
d. 
12, kv. 10, tel. 38-88-83, Yevgeniy V. Orlov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Section of the Nizhniy Novgorod City Organization of </H5>

the USSR Journalists Union ["Ekologicheskaya sektsiya 
Nizhegorodskoy organizatsii Soyuza zhurnalistov SSSR"] 
  It organizes publications on ecological issues, above all 
problems of the Volga. 
  Address: 603009, ul. Pyatigorskaya, d. 22a, kv. 8, tel. 
38-94-70, Tatyana P. Selivanovskaya. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Club [Ekologicheskiy klub"] at the (Nizhniy </H5>

Novgorod) Gorky Mayak Garment and Trade Production Association 
  It engages in planting greenery and ecological education. 
The 
aktiv is 15 persons. 
  Address: 603109, city of Nizhniy Novgorod, ul. Gogolya, d. 
5, 
tel. 34-22-46, Irina Vladimirovna Andreyeva. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecosphere ["Ekosfera"], Working Group </H5>

  It was formed by students of the medical and polytechnical 
institutes. It works on problems of vehicle emissions. 
  Address: 603146, city of Nizhniy Novgorod, ul. Beketova, d. 
66, kv. 12, tel. 62-06-28, Natalya Yuryevna Orlinskaya. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Vyksa </H5>

<H3>  Greens Party of the City of Vyksa ["Partiya zelenykh g. 
Vyksy"] </H3>
  It is taking action against cutting the forests and 
construction of the district road. 
  Address: 607000, Nizhniy Novgorod Oblast, city of Vyksa, 
mkrn. Gogolya, d. 6, kv. 41, Pavel Kudasov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Dzerzhinsk </H5>

<H3>  Initiative Ecology Group ["Initsiativnaya ekologicheskaya 
gruppa"] </H3>
  Address: 606005, Nizhniy Novgorod Oblast, city of 
Dzerzhinsk, 
pr. Tsiolkovskogo, d. 196, Aleksey Alekseyevich Lushnikov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Pravdinsk </H5>

<H3>  Greens Initiative Group ["Initsiativnaya gruppa zelenykh"] 
at the Radio Equipment Plant of the City of Pravdinsk </H3>
  It takes actions to improve working conditions and the 
ecological situation at the enterprise and near it. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    Novgorod Oblast </H5>
<H5>  City of Novgorod </H5>
<H5>  Greens Society ["Obshchestvo zelenykh"] </H5>
  Address: 173015, city of Novgorod, ul. Pskovskaya, d. 18, 
korp. 3, kv. 70, Aleksandra N. Martynovich. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology ["Ekologiya"], Club </H5>

  It works on ecological problems of the city: ecological 
education, study of public opinion, and collection and 
dissemination of ecological information. It participates in 
solving problems of protecting the plant and animal worlds and 
developing the system of specially protected natural areas and 
sites and problems related to agricultural pollution 
(pesticides, fertilizers, and the like) and industrial and 
domestic waste. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Addresses: 173011, city of Novgorod, ul. Koroleva, d. 7a, 
kv. 
76, Petr Gorchakov; 173003, ul. Sankt-Peterburgskaya, d. 27, kv. 
62, tel. 3-76-17, 7-67-43, Inessa Antonovna Pochetova. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H5>    City of Borovichi </H5>
<H3>  Ecology Club of the City of Borovichi ["Ekologicheskiy klub 
g. Borovichi"] </H3>
  It organizes ecological expert study of economic plans and 
administrative decisions and ecological education, studies 
public opinion, and collects and disseminates ecological 
information. It participates in solving problems related to the 
use of nuclear energy and construction of AES's. 
  Address: 174400, Novgorod Oblast, city of Borovichi, nab. 
Oktyabrskoy Revolyutsii, d. 17, Krayevoy muzey, tel. 5-51-81, 
Valentin Pavlov; ul. Gogolya, d. 17, tel. 45-48. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Novosibirsk Oblast </H5>

<H5>  City of Novosibirsk </H5>
<H5>  Initiative ["Initsiativa"], Novosibirsk Ecology Council </H5>
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 630081, city of Novosibirsk, ul. Michurina, d. 43, 
kv. 38, Vera Vladimirovna Mishurova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    "Pamyat" [Memory], Historical-Patriotic Association, Ecology </H5>

Section 
  The association emerged in 1985 from the radical part of the 
Volunteer Sobriety Society. It is registered. 
  The section conducts rallies. It has developed plans for 
alternative energy. Among other things, it is searching for an 
energy alternative to the GES proposed in Novosibirsk. On 7 June 
1988 the section, together with the Siberian Department of the 
USSR Academy of Sciences, conducted a conference on power 
engineering at which it presented and defended an alternative 
plan for development of the fuel-energy complex. 
  The leader is Bogdan Gavrilko. The total number of members 
is 
80. A majority of them are associates of the Siberian Department 
of the USSR Academy of Sciences; 20 percent are candidates and 
doctors of sciences, and about 20 percent are former CPSU 
members. 
  According to some evaluations, the members of the 
association 
initially held to a national socialist orientation, but since 
1990 anticommunists have dominated in the association. 
  In 1989 the section was admitted to the Social-Ecological 
Alliance (see article), which caused some participants in the 
SoES to protest. 
  Address: 630072, city of Novosibirsk, ul. Akademicheskaya, 
d. 
19, kv. 16, tel. 35-09-60, Tatyana A. Belogrudova 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 202. 

<H3>    Ecological Initiative Center ["Tsentr ekologicheskoy 
initsiativy"] </H3>
  This is chiefly a children's organization and engages in 
ecological education. 
  Address: 630122, city of Novosibirsk, ul. 2-ya Soyuza 
Molodezhi, d. 33, kv. 16, tel. 25-42-10, Yuliya R. Gertsvolf. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Omsk Oblast </H5>

<H5>  City of Omsk </H5>
<H3>  Green City ["Zelenyy gorod"], Social-Ecological Association 
(other name--Green World ["Zelenyy mir"]) </H3>
  It was founded in June 1988 based on a group at the NTTM 
[Youth Scientific-Technical Creativity] Center in Omsk. 
  The association has adopted by-laws. In 1989 30-50 persons 
participated in the weekly meetings at the Nature House. Since 
1989 meetings have been held in the Political Education House. 
The aktiv is 15 persons. The association's management organ is 
the council. 
  The association studies the condition of the air environment 
in the city, the level of its contamination, and the effect on 
public health. It makes observations of radiation discharges, 
conducts ecological expert studies, participates in the city 
debate tribune on ecology, holds conferences, organizes rallies 
and marches, and participates in political activity. 
  They have set up an information board in the center of the 
city. They worked to collect signatures against construction of 
the Southern Omsk Irrigation System and other undertakings 
without expert ecological studies. 
  In 1988 there was a conference on the issue of the state of 
the environment. 
  In December 1988 the association held a conference on 
questions of building a metro in the city. 
  In late 1988 they adopted an appeal to the citizens of the 
city concerning the ecological situation. Then they gathered 
about 6,000 signatures on it and in July 1989 sent all the 
signatures and an accompanying letter to the USSR Council of 
Ministers. 
  In 1989 they organized two major debates (several hundred 
people participated): on the eastern industrial center in the 
city, and about the plan to build a garbage-burning plant. 
(Representatives of the association spoke in favor of building a 
garbage processing plant, not a garbage-burning plant). 
  On 12 May 1989 they held a constituent meeting and adopted 
by-laws, a general conception of the ecology movement, and an 
appeal concerning the ecological situation in the oblast. They 
take part in sociopolitical actions together with other groups 
(preparation for the December 1988 rally and others). They took 
an active party in the 1989 and 1990 election campaigns. In the 
elections for USSR people's deputies, they supported A. K. 
Kazannik. In the summer of 1989 the association, together with 
the Dialog Club, collected signatures on a demand to transfer 
"nomenklatura" facilities--a dormitory, special polyclinic, the 
CPSU obkom dacha, and the like to the working people (by 
mid-August they had collected about 20,000 signatures). 
  On 13 August 1989, together with the Omsk sociopolitical 
club 
Dialog, the association participated in conducting a rally at 
DOSAAF Stadium with the title, "The Soviets and the Ecological 
Crisis" (2,500 participants). 
  On 18 June 1989 they participated in an information meeting 
of politicized "informal associations" of the city (in all about 
70 persons, 30 of them with full voting rights; 10 organizations 
were represented, including Dialog and Memorial). 
  On 3 June 1990 they conducted an ecology rally (300 
persons). 
Slogans demanding Russian independence rang out. 
  They took part in the conference of democratic movements of 
the city organized by the Omsk People's Front on 27 May 1990. 
Representatives of the Democratic Union, the Social-Democratic 
Party of Russia, Dialog, and the city voters club participated. 
  Addresses: 644048, city of Omsk, ul. Marksa, d. 6, kv. 56, 
tel. 31-30-83, Nikolay N. Senin; 644066, city of Omsk, a/ya 
2822; tel. 64-76-56, Vladimir Mikhaylovich Kuropatchenko. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 173. 

<H5>    Orenburg Oblast </H5>
<H5>  City of Orenburg </H5>
<H5>  Green Committee ["Zelenyy komitet"] </H5>
  It was founded at the Orenburg Polytechnical Institute in 
October 1988. Its by-laws and program were adopted in the middle 
of November of the same year. The total number of members is 
150, with an aktiv of 50 and an executive-coordinating council 
of 11 (in 1988). The average age is 30 years. The social 
composition is teachers and students. Meetings of committee 
members in 1989-1990 were held in the premises of the Pegasus 
["Pegas"] Scientific Research Institute (or VNIIPIGAS). 
  Goal--to avert ecological disaster. Tasks--develop a program 
for ecological normalization of the region and re-equip harmful 
production facilities. Their primary work is directed against 
construction of the Orenburg combine to produce BVK. Forms of 
work: picketing and work by ZK representatives in soviets at 
various levels. 
  In early December 1988 they picketed with ecological slogans 
in front of delegates to the city party conference and passed 
out fliers to the delegates; on 16 December they picketed the 
oblast party conference. 
  The Green Committee took an active part in the 1989 election 
campaign for USSR people's deputy. Committee member V. A. 
Shapovalenko became a USSR people's deputy. 
  In the course of the 1990 election campaign, they were able 
to get their representatives into soviets of people's deputies 
on the city and oblast levels. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Addresses: 460001, city of Orenburg, ul. Chkalova, d. 22, 
kv. 
55, tel. 41-47-79, Tamara V. Zlotnikova; 460000, city of 
Orenburg, ul. Pushkinskaya, d. 20, tel. 47-62-01; tel. 47-86-13, 
Gabriel Konstantinovich Shapovalenko (or Konstantin Gabrilov). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya" partii...," op. 
cit., vol 1, part 2, p 206. 

<H5>    Orel Oblast </H5>
<H5>  City of Orel </H5>
<H5>  Nature Protection Squad ["Druzhina okhrany prirody"] </H5>
  It collaborates with the city Association of Young 
Historians. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Rus ["Rus"] </H5>

  This is an ecology group. It works on ecological -cultural 
problems. It collaborates with the city Association of Young 
Historians. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Penza Oblast </H5>

<H5>  City of Penza </H5>
<H3>  Ecology Club at the Youth Initiatives Foundation 
[Ekologicheskiy klub pri Fonde molodezhnykh initsiativ"] </H3>
  It participates in solving problems related to the 
construction and operation of hydroengineering structures and 
also industrial pollution; among others, it conducts expert 
studies of pharmaceutical enterprises. 
  Address: 440011, city of Penza, ul. Ostrovskogo, d. 6, kv. 
54, tel. 62-39-96, 46-32-49, Dmitriy Georgiyevich Maslov. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H5>    Perm Oblast </H5>
<H5>  City of Perm </H5>
<H3>  Perm Oblast Nature Protection Committee ["Komitet po okhrane 
prirody Permskoy oblast"] </H3>
  Its activities are treated in the monthly newspaper LUCH, 
which has been coming out since mid-1990 (print run of 50,000). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "LUCH of Perm," ZELENYY MIR, No 
1-2, 1991, p 1. 

<H3>    Public Ecology Committee ["Obshchestvenno-ekologicheskiy 
komitet"] </H3>
  It originated after the newspaper VECHERNYAYA PERM in May 
1987 published an article about the ecological situation. They 
stepped up their work in early 1989 in connection with the start 
of surveying for construction of the Perm AES. 
  Goal: preserving habitat and averting an ecological disaster 
in the region and stopping construction of and rebuilding 
ecologically harmful production facilities. 
  Forms of work: rallies, collection of signatures, appeals, 
ecological monitoring, and participation in election campaigns. 
  In 1987 they collected signatures to an appeal by 
inhabitants 
of the city to the CPSU Central Committee and the USSR Supreme 
Soviet demanding the creation of a government commission with 
broad powers to study the ecological situation in the city. 
Members of the Perm League of Communists participated in the 
committee's work. 
  In September 1987 they held a rally on ecological issues at 
the DK imeni Yu. A. Gagarin (about 700 persons participated). 
  Beginning in 1988 some participants of the OEK belonged 
concurrently to the ecology section of the Perm public political 
club Dialog. 
  In the last months of 1989, they conducted a signature 
collection campaign to hold a referendum in the city on the 
issue of building the AES. (The committee alone gathered about 
40,000 signatures. In all volunteer groups in the city collected 
80,000 signatures on appeals for a referendum or demands to 
reject construction of the plant.) As a result of the 
committee's propaganda activities and a series of mass actions, 
surveying work for construction of the AES was stopped. 
  They conducted surveys of public opinion and surprise 
inspections to monitor the nitrate content in food products. In 
late 1989 they compiled an ecological map of the city that made 
it possible to study the link between the degree of 
contamination in different parts of the city and the 
distribution of illnesses. 
  They participated actively in the election campaign. The 
results of the 1990 election of people's deputies of the RSFSR 
and local soviets showed that Yu. A. Shchipakin, the committee 
chairman, was elected deputy; in connection with this S. A. 
Mazein was elected the new committee chairman. 
  They have no by-laws or program. The aktiv in 1989 was 15 
persons. Ages are from 20 to 60. Social-occupational 
composition: scientific workers, blue collar workers, office 
workers, engineering-technical personnel. 
  Meetings were held twice a month in the DK of the Plant 
imeni 
F. E. Dzerzhinskiy. From May 1988 to the end of 1989 they 
published a bulletin (edited by Yu. Shchipakin, 1-3 pages, press 
run--from 50 to a few hundred copies). 
  In 1988 they put out the journal CHELOVEK I MIR [Man and the 
World]. They maintain ties with the Kirovskiy Rayon nature 
protection society and several employees of the epidemiological 
station. A few representatives of the committee are members of 
the Social-Ecological Alliance (see article). In 1990 the 
journal and bulletin were not published, and the committee 
practically ceased to exist. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," vol l, 
part 2, p 208. 

<H5>    Kama Region Greens Party ["Partiya zelenykh Prikamya"] </H5>
  It appeared in 1990. It participates in the RPZ. It brings 
together specialists and activists of the ecology movement and 
monitors the environment in the region. In January-February 1992 
it participated unsuccessfully in the election campaign. 
  Address: city of Perm, tel. 33-63-73, Marsel Salakhovich 
Akhmetov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Perm Branch of the Social-Ecological Alliance (SES) </H5>

[Permskoye otdeleniye Sotsialno-ekologicheskogo soyuza (SES)"] 
  It was formed in May 1988 as a social-ecological commission. 
Total members--100. 
  The commission engaged in collecting and publishing 
ecological information. After the article about the ecological 
situation was published in VECHERNYAYA PERM, the SEK was 
disbanded and its members joined the public political club 
Dialog as an ecology section. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 614081, city of Perm, a/ya 5786; tel. 31-08-84, 
Galina Grigoryevna Shchipakina, as well as Aleksandr Kolotov and 
Valentin Tsitovich. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Aleksandrovsk </H5>

<H5>  Ecology Group ["Ekologicheskaya gruppa"] </H5>
  It organizes ecological education. 
  Address: 618330, Perm Oblast, city of Aleksandrovsk, ul. 
Lenina, d. 36, kv. 6, tel. 34-92, Robert P. Popov. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    City of Berezniki </H5>
<H5>  Ecology and Health ["Ekologiya i zdorovye"] </H5>
  The organization was founded in 1988. It fights to stop 
harmful emissions by a chemical combine. 
  It is a member of the Greens Movement (see article) and the 
Social-Ecological Alliance (see article). Among the 
organization's activists are Nikolay Ivanovich Savostyanov, 
Vladimir Mikhaylovich Vasev, and Boris Yefimovich Burdykin. 
  Address: 618400, Perm Oblast, city of Berezniki, ul. 
Khimikov, d. 8, kv. 78, tel. 5-26-68, fax 1224, Boris Yefimovich 
Burdykin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Settlement of Dobryanka </H5>

<H5>  Public Ecology Club </H5>
  It appeared in the mid-1980's as the legal organization of 
the semiunderground Union of Communists. It was formally 
constituted in 1987. 
  They collected 40,000 signatures for holding a referendum 
against construction of an AES. They conducted surveys of public 
opinion and monitored nitrate content. 
  The chairman is S. Mazein, and there is an aktiv of 15 
persons. Several are members of the Social-Ecological Alliance 
(see article). They put out a bulletin. 
  Address: 618710, Perm Oblast, settlement of Dobryanka, 
redaktsiya gazety KAMSKIYE ZORI, V. B. Plyusin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Cherdyn </H5>

<H5>  Ecology Group ["Ekologicheskaya gruppa"] </H5>
  It engages in investigation of underground nuclear testing 
in 
Perm Oblast. 
  Address: 618600, Perm Oblast, city of Cherdyn, ul. Gagarina, 
d. 122, Gennadiy Petrovich Dyakonov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Maritime Kray </H5>

<H5>  City of Vladivostok </H5>
<H3>  Maritime Ecology Action Society ["Primorskoye obshchestvo 
ekologicheskogo deystviya"] (POED) </H3>
  It was founded in February and officially registered in May 
1988 at the Geographic Society of the USSR Academy of Sciences. 
  Goal--harmonizing relations of man and nature. 
  Total members--50-100, aktiv--20. Coordinating council of 
seven members. They have by-laws and a program. The organization 
meets regularly in a building offered by the Geographic Society 
in the city of Vladivostok. It also operates in Arsenyev, 
Nakhodka, Dalnegorsk, Ussuriysk, and elsewhere. 
  It works on problems of defending the environment against 
the 
effect of nuclear energy. It protests against the construction 
of ecologically dangerous GES's and AES's in the Amur region and 
on the Iman and Ussuri Rivers (construction of a power plant on 
the Ussuri River was stopped in 1989). It fights against other 
forms of contamination of local bodies of water, including 
harmful discharges into the delta of the Amur River, and against 
logging the Ussuri taiga. It conducts surprise inspections to 
save the Amur Gulf resort zone and the Ussuri taiga. It favors 
conducting independent ecological expert studies. It conducts 
marches and rallies and publishes article in defense of the 
environment. 
  In 1988-1989 they held a series of rallies against 
construction of a GES in the Amur region. At the rally on 5 June 
1988 in a park in central Vladivostok, for example, about 1,000 
persons participated and about 3,000 signatures were gathered in 
support of their demand. In 1989 they opposed a visit to the 
Port of Vladivostok by the nuclear-powered lighter carrier 
Sevmorput. 
  Since 1989 they have participated in preparing deputy 
queries. 
  The society collaborates with ecology groups in Maritime 
Kray 
(cities of Arsenyev, Dalnegorsk, Dalnerechensk, Nakhodka, 
Roshchino, and Ussuriysk). 
  Address: 690000, Maritime Kray, city of Vladivostok, ul. 
Pervogo maya, d. 3, filial Geograficheskogo obshchestva AN; tel. 
2-49-17, Yuriy Kashuk. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiy: partii...," op. cit., 
vol 1, part 2, p 145. 

<H5>    Ecological Initiatives ["Ekologicheskiye initsiativy"] </H5>
  In addition to nature protection it engages in tourism. 
  It is a member of the Social-Ecological Alliance (see 
article). 
  Address: 690014, Maritime Kray, city of Vladivostok, ul. 
Nekrasova, d. 48, kv. 912a, Anatoliy V. Lebedev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Nakhodka </H5>

<H5>  Social Initiative Foundation ["Fond sotsialnoy initsiativy"] </H5>
  It was founded in January 1989. Goal--to give moral and 
financial support to the ecological initiatives of public 
organizations and individuals. 
  Address: 692900, Maritime Kray, city of Nakhodka, 
Nakhodkinskiy pr., d. 100, Yuriy Prokopyevich Platonov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Center ["Ekologicheskiy tsentr"] (ETs) </H5>

  It was founded in November 1988 and has 10 members. 
  Goal--participation in solving the ecological problems of 
the 
city and Maritime Kray. 
  Tasks--struggle against AES's and against visits to the port 
by nuclear-powered ships. 
  Forms of work: rallies, collection of signatures, seminars, 
debates, and information displays. 
  At the initiative of the Ecology Center, a campaign was 
organized to collect signatures against construction of the 
hydroengineering complex on the Bolshaya Ussurka River and 
against construction of an AES at any of three proposed 
locations (more than 5,000 signatures were gathered). Members of 
the group consider these structures inadvisable because of the 
uniqueness of the natural zone of Maritime Kray (the ETs 
proposes that these zones be declared national parks). 
Signatures were collected (more than 9,000 signatures) and a 
rally was held against allowing the nuclear-powered lighter 
carrier Sevmorput to enter the Port of Nakhodka. Together with 
the Glasnost political club, they gathered more than 2,000 
signatures to an appeal to the government against construction 
of a dock to load potassium salts and an oil bunker pier. These 
appeals with signatures were sent to the CPSU Central Committee, 
the party gorkom, and the Ministry of the Maritime Fleet. 
  Together with the International Maritime Fraternity Club, 
they conducted annual ecology and peace "peace watches" (in 
which a total of up to 500 persons took part). During these 
activities they put up displays with information on the 
ecological situation in Maritime Kray and the country as a 
whole, on the activities of "information organizations" in 
different parts of the USSR, and on other issues, and there were 
meetings with representatives of the city authorities. 
  Members of the club regularly give lectures on ecological 
problems. They organize debates on ecological and sociopolitical 
problems in the library of the Construction Worker DK. It was 
proposed to set up a permanently operating seminar (together 
with the International Maritime Fraternity Club). 
  In July 1989 the ETs, the International Maritime Fraternity 
Club, and the Glasnost political club came forward with a call 
to form the Organizing Committee of the Nakhodka Democratic 
Front. The organizing committee included 10 persons, members of 
these clubs and other citizens. 
  In 1989 the ETs had 5 permanent members and about 10 persons 
in support groups. They were chiefly young people--cadets, 
workers, and intelligentsia. The members of the ETs belonged to 
the Nakhodka Nature Protection Society. 
  The ETs has published an information bulletin (one page, 
21-30 copies) and the journal GRAZHDANIN [Citizen] (40-60 pages, 
7 copies) since May 1989. 
  Address: 692900, Maritime Kray, city of Nakhodka, ul. 
Vladivostokskaya, d. 40, kv. 5, Oleg Georgiyevich Bulyndenko. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," vol 1, 
part 2, pp 197-198. 

<H5>    Settlement of Roshchino (Krasnoarmeyskiy Rayon) </H5>
<H3>  Ecology Group of Krasnoarmeyskiy Rayon ["Ekologicheskaya 
gruppa Krasnoarmeyskogo rayona"] </H3>
  It conducts ecological expert studies of AES's and the 
Ussuri 
River basin. It promoted the victory of candidates with 
ecological programs in elections at all levels, from local 
soviets to the RSFSR. 
  Address:692130, Maritime Kray, Krasnoarmeyskiy Rayon, pos. 
Roshchino, tayezhnaya ekspeditsiya, Vladimir N. Zemtsov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Ussuriysk </H5>

<H3>  Public Ecology Commission ["Obshchestvennaya ekologicheskaya 
komissiya"] </H3>
  It collects information on ecological issues. 
  Address: 692500, Maritime Kray, city of Ussuriysk, ul. 
Nekrasova, d. 66, Gorispolkom. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Settlement of Chuguyevka </H5>

<H3>  Debate Club on Ecology Issues ["Diskussionnyy klub po 
voprosam ekologii"] </H3>
  It studies public opinion and conducts ecological expert 
studies of industrial plans. 
  Address: Maritime Kray, community of Chuguyevka, ul. 
50-letiya Oktyabrya, Antonina M. Mezhova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Pskov Oblast </H5>

<H5>  City of Pskov </H5>
<H5>  Greens Movement ["Zelenoye dvizheniye"] </H5>
  It operates in the territory of the oblast. It organizes 
ecological education, study of public opinion, and collection 
and dissemination of ecological information. It participates in 
solving problems of protecting the plant and animal worlds, 
preserving biological diversity, and preserving and developing 
the system of specially protected natural areas and sites. 
  It is a member of the Social-Ecological Alliance (see 
article) and the Greens Movement (see article). 
  Address: 180017, city of Pskov, ul. Stakhanovskaya, d. 4, 
kv. 
39, tel. 2-56-17, Anatoliy V. Verkhozin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecologist ["Ekolog"], Club at PGPI [Pskov State Pedagogical </H5>

Institute] 
  It is chiefly a student organization. Task--discussion of 
ecological problems. 
  Address: 180000, city of Pskov, ul. Sovetskaya, d. 21, PGPI, 
yest. fak., Viktoriya Grigoryeva. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Rostov Oblast </H5>

<H5>  City of Rostov-na-Donu </H5>
<H3>  Children To Save the Earth--Russia ["Deti za spaseniye 
Zemli--Rossiya"] </H3>
  They take actions to defend the environment against 
industrial and agricultural pollution and for preserving peace 
on Earth. Age composition is mixed. They collaborate with 
similar organizations in the United States and with the 
inter-regional youth organization Rainbow ["Raduga"] (see 
article). 
  Address: 344022, city of Rostov-na-Donu, ul. Pushkinskaya, 
d. 
213, kv. 8, tel. 264-46-80, Sergey Vadimovich Berezhnoy. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H5>    World ["Mir"] </H5>
  Youth ecology group, founded in May 1988. 
  Address: city of Rostov-na-Donu, ul. Zhmaylova, d. 25, kv. 
66, Aleksandr Popov. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H3>    Rostov Oblast Ecology Center ["Rostovskiy oblastnoy 
ekologicheskiy tsentr"] (ROETs) </H3>
  It participates in solving problems related to AES's. 
  Address: 344007, city of Rostov-na-Donu, ul. Stanislavskogo, 
d. 114-1, Valeriy Vladimirovich Privalenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Rostov Public Ecology Center ["Rostovskiy obshchestvennyy </H5>

ekologicheskiy tsentr"] 
  It is a member of the Social-Ecological Alliance (see 
article). One of the sections of the ROETs is a collective 
member of the Volgodonsk city public club Democratic 
Perestroyka. In October 1989 they were the initiators and 
participated in formation of the commission for conducting an 
independent, non-departmental social-ecological expert study of 
construction of the Rostov AES. 
  Address: 344034, city of Rostov-na-Donu, ul. Portovaya, d. 
78, kv. 29, tel. 59-45-55, Aleksey M. Pamelov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 157. 

<H5>    Rostov Ecology Center ["Rostovskiy ekologicheskiy tsentr"] </H5>
  It was formed in 1988. The aktiv is 10 persons. It 
collaborates with the Rostov GU. The leader is Demaratskiy. 
Since the summer of 1989 it has belonged to the Don People's 
Front (Rostov-na-Donu). The Rostov Ecology Center and the Green 
Wave social-ecological group of the city of Volgodonsk in Rostov 
Oblast (see article) were the first to demand an independent 
social-ecological expert study of construction of the Rostov AES 
involving specialists from the USSR Academy of Sciences, public 
representatives, and independent foreign ecologists. 
  On 3 September 1989 in Theater Square, the center, together 
with the Don People's Front, held an unapproved rally in 
connection with construction of the Rostov AES, formation of the 
front, and preparations for elections (300-400 participants). 
The organizers of the rally received administrative fines of 
R50-80 (see the oblast newspaper MOLOT). 
  On 17 May 1990 they participated in a rally that adopted a 
resolution against continuing construction of the Rostov AES and 
threatening to hold a warning strike. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Volgodonsk," EKSPRESS-KHRONIKA, 
No 42 (115) 15 October 1989, p 5; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 1, pp 133-134. 

<H3>    North Caucasus Branch of the USSR Ecological Foundation 
["Severokavkazskoye otdeleniye Ekologicheskogo fonda SSSR"] (see 
article) </H3>
  The chairman of the branch is Boris G. Rezhabek, director of 
the North Caucasus Research Center which works on the ecology of 
culture, among other subjects. 
  Address: 344091, city of Rostov-na-Donu, pr. 
Kommunisticheskiy, d. 28/1, kv. 28, tel. 22-38-55 (work), 
22-42-91 (home), Boris G. Rezhabek. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Volgodonsk </H5>

<H5>  Green Wave ["Zelenaya volna"] </H5>
  Social-ecological group (movement). It was founded in June 
1988. Total members: 12-15, age: 25-37 years. Technical 
intelligentsia, teachers, college instructors, and workers. 
  It fought against construction of the Rostov AES and for 
shutting down the Volgodonsk Chemical Plant. It gathered 
information about the ecological consequences of different types 
of production (including information on harmful discharges) in 
the oblast and published the material gathered, in fliers at 
first. 
  ZV and the Rostov Ecology Center (see article) demanded an 
independent social-ecological expert study of construction of 
the Rostov AES involving specialists from the USSR Academy of 
Sciences, public representatives, and independent foreign 
ecologists. 
  On 22 June 1988 the group prepared the first mandate for 
people's deputies from Volgodonsk and the leaders of the city 
and the oblast concerning improving the ecological state of the 
city environment. The text of the mandate was given to the 
press. The group made these mandates regular. 
  ZV members participate in holiday marches on 7 November (in 
1988 for the first time) carrying ecological slogans. 
  They took part in the round table discussion of AES problems 
that was held in Rostov-na-Donu in November 1988, a few days 
after the march. Group members spoke over the Atommash Plant 
radio, and published fliers. 
  The group was criticized in the local and oblast press and 
twice lost their premises. In October 1989 the administration of 
the school where ZV activist Yelena Malaya worked notified her 
that she was fired. The city authorities refused to review this 
matter. 
  They participated in preparation of the sections devoted to 
questions of ecology in the programs of people's deputy 
candidates in each election. They work with the deputy corps to 
achieve joint solutions to the various questions of protecting 
nature in the rayon. 
  They participated in forming the regional citizens committee 
called "For Closing the Rostov Atomic Plant," which organized 
the rally in Volgodonsk on 2 June 1990 under the slogan, "We are 
defending our children" (about 10,000 persons from Volgodonsk, 
Dubovka, Tsimlyansk, Novocherkassk, Semikarakorsk, Volgograd, 
and Rostov-na-Donu). A resolution was adopted demanding an 
immediate stop to construction of the AES. 
  ZV has been a collective member of the sociopolitical club 
Democratic Perestroyka since 14 November 1988, the date of its 
founding meeting. One of the leaders of ZV, A. Golubenko, 
belongs to the Confederation of Anarcho-Syndicalists. 
Representatives of Green Wave participated in the founding 
congress of the Social-Ecological Alliance (see article) in 
December 1988 and ZV has been a collective member of the SES 
since that time. 
  Addresses: 347340, Rostov Oblast, city of Volgodonsk, ul. 
Koshevogo, d. 13, kv. 101, tel 9-49-72, S. V. Skripnik; ul. 
Koroleva, d. 10, kv. 78; ul. Molodezhnaya, d. 15, kv. 95, tel. 
9-49-72, Valeriy Kibalnik; ul. Gorkogo, d. 182, kv. 134, tel. 
9-14-35, Aleksandr Ivanovich Golubenko (Democratic Perestroyka); 
tel. 5-66-67, Nikolay Petrovich Lukyanov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Volgodonsk," 
EKSPRESS-KHRONIKA, No 42 (115), 15 October 1989, p 5; 
  -  :Rossiya: 
partii...," vol 1, part 2, p 157. 

<H5>    City of Novocherkassk </H5>
<H5>  Green Don ["Zelenyy Don"] </H5>
  An independent ecological movement. It formed in 1988 and 
was 
registered on 14 March 1990 by the gorispolkom. 
  Goal: preserve and restore the natural and cultural riches 
of 
the Don region. 
  Forms of work: rallies, marches, independent expert studies, 
collection of information about ecological stress points, and 
"exposure of the predatory activities of departments and 
mercenary scientists." 
  They organized rallies on 5 August 1989 and 26 April 1990 
dedicated to the consequences of the Chernobyl accident with 
collection of money for the Chernobyl telephone marathon fund 
and to the need to stop construction of the Rostov AES. They 
organized collection of signatures on a demand to conduct an 
official expert study of the plan of the AES. ZD has been doing 
independent expert studies since the fall of 1989. 
  Green Don participates in the fight against expanding the 
ecologically dangerous production of butane-diol at the 
Novocherkassk Synthethic Products Plant. 
  ZD maintains regular contact with the city authorities, and 
the heads of ecologically dangerous production facilities report 
on their activity periodically to meetings of movement 
participants. 
  In the election campaign for people's deputies, they got 
several people onto the city and oblast soviets. 
  The aktiv is up to 50 persons. Membership is individual and 
collective. Social-occupational 
composition--engineering-technical personnel, teachers, 
students, office workers, and others. There are no dues. 
  The primary work is done by territorial cells. The movement 
has formed a Green Patrol group of schoolchildren and the 
creative association Don, which works to revive the traditions 
of bygone days in the Don region. 
  The chairman of the movement is V. V. Lagutov. They have no 
press organ, but publish articles in the large local newspapers 
and put out fliers and "ecoflashes" for internal use by 
activists prepared from information received from the public. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," vol 1, 
part 2, p 203. 

<H5>    Ryazan Oblast </H5>
<H5>  City of Ryazan </H5>
<H5>  Fatherland ["Otechestvo"] </H5>
  This is a club with an ecological-cultural orientation. It 
was formed in early 1987 at the Red Banner DK. It is registered 
at the oblast All-Union Society for the Protection of Monuments 
of History and Culture (VOOPIK) (see article). On 3 January 1988 
a program and by-laws were adopted which envisioned dues and 
individual membership. In 1989 membership was 24. Social 
composition: college and secondary students, workers. There is a 
club council (10 persons), and club secretary is M. A. Kachayeva. 
  Forms of work: regional studies excursions, evening meetings 
on special historical topics (assemblies), volunteer work days 
to restore monuments, and the like. 
  They are fighting actively against destruction of the 
floodplain (in late 1987 a draft Master Plan for Ryazan was 
approved which envisioned construction of a northern bypass 
highway on the floodplain in the zone of a protected natural 
landscape and the preserve land of the city kremlin [cathedrals 
of the 17th-19th centuries], development of a river freight 
port, and installation of a pressurized sewer collector system). 
In addition, intensive sand quarrying is going on for 
construction needs on Bolshoy Borkovskiy Island in the Oka 
floodplain, where there are remnants of an archeological complex 
of settlements (beginning from the 10th century B. C.). For this 
reason the club has difficult relations with its founding 
organization and the oblast leadership. 
  They are working in cooperation with the 5th of June group 
(see article). 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 211. 

<H5>    5th of June ["5-ye iyunya"] </H5>
  This is an ecology group. It was formed on 5 June 1988. The 
initiative group had existed since February 1988. In 1989 the 
group had 15 members and an aktiv of 6. The leader is Aleksandr 
Gavrilov. 
  Forms of work: rallies, picketing, collection of signatures, 
and participation in election campaigns. 
  They were persecuted by the authorities. 
  On 5 June 1988, on Environmental Defense Day, they took part 
in a rally at the Ryazan Kremlin which was organized by the 
Green Squad in connection with the ecological situation in the 
city and the irrational plan for installing the city sewer 
collector system (about 400 participants). On 24 June 1988 they 
participated in the second ecology rally organized by the Green 
Squad (800 persons). 
  From 18 June through 28 August 1988, they organized weekly 
information posts at the city department store. The displays at 
the post offered ecological information and political material 
received from Moscow groups. More than 15,000 signatures against 
construction of the city collector system were gathered. 
  On 15 December 1988 at the Oil Workers DK, they, along with 
ecologists from other groups, met the city authorities about the 
grave ecological situation, which had been greatly aggravated by 
the activity of the Italian Concceris Gigolo Company, which 
built a new leather plant in Ryazan. Mutual understanding was 
not reached. The company representatives who were present at the 
DK did not take part in the debate. 
  They participated in the election campaigns of 1989 and 1990 
as part of the Voters Club. 
  The group joined the Federation of Socialist Public Clubs 
(FSOK). It held to syndicalist-anarchist orientation. 
  In June 1988 they began publishing the almanac-reporter 
called "5-YE IUNYA" [5th of June] (20 pages, 10 copies). 
  The group ceased to exist in 1990. 
  Addresses: 390020, city of Ryazan, ul. Konyayeva, d. 169, 
tel. 53-96-41, Aleksandr Lavrukhin, Marina Kachayeva; 390023, 
city of Ryazan, ul. Lenina, d. 5a, kv. 11, tel. l77-40-04, 
Marina Kachayeva. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 211. 

<H3>    Ecology Group of the Settlement of Stroitel 
["Ekologicheskaya gruppa pos. Stroitel"] </H3>
  It works on issues of industrial pollution. 
  Address: 390017, city of Ryazan, ul. Kachevskaya, d. 34, kv. 
129, Tamara Alekseyevna Pushnikova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Section of the Ryazan Branch of the USSR Geographic </H5>

Society ["Ekologicheskaya sektsiya pri Ryazanskom otdelenii 
Geograficheskogo obshchestva SSSR"] 
  It studies the ecological situation in the country and 
especially in the oblast. 
  Address: 390000, city of Ryazan, pochtamt, a/ya 146, Yuriy 
Aleksandrovich Karelin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ekos Ecology Club ["Ekologicheskiy klub 'Ekos'"] </H5>

  It conducts debates on ecological issues. 
  Address: 390023, city of Ryazan, ul. Uritskogo, d. 6/106, 
kv. 
40, Lyudmila Mikhaylovna Manzhos. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Kasimov </H5>

<H3>  Ecoclub of the Kasimov DOSAAF Raykom ["Ekoklub pri 
Kasimovskom Raykome DOSAAF"] </H3>
  It acts in favor of a healthy way of life and studies the 
ecological situation in the region. 
  Address: 391330, Ryazan Oblast, city of Kasimov, ul. 
Sovetskaya, d. 23, DOSAAF, O. M. Semenov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Mikhaylov </H5>

<H3>  Ecology Club of Mikhaylovskiy Rayon ["Ekologicheskiy klub 
Mikhaylovskogo rayona"] </H3>
  It organizes ecological education. 
  Address: 391710, Ryazan Oblast, city of Mikhaylov, ul. 50 
let 
VLKCM, d. 24, kv. 13, Leonid S. Rodionov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Samara Oblast </H5>

<H5>  City of Samara </H5>
<H5>  Alternative ["Alternativa"] </H5>
  This is an ecological-political club. Involved in ecological 
and political activity; announced its formation in July 1988 at 
the first People's Front rally; registered in October of the 
same year at the gorispolkom. About 30 people. 
  In theory develops the idea of the "third path" (not 
capitalism and not state socialism); this presupposes the 
development of self-government, nonindustrial forms of living, 
and destatization. 
  The task is to organize permanent ecological monitoring of 
the work of installations which are potentially dangerous to 
nature and to develop the population's ecological sophistication. 
  Forms of work are lectures and propaganda, rallies, 
picketing, and protest camps. 
  Involved in commercial activity and the profits from it go 
for ecology programs. 
  On 1 May 1989 they marched in a separate column along with 
representatives of the People's Front, the Samara 
social-democratic club, and others (in all about 60 people); 
some of their slogans were directed against the CPSU. 
  In April 1989 (the anniversary of the accident at the 
Chernobyl AES) organized an authorized march in the city. 
  The club opposed the construction of a garbage burning 
plant. 
Supported the Social-Ecological Club's struggle against 
construction of the Volga-Chogray Canal, and other things. 
  The club participated in the conferences of the 
Social-Ecological Alliance (see article) and the Greens Movement 
(see article) in which preparations for creating the Greens 
Party (see article) began. Alternative and the Samara Greens 
Alliance became sponsors and initiators of the All-Union 
Ecological Conference held in Kuybyshev (Samara) on 24 April 
1989 (attending were representatives of ecology organizations 
from roughly 15 cities: Moscow, Arkhangelsk, Lipetsk, 
Chelyabinsk, Almaty, and others). One of the results of the 
conference was the organization of the Movement To Create a 
Greens Party. The conference showed the crisis in the purely 
ecological movement and the rapid politicization of ecology 
groups. 
  Participated in organizing picketing of the plant to destroy 
chemical weapons in the city of Chapayevsk in Kuybyshev (Samara) 
Oblast: thousands of leaflets, picketing, rallies, 
demonstrations, and two tent protest camps around the plant from 
5 August through 10 September 1989 in which 25 members of the 
club and another 200-300 people took part. During the constant 
blockade the movement grew to 7,000 people. On 10 September the 
directive of N. I. Ryzhkov (at that time the prime minister of 
the USSR) changing the plant's specialization into an 
educational center was published and afterwards the picketing 
stopped. 
  Puts out an information leaflet. Together with the Greens 
Party publishes the journal TRETIY PUT [Third Path]. 
  Member of the Social-Ecological Alliance (see article). Part 
of the People's Front of Samara (Kuybyshev). In November 1989 
the authorities accused the club of violating its charter 
activity in connection with involvement in business and denied 
registration; this caused a sharp internal conflict and 
dissolution of the club. Some of the members continued public 
activity in the Greens Party and the "Samarskaya Luka" Club (see 
article). 
  Address: 443084, city of Samara, ul. Voronezhskaya, d. 190. 
kv. 15, tel. 53-00-77, 53-00-22, Sergey G. Krivov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Zelenyye v SSSR. Krupneyshiye...," 
op. cit., pp 11-13; 
  -  PANORAMA, No 4, 1989; 
  -  "Rossiya: 
partii...," op. cit., vol 1, part 2, p 211; 
  -  TRETIY PUT, No 6-9, 
1989, p 12. 

<H5>    "Samarskaya luka" [Samara Bend] </H5>
  Ecology group. Favors improvement of the environment in the 
city, above all preservation of Samarskaya Luka Park, which is 
being destroyed by open-cut mining. 
  Address: city of Samara, tel. 52-50-52, Vladimir 
Aleksandrovich Tuchin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Samara Greens Alliance ["Samarskiy soyuz zelenykh"] </H5>

  Its task is to create a Greens Party. Involved in 
social-political activity. Conducts rallies in defense of the 
environment. Participates in solving problems of protecting the 
plant and animal worlds and preserving and developing the system 
of specially protected natural areas and 
historical-architectural monuments and problems related to the 
use of atomic energy and construction and operation of 
hydroengineering structures. 
  Collects ecological information, studies public opinion, and 
engages in ecological education. 
  After S. Fomichev moved to the city of Dzerzhinsk, in 
reality 
ceased to exist. 
  Member of the Social-Ecological Alliance (see article) and 
the Greens Movement (see article). 
  Address: 443002, city of Samara, ul. Iskrovskaya, d. 1, kv. 
14, Sergey Rudolfovich Fomichev; tel. 25-69-59, Dmitriy 
Vasilyevich Minayev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Nature Protection Council ["Sovet po okhrane prirody"] </H5>

  Created under the Samara All-Union Komsomol Obkom. 
Participates in solving problems of protecting the plant and 
animal worlds, preserving biological diversity, and preserving 
and developing the system of specially protected natural areas 
and sites and problems related to industrial pollution. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 443125, city of Samara, ul. Novo-Sadovaya, d. 381, 
kv. 85, tel. 32-48-26, 32-33-84, Aleksandr V. Fedorov 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Novokuybyshevsk </H5>

<H5>  Resonance ["Rezonanc"], Ecological-Political Club </H5>
  Opposed the excessive concentration of ecologically harmful 
enterprises in the city and supported the establishment of green 
planted areas. Politicized. Participated in the election 
campaign (four city soviet deputies). 
  Member of the Social-Ecological Alliance (see article). In 
1990 transformed into the Novokuybyshevsk Greens Party. Part of 
the Russian Greens Party (see article) and the Confederation of 
Anarcho-Syndicalists. 
  Address: 446205, Samara Oblast, city of Novokuybyshevsk, ul. 
Suvorova, d. 156, kv. 35, Viktor I. Lapkovskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Tolyatti </H5>

<H3>  Tolyatti Social-Ecological Alliance ["Tolyattinskiy 
socialno-ekologicheskiy soyuz"] </H3>
  Member of the Social-Ecological Alliance (see article). 
  Address: 445046, Samara Oblast, city of Tolyatti, ul. Lizy 
Chaykinoy, d. 23, kv. 179, tel. 26-13-13, Aleksey I. Kiryushin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Otradnyy </H5>

<H3>  Salvation ["Spaseniye"], Ecological-Political Society 
["Ekologo-politicheskoye obshchestvo"] (EPOS) </H3>
  Participates in solving problems of protecting the plant and 
animal worlds, preserving biological diversity, and establishing 
and preserving natural areas and monuments of culture. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 44630, Samara Oblast, city of Otradnyy, ul. 
Pionerskaya, d. 30a, kv. 57, tel. 2-33-92, 2-41-12, Vyacheslav 
A. Repin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Chapayevsk </H5>

<H3>  Position ["Pozitsiya"], Ecological-Political Club 
[Ekologichesko-politicheskiy klub"] </H3>
  Fights against construction of a military chemical plant to 
destroy toxic chemical weapons in Chapayevsk and demands it be 
moved outside the city limits and that an independent ecological 
expert study be done. Participated in the blockade of this 
enterprise in August-September 1989. As a result the 
specialization of the plant was changed. 
  The club is officially registered. 
  Address: 446100, Samara Oblast, city of Chapayevsk-5, ul. K. 
Libknekhta, d. 210, Vladimir A. Kuzmin. 
<H5>  Saratov Oblast </H5>
<H5>  City of Saratov </H5>
<H3>  Saratov Affiliate of the Alternative Club ["Saratovskiy 
filial kluba `Alternativa'"] </H3>
  Founded in 1989 in order to direct the public's attention to 
ecological problems. 
  Organizes ecological education, the study of public opinion, 
and collection and dissemination of ecological information. 
Participates in solving problems related to the use of nuclear 
energy and construction and operation of AES's and 
hydroengineering structures. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 410600, city of Saratov, ul. 20 let VLKSM, d. 84, 
kv. 3-a, Olga Nikolayevna Pitsunova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecologist ["Ekolog"], Club </H5>

  Social composition: for the most part workers in science and 
VUZ instructors. 
  Address: 410600, city of Saratov, pr. Lenina, d. 94, ISEP 
APK 
AN SSSR, tel. 25-52-01, Nikolay S. Makarevich. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Balakovo </H5>

<H5>  Ecocentury ["Ekovek"] </H5>
  City organization. Chairman is A. F. Gavrilin. 
  Protests against the Balakovo AES. 
  EK is a participant in the Greens Movement (see article). 
  Address: 413800, Saratov Oblast, city of Balakovo, ul. 
Naberezhnaya Leonova, 66-a, kv. 56, tel. 50-09, Aleksandr 
Fedorovich Gavrilin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Sakhalin Oblast </H5>

<H5>  Kuril Islands </H5>
<H5>  Frigate ["Fregat"], Society </H5>
  Goal is to create the Kuril Islands Association: a regional 
alliance which unites people with different convictions and 
views of the past and the future of the archipelago. 
  Membership in the society and the future association is 
secured only by practical actions. One of them is organizing 
provincial parks to monitor the influx of tourists, put up a 
barrier to plunderers of nature, keep its monuments under 
protection, and organize and monitor ecology paths. The parks' 
activity will be based on cost accounting and a large part of 
the monetary receipts will remain in the rayon's budget. 
  The society also supports demilitarization of the Kurils, 
which will help preserve and improve the natural environment. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Smorodkin,, S., "House in the 
Middle of the Ocean," SPASENIYE, No 8, August 1991, p 3. 

<H5>    Settlement of Smirnykh </H5>
<H5>  Initiative Ecogroup ["Initsiativnaya ekogruppa"] </H5>
  Studies questions of the impact of environmental pollution 
on 
the population's health. 
  Address: 693000, Sakhalinsk Oblast, settlement of Smirnykh, 
ul. Gorkogo, d. 11, S. A. Butyrin. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Yuzhno-Sakhalinsk </H5>

<H3>  Democratic Movement for Perestroyka ["Demokraticheskoye 
dvizheniye za perestroyku"] (DDP), Ecology Section </H3>
  Social composition includes intelligentsia and workers. In 
late May 1988 conducted a rally in the settlement of Tymovskoye 
in connection with the ecological crisis in the region. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, p 132. 

<H5>    Sakhalin Greens Party ["Partiya zelenykh Sakhalin"] </H5>
  Formed in the summer of 1991. Supports the preservation of 
the island's natural environment and self-government and opposes 
unrestrained invasion of foreign capital and the transfer of the 
Kuril Islands to Japan. Aligned with the Russian Greens Party 
(see article). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    North Ossetia </H5>

<H5>  City of Vladikavkaz </H5>
<H5>  Cradle ["Kolybel"], Ecological Society </H5>
  Conducts debates on ecological and philosophical themes. 
  Address: 362007, North Ossetia SSR, city of Vladikavkaz, ul. 
Pushkinskaya, d. 5, korp. 11, Gennadiy F. Shmatonov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Smolensk Oblast </H5>

<H5>  City of Smolensk </H5>
<H3>  Greens Movement of the City of Smolensk ["Zelenoye 
dzhizheniye g. Smolensk"] </H3>
  Organizes ecological education. 
  Address: 214000, city of Smolensk, ul. Kommunisticheskaya, 
a/ya 87; tel. 3-68-54, Viktor Petrovich Khonin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Tree Nursery ["Lesopitomnik"], Initiative Group </H5>

  Goal is to protect the environment, especially areas planted 
with trees. 
  Address: 214000, city of Smolensk, ul. P. Alekseyeva, 
16-134, 
Olga Vladimirovna Zlatogorskaya. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Yartsevo </H5>

<H5>  Ekos Ecological Group ["Ekologicheskaya gruppa Ekos"] </H5>
  Member of the Social-Ecological Alliance (see article). 
  Address: 215810, Smolensk Oblast, city of Yartsevo, ul. 
Sovetskaya, d. 27, tel. 4-26-12, 4-14-04, 4-27-92, Yevgeniy 
Stremovskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Stavropol Kray </H5>

<H5>  City of Stavropol </H5>
<H5>  Ecology ["Ekologiya"], City Debate Club </H5>
  Emerged on the base of the pedagogical institute. Studies 
questions of the introduction of "clean" technologies and 
alternative sources of energy. 
  Address: 355000, city of Stavropol, Pedagogical Institute, 
Vitaliy Stimanovich Igropulo. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Budennovsk </H5>

<H3>  Eko Ecology Club (or Ecology and Resources Center) 
["Ekologicheskiy klub `Eko' (Tsentr Ekologii i resursov)"] </H3>
  Primarily a children's organization supporting ecological 
education. 
  Address: 357920, Stavropol Kray, city of Budennovsk, ul. 
Mira, d. 123, Gorstantsiya yunnatov, Boris V. Bolshakov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Pyatigorsk </H5>

<H5>  To Be ["Byt"], Ecology Club at the Caucasus Mineral Waters </H5>
  Organizes monitoring of preservation of the environment, the 
quality of food products and consumer goods, and the 
population's health. Involved in developing alternative plans, 
projects, and technologies. 
  Participates in solving problems of protecting the plant and 
animal worlds, preserving biological diversity, and preserving 
and developing the system of specially protected natural areas 
and sites and problems related to the use of nuclear energy and 
construction of AES's. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 375500, Stavropol Kray, city of Pyatigorsk, ul. 
Degtyareva, d. 36, kv. 2, A. A. Shcherbakov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Steps ["Stupeni"], Studio Theater </H5>

  Puts on plays about ecology. 
  Address: 357500, Stavropol Kray, city of Pyatigorsk, 
glavpochtampt, a/ya 163. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Tambov Oblast </H5>

<H5>  City of Tambov </H5>
<H3>  Ecology Group of Memorial (Greens Movement) 
["Ekologicheskaya gruppa `Memoriala' (Zelenoye dvizheniye)"] </H3>
  Founded on 18 March 1989. Total number of members 154, aktiv 
of 4 people. Sets ecological, political, and historical-cultural 
tasks for itself. 
  At the election of people's deputies of the USSR in 1989, 
supported the candidate Davituliani (now a member of the SDPR 
[Social-Democratic Workers Party] governing board). The group is 
also involved in protecting monuments. The aktiv is part of the 
Russian Greens Party (see article). 
  Subjected to persecution by the authorities in August 1991. 
  Address: 392032, city of Tambov, bul. Entuziastov, d. 32, 
kv. 
47, Lyudmila Mikhaylovna Spiridonova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Tatarstan </H5>

<H5>  City of Kazan </H5>
<H3>  Antinuclear Movement of Tatarstan ["Antiyadernoye dvizheniye 
Tatarstana"] </H3>
  Created with the participation of the Ecology Club. Opposes 
construction of the Tatar AES and supports a gradual reduction 
in atomic power. Works on the problem of radioactive wastes. 
  Address: 420034, Republic of Tatarstan, city of Kazan, ul. 
Energetikov, d. 3, kv. 53, tel. 53-21-04, Albert Faripovich 
Garapov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Green World ["Zelenyy mir"], Ecology Club </H5>

  Issues protests against chemical enterprises and AES's. 
  Founded in April 1987. Member of the Social-Ecological 
Alliance (see article). 
  Address: 420083, Republic of Tatarstan, city of Kazan, ul. 
Novo-Azinskaya, d. 10, kv. 80, tel. 76-15-28, Vladimir A. 
Shushkov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Initiative Center of the People's Front ["Initsiativnyy </H5>

tsentr Narodnogo fronta"] 
  Created in July 1988. About 500 people and an aktiv of 60 
people. 
  On 31 August 1988 held a rally against the construction of 
the Tatar AES and on the problems of social justice (about 300 
participants). Gathered 20,000 signatures against the 
construction of the Tatar AES. 
  Has a branch in the city of Naberezhnyye Chelny. Held 
rallies 
against the chemical plant. More than 100,000 signatures 
gathered. VESTNIK NF TATARSKOY ASSR published. 
  Cooperated with Ekoklub (see article). 
  Address: Republic of Tatarstan, city of Kazan, tel. 54-01-30 
(city of Kazan), Aleksandr Sergeyevich Kotsey. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, pp 139-140. 

<H5>    Ants ["Muravyi"], School Movement </H5>
  Engages in ecological education of children, conducts 
actions 
against the pollution of forests, and participates in the 
Greenpeace International children's project. 
  Address: 420141, Republic of Tatarstan, city of Kazan, ul. 
Zavoyskogo, d. 12, kv. 120, Aleksandr Grigoryevich Dorofeyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Oasis ["Oazis"], Ecology Club </H5>

  Founded in 1988. Total number of members--100. 
  Trains specialists on the country's ecological problems. 
Cooperates with American ecologists and exchanges specialists 
with Eko-School. 
  Address: 4200110, Republic of Tatarstan, city of Kazan, ul. 
Zorge, d. 77, kv. 117, Yuliya V. Antipova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Club ["Ekologicheskiy klub"] ("Eko-klub") </H5>

  Organizes round table debates and marches and publishes 
articles on ecological subjects in the periodical press. 
  Aktiv consists of 30 people; the social composition is 
intelligentsia, including writers and journalists. 
  On 18 February 1990 participated in the rally, attended by 
many thousands, that demanded the resignation of the CPSU Obkom; 
the organizer of the rally was the People's Front of the Tatar 
ASSR (Tatarstan). 
  Cooperates with "Green World," city of Kazan (see article). 
  Address: 420034, Republic of Tatarstan, city of Kazan, ul. 
Energetikov, d. 3, kv. 53, tel. 53-21-04, Albert Faripovich 
Garapov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, p 140. 

<H5>    Tver Oblast </H5>
<H5>  City of Tver (Kalinin) </H5>
<H5>  Social Initiative ["Sotsialnaya initsiativa"] </H5>
  Created in May 1988. Membership--60 people. Supports 
democratization of society and solution of ecological problems. 
Puts out the journal KOLOKOL. Gathered 10,000 signatures against 
the Rzhevsk Hydropower System. Member of the Greens Movement 
(see article). 
  Address: 170001, city of Tver, ul. Proletarskaya, d. 20, 
Leonid Yuryevich Daryushin; 170005, city of Tver, ul. 
Musorgskogo, d. 6, korp. 4, kv. 38, tel. 3-66-99, Georgiy 
Nikolayevich Belodurov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Social Justice ["Sotsialnaya spravedlivost"] </H5>

  Group formed in May 1988. 
  Initially there were about 20 people and in 1989--50-55 
people; average age--20-30 years; intelligentsia. Management 
organ--committee (six people). A new version of the program and 
the by-laws was adopted in February 1989. 
  Goals are the people's greater well-being, democratization, 
and improvement of ecological conditions. 
  Gathered abut 10,000 signatures and held a rally (about 500 
participants) against the plan for building the Rzhevsk 
Hydropower System. Took an active part in the ecology festival 
organized in the city in late June 1989 by the Committee To Save 
the Volga (created on the initiative of SOVETSKAYA ROSSIYA and 
oblast newspapers), and held a conference on ecological 
questions. 
  During the First Congress of People's Deputies of the USSR 
participated in street debates; rallies were prohibited. 
  The organization maintained ties with ecology groups in 
other 
cities. Joined the Tver Association of Informal groups (starting 
in February 1989). Representatives of the group participated in 
the founding conference of the Greens Movement on 27-28 February 
1989. 
  Has been publishing the journal TVERSKOY KOLOKOL (editor--S. 
Vinogradov; epigraph: "The Socialist Society in Danger"; four 
issues came out in 1989; print run of the first--50 copies, and 
of the fourth--300 copies; size--42-45 pages) since February 
1989. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 2, p 218. 

<H5>    Ecological Initiative ["Ekologicheskaya initsiativa"] </H5>
  The task is to preserve the natural and cultural wealth of 
Tver Oblast. Protests against the Kalinin AES. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 17005, city of Tver, ul. Musorgskogo, d. 6, korp. 
4, 
kv. 38, tel. 30-66-99, tel. 1-26-48, Georgiy N. Belodurov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Ostashkov </H5>

<H3>  Ostashkov Branch of the Social-Ecological Alliance 
["Ostashkovskoye otdeleniye Sotsialno-ekologicheskogo soyuza"] 
(SES) </H3>
  Supports the preservation of the purity of Lake Seliger and 
toughening of control over the military enterprise Zvezda, the 
tannery in Ostashkov, and the cutting of forest plantations. 
Repeatedly prevented the cutting of high-grade forest. Involved 
in ecological education. 
  Put several deputies into the city soviet (the Greens 
faction). Linked with the Russian Greens Party (see article). 
  Member of the Social-Ecological Alliance (see article). 
  Address: 172750, Tver Oblast, city of Ostashkov, ul. 
Rabochaya, d. 42, korp. 45, kv. 36, tel. 2-07-31, Oleg I. 
Yegorov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Tomsk Oblast </H5>

<H5>  City of Tomsk </H5>
<H5>  Action ["Deystviye"] </H5>
  Created in April 1989 in the City of Tomsk-7. More than 100 
participants. Has a coordinating council and a sectional 
structure. There is an ecology section. Opposes the BVK plant 
and the Krapivenskiy Reservoir. Organized ecology rallies (up to 
7,000 people). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Public Committee To Save the Tom River ["Obshchestvennyy </H5>

komitet po spaseniyu reki Tomi"] 
  Formed in early 1989 and separated off from the Ecological 
Initiative Movement (see article). Coordinating council consists 
of 21 people. 
  In the summer of 1989 organized pickets at the Krapivenskiy 
Reservoir dam, from which water was to be taken for the coal 
pipeline from the Kuznets Basin to the European part of the 
USSR. The construction project was frozen by USSR Council of 
Ministers Decision No 13/3 of 18 July. 
  The founding conference of the Regional Public Committee To 
Save the Tom River was held on 23 October 1989. Representatives 
of the ecological community of Tomsk and Kemerovo oblasts and 
the cities of Novokuznetsk, Leninsk-Kuznetskiy, and Yurga 
participated in the conference's work. The catastrophic 
condition of the Tom River was discussed. The question was 
raised of the fate of the Shors ethnic group in connection with 
the industrial development of Gornaya Shoria. 
  There is an information bank on the pollution of the Tom 
River. The "Declaration on Defense of Sources of Rivers" was 
adopted. Linked with workers of the Kuzbass committees. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 219. 

<H5>    Siberia ["Sibir"], Association </H5>
  Coordinates the work of the ecology groups of Siberia. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 636108, city of Tomsk, ul. Mira, d. 1, kv. 29, tel. 
1-07-75, Oleg Kotikov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecological Initiative ["Ekologicheskaya initsiativa"] </H5>

  The former sixth section of the All-Russian Nature 
Protection 
Society (see article). Formed in April 1988. Has by-laws. 
Membership is individual. Total number of members in 1989 was 
about 50 and in 1991--70-100; the aktiv in 1989 consisted of 
about 20 people, in 1991--30-40, and the coordinating council 
(elected at general assemblies)--10. 
  The chairman is A. Grishin. Among the activists are O. 
Kotikov and Z. Chernysheva. 
  The movement's tasks are: to provide expert studies of 
industrial projects, to observe radioactive discharges in the 
region, to defend the rights and health of consumers, to fight 
against the production of BVI [extension unknown] and against 
plans for building a BVK plant, and to provide ecological 
education. 
  Forms of work are rallies, picketing, gathering of 
signatures, and debates. 
  The movement conducts yearly rallies with the participation 
of 1,000-1,500 people: on 1 June 1988 an ecology rally in front 
of the Palace of Pioneers building (1,500 participants) and on 
14 October a rally in the same place against the pollution of 
the Tom River (1,000-1,200 participants). In November movement 
activists held debates on problems of protecting the health of 
children. 
  In 1989 as a result of the movement's activity, construction 
of the Krapivinskiy Hydropower System and the BVK plant were 
stopped and attention was turned to the problem of the Tomsk-7 
atomic enterprises. A regular, constructive dialogue was set up 
with the city's leadership in developing city and oblast ecology 
programs. 
  Participated in elections. Separating off from the movement 
and becoming independent were the Consumers Club in early 1989, 
the Public Committee To Save the Tomi River (see article) in 
October 1989, and the Ecology Club in March 1990. 
  Member of the Social-Ecological Alliance (see article). 
  Meetings were first held in premises rented by the local 
branch of the Nature Protection Society, and then began to be 
held in premises offered by the local branch of the Writers 
Union. 
  Address: 634055, city of Tomsk, ul. 30-letiya Pobedy, d. 9, 
kv. 47, tel. 1-84-74, 25-84-74, 25-86-71, Anatoliy Ivanovich 
Grishin; 634050, city of Tomsk, pr. Lenina, d. 101, House of 
Creative Organizations, writers organization. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 220. 

<H5>    Tuva </H5>
<H5>  City of Kyzyl </H5>
<H3>  Tuva Republic VOOP Council ["Tuvinskiy respublikanskiy sovet 
VOOP] </H3>
  The goal is to protect nature in the republic and to use its 
resources rationally. 
  In 1990 along with the Tuva ASSR State Committee founded the 
monthly bulletin EKOLOGICHESKIY VESTNIK. 
  Address: Republic of Tuva, city of Kyzyl, ul. Moskovskaya, 
d. 
2, tel. 3-22-1, Oleg Ivanovich Gavrilov, editor of the bulletin. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Business Card," ZELENYY MIR, No 
9-10, 1991, p 11. 

<H5>    EKOLOGICHESKIY VESTNIK [Ecology Herald] </H5>
  Monthly four-page bulletin. Its task is to tell about nature 
protection and rational use of its resources. 
  The all-Union NEDELYA format. Print run--2,000 copies. 
  The editorial board has two members. The editor is Oleg 
Ivanovich Gavrilov, journalist and professional hunter. 
  Address: Republic of Tuva, city of Kyzyl, ul. Moskovskaya, 
d. 
2, tel. 3-22-16. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Business Card," ZELENYY MIR, No 
9-10, 1991, p 11. 

<H5>    Ecology Club ["Ekologicheskiy klub"] ("Ekoklub") </H5>
  Member of the Greens Movement (see article). 
  Address: 667010,, Republic of Tuva, city of Kyzyl, ul. 
Lozhanchona, d. 40, kv. 70, Tamara Anatolyevna Suge-Maadyr. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    Tula Oblast </H5>
<H5>  City of Tula </H5>
<H3>  Tula Oblast Youth Ecological Alliance ["Tulskiy oblast 
Molodezhnyy ekologicheskiy soyuz"] </H3>
  Provides monitoring of preservation of the environment, the 
quality of food products and consumer goods, and public health. 
Participates in solving problems of preserving forests. Develops 
alternative plans, projects, and technologies. Organizes 
ecological education, the study of public opinion, and the 
gathering and dissemination of ecological information. 
  Involved in social-political activity (participation in 
elections and so forth). 
  Member of the DOP Movement (see article). 
  Address: 300008, city of Tula, ul. Zhavoronkova, d. 1, kv. 
15, tel. 25-37-60, Mikhail Ivanovich Budenkov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Aleksin </H5>

<H5>  Greens Association ["Assotsiatsiya `Zelenykh'"] </H5>
  Task: to solve local ecological problems. Provides 
monitoring 
of the preservation of the environment, the quality of food 
products and consumer goods, and public health. Organizes 
ecological education, the study of public opinion, and the 
gathering and dissemination of ecological information. 
  Involved in social-political activity (participation in 
elections and so forth). 
  Address: 301340, Tula Oblast, city of Aleksin, ul. 50 let 
Oktyabrya, d. 21, kv. 13, tel. 22-3-97, 30-2-81, Sergey V. 
Zverev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Novomoskovsk </H5>

<H5>  Ecological Society ["Ekologicheskoye obshchestvo"] </H5>
  Organizes ecological education. 
  Address: 301670, Tula Oblast, city of Novomoskovsk, ul. 
Berezhnogo, d. 7, kv. 68, tel. 2-15-81, Tatyana Ivanovna 
Pershina. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Tyumen Oblast </H5>

<H5>  City of Tyumen </H5>
<H3>  Public Nature Protection Committee ["Obshchestvennyy komitet 
okrany prirody"] </H3>
  Formed in the summer of 1988. Goal: the struggle against 
irrational nature use and the development of the natural wealth 
of Tyumen Oblast. Aktiv--20-30 people. 
  Member of the Social-Ecological Alliance (see article). 
Cooperates with the Fatherland association (see article). 
  Address: 625043, city of Tyumen, ul. Pirogova, d. 17, kv. 2, 
tel. 26-78-96, Vadim Borisovich Kasinov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 2, p 222. 

<H5>    Fatherland ["Otechestvo"] </H5>
  Patriotic historical-literary association. Registered in the 
summer of 1987. Adopted a program and by-laws. 
  Goals: "protection of historical monuments and the living 
environment and health of people." 
  Opposed construction of a nitrogen combine in the city. Held 
ecology rallies on 25 May 1988 (5,000 people), 1 June 1988 
(10,000 people), and 15 June 1988 (2,000 people). Participated 
in virtually all mass events of 1989-1990. Organizes leisure 
evenings and Sunday volunteer work days at the city cemetery, 
and other things. 
  On 20-21 October 1989, at Fatherland's initiative a meeting 
of 51 people's deputies of the USSR and RSFSR was held in the 
city of Tyumen under the slogan "Rebirth of Russia." 
Twenty-eight deputies signed the appeal of the Tyumen Meeting 
(published in the newspaper LITERATURNAYA ROSSIYA). A public 
cost accounting university was created at the association's 
initiative. 
  The association has 50 members. Membership is individual. 
The 
social-vocational composition: scientists and white-collar 
workers. Up to several hundred people gathered at the large 
meetings in the DK. The council manages the association's work. 
The council's chairman is A. P. Repetov. 
  The association is part of the Council of Patriotic 
Organizations of the Urals and Siberia. Cooperates with the Ural 
People's Front and the Public Nature Protection Committee of the 
city of Tyumen (see article). 
  Has been putting out VESTNIK PATRIOTICHESKOGO OBYEDINENIYA 
"OTECHESTVO" (15 pages) since October 1989. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 222. 

<H5>    Settlement of Kondinskoye </H5>
<H5>  Sunflower ["Podsolnukh"], Group </H5>
  Works on the problem of defending the environment from 
industrial and agricultural pollution. 
  Address: 626300, Tyumen Oblast, settlement of Kondinskoye, 
ul. Svyazistov, d. 6, kv. 2, Oleg A. Obrosov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Labytnangi (Yamalo-Nenetsk Autonomous Okrug) </H5>

<H5>  Yamal Ecodefense Fund ["Fond ekozashchity Yamala"] </H5>
  Task: providing material assistance to organizations 
developing alternative technologies. 
  Address: 626520, Tyumen Oblast, Yamalo-Nenetsk AO, city of 
Labytnangi, per. Pervomayskiy, d. 9-6, kv. 6, Aleksey 
Aleksandrovich Akhrameyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Nefteyugansk </H5>

<H3>  Movement In Defense of Human Ecology ["Dvizheniye v 
zashchitu ekologii cheloveka"] </H3>
  Studies the impact of environmental pollution on the state 
of 
public health. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 626430, Tyumen Oblast, city of Nefteyugansk, 8-y 
mkrn., d. 1, kv. 103, tel. 2-11-26, Vladimir I. Moskovkin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Salekhard (Yamalo-Nenetsk AO) </H5>

<H3>  For Comprehensive Development of the Yamal Peninsula ["Za 
kompleksnoye razvitiye poluostrova Yamal"], Public Committee </H3>
  Created for the purpose of ensuring the region's ecological 
security. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 626600, Tyumen Oblast, Yamalo-Nenetsk AO, city of 
Salekhard, ul. Prudovaya, d. 23, kv. 4, tel. 6-16-11, Yevgeniy 
V. Lebedev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Surgut (Khanty-Mansiysk AO) </H5>

<H3>  Association To Save the Yugra [Assotsiatsiya spaseniya 
Yugry"] </H3>
  Ecological-political organization operating on the territory 
of the Khanty-Mansiysk Autonomous Okrug. Created in August 1989. 
  Goals: to join efforts to fight for ecological purity and 
social and economic development of the region; as well as the 
"ethno-political autonomy" of the okrug. 
  Immediate task: ecological security of the Yugra River 
basin. 
  It was announced at the founding congress on behalf of the 
peoples of the North Khanty-Mansiysk AO that "the barbarous 
destruction of our land leads to its death, and with its death 
our peoples are also condemned to death." 
  The management organs: first president--Ye. R. Kelmin (the 
former secretary of the Khanty-Mansiysk All-Union Komsomol 
Obkom), four vice presidents, a secretary, and a coordinating 
council. 
  Is creating a people's archives along with the Hungarian 
Academy of Sciences Institute of Ethnography. Has an agreement 
on cooperation with the Association of Canadian Eskimos, Arctic 
Circle, and with its help organized the sale of folkcraft items 
abroad. That is one of the main sources of income. Another 
source of financing is dues in the amount of 1 percent of wages. 
  Address: 626404, Tyumen Oblast, Khanty-Mansiysk AO, city of 
Surgut, pr. Molodezhnyy, d. 16, kv. 7, Yegor Romanovich Kelmin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    }Surgut People's Ecological Society ["Surgutskoye narodnoye </H5>

ekologicheskoye obshchestvo"] 
  Considers its task ensuring the ecologically safe 
development 
of Northern Siberia. Carries out ecological expert studies of 
petrochemical joint ventures in the region. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 626485, Tyumen Oblast, Khanty-Mansiysk AO, city of 
Surgut, RRS "Belyy Yar," d. 2, kv. 1, tel. 2-51-35, 6-26-19, 
Konstantin E. Lazerev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Tobolsk </H5>

<H5>  For New Thinking ["Za novoye myshleniye"] </H5>
  Youth cultural-ecological association (MKEO). Formed in 
March 
1988 on the base of the Tobolsk petrochemical complex and a 
branch of the Leningrad (St. Petersburg) firm Rekord. In April 
adopted by-laws and a program. In May the association was 
registered at the Center for the Realization of Young People's 
Ideas of the All-Union Komsomol City Committee. 
  The aktiv consists of 15 people, while in all there are 
about 
50 participants aged 18-30 years; composition includes students, 
intelligentsia, and workers. MKEO meetings are held in the 
Sintez House of Culture. 
  Goal: "promoting perestroyka in the city." Content of work: 
"disseminating, clarifying, and making more concrete ideas of 
the new thinking." 
  The association did vigorous ecological activity and took 
part in the election campaign. 
  MKEO participated in preparing a youth information bulletin 
(on the base of the Rekord firm). 
  Address: 626100, Tyumen Oblast, city of Tobolsk, 
Komsomolskiy 
prosp., d. 11, kv. 4, tel. 2-10-01, Sergey Viktorovich Arbuzov. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 218. 

<H3>    Tobolsk Ecological Society ["Tobolskoye ekologicheskoye 
obshchestvo"] </H3>
  Provides monitoring of preservation of the environment and 
compliance with nature protection laws, the quality of food 
products and consumer goods, and public health. Conducts 
ecological expert studies of economic projects and 
administrative decisions. Involved in ecological education. 
Participates in solving problems related to the construction and 
operation of hydroengineering structures. 
  Address: 626100, Tyumen Oblast, city of Tobolsk, ul. 3-ya 
Trudovaya, d. 2d, kv. 51, tel. 6-14-78, 6-32-74, Aleksandr V. 
Melnikov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Uvat </H5>

<H5>  Ecology ["Ekologiya"], Public Association </H5>
  Studies questions of agricultural and industrial pollution. 
  Address: 626700, Tyumen Oblast, city of Uvat, ul. Razina, d. 
34, tel. 2-12-66, 2-22-93, Boris G. Kuvshinov. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    Udmurtia </H5>
<H5>  City of Izhevsk </H5>
<H5>  Ecological Alliance ["Ekologicheskiy soyuz"] </H5>
  City organization. Involved in ecological education, the 
study of public opinion, and the gathering and dissemination of 
ecological information. Participates in solving problems of 
protecting the plant and animal worlds and preserving and 
developing the system of specially protected natural areas and 
sites and problems related to industrial pollution, the use of 
nuclear energy, and construction of AES's. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 426000, Udmurt Republic, city of Izhevsk, ul. 10 
let 
Oktyabrya, d. 55, kv. 315, tel. 77-82-10, Natalya P. Kunitsyna; 
426054, Udmurt Republic, city of Izhevsk, ul. 50 let VLKSM, d. 
32, kv. 71, Mikhail Petrovich Bashkov. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2. 

<H5>    City of Glazov </H5>
<H3>  Ecological Alliance of the City of Glazov ["Ekologicheskiy 
soyuz g. Glazova"] </H3>
  Member of the Social-Ecological Alliance (see article). 
  Address: 427600, Udmurt Republic, city of Glazov, ul. 
Sibirskaya, d. 16, kv. 51, tel. 7-86-35, Leonid Byvaltsev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ulyanovsk Oblast </H5>

<H5>  City of Ulyanovsk </H5>
<H5>  Noosphere ["Noosfera"], Ecology Club </H5>
  Engages in ecological education. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 432600, city of Ulyanovsk, ul. Kashtankina, d. 23, 
kv. 3, tel. 31-33-02, Andrey Vladimirovich Saltykov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Khabarovsk Kray </H5>

<H5>  City of Khabarovsk </H5>
<H5>  Alternative Movement ["Alternativnoye dvizheniye"] </H5>
  Created in the spring of 1990 by the activist of Work Day 
(see article) and the Confederation of Anarcho-Syndicalists 
[KAS], V. Blazhevich, and consists of members of Work Day, KAS, 
the DS [Democratic Union], the Transnational Radical Party, and 
nonparty members. Opposes AES's. Supports the constitution of A. 
D. Sakharov. 
  Address: city of Khabarovsk, tel. 55-34-25, Andrey 
Marchenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Work Day ["Trudoden"] </H5>

  This is a city club. Formed in early July 1988. Sets 
ecological-cultural and political tasks for itself: preserving 
and restoring the city's old architecture, fighting against 
construction of AES's, and fighting against totalitarianism and 
other things. Forms of work: rallies, volunteer work days, 
discussions, concerts, exhibits, and others. 
  Membership of about 30 and an aktiv of 15 people; for the 
most part students and intelligentsia, aged 18-30 years. In 1989 
there was no organizational structure. Elections of management 
organs were not held. 
  The initiative group held a number of cultural events in the 
spring of 1988 and series of discussion meetings "Youth and 
Perestroyka" in June-July. 
  In September 1988 the club participated in the campaign to 
preserve the city's old architecture: gathered signatures and 
capital to restore the monument to I. I. Muravyev-Amurskiy; on 
18 September conducted a rally in defense of the historical 
buildings of the city (about 200 participants). In October put 
out three issues of the wall newspaper OKRAINA. On 2, 16, and 30 
October members of the club took a newspaper stand to K. Marx 
Street and held talks with readers. 
  In late 1988 organized a campaign against the construction 
of 
an AES in Khabarovsk Kray and established contacts with ecology 
organizations of Komsomolsk-na-Amure. Members of the group held 
topical concerts, exhibits, including in the children's home, 
KVN [expansion unknown], and volunteer work days to restore 
architectural monuments. Published articles in the newspaper 
MOLODAYA DALNEVOSTOCHNIK. 
  In 1989 during the election campaign for people's deputies 
of 
the USSR, along with many other "informals," supported the 
candidacy of IZVESTIYA correspondent B. L. Reznik (he did not 
make it). Provided assistance to groups which supported Ye. A. 
Gayer (elected people's deputy of the USSR). Held a rally on the 
results of the election of people's deputies of the USSR. 
  Held a nonsanctioned rally devoted to the Georgian events of 
9 April 1989. 
  In April 1989 participated in the rally against the 
construction of an AES (about 1,000 people). Before the rally 
the club collected 650 signatures against the AES project. 
  Organized debates at an institute and participated in 
citywide debates and meetings (for example, in a meeting with 
KGB employees). Organized sociological research on political 
issues of a statewide and local nature. 
  On 7 October 1989 held a rally devoted to Constitution Day 
along with the Khabarovsk People's Front. 
  In early October 1989 the declaration "Unity Is in Not 
Accepting a Totalitarian Order" was adopted. 
  Starting in September 1988 put out the social-literary 
journal OKRAINA (editor B. Blazhevich, deputy editors Ye. 
Perovskaya and S. Mingazov; 50 pages, about 10 issues came out) 
and an appendix to the journal INFORMATSIONNYY LISTOK (2 issues 
total, 2 pages). Also put out the wall newspaper OKRAINA (a 
total of 7 issues), and in 1989 the newspaper was also 
reproduced in type-written form (print run of 18,000 copies). 
  Starting in the summer of 1989, the club became a branch of 
the Confederation of Anarcho-Syndicalists. On 21 February 1990 
the club disbanded. Its participants continued public activity 
in other associations, above all the Alternative Movement (see 
article). 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. cit., vol 1, part 2, p 223. 

<H5>    City of Amursk </H5>
<H5>  Independent Alliance ["Nezavisimyy soyuz"] </H5>
  Appeared in September 1989. Adheres to an 
anarchist-ecological orientation close to the Confederation of 
Anarcho-Syndicalists. Gathers signatures. Puts out an 
information bulletin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Komsomolsk-na-Amure </H5>

<H3>  Committee To Promote Perestroyka ["Komitet sodeystviya 
perestroyke"] (KSP). Ecology Section </H3>
  The initiative group (IG KSP) appeared in the spring of 
1988. 
The priority area of activity is ecology. In April 1988 
organized two volunteer ecology work days (several hundred 
people participated in one of them in Salinsk Park). On 26 
September 1988 the first rally devoted to ecology issues was 
held on the square near the Drama Theater at the initiative of 
the IG KSP (about 300 people participated). The second rally was 
organized there in February 1989 (about 3,000 participants). The 
main demand of those at the rally was to hold a referendum on 
the question of building the Dalnevostochnyy AES. (There are 
unique natural objects in the construction region). The rally's 
resolution with the demand to hold a referendum on the question 
of the AES's construction on the day of elections to the soviet 
of people's deputies (2,300 signatures) was delivered to the 
city soviet. Collected in the following months were 18,000 more 
signatures which were passed on to the First Congress of 
People's Deputies of the USSR through People's Deputy of the 
USSR V. D. Desyatov. 
  The KSP was formed at the founding conference on 19-22 July 
1989 as a non-professional sociopolitical organization. 
  The goals of KSP activity are: "consolidation of democratic 
forces to create a system of genuine people's power and a 
democratic socialist state." 
  The main forms of work are: organization of rallies, 
meetings, collection of signatures, and mass ecological actions, 
participation in the election process, work with people's 
deputies, and other things. 
  Has by-laws and a program. The press organ is the "KSP 
Herald" ["Vestnik KSP"] (published starting in the summer of 
1989, 9 issues have come out, about 12 type-written pages, a 
nonperiodical publication). In June 1990 there were about 250 
supporters in the KSP and the aktiv consisted of 30 people. 
  On 12 June 1990 at the House of Soviets took part in 
establishing the city organization of the Social Democratic 
Party of Russia [SDPR], which adopted the basic principles of 
the SDPR. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, pp 166-167. 

<H5>    City of Nikolayevsk-na-Amure </H5>
<H5>  Ecology Group ["Ekologicheskaya gruppa"] </H5>
  This is a city organization. Founded in 1989. Involved in 
the 
ecology of the Amur River and demands protection of fish sites 
and reduction of timber rafting. 
  Includes representatives of small peoples of the Far East: 
Nivkhi, Ulchi, and Evenki. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Settlement of Chegdomyn (Verkhnebureinskiy Rayon) </H5>

<H5>  Ecology Committee ["Ekologicheskiy komitet"] </H5>
  Formed in early 1989. Aktiv of 50 people; social and age 
composition is varied. Leader is Kolesnikov. 
  Goals: to preserve the habitat and protect the nature of the 
Far East from barbarian methods of industrial development. 
  The basic forms of work are collection of signatures, 
publications in the local and central press, organization of 
rallies, and work with deputies. 
  Trying to stop the contract with firms of the DPRK 
[Democratic People's Republic of Korea] to cut timber in the 
rayon. The Korean timber procurement concession in 
Verkhnebureinskiy Rayon operates on the basis of an 
intergovernmental agreement between the USSR and the DPRK of 15 
March 1967. There are 10,000 Koreans working in the DPRK timber 
procurement enterprise No 1 and they fell trees in 10 of the 
rayon's timber procurement establishments. In May 1990 the kray 
soviet of people's deputies adopted the decision to stop 
contract relations. But the cutting of trees was not stopped. 
According to data of the rayon committee on ecology and nature 
use, the Koreans leave 40 percent of the wood as waste, ruin the 
soil, and poach. [On 18 March 1992 in the settlement of Tyrma in 
Verkhnebureinskiy Rayon Korean proletarians beat up Russian 
ecologists (including the chairman of the rayon committee on 
ecology and nature use, Vladimir Khudayev) and correspondents of 
the German magazine DER SPIEGEL. The Koreans used Druzhba 
[Friendship] chainsaws to damage the helicopter which flew the 
ecologists in to conduct the expert study. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Tirmovich, A. "The Druzhba 
Chainsaw--a Weapon of the Korean Proletariat. The Korean-German 
Conflict in the Far East," KOMMERSANT, No 12, 16-23 March 1992, 
p 26; 
  -  "Rossiya: partii...," vol 1, part 2, p 224. 

<H5>    Chelyabinsk Oblast </H5>
<H5>  City of Chelyabinsk </H5>
<H3>  Greens Association of Chelyabinsk Oblast ["Assotsiatsiya 
'Zelenykh' Chelyabinskoy oblasti"] </H3>
  Formed in 1990 from ecology specialists and public figures. 
The impact of "patriotic" ideology is noticeable. 
  Provides monitoring of the condition of the environment. 
Fights against construction of the Yuzhnouralskaya [South Ural] 
AES and for compensating local residents for damages resulting 
from the radioactive contamination of the oblast. 
  Participated in the creation of the Greens Party (see 
article). 
  President of the association is V. Knyaginichev. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Battle on the Techa," ZELENYY 
MIR, No 5-6, 1991, pp 8-9. 

<H3>    Democratic Party of Greens ["Demokraticheskaya partiya 
Zelenykh"] (DPZ) </H3>
  Formed on 2 May 1990. Includes most ecology organizations in 
Chelyabinsk Oblast. Formal numbers are 1,000-2,000 people and 
the aktiv (for the most part participants in the Greens 
Association of Chelyabinsk Oblast [see article]) consists of 40 
people. The leader, N. Mironova, was elected deputy of the 
oblast soviet and is a member of the Nuclear Safety Council. 
  Held rallies, strikes, and public hearings on the 
Yuzhnouralskaya AES. 
  Is a member of the democratic associations of the Ural 
Region. Adheres to a liberal orientation. In conflict with the 
former leader of the local Greens Party, V. Knyaginichev. 
  In October 1991 announced it was joining the Greens Parties 
League (see article). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Earth's Birthday ["Den rozhdeniya Zemli], Ecology Group </H5>

  Goal: rebirth of the Yuryuzan River and other Southern Ural 
rivers. 
  Address: 450000, city of Chelyabinsk, 
Geological-Mineralogical Museum. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Pushkarev, Ye., "'Paradise' Too Is 
Not Forever," ZELENYY MIR, No 17-18, 1991, p 6. 

<H5>    Malachite ["Malakhit"], Oblast Ecological Association </H5>
  Founded in 1990. 
  Address: 454104, city of Chelyabinsk, ul. Rossiyskaya, d. 
161, kv. 2, tel. 36-98-40, 33-57-44, Vitaliy V. Knyaginichev. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    Miass ["Miass"], Ecology Club </H5>
  Formed in 1988. Aktiv of 25 people. Holds volunteer work 
days 
to save the Igumenka and Miass rivers. Collective member of the 
Chelyabinsk People's Front (see article) since 1989. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 2, p 149. 

<H5>    Youth Ecology Center ["Molodezhnyy tsentr ekologii"] </H5>
  Created in late 1980s under the Chelyabinsk City Committee 
of 
the All-Union Komsomol. Goal: to develop ecologically safe 
technologies. 
  Participant in the Greens Movement (see article). 
  Commercial director of the center is A. B. Belov. 
  Address: 454126, city of Chelyabinsk, ul. Rubezhnaya, d. 15, 
kv. 42, tel. 34-53-73, Andrey Borisovich Belov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Chelyabinsk People's Front ["Chelyabinskiy narodnyy front"], </H5>

Ecology Section 
  Studies the impact of radiation on human health and conducts 
ecological investigations and expeditions. 
  Address: 454084, city of Chelyabinsk, ul. Kaslinskaya, d. 
29, 
kv. 12, Natalya Ivanovna Mironova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Nuclear Safety ["Yadernaya bezopasnost"], Movement </H5>

  The movement's activists demand: "stop the further 
technological nuclear experiments in the Urals and change the 
specialization of the activity of the Mayak Production 
Association (with its radioactive discharges into the Tekha 
River in Southern Urals) to the rehabilitation and 
decontamination of the territory and underground waters polluted 
with radionuclides as a result of the use of 'dirty,' 
incompletely developed technologies." 
  Nuclear Safety fights against the construction of the 
Yuzhnouralskaya AES in the Tekha River valley. Rallies have been 
held with the movement's participation and about 300,000 people 
signed petitions demanding that construction, which had begun, 
be stopped. But in late 1990 the Chelyabinsk Oblast Soviet of 
People's Deputies adopted the decision: "Demand that the USSR 
Ministry of Atomic Energy and Industry immediately resume 
construction of the Yuzhnouralskaya AES as an indispensable 
installation for... stabilizing the ecological situation in the 
region of the Mayak Production Association and later improving 
it." The Chelyabinsk City Soviet of People's Deputies took a 
different posture: hold a referendum for Southern Urals 
residents on this issue on 3 March 1991. 
  The movement's coordinator is Natalya Mironova, a people's 
deputy of the Chelyabinsk Oblast Soviet. 
  Has been a collective member of the Chelyabinsk People's 
Front (see article) since 1989. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Battle on the Techa," ZELENYY 
MIR, No 5-6, 1991, pp 8-9; 
  -  SPASENIYE, No 8, August 1991, p 
6. 

<H5>    City of Zlatoust </H5>
<H5>  Fatherland ["Otchizna"] </H5>
  A patriotic association. Formed in January 1987. Goals: to 
promote the cultural, historical, economic, ecological, and 
demographic rebirth of the Russian people and other peoples of 
Russia. Forms of work: historical-educational activity, 
volunteer ecology work days, ecological monitoring of the 
environment, and protection and restoration of monuments of 
history and culture. Aktiv consists of 60 people. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 2, p 160. 

<H5>    City of Korkino </H5>
<H3>  Korkino People's Front ["Korkinskiy narodnyy front"], 
Ecology Section </H3>
  The People's Front was founded in August 1987 and registered 
by the ispolkom of the city soviet. 
  Forms of work: holding meetings, debates, and round tables, 
organizing rallies and collection of signatures, participating 
in the election process, and other things. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 167. 

<H5>    City of Kusa </H5>
<H3>  Kusinskiy Rayon Public Ecology Council ["Kusinskiy rayonnyy 
obshchestvennyy ekologicheskiy sovet"] </H3>
  Member of the Social-Ecological Alliance (see article). 
  Address: 456930, Chelyabinsk Oblast, city of Kusa, ul. 
Leningradskaya, d. 15a, kv. 2, Rakhib F. Abdurakhmanov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Magnitogorsk </H5>

<H5>  Counter Movement ["Vstrechnoye dvizheniye]. Ecology Section </H5>
  The VD is an amateur patriotic association of the city of 
Magnitogorsk. The organizing assembly was held on 13 March 1988. 
It is registered. Has by-laws and 40-50 members. The council 
(seven people) manages its activity. The chairman is V. 
Timofeyev. 
  The goal is to "implement perestroyka from the bottom up." 
The sections are ecology, nationality relations, legal, 
control-inspection, and social issues, plus a consumer society. 
Beginning in November 1988 put out the bulletin OKNO GLASNOSTI 
[Glasnost Window] consisting of 25-30 pages; 6 issues came out 
and the publication stopped. 
  Organizes lectures, concerts, treatment of alcoholism, 
rallies, collection of signatures, and debates. 
  In 1988 was able to get data on the pollution of the water 
and air basin of the Magnitka declassified and the coke battery 
shut down. 
  In June 1989 the collection of signatures against 
construction of the Yuzhnouralskaya AES (1,500 signatures) was 
organized. About 7,000 signatures were collected on the demand 
to discontinue construction of a press mold plant in the city. 
  Participates in "patriotic" conferences. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 1; 
  -  Galkina, L., op. cit., p 17; 
  -  "Rossiya: partii...," op. cit., vol 1, part 2, p 183. 

<H3>    Committee To Promote Perestroyka ["Komitet sodeystviya 
perestroyke"] </H3>
  Member of the Greens Movement (see article). 
  Address: 455001, Chelyabinsk Oblast, city of Magnitogorsk, 
ul. Gertsena, 23-a, kv. 48, Mikhail Yuryevich Kryukov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Checheno-Ingushetia </H5>

<H5>  City of Groznyy </H5>
<H3>  Greens Movement of Checheno-Ingushetia ["'Zelenoye 
dvizheniye' Checheno-Ingushetii"] </H3>
  Protests against the development of chemical industry in the 
republic, in particular against the use of BVK. Cooperates with 
Checheno-Ingushetia State University. 
  Member of the Greens Movement (see article). 
  Address: 364005, Checheno-Ingush Republic, city of Groznyy, 
ul. Gudermesskaya, 21-a, ChIGU Dormitory, No 1, kom. 31, tel. 
24-37-95, Ramazan Usmanovich Goytemirov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Funds 1, 2. 

<H5>    People's Front of Checheno-Ingushetia ["Narodnyy front </H5>

Checheno-Ingushetii"] (Initial Name: Alliance To Promote 
Perestroyka ["Soyuz sodeystviya perestroyke]) 
  The NF was created as a result of spontaneous rallies 
against 
the construction of a biochemical plant in Gudermess. 
  On 29 May 1988 a public commission on problems of ecology 
(more than 14 people) was formed at an ecology rally in Groznyy. 
On 2 July a rally demanded that the construction of the 
biochemical plant in Gudermess be stopped and persecution (by 
the local authorities) of the Alliance To Promote Perestroyka 
(the initial name of the People's Front of Checheno-Ingushetia) 
stop. Ecology rallies occurred on 10 and 17 July 1988. In late 
1989 about 5,000 people participated in a rally against the 
operation of the Serochistka [Sulfur Cleaning] installation in 
Groznyy. 
  Put out the Information Bulletin "Bart" (20 pages) starting 
in November 1989. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, pp 140-141. 

<H5>    Ecology Club ["Ekologicheskiy klub"] </H5>
  Engages in ecological education. 
  Address: 366022, city of Groznyy, Chechen-Aul, ul. 
Sheripova, 
d. 26, Aladin Amerkhanov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecological Alliance ["Ekologicheskiy soyuz"] </H5>

  Conducts ecological research on the territory of the 
Checheno-Ingush Republic. 
  Address: 364051, city of Groznyy, ul. Krasnykh Frontovikov, 
d. 8/70, kv. 11, tel. 22-43-84, 22-39-62, S. K. Gazaryants. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Chita Oblast </H5>

<H5>  City of Chita </H5>
<H5>  Greens Movement ["Zelenoye dvizheniye"] </H5>
  Opposes industrial pollution of the city. 
  Address: 672027, city of Chita, 6-y mikrorayon, d. 5, kv. 
22, 
tel. 67-20-27, Vadim Nikolayevich Valyukov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecological Front ["Ekologicheskiy front"] </H5>

  Founded in September 1988. Total number of members--20-30 
people. Participated in the ecology marches. Cooperated with the 
sociopolitical student club Glasnost. 
  Address: 672027, city of Chita, ul. Butina, d. 82, kv. 13, 
tel. 94-34-49, K. P. Despirak. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 226. 

<H5>    Chuvashia </H5>
<H5>  City of Cheboksary </H5>
<H3>  Greens Party of Chuvashia (Chuvash Republic Greens Party) 
["Partiya zelenykh Chuvashii (Chuvashkaya respublikanskaya 
partiya zelenykh)"] </H3>

  Organized in reality on 20 January 1991 at the first 
republic 
congress of ecology movements. More than 40 people from 6 of the 
republic's rayons spoke at the congress. The main issues raised 
were preventing the construction of a polycarbonate plant in the 
republic, the pollution of the Volga River, ground waters, 
farmland, and food products with chemical substances, and the 
excessive cutting of the forests. The congress adopted the 
party's by-laws and elected the coordinating council. Election 
of a chairman was postponed to the next congress because of the 
lack of a quorum. At the end of the congress a record of the 
first members of the party was made. Joining it were 73 people. 
  In 1991 coordinating council meetings were held every month. 
  At first collecting signatures for registering the party was 
the main activity. Legally it was registered on 18 December 1991. 
  Members of the party conducted an action against 
construction 
of a phosgene-based polycarbonate plant in the city of 
Novocherkassk. During the action 6,000 signatures were 
collected. The issue was examined in the Cheboksary City Soviet 
and the republic's Supreme Soviet. Construction was suspended. 
The Greens Party of Chuvashia joined the Russian Greens Party 
(see article) and the Greens Parties League (see article) of the 
former USSR. Cooperates with the Social-Ecological Alliance (see 
article). 
  Address: 428023, city of Cheboksary, ul. Grazhdanskaya, d. 
90/2, kv. 276, tel. 20-75-09, Yevgeniy Aleksandrovich Yedranov 
(member of the coordinating council). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Yakutia </H5>

<H5>  City of Yakutsk </H5>
<H3>  Public Ecology Center of Yakutia ["Obshchestvennyy 
ekologicheskiy tsentr Yakutii"] </H3>
  Conducts ecological expert studies of economic projects and 
administrative decisions, engages in ecological education, 
studies public opinion, collects ecological information, and 
engages in sociopolitical activity (participation in elections 
and so forth). Participates in resolving problems of protecting 
the plant and animal worlds, preserving biological diversity, 
and preserving and developing the system of specially protected 
natural territories and sites and problems related to the use of 
nuclear energy and the construction and operation of AES's and 
GES's. 
  Address: 677000, Republic of Sakha (Yakutia), city of 
Yakutsk, ul. Chernyshevskogo, d. 8, kv. 71, tel. 3-47-26, 
3-54-08, Nikolay A. Nakhodkin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Radical ["Radikal"] </H5>

  "A sociopolitical organization whose ideological basis is 
Marxism," emerged from a group of students who were conducting 
sociological research in Yakutsk on sociopolitical and 
ecological problems in April 1987. In June 1987 officially 
became a sociological analysis section under the Yaroslavskiy 
Rayon Committee of the All-Union Komsomol of the city of Yakutsk 
and after liquidation of the rayon branch of the organization 
was refused registration in the City Committee of the All-Union 
Komsomol. 
  Methods of work: participation in the election campaign, 
rallies, speeches at enterprises, leaflets. 
  On 3 June 1988 a rally devoted to ecological, political, and 
economic problems was held on Komsomol Square (more than 4,000 
participants). 
  Since 1989 primarily political activity (for the most part 
"of an anticommunist orientation"). 
  Size of the organization fluctuated from 10 to 150 people. 
Aktiv of up to 25 people. The chairman since the day of its 
creation is S. V. Yurkov, simultaneously, like a number of other 
participants in the group, a member of the Democratic Union. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Funds 1, 2; 
  -  "Rossiya: partii...," op. 
cit., vol 1, part 2, p 227. 

<H5>    Yaroslavl Oblast </H5>
<H5>  City of Yaroslavl </H5>
<H5>  Green Branch ["Zelenaya vetv"], Ecology Club </H5>
  A city organization. Founded in 1988. 
  Its goal is to turn the basin of the Volga River into an 
ecologically clean region. The club fights to reduce harmful 
emissions into the atmosphere and water and protests against the 
construction of AES's. 
  The cochairman of the club is Lidiya Baykova. 
  Green Branch is a member of the Social-Ecological Alliance 
(see article). 
  On 25 February 1990 the club participated in a march and 
rally (the organizer was the Yaroslav People's Front) in support 
of the candidates of the Democratic Russia bloc on Truda Square 
(about 20,000 participants). 
  Together with other ecology organizations of Yaroslavl as 
well as of Tver, Nizhniy Novgorod, Ulyanovsk, Cheboksary, 
Volgograd, and Astrakhan, the club formulated proposals for the 
state program for decontaminating the Volga-Caspian Region: 

  -  within a year of the day a Law on Nature Protection is 
adopted, obligate all organs of state power, all levels of 
soviets, ministries, and departments to stop increasing the 
number of industrial enterprises on the territory of the Volga 
River basin and allow renewal at old production sites, on the 
condition that no-waste technologies are created; 
  -  cut the 
amount of chemical production in half by abandoning toxic 
chemicals in agriculture and reducing the use of mineral 
fertilizers; 
  -  stop the operation of the Astrakhan, Tengizskiy, 
and Karachanaksiy oil and gas fields until no-waste production 
facilities are fully created; 
  -  prohibit construction of new and 
freeze existing nuclear power plants on the Volga; 
  -  do not erect 
more canals and cut off other attempts to withdraw water from 
the Volga, return the natural flow to all Volga dams, lower the 
water level in reservoirs, and completely dismantle the 
Volgograd GES; 
  -  power losses should be compensated by reducing 
the export of raw materials and fuel abroad and eliminating 
energy-intensive, especially dangerous chemical production 
facilities. 

    These proposals were examined at the Conference of Members 
of 
the RSFSR Supreme Soviet Committee on Ecology with 
representatives of ecology organizations of the land along the 
Volga no later than 11 July 1991. Deputies who attended the 
meeting made the decision to try to convince the rest of the 
members of the Ecology Committee and the RSFSR Supreme Soviet to 
single out a special Volga chapter in the Law on Nature 
Protection. 
  Address: 150000, city of Yaroslavl, ul. Trefoleva, d. 20, 
Planetarium; tel. 44-56-45, Antismog Center; tel. 21-77-48, 
Mariya S. Veselova. 
<H6>  Sources of Information </H6>

  -  Archives of A. V. Shubin; 
  -  IMPD Archives, Fund 2; 
  -  Solenikov, A., "We Rebelled," ZELENYY MIR, No 25-26, 1991, p 
3. 

<H5>    Young Naturalists Club ["Klub yunykh naturalistov"] </H5>
  Forms of work: ecological education, shaping and expression 
of public opinion, and gathering and dissemination of ecological 
information. 
  Participates in resolving problems related to the use of 
nuclear energy and operation of hydroengineering structures and 
in preserving biological diversity. 
  Address: 150000, city of Yaroslavl, Kotoroslnaya nab., d. 
30, 
kv. 109, Yelena Akatova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    People's Front (Movement To Promote Perestroyka) ["'Narodnyy </H5>

front' (Dvizheniye sodeystviya perestroyke)"]. Ecology Section 
  Collected about 7,000 signatures demanding a public expert 
study of the construction of the Yaroslavl Oblast AST. On 21 
October 1988 a public debate on the problems of atomic power 
engineering was held and broadcast on television. Taking part in 
the debate were employees of the construction trust who 
announced they refused to do more work at the AST construction 
site. 
  The section meets every week in the planetarium building. 
  Address: city of Yaroslavl, ul. Trefoleva, d. 12. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Rossiya: partii...," op. cit., 
vol 1, part 1, pp 135-136. 

<H5>    City of Pereyaslavl-Zalesskiy </H5>
<H3>  Dignity of the Pereyaslavl Land ["Dostoinstvo zemli 
pereyaslavskoy"] </H3>
  Created in January 1989. 10-15 people. Works on problems of 
local ecology and culture. Supports creation of an association 
of small cities of Russia. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Tajikistan </H5>

<H5>  SES Branch in Tajikistan </H5>
  Formulates measures on ecological security in industry, 
conducts ecological research, and organizes protests against the 
Ragunskaya GES. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 734058, city of Dushanbe, ul. Gissarskaya, d. 15, 
kv. 27, tel. 35-04-43, 23-25-23, Khamid A. Atakhanov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Turkmenistan </H5>

<H5>  Initiative Group of the Kaplankyr Preserve </H5>
  Conducts ecological research: studies the ecological 
situation, formulates nature protection programs for 
enterprises, and other things. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 746301, city of Tashauz, mkrn. Ts-1, d. 8, kv. 23, 
Andrey Lvovich Zatoka. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Uzbekistan </H5>

<H5>  Greens Movement of Uzbekistan </H5>
  Management organ is the coordinating council. Members of the 
council: Nitsa Mikhaylovna Popspirova, Fergana Polytechnic 
Institute, head of the school of nature protection; Oleg 
Ivanovich Tsaruk, head of the science department of the 
Uzzookombinat [Uzbek Zoological Combine] under the Uzbekistan 
Council of Ministers. 
  Address: city of Tashkent, tel. 90-16-47 (work), 91-39-35 
(home). 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Tashkent </H5>

<H5>  Public Committee To Save the Aral Sea and Region </H5>
  Created under the Writers Union of Uzbekistan. Involved in 
propagandizing ecological knowledge. Cooperates with other 
organizations who have set the goal of saving the Aral. 
  Address: 700000, city of Tashkent, ul. Pushkina, d. 1, P. 
Sh. 
Shermukhammedov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecologist, Association </H5>

  Appeared in 1988. Keeps track of the ecological situation 
with emphasis on the cotton industry and supports the creation 
of a republic state nature committee made up of specialists 
rather than bureaucrats. 
  Member of the Greens Movement of Uzbekistan (see article). 
  Address: 700105, city of Tashkent, pr. Gaydara, d. 11a, kv. 
10, tel. 91-39-95, 91-39-35, Oleg Ivanovich Tsaruk, member of 
the association's council. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Karakalpakia </H5>

<H5>  City of Nukus </H5>
<H5>  Alliance To Defend the Aral and the Amu Darya </H5>
  Founded in 1990. Its task is to prevent the disappearance of 
the Aral Sea and save the environment and the Karakalpak people. 
Conducts ecological research and develops ecologically clean 
technologies. 
  Address: 742000, Karakalpak AR [Autonomous Republic], city 
of 
Nukus, ul. Gorkogo, d. 179a, VTs, physics department, tel. 
4-55-93, Yusup S. Kamalov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Samarkand Oblast </H5>

<H5>  Settlement of Ziadin (Pakhtochiyskiy Rayon) </H5>
<H5>  Green Wave, Headquarters </H5>
  Member of the Greens Movement (see article). Among the 
headquarters activists is Bokhodir Dzhumayevich Khudayberdiyev. 
  Address: 704114, Samarkand Oblast, Pakhtochiyskiy Rayon, 
settlement of Ziadin, ul. Lenina, 20, Green Wave headquarters, 
tel. 311-62, Bakhridin Tangatarovich Khudayberdiyev. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Fergana Oblast </H5>

<H5>  City of Fergana </H5>
<H5>  For an Ecologically Clean Fergana, Association </H5>
  Participates in the Greens Movement (see article). Opposes 
industrial and agricultural pollution. Involved in ecological 
education. 
  Address: 712014, city of Fergana, ul. Kashkarskaya, d. 215, 
kv. 1, Nitsa Mikhaylovna Popspirova, member of the association's 
governing board. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ukraine </H5>

<H5>  Greens Movement of Ukraine </H5>
  Operates on the territory of all Ukraine, in particular in 
such populated points as the city of Voznesensk, the city of 
Dnepropetrovsk, the city of Kalush, the settlement of 
Novoamvrosiyevsk, and the city of Simferopol. 
  Management organ is the coordinating council. 
  Addresses; city of Cherkassy, tel. 66-87-79 (work), Yuriy 
Fedorovich Vysochin, chief design engineer; city of Odessa, tel. 
66-79-75 (work), 66-46-91 (home), Olimpiada Vitalyevna Gureyeva; 
city of Kremenchug, tel. 2-98-61 (home), Nikolay Antonovich 
Kutsenko; city of Dnepropetrovsk, tel. 42-85-57; telephone in 
Moscow 280-08-50 (SKZM [Soviet Peace Defense Committee]), Yuriy 
Aleksandrovich Koretskiy, pensioner; city of Zaporozhye, tel. 
64-78-75 (home), Vladislav Grigoryevich Faynshteyn. 
<H5>  Source of Information </H5>

  -  IMPD Archives, Fund 2. 

<H5>    "Zelenyy svit" (Green World) </H5>

  An ecological association. 
  The name "Zelenyy svit" is usually not translated into 
Russian and other languages in texts and the Ukrainian name 
remains in transliteration. 
  The association emerged at a meeting of primarily creative 
intelligentsia. The ZS was formed in December 1987 on the base 
of the meetings of creative intelligentsia alarmed at the 
ecological condition of Ukraine and the consequences of 
Chernobyl and was supported by the UkSSR Writers and 
Cinematographers unions. According to the by-laws, the founder 
of ZS is the Ukrainian Peace Defense Committee (UKZM). 
  The organizational center is in Kiev. The ZS has branches 
not 
only on the territory of Ukraine, including oblast and rayon 
branches and primary cells of the ZS at enterprises and 
institutions but also associated organizations and groups which 
in turn include collective members. Some of the groups which are 
part of the association, in particular those which participated 
in the First ZS Congress or joined the association later have 
their own names, including the Social-Ecological Initiative 
Association (Dneprodzerzhinsk) (see article), the Ecological 
Association "Zelenyy Rukh-Karpati" (Kalush, Ivano-Frankovsk 
Oblast) (see article), the Crimean Association Ecology and Peace 
(see article), and others. 
  In February 1990, according to the report of the ZS 
leadership, the number of branches reached 300. Large ZS 
branches exist in places where AES's exist or are being built, 
where ecologically dirty chemical industry enterprises and 
military installations are located, and in ecologically 
unfortunate large cities (Kiev, Kharkov, Odessa, and the mining 
centers). 
  Large organizations exist in Kharkov, where the movement 
emerged earlier than in Kiev. In Nikolayev in cooperation with 
the authorities the Greens prevented the expansion of the 
Yuzhnouralskaya AES. In Lvov and Ivano-Frankovsk oblasts, 
together with Rukh they are waging a fight against the North 
American enterprise Arnika and other ecologically dangerous 
objects. In Odessa they are protesting the expansion of the 
Southern Port to import African phosphates and are waging a 
fight against the transport of ammonia through Odessa by 
pipeline. The Crimean organization Ecology and Peace managed to 
get construction of the Crimean AES canceled. The 
Transcarpathian Greens oppose construction of the military radar 
station in Mukachevo. Large organizations also exist in Poltava, 
Kremenchug, Nikopol, Mariupol, and Gorlovka. 
  Neither the by-laws nor the program of the ZS adopted at the 
first congress make any mention of the language (or languages) 
of the organization. 
  The goal of the ZS is to combine the efforts of citizens and 
organizations of Ukraine in the cause of rectifying the 
ecological situation in the republic and ensuring the normal 
coexistence of man and the environment. 
  The by-laws envision individual and collective membership. 
Citizens who recognize the program and by-laws and participate 
in nature protection activity in one of the cells or an elected 
organ of the ZS may be members of the ZS. A ZS member is issued 
a certificate and a chest badge. The following may be collective 
members: 

  -  ecological associations (including cooperatives and 
scientific-technical centers); 
  -  ZS cells at enterprises, 
institutions, and organizations, as well as city and regional 
cells or centers of the ZS. 

    According to the report of the association's leadership, the 
size of the ZS at the time it was organized (January 1988) was 
27 people, but by January 1990 it had reached 160,000 members 
and--counting organizations which were collective members--up to 
500,000. 
  The highest body of the ZS is the republic congress convened 
once every 2 years. The congress adopts the by-laws and program 
of the ZS, introduces amendments and additions to them, elects 
the green council ("Zelena Rada"), the chairman of the ZS and 
his deputies, the secretariat, the managers of the executive 
organs, and the editor of the press organ. The green council is 
the main executive and representative organ of the ZS which 
coordinates ZS activity in the periods between congresses. The 
green council convenes the ZS congress, has the right of 
legislative initiative and the right to sue enterprises and 
institutions in connection with damaging the environment, 
represents the ZS in institutions and organizations of the 
republic and the USSR, and nominates candidates for deputies to 
the Supreme Soviet of Ukraine and local soviets of Ukraine. For 
the green council to adopt a decision, more than half of its 
members must be present. 
  The secretariat is the ZS standing organ which coordinates 
its activity in the period between meetings of the green council 
and handles routine organizing work. 
  The chairman of the ZS is People's Deputy of the USSR Yuriy 
Nikolayevich Shcherbak and the deputy chairmen are corresponding 
member of the UkSSR Academy of Sciences Dmitriy Mikhaylovich 
Grodzinskiy (on issues of science), Yuriy Anatolyevich Tkachenko 
(on issues of culture), Anatoliy Mikhaylovich Panov (on 
organizational issues), and Andrey Pavlovich Glazovoy (on issues 
of propaganda and information). 
  The ZS is a free association of fairly diverse groups and 
associations and collective members of the ZS. 
  According to the ZS by-laws, the regional ZS branches may 
elect their own secretariat and council to coordinate the 
activity of local cells. The organizational structure of the 
collective members (including the local ZS branches) is 
distinguished by diversity. For example, there are two 
cochairmen at the head of the Ternopol Territorial Organization 
of the ZS as well as a chairman of the executive secretariat, in 
an organization of 820 people (according to data as of April 
1990). In the Sumy Public Ecological Association of ZS, a 
council with 33 people was elected to organize general 
leadership, while 3 cochairmen with equal rights and a 
secretariat (3 people) were elected from the council for 
operational management of the work. 
  The charter forms of ZS activity are: organization and 
conduct of scientific conferences, seminars, lectures, contests, 
press conferences, picketing, rallies, marches, and other 
events; the creation of an information bank on the ecological 
situation in Ukraine; and conduct of public ecological expert 
studies; as well as active participation in peacekeeping and 
nature protection events of the Ukrainian Peace Defense 
Committee (UKZM). 
  The following are the basic stages of activity of the ZS: 
  March 1988--participation in a conference on problems of the 
accident at the Chernobyl AES. 
  On 25 April 1988 conduct, along with other organizations, of 
an unsanctioned march in Kiev in connection with the second 
anniversary of the Chernobyl accident. 
  On 25 April 1989 ZS was constituted at the All-Ukrainian 
Conference of Greens. Provisional by-laws were adopted. 
  On 28-29 October 1989 was the first ZS congress in Kiev. 
By-laws and a program were adopted and the green council and the 
secretariat were elected. Yu. N. Shcherbak was elected chairman 
of the ZS. The council of representatives, "Zelena Rada," and a 
board of experts were elected and an independent ecofund was 
created. There were more than 100 groups in the ZS. 
  Adopted at the congress were the resolutions "On the 
Ecological Crisis in the Crimea" and "On the Accident at the 
Chernobyl AES" and appeals to the Council of Ministers and the 
Supreme Soviet of the UkSSR in connection with Dzharylgach Gulf 
and the consequences of Chernobyl. 
  But charges were made against the documents adopted at the 
congress in some ecological information media. For example, the 
newspaper BLITS. VESTNIK DOP, No 2, for 1990 (publication of the 
Ozone Ecocenter in Kharkov) asserts that the congress itself and 
the documents adopted there bore evidence of haste. 
  ZS was dismissed from elections of people's deputies of the 
UkSSR, since the registration of the ZS by-laws at the State 
Nature Committee envisioned participation only in elections to 
the local soviets. As a sign of protest against discrimination 
against ZS during elections, Yu. N. Shcherbak withdrew his 
candidacy. Nonetheless, some people's deputies of Ukraine are 
members of the ZS. They are A. Kotsyuba and V. Shovkoshitnyy 
(from Kiev), M. Golubets (from Ivano-Frankovsk Oblast), V. 
Batalov (from Rovno Oblast), A. Gudima (from Volynia Oblast), T. 
Nagulko and L. Dorofeyeva (from Khmelnitskiy Oblast), B. 
Zadorozhnaya (from Zaporozhye Oblast), and V. Terekhov (from the 
Crimean Oblast). Yu. Shcherbak and L. Sandulyak are people's 
deputies of the USSR. 
  On 23 March 1990 was a meeting of the initiative group on 
creating the Greens Party of Ukraine (the future creation of 
this party was envisioned by a resolution of the first 
congress), which adopted the draft by-laws and program of the 
Greens Party of Ukraine (see article). 
  In April 1990 was participation, along with Rukh and other 
organizations, in measures related to the Chernobyl accident; a 
rally and a march on the streets of Kiev on 22 April 1990 (up to 
100,000 people participated) and the All-Ukraine Requiem for 
Victims of the Accident. 
  In April 1990 the first issue of the newspaper ZELENIY SVIT 
(or ZELENYY SVIT) envisioned by the by-laws of the ZS press 
organ, came out. The editor of the newspaper is Mikhail 
Prilutskiy. The initial print run was about 10,000. The 
newspaper comes out twice a month in eight pages in the 
Ukrainian language. 
  Thanks to the intervention of the ZS association among 
others, the burial of domestic and industrial waste near the 
village of Lesnaya Tarnovnitsa in Ivano-Frankovsk Oblast was 
prevented (RABOCHAYA GAZETA, Kiev, 8 June 1990). 
  On 12 December 1990 the green council adopted the decision 
to 
do an independent public investigation of the circumstances of 
the Chernobyl catastrophe and its consequences. The goal was to 
provide a legal evaluation of the facts related to the accident 
at the Chernobyl AES and prepare proposals to change existing 
legislation in order to reduce the likelihood of a repetition of 
the catastrophe. The group of independent jurists conducting the 
investigation obligated themselves to gather the materials, 
analyze them, and draw up a substantiated conclusion for a 
public hearing on the results of the investigation before April 
1991. In April 1991 the newspaper ZELENYY SVIT published a ZS 
letter with an appeal to the authorities, public organizations, 
labor collectives, editorial offices of newspapers, and 
individual citizens requesting them to assist the investigation. 
  No later than March 1991 the party along with the Greens 
from 
the Clamshell Alliance (United States) and the Children of 
Chernobyl Foundation (United States) began the action Project 
Vitamin to defend human rights in Ukraine. One of the methods 
for helping the victims of the nuclear accident is to ship 
vitamins or money to buy them to people who live in the zones of 
radioactive contamination. It is planned that several more of 
the world's ecology organizations will take part in the action. 
  The second congress of the association was no later than 
April 1991 in Ivanovo-Frankovsk. The congress approved the 
Ukrainian parliament's demand for an immediate and complete 
shutdown of the Chernobyl AES. The congress elected the 
governing board ("Zelena rada") and the executive organ of the 
association. Yuriy Shcherbak, a people's deputy of the USSR, was 
elected honorary chairman. His deputies are Leontiy Sandulyak 
(people's deputy of the USSR), Yuriy Tkachenko, Aleksandr Bagun, 
Anatoliy Zolotukhin, and Roman Stepanyuk. 
  Sources of financing are subsidies from the UKZM, sponsor 
contributions, and donations of citizens. 
  Membership and initiation fees are not envisioned by the 
by-laws. Membership fees are collected in some associated 
organizations, for example, the Dneprodzerzhinsk Association 
Social-Ecological Initiative--in the amount of R1 a month (with 
membership in the association at 78 people in early 1990). 
  ZS maintains permanent contacts with Greens organizations in 
the FRG and Scandinavian countries as well as in the Baltics, 
Belarus, Moscow, and the Transcaucasus (Georgia and Armenia). 
  Yu. Shcherbak and many other ZS activists are members of 
Rukh. 
  ZS has its own emblem and symbols (ZS by-laws, paragraph V, 
p. 27). 
  Addresses: 252021, city of Kiev, ul. Kirova, d. 5a, tel. 
225-67-35, Yu. N. Shcherbak; 254070, city of Kiev-70, 
Kontraktova pl., d. 4, tel. 417-02-83; city of Kiev, tel. 
263-61-67, D. M. Grodzinskiy; city of Kiev, tel. 227-41-21, Yu. 
A. Tkachenko; city of Kiev, tel. 271-10-45, A. M. Panov; city of 
Kiev, tel. 441-85-66, A. P. Glazovoy. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Galkina, L., op. cit., p 23; 
  -  "Greens--Life," SPASENIYE, No 3, March 1991, p 4; 
  -  Timonin, V. 
N., "The Chernobyl Investigation," ZELENYY MIR, No 15-16, 1991, 
p 3. 

<H5>    Greens Party of Ukraine </H5>
  An ecological-political organization. 
  Preparations to create the party began at the congress of 
"Zelenyy svit" (see article) on 29 October 1989 with a 
resolution of 30 deputies on the need to create a Greens party 
(among them were deputies of the USSR Yu. Shcherbak and N. 
Sandulyak and deputy of the UkSSR Yu. Shovkovitnyy). The 
initiative group was created on 23 March 1990 . Its founding 
meeting was held in Kiev in the fall of 1990. 
  One of the founders of the party, Anatoliy Panov, 
characterized its goals and place in this way: "We see our party 
as a component of a strong left-centrist bloc. Our political 
credo is humanism and the priority of common human values over 
ideological dogma." 
  The party's goal is to demand that the nonnuclear principles 
of the Declaration on the Sovereignty of Ukraine be realized; 
that is to say, the freeing of the republic not only of nuclear 
weapons but of nuclear power and nuclear industry (other than 
medical). 
  Yuriy Shcherbak, writer and people's deputy of the USSR, 
headed the party. The chairman of the party's auditing 
commission is Vladimir Nikolayevich Timonin. 
  On 2 June 1991 at the second party congress, a resolution 
regarding the results of the inspection by IAEA [International 
Atomic Energy Agency] and a strategy for overcoming the 
consequences of the Chernobyl catastrophe were adopted. The 
resolution expressed a lack of confidence in the IAEA which 
asserts, among other things, that "there are no grounds for 
considering that the deterioration of the health of the 
residents of Ukraine is related to radioactive emissions of 
Chernobyl." The resolution states that IAEA "as an agency for 
monitoring the spread of radioactive materials has become an 
agency for promoting atomic power engineering, in this way 
performing political tasks." 
  The general membership is about 5,000 people. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Left of Center," ZELENYY MIR, No 
11, 1990, p 2; 
  -  "Official Document," SPASENIYE, No 6, July 1991, 
p 3; 
  -  Timonin, V. N., op. cit., p 3. 

<H5>    Ukrainian Republic Chernobyl Committee </H5>
  Together with the representatives of the Belarusian, 
Russian, 
and Ukrainian republic Chernobyl committees (see article) (the 
territory of the republics which suffered most after the 
explosion of the reactor), took part in the conference in the 
USSR Commission on UNESCO Affairs in early 1991. The draft 
program of assistance in cleaning up the consequences of the 
Chernobyl accident was discussed at the conference. The program 
proposes that scientists, employees of state departments, and 
the public participate. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Klimovskaya Yu., "With UNESCO's 
Help," ZELENYY MIR, No 3-4, 1991, p 5. 

<H5>    City of Kiev </H5>
<H5>  Association of Victims of the Chernobyl Accident </H5>
  Studies the consequences of the Chernobyl accident and 
provides help for victims of the accident. Cooperates with 
similar organizations on the territory of the former USSR and 
outside its borders. 
  Address: 252207, city of Kiev, pr. Marshala Koshevogo, d. 
24, 
kv. 115, tel. 266-00-20, Yevgeniy V. Korobetskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Gromada, Society </H5>

  Engages in ecological education. 
  Address: 252101, city of Kiev, ul. Lomonosova, d. 59, kv. 
206, A. G. Sirenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Living Nature </H5>

  Involved in ecological problems of the Podol region of Kiev, 
and is making up an ecological map of Podol in order to restrict 
emissions of industrial enterprises. 
  Address: 252206, city of Kiev, ul. Malyshko, d. 15, kv. 80. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    "Zelena dopomoga" ("Green Aid") </H5>

  Founded in the summer of 1988 as the Committee To Defend the 
Goloseyevskiy Forest. Consists of students for the most part. 
Supports a charitable human attitude toward nature and provides 
aid to victims of Chernobyl. 
  Address: 252127, city of Kiev, ul. Sechenova, d. 6, 
Dormitory 
No 17, kom. 421, tel. 517-23-63, Sergey Salomatin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Katun, Movement </H5>

  Opposes construction of the Katun AES in the Altay. Studies 
the impact of hydroengineering structures on the condition of 
flora and fauna. 
  Address: 252034, city of Kiev, Yaroslavov val., d. 21a, kv. 
38, tel. 225-21-22. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Vinnitsa Oblast </H5>

<H5>  City of Kazatin </H5>
<H5>  "Sinto," Organization </H5>
  Involved in self-education on ecological issues. 
  Address: 287020, Vinnitsa Oblast, city of Kazatin, ul. 
Krasnoarmeyskaya, d. 121, kv. 2, Viktor Zavalnyuk. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Dnepropetrovsk Oblast </H5>

<H5>  City of Dnepropetrovsk </H5>
<H5>  City-Dwellers, Club </H5>
  Discusses ecological issues, engages in ecological 
education, 
studies public opinion, collects ecological information, and 
participates in solving problems of protecting the plant and 
animal worlds and problems related to industrial pollution. 
  Participates in the Greens Movement (see article). Chairman 
of the club is Igor Mikhaylovich Landa. 
  Address: 320050, city of Dnepropetrovsk, pr. Gagarina, d. 
125, kv. 69, tel. 44-22-62, V. I. Kudlad. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Save the Dnepr and the Dnepr Region, Public Committee </H5>

  Founded in 1989. Monitors the preservation of the 
environment, compliance with nature protection laws, the quality 
of food products and consumer goods, and public health, gathers 
ecological information, studies public opinion, and engages in 
ecological education. 
  Address: 320006, city of Dnepropetrovsk, ul. Sverdlova, d. 
62, kv. 4, tel. 280-08-50, Yuriy Aleksandrovich Koretskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Dneprodzerzhinsk </H5>

<H5>  Ecological Initiative, Association </H5>
  Monitors preservation of the environment, the quality of 
food 
products and consumer goods, and public health. Participates in 
solving problems related to industrial pollution. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 322622, Dnepropetrovsk Oblast, city of 
Dneprodzerzhinsk, ul. Komstromskaya, d. 13, kv. 36, tel. 
2-34-00, Sergey Savchenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Krivoy Rog </H5>

<H3>  Rebirth, Regional Association of Ecological and 
National-Cultural Salvation </H3>
  Joins together industrial workers and representatives of 
various political movements. 
  Supports giving Krivoy Rog the status of a city of republic 
subordination; the transfer to Ukraine of all ministries and 
departments whose competence includes the mining and processing 
of raw iron ore in the region; the closing of enterprises which 
are not amenable to respecialization to a technology of 
production which is safe for the ecological situation; and the 
revival of the Ingul settlement of the Zaporozhye Sech dwellers 
and the folkcrafts of the Cossacks. 
  A program was developed for using an ecologically safe 
concentration of volatile substances in the Yuzhrudy mines. 
  An independent ecology laboratory operates in the 
association 
and creation of a network of ecology sections in schools has 
begun. The association plans to build an ecology store. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "The Cossacks Are for Clean Air," 
ZELENYY MIR, No 23-24, 1991, p 10; 
  -  "The Cossacks Are for Clean 
Air," SPASENIYE, No 6, July 1991, p 2. 

<H5>    Chernobyl, Alliance </H5>
  A Krivoy Rog regional organization. 
  The alliance announced an international competition for 
children's drawings "For Clean Air" so that children's 
creativity would help draw the attention of governments and 
peoples of all countries to the problems of the environment. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  SPASENIYE, No 6, July 1991, p 
5. 

<H5>    Donetsk Oblast </H5>
<H5>  City of Donetsk </H5>
<H5>  Ecoclub Under the Newspaper VECHERNIY DONETSK </H5>
  Discusses problems of protecting the environment and 
prepares 
materials on ecological themes for the newspaper VECHERNIY 
DONETSK. 
  Address: 340092, city of Donetsk, ul. Nizhnekurganskaya, d. 
25, kv. 144, Stella Ivanovna Gurova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Yenakiyevo </H5>

<H5>  Ecology Club </H5>
  Formed under the Yenakiyevo City Committee of the Ukrainian 
Komsomol. Monitors preservation of the environment, the quality 
of food products and consumer goods, public health, and 
compliance with nature protection laws. 
  Organizes ecological education, the study of public opinion, 
and the gathering and dissemination of ecological information. 
  Participates in solving problems related to industrial 
pollution. 
  Address: 343820, Donetsk Oblast, city of Yenakiyevo, pl. 
Lenina, d. 7, GK LKSMU, Viktor Goncharov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Mariupol (Zhdanov) </H5>

<H5>  For a Clean Mariupol, Citizens Movement </H5>
  Founded in May 1988. Supported changing the name of the city 
of Zhdanov to Mariupol as well as ensuring ecological security. 
Conducts mass marches, collection of signatures, and debates on 
ecological and social problems. 
  Addresses: 341100, Donetsk Oblast, city of Mariupol, a/ya 
2991, V. L. Lykov; 341030, city of Mariupol, ul. Stroiteley, d. 
17, kv. 43, tel. 5-61-48, Ilya S. Krichman. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Committee To Save the Azov Sea </H5>

  Founded in March 1990. Cooperates with organizations working 
on problems of preserving bodies of water. 
  Address: 341032, Donetsk Oblast, city of Mariupol, pr. 
Lenina, d. 1. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Settlement of Novoamvrosiyevsk (Amvrosiyevskiy Rayon) </H5>

<H5>  Environmental Defense, Group </H5>
  Participates in the Greens Movement (see article). 
Participates in solving problems related to agricultural 
pollution. 
  Chairman of the group is T. N. Zdorovtsova. 
  Address: 343661, Donetsk Oblast, Amvrosiyevskiy Rayon, 
settlement of Novoamvrosiyevsk, ul. 1 maya, 7/2 (or 7/r), tel. 
9-93-84, Tatyana Nikolayevna Zdorovtsova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Transcarpathian Oblast </H5>

<H5>  City of Rakhov </H5>
<H5>  Carpathians, Ecology Group </H5>
  Member of the Social-Ecological Alliance (see article). 
Engages in ecological education and participates in solving 
problems related to industrial and agricultural pollution of the 
environment. 
  Address: 295800, Transcarpathian Oblast, city of Rakhov, 
a/ya 
8, Yaroslav Dovganich. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Zaporozhye Oblast </H5>

<H5>  City of Zaporozhye </H5>
<H5>  Peace Watch </H5>
  A Zaporozhye organization. Goals: to protect peace and the 
environment. 
  Participates in the Greens Movement of Ukraine (see 
article). 
  Address: 330056, city of Zaporozhye, ul. 40-letiya Sovetskoy 
Ukrainy, d. 86-a, kv. 3, tel. 64-78-75, Vladislav Grigoryevich 
Faynshteyn. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    For Ecological Perestroyka </H5>

  The organization was founded in June 1988. Studies public 
opinion, organizes ecological education, and monitors the state 
of the environment and compliance with nature protection laws. 
  Address: city of Zaporozhye, tel. 2-67-32, Olga Krivko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Green World </H5>

  Zaporozhye city organization. Involved in protecting the 
environment, among other things devised a technique for saving 
an oak that was a contemporary of the Zaporozhye Sech. But the 
local authorities and the small enterprise Aleksandrovskaya 
Starina which they charged with protecting the oak are mainly 
involved with souvenir stands rather than saving the celebrated 
tree. 
  The chairman of Green World is Ye. Kostenko. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  "Will the Oak Die?" SPASENIYE, No 
8, August 1991, p 2. 

<H3>    Young Ecologist-Tourists, Experimental Scientific-Sports 
Circle </H3>
  This is a children's organization. Engages in ecological 
education. Organizes walks whose participants study the 
condition of the environment. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 330041, city of Zaporozhye, ul. Kremlevskaya, d. 
61, 
kv. 45, tel. 52-66-73, Anatoliy Levin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ivanovo-Frankovsk Oblast </H5>

<H5>  City of Kalush </H5>
<H5>  Kalush Ecological Association "Zelenyy Rukh-Karpaty" </H5>
  Conducts ecological expert studies and protests against 
construction of the Soviet-American enterprise Polikhlorvinil 
[Polyvinyl Chloride]. 
  Collective member of the Association "Zelenyy svit" and 
participates in the Greens Movement (see article). 
  Addresses: 285400, Ivanovo-Frankovsk Oblast, city of Kalush, 
ul. B. Khmelnitskogo, d. 15, kv. 54, V. L. Kuzmich; city of 
Kalush, ul. Dzerzhinskogo, d. 4, kv. 480 (or 80), tel. 3-17-58, 
Mikhail Mikhaylovich Dovbenchuk. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Kirovograd Oblast </H5>

<H5>  City of Gayvoron </H5>
<H5>  Southern Bug, Ecology Club </H5>
  Organizes ecological education and conducts debates on 
environmental protection issues. 
  Address: 317600, Kirovograd Oblast, city of Gayvoron, ul. 
Karla Marksa, d. 63, kv. 10, Anatoliy Cherenkov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Crimean Oblast </H5>

<H5>  City of Kerch </H5>
<H5>  Kerch Branch of the Ecology and Peace Association </H5>
  Founded in the summer of 1988. Works on the problem of 
pollution of the Black Sea and other issues. Part of the Crimean 
Association Ecology and Peace. 
  Address: 334523, Crimean Oblast, city of Kerch, ul. L. 
Tolstogo, d. 130, kv. 84, tel. 2-10-65, Andrey K. Shirokov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Sevastopol </H5>

<H5>  For a Clean Crimea and Planet </H5>
  Organizes ecological education, the study of public opinion, 
and the gathering and dissemination of ecological information. 
  Participates in solving problems of protecting the plant and 
animal worlds, preserving biological diversity, and preserving 
and developing the system of specially protected natural areas 
and sites and problems related to the use of nuclear energy and 
the construction of AES's. 
  Address: 335045, Crimean Oblast, city of Sevastopol, ul. Dm. 
Ulyanova, d. 10, kv. 10, tel. 24-21-05. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology and Peace, Crimean Organization </H5>

  Organizes ecological education, the shaping and expression 
of 
public opinion, and the gathering and dissemination of 
ecological information. 
  Participates in solving problems of protecting the plant and 
animal worlds, preserving biological diversity, and preserving 
and developing the system of specially protected natural areas 
and objects and problems related to the use of nuclear energy 
and the construction of AES's. 
  Address: 335045, Crimean Oblast, city of Sevastopol, ul. 
Yeroshenko, d. 20, kv. 45, tel. 24-20-32, Valentin B. 
Serdobolskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Feodosiya </H5>

<H5>  Ecology and Peace </H5>
  Holds meetings on issues of ecology and culture. 
  Member of the Social-Ecological Alliance (see article). Part 
of the Crimean Association Ecology and Peace. 
  Address: 334809, Crimean Oblast, city of Feodosiya, ul. 
Chelnokova, d. 78, kv. 83, tel. 3-26-57, Boris Grigoryevich 
Ryzhov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Lugansk Oblast </H5>

<H5>  City of Lugansk </H5>
<H5>  Lugan, Society </H5>
  Monitors compliance with nature protection laws. Organizes 
ecological education, the study of public opinion, and gathering 
and dissemination of ecological information. 
  Participates in solving problems of protecting the plant and 
animal worlds, preserving biological diversity, and preserving 
and developing the system of specially protected natural areas 
and objects. 
  Member of the DOP Movement (see article). 
  Address: 348011, city of Lugansk, ul. Oboronnaya, d. 2, 
Pedagogical Institute, e/r f/t, Natalya Degtyareva. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Stakhanov </H5>

<H5>  Community Council on Problems of Ecology </H5>
  Studies public opinion on ecology issues and organizes 
ecological education. 
  Address: 349700, Lugansk Oblast, city of Stakhanov, per. 
Trestovskiy, d. 36, GorSES, Klara Anatolyevna Kharchenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Lvov Oblast </H5>

<H5>  City of Lvov </H5>
<H5>  Ecology Section "Tovarystva Leva" </H5>
  Founded in June 1987. 
  Opposed construction of two AES's. Source of 
financing--Ukrainian Culture Foundation. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 290005, city of Lvov, pr. Shevchenko, d. 23, tel. 
72-05-44, Andrey Mikhaylovich Stasiv. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Scientists' Ecology Club </H5>

  Engages in ecological education and conducts ecological 
expert studies of projects and decisions. 
  Address: 290044, city of Lvov, ul. Chernyakhovskogo, d. 10, 
kv. 6, M. N. Kolodko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Nikolayev Oblast </H5>

<H5>  City of Nikolayev </H5>
<H5>  Ecological Association of Nikolayev Oblast </H5>
  Member of the Social-Ecological Alliance (see article). 
  Address: 327003, city of Nikolayev, ul. Plekhanovskaya, d. 
147, kv. 63, tel. 24-66-84, Sergey Shapovalov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Pervomaysk </H5>

<H5>  Pervomayskiy Rayon Ecological Association </H5>
  Opposes pollution of the Southern Bug River. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 329810, Nikolayev Oblast, city of Pervomaysk, ul. 
Pobedy, d. 67, tel. 4-31-55, M. P. Samoylov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Odessa Oblast </H5>

<H5>  City of Odessa </H5>
<H5>  White Acacia, Youth Ecology Society </H5>
  Engages in ecological education. Takes part in measures to 
plant greenery in the city. 
  Address: 270059, city of Odessa, a/ya 408, White Acacia 
society, tel. 66-46-91, Olimpiada Vitalyevna Guryeva. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Odessa Oblast Ecology Club </H5>

  Organizes ecological education. Studies the problem of 
pollution of the Black Sea. Cooperates with the oblast's ecology 
organizations. 
  Address: 270074, city of Odessa, ul. Akademika Filatova, d. 
90, kv. 66, Yevgeniy Goncharov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    "Ekopolis," Experimental Creative Studio </H5>

  Develops ecologically safe technologies and is involved in 
creating an ecologically safe architectural complex. 
  Address: 270001, city of Odessa, ul. Bebelya, d. 28, tel. 
24-94-29, Eduard Iosifovich Gurvits. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ecology Club at the Newspaper VECHERNYAYA ODESSA </H5>

  Task is to prevent ecological catastrophes in the 
northwestern part of the Black Sea. Conducts ecological 
investigations and protests against the local nitrogen plant and 
is involved in the ecology of the Black Sea sand bars, 
ecological education on the newspaper's pages, and organization 
of work in the preserve on the Dniester delta. Helped elect more 
than 30 people's deputies of all levels. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 270076, city of Odessa, p. 50-letiya SSSR, d. 1, 
floor 8, tel. 65-71-41, L. O. Sokolovskaya. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Ilyichevsk </H5>

<H5>  Greens Party of the City of Ilyichevsk </H5>
  Ten people. Involved in ecological and sociopolitical 
issues. 
Part of the Greens Parties League (see article). 
  Address: tel. in Odessa 62-06-08, Oleg Romanenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Settlement of Yuzhnyy </H5>

<H5>  Ecology Club </H5>
  Organizes ecological education, the study of public opinion, 
and the gathering and dissemination of ecological information. 
  Participates in solving problems related to industrial 
pollution, the use of nuclear energy, and the construction of 
AES's. 
  Involved in sociopolitical activity (participation in 
elections and so forth). 
  Address: 272169, Odessa Oblast, settlement of Yuzhnyy, pr. 
Grigoryevskogo desanta, d. 26, kv. 26, V. S. Khmelnitskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Poltava Oblast </H5>

<H5>  City of Kremenchug </H5>
<H5>  Ecological Initiative, Association </H5>
  Founded in 1988. Task is to prevent an ecological 
catastrophe 
and to close the local BVK plant. 
  Helped elect two people's deputies of the USSR in 1989. 
Member of the Social-Ecological Alliance (see article) and the 
Greens Movement of Ukraine (see article). 
  Monitors the quality of food products and consumer goods and 
public health; develops alternative plans, projects, and 
technologies; participates in resolving problems related to the 
use of nuclear energy and the construction and operation of 
hydroengineering structures; and engages in issues of developing 
the system of specially protected natural areas and sites. 
  Addresses: 315300, Poltava Oblast, city of Kremenchug, ul. 
Gvardeyskaya, d. 7, kv. 64, tel. 5-49-43, Petr Fedorovich 
Tkachuk; city of Kremenchug, ul. Pervomayskaya, d. 42-a, kv. 46, 
tel. 2-98-61 (home), Nikolay Antonovich Kutsenko. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Ternopol Oblast </H5>

<H5>  City of Ternopol </H5>
<H5>  "Zelena planeta" [Green Planet] </H5>
  Founded in 1990. Conducts ecological expert studies of 
economic projects and administrative decisions. Organizes 
ecological education, the study of public opinion, and the 
gathering and dissemination of ecological information. 
Participates in solving problems related to industrial pollution 
and radiation contamination. 
  Involved in sociopolitical activity (participation in 
elections and so forth). 
  Member of the Social-Ecological Alliance (see article). 
  Address: 282024, city of Ternopol, ul. Zatonskogo, d. 10, 
kv. 
207, tel. 6-90-72, Dmitriy Pyasetskiy. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Noosphere, Social-Ecological Club </H5>

  Involved in problems of preserves and protection of 
monuments. Conducts debates on issues of philosophy and ecology. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 282006, city of Ternopol, ul. Chernovitskaya, d. 
52, 
kv. 56, Igor Korneyevich Pushkar. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Kharkov Oblast </H5>

<H3>  Kharkov Oblast Youth Ecology Center for Secondary and 
Primary School Students Under the Association Ecoforum </H3>
  The ecocenter, a non-professional public organization, 
operates on the basis of the Declaration of the All-Union School 
Children's Ecology Movement. 
  The ecocenter unites on a volunteer basis clubs and circles 
of young tourist-regional specialists, ecologists, geographers, 
and naturalists, schools, nonschool institutions, 
vocational-technical schools, and others which are its 
collective members. 
  The goal is to provide scientific, technical, 
methodological, 
and practical assistance to its collective members. 
  The tasks are: 

  -  to unite all protectors of nature in order to preserve 
life on Earth; 
  -  to create rayon ecology centers, quick reaction 
groups, ecology squads, and units of Greens and blue patrols in 
the rayons of the city of Kharkov and the oblast; 
  -  to organize 
ecology walks, expeditions, and volunteer work days; 
  -  to deepen 
knowledge of nature; exploratory and research work on the study 
of the nature, culture, and history of its region; 
  -  to take part 
in the international actions "For Peace and Ecology" and 
"Clean-Up and Beautify Cities and Villages," in "Green Trail" 
republic expeditions, "Green Detail of the Fatherland" and 
"Green Pharmacy" operations, and the oblast walk "Cleanliness 
and Full Waters for Small Rivers." 

    The main areas of activity are: 
  1. Nature and Man. 
  2. Nature and Society. 
  3. Nature and Culture. 
  4. Nature, Science, and Technology. 
  The participants in the ecocenter have their own emblem and 
badge. They are issued a certificate of the Ecoforum youth 
ecology movement for school children. 
  The basic principles of participation in the ecocenter's 
work 
are voluntary participation, democratism, humanism, 
independence, activism, and cooperation of pupils and mentors 
with equal rights. 
  The organizational structure: The coordinating work of the 
ecocenter is handled by the council which includes the manager 
of the ecocenter; the members of the Ecoforum council from 
public organizations--the oblast trade union council, the peace 
defense committee, the children's fund, the Red Cross, the 
Kharkov governing board of the NTO NGP [Scientific and Technical 
Society of the Oil and Gas Industry] imeni Gubkin, the petroleum 
and gas industry, and the oblast organization of the nature 
protection society; a representative of the oblast 
administration of public education, the obkom of the education 
workers union, and the oblast council of the pioneer 
organization; and two representatives (a pupil and a mentor) 
each from schools and nonschool institutions. 
  The council for assisting the ecocenter provides scientific 
leadership; it includes scientists and specialists of sectorial 
institutions. 
  Financing is provided from the budget of the Ecoforum 
association and is approved in the Ecoforum council. 
  Active participants in the ecology movement are awarded 
diplomas, valuable gifts, and vouchers for pioneer camps of the 
central committee of the All-Union Komsomol and the Ukrainian 
Komsomol and the international ecology camp for ecological 
exchanges. 
  Address: 310072, city of Kharkov, ul. Yesenina, d. 9, kv. 8, 
tel. 32-51-82, 92-30-14, Yalina Yakushenko. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; 
  -  Statute. Approved by the Ecoforum 
council on 11 March 1990." 

<H5>    City of Kharkov </H5>
<H5>  Cultural-Ecological Club </H5>
  Founded in the summer of 1987. 
  Task is to support ecological and cultural projects and 
publish information on the ecological situation in the oblast. 
Organizes protests at the Alekseyevskiy Dump. Publishes "Post 
Office Box." 
  Member of the Social-Ecological Alliance (see article). The 
club includes the organization "Chance" (see article). 
  Address: 310092, city of Kharkov, ul. Shekspira, d. 12, kv. 
4, tel. 32-91-35, Marianna Markova. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Kharkov Branch of the SES </H5>

  Member of the Social-Ecological Alliance (see article). 
  Monitors preservation of the environment, the quality of 
food 
products and consumer goods, and public health. Organizes 
ecological education, the study of public opinion, and the 
gathering and dissemination of ecological information. 
  Involved in sociopolitical activity (participation in 
elections and so forth). 
  Participates in solving problems of protecting the plant and 
animal worlds, preserving biological diversity, and preserving 
and developing the system of specially protected natural areas 
and sites. 
  Address: 310168, city of Kharkov, ul. Geroyev Truda, d. 12, 
kv. 461, tel. 43-80-70, Aleksandr Ryazanov. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Chance </H5>

  The organization was founded in 1987 at Kharkov State 
University. 
  Part of the Cultural-Ecological Club (see article). 
  Address: 310078, city of Kharkov, ul. Sumskaya, d. 82, kv. 
4, 
tel. 47-12-90, Igor Rassokha. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Kherson Oblast </H5>

<H5>  Settlement of Belozerka </H5>
<H5>  Public Institute of Ecology in Kherson Oblast </H5>
  Worked under the leadership of the Kherson branch of the 
Soviet Peace Defense Committee. Monitors preservation of the 
environment, the quality of food products and consumer goods, 
and public health. Organizes ecological education, the study of 
public opinion, and gathering and dissemination of ecological 
information. 
  Participates in solving problems of protecting the plant and 
animal worlds, preserving biological diversity, and preserving 
and developing the system of specially protected natural areas 
and sites and problems related to industrial and agricultural 
pollution (pesticides, fertilizers, and the like), the use of 
nuclear energy, and construction of AES's. 
  Address: 326200, Kherson Oblast, settlement of Belozerka, 
ul. 
Gagarina, d. 5, Nina Dmitrishina. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Cherkassy Oblast </H5>

<H5>  City of Cherkassy </H5>
<H5>  Ecology, Cherkassy Society </H5>
  Founded in the spring of 1988. Protests against the 
construction of an AES and organizes ecology rallies. The 
council manages the work of the society. The chairman of the 
Ecology council is Yu. F. Vysochin. 
  The society is a member of the "Zelenyy svit" Association 
(see article), the Social-Ecological Alliance (see article), and 
the Greens Movement (see article). 
  Addresses: 257002, city of Cherkassy, ul. Lenina, d. 41, kv. 
8, tel. 47-18-49, Sergey Anatolyevich Silkin; 257006, city of 
Cherkassy, ul. Gogolya, d. 580, kv. 3, tel. 43-75-28 (home), 
66-87-79 (work), Yuriy Fedorovich Vysochin. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Chernovtsy Oblast </H5>

<H5>  City of Chernovtsy </H5>
<H5>  "Zelenyy Rukh Radyanskoy Bukoviny" </H5>
  Monitors preservation of the environment, the quality of 
food 
products and consumer goods, and public health and conducts 
ecological expert studies of economic projects and 
administrative decisions. Develops alternative plans, projects, 
and technologies. 
  Participates in resolving problems of protecting the plant 
and animal worlds, preserving biological diversity, and 
developing the system of specially protected natural areas and 
sites and problems related to the construction and operation of 
hydroengineering structures. 
  Member of the Social-Ecological Alliance (see article). 
  Address: 274012, city of Chernovtsy, pr. 50-letiya 
Oktyabrya, 
d. 85/31, tel. 4-01-39, 9-84-41, Yevgeniy Rybchuk. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Estonia </H5>

<H5>  Friends of the Earth, Estonian Organization </H5>
  Founded in 1989. Organizes measures to plant greenery in 
cities. 
  Address: 202400, city of Tartu, ul. Michurina, d. 40, 
University, tel. 3-43-81, Toomas Frey [head of the Nature 
Protection Administration of Estonia in the early 1990s]. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Greens Party of Estonia </H5>

  The founding assembly was held on 10 August 1989 in Rapla; 
by-laws were adopted and the party's founding committee was 
created. Among the founders were M. Kivistik and A. Painumiae. 
Mario Kivistik became the chairman of the GPE. 
  The party was founded "thanks to the phosphorite war." 
Supports production of chemical-free food, opposes TETs's on 
shale because of high radioactivity, and supports cleaning up 
the consequences of Chernobyl. 
  GPE activists consider working in the organs of power the 
party's main task, while they consider the main task of the 
Greens Movement of Estonia to be propagandizing the "green way 
of life among the masses." The most immediate goal of this party 
is to "restore Estonian statehood without which protection of 
Estonia's living environment and its inhabitants cannot be 
ensured." 
  The party joined the unified election bloc with the People's 
Front of Estonia in the 1990 elections. 
  Address: 200090, city of Tallinn, a/ya 3046; tel. 68-13-19; 
tel. 44-45-70, Andres Torant [member of the Estonian Supreme 
Soviet]. 
<H6>  Sources of Information </H6>

  -  IMPD Archives, Fund 2; "Zelenyy v SSSR. Krupneyshiye...," 
op. cit., p 25. 

<H5>    Society for the Protection of Monuments of Old Estonia </H5>
  The initiative group appeared in late 1986, formed from 
local 
archeologists and regional studies specialists. The founding 
assembly was planned for September 1987 but was banned because 
of the possibility that dissidents would participate in it. The 
founding congress was held in December 1987. Delegates 
represented 3,000 people. T. Velliste was elected chairman. 
  In addition to ecological-cultural problems, it was involved 
in legal rights activity and the restoration of historical 
truth. Size rose to 10,000 people. In 1989 participated in 
preparations for the Congress of Citizens of Estonia. 
  Address: city of Tallinn, tel. 44-92-16. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Estonian Greens Movement </H5>

  Founded in May 1988 and registered in June 1989 by the 
republic State Nature Committee. The total number of members is 
1,500. The task is to develop nature protection measures and 
disseminate ecological information. Protests against irrational 
use of resources. 
  Also fights for democratization of social life and 
restoration of public awareness and against the steady 
deterioration of the ecological situation. Opposes pollution of 
the environment by the Soviet Army. Is developing a model of a 
free Green society in independent Estonia. "The fight for 
freedom and the fight for ecology are inseparable." 
  Six of the movement's deputies are in the Supreme Soviet of 
Estonia. Among the members of the coordinating council are: R. 
F. Ratas, member of the working bureau of the coordinating 
committee, deputy director of the ESSR Academy of Sciences 
Tallinn Botanical Gardens, and candidate of biological sciences; 
and Ya. S. Kopylov, member of the movement's council of 
authorized representatives and captain. 
  Address: 200009 (or 200035), city of Tallinn, a/ya 3207; 
city 
of Tallinn, ul. Yysmyae, d. 74, kv. 39, tel. 59-49-28, Yakov 
(Yan) Semonovich Kopylov; city of Tallinn, tel. 44-53-75 (work), 
Reyn Fedorovich Ratas. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    Tallinn Greens Movement </H5>

  Part of the Estonian Greens Movement (see article). 
<H3>  Estonian Nature Protection Society ("Eesti Loodu Skaitse 
Selts [ELKS]") </H3>
  In 1989 the society was the central public organization 
coordinating nature protection work of Estonia. ELKS was founded 
in 1966. The number of founders was 124. There are two museums 
operating under the society: the nature protection museum and 
the regional lore museum. ELKS is not involved in commercial 
activity (1989). 
  ELKS works in two areas: 
  1. Ecological education and propaganda of nature 
protection ideas (lectures, people's universities, summer 
courses, walks, excursions, and statements in the mass 
information media). 
  2. Care of landscapes (planning, consultation, and conduct 
of republic competitions). 
  The following work is done: 

  -  lecture work in all divisions; 
  -  holding of people's nature 
protection universities in the republic (a maximum of 56 
universities); 
  -  designing and laying of nature trails in the 
republic; ELKS has more than 25 years of experience here and is 
the pioneer in this area in the USSR (ELKS published a monograph 
on methods of educational trails); 
  -  conduct of a republic 
competition for caring for landscapes as well as design and 
consultation in this area; the designers' cooperative "Nature 
and Architecture" is in operation; 
  -  conduct of nature summer 
schools for teachers of all disciplines and the aktiv of nature 
protectors in Lakhemaask National Park; 
  -  conduct of measures to 
propagandize the art of flower arrangement (ikebana) in Estonia; 
  -  building up of a specialized library on nature protection 
under 
ELKS to have 16,000 volumes by 1985; 
  -  exhibits (including 
international ones), photos, posters, and children's 
drawings. 

    The society publishes the bulletin "News of the Estonian 
Nature Protection Society." 
  Maintains close ties with the Estonian Greens Movement (see 
article) and other nature protection organizations in Estonia 
and outside its borders. Member of the All-Union Nature 
Protection Society (see article). 
  Annual budget--about R80,000. Resources are from membership 
dues--R1 a year, initiation fees--50 kopecks, and from juridical 
(collective) members--at least R50; revenue from contract work, 
especially in connection with work caring for landscapes, and 
the like. 
  History: 
  Since 1967 has been conducting summer schools for upgrading 
skills of teachers: four groups under the leadership of (major) 
specialists. Each participant who is a pedagogue must make up 
collections of plants, insects, and the like which will be used 
in school as visual aids. At this time 1,200 have completed the 
17 sessions of the summer schools. 
  In 1972 the first All-Union Conference on Problems of Caring 
for Landscapes was conducted. Has been conducting fall forest 
care days since 1972. ELKS participates in managing school 
forest areas. Organizes special camps and seminars for managers 
of school forest areas. 
  In 1977 together with the Cinematographers Union of the 
Estonian SSR, held a nature film festival. Flower arrangement 
(ikebana) courses began to operate under the society. 
  The East-European Committee of the IUPN [International Union 
for the Protection of Nature] has been operating on the base of 
the society since 1978. The president of the East-European 
Committee is D. Kh. Eylart. 
  In 1980 an International Symposium on Landscape Care 
Problems 
was conducted. The East-European Committee of the IUPN working 
on the base of ELKS is the "founder of the international A. Kh. 
Tammsaare model," which is delivered to organizations and 
prominent figures in the area of ecological optimization of the 
landscape. In 1981-1985 they included the "Edisi" Kolkhoz in 
Pyarnuskiy Rayon, the "Ara vete" in Paydeskiy Rayon, the "Kindel 
Tee" in Vilyandiyskiy Rayon, and others. 
  In the early 1980s there were 36 people's universities with 
2,124 students. 
  In 1983 at the symposium "Graphic Art and Photography as a 
Means of Nature Protection Education," the Tallinn Declaration 
and its slogan "Unity of Nature and Art in the Name of Peace 
Throughout the World" were adopted. School curricula were 
modified on its basis in some countries. 
  In 1985 all-Union nature film days were held. 
  In 1985 there were 18,500 members (including 193 juridical 
members and 211 contract members) and 48 local branches in the 
society. New branches were added: the A. Kitsberg branch in 
Vilyandiyskiy Rayon (chairman--R. Mingi) and the Yu. Liyv branch 
in Alatskivi (chairman--K. Elnen). 
  Organizational structure: The basic organizational link is 
the local branch. The creation of branches is determined above 
all by territorial necessity. If necessary and if there are 
activists in the branch, sections which either operate on the 
territorial principle or join together people with certain 
interests are opened. By 1985 there were 100 of them: the Piarnu 
Phenoclub, the Tukhalaskaya section, the labor veterans section, 
and others. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Tallinn </H5>

<H5>  A-Club </H5>
  Task--to develop an ecological way of life. 
  Address: 200034, city of Tallinn, ul. Syutiste, d. 44, kv. 
32, Peeter Liyv. 
<H6>  Source of Information </H6>


  -  IMPD Archives, Fund 2. 

<H5>    Tallinn Greens Movement </H5>
  Involved in gathering and disseminating current information 
on ecological conditions. Founded in 1988. Member of the 
Estonian Greens Movement (see article). The chairman of the 
movement is R. F. Ratas. 
  Addresses: 200019, city of Tallinn, ul. Sakala, tel. 
23-84-68, Reyn Fedorovich Ratas; 200000, ul. Keresa, d. 33, kv. 
5, tel. 51-75-05, Reyn Fedorovich Ratas. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    City of Tartu </H5>

<H5>  Nature Protection Circle </H5>
  Founded in March 1958. Joins together students of Tartu 
State 
University and the Tartu Agricultural Academy. 
  Organizes ecological education, the study of public opinion, 
and the gathering and dissemination of ecological information. 
Participates in solving problems of protecting the plant and 
animal worlds, preserving biological diversity, and preserving 
and developing the system of specially protected natural areas 
and sites and problems related to industrial and agricultural 
pollution. 
  Member of the DOP Movement (see article). 
  Address: 202400, city of Tartu, ul. Lembitu, d. 1, tel. 
2-87-27, Reyn Akhas. 
<H6>  Source of Information </H6>

  -  IMPD Archives, Fund 2. 

<H5>    ALPHABETICAL INDEXES </H5>

<H5>  Index of Names </H5>
  Abdrakhmanov, K. Zh. Abdurakhmanov, R. F. Abromavicius, A. 
Averin, A. Akatova, Ye. Aleksandrov Alekseyeva Alekseyevskaya, 
L. Alyabyeva, G. N. Amarkhanova, T. Amerkhanov, A. Andreyeva, I. 
V. Anspoka, A. Antipova, Yu. V. Antonova, G. I. Arbuzov, S. V. 
Ardashnikov, I. V. Artamonov, V. A. Astafyev, V. Astrauskas, R. 
Atakhanov, Kh. A. Atnashev, A. Auezov, M. Afanasyev, Yu. Akhas, 
R. Akhmetov, M. S. Akhrameyev, A. A. Bagogishvili, Ye. N. Bagun, 
A. Baykova, L. Baymenov, A. M. Baklanova, V. A. Balabtseva, S. 
M. Balyberdin, A. N. Banshchikova, I. I. Barishpol, I. Barkar, 
A. A. Baskanova, T. F. Batalov, V. Batishchev, V. Bashkirov, S. 
G. Bashkov, M. P. Bekturganova, P. Belay, I. R. Belov, A. B. 
Belov, V. Belov, V. V. Belogrudova, T. A. Belodurov, G. N. 
Belousova, A. V. Berezhnoy, S. V. Berdnikov, S. L. Berkaliyev, 
A. Berkaliyev, M. Blazhevich, B. Blokov, I. Bobeyko, V. 
Bolshakov, B. V. Bondazhevskiy, S. Bondarev, Yu. Bondarchuk, N. 
S. Borzov, V. I. Boriskin, D. Borozin, M. L. Bortnik, P. I. 
Bortnikova, V. V. Bochkarev, Yu. Braziulis, R. Brodskiy, M. S. 
Brumelis, A. B. Budenkov, M. I. Bulat, T. Bulyndenko, O. G. 
Burakova, K. I. Burdykin, B. Ye. Butyrin, S. A. Bush, D. O. 
Byvaltsev, L. Bystrov, B. M. Vaysuras, A. Vayshvila, Z. Z. 
Balyukov, V. N. Vasev, V. M. Vasiliadi, V. I. Vasilyev, V. A. 
Vasilyev, L. Vasilyev, S. Vakharlovskaya, G. Velikhov, Ye. 
Velliste, T. Venetsianov, Ye. V. Verin, A. R. Verkhozin, A. V. 
Veselova, M. S. Vilnitis, V. A. Vinogradov, S. Vinokurov, V. 
Vitovtsev, N. Vitushka, S. Voyeykov, L. L. Volkov, A. Volkov, S. 
Volchek, B. Vorobyev, D. Vorobyeva, V. V. Vuori, M. Vysochin, 
Yu. F. Gabrielyan, A. G. Gavrilin, A. F. Gavrilko, B. Gavrilov, 
A. Gavrilov, O. I. Gagarin, K. Yu. Gayenkova, Ye. A. Gayer, Ye. 
A. Gazaryants, S. K. Galenko, V. P. Galochkina, G. Gamsakhurdia, 
Z. Ghandi, M. Ganzha, V. Ganzhina, L. A. Ganovskiy, G. A. 
Gapchak, V. Garapov, A. F. Garenkov, Yu. A. Garetskiy, R. G. 
Gdlyan, T. Kh. Geydt, V. German, A. M. Gertsvolf, Yu. R. 
Girusov, E. V. Glazovoy, A. P. Glazunov, S. N. Glebov, Ye. 
Gnezdilov, V. Goytemirov, R. U. Golitsyn, G. S. Golovina, Ye. 
Golubeva, T. I. Golubenko, A. I. Golubets, M. Goncharov, V. 
Goncharov, D. Goncharov, Ye. Gorelov, Yu. Gorchakov, P. 
Gorchakova, I. V. Grabovets, A. N. Grakauskas, L. Granin, D. 
Grigoryev, V. A. Grigoryeva, V. Grigoryan, A. V. Gricius, S. 
Grishin, A. I. Grodzinskiy, D. M. Grosheva, S. P. Gudima, A. 
Gulyayev, L. S. Gunich, D. V. Gurvits, E. I. Gureyeva, O. V. 
Kurkin, V. A. Gurova, S. I. Guryeva, O. V. Gusev, A. G. 
Gushchin, V. A. Gushchina, T. S. Davituliani Davydov Dadivanyan, 
A. K. Damye, V. Daryushin, L. Yu. Darchiya, M. Degtyareva, N. 
Demaratskiy Denisov, V. N. Desyatov, V. D. Dzhabaginov, Ye. 
Dzhukha, I. G. Dmitriyev, M. V. Dmitrishina, N. Dovbenchuk, M. 
M. Dovganich, Ya. Domashnev, S. A. Dorodnitsyn, A. A. Dorozhko, 
S. V. Dorofeyev, A. G. Dorofeyeva, L. Druganov, S. P. Duvanov, 
S. Dudov, D. Dundich, D. Durnov, V. F. Dyakonov, G. P. 
Dyakonova, N. G. Despirak, K. P. Yegorov, A. A. Yegorov, O. I. 
Yedranov, Ye. A. Yeleusizov, M. Kh. Yeltsin, B. N. Yeskaliyev, 
O. Yeslamov, S. B. Yefimenko, V. I. Yefremov, Yu. Zhavoronkov, 
M. Zhvaniya, Z. Zheludkov, A. Zhukov, S. Zhumambekov, K. 
Zhuravlev, B. A. Ziaizis, G. Zabelin, S. I. Zablovska, V. G. 
Zavalnyuk, V. Zagribelnyy, A. P. Zadorozhnaya, B. Zaikanova, I. 
N. Zakariadze, I. R. Zalygin, S. P. Zamoyskiy, V. Zaremba, B. P. 
Zatoka, A. L. Zverev, S. V. Zvirgzds, Yu. Zdorovtsova, T. N. 
Zemtsov, V. N. Zinchenko, V. G. Zlatogorskaya, O. V. Zlotnikova, 
T. V. Zolotukhin, A. Zonov, V. V. Zubkov, V. S. Zuyeva, N. 
Ivanov, A. N. Ivanov, V. V. Ivanov, S. Ivashkevich, V. 
Iventyeva, O. Ignatovich, A. V. Ignatavichyune, I. Igropulo, V. 
S. Ilyinskaya, N. V. Imanbayev, M. M. Iodis, Ya. Ya. Iskakbayev, 
M. U. Istomin, V. N. Kavtoradze, D. Kadukin, A. I. Kazannik, A. 
Kalashyan, V. R. Kaliyev, A. Kalinkin, N. M. Kalyuzhnaya, N. S. 
Kanevskaya, M. Karatayev, V. I. Karaulov, A. O. Karakhanyan, S. 
A. Karachev, V. Kruglova, S. K. Kamalov, Yu. S. Kant, I. 
Karelin, V. Karelin, Yu. A. Kasinov, V. B. Katamakhin, A. D. 
Katok, A. Kachayeva, M. A. Kashtanov, A. Kashuk, Yu. Kayumov, A. 
A. Kelmin, Ye. R. Kerchilev, S. I. Kibalnik, V. Kivistik, M. 
Kirillov, V. I. Kirpicheva, N. A. Kiryushin, A. I. Kiryushkina, 
N. P. Kiselev, A. A. Kinshunyane, V. Klushin, A. A. Kniginichev, 
V. Knorre, A. Knyaginichev, V. V. Knyazev, V. Kovalev, A. A. 
Kozhevnikov, P. V. Kozhevnikov, S. Kozeyev, G. A. Kozmin, Yu. 
Kokryatskiy, A. Koksharova, N. Kolbasov, O. P. Kolesnikov 
Kolodko, M. N. Kolotov, A. Koltunov, Ya. I. Konik, L. A. 
Kopylenko, V. M. Kopylov, P. V. Kopylov, Ya. S. Korablev, L. V. 
Koretskiy, Yu. A. Korobetskiy, Ye. V. Korotkikh, Yu. Ya. 
Korshunov, I. K. Kostenko, Ye. Kostromicheva, P. A. Kotikov, O. 
Kotsyuba, A. Krayev, N. Kregmer, M. A. Krivko, O. Krivov, S. G. 
Krinitsyn, S. Krichman, I. S. Krotov Kruchinina, N. Ye. Krylova, 
V. V. Kryukov, M. Yu. Kryukova, N. V. Ksionzhek, V. Kh. 
Kuvshinov, B. G. Kuvshinov, Yu. A. Kudasov, P. Kudlad, V. I. 
Kudryavtseva, T. T. Kuznetsov, S. Kuznetsova, N. D. Kuzmin, V. 
A. Kuzmich, V. L. Kuklin, V. V. Kukuliekis, A. Kulesh, N. N. 
Kunilovskiy, V. K. Kunitsyna, N. P. Kuratov, S. G. Kurlapov, L. 
I. Kuropatchenko, V. M. Kusov, V. S. Kufterin, A. Z. Kutsenko, 
N. A. Lavrentyev, I. A. Lavrukhin, A. Lagutov, V. V. Lazerev, K. 
E. Landa, I. M. Lapinis, S. Lapkovskiy, V. I. Latushkin, V. A. 
Lebedev, A. V. Lebedev, V. V. Lebedev, Ye. V. Levin, A. Levin, 
M. L. Legzdinsh, Ya. Ledetskiy, M. D. Leshchikova, M. Liyv, P. 
Lisetskiy, Ye. Limarenko, A. Likhachev, P. K. Likhachev, Yu. M. 
Likhodiyevskiy, A. Lobanov, V. S. Lubvennikov, I. L. Lukashvili, 
Yu. V. Lukyanov, N. P. Lurye, V. Lushnikov, A. A. Lvova, S. N. 
Lyzlov, N. Lykov, V. L. Lyubomudrov, M. Madonov, V. Mazein, S. 
A. Makarevich, N. S. Makarov, M. F. Malarchuk, G. Malakhova, V. 
V. Malaya, Ye. Malyy, P. V. Malyakov, V. V. Mamadzhanov, D. 
Mamaladze, L. Manzhos, L. M. Maniya, K. Markova, M. Martyanov, 
V. Yu. Martynova, M. V. Martynovich, A. N. Marchenko, A. 
Maslennikov, M. I. Maslov, D. G. Maslyakov, N. N. Matveychuk, V. 
N. Matrosov, A. Matulis, R. Masherov, P. M. Mezhova, A. M. Mey, 
I. Melkumova, Ye. Melnikov, A. V. Menshikov, V. Metlitskiy, F. 
F. Migi, R. Minayev, D. V. Minayev, Yu. B. Mingazov, S. 
Mironova, N. I. Mikhalchenko, Yu. I. Mikheyev, V. I. Mishurova, 
V. V. Movchan, V. A. Moiseyev, A. M. Moiseyev, N. N. Molodtsova, 
S. G. Molokanov, G. I. Molchanov, Yu. I. Monakhov, S. K. Monin, 
A. S. Monina, M. L. Montato, V. V. Morokhin, N. V. Moskovkin, V. 
I. Mudrov, A. B. Musinov, S. R. Mutaniol, V. V. Mushkudiani, D. 
A. Mukhachev, S. Nagulko, T. Nadreyev, R. M. Nazarbayev, N. 
Naydenko, V. V. Naumov, V. Nakhodkin, N. A. Nemsadze, N. 
Nikitin, V. P. Nikitin, Yu. N. Nikonov, A. L. Nikulin Novikov, 
V. I. Novitskiy, D. Ya. Nurgaliyev, Sh. Z. Obrosov, O. A. 
Overtedzh-Gudermanis, K. Ovcharenko, N. Ozhimkova, I. P. 
Oleynikov, A. S. Oniani, N. Orlinskaya, N. Yu. Orlov, A. Orlov, 
Ye. V. Oskin, D. V. Pavlenko, A. A. Pavlov, B. N. Pavlov, V. 
Pavlov, V. I. Painumiae, A. Pamelov, A. M. Panov, A. M. Panov, 
V. Panov, S. Panchenko, A. M. Parshikov, A. Perovskaya, Ye. 
Pershina, T. I. Petrov, A. T. Petrovskiy, N. A. Petryayev, Ye. 
P. Petryanov-Sokolov, I. V. Pets, L. A. Pikshris, S. Pinskiy, A. 
I. Pirogov, Yu. V. Pisarev, S. V. Pitsunova, O. N. Platonov, Yu. 
P. Plyusin, V. B. Plyusnin, V. S. Podva, T. N. Podshivalov, I. 
Polonskiy, Yu. M. Ponomarenko, S. V. Popov, A. Popov, R. P. 
Popov, S. V. Popova, T. V. Popspirova, N. M. Poptsov, O. M. 
Pochetova, I. A. Poyag, M. Prilutskiy, M. Primova, S. A. 
Prokushev, V. I. Pronkina, O. Pushkarev, V. Pushkar, I. K. 
Pushkov, P. V. Pushnikova, T. A. Pyasetskiy, D. Razdykov, B. K. 
Rapota, V. V. Rassokha, I. Rasputin, V. Ratas, R. F. Rakhilin, 
V. Rashchupkin, G. V. Revyakin, V. Rezhabek, B. G. Reznik, B. L. 
Reymers, N. F. Renitse, O. Renker, G. Repetov, A. P. Repin, V. 
A. Rerikh, Ye. I. Rerikh, N. Riverov, Yu. V. Rodionov, L. S. 
Rodionova, V. G. Rodomakha, A. Rozhnov, V. F. Romanenko, O. 
Rubinchik, L. B. Rustamov, I. Rybchuk, Ye. Ryzhenkov, A. P. 
Ryzkov, N. I. Ryzhov, B. G. Ryazanov, A. Savelyeva, L. N. 
Savitskiy, B. P. Savostyanov, N. I. Savukhin, N. S. Savchenko, 
S. Sagdeyev, R. Sadykov, Zh. A. Salakhov, M. Saldusov, V. 
Saleyev, A. A. Salin, A. B. Salomatin, S. Saltykov, A. V. 
Samoylov, M. P. Samoylova, L. V. Samokhvalov, V. B. Samykov, V. 
T. Sanbayev, S. Sandulyak, L. Sarkisyan, G. K. Safarov, M. G. 
Safronov, S. G. Sakharov, A. D. Satsevich, V. A. Svilans, M. 
Sevryukov, V. I. Sekerina, V. N. Selivanovskaya, T. P. Semenov, 
O. M. Semyashkina, V. T. Senin, N. N. Serdobolskiy, V. B. 
Serebrovskaya, K. B. Serebryakov, A. Sefer, A. F. Sidorenko, V. 
D. Silkin, S. A. Sinitsin, V. I. Sirenko, A. G. Sitnik, Zh. V. 
Skopin, A. Skorin, V. P. Skripnik, S. V. Slavko, Ye. Slednikov, 
V. A. Smolyev, S. N. Sokolov, B. S. Sokolov, V. Ye. Sokolov, S. 
A. Sokolova Sokolova, R. Sokolovskaya, L. O. Sokolchik, L. I. 
Solovyev, S. Solotova, M. V. Sosunov, A. Spiridonova, L. M. 
Stamboltsyan, Kh. Stasiv, A. M. Stakhurlov, G. A. Stepanov, A. 
Stepanyuk, R. Stepulenok, A. D. Streltsov, A. B. Stremovskiy, 
Ye. Strizhenov, G. Strom, A. D. Studenov, N. S. Suge-Maadyr, T. 
A. Suleymenov, O. O. Sumbayev, A. P. Surskiy, V. A. Sukhanov, A. 
O. Susha, A. Taglin, S. Takenov, Zh. A. Talitskaya, Z. V. 
Tamulis, Y. Tarasenko, L. G. Takenov, A. S. Talalay, M. 
Tarkhan-Mouravi, G. I. Tatibayev, R. A. Telker, F. Terentyev, A. 
I. Terekhov, V. Terekhov, Ye. G. Tesheva, N. A. Tikebayev, R. 
Timonin, V. N. Timofeyev, V. Timofeyev, V. S. Timofeyeva, M. I. 
Tikhonov, V. A. Tkachev, K. N. Tkachenko, Yu. A. Tkachuk, P. F. 
Toleubayev, B. Tolstyakov Toporovksiy, D. D. Torant, A. 
Toropyno, V. V. Troshin, V. A. Tugelbayev, S. Tumanishvili, G. 
Turbolikov, V. Tursunov, Ye. Tukhvatulin, A. Tuchin, V. A. 
Ulitin, A. A. Ulme, A. Umetskaya, S. Urazalin, M. M. Utenov, S. 
Faynshteyn, V. G. Falin, A. Fedorov Fedorov, A. V. Fedorov, A. 
M. Filatova, V. T. Filshin, G. N. Fomichev, S. R. Frey, T. 
Khabidulin, V. Yu. Khakkaraynen, N. T. Khamarkhanova, M. N. 
Khamiyev, M. Kh. Khantseverov, F. R. Kharitonenko, N. A. 
Kharitonov, V. V. Kharitonov, E. Kharlamov, A. M. Kharchenko, K. 
A. Khakhalov, A. A. Khmelinskiy, V. M. Khmelnitskiy, V. S. 
Khonin, V. P. Khoreva, G. A. Khokhlova, L. V. Khotsey, A. S. 
Khudayev, V. Khudayberdiyev, B. T. Khudyakov, V. T. Khuntsariya, 
R. Tsaruk, O. I. Tselovalnikov, A. Tsitovich, V. Chernevich, N. 
N. Chernysheva, Z. Cherp, O. Chilingarov, A. Chimbulatov, M. A. 
Chenarukhin, A. G. Cherenkov, A. Cherkasova, M. Chernov, A. V. 
Chernova, V. Chernovol, V. P. Chernovol, G. I. Chernyshev, A. V. 
Chernysheva, M. Shabanova, Yu. I. Shamin, V. V. Shapovalenko, V. 
A. Shapovalov, S. Shatokhin, S. A. Shakhanov, M. Sh. Shashkova, 
A. F. Shvedova, Yu. I. Shvetsova, V. M. Shevalev, V. P. 
Shevchuk, Yu. S. Sheyger, Ye. Sheydayev, T. Ya. Shermukhammedov, 
P. Sh. Shekhova Shilo, N. A. Shipunov, F. Ya. Shirobokov, S. A. 
Shirobokov, I. K. Shirokov, A. K. Shikhashvili, G. A. 
Shikhashvili, M. G. Shishin, M. Yu. Shmatonov, G. F. Shmitko, V. 
Shovkoshitnyy, V. Shparaga, V. S. Shubin, A. V. Shubin, M. 
Shumakov, S. N. Shushkov, V. A. Shcherbak, Yu. N. Shcherbakov, 
A. A. Shchipakina, G. G. Eylart, D. Kh. Eystere, I. Elnen, K. 
Ernshteinis, R. Yudin, V. D. Yuknis, R. Jukniavicius, R. Yurin 
Yurkov, S. V. Yablokov, A. V. Yakimenko, A. A. Yakimets, V. 
Yakovenko, V. T. Yakubauskas, G. V. Yakunin, G. Yakushenko, Ya. 
Yankina, V. A. Yanshin, A. L. 
<H5>  Index of Organizations </H5>
  5 June, Ecology Group 20th Century. Peace and Ecology, 
International Aral Movement of Poets A-Club Avant Garde, 
Association Agroresources Azhuolas (Oak), Ecology Club Azeri 
Nature Protection Society Airo Academy of the Urban Environment 
Aktyubinsk Ecologist Aktsiunya verde (AVE) (See Moldavian Greens 
Movement) Algorithm, Youth Scientific-Technical Creativity 
Center Altay Social-Ecological Alliance (Barnaul) Altair, Agency 
(Chisinau) Altair, Agency (Moscow) Alternative, Group (Gus 
Khrustalnyy) Alternative, Group (Petropavlovsk-Kamchatskiy) 
Alternative, Ecological-Political Club (Samara) Alternative, 
Ecological-Political Club (Samara). Saratov Affiliate 
Alternative Movement Alternative Education, Movement Angara 
Ecology Movement Antinuclear Movement (FRG) Antinicotine 
Foundation Antismog, Center Antinuclear Movement of Tatarstan 
Apogee, Cooperative (Kramatorsk) Apogee, Concern (Bryansk) 
Aral-Asia-Kazakhstan, Committee Aral-Front, Cooperative-Creative 
Association Arctic Movement Armenian Nature Protection Society 
Armenian Liberation Movement Association of Anarchist Movements 
(ADA) Greens Association (Aleksin) Greens Association of 
Kamchatka Greens Association of Chelyabinsk Oblast Kuril Islands 
Association USSR Association of Youth Ecology Groups Association 
of Young Historians Association of Victims of the Chernobyl 
Accident Association To Promote Ecological Initiatives 
Association To Save the Yugra Association of Public Ecology 
Organizations of Karelia Association of Ecology Centers (AETs) 
Atgaja, Club (Society) Baikal People's Front Bashkiria, 
Initiative Group GPN Bashkir Branch of the SES (See 
Social-Ecological Alliance [SES]. Bashkir Branch) White 
Acacia, Youth Ecology Society Belaya Rus, Youth Ecology Movement 
Belarusian Peace Defense Committee Belarusian Republic Chernobyl 
Committee Belarusian Council of the Ecology International of the 
Green Cross and the Green Crescent Belarusian Ecological 
Alliance (BES) Belarusian Greens Movement (BED) Biysk Branch of 
the SES (See Social-Ecological Alliance [SES]. City of Biysk 
Branch Bim, Society for the Defense of Animals Biotest 
Biosphere, Ecology Club Biryulevo-Zagorye, Self-Government 
Committee Bitsa, Society Fight To Survive (See Goyabaykar) 
Brateyevo, Public Self-Government Committee of the Brateyevo 
Microrayon Bryansk Woods, Preserve Buryat Branch of the Baikal 
Foundation (See Baikal Foundation, Buryat Branch) To Be, 
Ecology Club at the Caucasian Mineral Waters Bambi Bureau of 
Ecological Developments (BER) In Defense of the World of Nature, 
Ecology Club Vasizi, Club Peace Watch, Organization USSR 
Vegetarian Society Viola, Ecological Problems Center Vita Longa, 
International Movement Rebirth (See Goyatevum) Rebirth, Borovsk 
Noosphere Center Rebirth, Jewish Informal Organization Rebirth, 
Public Committee (Nizhniy Tagil) Rebirth, Regional Association 
of Ecological and National-Cultural Salvation (Krivoy Rog) 
Rebirth, Ecological-Cultural Society (Kaliningrad) Volzhskiy, 
Socialist Group Volzhskiy Ecological Alliance Vologda Ecology 
Club Physicians Against Nuclear War Provisional Citizens 
Committee Time, Group World Information Center All-Russian 
Association of Cat Fancier Clubs All-Russian Ecology Center 
(VETs) at the VOOP All-Russian Nature Protection Society (VOOP) 
All-Russian Nature Protection Society (VOOP). 6th Section 
All-Union Society for the Defense of Animals All-Union Council 
of Hunters and Fishermen's Societies (VSOOR) Counter Movement, 
Amateur Patriotic Association. Ecology Section Survival 
(Yerevan) Harmony, Cultural-Philosophical Society USSR 
Geographic Society Glasnost, Debate Club (Bryansk) Glasnost, 
Sociopolitical Student Club (Chita) Glasnost, Political Club 
(Vrangel) Citizen, Information Center (Volzhskiy) Citizen, 
Volunteer Club (Maykop) Citizens Initiative, Club Grin-Khipp 
[Green Hippie] Blue Baltic Little Dove Golyanovo, Public 
Self-Government Committee Gomel Oblast Ecological Alliance 
(GOES) Gornyy Altay Branch of the SES (See Social-Ecological 
Alliance [SES]. Gornyy-Altay Branch) City Committee on 
Ecological Problems City Dwellers, Club Goyabaykar, Ecology 
Group Goyatevum, Alliance Civil Dignity Greenpeace Gromada, 
Society Georgian Ecological Association Georgian Peace Defense 
Committee Nature Protection Group of the School of Geography of 
Moscow University Nature Protection Group (See Youth Nature 
Protection Society of Georgia) Group To Save the 
Historical-Cultural Monuments of St. Petersburg (See 
Salvation, Group [St. Petersburg]) Guzeripl Branch of the SES 
(See Social-Ecological Alliance [SES]. Branch of the 
Settlement of Guzeripl) Humanist Party Dagestan Council of the 
VOOP Movement in Defense of Baikal Movement in Defense of the 
Irtysh (See Coordinating Center of the Movement in Defense of 
the Irtysh) Movement in Defense of Human Ecology Nature 
Protection Squads Movement (DOP Movement) Movement for the 
National Independence of Latvia Movement To Create the Greens 
Party Movement To Create the Greens Party of Belarusia (See 
Movement To Create the Ecology Party of Belarus) Movement To 
Create the Ecology Party of Belarus Greens Movement (Kolomna) 
Greens Movement of Azerbaijan Greens Movement of Belarus (See 
Belarusian Greens Movement) Greens Movement of Georgia Greens 
Movement of Lithuania (DZL) Greens Movement of Moldova (See 
Moldavian Greens Movement) Greens Movement of Estonia Movement 
To Promote Perestroyka (See People's Front [Yaroslavl]. Ecology 
Section) Action (Tomsk) Action, Ecology Organization 
(Novodvinsk) Business Ecology Club Delta, Ecological Association 
Democratic Party of Greens Democratic Russia, Movement 
Democratic Azerbaijan, Bloc Democratic Choice Democratic Union 
Democratic Movement for Perestroyka (DDP). Ecology Section 
Earth's Birthday, Ecology Group Children To Save the 
Earth--Russia Children and Adolescents Ecology Club For the 
Children of Chernobyl, Belarusian Charitable Foundation Dialog 
(Krasnodar) Dialog, Sociopolitical Club (Omsk) Dialog, 
Sociopolitical Club (Perm) Didube, Club Debate Club on Ecology 
Issues Dniester, Interrepublic Public Committee Volunteer 
Society To Promote Perestroyka Don, Creative Association Don 
People's Front Dignity Dignity of the Pereyaslavskiy Land Dodo 
Bird, Ecology Center Greens Squad of Chisinau Pedagogical 
Institute Nature Protection Squad (Orel) Nature Protection Squad 
(Ryazan) Nature Protection Squad of Arzamas Pedagogical 
Institute Nature Protection Squad of Bashkiria Nature Protection 
Squad of Kazan Chemical-Technological Institute Nature 
Protection Squad of Nizhniy Novgorod University Friends of the 
Earth, International Organization Friends of the Earth, Estonian 
Organization Friends of Ropsha, Ecology Group European 
Headquarters of the Greens Parties Spruce, Group Hot August 
Zhem, Antinuclear Group Women Against AST's Zhetysu, Ecological 
Association Living Nature Zhyamina, Ecology Club For Atomic 
Safety, Volunteer Society For a Nonnuclear World and the 
Survival of Humankind, International Organization For 
Survival, Ecology Organization For the Survival and Development 
of Humankind, International Foundation For Closing the Rostov 
Nuclear Power Plant, Regional Citizens Committee For 
Comprehensive Development of the Yamal Peninsula, Public 
Committee For Our Common Future, Geneva Center For New Thinking, 
Youth Cultural-Ecological Association (MKEO) For a Clean Crimea 
and Planet For Clean Air and Water, Social-Ecological Society 
For a Clean Mariupol, Citizens Movement For an Ecologically 
Clean Fergana, Association For Ecological Perestroyka, 
Organization Zagorsk Ecological Society Environmental Defense, 
Group Star Peace, Center Zeyskiy Rayon Ecological Initiative 
Center Zelena planeta Green Branch, Ecology Club (Murmansk) 
Green Branch, Ecology Club (Yaroslavl) Green Wave, 
Social-Ecological Group (Volgodonsk) Green Wave, Headquarters 
(Ziadin) Green Squad (Ryazan) Greens Party of Estonia Green Aid 
Zeleniy svit, Ecological Association Zeleniy svit, Branch 
(Nikolayev) Zeleniy svit, Branch (Sumy) Greens Movement Greens 
Movement (Dzhambul) Greens Movement (Lipetsk) Greens Movement 
(Murmansk) Greens Movement (Nalchik) Greens Movement (Pskov) 
Greens Movement (Smolensk) Greens Movement (Tambov) (See 
Memorial [Tambov]. Ecology Group) Greens Movement (Chita) Greens 
Movement of Armenia Greens Movement of Kazakhstan Greens 
Movement of Ukraine Greens Movement of Uzbekistan Greens 
Movement of Checheno-Ingushetia Greens Movement, Regional 
Organization (Balashikha) Greens Movement, Ural Regional 
Federation Greens Movement, Ecology Club (Vladimir) Green 
Salvation Greens (Provideniya) Green Shore Green City, 
Social-Ecological Association Green Patrol, Group Green Don, 
Independent Ecology Movement Green Committee Green Leaf Green 
World (Astrakhan) Green World (Zaporozhye) Green World (Omsk) 
(See Green City, Social-Ecological Association) Green World 
(Sayanogorsk) Green World (Ukraine) Green Peace Green World, 
Association (Sosnovy Bor) ZELENYY MIR, Ecology Newspaper Green 
World, Ecology Club (Kazakn) Green World, Ecology Movement 
(Krasnoyarsk) Green World, Ecological Association (Nizhniy 
Novgorod) Green World--Rebirth, Ecology Group Green Alliance 
Green Hippie (See "Grin-Khipp") Greens Foundation Greens Front, 
Association (Kzyl-Orda) Greens Front of Kazakhstan Zimbru, 
Ecology Club Knowledge (SCIO), Moscow Esperanto Club Znich, 
Belarusian P. M. Masherov Alliance To Aid Victims of the 
Chernobyl Accident Zelena dopomoga (See Green Aid) Zelena 
planeta Zelenyy Rukh of Radyanska Bukovina Zelenyy 
Rukh--Karpati, Kalush Ecological Association Zelenyy svit (See 
Zeleniy svit) Engineering Ecology, Publishing Foundation 
Initiative, Architectural Organization (Moscow) Initiative, 
Social-Ecological Association (Almaty) Initiative, Novosibirsk 
Ecology Council Revolutionary Anarchists' Initiative Greens 
Initiative Group at the Radio Equipment Plant (Pravdinsk) 
Initiative Group of the Kaplankyr Preserve Initiative Ecology 
Group (Vidnoye) Initiative Ecology Group (Dzerzhinsk) Initiative 
Ecology Group (Nalchik) Initiative Ecology Group (St. 
Petersburg) Initiative Ecology Group (Smirnykh) Initiative Group 
for the Defense of Perestroyka Initiative Group To Save the 
Bityug River Initiative Center of the People's Front (See 
People's Front [Kazan]. Initiative Center) 
Information-Research Center of the Movement for Communes 
Information Agency on Nongovernmental Ecology Organizations 
(Ekoinform) Caucasian Circle, Society Kazakh Nature Protection 
Society Kalmyk Steppe, Social-Ecological Association Kalush 
Ecological Association "Zelenyy Rukh--Karpati" (See Zelenyy 
Rukh- Karpati, Kalush Ecological Association) Karelia, 
Travelers Club Carpathians, Ecology Group Katun, Movement Kaunas 
Ecology Club Cedar, Green Movement Kerch Branch of the Ecology 
and Peace Association (See Ecology and Peace, Association 
[Crimea]. Kerch Branch) Kitavras, Cultural-Ecological 
Association Left Bank Citizens Initiatives Club at Akademgorodok 
Environmental Defense Club (Vizes Aizsargs Klub--VAK) 
Environmental Defense Club (Liepaja) Environmental Defense Club 
(Jurmala) Greens Club Voters Club Nature Protection Club 
Consumers Club Travel Club in Defense of Peace and Nature Young 
Naturalists Club Club-81, Information Association of Literary 
Figures Cradle, Ecology Society USSR Commission on UNESCO 
Affairs Volga Defense Committee (See Committee To Save the 
Volga) Forest Defense Committee Environmental Defense Committee 
Nature Protection Committee of Perm Oblast Committee on Problems 
of the Aral Committee To Promote Perestroyka (Krasnoyarsk) 
Committee To Promote Perestroyka (Magnitogorsk) Committee To 
Promote Perestroyka (KSP) (Komsomolsk-na-Amure). Ecology 
Section Committee To Save the Azov Sea Committee To Save the 
Angara Committee To Save the Volga Committee To Save the Volga. 
Nizhniy Novgorod (Volgograd) Branch Committee To Save the Katun 
and Gornyy Altay Committee To Save the Pechora (Pechora) 
Committee To Save the Pechora (Ukhta) Committee To Save the Tom 
River Committee To Save the Black Sea Clear Air Committee 
Ecological Monitoring Committee Congress of Citizens of Estonia 
Confederation of Anarcho-Syndicalists Confederation of 
Independent Trade Unions Coordinating Center of the Movement in 
Defense of the Irtysh Korkino People's Front. Ecology Section 
Cosmos, People's University KSP (Bolshevo-1) Cosmos, 
Philosophical-Health Club (Moscow) Nomadic People's Trek into 
the 21st Century, Public Committee Nature Protection Circle 
Kuban People's Academy Cultural Initiative, Soviet-American 
Foundation Cultural-Ecological Club Kursk People's Front 
Kusinskiy Rayon Public Ecology Council Laboratory, Marxist 
Social-Political Club Ecological Planning Laboratory of the 
Soviet-American Cultural Initiative Foundation Landscape 
Ecology Section of the Nizhniy Novgorod Branch of the Architects 
Union Latvian Greens Party Forest, Social-Ecological Group 
Tree Nursery, Initiative Group Lefortovo, Ecology Group League 
of Democratic Forces of the City of Ufa Nature Defense League of 
Nepetsino Secondary School Greens Parties League (LPZ) Lipetsk 
Organization of the Greens Party (See Greens Party. Lipetsk 
Organization) Lithuanian Nature Protection Society (LOOP) Logos 
Lotus Lugan, Society Magadanskiy, Ecology Club Magnitude, 
Cooperative Geophysical Expedition Maladik, Group Malachite, 
Ecological Association March (See Sakavik) Matena, City NTTM 
Center International Greens Movement International Committee To 
Promote CED-92 International Nature Protection Alliance 
Interoblast Committee To Defend the Prut Memorial (Omsk) 
Memorial (Tambov). Ecology Group Memorial, Historical-Education 
Society (Murmansk) Memorial, Organization (Vorkuta) Miass, 
Ecology Club Commune ["Mir"], Volunteer Association (St. 
Petersburg) Peace, Youth Ecology Group (Rostov-na-Donu) 
Moldavian Greens Movement Moldavian Nature Protection Society 
Molitovka Public Council Youth Association To Promote Ecological 
Initiatives Georgia Youth Association for Nature Protection (See 
Youth Nature Protection Society of Georgia) Youth Nature 
Protection Society of Georgia Youth Nature Protection Council of 
Moscow University Youth Ecology Center Youth Ecology Center of 
the University of Latvia Moscow River, Society Moscow 
Organization of the Greens Party (See Greens Party, Moscow 
Organization) Moscow Ecological Federation Moscow People's Front 
Moscow Ecology Club under the Peace Defense Committee Moscow 
Ecology Center (METs) Moscow Society for the Defense of Animals 
Ants, School Movement Murlyka, Club People for Baikal, Ecology 
Organization People's Front (Kazan). Initiative Center People's 
Front (Samara) People's Front (Yaroslavl). Ecology Section 
People's Front of Belarus People's Front of Georgia People's 
Front of Karelia People's Front of Latvia People's Front of 
Checheno-Ingushetia People's Front of Estonia Nakhodka 
Democratic Front National Movement of Georgia National Congress 
(Azerbaijan) Our Common Future, Center Neburg, School Ecological 
Expedition Neva, Ladoga, and Onega, National Alliance (Public 
Salvation Committee) Nevada-Semipalatinsk, Antinuclear Alliance 
Nevada-Semipalatinsk. East Kazakhstan Oblast Branch 
Nevada-Semipalatinsk. Dzhambul Oblast Branch 
Nevada-Semipalatinsk. Karaganda Regional Branch 
Nevada-Semipalatinsk. Kokchetav Oblast Branch 
Nevada-Semipalatinsk. Pavlodar Oblast Branch 
Nevada-Semipalatinsk. Petropavlovsk Oblast Branch 
Nevada-Semipalatinsk. Semipalatinsk Oblast Branch 
Nevada-Semipalatinsk. Tselinograd Oblast Branch Battle of Neva, 
Historical Restorationists' Initiative Group Independent 
Alliance Next Stop USSR, Movement Nizhniy Novgorod Council for 
the Ecology of Culture (NSEK) Lower Volga (Volgograd) Branch of 
the Save the Volga Committee (See Committee To Save the 
Volga. Lower Volga [Volgograd] Branch) Novaya Zemlya-Nevada, 
Committee New World, Amateur Historical Restorationists Group 
Novosibirsk Initiative Noosphere (Volgograd) Noosphere, 
All-Union Ecological Association (VEO) Noosphere, Children's 
Ecology Station (Moscow) Noosphere, Social-Ecological Club 
(Ternopol) Noosphere, Ecology Club (Bryansk) Noosphere, Ecology 
Club (Kemerovo) Noosphere, Ecology Club (Leninogorsk) Noosphere, 
Ecology Club (Ulyanovsk) Noosphere, Ecology Committee (Mogilev) 
Noosphere Center Nura, Society Oasis, Ecology Club Oblast Greens 
Association (Chelyabinsk) Oblast Regional Studies Laboratory 
School (Samara) Oblast Youth Ecological Alliance (Tula) Commune 
["Obshchina"] Public Ecology Commission Sociopolitical 
Initiatives, Club Social-Ecological Committee Public Ecology 
Institute in Kherson Oblast Public Committee of the Aral, 
Balkhash, and the Ecology of Kazakhstan (See Public Committee 
on Problems of the Aral, Balkhash, and the Ecology of 
Kazakhstan Public Nature Protection Committee Public Committee 
To Protect the Seym River Public Committee on Problems of the 
Aral, Balkhash, and the Ecology of \Kazakhstan Public Committee 
To Save the Tom River Public Committee To Promote Perestroyka 
Public Committee To Save the Aral and the Aral Region Public 
Committee To Save the Volga (OKSV) Public Committee for 
Ecological Monitoring and Assistance (Tuapse) Public Council To 
Save the Volga Public Ecology Club (Dobryanka) Public Ecology 
Committee (Apatity) Public Ecology Center (Rostov-na-Donu) 
Public Ecology Center of Yakutia Society for the Defense of 
Baikal Greens Society (Novogorod) Greens Society of 
Leningradskiy Rayon in the City of Moscow Society of Regional 
Studies Specialists of Kazakhstan Society To Protect the 
Monuments of Old Estonia Nature Protection Society (Kursk) 
Society for the Protection of Nature and Monuments Artists' Aid 
Society Commune ["Obshchina"] Unified Committee of Public 
Organizations United Trade Union of Ecologists (OPZ) Odessa 
Oblast Ecology Club Health Improvement, Ecology Club Ozone, 
Ecology Club (Yekaterinburg) Ozone, Kharkov Oblast Ecology 
Center Oykos, Travel Club in Defense of Treasures of Culture and 
Nature Oka Ecological Society (Ekor) Omsk People's Front 
Ostashkov Branch of the SES (See Social-Ecological Alliance 
[SES]. Branch of the City of Ostashkov) OSEP SES Branch in 
Tajikistan (See Social-Ecological Alliance [SES]. Tajikistan 
Branch) Fatherland ["Otechestvo"], Ecological-Cultural 
Orientation Club (Ryazan) Fatherland ["Otechestvo"], Patriotic 
Historical-Literary Association (Tyumen) UNEKO Detachment (See 
UNEKO, Detachment) Fatherland ["Otchizna"], Patriotic 
Association Purification, Ecology Club (EKO) Monument, Cultural 
Studies Club Pamyat [Memory], Russian National-Patriotic Union 
Pamyat, Historical-Patriotic Association (City of Novosibirsk) 
Panayarvi, Creative Noosphere Club Greens Party (PZ) Greens 
Party (Vyksa) Greens Party (Ilyichevsk) Greens Party 
(Novokuybyshevsk) Greens Party (St. Petersburg) Greens Party. 
Lipetsk Organization Greens Party. Moscow Organization Greens 
Party of Georgia Greens Party of Krasnoyarsk Kray Greens Party 
of Latvia (See Latvian Greens Party) Greens Party of Lithuania 
[PZL] Greens Party of the Nizhniy Novgorod Region Greens Party 
of the Kama Region Greens Party of Sakhalin Greens Party of 
Ukraine Greens Party of Chuvashia Greens Party of Estonia (See 
Greens ["Zelenaya partiya"] Party of Estonia) Pedagogues for 
Ecological Sophistication, Association Pervomayskiy Rayon 
Ecological Association Perm Branch of the SES (See 
Social-Ecological Alliance [SES]. Branch of the City of Perm) 
Petersburg, Historical-Cultural Society Pilgrim, Communard Club 
Sunflower, Group Position, Ecological-Political Club Ecology 
Search, Club (Aboyan) Ecology Search, Club (Yerevan) Poklonnaya 
gora, Ecology Group Polesye Ecology Movement, Initiative Group 
Polar, Ecology Group Maritime Society of Technical Ecology 
Maritime Ecological Action Society (POED) Nature (See Tabigat) 
Nature, Initiative Group (Medvezhyegorsk) Nature, Association 
(Petrozavodsk) Nature and Society (Zheleznogorsk) Nature and 
Society (Khomutovka) Protva, Noosphere Committee Protvino Nature 
Protection Society Piarnu Phenoclub Radical, Sociopolitical 
Organization Rainbow, Interregional Youth Organization Ranitsa, 
Group Resonance, Ecological-Political Club (Novokuybyshevsk) 
Republic Public Committee To Save the Caspian Resource, 
Scientific-Production Center Robin Hood, Greens Movement (FRG) 
Spring, Voskresensk Ecological Society Spring, Sociopolitical 
Club (Kursk) Spring, Ecology Group (Moscow) Clean Water Rock, 
Musical Ecology Movement Russian Greens Party (RPZ) Russian 
Ecological Academy Russian Committee for the Defense and Rebirth 
of the Oka Russia's Open University (ROU) Russian Republic 
Chernobyl Committee Russian Social-Ecological Alliance Russian 
Ecological Alliance (RES) Russian Ecology Foundation Russian 
Christian-Democratic Movement Rostov Oblast Ecology Center 
(ROETs) Rostov Public Ecology Center Rostov Ecology Center 
Rublevo, Ecology Organization Rus, Ecology Group Rukh Sakavik, 
Ecological-National-Cultural Society Samarskaya Luka, Ecology 
Group Samara Greens Alliance Saratov Affiliate of the 
Alternative Club (See Alternative, Ecological- Political Club 
[Samara]. Saratov Affiliate) Sajudis Light Sviblovo, Ecology 
Club Free Student Green League North, Ecology Group Northern 
Region, Ecology Group Severobaykalsk Headquarters for the 
Defense of Baikal North Caucasus Branch of the USSR Ekofond (See 
USSR Ecology Foundation. North Caucasus Branch) Ecological 
Power Engineering Section Siberia, Association Sinto, 
Organization System, Alternative-Cultural Movement Scandal, 
Greens Alliance (Kondopoga) Scandal, Greens Alliance (Krasnodar) 
Sloboda, Ecological-Cultural Youth Association People's Front 
Council (Norilsk) Community Council on Problems of Ecology 
Public Initiatives Council (SOI) Council of Patriotic 
Organizations of the Urals and Siberia Nature Protection Council 
Council for the Ecology of Culture (SEK) Ecology Council of the 
USSR Artists Union Governing Board Commission on /m Ties with 
Creative Unions and Other Public Organizations Council of the 
Nature Protection Society in Oiyai Public Self-Government 
Council of the Lyublino-2 Microrayon Soviet Association of 
UNESCO Clubs Soviet Peace Defense Committee Soviet Committee on 
the UNESCO Program "Man and the Biosphere" Soviet 
Nongovernmental CED-92 Preparations Committee Soviet Peace 
Foundation Contemporary, Architectural Organization Promotion of 
Perestroyka, Organization. Ecology Section Solntsevo, Public 
Self-Government Committee Social-Democratic Party of Kazakhstan 
Social-Democratic Party of Russia Socialist Initiative Socialist 
Club Social Initiative Social Justice Social-Ecological Group 
Social-Ecological Initiative, Association Social-Ecological 
Alliance (SES, SoES) Social-Ecological Alliance (SES). Bashkir 
Branch Social-Ecological Alliance (SES). Gornyy Altay Branch 
Social-Ecological Alliance (SES). Tajikistan Branch 
Social-Ecological Alliance (SES). Branch of the City of Biysk 
Social-Ecological Alliance (SES). Branch of the City of 
Blagoveshchensk Social-Ecological Alliance (SES). Branch of the 
Settlement of Guzeripl Social-Ecological Alliance (SES). Branch 
of the City of Dubna Social-Ecological Alliance (SES). Branch of 
the City of Dushanbe Social-Ecological Alliance (SES). Branch of 
the City of Yerevan Social-Ecological Alliance (SES). Branch of 
the City of Yoshkar-Ola Social-Ecological Alliance (SES). Branch 
of the City of Krasnoyarsk Social-Ecological Alliance (SES). 
Branch of the City of Moscow Social-Ecological Alliance (SES). 
Branch of the City of Odessa Social-Ecological Alliance (SES). 
Branch of the City of Orshanka Social-Ecological Alliance (SES). 
Branch of the City of Ostashkov Social-Ecological Alliance 
(SES). Branch of the City of Perm Social-Ecological Alliance 
(SES). Branch of the City of Protvino Social-Ecological Alliance 
(SES). Branch of the City of Samara Social-Ecological Alliance 
(SES). Branch of the City of Tbilisi Social-Ecological Alliance 
(SES). Branch of the City of Troitsk Social-Ecological Alliance 
(SES). Branch of the City of Ulyanovsk Social-Ecological 
Alliance (SES). Branch of the City of Ufa Social-Ecological 
Alliance (SES). Branch of the City of Kharkov Social-Ecological 
Alliance (SES). Branch of the City of Cheboksary 
Social-Ecological Council of Informals Architects Union of 
Belarus USSR Journalists Union Alliance for Defense of the Aral 
and the Amu Darya Greens Alliance of Armenia Greens Alliance of 
Georgia Alliance of Communists (Dobryanka) Alliance of 
Communists (Perm) Alliance of Animal Lovers Alliance of Hunters 
and Fishermen's Societies of Kazakhstan Alliance of Hunters and 
Fishermen's Societies of the Russian Federation Writers Union of 
Belarus Writers Union of Kazakhstan USSR Writers Union Writers 
Union of Uzbekistan Alliance of Victims of Nuclear Testing 
Alliance To Promote Perestroyka (See People's Front of 
Checheno- Ingushetia) Soyuzekopress, Information-Publishing 
Association Salvation, Group (St. Petersburg) Salvation, 
Ecological-Political Society (EPOS) (Otradnyy) SPASENIYE, 
Newspaper Save the Dnepr and the Dnepr Region, Public Committee 
Save the Caspian Sea Let Us Save the World and Nature, 
Association Habitat (See Noosphere, Ecology Club [Bryansk]) 
USSR-USA, Friendship Society USSR-France, Friendship Society 
Strogino, Ecology Group Studenets, Society Steps, Studio Theater 
Surgut People's Ecology Society Skhivi, Photocenter Syktyvkar 
Social-Ecological Alliance Tabigat, Greens Party of Kazakhstan 
Taymyr Greens Front Talaka, Sociopolitical Club Tallinn Greens 
Movement Tver Association of Informal Groups Teplyy Stan, 
Ecology Group Tobolsk Ecology Society Tovarystvo Leva. Ecology 
Section Tolyatti Social-Ecological Alliance Grass, Club 
Transnational Radical Party Troitsk Branch of the SES (See 
Social-Ecological Alliance [SES]. Branch of the City of 
Troitsk) Work Day, City Club Tuva Republic VOOP Council Tula 
Oblast Youth Ecological Alliance (TOMES) Tourism, Sport, and 
Recreation, Association Tushino, Ecology Club Ukrainian Peace 
Defense Committee (UKZM) Ukrainian Republic Chernobyl Committee 
Ukrainian Culture Foundation Uly-Tau, Ecology Society UNEKO, 
Detachment Ural People's Front Torch of Rerikh, 
Cultural-Creative Association Fauna Nature Use Federation 
Federation of Socialist Public Clubs (FSOK) Fili, Regional 
Ecology Organization Baikal Foundation Baikal Foundation. Buryat 
Branch Baikal Foundation. Moscow Branch Global Infrastructure 
Fund of Japan Culture Foundation Culture Fund of Lithuania 
Foundation To Support Ecological Education Social Initiative 
Foundation (Nakhodka) Social Initiatives Foundation (Moscow) 
Ecological Inventions Foundation Foundation for the Ecological 
Defense of Brest Oblast Yamal Ecological Defense Foundation 
Frigate, Society Kharkov Oblast Youth Ecology Center for 
Secondary and Primary School Students at the "Ecoforum" 
Association (See Ecoforum, Association. Kharkov Oblast Youth 
Ecology Center for Secondary and Primary School Students) 
Kharkov Branch of the SES (See Social-Ecological Alliance [SES]. 
Branch of the City of Kharkov) Rainbow Keepers Christian 
Greens Movement Christian-Democratic Union (St. Petersburg) 
Christian-Democratic Union of Russia Christian-Ecological 
Alliance of Russia (KhESR) Youth Initiative Center (See Ecology, 
Section (Almaty) Center of Independent Ecology Programs Creative 
Initiative Center Ecology and Resources Center (See Eko, Ecology 
Club [Budennovsk]) Ecological Initiative Center Chelyabinsk 
People's Front. Ecology Section Chermyanka, Ecological Society 
Chernobyl, Belarusian Social-Ecological Alliance Chernobyl, 
Alliance Chernobyl, Alliance. Krivoy Rog Regional Organization 
Chernobyl, Alliance (Kazakhstan) Chernobyl, Alliance 
(Kazakhstan). Semipalatinsk Oblast Branch Black Sea, 
Organization Chuvash Republic Greens Party (See Greens Party of 
Chuvashia) Chance, Organization (Kharkov) Chance, Ecology Club 
(Pervouralsk) Siauliai Club for the Protection of Monuments and 
Nature Eureka, Scientific Apprentice Society of Ecology and 
Regional Studies Exotica, Small Enterprise Eko, Club (Tbilisi) 
Eko, Ecology Club (Budennovsk) EKO/Orbis, Children's Ecology 
Club Eco-Rock, Youth Group Eco-Center (See Ecology Center [ETs] 
[Petropavlovsk-Kamchatskiy]) Ecocentury EKOGANG EkoInfo 
(Yekaterinburg) Ekoinform (See Information Agency on 
Nongovernmental Ecology Organizations) Ecokordon (Krasnodar) 
Ecologist, Club (See Ecology, Club [Novokuznetsk]) Ecologist, 
Club (Bishkek) Ecologist, Club (Ivanovo) Ecologist, Club 
(Lipetsk) Ecologist, Club (Saratov) Ecologist, Club (Tashkent) 
Ecologist, Club at the Pskov Pedagogical Institute Ecologist, 
Society of the USSR Academy of Sciences Noginsk Science Center 
Ecologist, Association (Prokopyevsk) Ecologist, Association 
(Tashkent) Ecological Association (Tashauz) Ecological 
Association (Tyumen) Ecological Association of Nikolayev Oblast 
Ecological Association at the All-Georgian Rustaveli Society 
Ecology Group (Aleksandrovsk) Ecology Group (Kola) Ecology Group 
(Leninsk-Kuznetskiy) Ecology Group (Nodvoitsy) Ecology Group 
(Nikolayevsk-na-Amure) Ecology Group (Pechenga) Ecology Group 
(Stroitel) Ecology Group (Cherdyn) Ecology Group of the 
Severonikel Combine Ecology Group of Krasnoarmeyskiy Rayon 
(Roshchino) Ecology Group of Memorial (See Memorial [Tambov]. 
Ecology Group) Ecology Group of the Bioautomation Scientific 
Research Center (Nizhniy Novgorod) Ecology Group at the 
Socialist Association of Youth of the Leninskiy Raykom of the 
All-Union Komsomol (Nizhniy Novgorod) Ekos Ecology Group (See 
Ekos, Ecology Group [Yartsevo]) Ecological Initiative (Tver) 
Ecological Initiative (Tomsk) Ecological Initiative, Association 
(Dneprodzerzhinsk) Ecological Initiative, Association 
(Kremenchug) Ecological Initiative, Movement (Voronezh) Ecology 
Party of Belarus Ecological Perspective, Committee of the USSR 
Union of Scientific and Engineering Societies Ecology Section 
of the Association of Soviet Esperanto Specialists Ecology 
Section of the Democratic Initiative Movement Ecology Section of 
the Pamyat Historical-Patriotic Association (Novosibirsk) 
(See Pamyat [Novosibirsk]) Ecology Section of the Citizen Club 
(See Citizen Club) Ecology Section of the Citizens Initiative 
Club (See Citizens Initiative, Club) Ecology Section of MOSKh 
[Moscow Agricultural Society] Ecology Section of the Nizhniy 
Novgorod Branch of the Journalists Union Ecology Section at the 
Ryazan Branch of the USSR Geographic Society Ecology Section of 
the Moldova Journalists Union Ecology Section of Tovarystvo Leva 
(See Tovarystvo Leva. Ecology Section) Ecological Initiatives 
"Ecology Herald," Monthly Bulletin Propaganda for the 
Fundamentals of Ecological Knowledge ["Ekologicheskiy 
vseobuch"], Creative Association Ecology Club (Baku) Ecology 
Club (Borovichi) Ecology Club (Groznyy) Ecology Club 
(Yenakiyevo) Ecology Club (Kansk) Ecology Club (Tomsk) Ecology 
Club (Yuzhnyy) Ecology Club (Eko-klub) (Kazan) Ecology Club 
(Ekoklub) (Kyzyl) Ecology Club (Ekoklub) (Minsk) Ecology Club of 
Mikhaylovskiy Rayon Ecology Club at the Newspaper VECHERNYAYA 
ODESSA Ecology Club at the Newspaper VECHERNIY DONETSK Ecology 
Club at the Kasimovskiy Raykom of DOSAAF Ecology Club at the 
Nizhniy Novgorod Mayak Garment Trade Production Association 
Ecology Club at the Nature Protection Society (Kolchugino) 
Ecology Club at the Youth Initiatives Foundation (Penza) 
Scientists' Ecology Club (Lvov) Eko Ecology Club (See Eko, 
Ecology Club [Budennovsk]) Ekos Ecology Club (See Ekos, Ecology 
Club [Ryazan]) Ecology Committee (Angarsk) Ecology Committee 
(Moscow) Ecology Committee (Tyumen) Ecology Committee 
(Chegdomyn) Ecology Committee of the Kamensk-Uralskiy Regional 
Specialists Society Ecology Competition Ecological Alliance 
(Glazov) Ecological Alliance (Groznyy) Ecological Alliance 
(Izhevsk) Ecological Alliance of Belarus (Ekosoyuz) USSR 
Ecological Alliance (Ekosoyuz, ES) Ecology Foundation 
(Yenakiyevo) Ecology Foundation of Kazakhstan Ecology Foundation 
of Oktyabrsykiy Rayon in the City of Moscow USSR Ecology 
Foundation (Ekofond) USSR Ecology Foundation (Ekofond). North 
Caucasus Branch Ecology Center (Kaluga) Ecology Center (ETs) 
(Nakhodka) Ecology Center (ETs) (Petropavlovsk-Kamchatskiy) 
Ecology Movement (Bratsk) Ecology Movement (Ekodvizheniye) 
(Yerevan) Ecological Society (Novomoskovsk) Ecological Society 
(Sergiyev Posad) Ecological Society (Sumgait) Ecological Society 
of Georgia Ecology Branch of the Sociopolitical Initiatives Club 
(See Sociopolitical Initiatives, Club) Ecology, City Debate 
Club (Stavropol) Ecology, Group (Novokuznetsk) Ecology, 
Initiative Group (Kazakhstan) Ecology, Initiative Group 
(Sukhobuzima) Ecology, Club (Volgograd) Ecology, Club (Novgorod) 
Ecology, Club (Novokuznetsk) Ecology, Club (Svetlyy Yar) 
Ecology, Nizhniy Tagil Labor Association Ecology, Oblast Society 
(Ivanovo) Ecology, Public Association (Uvat) Ecology, Society 
(Dzhetygora) Ecology, Society (Cherkassy) Ecology, Association 
(Moscow) Ecology, Section (Almaty) Ecology, Health, and Life, 
Society Ecology-21st Century Ecology and Man (Norilsk) Ecology 
and Journalism, Association Ecology and Health (Berezniki) 
Ecology and Health (Meleuz) Ecology and Health (Meleuz). Salavat 
Branch Ecology and Health (Meleuz). Sterlitamak Branch Ecology 
and Peace (Feodosiya) Ecology and Peace, Association Ecology and 
Peace, Association (Vyatka) Ecology and Peace, Association 
(Crimea) Ecology and Peace, Association (Crimea). Kerch Branch 
Ecology and Public Opinion (EKOM) Ecology and Man Ecology of the 
North, Association Ecowitch ["Ekolokon"], Society Ekomor, 
Scientific Production Association Ekonord, Ecology Center 
Ekopolis, Experimental Creative Studio Ekopolis-Kosino, Club 
Ekopolis of the World, Russian Association Ekopress, Center 
Ekos, Youth Environmental Defense Club (Tuapse) Ekos, Ecology 
Group (Yartsevo) Ekos, Ecology Club (Ryazan) Ecosphere, Working 
Group Ekofam Ecoforum, Association. Kharkov Oblast Youth Ecology 
Center for Secondary and Primary School Students Ecocenter, 
Ecology Organization of Secondary Students and Young People 
Ecocenter (Makhachkala) Ecocenter (See Ecology Center [ETs] 
[Petropavlovsk-Kamchatskiy] ELTEKS, Association of Ecological 
Small Enterprises and Cooperatives Energy 2050, Moscow Power 
Engineering Institute Club Enio, All-Union Association of 
Applied Eniology (VA Enio) Epicenter Era, Ecology Group Estonian 
Greens Movement Estonian Nature Protection Society (Eesti loodu 
skaitse selts [ELKS]) Estonian Nature Protection Society. 
Tukhalaskiy Section Southern Bug, Ecology Club Young 
Ecologist-Tourists, Experimental Scientific-Sports Circle Yurga 
Branch of the Noosphere Club Nuclear Safety, Movement Japan-USSR 
Yaroslavl People's Front (See People's Front [Yaroslavl]. 
Ecology Section) Yauza, Public Council 
<H5>  Mass Information Media Index </H5>
  5 IYUNYA [5 June], Herald-Almanac (Green Squad) 
  BART, Information Bulletin (People's Front of 
Checheno-Ingushetia) 
  BYULLETEN [Bulletin] (Social-Ecological Committee [Perm]) 
  BYULLETEN (Ecology and Public Opinion) 
  "Bioshield," Film (All-Russian Nature Protection Society) 
  VESTNIK [Herald] (Nature Protection Squads Movement) 
  VESTNIK KOMITETA SODEYSTVIYA PERESTROYKE [Herald of the 
Committee To Promote Perestroyka] (Komsomolsk-na-Amure) 
  VESTNIK NARODNOGO FRONTA TATARSKOY ASSR [Herald of the 
People's Front of the Tatar ASSR] 
  VESTNIK OBSHCHESTVA ZASHCHITY BAYKALA [Herald of the Society 
for the Defense of Baikal] 
  VESTNIK PATRIOTICHESKOGO OBYEDINENIYA OTECHESTVO [Herald of 
the Fatherland Patriotic Association] (Tyumen) 
  VESTNIK SOVETA PO EKOLOGII KULTURY [Herald of the Council 
for 
the Ecology of Culture] 
  Vieda, Ecological Education Publishing House 
  Volnke [Kray], Publishing House (Kazakhstan Regional 
Specialists Society) 
  "Vsya nasha zhizn. Vestnik Sotsialno-ekologicheskogo soyuza" 
[All Our Life. Herald of the Social-Ecological Alliance], 
Anthology of Materials (Social-Ecological Alliance) 
  GRAZHDANIN, Journal (Ecology Center [Nakhodka]) 
  DEMOKRATICHESKIY VESTNIK [Democratic Herald] (Society for 
the 
Defense of Baikal) 
  YEDINSTVO [Unity], Journal (Pamyatnik) 
  "Zazerkalye" [Beyond the Mirror], Anthology of Materials 
(Bureau of Ecological Developments) 
  "Green Wave," Television Program (Greens Movement of 
Lithuania) 
  "Green Book" (Regular Page of the Nature Association in the 
Newspaper KOMSOMOLETS 
  ZELENAYA LITVA [Green Lithuania], Newspaper (Greens Movement 
of Lithuania) 
  "Green Thread," Information Agency (Greens Party) 
  "Green Thread," Radio Russia Program (Russian Greens Party) 
  ZELENIY SVIT [Green World] (Zeleniy svit, Ecological 
Association) 
  ZELENYY KVADRAT [Green Quadrant], Samizdat Journal (Free 
Student Green League) 
  ZELENYY KREST [Green Cross], Journal (Noosphere, All-Union 
Ecological Association) 
  ZELENYY MIR [Green World], Ecology Newspaper 
  ZEMLYA [Earth], Weekly (has a regular rubric of the Greens 
Movement) 
  IZBIRATEL [Voter], Newspaper (Nevada-Semipalatinsk) 
  IZVESTIYA ESTONSKOGO OBSHCHESTVA OKHRANY PRIRODY [News of 
the 
Estonian Nature Protection Society] 
  INFORMATSIONNYYE PISMA ECOLOGICHESKOGO DVIZHENIYA 
[Information Letters of the Ecology Movement] (Social-Ecological 
Alliance) 
  INFORMATSIONNYY BYULLETEN [Information Bulletin] (Promotion 
of Perestroyka) 
  INFORMATSIONNYY BYULLETEN [Information Bulletin] (Ecology 
Center [Nakhodka]) 
  INFORMATSIONNYY LISTOK [Information Sheet] (Independent 
Alliance) 
  INFORMATSIONNYY LISTOK [Information Sheet], Appendix to the 
Journal OKRAINA 
  KOLOKOL, Journal (Social Initiative) 
  KOMSOMOLETS, Newspaper (See "Green Book") 
  "Kray" (See Volnke) 
  LUCH, Monthly Newspaper (Nature Protection Committee of Perm 
Oblast) 
  "Metodologiya nauchnoy (ekologo-sotsialno-ekonomichekoy) 
expertizy proyektov i khozyaystvennykh nachinaniy" [Methodology 
of Scientific (Ecological-Social-Economic) Expert Studies of 
Projects and Economic Undertakings," brochure (USSR Ecological 
Alliance) 
  MOSKOVSKIY EKOLOGICHESKIY BYULLETEN [Moscow Ecology 
Bulletin] 
(Ecology and Journalism, Association) 
  NABAT, Interrepublic Ecology Newspaper (Chernobyl, 
Belarusian 
Social-Ecological Alliance) 
  NASLEDIYE [Legacy], Newspaper (Altair, Agency [Chisinau]) 
  NEZAVISIMAYA GAZETA [Independent Newspaper] (Ecology and 
Public Opinion) 
  NORCHI LENINELI, Newspaper (Greens Alliance of Georgia) 
  OBSHCHINA [Commune], Journal (Salvation, Group [St. 
Petersburg]) 
  OKNO GLASNOSTI [Glasnost Window], Bulletin (Counter 
Movement, 
Amateur Patriotic Association) 
  OKRAINA [Suburbs], Social-Literary Journal (Work Day, City 
Club) 
  OKRAINA [Suburbs], Wall Newspaper (Work Day, City Club) 
  "Weather for Tomorrow," (Regular Rubric of the Greens 
Movement in the Journal SELSKAYA MOLODEZH) 
  POLUSVIRA [Balance], Newspaper (Greens Party of Lithuania) 
  "Pochtovyy yashchik" [Post Office Box] (Cultural-Ecological 
Club [Kharkov]) 
  PUT K KOMMUNIZMU [Path to Communism], Newspaper (Aktyubinsk 
Ecologist. Monthly reports are published.) 
  "Balance" (See POLUSVIRA) 
  "Rivers of Our Childhood," Film (All-Russian Nature 
Protection Society) 
  SVETOCH, Journal (Torch of Rerikh) 
  SELSKAYA MOLODEZH [Rural Youth], Journal (See "Weather for 
Tomorrow") 
  "Sotsialno-ekologicheskiy soyuz. 
Informatsionno-metodicheskoye pismo, sbornik materialov" 
[Social-Ecological Alliance. Information-Methodological Letter, 
Anthology of Materials] (Social-Ecological Alliance) 
  SPASENIYE [Salvation], Weekly Ecology Newspaper 
  STRABURAGS, Journal (Environmental Defense Club [Vizes 
Aizsargs Klub (VAK)]) 
  TVERSKOY KOLOKOL [Tver Bell], Journal (Social Justice) 
  TRETIY PUT [Third Path], Amateur Journal (Greens Party 
together with the Ecological-Political Club Alternative [Samara]) 
  CHELOVEK I MIR [Man and the World], Journal 
(Social-Ecological Committee [Perm]) 
  "Scars of War and Wounds of Peace," Film (All-Russian Nature 
Protection Society) 
  EKOKURYER [Ecocourier], Information Bulletin (Ecology 
Center) 
[Petropavlovsk-Kamchatskiy]) 
  EKOLOGICHESKAYA GAZETA [Ecology Newspaper] (All-Russian 
Nature Protection Society) 
  "Ecological Expedition in the Moscow Region," Central 
Television Program (USSR Ecological Alliance) 
  EKOLOGICHESKIY BYULLETEN [Ecology Bulletin] 
(Aral-Asia-Kazakhstan, Committee) 
  EKOLOGICHESKIY VESTNIK [Ecology Herald], Newspaper (Green 
World [Krasnoyarsk]) 
  EKOLOGICHESKIY VESTNIK [Ecology Herald], Newspaper 
(Committee 
To Save the Pechora) 
  EKOLOGICHESKIY VESTNIK [Ecology Herald], Monthly Bulletin 
(Tuva Republic VOOP Council) 
  "Ecology, Problems and Us," Film (Greens Alliance of 
Georgia) 
  "Ekologiya i selskoye khozyaystvo" [Ecology and 
Agriculture], 
Anthology of Materials (Ecology and Peace, Association) 
  "Ekofact," Anthology of Materials (Social-Ecological 
Alliance) 
  EKOS, Journal (Social-Ecological Alliance) 
  GREENPEACE, Newspaper (Green World-Rebirth) 
<H5>  INDEX OF POPULATED POINTS </H5>
  Abovyan Aktau Aktyubinsk Aleksandrovsk Aleksin Almaty Amursk 
Angarsk Apatity Aralsk Arsenyev Arkhangelsk Assa Astrakhan Baku 
Balakovo Balashikha Bolshevo-1 Baranovichi Barnaul Belozerka 
Berezniki Biysk Bishkek Blagoveshchensk Bobrov Bobruysk 
Bogorodsk Bor Borovichi Borovsk Bratsk Brest Bryansk Budennovsk 
Burnoye Ventspils Vidzema Vidnoye Vilnius Vladikavkaz Vladimir 
Vladivostok Voznesensk Volgodonsk Volgograd Vologda Volokolamsk 
Volzhskiy Vorkuta Voronezh Voskresensk Vrangel Vyksa Vyatka 
Gayvoron Glazov Gomel Gorlovka Gorno-Altaysk Gorkiy (See Nizhniy 
Novgorod) Groznyy Gudermes Guzeripl Gus Khrustalnyy Dalnegorsk 
Dalnerechensk Dzhambul Dzhezkazgan Dzhetygora Dzerzhinsk 
Dimitrovgrad Dneprodzerzhinsk Dnepropetrovsk Dobryanka 
Dolgoprudnyy Donetsk Dubna Dubovki Dushanbe Yekaterinburg 
Yenakiyevo Yerevan Zheleznogorsk Zaporozhye Zarasay Zarechnyy 
Zarya Zvenigorod Zeya Ziadin Zlatoust Ivanovo Ivanovo-Frankovsk 
Izhevsk Ilyichevsk Ionovo Irkutsk Yoshkar-Ola Kazan Kazatin 
Kalinin (See Tver) Kaliningrad Kaliningrad (Moscow Oblast) 
Kaluga Kaluga (Ivanovo-Frankovsk Oblast) Kalush Kamensk-Uralskiy 
Kansk Kasimov Karaganda Karaul Kaunas Kezhma Kemerovo Kerch 
Kzyl-Orda Kiev Kirishi Kirov (See Vyatka) Kirovsk Chisinau 
Klaipeda Kobrin Kokchetav Kola Kolomna Kolchugino 
Komsomolsk-na-Amure Kondinskoye Kondopoga Korkino Kosino-1 
Kostomuksha Kostroma Kramatorsk Krasnodar Krasnoyarsk Kremenchug 
Krivoy Rog Kstov Kuybyshev (See Samara) Kuril Islands Kursk 
Kurchatov Kusa Kyzyl Kedlpiai Labytnangi Leningrad (See St. 
Petersburg) Lenino Leninogorsk Leninsk-Kuznetskiy Lesnaya 
Tarnovnitsa Liepaja Lipetsk Listvyansk Lugansk Lvov Magadan 
Magnitogorsk Mazieikiai Maykop Mariupol Makhachkala 
Medvezhyegorsk Meleuz Minsk Mikhaylov Mogilev Monchegorsk Moscow 
Mochalishche Mukachevo Murmansk Mytishchi Nadvoitsy Nalchik 
Nakhodka Nepetsino Nefteyugansk Nizhniy Novgorod Nizhniy Tagil 
Nikolayev Nikolayevsk-na-Amure Nikopol Novgorod Novoamvrosiyevsk 
Novodvinsk Novokuznetsk Novokuybyshevsk Novomoskovsk Novopolotsk 
Novorossiysk Novosibirsk Novocheboksarsk Novocherkassk Novyye 
Aneny Norilsk Nugush Nukus Obninsk Odessa Omsk Orel Orenburg 
Orshanka Ostashkov Otradnyy Pavlodar Panayarve Panevezhis Penza 
Pervomaysk Pervouralsk Pereyaslavl-Zalesskiy Perm Petrozavodsk 
Petropavlovsk Petropavlovsk-Kamchatskiy Pechenga Pechora Poltava 
Pravdinsk Provideniya Prokopyevsk Protvino Pskov Pudozh 
Pushchino Pyatigorsk Rakhov Riga Rozdan Rostov Rostov-na-Donu 
Roshchino Rybatskiy Rybinsk Ryazan Salavat Salekhard Samara St. 
Petersburg Saran Saratov Sayanogorsk Sverdlovsk (See 
Yekaterinburg) Svetlyy Yar Svisloch Sviyazhsk Sevastopol 
Severobaykalsk Semikarakorsk Semipalatinsk Sergiyev Posad 
Simferopol Smirnykh Smolensk Sosenki Sosnovyy Bor Sochi 
Stavropol Staryy Saltov Stakhanov Stepnogorsk Sterlitamak 
Stroitel Subochi Suzdal Sumgait Sumy Surgut Sukhobuzima 
Syktyvkar Taldy-Kurgan Tallinn Tambov Tartu Tautininkay Tashauz 
Tashkent Tbilisi Tver Temirtau Ternopol Tobolsk Tolyatti Tomsk 
Tomsk-7 Troitsk Tuapse Tula Tyumen Uvat Ulan-Ude Ulyanovsk 
Ulytau Uralsk Ussuriysk Ust-Ilimsk Ust-Kamenogorsk Ufa Ukhta 
Feodosiya Fergana Frunze (See Bishkek) Khabarovsk Kharkov Khimki 
Khmelnitskiy Khomutovka Khotkovo Tsimlyansk Chapayevsk 
Chapayevsk-5 Cheboksary Chegdomyn Chelyabinsk Cherdyn 
Cherepovets Cherkassy Chernobyl Chernovtsy Chernogolovka Chita 
Chuguyevka Siauliai Shevchenko (See Aktau) Ekibastuz Elista 
Yuzhno-Sakhalinsk Yuzhnyy Yurga Jurmala Yakutsk Yaroslavl 
Yartsevo Yatvez 


'''

text2 = '''

<DOC>
<DOCNO> FBIS3-60342 </DOCNO>
<HT>    "jpten001__l94001" </HT>


<HEADER>
<AU>   JPRS-TEN-94-001L </AU>
Document Type:JPRS 
Document Title:Environmental Issues 

</HEADER>

<ABS>  Directory of Ecological Organizations on the Territory of </ABS>


<TEXT>
the Former USSR 
<DATE1>  14 January 1994 </DATE1>
<F P=100></F>
<H3> <TI>     Directory of Ecological Organizations on the Territory of 
the Former USSR </TI></H3>
<F P=102>  93WN0655A Moscow SPRAVOCHNIK: EKOLOGICHESKIYE ORGANIZATSII 
NA TERRITORII BYVSHEGO SSSR in Russian 1992 pp 1-158--FOR </F>

OFFICIAL USE ONLY 
<F P=103> 93WN0655A </F>
<F P=104>  Moscow SPRAVOCHNIK: EKOLOGICHESKIYE ORGANIZATSII 
NA TERRITORII BYVSHEGO SSSR </F>

 Language: <F P=105>Russian </F>
Article Type:CSO 

<F P=106> [Text of directory of the RAU Press Information Agency </F>
Institute of Mass Political Movements in Moscow] 
  [Text] 
<H3>  RAU Corporation RAU Press Information Agency Institute of 
Mass Political Movements </H3>
  Ecological Organizations on the Territory of the Former 
USSR. 
Directory 
  RAU Press Publishing House Moscow 1992 BBK N-53 
  Compiling authors: Ye. N. Kofanova and N. I. Krotov. 
  Author of the article and scientific editor: A. B. Shubin. 
  Scientific editor of "Kazakhstan" chapter: A. M. Dzhunusov. 
  Editor and compiler of the index: N. N. Silin. 
  Taking part in the work were: A. V. Zudin, A. Ye. 
Kvatkovskiy, A. V. Koroleva, S. Yu. Kutukov, I. A. Nevskaya, G. 
V. Prokofyeva, and V. Yu. Khabidulin. 
  Ecological Organizations on the Territory of the Former 
USSR. 
Directory Moscow: RAU Press Publishing House, 1992. ISBN 
5-86014-052-5 
  This directory contains the most complete information on 818 
ecological organizations on the territory of the former USSR. 
  The publication is intended primarily for scientific 
workers, 
graduate students, teachers, students, and organizers of nature 
protection work, as well as all those who are interested in the 
contemporary ecology movement. 
  P 0803010200/594(03) - 92 Without declaration BBK N-53 
  The computer original was prepared by N. N. Silin using the 
"Russkoye slovo" (c) SP Para Graf package, which includes the 
word processing program MicroSoft Word 5.0 (c). 
  The format is 84 x 108 1/8. Book and journal paper. Offset 
print. 
  3,000 copies printed. Book price is by contract. Printed at 
the VAAP [All-Union Agency for Authors' Rights] Printing Plant. 
  ISBN 5-86014-052-5 
  Y. N. Kofanova, N. I. Krotov. Compilation, 
commentaries, reference articles, 1992. 
  A. M. Dzhunusov, Ye. N. Kofanova, N. I. Krotov. 
Compilation, commentaries, reference articles, the chapter 
"Kazakhstan," 1992. 
  A. V. Shubin. Introductory article, 1992. 
<H5>  FOREWORD </H5>
  To the reader! 
  This directory includes information on 818 ecological 
organizations operating on the territory of the former USSR 
(there are explanatory articles on 551 of them and another 267 
are mentioned). The states which were part of the Union still 
have a great deal in common, among other things, a grave 
ecological situation. And there are common patterns which can be 
traced in the history of the "Green" organizations here. 
  The stages of the development of the ecology movement and 
the 
classification of Green organizations by several criteria are 
presented in an article by Aleksandr Shubin, historian and 
cochairman of the Russian Greens Party. This article is placed 
at the beginning of the directory. 
  Data on organizations are combined into two chapters: 
  1. Interrepublic organizations (operating on the territory 
of 
all or several former Union republics); 
  2. Republic and local organizations. 
  Within the chapters devoted to a particular republic they 
are 
placed in the following order: 

  -  republic organizations, 
  -  the capital's organizations 
  -  organizations in oblasts, krays, and republics which are part 
of the Federation (oblast organizations, organizations of the 
oblast center, and organizations of populated points). 

    The directory has alphabetical indexes of names, 
nongovernmental organizations mentioned (the pages where the 
explanatory article is found are set off in italics 
[not given in English translation]), mass information media, and 
populated points. 
  The data on organizations are presented in items of 
information which usually tell the organization's size, age, and 
social make-up, the history of its creation and activity, the 
sources of financing, mass information media (set off in 
italics [given in all capital letters in English 
translation]), and other things. Then the addresses and contact 
telephone numbers and a short bibliography (set off in 
italics [merely listed in English translation]) are 
indicated. 
  The following were the primary materials used in working on 
the directory: 
  USSR Goskomprirody [USSR State Committee for Protection of 
Nature and Natural Resources]; 
  archives of the RAU Press Agency Institute of Mass 
Political Movements; 
  Galkina, L., "Zelenyye v SSSR. Spravochnik" ["Greens in 
the USSR. Directory"], Moscow, 1991; 
  "Zelenyye v SSSR. Krupneyshiye organizatsii i dvizheniya: 
kratkiy spavochnik" ["Greens in the USSR. Large Organizations 
and Movements: Short Directory"], Lika Information Research 
Center, Moscow, 1990; 
  catalog prepared by USSR Goskomprirody; 
  personal archives of A. V. Shubin; 
  personal archives of A. M. Dzhunusov; 
  "Rossiya: partii, assotsiatsii, soyuzy, kluby. 
Spravochnik" [Russia: Parties, Associations, Alliances, and 
Clubs. Directory"], Moscow, RAU PRESS, 1991, volume 1, parts 1-2; 
  "Spravochnik politicheskikh i obshchestvenyykh 
organizatsiy Latvii s kommentariyami" ["Directory of Political 
and Public Organizations of Latvia with Commentaries"], compiled 
by I. Kudryavtsev, Moscow, Moscow Public Bureau of Information 
Exchange, 1990; 
  "Spravochnik `Ekologicheskiye organizatsii.' 90 gorodov" 
["`Ecology Organizations' Directory. 90 Cities"], 
INFORMATSIONNYY BYULLETEN SMOT, No 75, January 1992; 
  "Samodeyatelnyye obshchestvennyye organizatsii (SOO) 
Kazakhskoy SSR (spravochnik)" ["Non-Professional Public 
Organizations (NPO) of the Kazakh SSR (Directory)"], Almaty, 
1990. 
  Newspapers of various political orientations and various 
regions (starting in 1987) were also studied. 
  The authors thank everyone who submitted information on the 
Greens organizations to us. 
  We will be grateful for all suggestions, comments, 
programs and by-laws of ecological organizations, information on 
their activities, excerpts from newspapers, "samizdat" material, 
and so on sent to the following address: 103104, Moscow, 
Tverskoy bulvar, 7/2, Institut massovykh politicheskikh 
dvizheniy (RAU-Korporatsiya) [Institute of Mass Political 
Movements (RAU Corporation)], telephone 202-05-85, Nikolay 
Ivanovich Krotov and Yelena Nikolayevna Kofanova. 
  At the present time work is being completed in our institute 
on a computer version of the directory which will also include 
materials accumulated in the institute's archives which were not 
part of this publication. A second edition (revised and 
enlarged) of this directory is being prepared. 
<H5>  BASIC ABBREVIATIONS USED </H5>
  AN--Academy of Sciences AO--autonomous oblast 
APK--agroindustrial complex APN--Novosti Press Agency 
AST--atomic heat plant ATS--telephone exchange AES--atomic power 
plant BVK--protein-vitamin concentrates VASKhNIL--All-Union 
Academy of Agricultural Sciences imeni V. I. Lenin VS--Supreme 
Soviet g.--year g.--city GK--city committee GU--state university 
GES--hydroelectric power plant d.--building DK--House of Culture 
DOSAAF--Voluntary Society for Assistance to the Army, Air Force, 
and Navy DS--Democratic Union IGP--Institute of the State and 
Law IMPD--Institute of Mass Political Movements 
ITR--engineering-technical worker kv.--apartment KGB--State 
Security Committee kom.--room korp.--block KPK--party control 
committee KPSS--Communist Party of the Soviet Union M.--Moscow 
MID--Ministry of Foreign Affairs mkrn.--microrayon MO--Ministry 
of Defense MP--small enterprise NII--scientific research 
institute NITs--scientific research center 
<H3>  A. SHUBIN: THE ECOLOGY MOVEMENT IN THE USSR AND THE 
COUNTRIES WHICH EMERGED FROM IT </H3>
  The ecology movement is a diverse and in many respects 
unique 
phenomenon which appeared in our countries in the second half of 
the 20th century. The lack of such a movement in the 
prerevolutionary history of Russia caused some serious 
differences between the domestic ecology movement and other 
social trends. Ecologists did not have a domestic tradition to 
which they could turn. The result of that was the initially slow 
rate of evolution of the ecology movement, the importance of 
Western experience for it, the lack of an independent positive 
ideal for a long time, and other things. 
  Just as in other industrial countries, the appearance of the 
ecology movement was caused by the crisis of the industrial 
system in a particular stage of its development. The attempt to 
implement the scientific-technical revolution by preserving the 
industrial structures of vertical management of production 
aggravated the ecological crisis, while the parallel development 
of social self-awareness and ordinary literacy in the natural 
sciences sphere made people willing to oppose the process of the 
destruction of the environment and man. 
  Industrial man, alienated from decision making, from 
information, and from nature itself, crowded in cities, and 
oppressed at the factory and at home, began to understand his 
position. He had become so complex that he could no longer 
fulfill his role of a specialized cog in the industrial machine 
on which industrial civilization is based. 
  Despite the universality of the causes of the appearance of 
the ecology movement in various countries of the world, its 
genesis in the USSR had its own particular features. Above all 
it occurred under conditions of a supermonopolized 
state-industrial system. The high degree of monopolization in 
all spheres of life determined the system's destructiveness in 
relation to nature and man. Police and political control over 
any kind of manifestation of public activism made it more 
difficult for the reaction to this destruction to develop. 
  At the same time, however, society's lack of influential 
social subjects independent of the party and state made its 
paternalistic function develop. The state attempted to protect 
its subjects from its own parts. As soon as the ecological 
problem began to be recognized by the official community (and 
that happened during the "thaw" of 1953-1964), "the party and 
the state" took some steps to increase control over certain 
violations of ecological standards (above all by private 
citizens). 
  Social activism which was directed against these violations 
but did not affect political aspects was also legalized. 
  Thus began the first INDUSTRIALIZED period of the 
ecology movement (approximately 1958-1982). During this period 
the movement was typically built into the structures of official 
public organizations like the All-Union Nature Protection 
Society (VOOP). But within the framework of these structures 
informal associations arose--Nature Protection Squads (DOP's). 
The first DOP's were formed in the early 1960s and in 1968-1972 
became a system which encompassed the entire country. This 
system was focused above all on the struggle against poaching 
and cautious, only within the framework of the law, restraint of 
the most flagrant manifestations of industrial expansion. 
  After the "thaw" was curtailed, the system of the nature 
protection movement became a refuge for the liberal-minded 
intelligentsia, above all youth, who in the DOP's and inspection 
offices of VOOP could find an opportunity to serve society 
outside state structures in relatively autonomous and not very 
bureaucratized groups, an opportunity which was very scarce at 
that time. Participation in DOP's and VOOP inspection offices by 
people with "unorthodox" views threatened the existence of these 
very organizations. This promoted the formulation of a unique 
ethical principle which excluded the political orientation of a 
nature protection group. "Our business is ecology." 
  The romance of the DOP's contrasted with the "orderliness" 
of 
"developed socialism" and provided an opportunity to temporarily 
escape the all-encompassing industrial system. At the same time, 
however, the state was able to channel this social activism in 
the direction it needed. Nevertheless, accumulated experience 
with the institutionalized nature protection movement allowed 
people to gradually come to the conclusion that large-scale 
ecological problems could not be solved within the framework of 
the official structures. 
  The rapid buildup of ecological problems in the second half 
of the 1970s and early 1980s also promoted this awareness. The 
attempt to deal with this wave of violations, which were the 
result of objective economic and social causes and the "sins of 
the system," led to an increasing number of confrontations 
between the nature protection movement and the system's 
influential links--beginning with bureaucratic poachers and 
ending with the ministries which joined the initiative to 
"reverse the flow of the northern rivers." Ecologists were made 
to understand that they were interfering in what was not their 
business. The crisis of the movement brought a new stage of the 
movement into being--the PETITION stage 
(approximately 1982-1989). 
  This stage was characterized by the greater independence and 
larger scale of the ecology movement. It still remained a nature 
protection movement and appealed primarily to the authorities, 
intending to change their particular decisions and at the same 
time not change the system. But the ecology movements and groups 
independently selected the object of the attack without taking 
into account the elite's position and resorted to mass 
mobilization means--they called on the population and proposed 
that they support the appeal to the authorities. 
  During this period the movement acquired a primarily 
negativistic orientation. Ecologists spoke out against the most 
destructive installations and projects, hoping to restrain 
industrial expansion and localize its harmful consequences. Such 
a strategy in the ecological organizations united people of the 
most diverse views, from conservative-ethnocratic to anarchist. 
  The first mass campaign of this stage ended in success. In 
1986 the "river reversal" project, which had originally been 
supported by the country's highest leadership (including the 
"architects of perestroyka"), was canceled, although the former 
system of water management was preserved and the problems of 
water supply which "reversing the rivers" was supposed to 
resolve continued to worsen. 
  The position of the country's leaders in relation to the 
growing ecology movement in this stage was relatively favorable. 
The protest of the citizens driven to desperation was directed 
against the local bureaucratic leadership and fit the strategy 
of "pressure from below" which was supposed to make the local 
clans more conciliatory toward the "perestroyka leadership." The 
"fathers of perestroyka" appealed to the public; they needed a 
powerful public movement, but one which would not encroach upon 
the foundations of the system, that is on the highest 
leadership's authority. 
  The original "apolitical nature" of the movement and the 
"patriotic" conservatism (which later took on an anticommunist 
slant) of many of its leaders from the writers' milieu, the 
concentration on particular objects, and the lack of a 
constructive program seemed to guarantee that the process was 
under control. 
  However, it became explosive. The years 1987-1989 were the 
most productive from the standpoint of the number of movements 
which arose and the scale of demonstrations. The need to 
coordinate efforts in the petition and rally campaigns brought 
broad associations of ecological organizations and movements to 
life. In 1987-1988 the Social-Ecological Alliance (SoES) 
emerged. In 1989 the even broader Greens Movement emerged. About 
a million people participated in the campaign against the 
construction of the Volga-Chogray Canal. 

</TEXT>
'''

text3 = '''

</P>
</LENGTH>
<HEADLINE>
<P>
TOP 10 NEW YORK EXCHANGE LOSERS 
</P>
</HEADLINE>
<TEXT>
<P>
List includes only common stocks and reflects stock splits and dividends. Not 
included are stocks whose 1988 closing price was below $2. 
</P>
<TABLE CWL="3.43IN:2.44IN:2.33IN:4.20IN" WDM="ABS" NCOLS="4">
<ROWRULE>  </ROWRULE>
<TABLEROW>
<CELLRULE>  </CELLRULE>
<TABLECELL CHJ="C" CVJ="C">
</TABLECELL>
<CELLRULE>  </CELLRULE>
<TABLECELL CHJ="C" CVJ="C">
Close (] 
</TABLECELL>
<CELLRULE>  </CELLRULE>
<TABLECELL CHJ="C" CVJ="C">
Yr. to date 
</TABLECELL>
<CELLRULE>  </CELLRULE>
<TABLECELL CHJ="C" CVJ="C">
</TABLECELL>
<CELLRULE>  </CELLRULE>
</TABLEROW>


'''


#
# dic = p.parseDoc(text3)
# doc = dic.termDocDictionary_term_termData
# print('ok')


#
# gaps = '''
# 22:41:281:20:24:22:1:65:117:1173:442:1022:474:381:119:27:75:151:183:4:546:4:180:27:30:5:126:43:37:38:14:45:379:20:181:73:8:5:142:50:264:25:71:187:70:435:169:15:47:79:82:194:100:117:1:22:91:830:435:227:5:2:5:1:8:5:7:6:3:6:6:3:11:255:75:218:16:169:24:131:123:103:14:198:15:100:15:4:113:23:140:123:7:160:18:17:38:5:5:8:5:4:15:4:14:4:411:167:141:4196:550:420:1510:2798:3599:435:229:142:133:87:193:21:35:218:168:181:46:285:8:6:36:22:16:12:29:32:36:15:9:4:63:226:3:50:104:29:1:3:12:27:53:56:15:34:8:6:22:7:19:91:65:112:17:20:17:11:1:16:8:194:100:3:41:27:10:9:10:6:17:3:30:5:5:62:16:16:14:15:48:85:21:33:15:30:86:53:7:117:57:21:16:36:9:51:50:6:40:186:53:2:125:72:68:46:18:107:18:28:14:14:76:8:44:74:35:35:28:54:1809:2223:365:3288:846:587:2231:42:12:25:53:39:115:60:49:38:76:148:35:22:69:50:60:50:78:109:72:264:238:4902:467:7184:1024:5102:396:533:37:277:186:10:3:6:2:3:3:6:4:156:148:145:163:307:301:22:362:140:44:101:134:364:199:182:78
# '''
#
#
# print('***************\n\n')
# splittedGaps = gaps.split(':')
# last = 0
# newList = []
# for g in splittedGaps:
#     g = int(g) + last
#     last = g
#     newList.append(str(g))
#
# print(':'.join(newList))
# print('\ncount:',gaps.count(':') + 1)



