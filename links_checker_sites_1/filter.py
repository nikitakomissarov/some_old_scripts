
def filtering(filtered_links, links):
    for i in links:
        if i not in filtered_links:
            filtered_links.append(i)
    return filtered_links