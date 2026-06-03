import csv

preds = list(csv.DictReader(open('outputs/metrics/predictions.csv', 'r', encoding='utf-8')))
ep = [p for p in preds if p['event'] == '4']

fp = [p for p in ep if p['label']=='0' and p['prediction']=='1']
fn = [p for p in ep if p['label']=='1' and p['prediction']=='0']
correct = [p for p in ep if p['label']==p['prediction']]

print(f'Event 4: {len(ep)} samples, Acc={len(correct)/len(ep):.3f}, errors={len(fp)+len(fn)}')
print(f'FP={len(fp)}, FN={len(fn)}')
print(f'Current threshold: 0.51')

fn.sort(key=lambda p: float(p['prob_1']))
print(f'\n=== FN: {len(fn)} rumors missed ===')
for p in fn:
    print(f'  prob={float(p["prob_1"]):.4f} | {p["text"][:110]}')

fp.sort(key=lambda p: float(p['prob_1']), reverse=True)
print(f'\n=== FP: {len(fp)} non-rumors falsely predicted ===')
for p in fp:
    print(f'  prob={float(p["prob_1"]):.4f} | {p["text"][:110]}')

print(f'\n=== 阈值扫描 ===')
for t in [0.70, 0.65, 0.60, 0.55, 0.51, 0.50, 0.45, 0.40, 0.35, 0.30, 0.25]:
    y_pred = [int(float(p['prob_1']) >= t) for p in ep]
    y_true = [int(p['label']) for p in ep]
    tp = sum(1 for a,b in zip(y_true,y_pred) if a==1 and b==1)
    tn = sum(1 for a,b in zip(y_true,y_pred) if a==0 and b==0)
    fp_n = sum(1 for a,b in zip(y_true,y_pred) if a==0 and b==1)
    fn_n = sum(1 for a,b in zip(y_true,y_pred) if a==1 and b==0)
    acc = (tp+tn)/len(ep)
    print(f'  t={t:.2f}: Acc={acc:.3f} TP={tp:2} TN={tn:2} FP={fp_n:2} FN={fn_n:2}')
