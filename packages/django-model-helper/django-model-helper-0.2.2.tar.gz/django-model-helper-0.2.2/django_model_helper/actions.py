__all__ = [
    "set_deleted_for_selected",
    "set_undeleted_for_selected",
    "set_enabled_for_selected",
    "set_disabled_for_selected",
    "set_visible_for_selected",
    "set_hidden_for_selected",
    "set_hotspot_for_selected",
    "clear_hotspot_for_selected",
    "set_published_for_selected",
    "set_unpublished_for_selected",
]


def set_deleted_for_selected(modeladmin, request, queryset):
    deleted = 0
    for item in queryset.all():
        item.set_deleted(save=False)
        item.save()
        deleted += 1
    modeladmin.message_user(
        request,
        f"已经为所选的 {deleted}个 {modeladmin.model._meta.verbose_name} 添加删除标记。",
    )


set_deleted_for_selected.allowed_permissions = ["set_deleted"]
set_deleted_for_selected.short_description = "为所选的 %(verbose_name)s 添加删除标记"


def set_undeleted_for_selected(modeladmin, request, queryset):
    deleted = 0
    for item in queryset.all():
        item.set_undeleted(save=False)
        item.save()
        deleted += 1
    modeladmin.message_user(
        request,
        f"已经清除所选 {deleted}个 {modeladmin.model._meta.verbose_name} 上的删除标记。",
    )


set_undeleted_for_selected.allowed_permissions = ["set_undeleted"]
set_undeleted_for_selected.short_description = "清除所选 %(verbose_name)s 上的删除标记"


def set_enabled_for_selected(modeladmin, request, queryset):
    enabled = 0
    for item in queryset.all():
        item.set_enabled(save=False)
        item.save()
        enabled += 1
    modeladmin.message_user(
        request,
        f"已经为所选的 {enabled}个 {modeladmin.model._meta.verbose_name} 添加启用标记。",
    )


set_enabled_for_selected.allowed_permissions = ["set_enabled"]
set_enabled_for_selected.short_description = "为所选的 %(verbose_name)s 添加启用标记"


def set_disabled_for_selected(modeladmin, request, queryset):
    disabled = 0
    for item in queryset.all():
        item.set_disabled(save=False)
        item.save()
        disabled += 1
    modeladmin.message_user(
        request,
        f"已经为所选 {disabled}个 {modeladmin.model._meta.verbose_name} 添加禁用标记。",
    )


set_disabled_for_selected.allowed_permissions = ["set_disabled"]
set_disabled_for_selected.short_description = "为所选的 %(verbose_name)s 添加禁用标记"


def set_visible_for_selected(modeladmin, request, queryset):
    changed = 0
    for item in queryset.all():
        item.set_visible(save=False)
        item.save()
        changed += 1
    modeladmin.message_user(
        request,
        f"已经为所选的 {changed}个 {modeladmin.model._meta.verbose_name} 添加可见标记。",
    )


set_visible_for_selected.allowed_permissions = ["set_visible"]
set_visible_for_selected.short_description = "为所选的 %(verbose_name)s 添加可见标记"


def set_hidden_for_selected(modeladmin, request, queryset):
    changed = 0
    for item in queryset.all():
        item.set_hidden(save=False)
        item.save()
        changed += 1
    modeladmin.message_user(
        request,
        f"已经为所选 {changed}个 {modeladmin.model._meta.verbose_name} 添加隐藏标记。",
    )


set_hidden_for_selected.allowed_permissions = ["set_hidden"]
set_hidden_for_selected.short_description = "为所选的 %(verbose_name)s 添加隐藏标记"


def set_hotspot_for_selected(modeladmin, request, queryset):
    changed = 0
    for item in queryset.all():
        item.set_hotspot(save=False)
        item.save()
        changed += 1
    modeladmin.message_user(
        request,
        f"已经为所选的 {changed}个 {modeladmin.model._meta.verbose_name} 添加热点标记。",
    )


set_hotspot_for_selected.allowed_permissions = ["set_hotspot"]
set_hotspot_for_selected.short_description = "为所选的 %(verbose_name)s 添加热点标记"


def clear_hotspot_for_selected(modeladmin, request, queryset):
    changed = 0
    for item in queryset.all():
        item.clear_hotspot(save=False)
        item.save()
        changed += 1
    modeladmin.message_user(
        request,
        f"已经清除所选 {changed}个 {modeladmin.model._meta.verbose_name} 上的热点标记。",
    )


clear_hotspot_for_selected.allowed_permissions = ["set_hidden"]
clear_hotspot_for_selected.short_description = "清除所选 %(verbose_name)s 上的热点标记"


def set_published_for_selected(modeladmin, request, queryset):
    changed = 0
    for item in queryset.all():
        item.set_published(save=False)
        item.save()
        changed += 1
    modeladmin.message_user(
        request,
        f"已经将所选的 {changed}个 {modeladmin.model._meta.verbose_name} 设置为已发布状态。",
    )


set_published_for_selected.allowed_permissions = ["set_published"]
set_published_for_selected.short_description = (
    "将所选的 %(verbose_name)s 设置为已发布状态"
)


def set_unpublished_for_selected(modeladmin, request, queryset):
    changed = 0
    for item in queryset.all():
        item.set_unpublished(save=False)
        item.save()
        changed += 1
    modeladmin.message_user(
        request,
        f"已经将所选的 {changed}个 {modeladmin.model._meta.verbose_name} 设置为未发布状态。",
    )


set_unpublished_for_selected.allowed_permissions = ["set_unpublished"]
set_unpublished_for_selected.short_description = (
    "将所选的 %(verbose_name)s 设置为未发布状态"
)
