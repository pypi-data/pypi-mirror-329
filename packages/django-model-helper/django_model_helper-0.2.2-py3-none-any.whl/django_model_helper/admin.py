from django.contrib import admin
from django.contrib.auth import get_permission_codename
from .actions import set_deleted_for_selected
from .actions import set_undeleted_for_selected
from .actions import set_enabled_for_selected
from .actions import set_disabled_for_selected
from .actions import set_visible_for_selected
from .actions import set_hidden_for_selected
from .actions import set_hotspot_for_selected
from .actions import clear_hotspot_for_selected
from .actions import set_published_for_selected
from .actions import set_unpublished_for_selected

__all__ = [
    "WithDeletedStatusFieldsAdmin",
    "WithEnabledStatusFieldsAdmin",
    "WithPublishStatusFieldsAdmin",
    "WithVisibleFieldsFieldsAdmin",
    "WithHotspotFieldsAdmin",
]


class WithDeletedStatusFieldsAdmin(admin.ModelAdmin):

    def has_set_deleted_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("set_deleted", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def has_set_undeleted_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("set_undeleted", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.update(
            {
                "set_deleted_for_selected": self.get_action(set_deleted_for_selected),
                "set_undeleted_for_selected": self.get_action(
                    set_undeleted_for_selected
                ),
            }
        )
        return actions


class WithEnabledStatusFieldsAdmin(admin.ModelAdmin):

    def has_set_enabled_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("set_enabled", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def has_set_disabled_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("set_disabled", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.update(
            {
                "set_enabled_for_selected": self.get_action(set_enabled_for_selected),
                "set_disabled_for_selected": self.get_action(set_disabled_for_selected),
            }
        )
        return actions


class WithVisibleFieldsFieldsAdmin(admin.ModelAdmin):

    def has_set_visible_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("set_visible", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def has_set_hidden_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("set_hidden", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.update(
            {
                "set_visible_for_selected": self.get_action(set_visible_for_selected),
                "set_hidden_for_selected": self.get_action(set_hidden_for_selected),
            }
        )
        return actions


class WithHotspotFieldsAdmin(admin.ModelAdmin):

    def has_set_hotspot_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("set_hotspot", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def has_clean_hotspot_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("clean_hotspot", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.update(
            {
                "set_hotspot_for_selected": self.get_action(set_hotspot_for_selected),
                "clear_hotspot_for_selected": self.get_action(
                    clear_hotspot_for_selected
                ),
            }
        )
        return actions


class WithPublishStatusFieldsAdmin(admin.ModelAdmin):

    def has_set_published_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("set_published", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def has_set_unpublished_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("set_unpublished", opts)
        result = request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return result

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.update(
            {
                "set_published_for_selected": self.get_action(
                    set_published_for_selected
                ),
                "set_unpublished_for_selected": self.get_action(
                    set_unpublished_for_selected
                ),
            }
        )
        return actions
