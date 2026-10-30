# Gate Doctrine Module: why your tests pass and your batch still breaks

> **Generic guidance for maintaining your own resource hub.**
> **Recall triggers:** writing a gate · writing a verification script · choosing a sample page to build against · *"all my gates are green"* · a batch broke that the test page didn't · a generator says the check itself is wrong · deciding whether a defect is real.

A gate is any automatic check that decides whether work may move forward: a test, a lint rule, a script that compares counts, a reviewer's checklist. This module collects the ways gates pass while the work is still wrong, and the habit that prevents each one.

---

## THE ONE-PARAGRAPH VERSION

Knowing about a bias does not protect you from it. Careful people, and careful agents, repeat the same mistakes because the mistake feels like good judgement at the moment it is made. So every rule below is a **mechanical step** you can put into a checklist or a script, not a reminder to "be careful". If a rule depends on noticing the problem in the moment, it will fail in the moment.

---

## 🔴 RULE 0: FILE A LESSON UNDER ITS CLASS, NOT UNDER THE TOOL THAT TAUGHT IT

Suppose you discover that a spreadsheet export showed an empty column because the export tool skipped that column, not because the data was empty. If you write the lesson down as "the export tool skips columns", it will come to mind only the next time you use that export tool. It will stay silent when a web scraper returns an empty list, when a search finds no matches, or when a log contains no errors, even though each of those can be the same mistake.

The general lesson is: **a tool's silence is evidence about the tool, not about the thing it looked at.**

- **Name the class first** and list specific tools underneath it as examples.
- **Search for and tag notes by the class.** A note tagged `tool-silence-does-not-prove-absence` will be found in more situations than one tagged with a product name.
- **Check your own lesson titles.** If the title names a single tool, rewrite it so it names the failure.

---

## 1. 🔴 ONE SAMPLE PAGE CANNOT SHOW YOU THE WHOLE COLLECTION

Building a template against one carefully chosen "representative" entry is a good way to check the **design**. It cannot check the **data**, because data problems are spread unevenly: only some entries are unusual, and one sample is either unusual or it is not.

A sample chosen for being "complete" is the entry least likely to have gaps. A sample chosen for being "difficult" is difficult only in the ways you already had in mind.

**Invented example: a seed library with one page per seed variety.** The template was built against a well-documented tomato. When the whole catalogue was rendered:

- Varieties with two common names written as "Runner bean / Pole bean" produced broken page addresses, because the slash was copied into the URL.
- Sowing windows that cross the new year ("November to February") rendered as empty, because the month-range code assumed the start month comes before the end month.
- A few germination rates were stored as the word "unknown" rather than a number, and the percentage formatter crashed on them.

None of these appeared on the tomato page.

### The countermeasure: survey every field before any batch

Before rendering a batch, **survey the whole collection** for every field the template displays. Not a sample.

- **Emptiness:** a real value, `null`, an empty string, only spaces, or a placeholder word such as "TBD" or "unknown"
- **Shape:** punctuation, symbols, unusual characters, very long or very short values, values in the wrong type
- **Geometry:** for images and files, orientation, size, page count and whether text can be extracted
- **Spread:** a field where nearly every entry holds the same value cannot be used to tell entries apart

One `GROUP BY` query, or a short script that counts distinct values, often finds what several careful reviews missed.

---

## 2. 🔴 A GATE NEEDS PROOF IT CAN PASS, NOT ONLY PROOF IT CAN FAIL

A "mutant" is a deliberately broken input used to confirm a gate catches mistakes. That proves the gate can **fail**. It says nothing about whether the gate **passes correct work**.

A gate that is too strict rejects good input. Every mutant is bad input, so every mutant is still rejected, and the test suite looks perfect while the gate blocks real work.

**Invented example:** an astronomy club adds a gate that every event page must include a ticket link. All the broken test pages are rejected, as expected. The gate also rejects every free public observing night, which is the kind of event the club most wants to promote. Only a correct page without a ticket, used as a **positive control**, reveals this.

> **Every gate ships with at least one mutant AND at least one positive control.**

A positive control covers only the cases it represents. Use the survey from §1 to decide which real shapes need a positive control.

---

## 3. 🔴 THE THING BEING CHECKED MAY NOT CHANGE THE CHECK

When a generator, or the person who did the work, reports that a check is wrong, that report may be correct. It may also be the easiest way to make a failing result pass. The rule:

- **Keep the checks and scoring rules fixed for the whole of one review loop.** If they change halfway, earlier and later scores can no longer be compared.
- **A disputed check is decided by someone independent of the work**, such as the reviewer or a person, not by the generator that failed it.
- **If the check really is wrong, fix it between loops**, write down why it changed, and re-run the earlier work against the corrected check.

---

## 4. 🔴 A MEASUREMENT CAN ANSWER A NEARBY QUESTION

Many tools give a confident answer to a slightly different question from the one you asked. Each of these can look like a clean result:

- **`command | tail` returns the exit status of `tail`**, not of `command`. A failed command followed by a successful `tail` looks like success. Write the command's output and its exit status to files, then read them.
- **`HTTP 200` describes the request, not the file.** Some servers return a normal page with status 200 for addresses that do not exist. Check the content type and the first bytes of the response.
- **A printed `None` or `null` may be how a program displays an empty value**, not text stored in the data.
- **The first few lines of a file are not the file.** Count lines before deciding you have seen everything.
- **A search with no matches proves nothing until you show the search could have matched.** Run it once on a case where the target is known to be present (a positive control).
- **A field's name is a claim.** A field called `exact_quote` may still contain a paraphrase.

---

## 5. 🔴 A REQUIRED FIELD WITH NO SOURCE INVITES INVENTION

If a template requires a field and nothing says where its value must come from, a writer under pressure to complete the template, and especially a language model, will supply something plausible. Structural checks still pass, because they test that the field exists and is well formed, not that it is true.

**Invented example:** a ceramic studio's class-page template requires an instructor biography. For a new class with no biography on file, the generated page includes a confident, pleasant, entirely invented one.

> **For every field a template displays, name where its value comes from and which check confirms it. A field that has neither must be optional, never required.**

When the evidence is missing, leaving the field out is better than filling it.

---

## 6. 🔴 WRITE DOWN HOW A NUMBER IS DERIVED, NOT JUST THE NUMBER

Code can be tested while the prose around it is never checked again. A total written into a comment, a README or a report is a measurement frozen at one moment, and it drifts as the data changes.

> Write "count the published guides that have a download link" instead of copying today's total. The description stays correct; the copied number does not.

Prefer stable descriptive names over temporary identifiers when linking notes, for the same reason.

---

## 7. 🔴 AN ASSERTION ONLY PROTECTS WHAT IT NAMES

Checks such as "every item has a unique key" or "the file count matches" are worth having. They catch, for example, two pages whose shortened slugs collide and overwrite each other.

They cannot catch a problem with a field they do not mention. A content migration can pass every count, hash and filename check while dropping image alt text, because no check looked at alt text.

> Report exactly what was checked ("filenames and file hashes match"), never a broader claim such as "nothing was lost".

A table written for people to read often merges details that the source keeps separate. When you need to verify something, compare against the source data, not the human-friendly summary.

---

## 8. 🔴 A RULE BORROWED FROM ANOTHER SITE BRINGS ITS ASSUMPTIONS

A rule such as "show related resources from the same category" works only if categories actually separate the content. On a bicycle-repair co-op's site, almost every guide might be filed under "repair", so the rule would recommend nearly everything. A different field, such as the part of the bike, might separate the guides well.

> Before reusing a rule, check that the field it relies on actually tells entries apart **in this collection**.

---

## 9. 🔴 WHEN DOCUMENTATION AND WORKING CODE DISAGREE, START FROM THE CODE

Written guidance usually carries an **intent** and an **illustration**. The intent tends to stay true. The illustration (a specific setting name, an exact string, a code sample, a capitalisation choice) goes out of date on its own.

**Ask: what would break if I did the opposite?** If nothing would break, that detail was probably an illustration.

Running code is exercised against real data and real services, so it is often the more accurate description of current behaviour. Confirm that it still meets the intent, then update the documentation so the two agree.

---

## 10. 🔴 YOU REVIEW OTHER PEOPLE'S WORK MORE STRICTLY THAN YOUR OWN

People read someone else's work for what it says and their own work for what they meant. That is why a reviewer can spot a mistake in another person's work and then make it themselves.

> **The reliable defence is independence:** a separate reviewer, with criteria that do not depend on the author's explanation.

- **Check the checker.** A review script can be wrong too. Say so when you find out.
- **Prefer "follow the instruction and flag the problem" over "quietly improve it".** A silent fix hides the conflict, and the next run reintroduces it. Raise the conflict so the instruction itself gets corrected.

---

## THE CHECKLIST

Before any batch:

- [ ] **Survey** every displayed field across the whole collection: emptiness, shape, geometry, spread
- [ ] Every gate has **at least one mutant** *and* **at least one positive control**
- [ ] Checks and scoring rules stay **fixed within a loop**; disputes go to an independent reviewer
- [ ] Exit statuses are read from files, not through pipes; negative searches have a positive control
- [ ] Every required field names **where its value comes from** and **which check confirms it** (otherwise make it optional)
- [ ] Prose names **how a number is derived** instead of freezing the number
- [ ] Reports claim **only what was checked**
- [ ] Borrowed rules: does the field they rely on **tell entries apart here**?
- [ ] Documentation and code disagree: **start from the tested code**, check it against the intent, then fix the documentation
