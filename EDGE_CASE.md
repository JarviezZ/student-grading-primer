# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation

# Edge Case: Handling Invalid or Non-Integer Marks

1) Identified Edge Case

The specification does not clearly define how the system should behave if a client submits a `mark` value that is:

- A string instead of an integer,
- A non-numeric string,
- Or a number outside a reasonable academic range.

Since marks represent academic scores, allowing invalid values could corrupt data integrity.


2) How It Is Handled in the Implementation

In `POST /students` and `PUT /students/<id>`, I implemented validation logic to ensure:

- If `mark` is provided as a numeric string (e.g., `"88"`), it is safely converted to an integer.
- If `mark` is not an integer after validation, the API returns:
  
  `400 Bad Request`

- If `mark` is outside the valid range (0–100), the API also returns:
  
  `400 Bad Request`

This ensures:

- Database consistency
- Clear feedback to API users
- Prevention of invalid academic records