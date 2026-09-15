# Change routing

Every pull request is routed by **who owns the paths it changes**, before review. The project keeps
its ownership table in its decision log; this procedure is project-neutral.

## Routes

| Route | When | Reviews | Decides | Merges |
|---|---|---|---|---|
| Technical | Every changed path is Architect-owned | Architect | Architect | Architect |
| Product | Any changed path is Product Owner-owned, or is not in the table | Architect for technical content, if any; PO Assistant compiles | Product Owner | PO Assistant |

A path missing from the table takes the product route, and the PO Assistant's card proposes a table row.

## Procedure

1. **Classify.** List changed paths with `git diff --name-status <base>...<head>`. Look up each path in
   the ownership table. Record the route and the path list as a comment on the issue.
2. **Split.** If the pull request is mixed and the Architect-owned part stands alone, split it into two
   pull requests so the technical part does not wait for the Product Owner.
3. **Technical route.** The Architect reviews against the issue's acceptance criteria and merges.
   The Architect does not merge a pull request it authored: it delegates authoring to the Implementor.
4. **Product route: compile.** The PO Assistant posts one confirmation card to the Product Owner:
   - what changes, in product terms;
   - the path list and a short diff summary;
   - the Architect's review verdict when technical paths are included;
   - risks, and what is not covered;
   - a recommendation, with approve and reject options.

   If the pull request lands a document the Product Owner already accepted in Paperclip, and the diff
   matches that accepted revision, cite the accepting card instead of posting a new one.
5. **Product route: execute.** On approval, merge exactly the approved head commit
   (`gh pr merge <n> --merge --match-head-commit <sha>`). If the head changed after the card, post a
   new card. On rejection, return the issue to its owner with the Product Owner's reason.
   Executing means carrying out the approved decision; a step that needs a new choice goes back to the
   Product Owner.
6. **Record.** The card is the decision record. The merge commit and the closing comment cite the issue.

## Rules

- Nobody pushes to the default branch. Implementors never merge.
- Review requires green CI once CI exists.
- Re-classify when a pull request gains commits that add paths.
