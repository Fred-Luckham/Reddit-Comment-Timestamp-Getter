from flask import Flask
from flask import request, escape
from urllib.request import urlopen
import re
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    url = request.args.get("url", "")
    if url:
        comment_ts = reddit_comment_ts(url)
    else:
        comment_ts = ""
    return (
        """<form action="" method="get">
                Comment URL: <input type="text" name="url">
                <input type="submit" value="Get timestamp">
              </form>"""
        + "Comment Timestamp: "
        + comment_ts
    )

@app.route("/<url>")
def reddit_comment_ts(url):
    try:
        # Append .json
        url = url + ".json"

        # Get page response and read
        response = urlopen(url)
        page_data = response.read().decode('utf-8')

        # Extract unix time stamp
        unix_ts = re.search(r'("created_utc":)(.+?),', page_data)
        ts = unix_ts.group(2)

        # Prepare for convertion
        ts.strip()
        ts = (int(float(ts)))

        # Print timestamp
        converted_ts = (datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S'))
        return converted_ts
    except:
        return "HTTP timeout or Input Error"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)