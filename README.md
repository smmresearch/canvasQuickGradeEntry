Runs in Python with pandas and numpy packages. 

Allows the creation of a csv file to upload to Canvas by typing in a few letters of a student's name and the score.
The canvas file should be obtained by downloading the gradebook with the students and deleting all of the columns except (Student	ID,	SIS User ID,	SIS Login ID	,Section).
This file can then be reused for the class every time.

It looks up students based upon 1-4 letters of the first name and 1-4 letters of the last name (case insensitive, no space). There is also a fallback of the full name.
For example, Jillian Weeks could be found with jw, jwee, jiwe, jilw, etc., and jillianweeks.
If multiple students in the class have similar initials, the user is prompted to add more letters to update the score.

If a student has multiple or hypenated names, as long as name A comes before name B, name A can be used as the first name and name B as the last.
For example, in Canvas a name appearing as Wood-Stock, Michael John could be found with mwoo, jwoo, msto, jsto, or even mjoh or wsto. It would not be found with jmic.

If the initials collide with one of the options below, it cannot be used.

It provides a warning for grades higher than 110% of the points possible.

Other options:
viewit: shows the current state of the table
finish: saves the final CSV
restZero: sets all currently blank entries to be 0
undoit: undoes the last score change
