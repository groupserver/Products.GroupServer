from string import find, rfind, join
width = int(width)
remaining = text
wrapped = []

while len(remaining) > width:
    cut = width
    newline = find(remaining, '\n', 0, cut)
    
    if newline != -1:
        cut = newline
    elif remaining[cut] != ' ':            
        temp = rfind(remaining, ' ', 0, cut-1)
        if temp == -1:temp = find(remaining, ' ', cut-1, len(remaining))
        if temp == -1: temp = len(remaining)
        cut = temp
    wrapped.append(remaining[:cut])
    remaining = remaining[cut+1:]

if remaining:
    wrapped.append(remaining)

return join(wrapped, '\n')

