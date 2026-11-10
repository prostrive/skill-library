# Good and bad tests

## Good tests

A good test checks behavior through the public interface. It survives a refactor that keeps the behavior.

```typescript
test("user can check out a valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

- It uses the public API only.
- Its name says what happens, not how.
- It has one logical assertion.

## Bad tests

**Tied to the implementation.** It breaks on a refactor although the behavior did not change.

```typescript
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

**Checks through a side door.** Read the result through the interface, not the database.

```typescript
// Bad
await createUser({ name: "Alice" });
const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
expect(row).toBeDefined();

// Good
const user = await createUser({ name: "Alice" });
expect((await getUser(user.id)).name).toBe("Alice");
```

**Cannot fail.** The expected value is computed the way the code computes it.

```typescript
// Bad
const expected = items.reduce((sum, item) => sum + item.price, 0);
expect(calculateTotal(items)).toBe(expected);

// Good
expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
```

Other tests that cannot fail:

- The test starts in the state it asserts.
- The test asserts that something did not happen, without proof that the code path ran.
- The test asserts on a mock it configured to return the expected value.

## Mocks

Mock only at system boundaries: external APIs, time, randomness, and sometimes the file system or database (prefer a test database).

Do not mock your own modules or internal collaborators.

Make boundaries easy to mock:

- Pass the external client in. Do not create it inside the function.
- Give each external operation its own function (`getUser`, `createOrder`), not one generic `fetch(endpoint)`.
