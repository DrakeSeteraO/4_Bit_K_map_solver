def main():
    K_map = create_K_map()
    queue = create_queue(K_map)
    val = queue.pop()
    possibilities, score = generate_boxes(val, queue, K_map)
    possibilities = narrow_possibilities(possibilities)
    
    segment = set()
    for p in possibilities:
        segment.add(p)
    
    possibilities = ''
    for s in segment:
        possibilities += s + ","
    possibilities.removesuffix(",")

    with open("segments.txt", 'a') as file:
        file.write(f"{possibilities}\n")
    
    

def narrow_possibilities(possibilities: list[str]) -> list[str]:
    min_score = 1_000
    distance = 1
    output = list()
    
    for possible in possibilities:
        if len(possible) < min_score + distance:
            prev = set()
            score = 0
            
            i = 0
            go = True
            left = 0
            while i < len(possible) and go:
                if score - distance > min_score:
                    go = False

                else:
                    if possible[i].isalpha():
                        score += 1
                    elif possible[i] == "'":
                        score += 1
                    elif possible[i] == '(':
                        left = i
                    elif possible[i] == ')':
                        prev.add(possible[left:i+1])
                i += 1
            
            if go:
                cur  = ''
                for val in prev:
                    cur += val + "+"
                output.append(cur.removesuffix("+"))

    return output
                       
                
                
def score_value(possibility: str) -> int:
    score = 0
    for p in possibility:
        if p.isalpha():
            score += 1
        elif p == "'":
            score -= 1
    return score

             
    
def create_K_map() -> dict:
    map = input("Type in K map, where\n0 = 0\n1 = 1\n2 = Doesn't matter\n")
    K_map = dict()
    
    for val in range(len(map)):
        K_map[bin(val).removeprefix('0b').zfill(4)] = map[val]
    return K_map
 


def create_queue(K_map: dict) -> set:
    queue = set()
    for key in K_map:
        if K_map[key] == '1':
            queue.add(key)
    return queue



def generate_boxes(val: str, queue: set, K_map: dict[str, int]) -> tuple[list[tuple[str, int]], int]:
    if len(val) <= 0:
        return [''], 0
    
    min_score = 1000
    output = list()
    for i in range(15, -1, -1):
        temp = bin(i).removeprefix('0b').zfill(4)
     
        bit_strings = generate_bit_strings(val, temp)
        if valid_bit_strings(bit_strings, K_map):
            
            new_queue, new_val = {}, ''
            if len(queue) > 0:
                new_queue = queue.copy()
                new_val = new_queue.pop()
            
            disp = convert_box(val, temp)
            new_score = score_value(disp)
            
            possibilities, score = generate_boxes(new_val, new_queue, K_map)
            
            if new_score + score - 1 <= min_score:
                if new_score + score <= min_score:
                    min_score = new_score + score

                possibilities = fuse(disp, possibilities)

                for possible in possibilities:
                    output.append(possible)
    return output, min_score
        
    

def fuse(val: str, lst: list) -> list:
    output = list()
    for l in lst:
        output.append(val+l)
    return output
    
    

def convert_box(val: str, required: str) -> str:
    output = str()
    org = ['A','B','C','D']
    opp = ["A'","B'","C'","D'"]
    
    for i in range(len(required)):
        if required[i] == '0':
            if val[i] == '1':
                output += org[i]
            else:
                output += opp[i]
    return '(' + output + ')+'
   
    
    
def generate_bit_strings(val: str, digits: str) -> list[str]:
    output = [val]
    for i in range(len(digits)):
        if digits[i] == '1':
            temp1 = list()
            temp2 = list()
            for o in output:
                val1 = ''
                val2 = ''
                if i > 0:
                    val1 = o[:i]
                    val2 = o[:i]
                val1 += '0'
                val2 += '1'
                if i < 3:
                    val1 += o[i+1:]
                    val2 += o[i+1:]
                temp1.append(val1)
                temp2.append(val2)
            output = temp1 + temp2
    return output



def valid_bit_strings(bit_strings: list[str], K_map = dict[str, int]):
    for b in bit_strings:
        if K_map[b] == '0':
            return False
    return True
        
if __name__ == '__main__':
    # weights = {}
    main()
