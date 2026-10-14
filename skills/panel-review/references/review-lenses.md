# Lens Index

Lenses are broad review perspectives, each with guiding questions. Choose
complementary lenses and load only their files; they are not a required roster.
Apply each to the actual domain without turning every technology or subsystem
into a separate lens.
Map material risks to reviewers before spawning. Lenses guide investigation, not
which problems a reviewer may notice. Route cross-lens discoveries to an owner,
and allow overlap where an independent second look is worth its cost. A Generalist
can provide broad coverage for a narrow target or complement focused reviews.
Record material gaps rather than assuming the roster proves completeness.

| Lens | Central question |
| --- | --- |
| [Intent](lenses/intent.md) | Does this deliver the requested outcome within the agreed scope? |
| [Correctness](lenses/correctness.md) | Does the behavior hold in supported situations, including failure? |
| [Design](lenses/design.md) | Is the solution understandable, cohesive, and proportionate to the problem? |
| [Experience](lenses/experience.md) | Can its intended users understand, use, and recover from it? |
| [Security](lenses/security.md) | Does it preserve trust boundaries and protect sensitive resources? |
| [Efficiency](lenses/efficiency.md) | Does it use time and resources reasonably for the expected workload? |
| [Integration](lenses/integration.md) | Does it fit the surrounding system and the way it is delivered and operated? |
| [Verification](lenses/verification.md) | Does the available evidence justify confidence in the changed behavior? |
| [Generalist](lenses/generalist.md) | What material issue might a focused review overlook across the target as a whole? |

Repository standards and recorded decisions apply across lenses. Cite actual
rules separately from judgment calls; standards compliance does not prove the
requested outcome was delivered.

Specialize the review brief instead of expanding the catalog: a migration raises
correctness and integration questions; a native boundary raises correctness and
security questions. Experience includes interfaces for people, developers, and
agents, along with the documentation they need.

Combine or split lenses to fit the work. Invent a new perspective when these do
not capture a meaningful risk; state its question and evidence standard in the
brief without requiring a new repository file.
