from usp.tree import sitemap_tree_for_homepage

tree = sitemap_tree_for_homepage('https://auto.drom.ru')

with open('res', 'w') as f:
    for elem in tree.all_pages():
        f.write(f'{elem} + \n')
