# Tests

Tests should be as concise and expressive as possible and focus on outcomes 
and not implementation details. 

- For example a test that checks that when 
a given sensor state changes, a new activity is set is good. 
- A test that checks that when a state change an arbitrary callback is 
executed is NOT ideal.

The test framework is limited and sometimes there’s no way around it. 
In those cases where possible try to create appropriate test doubles to 
preserve the spirit of concise, expressive, and outcome oriented testing.

## Fakes

When possible for the sake of readability, we create fakes with:
State machine approach: State is the single source of truth
Observable state: Tests assert on what they can observe, not internal flags
Protocol & Runtime checks: We introduce protocols and verify both fake and real implementation against