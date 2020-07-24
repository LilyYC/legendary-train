10/30/2016 Restaurant Recommendations: Planning the Program
10/30/2016 Restaurant Recommendations: Planning the Program
    Return a list of the restaurants in names_matching_price that serve at
    """ (dict of {str: list of str}) -> dict of {str: int}
	
    The table_to_foods dict has table names as keys (e.g., 't1', 't2', and so on) and each value
    is a list of foods ordered for that table.

    Return a dictionary where each key is a food from table_to_foods and each
    value is the quantity of that food that was ordered.
	
    >>> get_quantities({'t1': ['Vegetarian stew', 'Poutine', 'Vegetarian stew'], 't3': ['Steak pie', 'Poutine', 'Vegetarian stew'], 't4': ['Steak pie', 'Steak pie']})
    {'Vegetarian stew': 3, 'Poutine': 2, 'Steak pie': 3}	
    """

    food_to_quantity = {}
    count = 1
    for tables in table_to_foods:
        for index in range(len(table_to_foods[tables])):
            if table_to_foods[tables][index] not in food_to_quantity:
                food_to_quantity[table_to_foods[tables][index]] = count
            else:
                food_to_quantity[table_to_foods[tables][index]] += 1 
    return food_to_quantity