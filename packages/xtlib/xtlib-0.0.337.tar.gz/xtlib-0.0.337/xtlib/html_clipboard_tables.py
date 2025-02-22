# html_clipboard_tables.py: class to create and copy HTML tables to the clipboard
import base64
from xtlib.helpers import clipboard
from xtlib import console

html_prefix = html = '''Version:1.0
StartHTML:0000000106
EndHTML:0009992215
StartFragment:0000000527
EndFragment:0000002175
<html>

<style>
table { direction:ltr;border-collapse:collapse;border-style:solid;border-color:#A3A3A3;border-width:1pt}
td {border-style:solid;border-color:#A3A3A3;border-width:1pt; vertical-align:top;width:.6673in;padding:4pt 4pt 4pt 4pt; word-wrap: break-word; max-width: 80px;}
p {margin:0in;font-family:"Aptos Narrow";font-size:11.0pt;color:black; word-wrap: break-word; max-width: 80px}
</style>

<body lang=en-US style='font-family:Calibri;font-size:11.0pt'>
<!--StartFragment-->
'''

html_suffix = '''<!--EndFragment-->
</body>
</html>
'''

html_test = '''<table border=1 cellpadding=0 cellspacing=0 valign=top style='' title="" summary=""> 
 <tr>
  <td> <p class=p_bold>a</p> </td>
  <td> <p class=p_bold>b</p> </td>
  <td> <p class=p_bold>dog</p> </td>
 </tr>
 <tr>
  <td> <p>d</p> </td>
  <td> <p>e</p> </td>
  <td> <p>ferret</p> </td>  
 </tr>
</table>'''

class HtmlClipboardTables:
    def __init__(self):
        self.items = []

    def add_table(self, headers, rows, bold_headers=True, title=None):

        html = "<div style='direction:ltr'>\n"

        if title:
            html += "<p style='font-weight: bold'>" + title + "</p>\n"

        html += "<table border=1 cellpadding=0 cellspacing=0 valign=top style='' title='' summary=''>\n"

        # add header row
        html += "<tr>"
        for header in headers:
            if bold_headers:
                html += '<td> <p style="font-weight: bold">' + header + '</p> </td>'
            else:
                html += '<td> <p>' + header + '</p> </td>'
        html += "</tr>\n"

        for row in rows:
            # add regular row
            html += "<tr>"
            for value in row:
                html += '<td> <p>' + str(value) + '</p> </td>'
            html += "</tr>\n"

        html += "</table></div>\n"

        self.items.append(html)

    def add_image(self, fn_img, title=None, width=800):
        with open(fn_img, "rb") as image_file:
            b64_str = base64.b64encode(image_file.read()).decode("utf-8")

        html = "<div>\n"
        if title:
            html += "<p style='font-weight: bold'>" + title + "</p>\n"

        html += f'<img width="{width}" src="data:image/jpeg;base64,{b64_str}" />'
        html += "</div>\n"

        self.items.append(html)

    def copy_to_clipboard(self):
        with clipboard.Clipboard() as cb:
            html = html_prefix
            html += "<br/><br/>\n".join(self.items)
            html += html_suffix

            # cb.set_contents("HTML FORMAT", html)
            bytes = html.encode("utf-8")

            # 49418 is the clipboard format for HTML (for OneNote, at least)
            cb.set_contents("HTML Format", bytes)
            #cb.set_contents(1, bytes)            # for debugging in Notepad

        console.print("{:,} HTML item(s) copied to clipboard".format(len(self.items)))    
        self.tables = []


if __name__ == "__main__":          
    from xtlib.helpers import clipboard 

    headers = ["Name", "Age", "Sex"]
    rows = [
        ["John", "25", "Male"],
        ["Mary", "22", "Female"],
        ["Bill", "68", "Male"],
        ["Jane", "30", "Female"]]
    
    hct = HtmlClipboardTables()
    hct.add_table(headers, rows)
    hct.add_image("d:/photos/lucas_wrong_glasses.jpeg", title="Lucas with wrong glasses")
    hct.add_table(headers, rows)
    hct.copy_to_clipboard()


