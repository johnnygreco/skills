# Security

Does the change preserve trust boundaries and protect sensitive resources?

- Trace who controls inputs and which actions or resources those inputs can
  influence. Check that the enforcing boundary applies the required restrictions.
- Examine changes to authority, isolation, and default access against the actual
  actors and deployment model.
- Follow sensitive information through storage, outputs, logs, and external
  systems. Identify concrete exposure or misuse introduced by the change.
- Inspect assumptions about dependencies or external data where they cross a
  trust boundary.

Describe the actor's required access, reachable path, and impact. Tie missing
protections to an actual threat or requirement instead of proposing generic
hardening beyond the project's needs.
