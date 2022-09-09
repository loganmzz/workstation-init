#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

class KrewClient:
    def __init__(self, module):
        self.module=module
        self.bin='~/.krew/bin/kubectl-krew' #self.module.get_bin_path('~/.krew/bin/kubectl-krew', True)

    def list(self):
        _, stdout, _ = self.module.run_command(
            [
                self.bin,
                'list',
            ],
            check_rc=True,
        )
        return [plugin for plugin in stdout.split('\n') if plugin != '']

    def exists(self, name):
        founds=[plugin for plugin in self.list() if plugin == name]
        if len(founds) == 1:
            return founds[0]
        elif len(founds) == 0:
            return None
        else:
            self.module.fail_json({'msg': f'Too many plugins found with name {name}', 'state': founds})

    def install(self, name):
        return self.module.run_command(
            [
                self.bin,
                'install',
                name,
            ],
            check_rc=True,
        )

    def uninstall(self, name):
        return self.module.run_command(
            [
                self.bin,
                'uninstall',
                name,
            ],
            check_rc=True,
        )

class Params:
    def __init__(self, module):
        self.name=module.params['name']
        self.state=module.params['state']

def run_module():
    result = {
        'changed': False,
        'state': None,
    }

    module = AnsibleModule(
        argument_spec={
            'name': {
                'type': 'str',
                'required': True,
            },
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
            },
        },
    )
    params=Params(module)

    result['name']=params.name

    krew=KrewClient(module)
    result['executable']=krew.bin

    found=krew.exists(params.name)
    if params.state == 'present':
        if found == None:
            _, stdout, stderr = krew.install(params.name)
            result['stdout']=stdout
            result['stderr']=stderr
            result['changed']=True
            result['state']=krew.exists(params.name)
        else:
            result['state']=found
    elif params.state == 'absent':
        if found != None:
            rc, stdout, stderr = krew.uninstall(params.name)
            result['changed']=True
            result['old_state']=found
            result['stdout']=stdout
            result['stderr']=stderr
    else:
        module.fail_json({'msg': f'Unsupported state {params.state}', **result})

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()