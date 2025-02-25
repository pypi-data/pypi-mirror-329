from _typeshed import Incomplete
from firebase_admin import exceptions as exceptions

class Notification:
    title: Incomplete
    body: Incomplete
    image: Incomplete
    def __init__(self, title: Incomplete | None = None, body: Incomplete | None = None, image: Incomplete | None = None) -> None: ...

class AndroidConfig:
    collapse_key: Incomplete
    priority: Incomplete
    ttl: Incomplete
    restricted_package_name: Incomplete
    data: Incomplete
    notification: Incomplete
    fcm_options: Incomplete
    direct_boot_ok: Incomplete
    def __init__(self, collapse_key: Incomplete | None = None, priority: Incomplete | None = None, ttl: Incomplete | None = None, restricted_package_name: Incomplete | None = None, data: Incomplete | None = None, notification: Incomplete | None = None, fcm_options: Incomplete | None = None, direct_boot_ok: Incomplete | None = None) -> None: ...

class AndroidNotification:
    title: Incomplete
    body: Incomplete
    icon: Incomplete
    color: Incomplete
    sound: Incomplete
    tag: Incomplete
    click_action: Incomplete
    body_loc_key: Incomplete
    body_loc_args: Incomplete
    title_loc_key: Incomplete
    title_loc_args: Incomplete
    channel_id: Incomplete
    image: Incomplete
    ticker: Incomplete
    sticky: Incomplete
    event_timestamp: Incomplete
    local_only: Incomplete
    priority: Incomplete
    vibrate_timings_millis: Incomplete
    default_vibrate_timings: Incomplete
    default_sound: Incomplete
    light_settings: Incomplete
    default_light_settings: Incomplete
    visibility: Incomplete
    notification_count: Incomplete
    def __init__(self, title: Incomplete | None = None, body: Incomplete | None = None, icon: Incomplete | None = None, color: Incomplete | None = None, sound: Incomplete | None = None, tag: Incomplete | None = None, click_action: Incomplete | None = None, body_loc_key: Incomplete | None = None, body_loc_args: Incomplete | None = None, title_loc_key: Incomplete | None = None, title_loc_args: Incomplete | None = None, channel_id: Incomplete | None = None, image: Incomplete | None = None, ticker: Incomplete | None = None, sticky: Incomplete | None = None, event_timestamp: Incomplete | None = None, local_only: Incomplete | None = None, priority: Incomplete | None = None, vibrate_timings_millis: Incomplete | None = None, default_vibrate_timings: Incomplete | None = None, default_sound: Incomplete | None = None, light_settings: Incomplete | None = None, default_light_settings: Incomplete | None = None, visibility: Incomplete | None = None, notification_count: Incomplete | None = None) -> None: ...

class LightSettings:
    color: Incomplete
    light_on_duration_millis: Incomplete
    light_off_duration_millis: Incomplete
    def __init__(self, color, light_on_duration_millis, light_off_duration_millis) -> None: ...

class AndroidFCMOptions:
    analytics_label: Incomplete
    def __init__(self, analytics_label: Incomplete | None = None) -> None: ...

class WebpushConfig:
    headers: Incomplete
    data: Incomplete
    notification: Incomplete
    fcm_options: Incomplete
    def __init__(self, headers: Incomplete | None = None, data: Incomplete | None = None, notification: Incomplete | None = None, fcm_options: Incomplete | None = None) -> None: ...

class WebpushNotificationAction:
    action: Incomplete
    title: Incomplete
    icon: Incomplete
    def __init__(self, action, title, icon: Incomplete | None = None) -> None: ...

class WebpushNotification:
    title: Incomplete
    body: Incomplete
    icon: Incomplete
    actions: Incomplete
    badge: Incomplete
    data: Incomplete
    direction: Incomplete
    image: Incomplete
    language: Incomplete
    renotify: Incomplete
    require_interaction: Incomplete
    silent: Incomplete
    tag: Incomplete
    timestamp_millis: Incomplete
    vibrate: Incomplete
    custom_data: Incomplete
    def __init__(self, title: Incomplete | None = None, body: Incomplete | None = None, icon: Incomplete | None = None, actions: Incomplete | None = None, badge: Incomplete | None = None, data: Incomplete | None = None, direction: Incomplete | None = None, image: Incomplete | None = None, language: Incomplete | None = None, renotify: Incomplete | None = None, require_interaction: Incomplete | None = None, silent: Incomplete | None = None, tag: Incomplete | None = None, timestamp_millis: Incomplete | None = None, vibrate: Incomplete | None = None, custom_data: Incomplete | None = None) -> None: ...

class WebpushFCMOptions:
    link: Incomplete
    def __init__(self, link: Incomplete | None = None) -> None: ...

class APNSConfig:
    headers: Incomplete
    payload: Incomplete
    fcm_options: Incomplete
    def __init__(self, headers: Incomplete | None = None, payload: Incomplete | None = None, fcm_options: Incomplete | None = None) -> None: ...

class APNSPayload:
    aps: Incomplete
    custom_data: Incomplete
    def __init__(self, aps, **kwargs) -> None: ...

class Aps:
    alert: Incomplete
    badge: Incomplete
    sound: Incomplete
    content_available: Incomplete
    category: Incomplete
    thread_id: Incomplete
    mutable_content: Incomplete
    custom_data: Incomplete
    def __init__(self, alert: Incomplete | None = None, badge: Incomplete | None = None, sound: Incomplete | None = None, content_available: Incomplete | None = None, category: Incomplete | None = None, thread_id: Incomplete | None = None, mutable_content: Incomplete | None = None, custom_data: Incomplete | None = None) -> None: ...

class CriticalSound:
    name: Incomplete
    critical: Incomplete
    volume: Incomplete
    def __init__(self, name, critical: Incomplete | None = None, volume: Incomplete | None = None) -> None: ...

class ApsAlert:
    title: Incomplete
    subtitle: Incomplete
    body: Incomplete
    loc_key: Incomplete
    loc_args: Incomplete
    title_loc_key: Incomplete
    title_loc_args: Incomplete
    action_loc_key: Incomplete
    launch_image: Incomplete
    custom_data: Incomplete
    def __init__(self, title: Incomplete | None = None, subtitle: Incomplete | None = None, body: Incomplete | None = None, loc_key: Incomplete | None = None, loc_args: Incomplete | None = None, title_loc_key: Incomplete | None = None, title_loc_args: Incomplete | None = None, action_loc_key: Incomplete | None = None, launch_image: Incomplete | None = None, custom_data: Incomplete | None = None) -> None: ...

class APNSFCMOptions:
    analytics_label: Incomplete
    image: Incomplete
    def __init__(self, analytics_label: Incomplete | None = None, image: Incomplete | None = None) -> None: ...

class FCMOptions:
    analytics_label: Incomplete
    def __init__(self, analytics_label: Incomplete | None = None) -> None: ...

class ThirdPartyAuthError(exceptions.UnauthenticatedError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class QuotaExceededError(exceptions.ResourceExhaustedError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class SenderIdMismatchError(exceptions.PermissionDeniedError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...

class UnregisteredError(exceptions.NotFoundError):
    def __init__(self, message, cause: Incomplete | None = None, http_response: Incomplete | None = None) -> None: ...
