# Remote Control Another Computer Using Email

## A fully functional remote control program that uses email to send commands and receive results.

### Features:

- Send command from one computer to another using email.
- Receive command from the remote computer and send back corresponding results.
- The commands are as followings:
  - `screenshot` - Take a screenshot of the remote computer and send back an email with the screenshot attached.
  - `keylogger` - Start a keylogger on the remote computer. The command format is `keylogger <time in seconds>`. The keylogger will run for the specified time and send back an email with the keylogger log attached. If no time is specified, the keylogger will run for 10 seconds.
  - `processes` - See all the running processes on the remote computer.
  - `shutdown` - Shut down the remote computer.
  - `applications` - See all the running applications on the remote computer.

### How to use:

- Clone the repository.
- Run the `MailChecker.py` file on the computer that you want to use to receive commands.
- Send the command to mangmaytinhremotecontrol@gmail.com via your own email. The email subject will be the command as the **features section** describes. Format doesn't matter, it will all be set to lowercase.

### Requirements:

- Python 3.6 or above.
- Only run on Windows
- Install required packa.ges using `pip install -r requirements.txt`.
