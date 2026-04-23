# Testing Anti-Patterns — 9-Pathology Catalog

**Load this reference when:** writing or changing tests, adding mocks, authoring integration/e2e tests, or invoking the test-reviewer agent.

This file is the source of truth for the vocabulary the test-reviewer agent uses when flagging findings. Each entry maps a named LLM-test pathology to industry terms, detection signals, bad/good examples, and literature.

When the agent emits `WEAK ORACLE: self-fulfilling` or `MOCK SMELL: self-fulfilling`, the pathology has a name, a literature trail, and a known remediation — all here.

Ordered by severity and frequency per MSR '26 and MUTGEN data.

---

## Pathology 1: Self-fulfilling mocks

**Also known as**: tautological mocking, mock circular reasoning, self-validating tests, "testing the stub."

**What it is**: a test configures a mock to return value X and then asserts that the system returns X. The assertion is guaranteed by the mock setup, not by any SUT logic.

**Detection signal**: `when(dep.x()).thenReturn(VAL); ...; assertEquals(VAL, sut.method())` where the SUT does nothing but pass `VAL` through. Static scan: any test where the asserted literal matches a literal in the mock configuration with no intermediate transformation.

**Example (bad):**
```typescript
when(api.getUser(1)).thenReturn({ id: 1, name: 'Alice' });
const result = sut.fetchUserName(1);
assertEquals('Alice', result);  // proves only that the mock returned 'Alice'
```

**Example (good):**
```typescript
when(api.getUser(1)).thenReturn({ id: 1, first: 'Alice', last: 'Cooper' });
const result = sut.fetchUserName(1);
assertEquals('Alice Cooper', result);  // asserts SUT's first+last concatenation logic
```

**Reviewer check**: Check 4 flags as `MOCK SMELL: self-fulfilling`. Check 8 ALSO flags as `WEAK ORACLE: self-fulfilling` (double-flag per v2 design).

**Remediation**: either add a transformation the SUT performs that makes the assertion non-trivial, or remove the mock and use a real (or lightweight real) dependency.

**Literature**: MockMill study arXiv:2604.19315; Mark Sands "Mocking is Tautological" (2014); Randy Coulman "Tautological Tests" (2016); MSR '26 "Are Coding Agents Generating Over-Mocked Tests?" (andrehora.github.io/pub/2026-msr-agents-over-mocked-tests.pdf).

---

## Pathology 2: Asserting return shape, not behavior

**Also known as**: shape-only oracles, shallow oracles, type-only checks.

**What it is**: test only verifies structural properties of the output (type, presence of keys, length) without asserting on semantic content.

**Detection signal**: `expect(result).toHaveProperty('id')`, `expect(result.length).toBe(3)`, `expect(typeof result).toBe('object')`, `assert isinstance(result, dict)` without corresponding value assertions.

**Example (bad):**
```typescript
const result = await safariHover('#button');
expect(result.hovered).toBe(true);  // return shape, not hover behavior
```

**Example (good):**
```typescript
const result = await safariHover('#button');
expect(getComputedStyle(element)['background-color']).toBe('rgb(0, 0, 255)'); // verifies :hover CSS
```

**Reviewer check**: Check 8 flags as `WEAK ORACLE: shape-only`.

**Remediation**: assert on the specific observable effect of the claimed behavior, not just that the function returned a successful shape.

**Literature**: MUTGEN arXiv:2506.02954 (shallow oracles linked to low mutation scores); orbilu/ESE 2026 LLM test-smell study.

---

## Pathology 3: Happy-path-only coverage

**Also known as**: golden-path-only testing, positive-path-only.

**What it is**: tests exclusively exercise the successful scenario, neglecting errors, boundaries, and edge cases.

**Detection signal**: coverage report shows 100% line coverage on success path, 0% on error branches. No test mocks dependencies to throw. No boundary inputs (empty, null, max).

**Example (bad):**
```typescript
test('runs a task', async () => {
  await engine.run(async () => { /* success */ });
  expect(engine.failureCount()).toBe(0);
});
// No test for failure path
```

**Example (good):**
```typescript
test('increments failure count on exception', async () => {
  await expect(engine.run(async () => { throw new Error('boom'); }))
    .rejects.toThrow('boom');
  expect(engine.failureCount()).toBe(1);
});
```

**Reviewer check**: Check 3 flags as `GAPS` or `ERROR-PARITY GAP`.

**Remediation**: for each `throws`/`catch`/conditional error branch in the SUT, add a test that exercises it and asserts on the observable effect.

**Literature**: MUTGEN; CovQValue arXiv:2604.05159 (exploration-guided generation targets negative paths); systematic review arXiv:2511.21382.

---

## Pathology 4: Assertion-free tests

**Also known as**: empty tests, smoke-only tests.

**What it is**: test function executes code but has zero assertion calls. Passes as long as no uncaught exception is thrown.

**Detection signal**: AST scan for test function bodies lacking any `expect` / `assert` / `verify` / `should` / `toBe` / `toEqual` call.

**Example (bad):**
```python
def test_login_works():
    user = login(username='alice', password='pw')
    # no assertion — passes if login() returns anything non-throwing
```

**Example (good):**
```python
def test_login_returns_user_on_valid_credentials():
    user = login(username='alice', password='pw')
    assert user.username == 'alice'
    assert user.authenticated is True
```

**Reviewer check**: Check 8 flags as `WEAK ORACLE: assertion-free`.

**Remediation**: add an assertion on the observable effect of the operation. If truly a smoke test (does-not-crash check), name it `test_smoke_*` and allow-list it deliberately.

**Literature**: orbilu/ESE 2026 "Empty Test" smell prevalence; Siddiq et al. 2024 SF110 benchmark.

---

## Pathology 5: Tautological assertions

**Also known as**: trivial assertions, constant assertions.

**What it is**: assertions that are always true given the test setup — asserting literals equal themselves, or checking properties that cannot meaningfully fail.

**Detection signal**: `expect(1).toBe(1)`, `assert True`, `expect(typeof sut).toBe('object')` (always true for any defined class), assertions comparing a variable to the literal it was just assigned.

**Example (bad):**
```typescript
const sut = new Engine();
expect(sut.isReady).toBeDefined();  // always passes for any Engine instance
```

**Example (good):**
```typescript
const sut = new Engine();
await sut.initialize();
expect(sut.isReady).toBe(true);  // verifies initialization actually set the flag
```

**Reviewer check**: Check 8 flags as `WEAK ORACLE: tautological`.

**Remediation**: assert on a state that actually resulted from SUT work, not a state that was always true.

**Literature**: orbilu/ESE 2026 tautological-assertion prevalence; TsDetect test-smell tooling.

---

## Pathology 6: Tests that pass regardless of implementation

**Also known as**: vacuous tests, implementation-agnostic tests, weak oracles.

**What it is**: test is structured so it would pass for many plausible (including incorrect) implementations of the SUT.

**Detection signal**: mentally (or actually) replace the SUT body with `return null` or `throw new Error()`. If the test still passes or the test doesn't exercise the SUT at all, it's vacuous.

**Example (bad):**
```typescript
test('processPayment works', async () => {
  const result = await processPayment(100);
  expect(result).toBeDefined();  // passes for ANY non-undefined return
});
```

**Example (good):**
```typescript
test('processPayment charges the card and returns txn id', async () => {
  const result = await processPayment(100);
  expect(result.status).toBe('success');
  expect(result.amount).toBe(100);
  expect(await card.balance()).toBe(originalBalance - 100);
});
```

**Reviewer check**: Check 1 flags as `WEAK` + Check 8 flags as `WEAK ORACLE: trivially-passable`.

**Remediation**: strengthen assertions to verify specific semantic outcomes that only a correct implementation produces.

**Literature**: MUTGEN 100%-line / 4%-mutation evidence; Outsight AI case study (Cursor/Copilot coverage-vs-mutation gap).

---

## Pathology 7: Over-mocking

**Also known as**: unnecessary mocking, mocking local classes.

**What it is**: replacing dependencies with mocks where exercising the real dependency (or a lightweight real implementation) would be feasible. Particularly harmful for local, in-repo classes and pure-computation collaborators.

**Detection signal**: test mocks a class defined in the same repo; test has multiple `jest.mock()` or `Mockito.mock()` calls for classes without external I/O; heavy `@patch` decoration.

**Example (bad):**
```python
@patch('myapp.utils.format_currency')
@patch('myapp.tax.calculate_tax')
@patch('myapp.discount.apply_discount')
def test_order_total(mock_discount, mock_tax, mock_fmt):
    # mocks three pure functions that could just run
    mock_fmt.return_value = '$10.00'
    ...
```

**Example (good):**
```python
def test_order_total_applies_discount_and_tax():
    order = Order(items=[...], discount_code='SAVE10')
    total = compute_total(order)  # runs real format_currency, calculate_tax, apply_discount
    assert total == '$10.50'
```

**Reviewer check**: Check 4 flags as `MOCK SMELL: over-mocking`.

**Remediation**: exercise real collaborators when they are fast, pure, or lightweight. Reserve mocks for slow I/O, third-party APIs, and non-deterministic sources.

**Literature**: MockMill arXiv:2604.19315; MSR '26 agent over-mocking rate (36% vs 26% human baseline).

---

## Pathology 8: Snapshot tests locking in wrong behavior

**Also known as**: golden-file regressions, snapshot rot, baseline freeze.

**What it is**: snapshot test captures output at time T. If T's output is wrong, the wrong output becomes the approved baseline. Future runs pass as long as they keep reproducing the bug.

**Detection signal**: `toMatchSnapshot()` calls; frequent large snapshot file diffs in git history; snapshots containing error messages, stack traces, or known-bad values.

**Example (bad):**
```typescript
test('renders user profile', () => {
  const { container } = render(<UserProfile user={mockUser} />);
  expect(container).toMatchSnapshot();  // snapshot captures whatever initially renders, bugs and all
});
```

**Example (good):**
```typescript
test('renders user profile with name and verified badge', () => {
  render(<UserProfile user={mockUser} />);
  expect(screen.getByRole('heading', { name: 'Alice Cooper' })).toBeInTheDocument();
  expect(screen.getByLabelText('verified')).toBeInTheDocument();
});
```

**Reviewer check**: Check 8 flags snapshot tests with suspicious content as `WEAK ORACLE: snapshot-lock`.

**Remediation**: replace snapshot tests with targeted assertions on specific observable outputs. If snapshots are unavoidable (complex structured output), require human review of every snapshot update — never blanket-approve.

**Literature**: Jest documentation warnings; orbilu/ESE 2026 snapshot-lock prevalence.

---

## Pathology 9: Copy-pasted near-duplicate tests

**Also known as**: duplicated tests, test cloning, redundant tests.

**What it is**: multiple tests that are nearly identical, differing only in variable names or literal values. Inflates test count and maintenance burden without adding coverage.

**Detection signal**: high token-level similarity between test functions; adjacent `test()` or `def test_*()` blocks with identical structure and different literals.

**Example (bad):**
```typescript
test('adds 1 + 1', () => { expect(add(1, 1)).toBe(2); });
test('adds 2 + 2', () => { expect(add(2, 2)).toBe(4); });
test('adds 3 + 3', () => { expect(add(3, 3)).toBe(6); });
```

**Example (good):**
```typescript
test.each([
  [1, 1, 2],
  [2, 2, 4],
  [3, 3, 6],
])('adds %i + %i = %i', (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});
```

**Reviewer check**: this pathology is **ADVISORY-only** in v2 (research classifies as noise-not-bugs). The agent may emit a one-line note in the ADVISORY section: "heads up: `test_foo` and `test_bar` differ only in literal values — consider parameterizing." No PASS/REVISE verdict implication.

**Remediation**: consolidate into parameterized / table-driven tests. Not urgent.

**Literature**: TsDetect; Siddiq et al. 2024; orbilu/ESE 2026.

---

## Meta: When to override

Every pathology in this catalog has legitimate exceptions. Flags are starting points for a conversation, not automatic rewrites. If you have a specific reason a "pathology" is the right choice (e.g., shape-only assertion is intentional because the SUT is a type guard; snapshot is intentional because the output is genuinely large and stable), annotate the test with `// test-discipline: allow-<pattern> reason:<justification>` and the reviewer will suppress the flag for that specific test.

The goal is signal, not ceremony.

---

## Quick Reference — Flag → Pathology → Remediation

| Reviewer flag | Pathology | Primary fix |
|---|---|---|
| `MOCK SMELL: self-fulfilling` + `WEAK ORACLE: self-fulfilling` | Self-fulfilling mock | Remove mock or add transformation |
| `WEAK ORACLE: shape-only` | Shape-only oracle | Assert on computed value, not shape |
| `GAPS` / `ERROR-PARITY GAP` | Happy-path-only | Add test per error branch |
| `WEAK ORACLE: assertion-free` | Assertion-free test | Add explicit assertion |
| `WEAK ORACLE: tautological` | Tautological assertion | Assert on post-condition state |
| `WEAK` + `WEAK ORACLE: trivially-passable` | Vacuous test | Assert on semantic outcome |
| `MOCK SMELL: over-mocking` | Over-mocking | Run real collaborators |
| `WEAK ORACLE: snapshot-lock` | Snapshot rot | Targeted assertions on specific content |
| ADVISORY line about duplication | Copy-paste tests | Parameterize (low priority) |

---

## Integration with TDD Skill

The TDD skill (`SKILL.md`) references this catalog by name. When the test-reviewer agent flags an issue using a name from this file, developers can look up the pathology here for full context, examples, and remediation guidance.

Following strict TDD and Chicago-school practices (see `SKILL.md` sections "Chicago-School TDD" and "Testing Through the Production Boundary") prevents most of these pathologies at authoring time.
