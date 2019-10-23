from flaskblog.database import session
from flaskblog.models import Post, User
from sqlalchemy_paginator import Paginator

user = session.query(User).filter_by(username="Rachel").first()
query = session.query(Post).filter_by(author=user).order_by(Post.date_posted.desc())
posts = Paginator(query, 2)
posts_page = posts.page(1)

for post in  posts_page.object_list:
    print post.author.username
# print query.author.username
# print query.count()
# print dir(query)
# print dir(posts)
# print "\n"
# print dir(post_page)
# print post_page.number
# print posts.page(posts.pages_range[0]).has_next()
# print posts.page(posts.pages_range[-1]).has_next()

# for page_num in posts.pages_range:
#     print page_num
# for page_num in posts.pages_range:
#     print page_num
# print pages
# for page in pages:
#     post_page = posts.page(page)
#     print post_page
#     if post_page.object_list:
#         for post in post_page.object_list:
#             print post