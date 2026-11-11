from pathlib import Path
import csv
BASE=Path(__file__).parent;OUT=BASE/'output';OUT.mkdir(exist_ok=True)
seen=set();combined=[];duplicates=0
for filepath in sorted((BASE/'input').glob('*.csv')):
    with filepath.open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['order_id'] in seen:duplicates+=1;continue
            seen.add(r['order_id']);combined.append(r)
columns=['order_id','customer','amount']
def save(path,items):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(items)
save(OUT/'merged_orders.csv',combined)
for start in range(0,len(combined),3):save(OUT/f'chunk_{start//3+1:02d}.csv',combined[start:start+3])
print(f'Input files: 3 | Unique orders: {len(combined)} | Duplicates: {duplicates}')
