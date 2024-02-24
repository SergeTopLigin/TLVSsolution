# определение значения ключа словаря по значению другого ключа того же словаря, если словарь - элемент списка
from modules.country_codes import country_codes
country_codes = country_codes()
ass = 'GER'
print([country_codes[country_codes.index(elem)]['name'] for elem in country_codes if ass in elem['fifa']])


