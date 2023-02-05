from easy_tenants import tenant_context, tenant_context_disabled
from entities.models import Tenant, TenantUser
from django.conf import settings


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_tenant(self, request):
        """Get tenant saved in session request"""
        tenant_id = request.session.get("tenant_id", None)
        tenant = Tenant.objects.filter(id=tenant_id).first()
        if tenant:
            return tenant
        else:
            default_tenant = TenantUser.objects.filter(
                user=request.user, users_default_tenant=True
            ).first()
            if default_tenant:
                request.session["tenant_id"] = default_tenant.tenant.id
                return default_tenant.tenant
            else:
                new_tenant = Tenant.objects.create(
                    name=f"{request.user.username}'s Tenant", creator=request.user
                )
                new_tenant.save()
                new_default_tenant = TenantUser(
                    user=request.user, tenant=new_tenant, users_default_tenant=True
                )
                new_default_tenant.save()
                request.session["tenant_id"] = new_tenant.id
                return new_tenant

    def __call__(self, request):

        if request.path.startswith("/admin/"):
            with tenant_context_disabled():
                return self.get_response(request)

        self.tenant = self.get_tenant(request)

        if self.tenant:
            with tenant_context(self.tenant):
                request.tenant = self.tenant
                return self.get_response(request)

        return self.get_response(request)
