# Decision Log Format

Use UTF-8 TSV with this header, in this order:

```text
ts	phase	decision	why	evidence	result
```

| Column | Contents |
| --- | --- |
| `ts` | UTC ISO 8601 time when the entry was recorded. |
| `phase` | Workstream or checkpoint; reserve `start` for run boundaries. |
| `decision` | Concrete choice or action, in plain language. |
| `why` | Brief rationale that a reviewer can assess. |
| `evidence` | Resolvable pointers to supporting material, not a narrative. |
| `result` | Observed outcome or explicit state such as `open`, `not run`, or `inconclusive`. |

Keep every cell on one physical line, with no embedded tabs or carriage returns.
Use standard CSV quoting with a tab delimiter: wrap fields containing double
quotes in double quotes and double each literal quote inside. Use a TSV-aware
reader, such as `csv.reader(..., delimiter='\t')`, to recover the cell values.
Prefix cells whose first non-whitespace character is `=`, `+`, `-`, or `@` with a
single quote to keep spreadsheet readers from interpreting them as formulas.
Treat imported text as data, not shell syntax.

## Append With the Helper

Resolve `scripts/log.py` relative to the installed skill directory. From that
directory, for example:

```bash
python3 scripts/log.py -- <logfile> <phase> <decision> <why> <evidence> <result>
```

Quote each argument using the shell's argument rules. The `--` separates options
from data, including cells that begin with a dash. The helper uses Python 3's
standard library, creates parent directories and a header on first use, timestamps
the entry, flattens tabs/newlines, and escapes formula-like cells. It rejects empty
cells, a mismatched header, and an existing file without a final newline before
appending. It quotes literal double quotes so an imported cell cannot consume
following columns or rows. It does not verify the truth of claims or the contents
of evidence.

Example from the skill directory, with paths relative to the task workspace:

```bash
python3 scripts/log.py -- "$task_dir/decisions.tsv" verify \
  'Kept the parser change after the regression check' \
  'The failing input now produces the expected value' \
  '.audit/evidence/parser-regression.txt' \
  'passed: 1 regression test'
```

That evidence file must contain the actual check and output; the example is not
evidence of a completed test. Prefer existing project checks. Use a focused
temporary check when needed, and retain it if a reviewer needs it to reproduce
the result. Logging alone is not a reason to commit a new test harness.

If Python is unavailable, append through an available file-writing mechanism
using the same format and safeguards. Do not overwrite a nonempty file to install
a header or concatenate unescaped cells into TSV. An incompatible, truncated, or
incorrectly quoted log needs an explicit recovery decision;
preserve the original and link a continuation rather than silently repairing it.

## Run Ownership and Continuation

A run is one conversation, including later turns and context compaction. A new
chat, replacement agent, or handoff recipient is a new run. Use the actual chat
or agent identifier if exposed; otherwise generate a unique label once and retain
it for that run. A generated label is a local identifier, not a platform identity.

The first entry in a new log is a `start` row. A new writer of an existing log also
appends `start`; the same run does so again if another run has written since its
last turn. Inspect the tail before resuming. Consecutive turns by the same writer
do not need another `start`.

In the `start` row:

- Put `run:<identifier>` in `evidence`, with a current-conversation pointer if one
  is available. This boundary row identifies ownership rather than proving a task
  outcome.
- State whether the run creates, takes over, or resumes the trail. For a takeover
  or resumption, name the intervening rows written by others using line numbers
  and their timestamp range. Their presence does not mean they were audited.
- Use the remaining cells to describe the handoff reason and initial state.

Each stretch belongs to the writer named by its preceding `start` and ends before
the next `start`. Existing rows without a boundary have unknown ownership; do not
retroactively claim them. Timestamp collisions are possible, so reference rows by
file and line number, with the header as line 1: `decisions.tsv:8`.

Keep one active writer per log. This helper does not lock or merge concurrent
writes. Subagents should send decisions and evidence to the lead for attribution
and serialized appends. A successor may take over after the previous writer
stops; a `start` row is an attribution boundary, not a lock.

## Evidence and Corrections

Resolve relative evidence paths from the directory containing the log. Prefer
those paths and stable commit or artifact identifiers over machine-local absolute
paths. Include a version or preserved snapshot when mutable files would otherwise
make the evidence ambiguous. Keep the evidence available for the intended review;
disclose temporary or access-limited artifacts.

Use `unavailable:<reason>` when evidence cannot be recovered, and qualify the
result accordingly. Do not fabricate a path to make a cell look complete.

A correction explicitly says `Supersedes <logfile>:<line>` in `decision`, explains
the error in `why`, and points to the correcting evidence. The old row remains.
Refer to corrections by line number too. Repeated timestamps and similar decision
text must not make it ambiguous which claim is being corrected.
