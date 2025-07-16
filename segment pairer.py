def main():
    with open("segments.txt", 'r') as file:
        lines = file.readlines()
        
        segments = list()
        for line in lines:
            line = line.replace("\n", "")
            parts = line.split(",")
            segments.append(parts)
        
        possibilities = solver(segments, 0, set())
        possibilities = narrow_possibilities(possibilities)
        possibilities = sort_possibilities(possibilities)
        write_possibilities(possibilities, 100)



def write_possibilities(possibilities: list[str], amount: int) -> None:
    output = ''
    titles = ['A','B','C','D','E','F','G']
    for t in titles:
        output += t + ' ' * 29
    output += "\n"
    
    
    for i in range(amount):
        parts = possibilities[i].split("*")
        for part in parts:
            output += part + ' ' * (30 - len(part))
        output += "\n"
    with open("Best_Segments.txt", "w") as file:
        file.write(output)
        


def sort_possibilities(possibilities: list[str]):
    temp = list()
    for x in range(200):
        temp.append(list())
    
    for possible in possibilities:
        score = score_value(possible)
        temp[score].append(possible)
    
    output = list()
    for x in temp:
        for y in x:
             output.append(y)
    return output
    


def score_value(possibility: str) -> int:
    score = 0
    for p in possibility:
        if p.isalpha():
            score += 1
        elif p == "'":
            score += 1
    return score



def narrow_possibilities(possibilities: list[str]) -> list[str]:
    min_score = 1_000
    output = list()
    
    for possible in possibilities:
        if len(possible) < min_score:
            score = 0
            
            i = 0
            go = True
            while i < len(possible) and go:
                if score > min_score:
                    go = False

                else:
                    if possible[i].isalpha():
                        score += 1
                    elif possible[i] == "'":
                        score += 1
                i += 1
            
            if go:
                output.append(possible)

    return output



def solver(segments: list[list[str]], level: int, parts: set) -> list[str]:
    if level >= 7:
        return ['']
    
    output = list()
    min_parts = 1000
    
    for possibility in segments[level]:
        new_parts = get_parts(possibility)
        parts_copy = parts.copy()
        
        for new_part in new_parts:
            parts_copy.add(new_part)
            
        if len(parts_copy) <= min_parts:
            min_parts = len(parts_copy)
            
            possibility = f"{possibility}*"
            possibilities = fuse(possibility, solver(segments, level + 1, parts_copy))
            for possible in possibilities:
                output.append(possible)
    return output
                

def fuse(val: str, lst: list) -> list[str]:
    output = list()
    for l in lst:
        output.append(val+l)
    return output



def get_parts(equation: str) -> str:
    left = 0
    parts = list()
    for i in range(len(equation)):
        if equation[i] == '(':
            left = i
        elif equation[i] == ')':
            parts.append(equation[left:i+1])
    return parts
    

if __name__ == '__main__':
    main()