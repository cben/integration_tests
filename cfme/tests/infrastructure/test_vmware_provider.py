# -*- coding: utf-8 -*-
"""Manual VMware Provider tests"""
import pytest


@pytest.mark.manual
@pytest.mark.tier(3)
def test_vmware_provider_filters():
    """
    N-3 filters for esx provider.
    Example: ESXi 6.5 is the current new release.
    So filters for 6.7 (n), 6.5 (n-1), 6.0 (n-2) at minimum.

    Polarion:
        assignee: kkulkarn
        casecomponent: Provisioning
        caseimportance: low
        initialEstimate: 1/4h
        testSteps:
            1.Integrate VMware provider in CFME
            2.Go to Compute->Infrastructure->Hosts
            3.Try to use preset filters
        expectedResults:
            1.
            2.All hosts are listed.
            3.We should have at least 3 filters based on VMware version.
    """
    pass


@pytest.mark.manual
@pytest.mark.tier(3)
def test_appliance_scsi_control_vmware():
    """
    Appliance cfme-vsphere-paravirtual-*.ova has SCSI controller as Para
    Virtual

    Polarion:
        assignee: kkulkarn
        casecomponent: Appliance
        caseimportance: critical
        initialEstimate: 1/4h
    #TODO: yet to test this, once done, I will add steps. Test was not written by me originally.
    """
    pass


@pytest.mark.manual
@pytest.mark.tier(1)
def test_vmware_vds_ui_display():
    """
    Virtual Distributed Switch port groups are displayed for VMs assigned
    to vds port groups.
    Compute > Infrastructure > Host > [Select host] > Properties > Network

    Polarion:
        assignee: kkulkarn
        casecomponent: Infra
        caseimportance: medium
        initialEstimate: 1/12h
        testtype: integration
        testSteps:
            1.Integrate VMware provider in CFME
            2.Compute > Infrastructure > Host > [Select host] > Properties > Network
            3.Check if host has Distributed Switch and it is displayed on this page
        expectedResults:
            1.
            2.Properties page for the host opens.
            3.If DSwitch exists it will be displayed on this page.
    """
    pass


@pytest.mark.manual
@pytest.mark.tier(1)
def test_vmware_guests_linked_clone():
    """
    VMware guests are incorrectly marked as linked_clone true, remove attribute
    VMs are incorrectly marked as Linked Clones.
    Every VM discovered from VMware provider has "linked_clone": true.
    However, none of the VMs is sharing a disk or has a snapshot.
    Ideally they shouldn't mark them all as linked_clone=t
    https://bugzilla.redhat.com/show_bug.cgi?id=1588908

    Polarion:
        assignee: kkulkarn
        casecomponent: Infra
        caseimportance: critical
        initialEstimate: 1/3h
        testtype: integration
        testSteps:
            1.Integrate VMware provider in CFME
            2.Check the total number of VMs present
            # psql -U postgres -d vmdb_production -c "select name from vms where vendor='vmware';" |
            wc -l
            3.Now, check the total number of VMs having linked_clone set as True:
            # psql -U postgres -d vmdb_production -c "select name from vms where vendor='vmware'
            and linked_clone='t';" | wc -l
        expectedResults:
            1.
            2.Should return VM count
            3.Should return VM count where linked_clone='t' and should be less than count in step2.
    """
    pass


@pytest.mark.manual
@pytest.mark.tier(1)
def test_vmware_reconfigure_vm_controller_type():
    """
    Edit any VM which is provisioned for vSphere and select "Reconfigure this VM" option.
    In "Controller Type" column we do not see the Controller Type listed.
    Controller Type should be listed.
    https://bugzilla.redhat.com/show_bug.cgi?id=1650441

    Polarion:
        assignee: kkulkarn
        casecomponent: Infra
        caseimportance: medium
        initialEstimate: 1/4h
        testtype: integration
        title: Test Controller type is listed in "Reconfigure VM Disk" Controller Type Column
        testSteps:
            1.Integrate VMware provider in CFME
            2.Navigate to Compute->Infrastructure->Virtual Machines
            3.Select a virtual machine and select Configure->Reconfigure Selected Item
            4.Check if Disks table lists controller type
        expectedResults:
            1.
            2.
            3.Reconfigure VM opion should be enabled
            4.Controller type should be listed
    """
    pass


@pytest.mark.manual
@pytest.mark.tier(1)
def test_vmware_vds_ui_tagging():
    """
    Virtual Distributed Switch port groups are displayed for VMs assigned
    to vds port groups. Check to see if you can navigate to DSwitch and tag it.
    Compute > Infrastructure > Host > [Select host] > Properties > Network

    Polarion:
        assignee: kkulkarn
        casecomponent: Infra
        caseimportance: medium
        initialEstimate: 1/12h
        testtype: integration
        testSteps:
            1.Integrate VMware provider in CFME
            2.Compute > Infrastructure > Host > [Select host] > Properties > Network
            3.Check if host has Distributed Switch and it is displayed on this page
            4.If displayed, try to select Policy->Assign Tag to DSwitch.
        expectedResults:
            1.
            2.Properties page for the host opens.
            3.If DSwitch exists it will be displayed on this page.
            4.You can assign tags to DSwitch.
    """
    pass
