import pytest

from cfme import test_requirements
from cfme.utils.log import logger
from cfme.utils.wait import wait_for
from cfme.utils.wait import wait_for_decorator

pytestmark = [
    pytest.mark.ignore_stream("upstream"),
    test_requirements.ansible,
]


@pytest.fixture(scope='module')
def embedded_appliance(appliance):
    """Enables embedded ansible role via UI"""
    appliance.enable_embedded_ansible_role()
    assert appliance.is_embedded_ansible_running
    yield appliance
    appliance.disable_embedded_ansible_role()


@pytest.mark.tier(3)
def test_embedded_ansible_enable(embedded_appliance):
    """Tests whether the embedded ansible role and all workers have started correctly

    Polarion:
        assignee: sbulage
        casecomponent: Ansible
        caseimportance: critical
        initialEstimate: 1/6h
        tags: ansible_embed
    """
    assert wait_for(lambda: embedded_appliance.is_embedded_ansible_running, num_sec=30)
    assert wait_for(lambda: embedded_appliance.rabbitmq_server.running, num_sec=30)
    assert wait_for(lambda: embedded_appliance.nginx.running, num_sec=30)
    endpoint = "api" if embedded_appliance.is_pod else "ansibleapi"

    assert embedded_appliance.ssh_client.run_command(
        'curl -kL https://localhost/{endp} | grep "AWX REST API"'.format(endp=endpoint),
        container=embedded_appliance.ansible_pod_name)


@pytest.mark.tier(3)
def test_embedded_ansible_disable(embedded_appliance):
    """Tests whether the embedded ansible role and all workers have stopped correctly

    Polarion:
        assignee: sbulage
        casecomponent: Ansible
        caseimportance: critical
        initialEstimate: 1/6h
        tags: ansible_embed
    """
    assert wait_for(lambda: embedded_appliance.rabbitmq_server.running, num_sec=30)
    assert wait_for(lambda: embedded_appliance.nginx.running, num_sec=30)
    embedded_appliance.disable_embedded_ansible_role()

    if not embedded_appliance.is_pod:
        assert wait_for(lambda: embedded_appliance.supervisord.running,
                        fail_cond=True,
                        num_sec=180)
        assert wait_for(lambda: embedded_appliance.rabbitmq_server.running,
                        fail_cond=True,
                        num_sec=60)
        assert wait_for(lambda: embedded_appliance.nginx.running,
                        fail_cond=True,
                        num_sec=30)
    else:
        @wait_for_decorator(num_sec=300)
        def is_ansible_pod_stopped():
            # todo: implement appropriate methods in appliance
            return embedded_appliance.ssh_client.run_command(
                'oc get pods|grep ansible', ensure_host=True).failed


@pytest.mark.tier(1)
def test_embedded_ansible_event_catcher_process(embedded_appliance):
    """
    EventCatcher process is started after Ansible role is enabled (rails
    evm:status)

    Polarion:
        assignee: sbulage
        casecomponent: Ansible
        caseimportance: critical
        initialEstimate: 1/4h
        tags: ansible_embed
    """
    result = embedded_appliance.ssh_client.run_rake_command(
        "evm:status | grep 'EmbeddedAnsible'"
    ).output

    for data in result.splitlines():
        logger.info("Checking service/process %s started or not", data)
        assert "started" in data


@pytest.mark.tier(1)
def test_embedded_ansible_logs(embedded_appliance):
    """
    Separate log files should be generated for Ansible to aid debugging.
    p1 (/var/log/tower)

    Polarion:
        assignee: sbulage
        casecomponent: Ansible
        caseimportance: critical
        initialEstimate: 1/4h
        tags: ansible_embed
    """
    log_checks = [
        "callback_receiver.log",
        "dispatcher.log",
        "fact_receiver.log",
        "management_playbooks.log",
        "task_system.log",
        "tower.log",
        "tower_rbac_migrations.log",
        "tower_system_tracking_migrations.log",
    ]

    # Asserting log folder is present
    tower_log_folder = embedded_appliance.ssh_client.run_command(
        "ls /var/log/tower/"
    )
    assert tower_log_folder.success

    logs = tower_log_folder.output.splitlines()
    diff = tuple(set(logs) - set(log_checks))
    # Asserting all files except setup file.
    assert 1 == len(diff)
    # Retrieving setup log file from list and asserting with length
    # Setup log file contains date/time string in it.
    assert "setup" in diff[0]
