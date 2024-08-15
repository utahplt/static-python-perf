import time
import re
from requests.auth import HTTPBasicAuth
import logging
from locust import HttpUser, task, between


class admin(HttpUser):
    wait_time = between(1, 5)
    MAX_USERS_CREATED = 1000
    fixed_count = 10 # number of admin users to create
    num_editors = 0

    @task
    def view_dashboard(self):
        self.client.get(f"/admin/")

    @task(3)
    def make_new_editor(self):
        if admin.num_editors >= admin.MAX_USERS_CREATED:
            return
        
        with self.client.post(f"/admin/users/new/", data={
            "username": f"ed{admin.num_editors}",
            "password1": "editor1234",
            "password2": "editor1234",
            "email": f"e{admin.num_editors}@su.com",
            "first_name": "ed",
            "last_name": f"e{admin.num_editors}",
            "groups": 2,
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        }, catch_response=True) as response:
            response.success()

        admin.num_editors += 1
        editor.fixed_count += 1

    def on_start(self):
        # create csrf token and jwt     
        response = self.client.get("/admin/login/")
        self.csrftoken = response.cookies['csrftoken']

        self.login()

        # number of users created
        admin.num_editors = 0

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
                ids_to_delete.update({int(x) for x in re.findall(r'data-object-id="(\d+)"', response.text) if int(x) > 1})
                i += 1

        # delete users
        response = self.client.post(f"/admin/bulk/auth/user/delete/?next=%2Fadmin%2Fusers%2F&" + "&".join([f"id={x}" for x in ids_to_delete]), data={
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        })


class editor(HttpUser):
    wait_time = between(1, 5)
    editors_created = 0
    fixed_count = 0

    def on_start(self):        
        # create csrf token and jwt     
        response = self.client.get("/admin/login/")
        self.csrftoken = response.cookies['csrftoken']

        self.login()

    def login(self):
        # login as editor
        logging.info(f"Logging in as editor ed{editor.editors_created}")
        self.client.post("/admin/login/", data={
            "username": f"ed{editor.editors_created}",
            "password": "editor1234",
            "csrfmiddlewaretoken": self.csrftoken,
        }, headers={
            'X-CSRFToken': self.csrftoken,
        }, cookies={
            "csrftoken": self.csrftoken,
        })
        
        editor.editors_created += 1
    
    @task
    def view_dashboard(self):
        pass
