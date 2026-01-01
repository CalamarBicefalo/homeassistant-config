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