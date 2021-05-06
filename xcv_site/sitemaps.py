from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        urls = [
            'home',
            'sitemap', 'sitemap_xml', 
        ]

        return urls

    def location(self, item):
        if type(item) is tuple:
            return reverse(item[0], kwargs=item[1])
        else:
            return reverse(item)
