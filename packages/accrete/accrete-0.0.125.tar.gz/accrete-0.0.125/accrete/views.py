import os
from enum import Enum
from functools import wraps
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login_required
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from accrete.models import Tenant, Member
from accrete.tenant import get_tenant, tenant_has_group, member_has_group
from . import config


class GroupType(Enum):

    TENANT: str = 'tenant'
    MEMBER: str = 'member'


class TenantRequiredMixin(LoginRequiredMixin):

    TENANT_NOT_SET_URL = None
    GROUP_NOT_SET_URL = None
    TENANT_GROUPS = []
    MEMBER_GROUPS = []

    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        tenant = self.get_tenant()
        if not tenant:
            return self.handle_tenant_not_set()
        if not self.check_tenant_group():
            return self.handle_tenant_group_not_set()
        if not self.check_member_group():
            return self.handle_member_group_not_set()
        return res

    def handle_tenant_not_set(self):
        return redirect(self.get_tenant_not_set_url())

    def handle_tenant_group_not_set(self):
        return redirect(self.get_group_not_set_url(GroupType.TENANT))

    def handle_member_group_not_set(self):
        return redirect(self.get_group_not_set_url(GroupType.MEMBER))

    def get_tenant_not_set_url(self):
        tenant_not_set_url = (
                self.TENANT_NOT_SET_URL
                or settings.ACCRETE_TENANT_NOT_SET_URL
        )
        if not tenant_not_set_url:
            cls_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f"{cls_name} is missing the tenant_not_set_url attribute. "
                f"Define {cls_name}.TENANT_NOT_SET_URL, "
                f"settings.ACCRETE_TENANT_NOT_SET_URL, or override "
                f"{cls_name}.get_tenant_not_set_url()."
            )
        return tenant_not_set_url

    def get_group_not_set_url(self, group_type: GroupType):
        group_not_set_url = (
                self.GROUP_NOT_SET_URL
                or settings.ACCRETE_GROUP_NOT_SET_URL
        )
        if not group_not_set_url:
            cls_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f"{cls_name} is missing the group_not_set_url attribute. "
                f"Define {cls_name}.GROUP_NOT_SET_URL, "
                f"settings.ACCRETE_GROUP_NOT_SET_URL, or override "
                f"{cls_name}.get_group_not_set_url()."
            )
        return group_not_set_url

    def check_tenant_group(self) -> bool:
        if not self.TENANT_GROUPS:
            return True
        for group in self.TENANT_GROUPS:
            if tenant_has_group(group):
                return True
        return False

    def check_member_group(self) -> bool:
        if not self.MEMBER_GROUPS:
            return True
        for group in self.MEMBER_GROUPS:
            if member_has_group(group):
                return True
        return False

    @staticmethod
    def get_tenant():
        return get_tenant()


def tenant_required(
        tenant_groups: list[str] = None,
        member_groups: list[str] = None,
        redirect_field_name: str = None,
        login_url: str = None
):
    def decorator(f):
        @wraps(f)
        @login_required(
            redirect_field_name=redirect_field_name,
            login_url=login_url
        )
        def _wrapped_view(request, *args, **kwargs):
            tenant = request.tenant
            if not tenant:
                return redirect(config.ACCRETE_TENANT_NOT_SET_URL)
            for tenant_group in (tenant_groups or []):
                if not any([tenant_has_group(tenant_group)]):
                    return redirect(config.ACCRETE_GROUP_NOT_SET_URL)
            for member_group in (member_groups or []):
                if not any([member_has_group(member_group)]):
                    return redirect(config.ACCRETE_GROUP_NOT_SET_URL)
            return f(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@tenant_required()
def get_tenant_file(request, tenant_id, filepath):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    if not request.user.is_staff:
        member = Member.objects.filter(user=request.user, tenant=tenant)
        if not member.exists():
            return HttpResponseNotFound()
    filepath = f'{settings.MEDIA_ROOT}/{tenant_id}/{filepath}'
    if not os.path.exists(filepath):
        return HttpResponseNotFound()
    with open(filepath, 'rb') as f:
        return HttpResponse(f)
