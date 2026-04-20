# Write Autocomplete Implementation Instructions

## Goal

Improve the writing experience so sentence-completion suggestions appear automatically while typing, can be accepted with `Tab`, and can also be clicked in the autocomplete panel to copy the suggestion text.

## Scope

- [frontend/src/views/Write.vue](/Users/peternam/Desktop/onego/frontend/src/views/Write.vue)
- [frontend/src/components/layout/write/Autocom.vue](/Users/peternam/Desktop/onego/frontend/src/components/layout/write/Autocom.vue)
- Any related Vuex/module state in [frontend/src/store/modules/writeStore.ts](/Users/peternam/Desktop/onego/frontend/src/store/modules/writeStore.ts) if shared state is needed
- Optional shared CSS if the highlight/suggestion styling should be reused

## Desired Behavior

### 1. Debounced inline sentence completion in `Write.vue`

When the user types in the editor:

- detect the current sentence fragment near the cursor
- wait for a short idle delay before requesting completion
- recommended debounce delay: `600ms` to `1000ms`
- only request autocomplete if:
  - the current text is non-empty
  - the user has stopped typing
  - there is a meaningful sentence fragment to complete

### 2. Show inline suggestion with a shiny visual effect

When a completion suggestion is returned:

- show the suggested continuation inline in the editor area
- the suggestion should look visually different from normal text
- preferred appearance:
  - lighter or semi-transparent text color
  - subtle glow or shimmer effect
  - should feel like a ghost-text completion, not inserted content yet

Suggested UX:

- only show the top suggestion inline
- do not permanently insert it into the editor until accepted
- if the user keeps typing, the inline suggestion should disappear or refresh

### 3. Accept suggestion with `Tab`

When an inline suggestion is visible and the user presses `Tab`:

- prevent the default tab behavior
- insert the suggested completion into the editor content
- place the cursor immediately after the inserted text
- clear the pending inline suggestion state

If no suggestion is visible:

- keep the current existing `Tab` behavior for indentation

### 4. Autocomplete panel behavior in `Autocom.vue`

The existing autocomplete panel should keep listing multiple candidate sentences, but improve interaction:

- each sentence should be individually clickable
- on hover:
  - change text color or background color to show interactivity
  - show a tooltip labeled `copy text`
- on click:
  - copy the sentence text to the clipboard
  - do not include the leading number prefix such as `1.`, `2.`, etc.

### 5. Copy behavior details

If the displayed line is:

`1. 오늘은 문장을 조금 더 길게 써 보기로 했다.`

Then the copied text should be:

`오늘은 문장을 조금 더 길게 써 보기로 했다.`

Optional nice-to-have:

- briefly show copied feedback like:
  - tooltip change to `copied`
  - or a snackbar/toast

## Implementation Notes

### In `Write.vue`

Recommended approach:

1. Track the current editor text and cursor-aware active fragment.
2. Add a debounced autocomplete trigger method.
3. Call the `/ai/complete` endpoint with the current sentence fragment.
4. Store the top suggestion separately from the actual content.
5. Render the suggestion as ghost text or an overlay near the editor caret.
6. Handle `Tab` key acceptance only when a suggestion is active.

Important:

- do not spam the API on every keystroke
- cancel or ignore stale autocomplete responses if a newer request started later
- avoid showing a suggestion if it exactly duplicates already-typed text

### In `Autocom.vue`

Recommended approach:

1. Normalize the response into a list of plain suggestion strings.
2. Render each suggestion as its own clickable row/button.
3. Strip numeric prefixes before copying with a helper such as:
   - regex example: `^\s*\d+[.)]?\s*`
4. Use `navigator.clipboard.writeText(...)` for copying.
5. Add hover styling and a Vuetify tooltip labeled `copy text`.

## Suggested State Shape

If local component state is enough:

- `inlineSuggestion: string`
- `isSuggestionVisible: boolean`
- `isFetchingSuggestion: boolean`
- `lastAutocompleteQuery: string`

If shared state is needed:

- store suggestion text in `writeStore`
- keep UI-only hover/copy states local to `Autocom.vue`

## Acceptance Criteria

- typing pauses for the debounce interval and triggers completion
- an inline completion hint appears with a shiny/ghost effect
- pressing `Tab` accepts the suggestion into the editor
- typing again refreshes or clears the inline suggestion
- the `Autocom.vue` list shows clickable suggestion rows
- hover changes appearance and shows tooltip `copy text`
- clicking a sentence copies only the sentence text, without the numbering prefix

## Nice-to-Have Enhancements

- keyboard navigation for autocomplete suggestions
- `Esc` to dismiss inline suggestion
- use the top clicked suggestion to insert directly into the editor
- show loading state while awaiting `/ai/complete`
