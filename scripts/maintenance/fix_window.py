f = r"c:\Users\YOGA\Downloads\research\window.md"
c = open(f, 'rb').read().decode('utf-8')

changes = []

# 1) Remove duplicate IDoFT entry (line 20 is the older/longer version; keep line 18)
old1 = (
    "- **Adjacent artifact: IDoFT** (GitHub: TestingResearchIllinois/idoft, Wing Lam et al., ICST 2019). International Dataset of Flaky Tests. Three live CSVs: `pr-data.csv` (Java/Maven), `gr-data.csv` (Java/Gradle), `py-data.csv` (Python). Categorizes flaky tests by root cause: OD, ID, NIO, NOD, NDOD, NDOI, UD, OSD, TD, TZD. 176 contributors, 306 forks, actively maintained. Website: `http://mir.cs.illinois.edu/flakytests`. **Empirical grounding for Direction A** \u2014 labeled flaky test instances across projects that may overlap with TCP benchmark subjects.\n"
    "- **Adjacent artifact: DeepOrder**"
)
new1 = (
    "- **Adjacent artifact: IDoFT** (GitHub: TestingResearchIllinois/idoft, Wing Lam et al., ICST 2019). International Dataset of Flaky Tests. Three live CSVs: `pr-data.csv` (Java/Maven), `gr-data.csv` (Java/Gradle), `py-data.csv` (Python). Root causes: OD, ID, NIO, NOD, NDOD, NDOI, UD, OSD, TD, TZD. 176 contributors, 306 forks, actively maintained. Website: `http://mir.cs.illinois.edu/flakytests`. **Empirical grounding for Direction A** \u2014 labeled flaky test instances across projects that overlap with TCP benchmark subjects.\n"
    "- **Adjacent artifact: DeepOrder**"
)
if old1 in c:
    c = c.replace(old1, new1, 1)
    changes.append("Cleaned up IDoFT entry and removed duplicate marker")

# 2) Remove the second (duplicate) IDoFT entry that follows DeepOrder
old2 = (
    "Deep learning TCP for CI: regression-style neural model consuming historical test execution records. Already outperforms some prior approaches on efficiency and detection. Jointly with FALCON, establishes that the representation-learning space for TCP is **not underexplored** \u2014 the interesting question is no longer whether deep/semantic models beat classic heuristics but how they behave under flaky labels, federated constraints, and long-running suites.\n"
    "- **Adjacent artifact: IDoFT** (GitHub: TestingResearchIllinois/idoft, maintained by Wing Lam et al., ICST 2019 origin). International Dataset of Flaky Tests. Three live CSVs: `pr-data.csv` (Java/Maven), `gr-data.csv` (Java/Gradle), `py-data.csv` (Python). Categorizes flaky tests by root cause: OD (order-dependent), ID (implementation-dependent), NIO, NOD, NDOD, NDOI, UD, OSD, TD, TZD. Actively maintained with 176 contributors, 306 forks. Website: `http://mir.cs.illinois.edu/flakytests`. **This is the empirical grounding for Direction A** \u2014 provides labeled flaky test instances across projects that overlap with TCP benchmark subjects.\n"
    "\n## Lab Status"
)
new2 = (
    "Deep learning TCP for CI: regression-style neural model consuming historical test execution records. Already outperforms some prior approaches on efficiency and detection. Jointly with FALCON, establishes that the representation-learning space for TCP is **not underexplored** \u2014 the interesting question is no longer whether deep/semantic models beat classic heuristics but how they behave under flaky labels, federated constraints, and long-running suites.\n"
    "\n## Lab Status"
)
if old2 in c:
    c = c.replace(old2, new2, 1)
    changes.append("Removed duplicate IDoFT Source entry after DeepOrder")

# 3) Fix replication package row
old3 = "| Source paper replication package | Located | Zenodo 7036507 \u2014 not yet downloaded |"
new3 = "| Source paper replication package | Located \u2014 **files restricted** | Zenodo 7036507; structure confirmed: `collect_data/`, `rl/`, `supervised_learning/`, `origin/` (11 projects), `smote/`, `result/`; requires Understand + Ranklib; login required to download |"
if old3 in c:
    c = c.replace(old3, new3, 1)
    changes.append("Fixed replication package row")

# 4) Fix FAST row
old4 = "| FAST (ICSE 2018) non-ML baseline | **Running** | `FAST/` \u2014 Python 3.10 port complete; FAST-pw APFD ~0.878\u20130.948 on flex\\_v3 |"
new4 = "| FAST (ICSE 2018) non-ML baseline | **Running** | `FAST/` \u2014 Python 3.10 port complete; full 10-subject APFD table verified (see Hard Numbers) |"
if old4 in c:
    c = c.replace(old4, new4, 1)
    changes.append("Fixed FAST row")

# 5) Fix Full FAST baseline table row
old5 = "| Full FAST baseline table | Not yet run | All 10 subjects \u00d7 bbox + wbox \u2014 ~5 min automated |"
new5 = "| Full FAST baseline table | **Done** | All 10 subjects \u00d7 bbox mode \u00d7 10 reps \u2014 see Hard Numbers table |"
if old5 in c:
    c = c.replace(old5, new5, 1)
    changes.append("Fixed Full FAST baseline table row")

# 6) Fix urgency note
old6 = "**Highest-urgency gap:** Direction A flaky-test dataset (IDoFT) \u2014 the label-realism attack needs empirical grounding before it can anchor a motivation section."
new6 = "**Resolved gap:** IDoFT is now located (TestingResearchIllinois/idoft). **Remaining gap:** Android open-source CI data for Direction D."
if old6 in c:
    c = c.replace(old6, new6, 1)
    changes.append("Fixed urgency note")

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)

for ch in changes:
    print("OK:", ch)
if not changes:
    print("No changes made")
