# LHM_Scheduler_Tool
web app to assist in scheduling DJs for LHM's Decks on Deck event based on prioritizing DJs in the roster by their last scheduled date.


ORIGINGAL GPT PROMPT

I need help making a web app that I will run locally. We’ll use a Flask backend with HTML, CSS, and JavaScript on the frontend, and JSON for storing data.
This app is a tool to help me schedule DJs based on their most recent performance, taking future performances into account.
The JSON structure will use the DJ name as the key. Each entry will have:
* an index (automatically assigned as one greater than the highest current index),
* a list of performance_dates (in YYYY-MM-DD format).

🎨 Priority Color System (“Tier System”)
We will calculate the “priority color” for each DJ based on the time difference between today and their most recent performance date, including both past and future dates.
* Red: DJ has a scheduled performance within ±14 days of the most future performance date in the data
* Yellow: 15–45 days from that future-most date
* Green: 46–90 days from that future-most date
* Blue: Over 90 days out or no performance data at all
This color code will be used throughout the UI to indicate recency and scheduling priority.

🧭 Main Page (index.html)
Page title: LHM Scheduler Tool
Section 1: Performance Schedule Table
* One row per unique performance date found in the data
* Columns:
    * Date
    * DJs performing that day (names from DJs whose list includes that date)
    * “Edit” button → links to edit_performance.html
* Search bar above the table to filter by DJ name
* Button at the bottom → links to add_performance.html
Section 2: Full DJ Roster Table
* One row per DJ
* Columns:
    * DJ name
    * Most recent performance date (from their list)
    * “Edit” button → links to edit_dj.html
* Each row should be color-coded by priority color
* Search bar above table for name filtering
* Checkbox filters for each priority color (Red, Yellow, Green, Blue)
* Button at bottom → links to add_dj.html

🧾 add_performance.html
* Form with:
    * Date picker
    * Dropdown list of all DJs in the roster, with names styled in their current priority color
* On double-clicking a DJ, add them to a visible “lineup” list (also color-styled)
* Below lineup list:
    * “Submit” button → assigns the selected date to each DJ's performance_dates
    * Show confirmation message
* Link back to main page

✏️ edit_performance.html
* Page for editing the lineup for a specific performance date
* Ability to:
    * Add/remove DJs from that date
    * Option to remove the date entirely
* “Submit” button to save changes
* Show confirmation message
* Link back to main page

➕ add_dj.html
* Form with:
    * Text field for DJ name (required)
* On submit:
    * Add new DJ to JSON with no performance dates
    * Assign them an index that is one greater than the current highest
    * Show confirmation message
* Prevent duplicate DJ names
* Link back to main page

🛠 edit_dj.html
* Form to:
    * Edit DJ name
    * Edit performance dates list
* Submit button to update
* Update all references to DJ name throughout the data
* Show confirmation message
* Link back to main page
