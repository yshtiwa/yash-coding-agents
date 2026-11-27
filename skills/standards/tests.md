# Tests

## What to test

- **Our own logic.** Every rule, calculation, mapping and decision we wrote.
- **At a boundary.** Give a function or a stage its input and check its
  output is exactly what the next step expects. Each small function's input
  and output is a fair place to test.
- **Not a library.** A test that saves a thing and reads it back proves the
  library works. Check an outside boundary by hand once, then leave it.
- **Not pure wiring.** Code that only passes values along has nothing of ours
  to assert. Say "no test: wiring only" in the report and let the real run
  cover it. A test written anyway would pass by construction.

## The two-edit check

Ask these of every test. It must pass both.

1. **Break the behaviour.** Would this test fail? If not, it tests nothing.
2. **Change the internals, keep the behaviour.** Would this test still pass?
   If not, it is tied to how the code works and will break on every tidy-up.

## Tests that look fine and are not

| Name | What it looks like | The tell |
|---|---|---|
| Tautological | The expected value is worked out with the same formula as the code | It cannot fail |
| Implementation-coupled | It checks which helper was called, or in what order | It breaks when you rename a helper |
| Peeking behind | It reads a private field or the stored file to check a result the function returns | It skips the real interface |
| Faking our own code | It replaces one of our functions with a stand-in | It tests the stand-in |
| All tests first | Ten tests written before any code | They check imagined behaviour |
| Weakened to pass | An assertion was loosened or removed to go green | The diff shows it |

## Rules

- **One test, then the code for it, then the next.** Never a batch of tests
  up front.
- **A new test that passes on its first run is suspect.** Find out why.
- **Expected values are typed by hand** from the requirement, never computed
  by the code under test.
- **Stand-ins only at the outer edge** (network, clock, an outside service).
  Prefer the real thing, then a simple fake. Never stand in for our own code.
- **Each test stands alone:** readable without opening another file, one idea
  per test, a name that reads as a sentence about behaviour. Repeating setup
  across tests is fine.
- **Check the kind of error, not its wording.**
- **Repeatable.** Same result every run. No real clock, network or shared
  state.
- **Pair every "this never happens"** with a test where it does.

## Prove the tests bite

After the tests pass, do this once per ticket:

1. Break one thing the change added (flip a condition, change a number).
2. Run the tests. At least one must fail.
3. Put it back. Run the tests. All pass.

If nothing failed in step 2, a test is missing. Write it.

## By kind of change

- **New behaviour:** a failing test first, then the code.
- **Bug:** a test that shows the bug first. After the fix, the original
  failing command must also pass; a unit test alone does not prove the bug
  is gone.
- **Change of structure only:** record the current output first. Afterwards
  the output must be identical, and existing tests pass unchanged. If a test
  had to change, behaviour changed.

## Never

- Skip, delete or loosen a test to go green.
- Edit a fixture or an expected value so the code passes. If the expected
  value looks wrong, stop and ask.
- Reshape the code only to dodge a check.
