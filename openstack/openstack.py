from argparse import ArgumentParser


class openstack:

    def __init__(self, *args, **kwargs):
        self.args = args[0]
        self.all_data = {}
        self.__keystoneclient = None
        self.__novaclient = None

    @property
    def __NovaClient(self):
        return self.__novaclient

    @__NovaClient.getter
    def __NovaClient(self):
        if self.__novaclient is None:
            from novaclient.client import Client as NovaClient
            self.__novaclient = NovaClient(
                '2',
                self.args.username,
                self.args.password,
                self.args.tenant_name,
                self.args.auth_url)
        return self.__novaclient

    @property
    def __KeystoneClient(self):
        return self.__keystoneclient

    @__KeystoneClient.getter
    def __KeystoneClient(self):
        if self.__keystoneclient is None:
            from keystoneclient.v2_0 import client as KeystoneClient
            self.__keystoneclient = KeystoneClient.Client(
                username=self.args.username,
                password=self.args.password,
                auth_url=self.args.auth_url,
                tenant_name=self.args.tenant_name)
        return self.__keystoneclient

    def keystone(self):

        self.all_data['openstack.keystone.users.count'] = len(
            self.__KeystoneClient.users.list())
        self.all_data['openstack.keystone.tenants.count'] = len(
            self.__KeystoneClient.tenants.list())

        # Get regions count
        regions = {}
        endpoints = self.__keystoneclient.endpoints.list()
        for endpoint in endpoints:
            if not endpoint.region in regions:
                regions[endpoint.region] = 1
        self.all_data['openstack.keystone.regions.count'] = len(regions)

    def nova(self):
        self.nova_hypervisor()
        self.nova_tenants_usage()
        self.nova_services()

    def nova_hypervisor(self):
        import ast

        hypervisor_metrics = (
            'free_disk_gb',
            'free_ram_mb',
            'local_gb',
            'local_gb_used',
            'memory_mb',
            'memory_mb_used',
            'running_vms',
            'vcpus',
            'vcpus_used')
        all_hypervisor_stats = self.__NovaClient.hypervisor_stats.statistics()

        metric_str = 'openstack.allhypervisors.'
        for metric in hypervisor_metrics:
            full_metric_str = metric_str + metric
            self.all_data[full_metric_str] = getattr(
                all_hypervisor_stats, metric)

        hypervisors = self.__NovaClient.hypervisors.list()
        metric_str = 'openstack.hypervisors.'
        for hypervisor in hypervisors:
            hypervisor_name = hypervisor.hypervisor_hostname.split('.', 1)[0]

            for metric in hypervisor_metrics:
                full_metric_str = metric_str + hypervisor_name + '.' + metric
                self.all_data[full_metric_str] = getattr(hypervisor, metric)
            # state metric
            full_metric_str = metric_str + hypervisor_name + '.state'
            if hypervisor.state == 'up':
                self.all_data[full_metric_str] = 1
            else:
                self.all_data[full_metric_str] = 0
            # arch metric
            try:
                cpu_dict = ast.literal_eval(hypervisor.cpu_info)
                full_metric_str = metric_str + hypervisor_name + \
                    '.cpu_info_arch.' + cpu_dict['arch']
                self.all_data[full_metric_str] = 1
            except:
                pass

    def nova_tenants_usage(self):
        tenants_dict = {}
        tenants = self.__KeystoneClient.tenants.list()
        for tenant in tenants:
            tenants_dict[tenant.id] = tenant.name

        tenant_metrics = (
            'total_vcpus_usage',
            'total_hours',
            'total_memory_mb_usage',
            'total_local_gb_usage')
        import datetime
        now = datetime.datetime.now()
        epoch = datetime.datetime(year=1970, month=1, day=1)
        usages = self.__NovaClient.usage.list(epoch, now, detailed=True)
        metric_str = 'openstack.tenant.'
        for usage in usages:
            if usage.tenant_id not in tenants_dict:
                continue
            for metric in tenant_metrics:
                full_metric_str = metric_str + \
                    tenants_dict[usage.tenant_id] + '.' + metric
                self.all_data[full_metric_str] = getattr(usage, metric)
            full_metric_str = metric_str + \
                tenants_dict[usage.tenant_id] + '.Servers'
            self.all_data[full_metric_str] = len(usage.server_usages)

    def nova_services(self):
        services = self.__NovaClient.services.list()
        enabled = disabled = up = down = 0
        for service in services:
            if service.state == 'up':
                up += 1
            elif service.state == 'down':
                down += 1
            else:
                pass
            if service.status == 'enabled':
                enabled += 1
            elif service.status == 'disabled':
                disabled += 1
            else:
                pass
        self.all_data['openstack.nova.services.up'] = up
        self.all_data['openstack.nova.services.down'] = down
        self.all_data['openstack.nova.services.enabled'] = enabled
        self.all_data['openstack.nova.services.disabled'] = disabled

    def get_data(self):
        self.keystone()
        self.nova()
        return self.all_data

    def print_data(self):
        self.get_data()
        import time
        time_now = int(time.time())

        for key in sorted(self.all_data.keys()):
            print '{}\t{}\t{}'.format(key, self.all_data[key], time_now)


def main():
    parser = ArgumentParser()
    parser.add_argument('-u', '--username', default='admin')
    parser.add_argument('-p', '--password', default='G3rm4n1cus')
    parser.add_argument('-t', '--tenant_name', default='admin')
    parser.add_argument(
        '-a',
        '--auth_url',
        default='http://192.168.3.130:5000/v2.0')
    parser.add_argument('-S', '--service-type', default='compute')
    parser.add_argument('-H', '--host')
    args = parser.parse_args()

    obj = openstack(args)
    obj.print_data()


if __name__ == '__main__':
    main()
