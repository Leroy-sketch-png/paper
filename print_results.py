"""Print master results table combining all computed baselines and FAST numbers."""
import csv, pathlib, statistics

FAST = pathlib.Path(r'c:\Users\YOGA\Downloads\research\FAST')

def fast_stats(subj, method):
    tsv = FAST / 'output' / subj / f'{method}-bbox.tsv'
    if not tsv.exists():
        return None, None
    rows = [r for r in csv.reader(open(tsv), delimiter='\t') if r and r[0] != 'SignatureTime']
    apfds = [float(r[2]) for r in rows if len(r)>2]
    if not apfds: return None, None
    return statistics.mean(apfds), statistics.stdev(apfds) if len(apfds)>1 else 0

# Read heuristic baselines
heur = {}
with open(r'c:\Users\YOGA\Downloads\research\heuristic_baselines.csv') as f:
    for row in csv.DictReader(f):
        heur[row['subject']] = row

SIR = ['flex_v3','grep_v3','gzip_v1','make_v1','sed_v6']
D4J = ['chart_v0','closure_v0','lang_v0','math_v0','time_v0']

print("MASTER RESULTS TABLE")
print("="*105)
header = f"{'Subject':<15} {'Suite':<5} {'N':>5} {'Rand-30':>10} {'FFF':>8} {'FAST-pw':>17} {'FAST-log':>17}"
print(header)
print("-"*105)

for subj in SIR + D4J:
    suite = 'D4J' if subj in D4J else 'SIR'
    pw_mean, pw_std = fast_stats(subj, 'FAST-pw')
    log_mean, log_std = fast_stats(subj, 'FAST-log')
    h = heur.get(subj, {})
    rand = h.get('rand30_mean', '?')
    fff = h.get('fff_apfd', '?')
    n = h.get('n_tests', '?')
    pw_str = f'{pw_mean:.4f}+/-{pw_std:.4f}' if pw_mean is not None else 'RUNNING...'
    log_str = f'{log_mean:.4f}+/-{log_std:.4f}' if log_mean is not None else 'RUNNING...'
    print(f"{subj:<15} {suite:<5} {n:>5} {rand:>10} {fff:>8} {pw_str:>17} {log_str:>17}")

print()
print("FFF = Failure-Frequency-First (oracle upper bound)")
print("Rand-30 = mean of 30 random orderings (fixed seeds)")
print("FAST-pw/log = mean over all rows in TSV (n=30 for SIR once done, n=70-1010 for D4J)")
