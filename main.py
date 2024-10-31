from rule import Rule


def print_function(f):
    def wrapper(*args):
        print(f'\n--- in [{f.__name__}]')
        result = f(*args)
        print(f'--- out [{f.__name__}]\n')
        return result
    
    return wrapper


@print_function
def search(rules: list[Rule], goal, has_nodes):
    close_nodes = has_nodes

    close_rules = []

    @print_function
    def help_parent_search():
        is_found_parent = False

        for rule in rules:
            if rule not in close_rules:
                if set(rule.required_nodes).issubset(close_nodes):
                    close_rules.append(rule)
                    close_nodes.append(rule.end_node)

                    if rule.end_node == goal:
                        return (True, True)
                    
                    is_found_parent = True
        
        return (is_found_parent, False)

    while True:
        (is_found_parent, is_found_solution) = help_parent_search()

        if is_found_solution:
            return True

        if not is_found_parent:
            return False
 
if __name__ == '__main__':
    rules = [
        Rule(2, [20]),
        Rule(2, [4, 5, 6]),
        Rule(2, [9, 10]),
        Rule(1, [20, 30]),
        Rule(30, [10]),
        Rule(1, [2, 3]),
        Rule(9, [11, 12, 13]),
        Rule(3, [6, 7, 8]),
    ]

    if search(rules, 1, [6, 7, 8, 9, 10]):
        print('Has solution')
    else:
        print("Not has solution")
