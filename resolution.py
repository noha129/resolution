import re
def fix_spaces(text):
    # Replace multiple consecutive spaces with a single space
    return re.sub(r'\s+', ' ', text).strip()
#####################################################################################################################################
def eliminate_implication(statement):
    # Initialize iteration count
    iteration = 1
    while '->' in statement:
        print(f"Iteration {iteration}: {statement}")

        # Find the next  '->'
        imp_index = statement.find("->")

        # Find the index of the first function (start from the beginning of the statement and search up to imp_index)
        last_bracket = statement.rfind("(", 0, imp_index)

        # Get the character before the second-to-last '('
        char_before_last_bracket = statement[last_bracket- 1]

        # Find the index of the second function (start from the imp_index and search forwards)
        function2_end = statement.find(")", imp_index)

        # Construct the modified statement
        statement = statement[:last_bracket-1] + "¬ " + char_before_last_bracket + statement[last_bracket:imp_index] + "∨" + statement[imp_index+2:function2_end] + statement[function2_end:]

        # Increment iteration count
        iteration += 1

    # Print the final iteration
    print(f"Iteration {iteration}: {statement}")
    print()
    return statement

# # Original statement
# original_statement = "∃x∀y∀z((ρ(y)->(Q(z)->(P(x)->Q(x)))"

# # Apply elimination of implication
# result=eliminate_implication(original_statement)
# print(result)
####################################################################################################################################
def de_morgan_law(s):
    symbols = ['P', 'Q', 'S','R']
    # Check if '!' appears before '('
    get_not = s.find('¬')
    part = s.find('(', get_not)
    if '¬' in s and s.index('¬') < s.index('('):
        if  '¬∃' in s :
          s=s.replace('∃','temp')
          s=s.replace('∃','∀')
          s=s.replace('temp','∀')
        elif '¬∀' in s:
          s=s.replace('∀','temp')
          s=s.replace('∀','∃') 
          s=s.replace('temp','∃') 

        #s = s.replace('¬', '')
        # Replace '&' with '|', and vice versa
        s = s.replace('∧', 'temp')  # Replace '&' with a temporary placeholder
        s = s.replace('∨', '∧')
        s = s.replace('temp', '∨')  # Replace the temporary placeholder with '|'
        for symbol in symbols:
            s = s.replace(symbol, '¬' + symbol)  # Add '¬' before each symbol occurrence
        s=s[:get_not]+s[get_not+1:]

    return s
#s = "(¬p(x)∧(Q(x)∨¬R(x)))"
# processed_s = de_morgan_law(s)
# print("s",processed_s)
# s2 = "¬∃(¬p(x)∧(Q(x)∨¬R(x)))"
# processed_s = de_morgan_law(s2)
# print("s2",processed_s)

# s3 = "¬∀(¬p(x)∧(Q(x)∨¬R(x)))"
# processed_s = de_morgan_law(s3)
# print("s3",processed_s)

# s4 = "¬(¬p(x)∧(Q(x)∨¬R(x)))"
# processed_s = de_morgan_law(s4)
# print("s4",processed_s)
#####################################################################################
def remove_double_negations(s):
  if '¬¬' in s:
    s = s.replace('¬¬', '') 
  elif '¬ ¬' in s:
     s = s.replace('¬ ¬', '')  
  return s

# # Example usage:
# s = '(Q(x))^ ¬¬(p(x))'
# processed_s = remove_double_negations(s)
# print(processed_s)
#########################################################################################
import re

def standardize_expression(expression):
    var_counter = {}
    
    def replace_var(match):
        nonlocal var_counter
        var = match.group(0)
        if var not in var_counter:
            var_counter[var] = 1
        else:
            var_counter[var] += 1
            var = f'{var}{var_counter[var]}'
        return var
    
    pattern = r'[a-zA-Z]+'
    standardized_expression = re.sub(pattern, replace_var, expression)
    
    return standardized_expression

# Test the function with the provided expression
expression = "∃x∀x∀z((ρ(y)->(Q(z)->(P(x)->Q(x))))"
standardized_expression = standardize_expression(expression)
print(standardized_expression)
################################################################################

def move_quantifiers_left(expression):
    quantifiers = ""
    predicates = ""
    has_quantifier = False

    for char in expression:
        if has_quantifier:
            if char == ' ':
                continue
            quantifiers += char
            has_quantifier = False
        elif char in ['∀', '∃']:
            quantifiers += char
            has_quantifier = True
        else:
            predicates += char

    return quantifiers + predicates

# # Test the function
# expression = "(∀x P(x)) ∨ (∃y Q(y))"
# modified_expression = move_quantifiers_left(expression)
# print(modified_expression)
########################################################################################################
def skolemization(expression):
    flag = False
    new_expression = expression  # Initialize new expression
    new_variable=" "
    k=0
    for i in range(len(new_expression)):
        if expression[i] == '∀':
            flag=True
            new_variable = expression[i + 1]  # Here you can replace the universal
    for i in range(len(new_expression)):
        if expression[i] == '∃':
            k+=1
            variable = expression[i + 1]
            for j in range(len(new_expression)):
                if new_expression[j] == variable:
                  if flag:
                    new_expression = new_expression.replace(new_expression[j], 'F' +str(k)+'(' + new_variable + ')')
                  else:
                      new_expression = new_expression.replace(new_expression[j], 'F'+str(k)+'(A)')
            if flag:
                  new_expression = new_expression.replace('∃F'+str(k)+'(' + new_variable + ')' , "")
            else:
                 new_expression = new_expression.replace('∃F'+str(k)+'(A)'," ")


    return fix_spaces(new_expression)

# Test the function
expression = "∀x ∃y ∃z P(x) ∨ Q(y) p(y) p(z)"
# expression="∃z P(x) ∨ Q(y) p(y) p(z)"
# expression = "∃z P(x) ∨ Q(y) p(y) p(z)"
modified_expression = skolemization(expression)
print(modified_expression)

##########################################################################################################################
def EliminateUniversalQuantifiers(expression):
    new_expression = " "
    for i in range(len(expression)):
        if expression[i] == '∃' or expression[i] == '∀':
            continue
        elif expression[i-1] == '∃' or expression[i-1] == '∀' :
            continue
        else:
            new_expression+=expression[i]
    return   new_expression.strip()

# expression = "∀y ∀y P(A) ∨ ∀yQ(y)"
# modified_expression =  EliminateUniversalQuantifiers(expression)
# print(modified_expression)
##################################################################################################################################
def distribute_cnf(expression):
    if '∨' not in expression:  # Check if disjunction (∨) exists in the expression
        return expression

    parts = expression.split("∨")
    left = parts[0].strip()  # Remove leading/trailing whitespaces
    right = parts[1].strip("()")  # Remove leading/trailing parentheses

    conjuncts = right.split("∧")
    if len(conjuncts) == 1:
        return expression
    else:
        conjuncts = [conj.replace('(', "").strip() for conj in conjuncts]  # Remove '(' and strip whitespaces
        cnf = []
        for conj in conjuncts:
            conj = conj.strip()  # Strip whitespaces
            if conj.startswith('∨'):
                cnf.append("(" + left.strip() + conj.strip() + ")")  # Avoid redundant parentheses
            else:
                cnf.append("(" + left.strip() + " ∨ " + conj.strip() + ")")  # Add missing disjunction

    return " ∧ ".join(cnf)


# Test case
expression1 = "p ∨ (q ∧ r)"
print(distribute_cnf(expression1))  # Output: "(p ∨ q ∨ r)"
#############################################################################################################################
def convert_to_clauses(expression):
    clauses = []
    var_counter = {}
    result = ""

    for char in expression:
        if char.isalpha():
            if char not in var_counter:
                var_counter[char] = 1
            else:
                var_counter[char] += 1
                char = f'{char}{var_counter[char]}'

        result += char

    parts = result.split("∧")
    clauses.append(parts)
    return clauses


# # Test the function
# expression = "(p ∨ q) ∧ (r ∨ c) ∧ (r ∨ c) ∧(p ∨ q ) ∧(p ∨ q ))"
# clauses = convert_to_clauses(expression)
# print("Clauses:", clauses)
############################################################################################################
#Test 
expression = "∃x∀z∀y((R(y)->(Q(z)->(R(x)->Q(y)))"
#to prove resolution 
#the first add negation for this expression

negated_expression = '¬' + expression
print("Steps for Eliminate implication: ")
implication=eliminate_implication(negated_expression) #1
demorgan=de_morgan_law(implication)                   #2
removeDN=remove_double_negations(demorgan)            #3
moveQuan=move_quantifiers_left(removeDN)              #5
skol= skolemization(moveQuan)                         #6
Eli_univer=EliminateUniversalQuantifiers(skol)        #7
convert_conForm=distribute_cnf(Eli_univer)            #8
clauses = convert_to_clauses(convert_conForm)   #9&10
print("Eliminate implication for expression: ",implication,'\n')
print("Apply Demorgan Law: ",demorgan,'\n')
print("Remove double-not. if found : ", removeDN,'\n')
print("move quantifiers left: ",moveQuan,'\n')
print("Apply Skolemization for existential quantifiers: ", skol,'\n')
print("apply Eliminate for universal quantifiers: ", Eli_univer,'\n')
print("Convert expression to conjunctive normal form: ", convert_conForm,'\n')
print("Clauses:", clauses)
