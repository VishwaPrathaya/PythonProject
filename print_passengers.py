from passenger import load_passengers
ps = [p for p in load_passengers() if p.fno == 'F1']
print('Total passengers for F1:', len(ps))
for p in ps[:10]:
    print(p.pid, p.counter_id)
