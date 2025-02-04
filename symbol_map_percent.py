'''
Counts the percentage of functions in the symbol map that are documented.
'''
with open('GWME51.map') as map:
    total = 0
    documented = 0
    for line in map.readlines():
        if '8035e520' in line:
            # Start of .data0
            break
        total += 1
        if 'FUN_' not in line:
            documented += 1
print(f'Total: {total}')
print(f'Documented: {documented}')
print(f'Percent: {documented / total}')
