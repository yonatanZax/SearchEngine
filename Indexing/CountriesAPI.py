import pycountry
from restcountries.api import RestCountries
from restcountries.api import Country
import geocoder
from Parsing.ConvertMethods import convertNumToKMBformat
import requests
import json



class CityAPI:

    def __init__(self):
        self.usename = 'myengine'
        self.geoCoder = geocoder
        self.dictionary_country_currencyPopulation = {}
        self.dictionary_CapitalCity_country = {}

        self.restCountries = RestCountries()
        countryList = self.restCountries.all()
        for country in countryList:
            countryCode = country.alpha2Code
            countryCurrencyName = country.currencies[0].name
            countryPopulation = country.population
            capitalCity = country.capital

            self.dictionary_country_currencyPopulation[countryCode] = (countryCurrencyName,countryPopulation)
            self.dictionary_CapitalCity_country[capitalCity] = (countryCode, country.name)


    # def getDetailsWithGeobytes(self, cityName):
    #     from io import StringIO
    #     import os
    #     try:
    #         session = requests.Session()
    #         js_stream = requests.get('http://gd.geobytes.com/GetCityDetails?callback=&fqcn=' + cityName.replace(' ','&'))
    #         content = js_stream.text
    #         dictionary = json.loads(content)
    #         country = dictionary['geobytescountry']
    #         currency = dictionary['geobytescurrency']
    #         population = dictionary['geobytespopulation']
    #
    #         if len(country) < 2:
    #             return None
    #
    #         return [country, currency, population]
    #     except Exception as ex:
    #         print("City wasn't found: " , cityName)
    #         return None


    # def getDetailsWithGeobytesWithSession(self, cityNameList):
    #     from io import StringIO
    #     import os
    #     citiesDictionary = {}
    #     with requests.Session() as session:
    #         for cityName in cityNameList:
    #             try:
    #                 result = session.get('http://gd.geobytes.com/GetCityDetails?callback=&fqcn=' + cityName.replace(' ','&'))
    #
    #             except Exception as ex:
    #                 print("City wasn't found: " , cityName)
    #                 print(str(ex))
    #                 continue
    #             content = result.text
    #             dictionary = json.loads(content)
    #             country = dictionary['geobytescountry']
    #             if len(country) < 2:
    #                 print("City wasn't found: " , cityName)
    #
    #                 continue
    #             currency = dictionary['geobytescurrency']
    #             population = dictionary['geobytespopulation']
    #             fixedPopulation = convertNumToKMBformat(population)
    #             citiesDictionary[cityName] = '|'.join([country, currency, fixedPopulation])
    #     return citiesDictionary



    def getInformation(self, cityName):
        """
        get all the information we need
        :param cityName: the city name
        :return: the information as a format: Country, currency, population
        """
        try:
            city = self.geoCoder.geonames(location=cityName, fuzzy=0.8, key = self.usename, timeout=8)

            if city is None:
                if self.dictionary_country_currencyPopulation.get(city.country_code) is None:
                    city = self.restCountries.capital(capital=cityName)
                    if city is None:
                        if self.dictionary_CapitalCity_country.get(cityName) is None:

                            print (cityName)
                            return None
                        else:
                            countryCode = self.dictionary_CapitalCity_country[cityName][0]
                            countryName = self.dictionary_CapitalCity_country[cityName][1]
                            fixedPopulation = convertNumToKMBformat( str(self.dictionary_country_currencyPopulation[countryCode][1]))
                            return [countryName, str(self.dictionary_country_currencyPopulation[countryCode][0]),str(fixedPopulation)]

                    fixedPopulation = convertNumToKMBformat(
                        str(self.dictionary_country_currencyPopulation[city.country_code][1]))

                    return [city.country, str(self.dictionary_country_currencyPopulation[city.country_code][0]),
                            str(fixedPopulation)]
                print(cityName)
                return None

            fixedPopulation = convertNumToKMBformat(str(self.dictionary_country_currencyPopulation[city.country_code][1]))

            return [city.country, str(self.dictionary_country_currencyPopulation[city.country_code][0]), str(fixedPopulation)]
        except Exception as err:
            print(err)
            return None

    def getInformationAsString(self, cityName):
        information = self.getInformation(cityName)
        if information is None:
            return None
        return '|'.join(information)


# cityAPI = CityAPI()
# print(cityAPI.getDetailsWithGeobytesWithSession(['new york','san fransisco']))

# g = geocoder.geonames('New York', key='myengine', featureClass='A')
# g = geocoder.google('New York', key='AIzaSyCG6LwcdSUeuHsTOB_lCRlzRqvcOTiqC5I',method='places')
# d = geocoder.get('New York', key='AIzaSyCG6LwcdSUeuHsTOB_lCRlzRqvcOTiqC5I')
# print(g.country)

