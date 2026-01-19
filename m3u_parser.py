def generate_m3u_with_custom_names(renamed_categories_dict):
    """
    Generate M3U content for a dict {new_category: [channel_lines]} where channel_lines need their group-title updated.
    """
    import re
    output = ['#EXTM3U']
    group_title_re = re.compile(r'(group-title=")([^"]+)(")')
    for new_cat, channels in renamed_categories_dict.items():
        for channel in channels:
            extinf = channel[0]
            url = channel[1] if len(channel) > 1 else ''
            # Replace group-title with new_cat
            if 'group-title' in extinf:
                extinf = group_title_re.sub(r'\1' + new_cat + r'\3', extinf)
            output.append(extinf)
            output.append(url)
    return '\n'.join(output)
def parse_m3u(m3u_content):
    """
    Parses M3U content and returns a dict: {category: [channel_lines]}
    """
    import re
    from collections import defaultdict
    
    category_pattern = re.compile(r'group-title="([^"]+)"')
    lines = m3u_content.splitlines()
    categories = defaultdict(list)
    current_category = "Uncategorized"
    buffer = []
    for line in lines:
        if line.startswith("#EXTINF"):
            match = category_pattern.search(line)
            if match:
                current_category = match.group(1)
            else:
                current_category = "Uncategorized"
            buffer = [line]
        elif line.startswith("http"):
            buffer.append(line)
            categories[current_category].append(tuple(buffer))
            buffer = []
    return dict(categories)

def generate_m3u(selected_categories, categories_dict):
    """
    Generate M3U content for selected categories from the parsed dict.
    """
    output = ['#EXTM3U']
    for cat in selected_categories:
        for channel in categories_dict.get(cat, []):
            output.extend(channel)
    return '\n'.join(output)
