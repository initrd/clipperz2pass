# clipperz2pass

This script is a cleaned up version of clipperz2pass.py submitted to the [password-store](https://lists.zx2c4.com/pipermail/password-store/2015-June/001584.html) mailing list in June 2015. It also adds support to import notes from the Clipperz export.

The JSON export is embedded in the HTML file that Clipperz provides on exporting using the "HTML+JSON" option. The JSON is obfuscated and needs some work to be displayed. Open the exported HTML file in an editor, find and remove `textarea {display: none}`. Open the HTML in the browser and you should see a textarea box at the end of the page. Copy the contents to a file, say `clipperz.json`. Now run:

`$ python ./clipperz2pass.py clipperz.json`

