# -*- coding: utf-8 -*-
"""A Qt Widget for login ArtHub."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import requests
import os
import re

from arthub_api import APIResponse

# Import local modules
from arthub_login_widgets_sso.filesystem import get_client_exe_path
from arthub_login_widgets_sso.filesystem import get_token_from_file
from arthub_login_widgets_sso.filesystem import run_exe_sync
from arthub_login_widgets_sso.constants import SERVICE_CONFIGS
from arthub_login_widgets_sso.exception import ErrorClientNotExists


def load_style_sheet(style_file):
    with open(style_file, "r") as css_file:
        css_string = css_file.read().strip("\n")
        data = os.path.expandvars(css_string)
        return data


class LoginBackend(object):
    def __init__(
            self,
            service_type="test",
            service_id=11000,
            exe_path=None
    ):
        r"""
        service_type(str): "test" | "mainland" | "overseas"
        """

        self.service_type = service_type
        self.service_id = service_id
        self._last_token = None
        self._account_detail = None
        self._exe_path = get_client_exe_path()
        self._did_logged_out = False
        if exe_path:
            self._exe_path = exe_path
        self.check_exe()

    @property
    def api_host(self):
        if self.service_type in SERVICE_CONFIGS:
            return SERVICE_CONFIGS[self.service_type]["api"]
        else:
            raise ValueError("Invalid service_type: {}".format(self.service_type))

    @property
    def page_host(self):
        if self.service_type in SERVICE_CONFIGS:
            return SERVICE_CONFIGS[self.service_type]["page"]
        else:
            raise ValueError("Invalid service_type: {}".format(self.service_type))

    @property
    def exe_path(self):
        return self._exe_path

    @property
    def token(self):
        return self._last_token

    @property
    def account_detail(self):
        return self._account_detail

    @property
    def token_cache_file_path(self):
        appdata_path = os.getenv('APPDATA')
        return os.path.join(appdata_path, 'arthub-tools', self.api_host, str(self.service_id), "token_cache.yml")

    def base_url(self):
        return "https://%s" % self.api_host

    def check_exe(self):
        if not os.path.exists(self.exe_path):
            raise ErrorClientNotExists()

    def get_token_from_cache(self):
        return get_token_from_file(self.token_cache_file_path)

    def clear_token_cache(self):
        file_path = self.token_cache_file_path
        if os.path.exists(file_path):
            os.remove(file_path)

    def is_login(self):
        if self._check_local_token_cache():
            return True
        return False

    def popup_login(self, window_x=None, window_y=None):
        args = self.get_args(window_x=window_x, window_y=window_y)
        r = self._call_exe(args)
        if not r[0]:
            return False
        return bool(r[1])

    def get_args(self, window_x=None, window_y=None):
        args = [
            "--service-id={}".format(self.service_id),
            "--service-page-host={}".format(self.page_host),
            "--service-api-host={}".format(self.api_host),
        ]
        if (window_x is not None) and (window_y is not None):
            args.append("--window-center-x={}".format(window_x))
            args.append("--window-center-y={}".format(window_y))
        return args

    def _call_exe(self, args):
        exit_code, stdout = run_exe_sync(self._exe_path, args)
        match = re.search(r'\[GetArtHubToken\]\s*([^\n]+)', stdout)
        if not match:
            return True, None
        if not self._check_local_token_cache():
            return True, None
        return True, self.token

    def logout(self):
        self.clear_token_cache()
        self._on_logout()

    def _on_logout(self):
        self._last_token = None
        self._account_detail = None
        self._did_logged_out = True

    def _check_local_token_cache(self):
        token_data = self.get_token_from_cache()
        if not token_data:
            return False
        # token_data: {"api_token": "xx"}
        token = token_data.get("api_token")
        if not token:
            return False
        return self.check_token(token)

    @staticmethod
    def make_api_request(url, token, data=None, method='POST'):
        # set token to headers
        headers = {
            "content_type": "application/json",
            "arthub-main-site-token": token,
        }
        # send request
        try:
            res = requests.request(method=method, url=url, headers=headers, json=data, timeout=15)
        except Exception as e:
            response = APIResponse(None, True)
            response.exception = e
            return response

        return APIResponse(res)

    def check_token(self, token):
        url = "%s/cas/cas/openapi/v1/core/get-login-user-account-detail" % self.base_url()
        res = self.make_api_request(url, token)
        if not res.is_succeeded():
            return False
        self._account_detail = res.result[0]
        self._last_token = token
        return True

    def get_service_ticket(self):
        token = self.token
        if not token:
            raise RuntimeError("User is not logged in.")
        url = "%s/cas/cas/openapi/v1/core/get-service-ticket" % self.base_url()
        res = self.make_api_request(url, token, data={"service_id": str(self.service_id)})
        if not res.is_succeeded():
            raise RuntimeError(res.error_message())
        return res.result[0].get("service_ticket")
