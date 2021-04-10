class BlogNavigation:
    def contents_parsed(self, context):
        for lang in ('de', 'en', ):
            blog_posts = context.contents.filter(
                type='blog',
                lang=lang,
            ).order_by(
                '-date',
            )

            blog_posts_len = len(blog_posts)

            for index, blog_post in enumerate(blog_posts):
                if index > 0:
                    blog_post['next_blog_post'] = blog_posts[index-1]['url']

                if index < blog_posts_len - 1:
                    blog_post['prev_blog_post'] = blog_posts[index+1]['url']
