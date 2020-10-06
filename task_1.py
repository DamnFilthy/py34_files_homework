import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_recipes(filename):
    result = {}
    with open(filename, encoding='utf-8') as recipes:
        line = recipes.readline()
        recipe_name = None
        ingred_count = -1
        while line != '':
            line = line.strip()
            if recipe_name is None:
                recipe_name = line
                result[recipe_name] = []
                line = recipes.readline()
                continue
            if ingred_count < 0:
                try:
                    ingred_count = int(line)
                except ValueError as e:
                    return {}
            elif ingred_count == 0:
                recipe_name = None
                ingred_count = -1
            else:
                tmp_dict = dict(zip(
                    ['ingredient_name', 'quantity', 'measure'],
                    [x.strip() for x in line.split('|')]))
                try:
                    tmp_dict['quantity'] = int(tmp_dict.setdefault('quantity', 0))
                except ValueError as e:
                    return {}
                result[recipe_name].append(tmp_dict)
                ingred_count -= 1
            line = recipes.readline()
    return result

def get_shop_list_by_dishes(dishes, person_count, filename='recipes.txt'):
    # убираем повторяющиеся блюда
    for i, v in enumerate(dishes):
        if dishes[i] in dishes[2:]:
            del dishes[i]
    # if dishes[0] == dishes[1]:
    #     dishes = [dishes[0]]
    result = {}
    for dish in dishes:
        ingred_list = get_recipes(filename)[dish]
        for item in ingred_list:
            ingred_name = item['ingredient_name']
            ingred_found = result.setdefault(ingred_name,
                                             {'measure': item['measure'],
                                             'quantity': 0})
            ingred_found['quantity'] = ingred_found['quantity'] + \
            item['quantity'] * person_count
            result[ingred_name] = ingred_found
    return result

print('Рецепты:')
cook_book = get_recipes('recipes.txt')
pp.pprint(cook_book)

print('\nНеобходимые покупки для блюд:')
pp.pprint(get_shop_list_by_dishes(['Омлет', \
'Утка по-пекински', 'Омлет', 'Утка по-пекински'], 3))
