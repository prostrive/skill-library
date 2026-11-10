---
name: codebase-design
description: Shared vocabulary and principles for designing deep modules, placing seams and making code testable through its interface. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or easier for agents to navigate, or when another skill needs the deep-module vocabulary.
---
<!-- Based on mattpocock/skills: skills/engineering/codebase-design (MIT) -->

# Codebase design

Design **deep modules**: a lot of behavior behind a small interface, at a clean seam, testable through that interface. The aim is leverage for callers, locality for maintainers and testability for everyone.

## Vocabulary

Use these words exactly. Do not swap in "component", "service", "API" or "boundary". Consistent words are the point.

- **Module**: anything with an interface and an implementation, at any scale: a function, a class, a package, a slice across tiers. Avoid: unit, component, service.
- **Interface**: everything a caller must know to use the module: the types, plus invariants, ordering, error modes, required config and performance. Avoid: API, signature (too narrow).
- **Implementation**: the code inside a module. Say "adapter" when the seam is the topic, "implementation" otherwise.
- **Depth**: leverage at the interface. How much behavior a caller or test gets per unit of interface it must learn. **Deep**: much behavior behind a small interface. **Shallow**: the interface is nearly as complex as the implementation.
- **Seam** (Michael Feathers): a place where you can change behavior without editing that place. It is where a module's interface lives. Where to put the seam is its own decision. Avoid: boundary.
- **Adapter**: a concrete thing that fills an interface at a seam. It names a role, not a size.
- **Leverage**: what callers get from depth. One implementation pays back across many call sites and tests.
- **Locality**: what maintainers get from depth. Changes, bugs and checks sit in one place. Fix once, fixed everywhere.

If the project has a `GLOSSARY.md`, use its domain words for the things the modules model.

## Deep vs shallow

```
Deep                         Shallow (avoid)
┌───────────────┐            ┌─────────────────────────┐
│ small interface│            │ large interface         │
├───────────────┤            ├─────────────────────────┤
│               │            │ thin implementation     │
│ deep          │            └─────────────────────────┘
│ implementation│
└───────────────┘
```

When you design an interface, ask:
- Can I remove a method?
- Can I simplify the parameters?
- Can I hide more inside?

## Principles

- **Depth belongs to the interface, not the implementation.** A deep module can be built from small swappable parts inside. Those parts are internal seams, used by its own tests, and not part of the interface.
- **The deletion test.** Imagine you delete the module. If complexity disappears, it was a pass-through. If complexity reappears across many callers, it earned its place.
- **The interface is the test surface.** Callers and tests cross the same seam. If you need to test past the interface, the module has the wrong shape.
- **One adapter is a hypothetical seam. Two adapters make a real one.** Do not add a seam unless something actually varies across it, usually production and test.

## Design for testability

1. Accept dependencies, do not create them.

   ```typescript
   function processOrder(order, paymentGateway) {}   // testable
   function processOrder(order) {                    // hard to test
     const gateway = new StripeGateway();
   }
   ```

2. Return results, do not cause side effects.

   ```typescript
   function calculateDiscount(cart): Discount {}     // testable
   function applyDiscount(cart): void {              // hard to test
     cart.total -= discount;
   }
   ```

3. Keep the surface small. Fewer methods need fewer tests. Fewer parameters need less setup.

## Relationships

- A module has exactly one interface.
- Depth is measured against that interface.
- A seam is where the interface lives.
- An adapter sits at a seam and fills the interface.
- Depth gives leverage to callers and locality to maintainers.

## Go deeper

- Deepening a cluster of modules given its dependencies, with seam rules and "replace, don't layer" testing: [references/deepening.md](references/deepening.md).
- Comparing several radically different interfaces with parallel subagents: [references/design-it-twice.md](references/design-it-twice.md).
