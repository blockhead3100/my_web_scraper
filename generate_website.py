from bs4 import BeautifulSoup
import os
import argparse

def create_website(template_file, output_file, user_data):
    """
    Creates a website from a template HTML file, replacing placeholders with user-provided data.

    Args:
        template_file (str): Path to the template HTML file.
        output_file (str): Path to save the generated HTML file.
        user_data (dict): Dictionary containing the data to replace the placeholders.
    """

    with open(template_file, "r") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Replace content placeholders
    placeholders = {
        "home-text": "home",
        "about-text": "about",
        "services-text": "services",
        "pro-packs-text": "pro-packs",
        "promotions-text": "promotions",
        "EMAILJS_PUBLIC_KEY": "emailjs_public_key",
        "EMAILJS_SERVICE_ID": "emailjs_service_id",
        "EMAILJS_TEMPLATE_ID": "emailjs_template_id"
    }

    for placeholder_id, data_key in placeholders.items():
        element = soup.find(id=placeholder_id)
        if element:
            element.string = user_data.get(data_key, element.string)  # Use get() with default

    with open(output_file, "w") as f:
        f.write(str(soup))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Website Generator.")
    parser.add_argument("output_file", help="Name of the output HTML file.")
    args = parser.parse_args()

    user_data = {}
    user_data["home"] = input("Enter home section text: ")
    user_data["about"] = input("Enter about section text: ")
    user_data["services"] = input("Enter services section text: ")
    user_data["pro-packs"] = input("Enter pro-packs section text: ")
    user_data["promotions"] = input("Enter promotions section text: ")
    user_data["emailjs_public_key"] = input("Enter EmailJS Public Key: ")
    user_data["emailjs_service_id"] = input("Enter EmailJS Service ID: ")
    user_data["emailjs_template_id"] = input("Enter EmailJS Template ID: ")

    create_website("template.html", args.output_file, user_data)

    print(f"Website created: {args.output_file}")
