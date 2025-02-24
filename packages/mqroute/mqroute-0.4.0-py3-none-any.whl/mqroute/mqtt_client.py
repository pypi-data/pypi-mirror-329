"""
This module provides functionality for creating and managing an MQTT client.

It includes necessary methods for connecting to an MQTT broker, subscribing to topics,
publishing messages, and handling incoming messages.

The implementation is done in Python 3.13.1 and relies on the `paho-mqtt` library for
the MQTT protocol handling.

Dependencies:
- docutils
- pip
- pylint
- pytest
- requests
- wheel

Make sure to configure the MQTT broker settings appropriately before using the module.
"""
import asyncio
import socket
import time
from asyncio import iscoroutine
from functools import singledispatchmethod
from logging import getLogger
from random import randint, uniform
import signal
from typing import Any, Callable, Coroutine, Optional, Union

from paho.mqtt import client as mqtt
from typeguard import typechecked, check_type

from .callback_runner import CallbackRunner
from .message_publisher import MessagePublisher
from .mqtt_client_userdata import MQTTClientUserData
from .mqtt_message import MQTTMessage
from .mqtt_subscription import MQTTSubscription
from .payload_formats import PayloadFormat
from .qos import QOS
from .callback_resolver import CallbackResolver
from .publish_message import PublishMessage


__all__ = ["MQTTClient"]

# To be decided if there is a need to actually publish these definitions. If so, it's just
# a matter of adding these to  __all__
type MessageHandlerCallbackType = Callable[[str, MQTTMessage, Optional[dict[str, str]]],
                                           None]
type AsyncMessageHandlerCallbackType = Callable[[str, MQTTMessage, Optional[dict[str, str]]],
                                                Coroutine[Any, Any, None]]
type GenericMessageCallbackType = Union[MessageHandlerCallbackType,
                                        AsyncMessageHandlerCallbackType]


logger = getLogger(__name__)


class MQTTClient:
    """
    The MQTTClient class provides a wrapper around the Paho MQTT library to manage MQTT
    connections, subscriptions, and messaging callbacks. It facilitates setting up MQTT
    communication with additional utilities for message handling, subscriptions, decorators,
    and logging. The class is highly configurable, allowing for easy integration into various
    applications requiring MQTT messaging.

    This class configures connection management, initializes callbacks, and supports advanced
    features such as JSON payload processing, fallback mechanisms, and wildcard topic handling.

    :ivar __host: The MQTT broker host to connect to.
    :type __host: str
    :ivar __port: The MQTT broker port to connect to.
    :type __port: int
    :ivar __backoff_time: Tracks the backoff duration for connection retries.
    :type __backoff_time: int
    :ivar __subscriptions: Holds the list of active MQTT subscriptions.
    :type __subscriptions: list[MQTTSubscription]
    :ivar __msg_callbacks: Manages message callbacks for MQTT topics.
    :type __msg_callbacks: CallbackResolver
    :ivar __cb_runner: Handles execution of the callback queue.
    :type __cb_runner: CallbackRunner
    :ivar __cb_runner_task: Task associated with running callbacks.
    :type __cb_runner_task: Optional[asyncio.Task]
    :ivar __running: Tracks if the MQTT client is running.
    :type __running: bool
    :ivar __client: The internal Paho MQTT client instance.
    :type __client: mqtt.Client
    :ivar sigstop_handlers: Handlers for SIGSTOP and related signals.
    :type sigstop_handlers: list
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # noinspection PyArgumentList
    @typechecked
    def __init__(self, *,
                 host: str,
                 port: int = 1883,
                 transport: str = "tcp",
                 ws_path: str = "/mqtt",
                 set_tls:  bool = False,
                 paho_logs = False ):
        """
        Initializes an MQTTClient instance with essential configurations such as host, port, and
        optional logging. This class configures the client's callbacks and prepares it to handle
        MQTT network operations, including connection, subscription, messaging, publishing, and
        logging.

        :param host: Hostname or IP address of the MQTT broker to connect to.
        :type host: str
        :param port: Port number of the MQTT broker for connection. If not provided, defaults
                     to 1883.
        :type port: int
        :param paho_logs: Optional parameter to enable or disable Paho MQTT client logs. Defaults
                          to False.
        :type paho_logs: bool
        """
        self.__host: str = host
        self.__port: int = port

        self.__backoff_time = 1

        self.__subscriptions: list[MQTTSubscription] = []

        self.__msg_callbacks: CallbackResolver = CallbackResolver()
        self.__cb_runner = CallbackRunner()

        # this is unused, however, the task needs to be stored somewhere in order
        # to avoid it be garbage collected and thus killed prematurely.
        self.__cb_runner_task: Optional[asyncio.Task] = None # pylint: disable=unused-private-member
        self.__msg_publisher_task: Optional[asyncio.Task] = None # pylint: disable=unused-private-member

        self.__running = False

        client_host_name = socket.gethostname()
        client_id = f"{client_host_name}-{randint(0, 1_000_000):x}"

        logger.info(("Initializing MQTTClient: client_id=%s, host=%s, port=%s, transport=%s, "
                     "set_tls=%s, paho_logs=%s"),
                    client_id,
                    host,
                    port,
                    transport,
                    set_tls,
                    paho_logs)
        self.__client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                                    transport=transport)
        if set_tls:
            self.__client.tls_set()
        self.__client.ws_set_options(path=ws_path)

        self.__msg_publisher = MessagePublisher(self.__client)

        userdata = MQTTClientUserData(self)
        self.__client.user_data_set(userdata)

        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.on_publish = self.__on_publish
        self.__client.on_subscribe = self.__on_subscribe
        self.__client.on_connect_fail = self.__on_connect_fail
        self.__client.on_disconnect = self.__on_disconnect

        if paho_logs:
            self.__client.on_log = self.on_log

        self.__client.on_unsubscribe = self.on_unsubscribe

        self.sigstop_handlers = []

        signal.signal(signal.SIGINT, self.sigint_handler)

    @property
    def running(self):
        """
        Indicates whether the related process or service is currently in a running state.

        The `running` property provides a Boolean value reflecting the status of the
        underlying process or service. It is used to determine if the process/service
        is actively running or has been stopped. This property is read-only.

        :rtype: bool
        :return: True if the process/service is running, otherwise False.
        """
        return self.__running

    @property
    def ready(self) -> bool:
        """
        Indicates whether the MQTTClient is ready for use or not.

        This property checks the internal readiness state of the object.
        It returns a boolean value that indicates if the object has been
        appropriately initialized or is prepared to perform its functions.

        :return: The readiness state of the object.
        :rtype: bool
        """
        ready = True
        if self.__cb_runner is None or self.__msg_publisher is None:
            ready = False
        elif not self.__cb_runner.ready or not self.__msg_publisher.ready:
            ready = False
        return ready


    @property
    def callback_resolver(self):
        """
        Provides access to the internal message callback resolver.

        This property returns the stored message callback dictionary that associates
        specific message types or identifiers with their corresponding callbacks.
        It is intended to facilitate the retrieval or management of the message-to-callback
        mappings for message handling processes.

        :rtype: dict
        :return: The dictionary containing message-to-callback mappings.
        """
        return self.__msg_callbacks

    @callback_resolver.setter
    def callback_resolver(self, resolver: CallbackResolver):
        """Setter for callback_resolver"""
        self.__msg_callbacks = resolver

    # pylint: disable=too-many-arguments
    # We want to use same parameters than we use with decorator interface + the callback
    @typechecked
    def add_subscription(self,
                         callback: GenericMessageCallbackType,
                         *,
                         topic: str,
                         qos: QOS = QOS.AT_MOST_ONCE,
                         raw_payload: bool = False,
                         fallback: bool = False):
        """
        Adds a subscription for a specific MQTT topic with the given callback.

        This method allows the user to subscribe to an MQTT topic and associate it with
        a callback function that processes messages received on that topic. The subscription
        can specify options such as the quality of service (QoS) level, whether the payload
        should be treated as raw bytes or JSON, and a fallback flag for additional functionality.

        :param callback: The function or coroutine that processes messages received on the
            specified topic.
        :type callback: GenericMessageCallbackType
        :param topic: The MQTT topic to which the subscription is made.
        :type topic: str
        :param qos: The quality of service (QoS) level for the subscription. Defaults to
                    AT_MOST_ONCE.
        :type qos: QOS
        :param raw_payload: A flag indicating whether the payload should be treated as raw bytes
            or JSON. Defaults to False (JSON format).
        :type raw_payload: bool
        :param fallback: An optional flag determining if fallback behavior is enabled during
            message callback processing. Defaults to False.
        :type fallback: bool
        :return: None
        """
        payload_format = PayloadFormat.RAW if raw_payload else PayloadFormat.JSON
        # In practice, this checks just that it's Callable. Maybe more one day...
        check_type(callback,
                   expected_type=GenericMessageCallbackType)

        rewritten_topic = self.__msg_callbacks.register(topic=topic,
                                                        callback=callback,
                                                        payload_format=payload_format,
                                                        fallback=fallback)
        self.__mqtt_subscribe(rewritten_topic, qos)


    @singledispatchmethod
    async def async_publish_message(self, *args, **kwargs):
        """
        Dispatch method for publishing a message asynchronously.

        This method serves as a generic single-dispatch method for unknown signatures.
        :raises NotImplementedError: If the method is called with an unsupported signature.
        """
        raise NotImplementedError("Unsupported signature for async_publish_message")

    @async_publish_message.register
    def _(self, publishable: PublishMessage):
        """
        Asynchronously publishes a message using the provided publishable data.

        This function is a part of a multiple-dispatch mechanism that handles
        publishing operations. It specifically handles a scenario where the
        `PublishMessage` type is passed as the argument. The function delegates
        the actual task of publishing to the `self.async_publish_message` method,
        ensuring the process is executed asynchronously.

        Necessary conditions for this operation are typically defined externally,
        and the method assumes that the `publishable` argument adheres to the required
        structure for successful execution.

        :param publishable: The message to be published, encapsulated in a
            `PublishMessage` type structure.
        :return: None
        """
        self.async_publish_message(publishable=publishable)

    @async_publish_message.register
    async def _(self,
                topic : str,
                payload: Union[str, dict],
                qos: QOS = QOS.AT_MOST_ONCE,
                *,
                retain: bool = False, ):
        """
        Publishes a message asynchronously to a specified topic using the given parameters.
        This function allows sending structured payloads with different QoS levels and
        optional message retention. It provides flexibility for real-time communication
        between distributed systems using MQTT.

        :param topic: The target MQTT topic where the message should be published.
        :type topic: str
        :param payload: The message content or data to be sent. Can be a string or dictionary.
        :type payload: Union[str, dict]
        :param qos: The Quality of Service (QoS) level for message delivery. Defaults to
            QOS.AT_MOST_ONCE.
        :type qos: QOS
        :param retain: A flag indicating whether the message should be retained on the broker.
            Defaults to `False`.
        :type retain: bool
        :return: None
        :rtype: None
        """
        self.publish_message(topic, payload=payload, qos=qos, retain=retain)

    @singledispatchmethod
    def publish_message(self, *args, **kwargs):
        """
        Dispatch method for publishing a message.

        This method serves as a generic single-dispatch method for unknown signatures.
        :raises NotImplementedError: If the method is called with an unsupported signature.
        """
        raise NotImplementedError("Unsupported signature for publish_message method")

    @publish_message.register
    def _(self, publishable: PublishMessage):
        """
        Publishes a given message through the message publisher system. The function
        is part of a message dispatching mechanism and is designed to handle objects
        of type `PublishMessage`. It logs a debug message indicating the content
        being published before invoking the underlying publishing mechanism.

        :param publishable: The message object of type `PublishMessage` to be published.
        :return: None
        """
        logger.debug("Publishing: %s", publishable)
        self.__msg_publisher.publish(publishable)

    @publish_message.register
    def _(self,
          topic : str,
          payload: Union[str, dict],
          qos: QOS = QOS.AT_MOST_ONCE,
          *,
          retain: bool = False, ):
        """
        Publishes a message to a specified topic with optional quality of service (QoS) and
        retain flag.

        This method allows sending a publish message to a specific MQTT topic
        with an optional payload, QoS level, and retain flag. The payload can
        be a string or dictionary. The QoS level determines the message delivery
        guarantee, and the retain flag specifies if the message should be retained
        on the broker.

        :param topic: The MQTT topic to which the message should be published.
        :type topic: str
        :param payload: The content of the message to send. Payload can be a string or dictionary.
        :type payload: Union[str, dict]
        :param qos: Quality of Service level defining message delivery guarantees.
        :type qos: QOS
        :param retain: Boolean flag specifying whether the message should be retained on the broker.
                       Defaults to False.
        :type retain: bool
        :return: None
        """
        message = PublishMessage(topic=topic,
                                 payload=payload,
                                 qos=qos,
                                 retain=retain)
        self.publish_message(message)

    def publish(self,
                topic : str,
                qos: QOS = QOS.AT_MOST_ONCE,
                *,
                retain: bool = False ):
        """
        This method is a decorator designed to allow seamless message
        publishing for synchronous or asynchronous functions. It decorates
        a function to automatically convert its return value into a format
        suitable for publishing and sends it as a `PublishMessage`
        via the `self.publish_message()` method. The decorator supports
        customizable parameters for the topic, quality of service (QoS),
        and retention policy of the message.

        The decorated function's result is automatically transformed into
        a publishable message and transmitted. It is compatible with both
        coroutine (async) functions and standard Python functions.

        :param topic: The topic string under which the message will be published.
                      This topic organizes how messages are communicated.
        :param qos: The quality of service level to use for the message.
                    Defaults to `QOS.AT_MOST_ONCE`. This determines how
                    delivery of the message is handled.
        :param retain: A boolean flag determining if the message should be
                       retained by the server. Retained messages can act as
                       "last known good states" for subscribers. Optional
                       and defaults to `False`.
        :return: The wrapping function that ensures the decorated function's
                 result is converted into a publishable message and sent via
                 `self.publish_message()`.
        """
        def decorator(func):
            if iscoroutine(func):
                async def wrapper(*args, **kwargs):
                    message = await func(*args, **kwargs)
                    publishable = PublishMessage(topic=topic,
                                                 payload=message,
                                                 qos=qos,
                                                 retain=retain
                                                 )
                    if publishable is not None:
                        self.publish_message(publishable)
            else:
                def wrapper(*args, **kwargs):
                    message = func(*args, **kwargs)
                    publishable = PublishMessage(topic=topic,
                                                 payload=message,
                                                 qos=qos,
                                                 retain=retain
                                                 )
                    if publishable is not None:
                        self.publish_message(publishable)

            return wrapper

        return decorator


    # pylint: enable=too-many-arguments

    @typechecked
    def subscribe(self,
                  topic: str,
                  qos: QOS = QOS.AT_MOST_ONCE,
                  raw_payload: bool = False,
                  fallback: bool = False):
        """
        The `subscribe` method facilitates MQTT topic subscription by allowing the user to create
        a decorator that processes incoming messages before invoking the decorated function.
        It provides the option to automatically convert JSON payloads to Python dictionaries.
        It also registers the callback to the specified topic and subscribes to it with the
        desired Quality of Service (QoS) level.

        Standard MQTT wildcards are supported:
           - "#" matches any topics under the current level, including multilevel matches.
           - "+" matches exactly one level.
           - If there is a need to capture the value of single level wildcard matched
             by + a parameter can be created. This is achieved by using - instead of
             single + as MQTT standard - syntax like +<parameter_name>+
             The CallbackResolver will then create a parameter <parameter_name> that is
             assigned with value found in the matched topic.

        :param topic: The MQTT topic to subscribe to.
        :param qos: The Quality of Service level for the topic subscription.
        :param raw_payload: If set to True, the message payload will not be converted from JSON.
                            Defaults to False.
        :param fallback: If set to True, the callback is only called when no other callbacks were
                         called by the topic. Defaults to False.
        :return: A decorator function that wraps the user's callback function.
        """
        def decorator(func):
            payload_format = PayloadFormat.RAW if raw_payload else PayloadFormat.JSON
            # In practice, this checks just that it's Callable. Maybe more one day...
            check_type(func, expected_type=GenericMessageCallbackType)

            rewritten_topic = self.__msg_callbacks.register(topic=topic,
                                                            callback=func,
                                                            payload_format=payload_format,
                                                            fallback=fallback)
            self.__mqtt_subscribe(rewritten_topic, qos)

            return func

        return decorator

    @property
    def subscriptions(self) -> list[MQTTSubscription]:
        """
        Provides access to the list of MQTTSubscription objects that represent the
        current subscriptions. The returned list contains all active subscriptions
        associated with the instance, allowing external access in a read-only manner.

        :return: A list of MQTTSubscription objects representing active subscriptions
        :rtype: list[MQTTSubscription]
        """
        return self.__subscriptions

    def connect(self):
        """
        Connects to the server using the specified host and port configuration. This method
        establishes a connection with the server by utilizing the internal messaging callbacks
        and client properties.

        Logs the current message callbacks for debugging purposes before attempting to connect
        to the specified server endpoint.

        :raises ConnectionError: If the connection attempt fails for any reason.
        """
        logger.debug(self.__msg_callbacks)
        self.__client.connect(host=self.__host,
                              port=self.__port)

    def reconnect(self):
        """
        Attempts to reconnect to a service with an exponential backoff strategy.

        This method repeatedly tries to establish a connection by invoking the
        `connect` method. In the event of a failure, it waits for an exponentially
        increasing duration, capped at 60 seconds, before retrying. The backoff time
        is also randomized slightly to prevent synchronized retry bursts.

        :return: None
        """
        backoff = self.__backoff_time
        while True:
            try:
                self.connect()
                break
            except Exception as e:  # pylint: disable=broad-exception-caught
                # catch exception. This is reconnect, so stupid mistakes like invalid host name
                # are found earlier - the connection was working already. Also, paho does not
                # document exceptions possible raised by connect so we cannot easily be more
                # specific.
                logger.warning("Reconnect failed: %s. Retrying in %s seconds...",
                               e,
                               backoff)
                time.sleep(self.__backoff_time)
                backoff = min(60, backoff * 2 + uniform(0, 1))  # cap at 60 seconds

    @property
    def topic_map(self) -> CallbackResolver:
        """
        Provides access to the topic map which holds the message callback
        resolvers. This property is used to retrieve the callback resolver
        that is linked with message topics to handle incoming messages.

        :return: The message callback resolver associated with topics.
        :rtype: CallbackResolver
        """
        return self.__msg_callbacks

    # noinspection PyTypeChecker
    async def run(self):
        """
        Represents a method to initiate and maintain a connection loop for a client.

        This method establishes a connection and transitions the client to continually
        process events until explicitly stopped. It is often used in environments
        where a continuous bidirectional connection needs to persist.

        :raises Exception: If the connection fails or an error occurs during the
            looping process.

        :return: None
        """
        self.__running = True

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None,
                                   self.__client.connect,
                                   self.__host,
                                   self.__port)

        self.__cb_runner.loop = loop
        self.__msg_publisher.loop = loop

        # self.__msg_publisher and  self.__cb_runner_task are unused , however, the task needs to be
        # stored somewhere in order to avoid it be garbage collected and thus killed prematurely.
        self.__msg_publisher_task = asyncio.create_task(   # pylint: disable=unused-private-member
            self.__msg_publisher.execute())

        self.__cb_runner_task = asyncio.create_task(       # pylint: disable=unused-private-member
            self.__cb_runner.process_callbacks())

        self.__client.loop_start()

    def stop(self):
        """
        Stops the running MQTT client loop and associated callback thread.

        This method will safely stop the client loop and its associated callback runner,
        ensuring all operations are halted cleanly.

        :return: None
        """
        self.__running = False
        self.__client.loop_stop()
        self.__cb_runner.stop()

    def sigint_handler(self,
                       _,  #signum,
                       __):  # frame
        """
        Handler for the SIGSTOP signal. Logs a termination message, executes all
        registered `sigstop_handlers` functions, and initiates the stop process.

        :param signum: Signal number received.
        :param frame: Current stack frame at the time the signal was intercepted.
        :return: None
        """
        logger.info("Terminating...")
        for func in self.sigstop_handlers:
            func()
        self.stop()

    def sigint(self, func: Callable):
        """
        Decorator  that wraps a given function with additional functionality and appends it to the 
        `sigintp_handlers` list of the current instance. The wrapped function can
        later be used for handling specific signal stop functionalities as needed.

        :param func: The function to be wrapped and added to `sigstop_handlers`.
        :type func: Callable
        :return: The wrapped function that adds functionality to `sigstop_handlers`.
        :rtype: Callable
        """
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        self.sigstop_handlers.append(wrapper)
        return wrapper


    @singledispatchmethod
    def __mqtt_subscribe(self, *args, **kwargs):
        raise NotImplementedError("Unsupported signature for __mqtt_subscribe method")

    @__mqtt_subscribe.register
    def _(self, subscription: MQTTSubscription) -> MQTTSubscription:
        """
        Subscribe to a topic by adding the given subscription to the list of current
        subscriptions and returns it. The method is a dispatch function for handling
        varied input arguments based on the type.

        :param subscription: The MQTT subscription to be added to the list of
            subscriptions.
        :return: The MQTT subscription that was successfully subscribed.
        """
        self.__subscriptions.append(subscription)
        return subscription

    @__mqtt_subscribe.register
    def _(self, topic: str, qos: QOS) -> MQTTSubscription:
        """
        Subscribes to a specific MQTT topic with a designated quality of service (QoS) level
        and registers the subscription. This method allows managing MQTT subscriptions
        by adding them to an internal list and returning the created subscription object.

        :param topic: The MQTT topic to subscribe to.
        :type topic: str
        :param qos: Quality of Service level for the subscription (0, 1, or 2).
        :type qos: QOS
        :return: An `MQTTSubscription` object representing the subscription with the
                 specified topic and QoS level.
        :rtype: MQTTSubscription
        """
        subscription = MQTTSubscription(topic=topic, qos=qos.value)
        self.__subscriptions.append(subscription)
        return subscription

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    # these are callbacks with signatures defined in paho.mqtt - and we can't do anything
    # to these having too many arguments.

    @staticmethod
    def __on_connect(client: mqtt.Client,
                     userdata: MQTTClientUserData,
                     _: dict[str, Any],  # connect_flags
                     reason_code: mqtt.ReasonCodes,
                     __: mqtt.Properties):              # properties
        """
        Handles the connection of the MQTT client to the server. This method is invoked
        when the client establishes a connection to the broker. It logs the connection
        reason code and processes any subscriptions defined in the client's userdata.
        If subscriptions are present, it sends the subscription requests and stores
        them. If no subscriptions are found, a warning is logged and the current
        subscriptions list is cleared.

        :param client: The MQTT client instance that represents the connection to the broker.
        :param userdata: User-defined data of type MQTTClientUserData, which typically holds
            application-specific information, including client's subscriptions.
        :param _: A dictionary representing the connection flags in MQTT protocol.
        :param reason_code: The reason code for the connection result as provided by the MQTT
                            broker.
        :param __: MQTT properties that are associated with the connection establishment.
        :return: None
        """
        logger.debug("Connected with reason code %s", reason_code)
        subscriptions = [ (s.topic, s.qos)  for s in userdata.client.subscriptions]
        if subscriptions:
            logger.debug(" => Subscribing %s", subscriptions)
            client.subscribe(subscriptions)
        else:
            logger.warning(" => Nothing to subscribe")



    def __on_message(self,
                     _: mqtt.Client,  # client
                     userdata: MQTTClientUserData,
                     message: mqtt.MQTTMessage):
        """
        Handles incoming MQTT messages by processing them and executing corresponding callbacks
        registered to the topic.

        This method is triggered whenever a subscribed topic receives a new message. It decodes
        the message payload, maps it to the respective topic, and executes each callback associated
        with the topic. The callbacks are executed using a callback runner for proper handling.

        :param _:
            Represents an instance of the MQTT client that initiated the callback. This parameter
            is typically required by the MQTT library but is unused in this implementation.
        :param userdata:
            The user-specific data passed to the MQTT client. Should contain a `client` object with
            a `topic_map` attribute mapping topics to their respective callbacks.
        :param message:
            The received MQTT message object containing information such as the message payload and
            topic.
        :return:
            None. This function does not return any value.
        """
        topic = message.topic
        topic_map = userdata.client.topic_map
        msg = MQTTMessage(topic=message.topic,
                          message=message.payload.decode('utf-8'))
        for cb in topic_map.callbacks(topic):
            #cb.cb_method(cb.topic, msg, cb.parameters)
            self.__cb_runner.run_callback(cb, msg)



    def __on_publish(self,
                     client: mqtt.Client,
                     userdata: MQTTClientUserData,
                     mid: int,
                     reason_code: mqtt.ReasonCodes,
                     properties: mqtt.Properties):
        """
        Handles the event triggered when a message is successfully published.

        This callback is invoked upon the completion of a message publishing
        operation. It provides details about the publishing process, including the
        message ID, reason code, and any properties included.

        :param client: An instance of the MQTT client that triggered the callback.
        :param userdata: A user-defined data structure containing context.
        :param mid: The unique identifier of the published message.
        :param reason_code: The result of the publish action, represented as a reason code.
        :param properties: Additional MQTT properties associated with the publish event.
        :return: None
        """


    @staticmethod
    def __on_subscribe(_: mqtt.Client,  # client
                       userdata: MQTTClientUserData,  # userdata
                       __: int,  # mid
                       reason_code_list: list[mqtt.ReasonCodes],
                       ___: mqtt.Properties):                          # properties
        """
        Handle the MQTT client subscription event.

        This method is triggered when the client has successfully completed a
        subscription request. It logs the subscriptions along with their
        corresponding reason codes.

        :param _: The MQTT client instance.
        :param userdata: An instance of MQTTClientUserData used to track client-specific
            data throughout the connection's context.
        :param __: Message identifier (mid), which helps in tracking subscription
            requests.
        :param reason_code_list: A list of reason codes detailing outcomes for each subscribed
            topic.
        :param ___: An instance of mqtt.Properties containing additional properties related
            to the subscription.
        :return: None
        """
        logger.debug("Subscriptions completed with following reason codes:")

        for sub, reason in zip(userdata.client.subscriptions, reason_code_list):
            logger.debug("   %s: '%s'", sub.topic, reason)

    def __on_connect_fail(self,
                          client: mqtt.Client,
                          userdata: MQTTClientUserData,
                          mid: int,
                          reason_code_list: list[mqtt.ReasonCodes],
                          properties: mqtt.Properties):
        """
        Callback triggered when the client fails to connect to the MQTT broker.

        This method is called when a connection attempt to the broker fails.
        The reason for the failure, along with other pertinent details, is
        provided through the parameters.

        :param client: The MQTT client instance that failed the connection attempt.
        :param userdata: The private user data object provided to the client,
            which can be used to maintain application data related to the connection.
        :param mid: The message identifier associated with the connection attempt.
        :param reason_code_list: A list of reason codes providing detail about why
            the connection attempt failed.
        :param properties: Set of properties for the MQTT message
            associated with the connection attempt, following MQTT v5.0 protocols.
        :return: None
        """

    @staticmethod
    def __on_disconnect(_: mqtt.Client,
                        userdata: MQTTClientUserData,
                        __: mqtt.DisconnectFlags,
                        reason_code: mqtt.ReasonCodes,
                        ___: mqtt.Properties):
        """
        Handles client disconnection event from the MQTT broker. Clears the
        current subscriptions, logs the disconnection reason, and attempts
        to reconnect to the broker.

        :param _: An instance of `mqtt.Client` representing the client that
            encountered the disconnect event.
        :param userdata: An instance of `MQTTClientUserData` holding application-
            specific user data associated with the MQTT client.
        :param __: An instance of `mqtt.DisconnectFlags` providing additional flags
            describing the reason for the disconnection.
        :param reason_code: A value of `mqtt.ReasonCodes` enum indicating the
            reason for the disconnect as specified by the MQTT protocol.
        :param ___: An instance of `mqtt.Properties` containing additional
            properties and metadata related to the disconnection.
        :return: None
        """
        logger.warning("Disconnected with reason %s", reason_code)
        logger.info("Trying to reconnect")
        userdata.client.reconnect()




    @staticmethod
    def on_log(_: mqtt.Client,  # client
               __: MQTTClientUserData,  # userdata
               level: int,
               buf: str):
        """
        Handles MQTT logging events for the client. This function is triggered
        whenever an MQTT log event occurs during the client's runtime.

        :param _: The MQTT client instance for the session.
        :param __: User-defined data of type ``MQTTClientUserData`` passed to the
            client during initial configuration.
        :param level: An integer representing the severity level of the log
            event. Higher values typically indicate more severe issues.
        :param buf: A string containing the log message generated by the MQTT
            client or library.

        :return: None. This function does not return any value.
        """
        logger.debug(msg=f"mqtt-client: ({level}): {buf}")


    def on_unsubscribe(self,
                       client: mqtt.Client,
                       userdata: MQTTClientUserData,
                       disconnect_flags: mqtt.DisconnectFlags,
                       reason_code: mqtt.ReasonCodes,
                       properties: mqtt.Properties):
        """
        This method is a callback invoked when the client completes an unsubscribe request to the
        broker. It provides information about the unsubscribe operation, including user data,
        disconnect flags, reason code, and any properties associated with the process.

        :param client: The MQTT client instance that is invoking the callback.
        :type client: mqtt.Client
        :param userdata: The private user data set for the client. It is passed to callbacks as-is
            without any modifications.
        :type userdata: MQTTClientUserData
        :param disconnect_flags: Flags indicating the disconnection state of the client.
        :type disconnect_flags: mqtt.DisconnectFlags
        :param reason_code: The reason code for unsubscribing as sent by the broker. Useful to
            understand why the unsubscribe was processed.
        :type reason_code: mqtt.ReasonCodes
        :param properties: Optional properties associated with the unsubscribe process, provided
            in MQTT v5.0 or higher. May include broker-specific metadata.
        :type properties: mqtt.Properties
        :return: None
        """

    # pylint: enable=too-many-arguments
