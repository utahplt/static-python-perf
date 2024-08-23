import lorem
import string
import random
import re
import logging
from locust import HttpUser, task, between
from requests.adapters import HTTPAdapter

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class admin(HttpUser):
    fixed_count = 0
    num_editors = 0
    admin_instance = None
    blogpage_id = None
    homepage_id = None

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
        with self.client.post(f"/admin/pages/add/blog/blogindexpage/{admin.get_homepage_id()}/", data={
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

    def on_start(self):
        # create csrf token
        response = self.client.get("/admin/login/")
        self.csrftoken = response.cookies['csrftoken']

        self.login()
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

    def delete_editors(self):
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

    def delete_blog(self):
        self.client.post(f"/admin/pages/{admin.get_blogpage_id()}/delete/", data={
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        })

    @staticmethod
    def create_editor(env):
        if not admin.admin_instance:
            admin.admin_instance = admin(env)
            admin.admin_instance.on_start()
        return admin.admin_instance.make_new_editor()

    @staticmethod
    def get_blogpage_id():
        if not admin.blogpage_id:
            with admin.admin_instance.client.get(f"/admin/pages/{admin.get_homepage_id()}/", catch_response=True) as response:
                response.success()
                admin.blogpage_id = re.findall(r'/admin/pages/(\d+)/add_subpage', response.text)[-1]
        return admin.blogpage_id

    @staticmethod
    def get_homepage_id():
        if not admin.homepage_id:
            with admin.admin_instance.client.get(f"/admin/pages/", catch_response=True) as response:
                response.success()
                admin.homepage_id = re.findall(r'/admin/pages/(\d+)/add_subpage', response.text)[-1]
        return admin.homepage_id


class editor(HttpUser):
    wait_time = between(5, 10)
    fixed_count = 1000
    weight = 10
    blogs = set() # set of blog slugs
    num_instances = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('http://', HTTPAdapter(pool_maxsize=editor.fixed_count))

    def on_start(self):
        # create csrf token
        response = self.client.get("/admin/login/")
        self.csrftoken = response.cookies['csrftoken']

        self.id = admin.create_editor(self.environment)
        self.logged_in = False

        self.login()
        editor.num_instances += 1

    def on_stop(self):
        editor.num_instances -= 1
        if editor.num_instances == 0:
            admin.admin_instance.delete_editors()

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


class reader(HttpUser):
    wait_time = between(1, 3)
    fixed_count = 10000
    weight = 1
    num_instances = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('http://', HTTPAdapter(pool_maxsize=reader.fixed_count))

    def on_start(self):
        reader.num_instances += 1

    def on_stop(self):
        reader.num_instances -= 1
        if reader.num_instances == 0:
            admin.admin_instance.delete_blog()

    @task
    def view_blog_index(self):
        if not admin.blogpage_id: return
        with self.client.get("/blog/", catch_response=True) as response:
            response.success()

    @task
    def view_blog_post(self):
        if not editor.blogs: return
        with self.client.get(f"/blog/{random.choice(list(editor.blogs))}/", catch_response=True) as response:
            response.success()
