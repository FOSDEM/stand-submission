# FOSDEM

This is the tool that allows you to submit a request for a stand at [stands.fosdem.org/submission](https://stands.fosdem.org/submission).
Most if not all of the information in this document will only be useful for FOSDEM staff, as you probably can't or won't want
to use this for something else.

## Add a new edition

*Note: This requires both SSH access to the server on which this tool runs and admin access to the back-end.*

### In the admin area
*To be found at [stands.fosdem.org/admin](https://stands.fosdem.org/admin).*

1. Create a new *Fosdem edition* for the next edition.
2. Create a new *Fosdem stands edition* for the next edition.
    1. Set *Submissions open* to true (set this to false when closing the submissions).
    2. Set the *Deadline*. The tool will refuse to accept any submission after this deadline, so to allow latecomers, set this
       to some time later than the actual deadline.
    3. Write something creative for the *Blurb* (this is shown on the submissions page). HTML can be used.
    4. Link to the *Edition* you just created.
3. (Optional) Add, remove or update the themes for the stands.

### On the server
*To be found in our data center.*

1. Update */var/opt/app/fosdem_submission/latest/standssubmission/standssubmission/local_settings.py* so it reads:
    1. *EDITION* to whatever you set as edition in the admin area (e.g. 2024).
    2. *SUBMISSION_DEADLINE* to the announced submission deadline.
    3. *ANNOUNCEMENT_DATE* to the date you are going to announce the list of accepted stands.
2. Restart the *fosdem_submission* service.
