import pycountry
from restcountries.api import RestCountries
from restcountries.api import Country
import geocoder


class CityAPI:

    def __init__(self):
        self.usename = 'myengine'
        self.geoCoder = geocoder
        self.dictionary_country_currencyPopulation = {}

        restCountries = RestCountries()
        countryList = restCountries.all()
        for country in countryList:
            countryName = country.alpha2Code
            countryCurrencyName = country.currencies[0].name
            countryPopulation = country.population

            self.dictionary_country_currencyPopulation[countryName] = (countryCurrencyName,countryPopulation)


    def getInformation(self, cityName):
        """
        get all the information we need
        :param cityName: the city name
        :return: the information as a format: Country, currency, population
        """
        city = self.geoCoder.geonames(cityName, key = self.usename,featureClass='A')

        print (city.country_code)
        print (city.population)
        print (self.dictionary_country_currencyPopulation[city.country_code])

        return city.counryself.dictionary_country_currencyPopulation[city.country_code][0],self.dictionary_country_currencyPopulation[1]


cityAPI = CityAPI()
cityAPI.getInformation('tel')



g = geocoder.geonames('New York', key='myengine', featureClass='A')
print(g.address)
restCountries = RestCountries()
all = restCountries.all()
country = all[0]
print(country.currencies)
# country.
# for country in all:
#     print (country)


# germany = pycountry.countries.get(alpha_2='DE')
# print (germany)
# currencyList = list(pycountry.currencies)
# for i in range(0,len(currencyList)):
#     print (currencyList[i])