

class MessageTemplates:
    
    @staticmethod
    def inviteMail(name:str, role:str, meetingTime:str, meetingLink:str, meetingDate:str):
        return f"""
            <html>
              <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6; background-color: #f9f9f9; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: #fff; border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                
                <!-- Logo -->
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="http://res.cloudinary.com/drxzba3j8/image/upload/v1759219807/du-logo-a.png" alt="DreemUni Logo" style="width: 150px;">
                </div>
                
                <!-- Greeting -->
                <h2 style="color: #002244; font-weight: 600;">Hello {name},</h2>
                
                <p>
                    🎉Thank you for applying for the <b>{role} internship</b> programme with DreemUni.
                    We'd love to meet you for a quick 10-15min online meeting to know more about you.
                </p>
                
                <!-- Details Card -->
                <div style="background: #f0f4f8; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 5px solid #002244;">
                    <p><b>📅 Date:</b> {meetingDate}</p>
                    <p><b>⌚ Time:</b> {meetingTime}</p>
                    
                    <a href="{meetingLink}" style="color: #fff; background: #8f75fd; padding: 10px 10px; border-radius: 6px; text-decoration: none;     ">
                        Click to join
                    </a>
                </div>
               
                <p>Please reply <b>“Confirmed”</b> to this email before 9am tomorrow to keep your spot.</p>

                <!-- Footer -->
                <div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 10px; font-size: 14px; color: #777;">
                    Warm regards,<br>
                    <b style="color: #002244;">The DreemUni Team</b>
                </div>
                </div>
            </body>
            </html>
            """

    @staticmethod
    def smsNotfConfirmation(institution: str = "admission notifications"):
        return f'Request to received notifications for {institution} received. Make payment to complete your transaction'
    
    @staticmethod
    def checkerBuy(serialNumber: str, pin:str, level:str="WASSCE", url:str="https://eresults.waecgh.org"):
        return f"Your {level} voucher is ready. \n\nSerial Number:\n{serialNumber}\n\nPIN:\n{pin}\n\nTo start click here: {url}"


    @staticmethod
    def smsNotfSuccess(institution: str):
        return f'Your {institution} subscription is active. Notfications will start soon. Thanks for choosing DreemUni.'
    
    @staticmethod
    def smsPaid():
        return f'Payment successful. Thanks for choosing DreemUni.'
    
    @staticmethod
    def creditTopUpSucess():
        return f'Credit Topup successful. Thanks for choosing DreemUni.'

    @staticmethod
    def smsOTP(name, code):
        return f'''Enter {code} as your verification code.\nThis code expires in 1hour'''

    @staticmethod
    def emailNotfConfirmation(username: str, institution: str) -> str:
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>DreemUni Subscription Confirmation</title>
            <style>
                body {{
                font-family: 'Poppins', sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
                }}
                .email-container {{
                max-width: 600px;
                margin: auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                }}
                .header {{
                text-align: center;
                padding-bottom: 10px;
                }}
                .header img {{
                width: 100px;
                }}
                .title {{
                color: #002244;
                font-size: 22px;
                font-weight: bold;
                }}
                .content {{
                font-size: 16px;
                color: #333333;
                line-height: 1.6;
                padding: 10px 0;
                }}
                .footer {{
                font-size: 14px;
                color: #777777;
                text-align: center;
                margin-top: 30px;
                }}
                .accent {{
                color: #8f75fd;
                font-weight: 600;
                }}
            </style>
            </head>
            <body>
            <div class="email-container">
                <div class="title">Subscription Request🔔</div>
                <div class="content">
                    Hello <strong>{username}</strong>,<br /><br />
                    Request to get timed updates from  <span class="accent">{institution}</span> has been successfully received.<br />
                    Please complete your payment to confirm.<br /><br />
                    Thank you for choosing DreemUni. </div>
                <div class="footer">
                &copy; 2025 DreemUni<br />
                📍 Accra, Ghana &nbsp; | &nbsp;
                <a href="mailto:app@dreemuni.com" style="color:#8f75fd;">app@dreemuni.com</a><br />
                <a href="https://dreemuni.com" style="color:#002244;">Visit Website</a>
                </div>
            </div>
            </body>
            </html>
            """
    
    @staticmethod
    def emailNotfSuccess(institution: str = "Universities") -> str:
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Payment Successful</title>
                <style>
                    body {{
                        font-family: 'Poppins', sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .email-container {{
                        max-width: 600px;
                        margin: auto;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        border: 1px solid #ddd;
                    }}
                    .title {{
                        font-size: 20px;
                        font-weight: bold;
                        color: #8f75fd;
                        margin-bottom: 10px;
                    }}
                    .content {{
                        font-size: 15px;
                        color: #333;
                        line-height: 1.6;
                    }}
                    .accent {{
                        color: #8f75fd;
                        font-weight: 600;
                    }}
                    .footer {{
                        font-size: 13px;
                        text-align: center;
                        color: #777;
                        margin-top: 30px;
                    }}
                    a {{
                        color: #8f75fd;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="title">Subscription confirmed✅</div>
                    <div class="content">
                        Your email has been added to a list of destinations to receive timed notifications for  <span class="accent">{institution}</span><br />
                        You will now receive timely notifications directly to your inbox or device.<br /><br />
                        Thank you for choosing DreemUni🎓
                    </div>
                    <div class="footer">
                        &copy; 2025 DreemUni<br />
                        📍 Accra, Ghana · 
                        <a href="mailto:contact@dreemuni.com">contact@dreemuni.com</a> · 
                        <a href="https://dreemuni.com">dreemuni.com</a>
                    </div>
                </div>
            </body>
            </html>
        """

    @staticmethod
    def emailOTP(code):
        return f"""
            <!DOCTYPE html>
            <head>
                <meta charset="UTF-8">
                <title>Your OTP Code</title>
            </head>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 0; margin: 0;">
                <table align="center" width="100%" style="max-width: 600px; background-color: #ffffff; margin-top: 40px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
                    <!-- Header with logo -->
                    
                    <!-- Welcome Banner -->
                    <tr>
                        <td style="background-color: #002244; padding: 20px; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                            <h2 style="color: white; margin: 0;">Welcome to DreemUni!</h2>
                        </td>
                    </tr>

                    <!-- Additional content would go here -->

                    <td style="padding: 30px;">
                        <p style="font-size: 16px; color: #333;">Use the OTP below to complete your account setup:</p>

                        <div style="margin: 0px 0; text-align: center;">
                        <span style="display: inline-block; background-color: #8f75fd; color: white; font-size: 24px; font-weight: bold; padding: 14px 30px; border-radius: 6px; letter-spacing: 4px;">
                            {code}
                        </span>
                        </div>

                        <p style="font-size: 14px; color: #666;">This code is valid for 1Hour. Do not share it with anyone.</p>

                        <p style="font-size: 14px; color: #666;">If you didn't request this code, please ignore this message.</p>

                        <p style="font-size: 14px; color: #999; margin-top: 40px;">— The DreemUni Team</p>
                    </td>
                    </tr>
                </table>
                </body>
                </html>

        """

