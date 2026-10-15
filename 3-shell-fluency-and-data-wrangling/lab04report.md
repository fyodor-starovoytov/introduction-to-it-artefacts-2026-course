1. .gitignore makes sure that the file with that name in that directory will never be added to git for its uselesness in a remote repository or for its privateness.

2.  1. Count all lines in x file
    2. Count all lines containing ERROR word inside
    3. Get the second word or element of the line, which in this scenario contains WARN, INFO or ERROR indicating the severity of the log, sort it and get all of them together.
    4. Get the third element of the log, which now contains the operation done.
    5. Get all the error lines and then get the third element of the ERROR lines to get what operations caught the ERROR. Sort and count.
3. | Connects 2 or more commands so we dont have to manually enter all the data we get from one to another, making it easier for us.
4. uniq -c counts only similar adjacent lines, so if a line is between two other lines that have different value it won't be counted. Sorting makes the lines with same value adjacent and countable by uniq -c
5. ">" rewrites the file or creates a new one. Using it on an existing file rewrites it completely with the data given before it, therefore for safer modification you either create a new file instead of overwriting the same or use >> to add data to the file, not overwrite it.