from typing import Union
from typing import Optional
from typing import Type
from typing import Dict
import json
import uuid
import datetime
import logging

import yaml
from bizerror import BizError
from zenutils import jsonutils
from zenutils import importutils

from django.db import models
from django.db.models.aggregates import Max
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext as _

from django_safe_fields.fields import SafeTextField

from .settings import DJANGO_USER_SCHEMA
from .schemas import UserBase

__all__ = [
    "WithAddModTimeFields",
    "WithEnabledStatusFields",
    "WithLockStatusFields",
    "WithDeletedStatusFields",
    "WithConfigFields",
    "WithDisplayOrderFields",
    "WithJsonDataFields",
    "WithUidFields",
    "WithSimpleNRRDStatusFields",
    "WithSimplePRSFStatusFields",
    "WithSimpleResultFields",
    "WithCountFields",
    "WithExpireTimeFields",
    "WithVisibleFields",
    "WithHotspotFields",
    "WithArgsKwargsFields",
    "WithHitsFields",
    "WithOwnerFields",
    "WithInitiatorFields",
    "WithPublishStatusFields",
]

_logger = logging.getLogger(__name__)


class WithAddModTimeFields(models.Model):
    """添加创建时间/修改时间相关字段。"""

    add_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Add Time"),
    )
    mod_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Modify Time"),
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.add_time is None:
            self.add_time = timezone.now()
        self.mod_time = timezone.now()
        return super().save(*args, **kwargs)


class WithEnabledStatusFields(models.Model):
    """添加启用状态相关字段。"""

    auto_enable = True

    enabled = models.BooleanField(
        null=True,
        verbose_name=_("Enabled Status"),
    )
    enabled_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Enabled Time"),
    )
    disabled_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Disabled Time"),
    )

    class Meta:
        permissions = [
            ("set_enabled", "允许设置启用标记"),
            ("set_disabled", "允许设置禁用标记"),
        ]
        abstract = True

    def save(self, *args, **kwargs):
        if (self.enabled is None) and self.auto_enable and (not self.pk):
            self.enabled = True
        if self.enabled is True:
            if self.enabled_time is None:
                self.enabled_time = timezone.now()
            if self.disabled_time is not None:
                self.disabled_time = None
        elif self.enabled is False:
            if self.enabled_time is not None:
                self.enabled_time = None
            if self.disabled_time is None:
                self.disabled_time = timezone.now()
        else:
            if self.enabled_time is not None:
                self.enabled_time = None
            if self.disabled_time is not None:
                self.disabled_time = None
        return super().save(*args, **kwargs)

    def clean_enabled_status(self, save=True):
        self.enabled = None
        self.enabled_time = None
        self.disabled_time = None
        if save:
            self.save()

    def set_enabled(self, save=True):
        self.enabled = True
        self.enabled_time = timezone.now()
        self.disabled_time = None
        if save:
            self.save()

    def set_disabled(self, save=True):
        self.enabled = False
        self.enabled_time = None
        self.disabled_time = timezone.now()
        if save:
            self.save()

    @property
    def is_enabled(self):
        return self.enabled

    def enabled_display(self):
        return self.enabled and _("Enabled") or _("Disabled")

    enabled_display.short_description = _("Enable Status")


class WithLockStatusFields(models.Model):
    """添加锁定相关字段。"""

    lock = models.BooleanField(
        default=False,
        verbose_name=_("Lock Status"),
    )
    locked_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Lock Time"),
    )
    unlocked_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Lock Release Time"),
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.lock:
            if self.locked_time is None:
                self.locked_time = timezone.now()
            if self.unlocked_time is not None:
                self.unlocked_time = None
        else:
            if self.locked_time is not None:
                self.locked_time = None
            if self.unlocked_time is None:
                self.unlocked_time = timezone.now()
        return super().save(*args, **kwargs)

    def set_locked(self, save=True):
        self.lock = True
        if save:
            self.save()

    def set_unlocked(self, save=True):
        self.lock = False
        if self.save:
            self.save()

    @property
    def is_locked(self):
        return self.lock


class WithDeletedStatusFields(models.Model):
    """添加删除状态相关字段。"""

    deleted = models.BooleanField(
        default=False,
        verbose_name=_("Deleted Status"),
    )
    deleted_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Deleted Time"),
    )

    class Meta:
        permissions = [
            ("set_deleted", "允许设置删除标记"),
            ("set_undeleted", "允许清除删除标记"),
        ]
        abstract = True

    def save(self, *args, **kwargs):
        if self.deleted:
            if self.deleted_time is None:
                self.deleted_time = timezone.now()
        else:
            if self.deleted_time is not None:
                self.deleted_time = None
        return super().save(*args, **kwargs)

    def set_deleted(self, save=True):
        self.deleted = True
        if save:
            self.save()

    def set_undeleted(self, save=True):
        self.deleted = False
        if save:
            self.save()

    @property
    def is_deleted(self):
        return self.deleted

    def deleted_display(self):
        return self.deleted and _("Deleted") or _("Not Deleted")

    deleted_display.short_description = _("Deleted Status")


class WithConfigFields(models.Model):
    is_config_valid = models.BooleanField(
        null=True,
        verbose_name="参数设置是否正确",
        help_text="保存后自动判定格式是否正确。",
        editable=False,
    )
    config_data = SafeTextField(
        null=True,
        blank=True,
        verbose_name="参数设置",
        help_text="参数设置格式为YAML格式。",
    )

    class Meta:
        abstract = True

    def get_config(self):
        if not self.config_data:
            return {}
        else:
            return yaml.safe_load(self.config_data)

    def set_config(self, data):
        self.config_data = yaml.safe_dump(data)

    config = property(get_config, set_config)

    def save(self, *args, **kwargs):
        try:
            self.config
            self.is_config_valid = True
        except Exception as error:
            _logger.error(
                "config数据格式非法：error=%s",
                error,
            )
            self.is_config_valid = False
        return super().save(*args, **kwargs)


class WithDisplayOrderFields(models.Model):
    display_order_offset = 10000
    display_order_increment = 100

    display_order = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="显示排序",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.display_order:
            self.display_order = self.get_next_display_order()
        return super().save(*args, **kwargs)

    @classmethod
    def get_next_display_order(cls):
        display_order__max = cls.objects.aggregate(Max("display_order")).get(
            "display_order__max"
        )
        if display_order__max is None:
            return cls.display_order_offset
        else:
            return display_order__max + cls.display_order_increment


class WithJsonDataFields(models.Model):
    data_raw = SafeTextField(
        null=True,
        blank=True,
        verbose_name="数据",
        help_text="JSON格式。",
    )

    class Meta:
        abstract = True

    def get_data(self):
        if not self.data_raw:
            return {}
        else:
            return json.loads(self.data_raw)

    def set_data(self, value):
        self.data_raw = jsonutils.simple_json_dumps(value, ensure_ascii=False)

    data = property(get_data, set_data)


class WithUidFields(models.Model):

    uid = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name="唯一码",
    )

    class Meta:
        abstract = True

    @classmethod
    def uidgen(cls):
        return uuid.uuid4().hex

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = self.uidgen()
        return super().save(*args, **kwargs)


class WithSimpleNRRDStatusFields(models.Model):
    """添加简易流程状态。

    状态列表：
        NEW
        READY
        RUNNING
        DONE
    状态转化方法：
        set_new
        set_ready
        start
        set_done
    状态转化流程：
        NEW --set_ready()--> READY --start()--> RUNNING --set_done()--> DONE

    状态值：
        NEW = 0 或 None
        READY = 10
        RUNNING 20
        DONE = 30

    默认情况下：
        对象在保存时，会自动进入READY状态。

    当设置类属性is_auto_ready=False时：
        对象在保存时，不会进入READY状态。

    """

    is_auto_ready = True

    NEW = 0
    READY = 10
    RUNNING = 20
    DONE = 30
    STATUS = [
        (NEW, "新建"),
        (READY, "就绪"),
        (RUNNING, "执行中"),
        (DONE, "完成"),
    ]

    status = models.IntegerField(
        choices=STATUS,
        null=True,
        blank=True,
        verbose_name="状态",
    )
    ready_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="就绪时间",
    )
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="开始时间",
    )
    done_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="完成时间",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.status is None:
            if self.is_auto_ready:
                self.status = self.READY
            else:
                self.status = self.NEW
        if self.status == self.NEW:
            if self.ready_time is not None:
                self.ready_time = None
            if self.start_time is not None:
                self.start_time = None
            if self.done_time is not None:
                self.done_time = None
        if self.status == self.READY:
            if self.ready_time is None:
                self.ready_time = timezone.now()
            if self.start_time is not None:
                self.start_time = None
            if self.done_time is not None:
                self.done_time = None
        elif self.status == self.RUNNING:
            if self.ready_time is None:
                self.ready_time = timezone.now()
            if self.start_time is None:
                self.start_time = timezone.now()
            if self.done_time is not None:
                self.done_time = None
        elif self.status == self.DONE:
            if self.ready_time is None:
                self.ready_time = timezone.now()
            if self.start_time is None:
                self.start_time = timezone.now()
            if self.done_time is None:
                self.done_time = timezone.now()
        return super().save(*args, **kwargs)

    def set_new(self, save=True):
        self.status = self.NEW
        self.ready_time = None
        self.start_time = None
        self.done_time = None
        if self.save:
            return self.save()

    def set_ready(self, save=True):
        self.status = self.READY
        self.ready_time = timezone.now()
        self.start_time = None
        self.done_time = None
        if self.save:
            self.save()

    def start(self, save=True):
        self.status = self.RUNNING
        self.ready_time = None
        self.start_time = timezone.now()
        self.done_time = None
        if save:
            self.save()

    def set_done(self, save=True):
        self.status = self.DONE
        self.ready_time = None
        self.start_time = None
        self.done_time = timezone.now()
        if save:
            self.save()

    @property
    def is_new(self):
        return (self.status == self.NEW) or (self.status is None)

    @property
    def is_ready(self):
        return self.status == self.READY

    @property
    def is_running(self):
        return self.status == self.RUNNING

    @property
    def is_done(self):
        return self.status == self.DONE


class WithSimplePRSFStatusFields(models.Model):
    """添加简易流程状态。

    状态列表：
        待处理
        正在处理
        处理成功
        处理失败

    状态转化方法：
        start
        set_success
        set_failed
    状态转化流程：
        PENDING --start()--> RUNNING --set_success()--> SUCCESS
                                +
                                |
                                +------set_failed()---> FAILED

    状态值：
        PENDING = 0 或 None
        RUNNING = 10
        SUCCESS 20
        FAILED = 30

    完成状态：
        SUCCESS 和 FAILED 都属于完成状态，此is_done值为直。


    """

    PENDING = 0
    RUNNING = 10
    SUCCESS = 20
    FAILED = 30
    STATUS = [
        (PENDING, "待处理"),
        (RUNNING, "正在处理"),
        (SUCCESS, "处理成功"),
        (FAILED, "处理失败"),
    ]

    status = models.IntegerField(
        choices=STATUS,
        null=True,
        blank=True,
        verbose_name="状态",
    )
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="开始时间",
    )
    done_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="完成时间",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.status is None:
            self.status = self.PENDING
        if self.status == self.PENDING:
            if self.start_time is not None:
                self.start_time = None
            if self.done_time is not None:
                self.done_time = None
        if self.status == self.RUNNING:
            if self.start_time is None:
                self.start_time = timezone.now()
            if self.done_time is not None:
                self.done_time = None
        elif self.status == self.SUCCESS:
            if self.start_time is None:
                self.start_time = timezone.now()
            if self.done_time is None:
                self.done_time = timezone.now()
        elif self.status == self.FAILED:
            if self.start_time is None:
                self.start_time = timezone.now()
            if self.done_time is None:
                self.done_time = timezone.now()
        return super().save(*args, **kwargs)

    def start(self, save=True):
        self.status = self.RUNNING
        self.start_time = timezone.now()
        if save:
            self.save()

    def set_success(self, save=True):
        self.status = self.SUCCESS
        self.done_time = timezone.now()
        if save:
            self.save()

    def set_failed(self, save=True):
        self.status = self.FAILED
        self.done_time = timezone.now()
        if save:
            self.save()

    @property
    def is_pending(self):
        return (self.status == self.PENDING) or (self.status is None)

    @property
    def is_running(self):
        return self.status == self.RUNNING

    @property
    def is_success(self):
        """如果未完成，则返回None。如果成功，则返回True。如果失败，则返回False。"""
        if self.status == self.SUCCESS:
            return True
        if self.status == self.FAILED:
            return False
        return None

    @property
    def is_failed(self):
        """如果未完成，则返回None。如果成功，则返回False。如果失败，则返回True。"""
        if self.status == self.FAILED:
            return True
        if self.status == self.SUCCESS:
            return False
        return None

    @property
    def is_done(self):
        return self.status == self.SUCCESS or self.status == self.FAILED


class WithSimpleResultFields(models.Model):
    success = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_("Success"),
    )
    result_data = SafeTextField(
        null=True,
        blank=True,
        verbose_name=_("Result Data"),
    )
    error_data = SafeTextField(
        null=True,
        blank=True,
        verbose_name=_("Error Message"),
    )
    result_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Result Got Time"),
    )

    class Meta:
        abstract = True

    def clean_result(self, save=True):
        self.success = None
        self.result_data = None
        self.error_data = None
        self.result_time = None
        if save:
            self.save()

    def set_result(self, result, save=True):
        self.success = True
        self.result = result
        self.error = None
        self.result_time = timezone.now()
        if save:
            self.save()

    def set_error(self, error, save=True):
        self.success = False
        self.result = None
        self.error = BizError(error)
        self.result_time = timezone.now()
        if save:
            self.save()

    def _get_result(self):
        if not self.result_data:
            return None
        else:
            return json.loads(self.result_data)

    def _set_result(self, result):
        if result is None:
            self.result_data = None
        else:
            self.result_data = jsonutils.simple_json_dumps(result, ensure_ascii=False)

    result = property(_get_result, _set_result)

    def _get_error(self):
        if not self.error_data:
            return None
        else:
            return BizError(json.loads(self.error_data))

    def _set_error(self, error):
        if error is None:
            self.error_data = None
        else:
            self.error_data = jsonutils.simple_json_dumps(error, ensure_ascii=False)

    error = property(_get_error, _set_error)


class WithExpireTimeFields(models.Model):

    EXPIRES_UNIT_SECOND = 10
    EXPIRES_UNIT_MINUTE = 20
    EXPIRES_UNIT_HOUR = 30
    EXPIRES_UNIT_DAY = 40
    EXPIRES_UNITS = [
        (EXPIRES_UNIT_SECOND, _("Second")),
        (EXPIRES_UNIT_MINUTE, _("Minute")),
        (EXPIRES_UNIT_HOUR, _("Hour")),
        (EXPIRES_UNIT_DAY, _("Day")),
    ]
    EXPIRES_SECONDS = {
        EXPIRES_UNIT_DAY: 60 * 60 * 24,
        EXPIRES_UNIT_HOUR: 60 * 60,
        EXPIRES_UNIT_MINUTE: 60,
        EXPIRES_UNIT_SECOND: 1,
    }

    expires = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Expires"),
    )
    expires_unit = models.IntegerField(
        choices=EXPIRES_UNITS,
        default=EXPIRES_UNIT_SECOND,
        verbose_name=_("Expires Unit"),
    )
    expire_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expire Time"),
    )

    default_expires = None
    default_expires_unit = EXPIRES_UNIT_SECOND

    class Meta:
        abstract = True

    def clean_expire_time(self, save=True):
        self.expires = None
        self.expires_unit = None
        self.expire_time = None
        if save:
            self.save()

    def set_expire_time(self, expires=None, expires_unit=None, nowtime=None, save=True):
        if nowtime is None:
            nowtime = timezone.now()
        if expires is None:
            expires = self.default_expires
        if expires_unit is None:
            expires_unit = self.default_expires_unit
        self.expires = expires
        self.expires_unit = expires_unit
        self.expire_time = nowtime + datetime.timedelta(
            seconds=self.get_expire_seconds()
        )
        if save:
            self.save()

    def get_expire_seconds(self):
        multiple = self.EXPIRES_SECONDS.get(self.expires_unit, 1)
        return self.expires * multiple

    @property
    def is_expired(self):
        nowtime = timezone.now()
        if self.expire_time:
            if self.expire_time < nowtime:
                return True
        return False

    def save(self, *args, **kwargs):
        if self.expires is None:
            if self.default_expires:
                self.expires = self.default_expires
        if self.expires_unit is None:
            if self.default_expires_unit:
                self.expires_unit = self.default_expires_unit
        if self.expires:
            if self.expire_time is None:
                self.expire_time = timezone.now() + datetime.timedelta(
                    seconds=self.get_expire_seconds()
                )
        return super().save(*args, **kwargs)


class WithVisibleFields(models.Model):
    visible = models.BooleanField(
        null=True,
        verbose_name=_("Visible"),
    )
    hidden_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Hidden Time"),
    )
    visible_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Visible Time"),
    )

    class Meta:
        permissions = [
            ("set_visible", _("Allow Set Visible")),
            ("set_hidden", _("Allow Set Hidden")),
        ]
        abstract = True

    def save(self, *args, **kwargs):
        if self.visible:
            if self.hidden_time is not None:
                self.hidden_time = None
            if self.visible_time is None:
                self.visible_time = timezone.now()
        else:
            if self.hidden_time is None:
                self.hidden_time = timezone.now()
            if self.visible_time is not None:
                self.visible_time = None
        return super().save(*args, **kwargs)

    def set_hidden(self, save=True):
        self.visible = False
        if self.save:
            self.save()

    def set_visible(self, save=True):
        self.visible = True
        if self.save:
            self.save()

    def visible_display(self):
        return self.visible and "可见" or "隐藏"

    visible_display.short_description = "可见性"


class WithHotspotFields(models.Model):
    hotspot = models.BooleanField(
        null=True,
        verbose_name="是否热点",
    )
    hotspot_weight = models.IntegerField(
        null=True,
        blank=True,
        default=100,
        verbose_name="热度",
    )
    hotspot_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="设置热点时间",
    )
    non_hotspot_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="取消热点时间",
    )

    class Meta:
        permissions = [
            ("set_hotspot", "允许设置热点标记"),
            ("clean_hotspot", "允许清除热点标记"),
        ]
        abstract = True

    def save(self, *args, **kwargs):
        if self.hotspot:
            if self.hotspot_time is None:
                self.hotspot_time = timezone.now()
            if self.non_hotspot_time is not None:
                self.non_hotspot_time = None
        else:
            if self.hotspot_time is not None:
                self.hotspot_time = None
            if self.non_hotspot_time is None:
                self.non_hotspot_time = timezone.now()
        return super().save(*args, **kwargs)

    def set_hotspot(self, save=True):
        self.hotspot = True
        if save:
            self.save()

    def clear_hotspot(self, save=True):
        self.hotspot = False
        if save:
            self.save()

    def hotspot_display(self):
        return self.hotspot and "热点" or "非热点"

    hotspot_display.short_description = "热点状态"


class WithArgsKwargsFields(models.Model):
    args_raw = models.TextField(
        null=True,
        blank=True,
        verbose_name="args",
    )
    kwargs_raw = models.TextField(
        null=True,
        blank=True,
        verbose_name="kwargs",
    )

    def get_args(self):
        if not self.args_raw:
            return []
        else:
            return yaml.safe_load(self.args_raw)

    def set_args(self, args):
        if args:
            self.args_raw = yaml.safe_dump(list(args))
        else:
            self.args_raw = None

    args = property(get_args, set_args)

    def get_kwargs(self):
        if not self.kwargs_raw:
            return {}
        else:
            return yaml.safe_load(self.kwargs_raw)

    def set_kwargs(self, kwargs):
        if kwargs:
            self.kwargs_raw = yaml.safe_dump(dict(kwargs))
        else:
            self.kwargs_raw = None

    kwargs = property(get_kwargs, set_kwargs)

    class Meta:
        abstract = True


class WithHitsFields(models.Model):
    hits_tmp_value_key = "_with_hits_fields_hits_tmp_value"
    hits = models.IntegerField(
        default=0,
        verbose_name="访问量",
    )
    last_hit_time = models.DateTimeField(
        null=True, blank=True, verbose_name="最后访问时间"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if not isinstance(self.hits, int):
            using = kwargs.get("using", None)
            self.refresh_from_db(using=using, fields=["hits"])
        if hasattr(self, self.hits_tmp_value_key):
            delattr(self, self.hits_tmp_value_key)
        return result

    def hits_incr(self, save=True):
        if hasattr(self, self.hits_tmp_value_key):
            setattr(
                self,
                self.hits_tmp_value_key,
                getattr(self, self.hits_tmp_value_key) + 1,
            )
            self.hits += 1
        else:
            setattr(self, self.hits_tmp_value_key, self.hits + 1)
            self.hits = F("hits") + 1
        self.last_hit_time = timezone.now()
        if save:
            self.save()
        return self.get_hits()

    def get_hits(self):
        if isinstance(self.hits, int):
            return self.hits
        else:
            return getattr(self, self.hits_tmp_value_key)

    def hits_reset(self, save=True):
        self.hits = 0
        if hasattr(self, self.hits_tmp_value_key):
            delattr(self, self.hits_tmp_value_key)
        self.last_hit_time = None
        if save:
            self.save()


class WithCountFields(models.Model):
    count_tmp_value_key = "_with_count_fileds_count_tmp_value"
    count = models.IntegerField(
        default=0,
        verbose_name="计数",
    )
    last_count_changed_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="计数最近变动时间",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if not isinstance(self.count, int):
            using = kwargs.get("using", None)
            self.refresh_from_db(using=using, fields=["count"])
        if hasattr(self, self.count_tmp_value_key):
            delattr(self, self.count_tmp_value_key)
        return result

    def incr(self, delta=1, save=True):
        """计数器加。"""
        if hasattr(self, self.count_tmp_value_key):
            setattr(
                self,
                self.count_tmp_value_key,
                getattr(self, self.count_tmp_value_key) + delta,
            )
            self.count += delta
        else:
            setattr(self, self.count_tmp_value_key, self.count + delta)
            self.count = F("count") + delta
        self.last_count_changed_time = timezone.now()
        if save:
            self.save()
        return self.get_count()

    def decr(self, delta=1, save=True):
        """计数器减。"""
        if hasattr(self, self.count_tmp_value_key):
            setattr(
                self,
                self.count_tmp_value_key,
                getattr(self, self.count_tmp_value_key) - delta,
            )
            self.count -= delta
        else:
            setattr(self, self.count_tmp_value_key, self.count - delta)
            self.count = F("count") - delta
        self.last_count_changed_time = timezone.now()
        if save:
            self.save()
        return self.get_count()

    def get_count(self):
        if isinstance(self.count, int):
            return self.count
        else:
            return getattr(self, self.count_tmp_value_key)

    def count_reset(self, save=True):
        self.count = 0
        if hasattr(self, self.count_tmp_value_key):
            delattr(self, self.count_tmp_value_key)
        self.last_count_changed_time = None
        if save:
            self.save()


class WithUserFields(models.Model):
    user_schema: Optional[Union[str, UserBase]] = None

    class Meta:
        abstract = True

    @classmethod
    def get_user_schema(cls) -> Type[UserBase]:
        if cls.user_schema:
            user_schema = cls.user_schema
        else:
            user_schema = DJANGO_USER_SCHEMA
        if isinstance(user_schema, str):
            return importutils.import_from_string(user_schema)
        else:
            return user_schema

    def get_user(
        self,
        user_field: str,
        user_info_field: str,
    ) -> UserBase:
        UserSchema = self.get_user_schema()
        if not getattr(self, user_field):
            return None
        if not getattr(self, user_info_field):
            return UserSchema.from_str(getattr(self, user_field))
        else:
            return UserSchema.from_dict(yaml.safe_load(getattr(self, user_info_field)))

    def set_user(
        self,
        user_field,
        user_info_field,
        user: Union[
            str,
            int,
            models.Model,
            Dict,
        ],
        save=True,
    ):
        user = self.get_user_data_object(user)
        setattr(self, user_field, user.get_user_identify())
        setattr(self, user_info_field, yaml.safe_dump(user.model_dump()))
        if save:
            self.save()

    def get_user_data_object(
        self,
        user: Union[
            str,
            int,
            models.Model,
            Dict,
        ],
    ) -> UserBase:
        UserSchema = self.get_user_schema()
        if isinstance(user, str):
            user = UserSchema.from_str(user)
        elif isinstance(user, int):
            user = UserSchema.from_int(user)
        elif isinstance(user, dict):
            user = UserSchema.from_dict(user)
        elif isinstance(user, models.Model):
            user = UserSchema.from_django_user(user)
        return user


class WithOwnerFields(WithUserFields):

    owner = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_("Owner"),
    )
    owner_info_data = SafeTextField(
        null=True,
        blank=True,
        verbose_name=_("Owner Information"),
    )

    class Meta:
        abstract = True

    def get_owner(self):
        return self.get_user("owner", "owner_info_data")

    def set_owner(self, owner, save=True):
        return self.set_user("owner", "owner_info_data", owner, save=save)

    def is_owner(self, user: Union[str, UserBase]):
        user = self.get_user_data_object(user)
        uid = user.get_user_identify()
        if self.owner == uid:
            return True
        else:
            return False


class WithInitiatorFields(WithUserFields):

    initiator = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_("Initiator"),
    )
    initiator_info_data = SafeTextField(
        null=True,
        blank=True,
        verbose_name=_("Initiator Information"),
    )

    class Meta:
        abstract = True

    def get_initiator(self):
        return self.get_user("initiator", "initiator_info_data")

    def set_initiator(self, initiator, save=True):
        return self.set_user("initiator", "initiator_info_data", initiator, save=save)

    def is_initiator(self, user):
        user = self.get_user_data_object(user)
        uid = user.get_user_identify()
        if self.initiator == uid:
            return True
        else:
            return False


class WithPublishStatusFields(models.Model):
    """添加发布状态相关字段。"""

    auto_publish = False

    published = models.BooleanField(
        null=True,
        verbose_name=_("Published Status"),
    )
    published_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Published Time"),
    )
    unpublished_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Unpublished Time"),
    )

    class Meta:
        permissions = [
            ("set_published", _("Allow Publish")),
            ("set_unpublished", _("Allow Unpublish")),
        ]
        abstract = True

    def save(self, *args, **kwargs):
        if (self.published is None) and self.auto_publish and (not self.pk):
            self.published = True
        if self.published is True:
            if self.published_time is None:
                self.published_time = timezone.now()
            if self.unpublished_time is not None:
                self.unpublished_time = None
        elif self.published is False:
            if self.published_time is not None:
                self.published_time = None
            if self.unpublished_time is None:
                self.unpublished_time = timezone.now()
        else:
            if self.published_time is not None:
                self.published_time = None
            if self.unpublished_time is not None:
                self.unpublished_time = None
        return super().save(*args, **kwargs)

    def clean_publish_status(self, save=True):
        self.published = None
        self.published_time = None
        self.unpublished_time = None
        if save:
            self.save()

    def set_published(self, save=True):
        self.published = True
        self.published_time = timezone.now()
        self.unpublished_time = None
        if save:
            self.save()

    def set_unpublished(self, save=True):
        self.published = False
        self.published_time = None
        self.unpublished_time = timezone.now()
        if save:
            self.save()

    @property
    def is_published(self):
        return self.published

    def published_display(self):
        return self.published and _("Pubished") or _("Unpublished")

    published_display.short_description = _("Published Status")
