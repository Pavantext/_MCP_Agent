import requests

def get_unread_emails(access_token, top=5):
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages?$filter=isRead eq false&$top=" + str(top)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        emails = response.json().get("value", [])
        return [
            {
                "subject": email.get("subject"),
                "from": email.get("from", {}).get("emailAddress", {}).get("name"),
                "body_preview": email.get("bodyPreview")
            }
            for email in emails
        ]
    else:
        raise Exception("Failed to fetch emails")
