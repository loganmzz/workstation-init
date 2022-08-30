#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

class VsCodeExtension:
    def __init__(self, spec):
        self.spec=spec
        splits=self.spec.split('@')
        self.id=splits[0].lower()
        self.version=splits[1] if len(splits) >= 2 else None

class VsCodeClient:
    def __init__(self, module):
        self.module=module
        self.bin=self.module.get_bin_path('code', True)

    def list_extensions(self):
        _, stdout, _ = self.module.run_command(
            [
                self.bin,
                '--list-extensions',
                '--show-versions',
            ],
            check_rc=True,
        )
        return [VsCodeExtension(spec) for spec in stdout.split('\n') if spec != '']

    def get_extension(self, id):
        founds=[ext for ext in self.list_extensions() if ext.id == id]
        if len(founds) == 1:
            return founds[0]
        elif len(founds) == 0:
            return None
        else:
            self.module.fail_json({'msg': f'Too many extensions found with id {id}', 'state': [vars(ext) for ext in founds]})

    def install_extension(self, extension):
        return self.module.run_command(
            [
                self.bin,
                '--install-extension',
                extension.spec,
            ],
            check_rc=True,
        )

    def uninstall_extension(self, extension):
        return self.module.run_command(
            [
                self.bin,
                '--uninstall-extension',
                extension.id,
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

    require=VsCodeExtension(params.name)
    result['query']=vars(require)

    vscode=VsCodeClient(module)
    result['executable']=vscode.bin

    found=vscode.get_extension(require.id)
    if params.state == 'present':
        if found == None or (require.version != None and found.version != require.version):
            _, stdout, stderr = vscode.install_extension(require)
            result['stdout']=stdout
            result['stderr']=stderr
            result['changed']=True
            result['state']=vars(vscode.get_extension(require.id))
        else:
            result['state']=vars(found)
    elif params.state == 'absent':
        if found != None:
            rc, stdout, stderr = vscode.uninstall_extension(require)
            result['changed']=True
            result['old_state']=vars(found)
            result['stdout']=stdout
            result['stderr']=stderr
    else:
        module.fail_json({'msg': f'Unsupported state {params.state}', **result})

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()