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
        try:
            city = self.geoCoder.geonames(cityName, key = self.usename)

            # city = self.geoCoder.get(cityName,key = self.usename)
            if city is None or self.dictionary_country_currencyPopulation.get(city.country_code) is None:
                print (cityName )
                return None


            return [city.country, str(self.dictionary_country_currencyPopulation[city.country_code][0]), str(self.dictionary_country_currencyPopulation[city.country_code][1])]
        except Exception as err:
            print(err)
            return None

    def getInformationAsString(self, cityName):
        return '|'.join(self.getInformation(cityName))


# cityAPI = CityAPI()
# print(cityAPI.getInformation('Aemstedam'))
#
#
#
# g = geocoder.geonames('New York', key='myengine', featureClass='A')
# print(g.address)
# restCountries = RestCountries()
# all = restCountries.all()
# country = all[0]
# print(country.currencies)
# country.
# for country in all:
#     print (country)


# germany = pycountry.countries.get(alpha_2='DE')
# print (germany)
# currencyList = list(pycountry.currencies)
# for i in range(0,len(currencyList)):
#     print (currencyList[i])