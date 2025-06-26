email = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="x-apple-disable-message-reformatting">
    <title>Your Awesome Email</title>
    <!--[if mso]>
    <noscript>
        <xml>
            <o:OfficeDocumentSettings>
                <o:AllowPNG/>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
    <style>
        table, td, div, h1, p {
            '''font-family: Arial, sans-serif;'''
        }
        @media screen and (max-width: 600px) {
            '''.full-width-mobile {
                width: 100% !important;
                display: block !important;
            }
            .padding-mobile {
                padding: 20px !important;
            }
            .img-max-width {
                max-width: 100% !important;
                height: auto !important;
            }
            .text-center-mobile {
                text-align: center !important;
            }'''
        }
    </style>
</head>
<body style="margin:0;padding:0;word-spacing:normal;background-color:#f0f0f0;">
    <div role="article" aria-roledescription="email" lang="en" style="text-size-adjust:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;background-color:#f0f0f0;">
        <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background-color:#f0f0f0;">
            <tr>
                <td align="center" style="padding:0;">
                    <table role="presentation" style="width:600px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;background-color:#ffffff;" class="full-width-mobile">
                        <!-- Header Section -->
                        <tr>
                            <td style="padding:20px;background-color:#3b82f6;text-align:center;">
                                <h1 style="margin:0;font-size:24px;line-height:28px;font-weight:bold;color:#ffffff;">
                                    Your Brand Name
                                </h1>
                            </td>
                        </tr>
                        <!-- Main Content Section -->
                        <tr>
                            <td style="padding:40px 30px 40px 30px;">
                                <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                                    <tr>
                                        <td style="padding:0 0 30px 0;color:#153643;">
                                            <h2 style="font-size:24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Hello, {{name}} {{surname}}!</h2>
                                            <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">
                                                Your account has been created, and you password is <b><i>{{password}}</i></b>. This is a sample email template. You can use this structure for various purposes like newsletters, notifications, or transactional emails.
                                                We've kept it clean and simple for easy customization.
                                            </p>
                                            <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">
                                                Here's some more content to showcase how paragraphs look. Feel free to add more details, images, or links as needed.
                                            </p>
                                            <p style="margin:0;">
                                                <a href="https://www.example.com" style="background-color:#3b82f6;color:#ffffff;text-decoration:none;padding:10px 20px;border-radius:5px;display:inline-block;font-weight:bold;">Call to Action Button</a>
                                            </p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding:0;">
                                            <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                                                <tr>
                                                    <td style="width:260px;padding:0;vertical-align:top;" class="full-width-mobile">
                                                        <p style="margin:0 0 25px 0;"><img src="https://static.vecteezy.com/system/resources/previews/011/063/921/non_2x/example-button-speech-bubble-example-colorful-web-banner-illustration-vector.jpg" alt="Placeholder Image 1" width="260" style="height:auto;display:block;" class="img-max-width"/></p>
                                                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;color:#153643;">
                                                            This is a caption for the first image. Describe what's happening or provide more context.
                                                        </p>
                                                    </td>
                                                    <td style="width:20px;padding:0;font-size:0;line-height:0;">&nbsp;</td>
                                                    <td style="width:260px;padding:0;vertical-align:top;" class="full-width-mobile">
                                                        <p style="margin:0 0 25px 0;"><img src="https://static.vecteezy.com/system/resources/previews/011/063/921/non_2x/example-button-speech-bubble-example-colorful-web-banner-illustration-vector.jpg" alt="Placeholder Image 2" width="260" style="height:auto;display:block;" class="img-max-width"/></p>
                                                        <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;color:#153643;">
                                                            And here's a caption for the second image, adding more visual storytelling to your email.
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <!-- Footer Section -->
                        <tr>
                            <td style="padding:30px;background-color:#eeeeee;text-align:center;">
                                <p style="margin:0;font-size:14px;line-height:20px;font-family:Arial,sans-serif;color:#666666;">
                                    &copy; 2025 Your Brand Name. All rights reserved.<br/>
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </div>
</body>
</html>
"""