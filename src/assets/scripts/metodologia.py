from bs4 import BeautifulSoup

# Read the HTML file
with open('pages/metodologia/edit.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all elements with class 'content-item-body'
content_items = filter(lambda item: "url" in item['style'], soup.select('.large-pallet > div > div > div'))

# Process each content item
for item in content_items:
    image_url = tuple(filter(lambda attr: "url" in attr, item['style'].split(";")))[0].split("url(")[1].rstrip().strip()[:-1]
    icon = image_url.split("-")[-2]
    div_tag = soup.new_tag('div')
    div_tag['class'] = "header-item"
    div_tag['id'] = f"item-{icon}"
    item.replace_with(div_tag)


# Save the modified HTML to 'output.html'
with open('pages/metodologia/transition.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
