# Journeys

Flows that cross several features. A sweep ends here, because a journey can break when each feature on its own still passes.

## Sub-features

- `journey-create-then-find`: a note created in the browser is found by CLI search.

## How to get to it (user POV)

- Create a note in the browser, then search for it from the terminal.

## Driving it with control-notes

Preconditions: baseline state.

- **Create:** `control-notes browser click "New note"`, type the title `Journey check`, save. Expect the note in the list.
- **Find:** `control-notes cli -- notes search "Journey check"`. Expect one result with that title and exit code 0.

## Gotchas

- The CLI reads the same data folder as the browser instance only when `NOTES_DATA_DIR` matches. Check it with `control-notes info`.
