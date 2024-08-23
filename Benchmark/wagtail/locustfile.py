import lorem
import string
import random
import re
import logging
from locust import HttpUser, task, between

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class admin(HttpUser):
    fixed_count = 0
    num_editors = 0
    admin_instance = None
    blogpage_id = None
    stopped = False

    def make_new_editor(self):        
        with self.client.post(f"/admin/users/new/", data={
            "username": f"ed{admin.num_editors}",
            "password1": "editor1234",
            "password2": "editor1234",
            "email": f"e{admin.num_editors}@su.com",
            "first_name": "ed",
            "last_name": f"e{admin.num_editors}",
            "groups": [1, 2],
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        }, catch_response=True) as response:
            response.success()

        admin.num_editors += 1
        return admin.num_editors - 1

    def make_blog_index_page(self):
        with self.client.post("/admin/pages/add/blog/blogindexpage/3/", data={
            "title": "Blog",
            "slug": "blog",
            "intro": """{"blocks":[{"key":"60mvf","text":"This is our blog!","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}""",
            "comment_notifications": "on",
            "comments-TOTAL_FORMS": "0",
            "comments-INITIAL_FORMS": "0",
            "comments-MIN_NUM_FORMS": "0",
            "action-publish": "action-publish",
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        }, catch_response=True) as response:
            response.success()

    def make_home_page(self):
        with self.client.post("/admin/pages/add/home/homepage/1/", data={
            "title": "Home",
            "slug": "home",
            "comment_notifications": "on",
            "comments-TOTAL_FORMS": "0",
            "comments-INITIAL_FORMS": "0",
            "comments-MIN_NUM_FORMS": "0",
            "action-publish": "action-publish",
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        }, catch_response=True) as response:
            response.success()

    def on_start(self):
        # create csrf token
        response = self.client.get("/admin/login/")
        self.csrftoken = response.cookies['csrftoken']

        self.login()

        self.make_home_page()
        self.make_blog_index_page()

    def login(self):
        # login as admin
        self.client.post("/admin/login/", data={
            "username":"su",
            "password":"sudo1234",
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        })

    def on_stop(self):
        # get list of user Ids and delete them
        ids_to_delete = set()

        i = 1
        while True:
            with self.client.get(f"/admin/users/?p={i}", catch_response=True) as response:
                response.success()
                if response.status_code != 200:
                    break
                collected_ids = {int(x) for x in re.findall(r'data-object-id="(\d+)"', response.text) if x and int(x) > 1}
                if not collected_ids:
                    break
                ids_to_delete.update(collected_ids)
                i += 1

        # delete users
        response = self.client.post(f"/admin/bulk/auth/user/delete/?next=%2Fadmin%2Fusers%2F&" + "&".join([f"id={x}" for x in ids_to_delete]), data={
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        })
        
        # delete blog
        response = self.client.post(f"/admin/pages/{admin.get_blogpage_id()}/delete/", data={
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        })

        admin.stopped = True

    @staticmethod
    def create_editor(env):
        if not admin.admin_instance:
            admin.admin_instance = admin(env)
            admin.admin_instance.on_start()
        return admin.admin_instance.make_new_editor()

    @staticmethod
    def get_blogpage_id():
        if not admin.blogpage_id:
            with admin.admin_instance.client.get(f"/admin/pages/3/", catch_response=True) as response:
                response.success()
                admin.blogpage_id = re.findall(r'href="/admin/pages/(\d+)/add_subpage', response.text)[-1]
        return admin.blogpage_id


class editor(HttpUser):
    wait_time = between(5, 10)
    fixed_count = 1000
    weight = 1
    blogs = set() # set of blog slugs

    def on_start(self):
        # create csrf token
        response = self.client.get("/admin/login/")
        self.csrftoken = response.cookies['csrftoken']

        self.id = admin.create_editor(self.environment)
        self.logged_in = False

        self.login()

    def on_stop(self):
        if admin.stopped:
            return
        admin.admin_instance.on_stop()

    def login(self):
        # login as editor
        with self.client.post("/admin/login/", data={
            "username": f"ed{self.id}",
            "password": "editor1234",
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        }, catch_response=True) as response:
            response.success()
            
            if response.status_code != 200:
                return

            self.logged_in = True

    @task
    def view_dashboard(self):
        if not self.logged_in: return
        self.client.get(f"/admin/")

    @task
    def create_blog_post(self):
        if not self.logged_in: return

        blog_slug = f"blog{id_generator()}"
        while blog_slug in editor.blogs:
            blog_slug = f"blog{id_generator()}"

        with self.client.post(f"/admin/pages/add/blog/blogpage/{admin.get_blogpage_id()}/", data={
            "title": lorem.sentence(),
            "slug": blog_slug,
            "date": "2024-08-22",
            "intro": lorem.sentence(),
            "body": """{"blocks":[{"key":"cq08z","text":\"""" + lorem.paragraph() + """\","type":"unstyled","depth":0,"inlineStyleRanges":[],"entityRanges":[],"data":{}}],"entityMap":{}}""",
            "comment_notifications": "on",
            "comments-TOTAL_FORMS": "0",
            "comments-INITIAL_FORMS": "0",
            "comments-MIN_NUM_FORMS": "0",
            "action-publish": "action-publish",
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        }, catch_response=True) as response:
            response.success()
            editor.blogs.add(blog_slug)
