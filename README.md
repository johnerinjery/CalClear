# CalClear

A Google Calendar API CLI that clears weekly recurring events in my Google Calendar. I made this to be run at end of a semester to clear my calendar.

I use this along with my project [PDF2Cal](https://github.com/johnerinjery/PDF2Cal) to set up the new timetable.

## Usage

After cloning this repo, replace ```credentials.txt``` with your ```credentials.json``` file. Inside a python environment, run 

```bash
pip install -r requirements.txt
```
to install dependencies. Then run

```bash
python src/main.py
```
When run for the first time, it will ask you to choose the Google account to run the program inside (you might need to sign in). This choosing will generate a ```token.json``` file inside the directory, specific to the chosen google account.

If you wish to run the program again for a different account, delete ```token.json``` and run the program again.

## Footnote
Setting up the Google Cloud project for the first time might be a bit tricky. See this [quickstart](https://developers.google.com/workspace/calendar/api/quickstart/python) guide if needed.

## Disclaimer
The program will give a preview of what all events are to be deleted, requesting affirmation. Please note that the program detects ALL the events that recur weekly. 

It's not a problem for me personally because I only have my college time table as a weekly recurring event, but it might be troublesome for some users. Use at your own discretion.