##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
import inspect
import itertools
import uuid
import connexion as cx
import pkg_resources
import yaml

from flask import Response
from rwlock.rwlock import RWLock


import mistk.data.utils
from mistk.watch import watch_manager
from mistk.data import TransformSpecificationInitParams, TransformInstanceStatus, ObjectInfo, ServiceError

from mistk.transform.server.controllers import transform_plugin_endpoint_controller
import mistk.transform
from mistk import logger

class TransformPluginTask:
    """
    A task to be submitted to the Transform Plugin instance that will be performed and report status of.
    """
    
    def __init__(self, operation, parameters = None, submitted = None, 
                 completed = None, status = None, message = None):
        """
        Initializes the  Transform Plugin Task 
        
        :param operation: The operation to be performed by this task
        :param parameters: Optional parameters for this specific operation
        :param submitted: Optional flag indicating whether the task was submitted
        :param completed: Optional flag indicating whether the task was completed
        :param status: Optional status of the task
        :param message: Optional text message regarding the status of the task        
        """
        self.operation = operation
        self.parameters = parameters
        self.submitted = submitted
        self.completed = completed
        self.status = status
        self.message = message


class TransformPluginEndpoint():
    
    def __init__(self):
        """
        Initializes the Model Instance Endpoint service
        """
    
        initializeEndpointController(self, transform_plugin_endpoint_controller)

        self.app = cx.FlaskApp('mistk.transform.server')
        self.app.app.json_encoder = mistk.data.utils.PresumptiveJSONEncoder
        self.app.add_api(self._load_api_spec())
        self.http_server = None
        
        self._state_machine = None
        self._transform_plugin = None
        self._current_task = None
        
        self._status_lock = RWLock() 
        self._task_lock = RWLock()
         
        self._old_tasks = list()
        self._thread_pool = ThreadPoolExecutor()
        
        info = ObjectInfo('TransformInstanceStatus', resource_version=1)
        self._status = TransformInstanceStatus(object_info=info, state='started')
        logger.info('Transform Plugin initialized')

    def start_server(self, port=8080):
        """
        Starts the http server of the Service
        
        :param port: The port on which to start the server, defaults to 8080
        """
        self.app.run(port=port)

    def _load_api_spec(self):
        """
        Gets the API specification of the module specified
        
        :param module: THe name of the module
        """
        return yaml.load(pkg_resources.ResourceManager().resource_stream('mistk.transform', '/server/swagger/swagger.yaml'), Loader=yaml.SafeLoader)
    
    @property
    def state_machine(self):
        """
        Retrieves the state machine associated with this TransformPluginEndpoint
        
        :return: the state machine
        """
        return self._state_machine
    
    @state_machine.setter
    def state_machine(self, state_machine):
        """
        Sets the state machine associated with this TransformPluginEndpoint
        
        :param state_machine: The new state machine to set
        """
        self._state_machine = state_machine

    @property
    def transform_plugin(self):
        """
        Retrieves the model associated with this TransformPluginEndpoint
        
        :return: the model
        """
        return self._transform_plugin
    
    @transform_plugin.setter
    def transform_plugin(self, transform_plugin):
        """
        Sets the model associated with this TransformPluginEndpoint
        
        :param model: the new model to set
        """
        self._transform_plugin = transform_plugin
    
    def delete_task(self, task):
        """
        Deletes the specified Task.
        This function is currently not supported
        
        :param task: The task to delete
        """
        logger.debug("Ignoring delete task request: %s", str(task))
        return ServiceError(501, "Not currently supported"), 501
     
    def add_task(self, task):
        """
        Adds a task to this TransformPluginService and starts it using a pool of worker threads
        
        :param task: The Task to register and start
        :return: The running task
        """
        try:
            task.id = uuid.uuid4().hex
            task.status = 'queued'
            task.submitted = datetime.now()
            ops = ['transform', 'terminate'] 
             
            if not task.operation in ops:
                msg = "Operation %s must be one of %s" % (str(task.operation), str(ops))
                logger.error(msg)
                return ServiceError(400, msg), 400
         
            with self._task_lock.writer_lock:
                if isinstance(self._current_task, TransformPluginTask):
                    status = self._current_task.status
                    if not status == 'complete' and not status == 'failed':
                        return "Cannot submit a task while current task is not complete.  Current task status is " + status, 400
                if self._current_task:
                    self._old_tasks.insert(0, self._current_task)
                self._current_task = task
                task.status = 'running'

            self._thread_pool.submit(self._process_task)
            return task
        
        except RuntimeError as inst:
            msg = "Error while adding task to TransformPluginService and starting the task. %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def update_state(self, state=None, payload=None):
        """
        Updates the state of the TransformPluginService
        
        :param state: The new state. If not given, the current state will be used.
        :param payload: Additional data to attach to the state
        """
        try:
            with self._status_lock.writer_lock:
                state = state or self._status.state
                ver = self._status.object_info.resource_version + 1
                info = ObjectInfo('TransformInstanceStatus', resource_version=ver)
                self._status = TransformInstanceStatus(info, state=state, payload=payload)
                watch_manager.notify_watch('status', item=self._status)
        except RuntimeError as inst:
            msg = "Error while updating state of the TransformPluginService. %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500
                     
    def _process_task(self):
        """
        Processes the currently queued Task and updates its status as appropriate        
        """
        try:
            logger.info('Processing task %s', self._current_task.operation)
            m = getattr(self.transform_plugin, self._current_task.operation)
            m(**(self._current_task.parameters or {}))
            with self._task_lock.writer_lock:
                self._current_task.status = 'complete'
                self._current_task.completed = datetime.now()
            logger.info('Processing of task is complete')
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error occurred running task")
            self._current_task.status = 'failed'
            self._current_task.message = str(ex)
            raise
    
    def get_status(self, watch=None, resourceVersion=None):  # noqa: E501
        """
        Retrieves the status of the transform plugin
    
        :rtype: TransformInstanceStatus
        """
        logger.debug("Get status called")
        try:
            with self._status_lock.reader_lock:
                if watch:
                    return Response(
                        watch_manager.watch('status', resourceVersion, self._status),
                        mimetype="application/json")
                else:         
                    return self._status
        except RuntimeError as inst:
            msg = "Error while retrieving status for transform plugin. %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500
        return 'do some magic!'
       
    
    def terminate(self):  # noqa: E501
        """
        Shutdowns the transform plugin and cleans up any resources.
        
        :rtype: None
        """
        logger.debug("Terminate called")
        try:
            self.add_task(TransformPluginTask(operation="terminate"))
        except RuntimeError as inst:
            msg = "Error while terminating the transform plugin and cleaning up resources. %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500
    
    
    def transform(self, initParams):  # noqa: E501
        """
        Performs the transforms defined for this plugin
    
        :param initParams: A list of directory paths where input files can be found.
        :type initParams: dict | bytes
    
        :rtype: None
        """
        logger.debug("transform called")
        try:
            if not isinstance(initParams, TransformSpecificationInitParams) and cx.request.is_json:
                initParams = mistk.data.utils.deserialize_model(cx.request.get_json(), TransformSpecificationInitParams)
            assert isinstance(initParams, TransformSpecificationInitParams)
            
            task = TransformPluginTask(operation='transform',
                parameters={"inputDirs": initParams.input_datasets, 
                            "outputDir": initParams.output_dataset, 
                            "properties": initParams.properties})
        except RuntimeError as inst:
            msg = "Error during transform. %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500
        
        self.add_task(task)
        
    def get_api_version(self):
        """
        Returns the version of the MISTK API
    
        :return: The MISTK API version as text
        """
        try:
            version = pkg_resources.require("mistk")[0].version
            return version, 200
        except Exception as ex:
            msg = 'Error occurred while attempting to retrieve MISTK API version: %s' % str(ex)
            logger.exception(msg)
            return ServiceError(500, msg), 500
    
    
def initializeEndpointController(handler, *modules):
    """
    This method iterates over the functions defined in the auto-generated flask modules
    And creates a function in this package which points bound member methods of the 
    handler
    
    :param handler: The handler object which must implement bound member methods which
        otherwise have the same signature as those defined in the controller_modules 
    :param modules: These are the autogenerated swagger controller modules
    """
    
    fns = itertools.chain(*[inspect.getmembers(m, inspect.isfunction) for m in modules])
    for name, fn1 in fns:
        sig1 = inspect.signature(fn1)
        logger.debug("Building redirect for " + name + str(sig1))
        
        fn2 = getattr(handler, name)
        sig2 = inspect.signature(fn2)
        assert sig1 == sig2, "Can't redirect " + name +" : " + str(sig1) + "-" + str(sig2)
        globals()[name] = getattr(handler, name)
