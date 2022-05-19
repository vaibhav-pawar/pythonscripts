SCRIPT_STOPPED = \
    """
<!DOCTYPE html>
    <html>
        <body>
            <h3 style="color:Black;">Meraki Availability Script has stopped working</h3>
            <h4 style="color:Black;">Urgent attention is required..!!</h4>
            <h4>Next reminder notification in 1 hour if script is still failing to run. </h4>
            <br>
            <h5 style="color:Black;">Regards</h5>
            <h4 style="color:Black;">Meraki Automation</h4>
        </body>
    </html>
"""

SCRIPT_STARTED_AGAIN = \
    """
<!DOCTYPE html>
    <html>
        <body>
            <h3 style="color:Black;">Meraki Availability Script has started again working</h3>
            <h4 style="color:Black;">Meraki Availability Script has starting running again.</h4>
            <br>
            <h5 style="color:Black;">Regards</h5>
            <h4 style="color:Black;">Meraki Automation</h4>
            <h5>This is an automated mail. </h5>
        </body>
    </html>
"""

SEND_REPORT_CONTENT = \
    """
    <!DOCTYPE html>
        <html>
            <body>
                <h2 style="color:SlateGray;">Meraki Availability Report attached in this email.</h2>
                <br>
                <h5 style="color:Black;">Regards</h5>
                <h4 style="color:Black;">Meraki Automation</h4>
                <h5>This is an automated email.</h5>
            </body>
        </html>
        """

TEST_HTML_CONTENT = \
    """
<!DOCTYPE html>
    <html>
        <body>
            <h3 style="color:Black;">This is a Test Email. Please ignore.</h3>
            <br>
            <h5 style="color:Black;">Regards</h5>
            <h4 style="color:Black;">Meraki Automation</h4>
        </body>
    </html>"""