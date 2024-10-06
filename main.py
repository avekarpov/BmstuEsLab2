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
    open_nodes_stack = [goal]
    open_rules = []

    close_nodes = has_nodes
    close_rules = []

    forbidden_nodes = []
    forbidden_rules = []

    @print_function
    def help_child_search():
        top_node = open_nodes_stack[-1]
        print(f'top_node={top_node}')

        for rule in rules:
            if rule.is_used:
                continue

            print(f'rule={{end_node={rule.end_node}, required_nodes={rule.required_nodes}}}')
            if rule.end_node == top_node:
                rule.is_used = True

                open_rules.append(rule)

                is_found_new_goal = False
                for node in rule.required_nodes:
                    if node not in close_nodes:
                        print(f'\topen: node={node}')
                        open_nodes_stack.append(node)

                        is_found_new_goal = True
                
                if not is_found_new_goal:
                    while True:
                        open_rule = open_rules.pop()
                        node = open_nodes_stack.pop()

                        print(f'\tclose: rule={{end_node={open_rule.end_node}, required_node={open_rule.required_nodes}}}, node={node}')
                        close_rules.append(open_rule)
                        close_nodes.append(node)

                        if node == goal:
                            # Found solution
                            return (True, True)

                        # If next node not end for next rule break
                        if open_rules[-1].end_node != open_nodes_stack[-1]:
                            break

                return (True, False)

            for node in rule.required_nodes:
                if node in forbidden_nodes:
                    print(f'\tforbbiden: rule={{{rule.end_node}, required_node={rule.required_nodes}}} (bcs node={node} already forbidden)')
                    rule.is_used = True
                    break
            
        return (False, False)

    while True:
        print(f'open_node(stack)={open_nodes_stack}')
        print(f'close_nodes={close_nodes}')

        (is_found_child, is_found_solution) = help_child_search()

        if is_found_solution:
            return True
        
        if not is_found_child:
            if len(open_nodes_stack) <= 1:
                return False

            node = open_nodes_stack.pop()
            rule = open_rules.pop()

            print(f'forbbiden: rule={{{rule.end_node}, required_node={rule.required_nodes}}}, node={node}')

            forbidden_nodes.append(node)
            forbidden_rules.append(rule)

            for node in rule.required_nodes:
                try:
                    print(f'try remove from open: node={node}')
                    open_nodes_stack.remove(node)
                except:
                    pass


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
