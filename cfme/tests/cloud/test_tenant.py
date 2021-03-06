import fauxfactory
import pytest

from cfme.cloud.provider.openstack import OpenStackProvider
from cfme.utils.log import logger
from cfme.utils.update import update

pytestmark = [pytest.mark.provider([OpenStackProvider], scope='module')]


@pytest.fixture(scope='function')
def tenant(provider, setup_provider, appliance):
    tenant = appliance.collections.cloud_tenants.create(name=fauxfactory.gen_alphanumeric(8),
                                                        provider=provider)
    yield tenant

    try:
        if tenant.exists:
            tenant.delete()
    except Exception:
        logger.warning(
            'Exception while attempting to delete tenant fixture, continuing')
    finally:
        if tenant.name in provider.mgmt.list_tenant():
            provider.mgmt.remove_tenant(tenant.name)


def test_tenant_crud(tenant):
    """ Tests tenant create and delete

    Metadata:
        test_flag: tenant

    Polarion:
        assignee: rhcf3_machine
        initialEstimate: 1/4h
    """

    with update(tenant):
        tenant.name = fauxfactory.gen_alphanumeric(8)
    tenant.wait_for_appear()
    assert tenant.exists
