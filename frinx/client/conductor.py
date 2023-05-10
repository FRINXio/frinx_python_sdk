#
#  Copyright 2017 Netflix, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import json
import socket

import requests

hostname = socket.gethostname()


class BaseClient:
    print_url = False
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def __init__(self, base_url, base_resource, headers=None):
        self.base_url = base_url
        self.base_resource = base_resource
        if headers is not None:
            self.headers = self.merge_two_dicts(self.headers, headers)

    def get(self, res_path, query_params=None):
        the_url = f'{self.base_url}/{res_path}'
        resp = requests.get(the_url, params=query_params, headers=self.headers)
        self.__check_for_success(resp)
        if resp.content == b'':
            return None
        else:
            return resp.json()

    def post(self, res_path, query_params, body, headers=None):
        the_url = f'{self.base_url}/{res_path}'
        the_header = self.headers
        if headers is not None:
            the_header = self.merge_two_dicts(self.headers, headers)
        if body is not None:
            json_body = json.dumps(body, ensure_ascii=False).encode('utf8')
            resp = requests.post(the_url, params=query_params, data=json_body, headers=the_header)
        else:
            resp = requests.post(the_url, params=query_params, headers=the_header)

        self.__check_for_success(resp)
        return self.__return(resp, the_header)

    def put(self, res_path, query_params=None, body=None, headers=None):
        the_url = f'{self.base_url}/{res_path}'
        the_header = self.headers
        if headers is not None:
            the_header = self.merge_two_dicts(self.headers, headers)

        if body is not None:
            json_body = json.dumps(body, ensure_ascii=False).encode('utf8')
            resp = requests.put(the_url, params=query_params, data=json_body, headers=the_header)
        else:
            resp = requests.put(the_url, params=query_params, headers=the_header)

        self.__print(resp)
        self.__check_for_success(resp)

    def delete(self, res_path, query_params):
        the_url = f'{self.base_url}/{res_path}'
        resp = requests.delete(the_url, params=query_params, headers=self.headers)
        self.__print(resp)
        self.__check_for_success(resp)

    def make_url(self, urlformat=None, *argv):
        url = self.base_resource + '/'
        if urlformat:
            url += urlformat.format(*argv)
        return url

    def make_params(self, **kwargs):
        return dict((k, v) for k, v in kwargs.items() if v is not None) or None

    def merge_two_dicts(self, x, y):
        z = x.copy()
        z.update(y)
        return z

    def __print(self, resp):
        if self.print_url:
            print(resp.url)

    @staticmethod
    def __return(resp, header):
        retval = ''
        if len(resp.text) > 0:
            if header['Accept'] == 'text/plain':
                retval = resp.text
            elif header['Accept'] == 'application/json':
                retval = resp.json()
            else:
                retval = resp.text
        return retval

    @staticmethod
    def __check_for_success(resp):
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            print('ERROR: ' + resp.text)
            raise


class MetadataClient(BaseClient):
    BASE_RESOURCE = 'metadata'

    def __init__(self, base_url, headers=None):
        BaseClient.__init__(self, base_url, self.BASE_RESOURCE, headers)

    def get_workflow_def(self, wf_name, version=None):
        url = self.make_url('workflow/{}', wf_name)
        return self.get(url, self.make_params(version=version))

    def create_workflow_def(self, wfd_obj):
        url = self.make_url('workflow')
        return self.post(url, None, wfd_obj)

    def update_workflow_defs(self, list_of_wfd_obj):
        url = self.make_url('workflow')
        self.put(url, None, list_of_wfd_obj)

    def get_all_workflow_defs(self):
        url = self.make_url('workflow')
        return self.get(url)

    def unregister_workflow_def(self, wf_name, version):
        url = self.make_url(f'workflow/{wf_name}/{version}')
        self.delete(url, None)

    def get_task_def(self, td_name):
        url = self.make_url('taskdefs/{}', td_name)
        return self.get(url)

    def register_task_defs(self, list_of_task_def_obj: dict):
        url = self.make_url('taskdefs')
        return self.post(url, None, list_of_task_def_obj)

    def update_task_def(self, task_def_obj):
        url = self.make_url('taskdefs')
        self.put(url, None, task_def_obj)

    def unregister_task_def(self, td_name, reason=None):
        url = self.make_url('taskdefs/{}', td_name)
        self.delete(url, self.make_params(reason=reason))

    def get_all_task_defs(self):
        url = self.make_url('taskdefs')
        return self.get(url)


class TaskClient(BaseClient):
    BASE_RESOURCE = 'tasks'
    EXTERNAL_INPUT_KEY = 'externalInputPayloadStoragePath'

    def __init__(self, base_url, headers=None):
        BaseClient.__init__(self, base_url, self.BASE_RESOURCE, headers)

    def get_task(self, task_id):
        url = self.make_url('{}', task_id)
        return self.get(url)

    def update_task(self, task_obj):
        url = self.make_url('')
        headers = {'Accept': 'text/plain'}
        self.post(url, None, task_obj, headers)

    def poll_for_task(self, task_type, worker_id, domain=None):
        url = self.make_url('poll/{}', task_type)
        params = {'workerid': worker_id}
        if domain is not None:
            params['domain'] = domain

        try:
            return self.get(url, params)
        except Exception as err:
            print('Error while polling ' + str(err))
            return None

    def poll_for_batch(self, task_type, count, timeout, worker_id, domain=None):
        url = self.make_url('poll/batch/{}', task_type)
        params = {'workerid': worker_id, 'count': count, 'timeout': timeout}

        if domain is not None:
            params['domain'] = domain

        try:
            return self.get(url, params)
        except Exception as err:
            print('Error while polling ' + str(err))
            return None

    def get_tasks_in_queue(self, task_name):
        url = self.make_url('queue/{}', task_name)
        return self.get(url)

    def remove_task_from_queue(self, task_id, reason=None):
        url = self.make_url('queue/{}', task_id)
        params = {'reason': reason}
        self.delete(url, params)

    def get_task_queue_sizes(self, list_of_task_name):
        url = self.make_url('queue/sizes')
        return self.post(url, None, list_of_task_name)

    def get_task_input_external_payload_location(self, path):
        url = self.make_url('externalstoragelocation')
        params = {'path': path, 'operation': 'READ', 'payloadType': 'TASK_INPUT'}
        return self.get(url, params)


class WorkflowClient(BaseClient):
    BASE_RESOURCE = 'workflow'

    def __init__(self, base_url, headers=None):
        BaseClient.__init__(self, base_url, self.BASE_RESOURCE, headers)

    def get_workflow(self, wf_id, include_tasks=True):
        url = self.make_url('{}', wf_id)
        params = {'includeTasks': include_tasks}
        return self.get(url, params)

    def get_running_workflows(self, wf_name, version=None, start_time=None, end_time=None):
        url = self.make_url('running/{}', wf_name)
        params = {'version': version, 'startTime': start_time, 'endTime': end_time}
        return self.get(url, params)

    def start_workflow(self, wf_name, input_json, version=None, correlation_id=None):
        url = self.make_url('{}', wf_name)
        params = {'version': version, 'correlationId': correlation_id}
        headers = {'Accept': 'text/plain'}
        return self.post(url, params, input_json, headers)

    def terminate_workflow(self, wf_id, reason=None):
        url = self.make_url('{}', wf_id)
        params = {'reason': reason}
        self.delete(url, params)

    def remove_workflow(self, wf_id, archive_workflow, reason=None):
        url = self.make_url('{}/remove', wf_id)
        self.delete(url, self.make_params(archiveWorkflow=archive_workflow, reason=reason))

    def pause_workflow(self, wf_id):
        url = self.make_url('{}/pause', wf_id)
        self.put(url)

    def resume_workflow(self, wf_id):
        url = self.make_url('{}/resume', wf_id)
        self.put(url)

    def skip_task_from_workflow(self, wf_id, task_ref_name, skip_task_request):
        url = self.make_url('{}/skiptask/{}', wf_id, task_ref_name)
        self.post(url, None, skip_task_request)

    def rerun_workflow(self, wf_id, task_ref_name, rerun_workflow_request):
        url = self.make_url('{}/rerun', wf_id)
        return self.post(url, None, rerun_workflow_request)

    def restart_workflow(self, wf_id, task_ref_name, from_task_ref):
        url = self.make_url('{}/restart', wf_id)
        params = {'from': from_task_ref}
        self.post(url, params, None)


class EventServicesClient(BaseClient):
    BASE_RESOURCE = 'event'

    def __init__(self, base_url, headers=None):
        BaseClient.__init__(self, base_url, self.BASE_RESOURCE, headers)

    def get_event_handler_def(self, event, active_only=True):
        url = self.make_url('{}', event)
        params = {'activeOnly': active_only}
        return self.get(url, params)

    def get_event_handler_defs(self):
        url = self.make_url()
        return self.get(url)

    def create_event_handler_def(self, eh_obj):
        url = self.make_url()
        return self.post(url, None, eh_obj)

    def update_event_handler_def(self, eh_obj):
        url = self.make_url()
        return self.put(url, None, eh_obj)

    def remove_event_handler(self, eh_name):
        url = self.make_url('{}', eh_name)
        self.delete(url, {})

    def get_event_handler_queues(self):
        url = self.make_url('queues')
        return self.get(url)

    def get_event_handler_queues_providers(self):
        url = self.make_url('queues/providers')
        return self.get(url)


class WFClientMgr:
    def __init__(self, server_url='http://localhost:8080/api/', headers=None):
        self.workflow_client = WorkflowClient(server_url, headers)
        self.task_client = TaskClient(server_url, headers)
        self.metadata_client = MetadataClient(server_url, headers)
