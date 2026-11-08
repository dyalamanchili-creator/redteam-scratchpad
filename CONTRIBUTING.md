# Contributing (to your own scratchpad)

It's a working copy — keep it usable, not pretty.

- **One concept per note.** New technique → new `techniques/*.md` from the template.
- **Every note ends in a mitigation/detection.** That's the point.
- **Payloads are canaries, not weapons.** No destructive or mass-targeting payloads; link
  to public corpora instead of vendoring them.
- **Never commit:** secrets, real creds, captures (`harness/out/`), `.tfstate`, PII.
  `.gitignore` covers the common cases — check `git status` before committing.
- **Labs stay isolated.** Loopback / sandbox account only. Tear down after.
- **Scope first.** Update `SCOPE.md` before any run against something new.
