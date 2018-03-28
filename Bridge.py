from subprocess import call, PIPE, Popen


class Shell:
    @staticmethod
    def excute_cmd(cmd):
        err_code = call(cmd, shell=True, )
        screen = ''
        return err_code, screen


class meter:
    bridge = {'name': 'meter_bridge', 'port': ['eth1', 'eth2']}
    management = {'port': 'eth0', 'ip': '192.44.44.44'}

    def __init__(self):
        pass

    def cfg_net_bridge(self):

        if not self.is_port_installed():
            return

        if not self.add_net_bridge():
            return

        if not self.add_port_to_bridge():
            return

    def cfg_net_management(self):
        Shell.excute_cmd('sudo ifconfig %s %s up' % (meter.management['port'], meter.management['ip']))

    def add_net_bridge(self):

        # try to delete old net bridge
        Shell.excute_cmd('sudo ifconfig %s down' % meter.bridge['name'])
        Shell.excute_cmd('sudo brctl delbr %s' % meter.bridge['name'])

        err_code, screen = Shell.excute_cmd('sudo brctl addbr %s' % meter.bridge['name'])

        if 1 == err_code:
            print('add net_bridge fail')
            return False
        return True

    def add_port_to_bridge(self):
        for port in meter.bridge['port']:
            err_code, screen = Shell.excute_cmd('sudo brctl addif %s %s' % (meter.bridge['name'], port))
            if 1 == err_code:
                print('if %s add to %s is Fail ' % (port, meter.bridge['name']))

    def is_port_installed(self):
        for port in meter.bridge['port']:
            err_code, screen = Shell.excute_cmd('ifconfig %s' % port)
            if 1 == err_code:
                print('bridge port:%s is not install!' % port)
                return False
        return True


if __name__ == '__main__':
    damage_meter = meter()

    damage_meter.cfg_net_management()

    damage_meter.cfg_net_bridge()
