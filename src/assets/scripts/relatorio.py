from bs4 import BeautifulSoup

# Read the HTML file
with open('test.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all elements with class 'content-item-body'
content_items = soup.find_all(class_='item-content')

# Process each content item
for item in content_items:
    link = item.find('a')
    if link:
        # Find the first 'img' tag inside the 'a' tag
        img = link.find('img')
        if img:
            # Add style to the 'img' tag
            img['style'] = img['style'].replace('calc(50% - 32px)', '32px')
    # Check if the text 'Boletins' is not present
        if 'Boletins' not in item.get_text():
            div_tag = soup.new_tag('div')
            div_tag.extend(link.contents)
            link.replace_with(div_tag)

# Save the modified HTML to 'output.html'
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
